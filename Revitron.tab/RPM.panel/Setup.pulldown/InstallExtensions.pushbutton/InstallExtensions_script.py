# -*- coding: utf-8 -*-
"""
Install all extensions defined for this project. You can define extensions for this project in the "Project Setup". 
"""
import revitron
from rpm.system.ui import UI
import os
import rpm
from pyrevit.coreutils import logger
from pyrevit import script


mlogger = logger.get_logger(__name__)

if not revitron.Document().isFamily():

	out = script.get_output()
	UI.printLogo()
	UI.printTitle()
	out.print_html('Removing registered extensions')

	extManager = rpm.ExtensionsManager()
	extManager.removeAll()

	out.print_html('Getting project dependencies<br>')
	lines = revitron.DocumentConfigStorage().get('rpm.extensions', '').split('\r\n')

	for line in lines:
		
		items = line.split('\t')
		
		try:
			extType = items[0].strip()
			extRepo = items[1].strip()
			extName = os.path.basename(extRepo).replace('.git', '')
			out.print_html('Installing {}'.format(extName))
			extManager.install(extName, extRepo, extType)
		except:
			try:
				mlogger.error('Installing {} failed'.format(extName))
			except:
				pass
	
	out.print_html('<br>Installation has finished. Reloading ...')
	rpm.system.Session.reload()
