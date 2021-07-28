import revitron
from revitronui import RoomTags

transaction = revitron.Transaction()
RoomTags.add(revitron.RoomTag.bottomLeft, 'Select Room Tag Type (Bottom Left)')
transaction.commit()