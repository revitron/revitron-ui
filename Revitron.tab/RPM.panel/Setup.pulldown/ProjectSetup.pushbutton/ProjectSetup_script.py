# -*- coding: utf-8 -*-
"""
Define extensions to be used with this Revit model. Defined extensions can be installed by using the "Install Extensions" button. 
"""
import revitron
import System.Windows
from pyrevit import script
from rpw.ui.forms import FlexForm, TextBox, Button, Label


def openHelp(sender, e):
	script.open_url('https://revitron-ui.readthedocs.io/en/latest/tools/rpm.html')


if not revitron.Document().isFamily():

	config = revitron.DocumentConfigStorage().get('rpm.extensions')

	components = [
	    Label(
	        'You can define a list of pyRevit extensions to be used with the currently active model.\n'
	        'That list will be stored in the project information and therefore can be easily distributed\n'
	        'among other team members to easly create a common work environment.\n'
	        'To install or switch to the extension saved with your project just hit the "Install Extensions" button.\n\n'
	        'Enter one extension per line providing the type of the extension ("ui" or "lib")\n'
	        'and the repository URL separated by a TAB as follows:',
	        FontSize=14,
	        Height=140,
	        Width=650
	    ),
	    Label(
	        'ui	https://ui-extension-repository.git\r\nlib	https://lib-extension-repository.git',
	        FontFamily=System.Windows.Media.FontFamily('Consolas'),
	        FontSize=14,
	        Height=50,
	        Width=650
	    ),
	    TextBox(
	        'extensions',
	        Text=config,
	        TextWrapping=System.Windows.TextWrapping.Wrap,
	        AcceptsTab=True,
	        AcceptsReturn=True,
	        Multiline=True,
	        Height=200,
	        Width=650,
	        FontFamily=System.Windows.Media.FontFamily('Consolas'),
	        FontSize=14
	    ),
	    Button('Open Documentation',
	           on_click=openHelp,
	           Width=650),
	    Button('Save',
	           Width=650)
	]

	form = FlexForm('Project Extensions', components)
	form.show()

	if 'extensions' in form.values:
		revitron.DocumentConfigStorage().set(
		    'rpm.extensions',
		    form.values.get('extensions')
		)
