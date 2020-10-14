import revitron 
from revitron import _ 
from revitronui import SelectType
from pyrevit import forms

roomTagTypes = revitron.Filter().byCategory('Room Tags').onlyTypes().getElements()
roomTagType = SelectType(roomTagTypes).show()

transaction = revitron.Transaction()
for room in revitron.Filter(revitron.ACTIVEVIEW.Id).byCategory('Rooms').noTypes().getElements():
    revitron.RoomTag.bottomRight(room)
transaction.commit()