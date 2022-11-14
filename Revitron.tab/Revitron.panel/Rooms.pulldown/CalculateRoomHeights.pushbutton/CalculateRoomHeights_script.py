import revitron
from revitron import _
from revitron.ui import TabWindow, TextBox, SelectBox, Label, CheckBox
from pyrevit import script
from pyrevit.forms import ProgressBar
from collections import defaultdict, OrderedDict
from rpw.ui.forms.resources import *

config = revitron.DocumentConfigStorage().get(
    'revitron.rooms.calculateRoomHeights', defaultdict()
)

tabs = ['Settings', 'Raw', 'Finished']

window = TabWindow(
    'Export Settings', tabs, okButtonText='Calculate', width=560, height=600
)

TextBox.create(
    window, tabs[0], 'roomFltrParam', config, title='Room Filter Parameter Name'
)

TextBox.create(
    window,
    tabs[0],
    'roomFltrList',
    config,
    title='Room Filter List (separate multiple by comma)'
)

CheckBox.create(window, tabs[0], 'roomFltrInvert', config, title='Invert Room Filter')

TextBox.create(window, tabs[0], 'gridSize', config, title='Grid Size', default='5')

TextBox.create(
    window, tabs[1], 'rawEleFltrParam', config, title='Raw Element Filter Parameter Name'
)

TextBox.create(
    window,
    tabs[1],
    'rawEleFltrList',
    config,
    title='Raw Element Filter List (separate multiple by comma)'
)

CheckBox.create(
    window, tabs[1], 'rawEleFltrInvert', config, title='Invert Raw Element Filter'
)

TextBox.create(
    window,
    tabs[1],
    'rawBottomMinParam',
    config,
    title='Min Top of Floor (Raw) Parameter Name',
    default='Raw: Top of floor (min)'
)

TextBox.create(
    window,
    tabs[1],
    'rawBottomMaxParam',
    config,
    title='Max Top of Floor (Raw) Parameter Name',
    default='Raw: Top of floor (max)'
)

TextBox.create(
    window,
    tabs[1],
    'rawTopMinParam',
    config,
    title='Min Bottom of Ceiling (Raw) Parameter Name',
    default='Raw: Bottom of ceiling (min)'
)

TextBox.create(
    window,
    tabs[1],
    'rawTopMaxParam',
    config,
    title='Max Bottom of Ceiling (Raw) Parameter Name',
    default='Raw: Bottom of ceiling (max)'
)

TextBox.create(
    window,
    tabs[2],
    'finEleFltrParam',
    config,
    title='Finished Element Filter Parameter Name'
)

TextBox.create(
    window,
    tabs[2],
    'finEleFltrList',
    config,
    title='Finished Element Filter List (separate multiple by comma)'
)

CheckBox.create(
    window, tabs[2], 'finEleFltrInvert', config, title='Invert Finished Element Filter'
)

TextBox.create(
    window,
    tabs[2],
    'finBottomMinParam',
    config,
    title='Min Top of Floor (Finished) Parameter Name',
    default='Finished: Top of floor (min)',
)

TextBox.create(
    window,
    tabs[2],
    'finBottomMaxParam',
    config,
    title='Max Top of Floor (Finished) Parameter Name',
    default='Finished: Top of floor (max)',
)

TextBox.create(
    window,
    tabs[2],
    'finTopMinParam',
    config,
    title='Min Bottom of Ceiling (Finished) Parameter Name',
    default='Finished: Bottom of ceiling (min)',
)

TextBox.create(
    window,
    tabs[2],
    'finTopMaxParam',
    config,
    title='Max Bottom of Ceiling (Finished) Parameter Name',
    default='Finished: Bottom of ceiling (max)',
)

window.show()

values = revitron.AttrDict(window.values)

if window.values:
	with revitron.Transaction(suppressWarnings=True):

		revitron.DocumentConfigStorage().set(
		    'revitron.rooms.calculateRoomHeights', window.values
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
				    values.rawEleFltrParam,
				    values.rawEleFltrList,
				    values.rawEleFltrInvert
				)
				rawElements = rawFilter.noTypes().getElementIds()

			pb.update_progress(2, max_value)

			if values.finEleFltrParam:
				finFilter = revitron.Filter().byStringContainsOneInCsv(
				    values.finEleFltrParam,
				    values.finEleFltrList,
				    values.finEleFltrInvert
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
