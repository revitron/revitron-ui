import revitron
from revitron import _
from collections import defaultdict

config = revitron.DocumentConfigStorage().get('revitron.export', defaultdict())
setup = config.get('DWG_Export_Setup')
exporter = revitron.DWGExporter(setup)

sheets = revitron.Selection().get()

if not sheets:
    sheets = [revitron.ACTIVEVIEW]

for sheet in sheets:
	exporter.exportSheet(sheet, 
                      	 config.get('Sheet_Export_Directory'), 
						 config.get('Sheet_Naming_Template'))
