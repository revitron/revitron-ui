import revitron
from revitron import _
from collections import defaultdict


class DWG:

	def __init__(self):
		import revitronui
		self.config = revitron.DocumentConfigStorage().get(
		    'revitron.export',
		    defaultdict()
		)
		try:
			self.exporter = revitron.DWGExporter(self.config.get('DWG_Export_Setup'))
		except:
			revitronui.Alert('Please configure your DWG exporter first!')
		self.directory = self.config.get('Sheet_Export_Directory', False)
		if not self.directory:
			revitronui.Alert('Please configure the export directory first!')

	def export(self, sheet):
		return self.exporter.exportSheet(
		    sheet,
		    self.directory,
		    getattr(revitron.DB.ExportUnit,
		            self.config.get('DWG_Export_Unit')),
		    self.config.get('Sheet_Naming_Template')
		)


class PDF:

	def __init__(self):
		import revitronui
		self.config = revitron.DocumentConfigStorage().get(
		    'revitron.export',
		    defaultdict()
		)
		try:
			address = self.config.get('PDF_Printer_Address')
			output = self.config.get('PDF_Temporary_Output_Path')
			self.directory = self.config.get('Sheet_Export_Directory')
			self.defaultSize = self.config.get('Default_Sheet_Size')
		except:
			revitronui.Alert('Please configure your PDF exporter first!')
		if not address:
			revitronui.Alert('Please configure the PDF Printer address first!')
		if not output:
			revitronui.Alert('Please configure the temporary PDF output directory first!')
		if not self.directory:
			revitronui.Alert('Please configure the export directory first!')
		if not self.defaultSize:
			revitronui.Alert('Please configure a paper size settings first!')
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

		return self.exporter.printSheet(
		    sheet,
		    sheetSize,
		    sheetOrientation,
		    self.directory,
		    self.config.get('Sheet_Naming_Template')
		)
