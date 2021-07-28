import revitron
from pyrevit import forms


class RoomTags():

	@staticmethod
	def add(method, title):
		import revitronui
		roomTagTypes = revitron.Filter().byCategory('Room Tags').onlyTypes().getElements()
		roomTagType = revitronui.SelectType(roomTagTypes, title).show()
		scope = revitron.Selection.get()
		if not scope:
			scope = revitron.ACTIVE_VIEW.Id
		if roomTagType:
			rooms = revitron.Filter(scope).byCategory('Rooms').noTypes().getElements()
			max_value = len(rooms)
			counter = 0
			with forms.ProgressBar(
			    title='Tagging rooms ... ({value} of {max_value})'
			) as pb:
				for room in rooms:
					counter = counter + 1
					try:
						method(room, roomTagType.Id)
					except:
						pass
					pb.update_progress(counter, max_value)