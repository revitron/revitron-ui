from revitronui import CSV
from pyrevit import script
from pyrevit import forms
import sys, os

csv = CSV()
schedules = forms.select_schedules()

if not schedules:
	sys.exit()

dirs = []

max_value = len(schedules)
counter = 1

with forms.ProgressBar(title='Exporting CSV ... ({value} of {max_value})') as pb:
	for schedule in schedules:
		counter = counter + 1
		path = csv.export(schedule)
		if path:
			dirs.append(os.path.dirname(path))
		else:
			script.get_output().print_html(':pouting_face: Error exporting')
		pb.update_progress(counter, max_value)

dirs = list(set(dirs))

for d in dirs:
	script.show_folder_in_explorer(d)