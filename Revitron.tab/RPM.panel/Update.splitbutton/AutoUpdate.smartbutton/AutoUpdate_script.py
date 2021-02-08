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

template = r"""
@echo off

set pwd=%CD%
set pyrevit={}
set extensions={}
set log="C:\temp\pyRevitUpdate.log"

echo %DATE% >%log% 2>&1
echo %TIME% >>%log% 2>&1

call :pull %pyrevit% >>%log% 2>&1

cd "%extensions%"

for /D %%d in (*) do (
	if exist "%%d\.git" (
		call :pull %extensions%\%%d >>%log% 2>&1
	)
)

cd %pwd%

goto:end

:pull
echo:
cd %1
echo %1
set "status="
for /f "delims=" %%s in ('git status --porcelain') do set status=%%s
if not "%status%" == "" (
	echo Working copy is dirty - skipping
) else (
	git pull
)
cd ..

:end
"""

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
		f.write(template.format(config.RPM_PYREVIT_DIR, config.RPM_EXTENSIONS_DIR))
		f.close()
		setIcon(True)
