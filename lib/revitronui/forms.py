import revitron
from pyrevit import forms


class SelectType:

	def __init__(self, elementTypes, title):
		self.title = title
		self.options = []
		for elementType in elementTypes:
			self.options.append(OptionListTypes(elementType))

	def show(self, multiselect=False):
		return forms.SelectFromList.show(
		    self.options,
		    title=self.title,
		    multiselect=multiselect,
		    button_name='Select Type'
		)


class OptionListTypes(forms.TemplateListItem):

	@property
	def name(self):
		return revitron.ParameterTemplate(
		    self.item, '{Family Name} - {Type Name}', False
		).render()
