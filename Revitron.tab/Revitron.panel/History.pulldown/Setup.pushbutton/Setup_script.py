import revitron
import sys
from pyrevit import forms

if not forms.check_workshared(revitron.DOC):
	sys.exit()

config = revitron.DocumentConfigStorage().get('revitron.history', dict())
sqliteFile = config.get('file', '')

msg = """Logging transactions is enabled for this Revit model. The following database is used:

{}"""

def selectFile(): 
	sqliteFile = forms.save_file(file_ext='sqlite',
								default_name='{}.sqlite'.format(revitron.DOC.Title),
								unc_paths=False)
	if sqliteFile:
		revitron.DocumentConfigStorage().set('revitron.history', {'file': sqliteFile})

res = None
optionChange = 'Change database'
optionDisable = 'Disable logging'
optionCancel = 'Keep settings and close'

if not sqliteFile:
	selectFile()
else:
	res = forms.alert(msg.format(sqliteFile),
					  options=[optionChange, optionDisable, optionCancel])

if res == optionChange:
	selectFile()
