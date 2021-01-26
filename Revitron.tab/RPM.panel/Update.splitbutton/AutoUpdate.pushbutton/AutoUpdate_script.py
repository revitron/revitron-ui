import os
from rpm import config
from rpm.system.ui import UI
from rpm.system.update import Update
from pyrevit.coreutils.ribbon import ICON_LARGE
from pyrevit.coreutils.ribbon import get_current_ui
from pyrevit import EXEC_PARAMS
from pyrevit import script
from _winreg import EnumValue, OpenKey, HKEY_CURRENT_USER, KEY_READ

__context__ = 'zero-doc'

def getBundleFile(name):
    return os.path.join(EXEC_PARAMS.command_path, name)

def getButton():
    tabs = get_current_ui().get_pyrevit_tabs()
    for tab in tabs:
        button = tab.find_child(EXEC_PARAMS.command_name)
        if button:
            return button
    return None

def setIcon(state):
	uibutton = getButton()
	if state:
		uibutton.set_icon(getBundleFile('on.png'), icon_size=ICON_LARGE)
	else:
		uibutton.set_icon(getBundleFile('icon.png'), icon_size=ICON_LARGE)

def getStartUpFolder():
	shellFolders = OpenKey(HKEY_CURRENT_USER, 
						'Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders', 
						0, 
						KEY_READ)
	try:
		count = 0
		while True:
			name, value, type = EnumValue(shellFolders, count) 
			if name == 'Startup':
				return value
			count = count + 1
	except WindowsError:
		pass

startUpFolder = getStartUpFolder()
autoUpdateFile = os.path.join(startUpFolder, 'pyRevitAutoUpdate.bat')

def __selfinit__(script_cmp, ui_button_cmp, __rvt__):
	if os.system('git --version') != 0:
		return False
	if os.path.isfile(autoUpdateFile):
		update_icon = script_cmp.get_bundle_file('on.png')
		ui_button_cmp.set_icon(update_icon, icon_size=ICON_LARGE)
		
	return True

if __name__ == '__main__':
	if os.path.isfile(autoUpdateFile):
		os.remove(autoUpdateFile)
		setIcon(False)
	else:
		f = open(autoUpdateFile, 'w')
		f.write('call {}\AutoUpdate.bat {} {}'.format(
			os.path.dirname(__file__), 
			config.RPM_PYREVIT_DIR, 
			config.RPM_EXTENSIONS_DIR))
		f.close()
		setIcon(True)
