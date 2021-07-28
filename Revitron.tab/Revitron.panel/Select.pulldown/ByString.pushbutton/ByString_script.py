import revitron
from revitron import _
from rpw.ui.forms import FlexForm, TextBox, Button, Label, Separator, ComboBox, CheckBox
import System.Windows

defaultParameter = False
parameters = revitron.ParameterNameList().get()
selection = revitron.Selection.get()

categories = []

for cat in revitron.DOC.Settings.Categories:
	categories.append(cat.Name)

categories.sort()
categories.insert(0, 'All')

if 'Family and Type' in parameters:
	defaultParameter = 'Family and Type'

components = [
    Label('Parameter Name'),
    ComboBox('parameter', parameters, default=defaultParameter),
    Label('Category'),
    ComboBox('category', categories, default='All'),
    Label('Search String'),
    TextBox('search'),
    Separator(),
    CheckBox('invert', 'Invert Selection', default=False)
]

if selection:
	components.append(CheckBox('selection', 'Search in selection only', default=True))
else:
	components.append(CheckBox('viewOnly', 'Search in this view only', default=False))

components.append(
    Button(
        'Select', Width=100, HorizontalAlignment=System.Windows.HorizontalAlignment.Right
    )
)

form = FlexForm('Select by String Parameter', components)
form.show()

if 'search' in form.values:

	scope = False

	if 'selection' in form.values and form.values['selection']:
		scope = selection
	else:
		if 'viewOnly' in form.values and form.values['viewOnly']:
			scope = revitron.ACTIVE_VIEW.Id

	fltr = (
	    revitron.Filter(scope).noTypes().byStringContains(
	        form.values['parameter'], form.values['search'], form.values['invert']
	    )
	)

	if form.values['category'] != 'All':
		fltr.byCategory(form.values['category'])

	ids = fltr.getElementIds()

	revitron.Selection.set(ids)