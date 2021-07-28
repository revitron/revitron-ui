import revitron
from revitron import _
from pyrevit import script

output = script.get_output()

transaction = revitron.Transaction()

for element in revitron.Selection.get():
	_element = _(element)
	if _element.isNotOwned():
		for intersected in revitron.Filter().byIntersection(element).getElements():
			if not revitron.DB.JoinGeometryUtils.AreElementsJoined(
			    revitron.DOC,
			    element,
			    intersected
			):
				try:
					if _(intersected).isNotOwned:
						revitron.DB.JoinGeometryUtils.JoinGeometry(
						    revitron.DOC,
						    element,
						    intersected
						)
					else:
						print(
						    'Element {} is used by another user!'.format(
						        output.linkify(intersected.Id)
						    )
						)
				except:
					pass

transaction.commit()