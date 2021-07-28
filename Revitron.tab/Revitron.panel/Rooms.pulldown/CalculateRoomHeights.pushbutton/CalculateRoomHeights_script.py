import revitron
from revitron import _
from pyrevit import script
from pyrevit.forms import ProgressBar
from rpw.ui import forms
from collections import defaultdict, OrderedDict
import System.Windows
from rpw.ui.forms import FlexForm, Button
from rpw.ui.forms.resources import *


def openHelp(sender, e):
	script.open_url('https://revitron-ui.readthedocs.io/en/latest/tools/rooms.html')


def addField(
    fields, config, name, title, component='TextBox', default='', tab='Settings'
):
	value = config.get(name)
	if not value:
		value = default
	_component = getattr(forms, component)
	if component == 'CheckBox':
		fields[name] = revitron.AttrDict({
		    'label':
		    forms.Label('', **{"tab": tab}),
		    'input':
		    _component(name, title, value, **{"tab": tab})
		})
	else:
		kwargs = {'name': name, 'default': value, 'tab': tab}
		fields[name] = revitron.AttrDict({
		    'label': forms.Label(title, **{"tab": tab}),
		    'input': _component(**kwargs)
		})
	return fields


class TabWindowButton(Button):

	def __init__(self, button_text, on_click=None, **kwargs):
		self.Content = button_text
		self.on_click = on_click or TabWindow.get_values
		self.set_attrs(**kwargs)


class TabWindow(FlexForm):

	layout = """
			<Window
				xmlns="http://schemas.microsoft.com/winfx/2006/xaml/presentation"
				xmlns:x="http://schemas.microsoft.com/winfx/2006/xaml"
				xmlns:d="http://schemas.microsoft.com/expression/blend/2008"
				xmlns:mc="http://schemas.openxmlformats.org/markup-compatibility/2006"
				xmlns:local="clr-namespace:WpfApplication1" mc:Ignorable="d"
				Height="630" Width="362"
				WindowStartupLocation="CenterScreen"
				Topmost="True"
				>
				<StackPanel Name="MainGrid" Margin="0,10,0,10">
					<TabControl TabStripPlacement="Top" Margin="10,10,10,10">
						<TabItem Header="Settings">
							<StackPanel Name="Settings" Height="430"></StackPanel>
						</TabItem>
						<TabItem Header="Raw">
							<StackPanel Name="Raw" Height="430"></StackPanel>
						</TabItem>
						<TabItem Header="Finished">
							<StackPanel Name="Finished" Height="430"></StackPanel>
						</TabItem>
					</TabControl>
					<StackPanel Name="Main" Margin="10,10,10,10">
					</StackPanel>
				</StackPanel>
			</Window>
			"""

	def __init__(self, title, components, **kwargs):

		self.ui = wpf.LoadComponent(self, StringReader(self.layout))
		self.ui.Title = title
		self.values = {}

		for key, value in kwargs.iteritems():
			setattr(self, key, value)

		for n, component in enumerate(components):

			try:
				_container = component.tab
				if component.__class__.__name__ == 'Label':
					component.Margin = Thickness(10, 10, 10, 0)
				else:
					component.Margin = Thickness(10, 0, 10, 0)
			except:
				_container = 'Main'
				component.Margin = Thickness(10, 5, 10, 5)

			container = getattr(self, _container)
			container.Children.Add(component)

			if hasattr(component, 'on_click'):
				component.Click += component.on_click

	@staticmethod
	def get_values(sender, e):

		component_values = {}
		window = Window.GetWindow(sender)
		for container in [window.Main, window.Settings, window.Raw, window.Finished]:
			for component in container.Children:
				try:
					component_values[component.Name] = component.value
				except AttributeError:
					pass
		window.values = component_values
		window.close()


config = revitron.DocumentConfigStorage().get(
    'revitron.rooms.calculateRoomHeights', defaultdict()
)

fields = addField(
    OrderedDict(),
    config,
    'roomFltrParam',
    'Room Filter Parameter Name',
    'TextBox',
    tab='Settings'
)

fields = addField(
    fields,
    config,
    'roomFltrList',
    'Room Filter List (separate multiple by comma)',
    'TextBox',
    tab='Settings'
)

fields = addField(
    fields, config, 'roomFltrInvert', 'Invert Room Filter', 'CheckBox', tab='Settings'
)

fields = addField(
    fields,
    config,
    'rawEleFltrParam',
    'Raw Element Filter Parameter Name',
    'TextBox',
    tab='Raw'
)

fields = addField(
    fields,
    config,
    'rawEleFltrList',
    'Raw Element Filter List (separate multiple by comma)',
    'TextBox',
    tab='Raw'
)

fields = addField(
    fields,
    config,
    'rawEleFltrInvert',
    'Invert Raw Element Filter',
    'CheckBox',
    tab='Raw'
)

fields = addField(
    fields,
    config,
    'rawBottomMinParam',
    'Min Top of Floor (Raw) Parameter Name',
    'TextBox',
    default='Raw: Top of floor (min)',
    tab='Raw'
)

