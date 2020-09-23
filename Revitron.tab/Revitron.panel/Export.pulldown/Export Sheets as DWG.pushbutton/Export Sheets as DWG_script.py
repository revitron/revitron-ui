import revitron
import os
from revitron import _
from pyrevit import script
from collections import defaultdict

config = revitron.DocumentConfigStorage().get('revitron.export', defaultdict())
setup = config.get('DWG_Export_Setup')
exporter = revitron.DWGExporter(setup)

sheets = revitron.Selection().get()

if not sheets:
    sheets = [revitron.ACTIVEVIEW]

dirs = []

for sheet in sheets:
	path = exporter.exportSheet(sheet, 
                      		    config.get('Sheet_Export_Directory'), 
						 	    config.get('Sheet_Naming_Template'))
	if path:
		dirs.append(os.path.dirname(path))
		script.get_output().print_html(':smiling_face: Exported <em>{}</em>'.format(os.path.basename(path)))
	else:
		script.get_output().print_html(':pouting_face: Error exporting <em>{}</em>'.format(os.path.basename(path)))

dirs = list(set(dirs))

for d in dirs:
    script.show_folder_in_explorer(d)