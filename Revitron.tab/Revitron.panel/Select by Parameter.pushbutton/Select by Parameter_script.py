import revitron
from revitron import _
from rpw.ui.forms import FlexForm, TextBox, Button, Label, Separator, ComboBox, CheckBox
import System.Windows

defaultParameter = False
parameters = revitron.ParameterNameList().get()

if 'Family and Type' in parameters:
    defaultParameter = 'Family and Type'

components = [
    Label('Parameter Name'),
    ComboBox('parameter', parameters, default=defaultParameter),
    Label('Search String'),
    TextBox('search'),
    Separator(),
    CheckBox('invert', 'Invert Selection', default=False),
    CheckBox('viewOnly', 'This view only', default=False),
    Button('Select', Width=100, HorizontalAlignment=System.Windows.HorizontalAlignment.Right)
]

form = FlexForm('Select by Parameter', components)
form.show()

if 'search' in form.values:

    viewId = False

    if form.values['viewOnly']:
        viewId = revitron.ACTIVEVIEW.Id

    ids = revitron.Filter(viewId).noTypes().byStringContains(form.values['parameter'], form.values['search'], form.values['invert']).getElementIds()

    revitron.Selection.set(ids)