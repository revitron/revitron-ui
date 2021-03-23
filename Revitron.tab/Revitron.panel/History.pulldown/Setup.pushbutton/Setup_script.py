import revitron
import sys
from pyrevit import forms

if not forms.check_workshared(revitron.DOC):
	sys.exit()

config = revitron.DocumentConfigStorage().get('revitron.history', dict())
sqliteFile = config.get('file', '')

msgDisabled = """Logging transactions is disabled for this Revit model. Select or create a database to enable logging."""

msgEnabled = """Logging transactions is enabled for this Revit model. The following database is used:

{}"""

def alertReopen():
	forms.alert('Note that changes won\'t take effect until the current file is closed and reopened again.')

res = None
optionSelect = 'Select or create database'
optionDisable = 'Disable logging'
optionCancel = 'Close'

if not sqliteFile:
	res = forms.alert(msgDisabled, options=[optionSelect, optionCancel])
else:
	res = forms.alert(msgEnabled.format(sqliteFile), options=[optionSelect, optionDisable, optionCancel])

if res == optionSelect:
	sqliteFile = forms.save_file(file_ext='sqlite',
								default_name='{}.sqlite'.format(revitron.DOC.Title),
								unc_paths=False)
	if sqliteFile:
		revitron.DocumentConfigStorage().set('revitron.history', {'file': sqliteFile})
		alertReopen()

if res == optionDisable:
	revitron.DocumentConfigStorage().set('revitron.history', dict())
	alertReopen()
