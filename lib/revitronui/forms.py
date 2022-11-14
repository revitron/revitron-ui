import revitron
from pyrevit.forms import SelectFromList, TemplateListItem
from rpw.ui.forms.resources import *


class SelectType:

	def __init__(self, elementTypes, title):
		self.title = title
		self.options = []
		for elementType in elementTypes:
			self.options.append(OptionListTypes(elementType))

	def show(self, multiselect=False):
		return SelectFromList.show(
		    self.options,
		    title=self.title,
		    multiselect=multiselect,
		    button_name='Select Type'
		)


class OptionListTypes(TemplateListItem):

	@property
	def name(self):
		return revitron.ParameterTemplate(
		    self.item, '{Family Name} - {Type Name}', False
		).render()
