import revitron
import os
import sys
from revitron import _
from pyrevit import forms
from pyrevit import output
from collections import defaultdict


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
		if not self.config:
			print('Please configure your DWG exporter first!')
			sys.exit()
		setup = self.config.get('DWG_Export_Setup')
		self.exporter = revitron.DWGExporter(setup)
  
	def export(self, sheet):
		return self.exporter.exportSheet(sheet, 
					  					 self.config.get('Sheet_Export_Directory'), 
						 				 self.config.get('Sheet_Naming_Template'))


class PDF:
	
	def __init__(self):
		self.config = revitron.DocumentConfigStorage().get('revitron.export', defaultdict())
		if not self.config:
			print('Please configure your PDF exporter first!')
			sys.exit()
		self.exporter = revitron.PDFExporter(self.config.get('PDF_Printer_Address'), self.config.get('PDF_Temporary_Output_Path'))
		self.sizeParamName = self.config.get('Sheet_Size_Parameter_Name')
		self.defaultSize = self.config.get('Default_Sheet_Size')
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
										self.config.get('Sheet_Export_Directory'), 
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
					method(room, roomTagType.Id)
					pb.update_progress(counter, max_value)