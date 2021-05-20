from revitronui import PDF
from pyrevit import script
from pyrevit import forms
import sys, os

pdf = PDF()
sheets = forms.select_sheets()

if not sheets:
	sys.exit()

dirs = []

max_value = len(sheets)
counter = 1

with forms.ProgressBar(title='Exporting PDF ... ({value} of {max_value})') as pb:
	for sheet in sheets:	
		counter = counter + 1
		path = pdf.export(sheet)
		if path:
			dirs.append(os.path.dirname(path))
		else:
			script.get_output().print_html(':pouting_face: Error exporting')
		pb.update_progress(counter, max_value)

dirs = list(set(dirs))

for d in dirs:
	script.show_folder_in_explorer(d)