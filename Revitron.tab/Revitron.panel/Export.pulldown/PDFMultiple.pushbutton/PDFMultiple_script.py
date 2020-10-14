from revitronui import PDF
from pyrevit import script
from pyrevit import forms
import sys, os

sheets = forms.select_sheets()

if not sheets:
    sys.exit()

pdf = PDF()
dirs = []

for sheet in sheets:
	
	path = pdf.export(sheet)

	if path:
		dirs.append(os.path.dirname(path))
		script.get_output().print_html(':smiling_face: Exported <em>{}</em>'.format(os.path.basename(path)))
	else:
		script.get_output().print_html(':pouting_face: Error exporting <em>{}</em>'.format(os.path.basename(path)))

dirs = list(set(dirs))

for d in dirs:
    script.show_folder_in_explorer(d)