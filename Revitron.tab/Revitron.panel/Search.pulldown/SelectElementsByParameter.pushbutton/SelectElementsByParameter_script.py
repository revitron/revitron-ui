import revitron
from revitron import _
from rpw.ui.forms import FlexForm, TextBox, Button, Label, Separator, ComboBox, CheckBox
import System.Windows

defaultParameter = False
parameters = revitron.ParameterNameList().get()
selection = revitron.Selection.get()

if 'Family and Type' in parameters:
    defaultParameter = 'Family and Type'

components = [
    Label('Parameter Name'),
    ComboBox('parameter', parameters, default=defaultParameter),
    Label('Search String'),
    TextBox('search'),
    Separator(),
    CheckBox('invert', 'Invert Selection', default=False)
]

if selection:
    components.append(CheckBox('selection', 'Search in selection only', default=True))
else:
    components.append(CheckBox('viewOnly', 'Search in this view only', default=False))
    
components.append(Button('Select', Width=100, HorizontalAlignment=System.Windows.HorizontalAlignment.Right))

form = FlexForm('Select by Parameter', components)
form.show()

if 'search' in form.values:

    scope = False

    if 'selection' in form.values and form.values['selection']:
        scope = selection
    else:
        if 'viewOnly' in form.values and form.values['viewOnly']:
            scope = revitron.ACTIVE_VIEW.Id

    ids = revitron.Filter(scope).noTypes().byStringContains(form.values['parameter'], form.values['search'], form.values['invert']).getElementIds()

    revitron.Selection.set(ids)