fields = addField(
    fields,
    config,
    'rawBottomMaxParam',
    'Max Top of Floor (Raw) Parameter Name',
    'TextBox',
    default='Raw: Top of floor (max)',
    tab='Raw'
)

fields = addField(
    fields,
    config,
    'rawTopMinParam',
    'Min Bottom of Ceiling (Raw) Parameter Name',
    'TextBox',
    default='Raw: Bottom of ceiling (min)',
    tab='Raw'
)

fields = addField(
    fields,
    config,
    'rawTopMaxParam',
    'Max Bottom of Ceiling (Raw) Parameter Name',
    'TextBox',
    default='Raw: Bottom of ceiling (max)',
    tab='Raw'
)

fields = addField(
    fields,
    config,
    'finEleFltrParam',
    'Finished Element Filter Parameter Name',
    'TextBox',
    tab='Finished'
)

fields = addField(
    fields,
    config,
    'finEleFltrList',
    'Finished Element Filter List (separate multiple by comma)',
    'TextBox',
    tab='Finished'
)

fields = addField(
    fields,
    config,
    'finEleFltrInvert',
    'Invert Finished Element Filter',
    'CheckBox',
    tab='Finished'
)

fields = addField(
    fields,
    config,
    'finBottomMinParam',
    'Min Top of Floor (Finished) Parameter Name',
    'TextBox',
    default='Finished: Top of floor (min)',
    tab='Finished'
)

fields = addField(
    fields,
    config,
    'finBottomMaxParam',
    'Max Top of Floor (Finished) Parameter Name',
    'TextBox',
    default='Finished: Top of floor (max)',
    tab='Finished'
)

fields = addField(
    fields,
    config,
    'finTopMinParam',
    'Min Bottom of Ceiling (Finished) Parameter Name',
    'TextBox',
    default='Finished: Bottom of ceiling (min)',
    tab='Finished'
)

fields = addField(
    fields,
    config,
    'finTopMaxParam',
    'Max Bottom of Ceiling (Finished) Parameter Name',
    'TextBox',
    default='Finished: Bottom of ceiling (max)',
    tab='Finished'
)

fields = addField(fields, config, 'gridSize', 'Grid Size', default='5', tab='Settings')

components = []

for field in fields.values():
	if field.label:
		components.append(field.label)
	components.append(field.input)

components.append(forms.Button('Open Documentation', on_click=openHelp))
components.append(TabWindowButton('Start'))

form = TabWindow('Calculate Room Heights', components)

form.show()

values = revitron.AttrDict(form.values)

if form.values:

	transaction = revitron.Transaction(suppressWarnings=True)

	revitron.DocumentConfigStorage().set(
	    'revitron.rooms.calculateRoomHeights', form.values
	)

	max_value = 4

	with ProgressBar(
	    indeterminate=True, title='Preparing ... ({value} of {max_value})'
	) as pb:

		pb.update_progress(0, max_value)

		roomFilter = revitron.Filter().noTypes().byCategory('Rooms')

		if values.roomFltrParam and values.roomFltrList:
			roomFilter = roomFilter.byStringContainsOneInCsv(
			    values.roomFltrParam, values.roomFltrList, values.roomFltrInvert
			)
		rooms = roomFilter.getElements()

		rawElements = None
		finElements = None

		pb.update_progress(1, max_value)

		if values.rawEleFltrParam:
			rawFilter = revitron.Filter().byStringContainsOneInCsv(
			    values.rawEleFltrParam, values.rawEleFltrList, values.rawEleFltrInvert
			)
			rawElements = rawFilter.noTypes().getElementIds()

		pb.update_progress(2, max_value)

		if values.finEleFltrParam:
			finFilter = revitron.Filter().byStringContainsOneInCsv(
			    values.finEleFltrParam, values.finEleFltrList, values.finEleFltrInvert
			)
			finElements = finFilter.noTypes().getElementIds()

		pb.update_progress(3, max_value)

		view3D = revitron.Create.view3D()

		pb.update_progress(4, max_value)

	max_value = len(rooms)
	counter = 0
	with ProgressBar(title='Processing Rooms ... ({value} of {max_value})') as pb:
		pb.update_progress(counter, max_value)
		for room in rooms:
			heights = _(room).traceHeight(view3D, rawElements, float(values.gridSize))
			try:
				_(room).set(values.rawBottomMinParam, heights.bottom.min, 'Length')
				_(room).set(values.rawBottomMaxParam, heights.bottom.max, 'Length')
			except:
				pass
			try:
				_(room).set(values.rawTopMinParam, heights.top.min, 'Length')
				_(room).set(values.rawTopMaxParam, heights.top.max, 'Length')
			except:
				pass
			heights = _(room).traceHeight(view3D, finElements, float(values.gridSize))
			try:
				_(room).set(values.finBottomMinParam, heights.bottom.min, 'Length')
				_(room).set(values.finBottomMaxParam, heights.bottom.max, 'Length')
			except:
				pass
			try:
				_(room).set(values.finTopMinParam, heights.top.min, 'Length')
				_(room).set(values.finTopMaxParam, heights.top.max, 'Length')
			except:
				pass
			counter = counter + 1
			pb.update_progress(counter, max_value)

	_(view3D).delete()

	transaction.commit()