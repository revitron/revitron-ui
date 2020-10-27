from rpm.system.ui import UI
from rpm.system.update import Update 
from rpm.system.session import Session
from pyrevit import script
from pyrevit import forms


update = 'Discard all changes and update now'
cancel = 'Cancel'
res = forms.alert('Updating will discard all local changes in your extension repositories!',
				  title = 'Force Extension Update',
				  options = [update, cancel])

if res == update:
	out = script.get_output()
	UI.printLogo()
	UI.printTitle()
	Update.extensions(True)
	out.print_html('<br><br>Update has finished. Reloading ...<br><br>')
	Session.reload() 