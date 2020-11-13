import revitron
import revitronui 

revitronui.ElementInfo(revitron.Selection().get()).show('Info: Selected Elements')