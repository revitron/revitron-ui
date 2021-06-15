import revitron 
from revitron import _
from rpw.ui import forms
import re, sys

selection = revitron.Selection().get()

if not selection:
	print('Nothing selected!')
	sys.exit()

def isFamilyType(element):
	if 'FamilySymbol' in str(element):
		return True
	if 'Type' in str(element):
		return True 
	return False

parameters = revitron.ParameterNameList().get()
defaultParameter = False

if 'Name' in parameters:
    defaultParameter = 'Name'

form = forms.FlexForm('Search and Replace in Selection', [	
	forms.Label('Parameter (any paramert or "Name" for type names)'),
	forms.ComboBox('parameter', parameters, default=defaultParameter),
	forms.Separator(),
	forms.Label('Add Prefix'),
	forms.TextBox('prefix'),
	forms.Label('Add Suffix'),
	forms.TextBox('suffix'),
	forms.Separator(),
	forms.Label('Advanced Regex Operations'),
	forms.Label('Search Pattern'),
	forms.TextBox('regex'),
	forms.Label('Replacement'),
	forms.TextBox('replace'),
	forms.Separator(),
	forms.Button('Apply')
])

form.show()

t = revitron.Transaction()

for element in selection:
	if 'parameter' in form.values.keys():
		param = form.values['parameter']
		if param:
			prefix = form.values['prefix']
			suffix = form.values['suffix']
			regex = form.values['regex']
			replace = form.values['replace']
			if isFamilyType(element) and param == 'Name':
				if prefix or suffix:
					element.Name = prefix + _(element).get('Type Name') + suffix
				if regex:
					element.Name = str(re.sub(regex, replace, _(element).get('Type Name'), flags = re.IGNORECASE))
			else:
				if revitron.Parameter(element, param).exists():	
					if prefix or suffix:
						_(element).set(param, prefix + _(element).get(param) + suffix)
					if regex:
						_(element).set(param, str(re.sub(regex, replace, _(element).get(param), flags = re.IGNORECASE)))
		
t.commit()