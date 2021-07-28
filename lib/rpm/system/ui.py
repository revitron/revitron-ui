from pyrevit import script
from pyrevit import output
from pyrevit import forms
from rpm import config
from rpm.system.update import Update
from rpm.system.session import Session


class UI:

	@staticmethod
	def checkUpdates(noInteraction=False):

		hasUpdates = False
		out = script.get_output()
		pyRevit = Update.checkPyRevit()
		extensions = Update.checkExtensions()

		if pyRevit:
			install = 'Close open Revit sessions and install pyRevit core update now'
			skip = 'Skip update and keep Revit sessions open'
			res = forms.alert(
			    'A pyRevit core update is ready to be installed.\n'
			    'Note that all running Revit sessions will be closed automatically when installing the update.',
			    title='pyRevit Update',
			    options=[install,
			             skip]
			)
			if res == install:
				Update.pyRevit()
			else:
				hasUpdates = True

		if extensions:
			install = 'Install extension updates now'
			skip = 'Skip updates'
			if noInteraction:
				res = install
			else:
				res = forms.alert(
				    'There are pyRevit extension updates ready to be installed.',
				    title='pyRevit Extensions Updates',
				    options=[install,
				             skip]
				)
			if res == install:
				UI.printLogo()
				UI.printTitle()
				Update.extensions()
				out.print_html('<br><br>Update has finished. Reloading ...<br><br>')
				Session.reload()
			else:
				hasUpdates = True

		return hasUpdates

	@staticmethod
	def printLogo():
		out = script.get_output()
		out.print_html(
		    '<div style="text-align:center; margin: 30px 0"><img src="{}" style="max-width:35rem;"></div>'
		    .format(config.RPM_DIR + '/svg/rpm-ui.svg')
		)

	@staticmethod
	def printTitle():
		out = script.get_output()
		out.print_html('<h2>Revitron Package Manager</h2>')
