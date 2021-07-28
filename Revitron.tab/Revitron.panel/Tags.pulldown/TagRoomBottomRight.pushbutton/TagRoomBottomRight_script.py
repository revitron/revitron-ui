import revitron
from revitronui import RoomTags

transaction = revitron.Transaction()
RoomTags.add(revitron.RoomTag.bottomRight, 'Select Room Tag Type (Bottom Right)')
transaction.commit()