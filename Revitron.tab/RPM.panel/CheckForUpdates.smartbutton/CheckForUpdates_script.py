"""
Check for pyRevit core and extension updates and optionally install them. 
"""
import os
from rpm.system.ui import UI
from pyrevit.coreutils.ribbon import ICON_LARGE

__context__ = 'zero-doc'

def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
	if os.system('git --version') != 0:
		return False
	if UI.checkUpdates():
		ui_button_cmp.set_title('Install\nUpdates')
		update_icon = script_cmp.get_bundle_file('icon-has-updates.png')
		ui_button_cmp.set_icon(update_icon, icon_size=ICON_LARGE)
	return True

if __name__ == '__main__':
	UI.checkUpdates(True)
