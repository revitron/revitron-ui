#-*- coding: UTF-8 -*-
import revitron
import System
import datetime
import re
import os
import os.path
import collections
import json
import logging
from revitronui.history.database import HistoryDatabase
from System import EventHandler
from Autodesk.Revit.DB.Events import DocumentChangedEventArgs
from Autodesk.Revit.DB.Events import DocumentOpenedEventArgs
from Autodesk.Revit.DB.Events import DocumentSynchronizingWithCentralEventArgs
from Autodesk.Revit.DB.Events import DocumentSynchronizedWithCentralEventArgs
from Autodesk.Revit.DB.Events import DocumentSavedEventArgs


class HistoryDocUtils:

	def __init__(self, doc):
		revitron.DOC = doc

	def getDumpFilePath(self):
		return os.path.join(
		    os.path.dirname(revitron.DOC.PathName),
		    '{}.dump.json'.format(revitron.DOC.Title)
		)

	def getFileSize(self):
		try:
			return self.bytes2MB(os.path.getsize(revitron.DOC.PathName))
		except:
			return ''

	def bytes2MB(self, byte):
		return float(byte) / 1024 / 1024

	def deleteDumpFile(self):
		if os.path.exists(self.getDumpFilePath()):
			try:
				os.remove(self.getDumpFilePath())
			except:
				pass

	def getSqliteFile(self):
		config = revitron.DocumentConfigStorage().get('revitron.history', dict())
		return config.get('file', '')

	def isTrackedProject(self):
		return (self.getSqliteFile() != '')


