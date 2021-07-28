import revitron
import sys
from revitron import _
from revitronui import SelectType
from pyrevit import forms
from pyrevit import script
from rpw.ui.forms import Alert


def purge(elementIds, typeIdsInteger, title='Purging duplicate instances - 1st pass'):
	output = script.get_output()
	deletedCount = 0
	max_value = len(elementIds)
	counter = 0
	with forms.ProgressBar(title=title + ' ({value} of {max_value})') as pb:
		for elementId in elementIds:
			counter = counter + 1
			try:
				_element = _(elementId)
				if _element.get('Family and Type').IntegerValue in typeIdsInteger:
					if _element.isNotOwned():
						_element.delete()
						deletedCount = deletedCount + 1
					else:
						print(
						    'The duplicate instance {} is owned by another user!'.format(
						        output.linkify(elementId)
						    )
						)
			except:
				pass
			pb.update_progress(counter, max_value)
	return deletedCount


duplicates = revitron.Document().getDuplicateInstances()

if not duplicates:
	sys.exit()

familyTypes = []

for elementId in duplicates:
	familyTypes.append(_(elementId).get('Family and Type'))

dialog = SelectType(list(set(familyTypes)), 'Select family types to be purged')
selectedTypeIds = dialog.show(True)
typeIdsInteger = []

if not selectedTypeIds:
	sys.exit()

for typeId in selectedTypeIds:
	typeIdsInteger.append(typeId.IntegerValue)

transaction = revitron.Transaction()
# Purge twice to also get the nested family instances..
# The first pass will remove always the younger element, the second pass will get
# a new warning list with all the duplicates that couldn't be remove in the first pass
# (which must be shared families inside another family).
# The second run will then remove always the older instances (getDuplicateInstances(True)).
deletedCount = purge(duplicates, typeIdsInteger)
deletedCount = deletedCount + purge(
    revitron.Document().getDuplicateInstances(True), typeIdsInteger,
    'Purging duplicate instances - 2nd pass'
)
transaction.commit()

Alert('', header='Purged {} duplicate instances!'.format(deletedCount))
