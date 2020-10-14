import revitron
from revitron import _
from revitronui import DWG
from pyrevit import script
from pyrevit import forms
import sys, os

sheet = revitron.ACTIVEVIEW

if _(sheet).getClassName() == 'ViewSheet':
	dwg = DWG()
	path = dwg.export(sheet)
	if path:
		script.get_output().print_html(':smiling_face: Exported <em>{}</em>'.format(os.path.basename(path)))
		script.show_folder_in_explorer(os.path.dirname(path))
	else:
		script.get_output().print_html(':pouting_face: Error exporting <em>{}</em>'.format(os.path.basename(path)))