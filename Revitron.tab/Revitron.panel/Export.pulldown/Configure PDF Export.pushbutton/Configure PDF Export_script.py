import revitron
from revitron import _
from rpw.ui.forms import FlexForm, TextBox, Button, Label, Separator, ComboBox
import System.Windows


if not revitron.Document().isFamily():
    
    info = _(revitron.DOC.ProjectInformation)
    
    fields = [
        'Revitron PDF Printer Address',
        'Revitron PDF Temporary Output Path',
        'Revitron Sheet Export Directory',
        'Revitron Sheet Naming Template',
        'Revitron Sheet Size Parameter Name',
        'Revitron Default Sheet Size',
        'Revitron Sheet Orientation Parameter Name'
    ]
    
    components = []
    
    for field in fields:
        components.append(Label(field))
        components.append(TextBox(revitron.String.sanitize(field), Text=info.get(field), Width=500))

    orientationField = 'Revitron Default Sheet Orientation'
    orientations = ['Landscape', 'Portrait']
    default = orientations[0]
    if info.get(orientationField) in orientations:
        default = info.get(orientationField)
    components.append(Label(orientationField))
    components.append(ComboBox(revitron.String.sanitize(orientationField), orientations, default=default, Width=500))
    components.append(Label(''))
    components.append(Button('Save', Width=100, HorizontalAlignment=System.Windows.HorizontalAlignment.Right))
    
    form = FlexForm('Revitron PDF Printer Setup', components)
    form.show()
          
    if form.values: 
        transaction = revitron.Transaction()
        for field in fields:
            info.set(field, form.values[revitron.String.sanitize(field)])
        info.set(orientationField, form.values[revitron.String.sanitize(orientationField)])   
        transaction.commit()
       
       
        