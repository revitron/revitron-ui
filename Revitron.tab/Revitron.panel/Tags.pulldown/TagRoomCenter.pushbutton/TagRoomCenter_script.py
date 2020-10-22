import revitron 
from revitronui import RoomTags

transaction = revitron.Transaction()
RoomTags.add(revitron.RoomTag.center, 'Select Room Tag Type (Center)')
transaction.commit()