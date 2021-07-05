import revitron
from rpm.extensions import ExtensionsManager
from pyrevit import forms

forms.alert(
	'Saving the list of currently installed extensions as the new project '
	'setup will overwrite the existing setup! '
	'Are you sure to continue?',
	yes=True, no=True, exitscript=True
)

manager = ExtensionsManager()
installed = manager.getInstalled()
configContent = ''

for extension in installed.values():
	configContent += '{}\t{}\n'.format(extension['type'], extension['repo']) 

revitron.DocumentConfigStorage().set('rpm.extensions', configContent)