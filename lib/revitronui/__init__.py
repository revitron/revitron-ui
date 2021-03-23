import revitron
import os
import sys
from revitron import _
from pyrevit import forms
from pyrevit import output
from collections import defaultdict


class Alert:

	def __init__(self, text):
		forms.alert(text, title='Note', ok=True, exitscript=True)


class ElementInfo:

	def __init__(self, elements):

		out = output.get_output()
		self.info = []

		for element in elements:
			
			dependents = []

			for dep in _(element).getDependent():
				depFamType = revitron.Parameter(dep, 'Family and Type').getValueString()
				depInfo = '{} {}, {}'.format(out.linkify(dep.Id), _(dep).getCategoryName(), depFamType).strip(', ')
				depInfo = depInfo + '<br>'
				dependents.append(depInfo)
				
			self.info.append([
				out.linkify(element.Id),
				_(element).getClassName(),
				_(element).getCategoryName(),
				revitron.Parameter(element, 'Family and Type').getValueString(),
				''.join(dependents)
			])

	def show(self, title = ''):

		out = output.get_output()
		out.print_table(self.info, 
						title = title, 
						columns = ['ID', 'Class', 'Category', 'Family / Type', 'Dependent'])


class DWG:
	
	def __init__(self):
		self.config = revitron.DocumentConfigStorage().get('revitron.export', defaultdict())
		try:
			self.exporter = revitron.DWGExporter(self.config.get('DWG_Export_Setup'))
		except:
			Alert('Please configure your DWG exporter first!')
		self.directory = self.config.get('Sheet_Export_Directory', False)
		if not self.directory:
			Alert('Please configure the export directory first!')
  
	def export(self, sheet):
		return self.exporter.exportSheet(sheet, 
					  					 self.directory, 
										 getattr(revitron.DB.ExportUnit, self.config.get('DWG_Export_Unit')),
						 				 self.config.get('Sheet_Naming_Template'))


class PDF:
	
	def __init__(self):
		self.config = revitron.DocumentConfigStorage().get('revitron.export', defaultdict())
		try:
			address = self.config.get('PDF_Printer_Address')
			output = self.config.get('PDF_Temporary_Output_Path')
			self.directory = self.config.get('Sheet_Export_Directory')
			self.defaultSize = self.config.get('Default_Sheet_Size')
		except:					
			Alert('Please configure your PDF exporter first!')
		if not address:
			Alert('Please configure the PDF Printer address first!')
		if not output:
			Alert('Please configure the temporary PDF output directory first!')
		if not self.directory:
			Alert('Please configure the export directory first!')
		if not self.defaultSize:
			Alert('Please configure a paper size settings first!')
		self.exporter = revitron.PDFExporter(address, output)
		self.sizeParamName = self.config.get('Sheet_Size_Parameter_Name')
		self.orientationParamName = self.config.get('Sheet_Orientation_Parameter_Name')
		self.defaultOrientation = self.config.get('Default_Sheet_Orientation')
		
	def export(self, sheet):
		
		sheetSize = False
		sheetOrientation = False

		if self.sizeParamName:
			sheetSize = _(sheet).get(self.sizeParamName)

		if self.orientationParamName:
			sheetOrientation = _(sheet).get(self.orientationParamName)
			
		if not sheetSize:
			sheetSize = self.defaultSize
			
		if not sheetOrientation:
			sheetOrientation = self.defaultOrientation

		return self.exporter.printSheet(sheet, 
										sheetSize, 
										sheetOrientation, 
										self.directory, 
										self.config.get('Sheet_Naming_Template')
										)


class SelectType:
	
	def __init__(self, elementTypes, title):
		self.title = title
		self.options = []
		for elementType in elementTypes:
			self.options.append(OptionListTypes(elementType))
	
	def show(self, multiselect=False):
		return forms.SelectFromList.show(self.options,
										 title=self.title,
										 multiselect=multiselect,
										 button_name='Select Type')
	
	
class OptionListTypes(forms.TemplateListItem):
	
	@property
	def name(self):
		return revitron.ParameterTemplate(self.item, '{Family Name} - {Type Name}', False).render()


class RoomTags():

	@staticmethod
	def add(method, title):
		roomTagTypes = revitron.Filter().byCategory('Room Tags').onlyTypes().getElements()
		roomTagType = SelectType(roomTagTypes, title).show()
		scope = revitron.Selection.get()
		if not scope:
			scope = revitron.ACTIVE_VIEW.Id
		if roomTagType:
			rooms = revitron.Filter(scope).byCategory('Rooms').noTypes().getElements()
			max_value = len(rooms)
			counter = 0
			with forms.ProgressBar(title='Tagging rooms ... ({value} of {max_value})') as pb:
				for room in rooms:
					counter = counter + 1
					try:
						method(room, roomTagType.Id)
					except:
						pass
					pb.update_progress(counter, max_value)