# -*- coding: utf-8 -*-
"""
Define extensions to be used with this Revit model. Defined extensions can be installed by using the "Install Extensions" button. 
"""
import revitron
import System.Windows
from rpw.ui.forms import FlexForm, TextBox, Button, Label


if not revitron.Document().isFamily():

	config = revitron.DocumentConfigStorage().get('rpm.extensions')
	
	components = [
			Label('Enter one extension per line like this (note the tab after the extension type):', Width=600),   
			Label('"ui   ⇥  https://repository.git" for UI extensions or\r\n"lib  ⇥  https://repository.git" for libraries', Height=50, Width=600),
			TextBox('extensions', Text=config, TextWrapping=System.Windows.TextWrapping.Wrap, AcceptsTab=True, AcceptsReturn=True, Multiline=True, Height=200, Width=600),
			Button('Save', Width=100, HorizontalAlignment=System.Windows.HorizontalAlignment.Right)
	]
	
	form = FlexForm('RPM Extensions', components)
	form.show()
		
	if 'extensions' in form.values:
		revitron.DocumentConfigStorage().set('rpm.extensions', form.values.get('extensions'))
		