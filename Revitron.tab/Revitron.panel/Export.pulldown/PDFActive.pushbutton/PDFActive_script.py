import revitron
from revitron import _
from revitronui import PDF
from pyrevit import script
from pyrevit import forms
import sys, os

sheet = revitron.ACTIVE_VIEW

if _(sheet).getClassName() == 'ViewSheet':
	pdf = PDF()
	path = pdf.export(sheet)
	if path:
		script.get_output().print_html(':smiling_face: Exported <em>{}</em>'.format(os.path.basename(path)))
		script.show_folder_in_explorer(os.path.dirname(path))
	else:
		script.get_output().print_html(':pouting_face: Error exporting')