class HistoryEventHandler:

	def __init__(self):

		self.user = os.getenv('username')
		self.app = __revit__.Application
		self.activeDocs = dict()
		self.eventHandlersRegistered = False
		self.debugging = False

		# Note that the transactions names should be taken from the database, since they are modified (see below).
		self.igonredTransactions = [
		    'Reload Latest', 'VisibilityGraphics', 'Do Not Crop View', 'Crop View',
		    'HideIsolate', 'Temporary HideIsolate', 'Selection Box',
		    'Temporary View Properties', 'Cleanup Worksets', 'Filter'
		]

		self.app.DocumentOpened += EventHandler[DocumentOpenedEventArgs](self.onOpened)

	def debug(self, text):
		if self.debugging:
			doc = self.getCurrentlyActiveDoc()
			debugDir = os.path.dirname(HistoryDocUtils(doc).getSqliteFile())
			if not os.path.exists(debugDir):
				os.makedirs(debugDir)
			file = os.path.join(
			    debugDir, '{}.history.log'.format(self.getCurrentlyActiveDocTitle())
			)
			logging.basicConfig(filename=file, level=logging.DEBUG)
			logging.debug(text)

	def getCurrentlyActiveDoc(self):
		return __revit__.ActiveUIDocument.Document

	def getCurrentlyActiveDocTitle(self):
		return __revit__.ActiveUIDocument.Document.Title

	def docDict(self):
		docDict = dict()
		docDict['elements'] = collections.OrderedDict()
		return docDict

	def elemDict(self):
		elem = dict()
		elem['transactions'] = []
		return elem

	def timestamp(self):
		return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

	def uniqueList(self, l):
		seen = set()
		seenAdd = seen.add
		return [x for x in l if not (x in seen or seenAdd(x))]

	def sanitize(self, string):
		if string:
			string = string.replace('ü', 'ue')
			string = string.replace('Ü', 'Ue')
			string = string.replace('ö', 'oe')
			string = string.replace('Ö', 'Oe')
			string = string.replace('ä', 'ae')
			string = string.replace('Ä', 'Ae')
			string = re.sub('[^a-zA-Z0-9_\-\s]', '', string)
			return string
		return ''

	def onSynced(self, sender, args):

		if str(args.Status) == 'Succeeded':

			doc = self.getCurrentlyActiveDoc()
			hdu = HistoryDocUtils(doc)

			if hdu.isTrackedProject():

				if doc.PathName in self.activeDocs:

					self.activeDocs[doc.PathName]['finishTime'] = self.timestamp()
					self.activeDocs[doc.PathName]['size'] = hdu.getFileSize()

					data = self.activeDocs[doc.PathName]
					db = HistoryDatabase(hdu.getSqliteFile())

					self.debug('Writing to sync data')
					syncId = db.sync({
					    'startTime': data['startTime'],
					    'finishTime': data['finishTime'],
					    'size': data['size'],
					    'user': data['user']
					})

					self.debug('Writing to transaction data')
					rows = []
					for elemId in data['elements']:
						row = dict()
						row['elementId'] = elemId
						row['transactions'] = json.dumps(
						    data['elements'][elemId]['transactions']
						)
						# Add current Type to change type event.
						try:
							elem = doc.GetElement(revitron.DB.ElementId(int(elemId)))
							if elem:
								row['transactions'] = row['transactions'].replace(
								    'Change Type', 'Change Type to ' +
								    revitron.Parameter(elem,
								                       'Family and Type').getValueString()
								)
						except:
							pass
						rows.append(row)

					db.transactions(rows, syncId)

					# Reset lists
					del self.activeDocs[doc.PathName]
					# Delete dump file
					hdu.deleteDumpFile()
					self.debug('Synced')

		else:

			self.debug('Syncing failed or cancelled')

	def onSyncing(self, sender, args):

		doc = __revit__.ActiveUIDocument.Document
		hdu = HistoryDocUtils(doc)

		if hdu.isTrackedProject() and doc.PathName is not None:

			self.debug('Start syncing')

			if doc.PathName not in self.activeDocs:
				self.activeDocs[doc.PathName] = self.docDict()

			self.activeDocs[doc.PathName]['startTime'] = self.timestamp()
			self.activeDocs[doc.PathName]['user'] = self.user

	def onChanged(self, sender, args):

		doc = self.getCurrentlyActiveDoc()
		hdu = HistoryDocUtils(doc)

		if hdu.isTrackedProject() and doc.PathName is not None:

			transactions = self.sanitize(', '.join(list(set(args.GetTransactionNames()))))

			if transactions not in self.igonredTransactions:

				if doc.PathName not in self.activeDocs:
					self.activeDocs[doc.PathName] = self.docDict()

				elements = self.activeDocs[doc.PathName]['elements']

				for id in args.GetAddedElementIds():
					idStr = id.ToString()
					if idStr not in elements:
						elements[idStr] = self.elemDict()
					elements[idStr]['transactions'].append('added')

				for id in args.GetModifiedElementIds():
					idStr = id.ToString()
					if idStr not in elements:
						elements[idStr] = self.elemDict()
					elements[idStr]['transactions'].append(transactions)
					# Make list unique.
					elements[idStr]['transactions'] = self.uniqueList(
					    elements[idStr]['transactions']
					)

				for id in args.GetDeletedElementIds():
					idStr = id.ToString()
					if idStr not in elements:
						elements[idStr] = self.elemDict()
					elements[idStr]['transactions'].append('deleted')

				self.activeDocs[doc.PathName]['elements'] = elements

	def onSaved(self, sender, args):

		doc = self.getCurrentlyActiveDoc()
		hdu = HistoryDocUtils(doc)

		if hdu.isTrackedProject() and doc.PathName is not None:
			self.debug('Saving ' + doc.PathName)
			self.debug('Saving dump file ' + hdu.getDumpFilePath())
			if not doc.PathName in self.activeDocs:
				self.activeDocs[doc.PathName] = self.docDict()
			jsonElements = json.dumps(self.activeDocs[doc.PathName]['elements'])
			dumpFile = open(hdu.getDumpFilePath(), 'w')
			dumpFile.write(jsonElements)
			dumpFile.close()

	def onOpened(self, sender, args):

		doc = args.Document
		hdu = HistoryDocUtils(doc)
		self.debug('Open ' + doc.PathName)

		if hdu.isTrackedProject():

			if os.path.exists(hdu.getDumpFilePath()):

				cDateDump = os.path.getctime(hdu.getDumpFilePath())
				cDateLocal = os.path.getctime(doc.PathName.replace('.rvt', '_backup'))

				# Ignore and delete dump file when a new local was created.
				if cDateLocal <= cDateDump:

					dumpFile = open(hdu.getDumpFilePath())
					elements = dumpFile.read()
					dumpFile.close()
					self.activeDocs[doc.PathName] = self.docDict()
					self.activeDocs[doc.PathName]['elements'] = json.loads(elements)
					self.debug('Loading dump file')

				else:
					self.debug(
					    'Local file is newer than dump file. Deleting ' +
					    hdu.getDumpFilePath()
					)
					hdu.deleteDumpFile()

		# Check if events are registered already when opening a second model.
		if not self.eventHandlersRegistered:
			if hdu.isTrackedProject():
				self.debug('Registering event handlers')
				self.app.DocumentChanged += EventHandler[DocumentChangedEventArgs](
				    self.onChanged
				)
				self.app.DocumentSynchronizingWithCentral += EventHandler[
				    DocumentSynchronizingWithCentralEventArgs](self.onSyncing)
				self.app.DocumentSynchronizedWithCentral += EventHandler[
				    DocumentSynchronizedWithCentralEventArgs](self.onSynced)
				self.app.DocumentSaved += EventHandler[DocumentSavedEventArgs](
				    self.onSaved
				)
				self.eventHandlersRegistered = True
