import revitron
from revitron import _
from rpw.ui.forms import FlexForm, TextBox, Button, Label, Separator, ComboBox
from collections import defaultdict
import System.Windows


if not revitron.Document().isFamily():
    
    config = revitron.DocumentConfigStorage().get('export.pdf', defaultdict())
    
    fields = [
        'PDF Printer Address',
        'PDF Temporary Output Path',
        'Sheet Export Directory',
        'Sheet Naming Template',
        'Sheet Size Parameter Name',
        'Default Sheet Size',
        'Sheet Orientation Parameter Name'
    ]
    
    components = []
    
    for field in fields:
        key = revitron.String.sanitize(field)
        components.append(Label(field))
        components.append(TextBox(key, Text=config.get(key), Width=500))

    orientationField = 'Default Sheet Orientation'
    orientationKey = revitron.String.sanitize(orientationField)
    orientations = ['Landscape', 'Portrait']
    default = orientations[0]
    if config.get(orientationKey) in orientations:
        default = config.get(orientationKey)
    components.append(Label(orientationField))
    components.append(ComboBox(orientationKey, orientations, default=default, Width=500))
    components.append(Label(''))
    components.append(Button('Save', Width=100, HorizontalAlignment=System.Windows.HorizontalAlignment.Right))
    
    form = FlexForm('Revitron PDF Printer Setup', components)
    form.show()
          
    if form.values: 
        revitron.DocumentConfigStorage().set('export.pdf', form.values)
       
       
        