import revitron
from revitron import _
from rpw.ui.forms import FlexForm, TextBox, Button, Label, Separator, ComboBox, CheckBox
import System.Windows

components = [
    Label('Parameter Name'),
    ComboBox('parameter', revitron.ParameterNameList().get()),
    Label('Search String'),
    TextBox('search'),
    Separator(),
    CheckBox('invert', 'Invert Selection', default=False),
    CheckBox('viewOnly', 'This view only', default=False),
    Button('Select', Width=100, HorizontalAlignment=System.Windows.HorizontalAlignment.Right)
]

form = FlexForm('Select by Parameter', components)
form.show()

ids = revitron.Filter().noTypes().byStringContains(form.values['parameter'], form.values['search'], form.values['invert']).getElementIds()

revitron.Selection.set(ids)