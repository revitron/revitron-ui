import revitron
from revitron import _
from rpw.ui.forms import FlexForm, TextBox, Button, Label, Separator, ComboBox, CheckBox
import System.Windows

defaultParameter = False
parameters = revitron.ParameterNameList().get()
selection = revitron.Selection.get()
duType = revitron.DB.DisplayUnitType

categories = []

for cat in revitron.DOC.Settings.Categories:
	categories.append(cat.Name)

categories.sort()
categories.insert(0, 'All')

if 'Area' in parameters:
	defaultParameter = 'Area'

components = [
	Label('Parameter Name'),
	ComboBox('parameter', parameters, default=defaultParameter),
	Label('Category'),
	ComboBox('category', categories, default='All'),
	Label('Evaluator'),
	ComboBox('evaluator', {
		'Greater than': 'byNumberIsGreater', 
		'Greater than or equal': 'byNumberIsGreaterOrEqual', 
		'Equal': 'byNumberIsEqual', 
		'Less than': 'byNumberIsLess', 
		'Less than or equal': 'byNumberIsLessOrEqual'
	}),
	Label('Value'),
	TextBox('value'),
	Separator(),
	CheckBox('invert', 'Invert Selection', default=False)
]

if selection:
	components.append(CheckBox('selection', 'Search in selection only', default=True))
else:
	components.append(CheckBox('viewOnly', 'Search in this view only', default=False))
	
components.append(Button('Select', Width=100, HorizontalAlignment=System.Windows.HorizontalAlignment.Right))

form = FlexForm('Select by Numeric Parameter', components)
form.show()

if 'value' in form.values:

	try:
		el = (
			revitron.Filter()
			.byNumberIsGreater(form.values['parameter'], 0.0)
			.noTypes()
			.getElementIds()[0]
		)
		unit = _(el).getParameter(form.values['parameter']).unit()
		value = revitron.Unit.convertToInternalUnit(form.values['value'], unit)
	except:
		value = float(form.values['value'])
		print('no unit', value)

	scope = False

	if 'selection' in form.values and form.values['selection']:
		scope = selection
	else:
		if 'viewOnly' in form.values and form.values['viewOnly']:
			scope = revitron.ACTIVE_VIEW.Id

	evaluator = getattr(revitron.Filter, form.values['evaluator'])

	fltr = revitron.Filter(scope)

	if form.values['category'] != 'All':
		fltr.byCategory(form.values['category'])

	ids = evaluator(
		fltr, 
		form.values['parameter'], 
		value, 
		form.values['invert']
	).noTypes().getElementIds()

	revitron.Selection.set(ids)