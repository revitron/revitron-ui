from rpm.system.ui import UI
from rpm.system.update import Update 
from rpm.system.session import Session
from pyrevit import script

out = script.get_output()
UI.printLogo()
UI.printTitle()
Update.extensions(True)
out.print_html('<br><br>Update has finished. Reloading ...<br><br>')
Session.reload() 