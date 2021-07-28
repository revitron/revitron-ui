import revitron
from revitronui import RoomTags

transaction = revitron.Transaction()
RoomTags.add(revitron.RoomTag.topRight, 'Select Room Tag Type (Top Right)')
transaction.commit()