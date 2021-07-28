import revitron
from revitron import _
from pyrevit import output


class ElementInfo:

	def __init__(self, elements):

		out = output.get_output()
		self.info = []

		for element in elements:

			dependents = []

			for dep in _(element).getDependent():
				depFamType = revitron.Parameter(dep, 'Family and Type').getValueString()
				depInfo = '{} {}, {}'.format(
				    out.linkify(dep.Id),
				    _(dep).getCategoryName(), depFamType
				).strip(', ')
				depInfo = depInfo + '<br>'
				dependents.append(depInfo)

			self.info.append([
			    out.linkify(element.Id),
			    _(element).getClassName(),
			    _(element).getCategoryName(),
			    _(element).getFamilyAndTypeName(), ''.join(dependents)
			])

	def show(self, title=''):

		out = output.get_output()
		out.print_table(
		    self.info,
		    title=title,
		    columns=['ID', 'Class', 'Category', 'Family / Type', 'Dependent']
		)
