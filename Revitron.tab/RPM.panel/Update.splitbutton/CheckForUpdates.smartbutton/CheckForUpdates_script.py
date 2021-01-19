import os
from rpm.system.ui import UI
from rpm.system.update import Update
from pyrevit.coreutils.ribbon import ICON_LARGE
from pyrevit import forms

__context__ = 'zero-doc'

def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
	if os.system('git --version') != 0:
		return False
	if Update.checkPyRevit() or Update.checkExtensions():
		ui_button_cmp.set_title('Install\nUpdates')
		update_icon = script_cmp.get_bundle_file('icon-has-updates.png')
		ui_button_cmp.set_icon(update_icon, icon_size=ICON_LARGE)
		forms.alert('There are some pyRevit updates ready to be installed.\n\n'
					'Please run "Revitron > RPM > Install Updates" to update pyRevit and extensions.',
					title = 'pyRevit Updates',
					options = ['Ok, I got it!'])
	return True

if __name__ == '__main__':
	UI.checkUpdates(True)
