import revitron
from revitronui import RoomTags

transaction = revitron.Transaction()
RoomTags.add(revitron.RoomTag.topLeft, 'Select Room Tag Type (Top Left)')
transaction.commit()