import revitron
from revitron import _
from revitron.ui import TabWindow, TextBox, SelectBox, Label
from collections import defaultdict

tabs = ['PDF Settings', 'PDF Printer', 'DWG Settings']

window = TabWindow('Export Settings', tabs, width=500, height=610)

config = revitron.DocumentConfigStorage().get('revitron.export', defaultdict())

TextBox.create(window, tabs[0], 'Sheet Export Directory', config)
TextBox.create(window, tabs[0], 'Sheet Naming Template', config)
TextBox.create(window, tabs[0], 'Sheet Size Parameter Name', config)
TextBox.create(window, tabs[0], 'Default Sheet Size', config)
TextBox.create(window, tabs[0], 'Sheet Orientation Parameter Name', config)

SelectBox.create(
    window, tabs[0], 'Default Sheet Orientation', ['Landscape', 'Portrait'], config
)

SelectBox.create(
    window, tabs[0], 'Color Mode', ['Color', 'BlackLine', 'GrayScale'], config
)

TextBox.create(window, tabs[1], 'PDF Printer Address', config)
TextBox.create(window, tabs[1], 'PDF Temporary Output Path', config)

dwgSettings = list(revitron.DB.BaseExportOptions.GetPredefinedSetupNames(revitron.DOC))

if dwgSettings:
	SelectBox.create(window, tabs[2], 'DWG Export Setup', dwgSettings, config)

	SelectBox.create(
	    window,
	    tabs[2],
	    'DWG Export Unit', ['Meter', 'Centimeter', 'Millimeter', 'Foot', 'Inch'],
	    config
	)
else:
	Label.create(window, tabs[2], 'Please first define a named export setting.')

window.show()

if window.ok:
	revitron.DocumentConfigStorage().set('revitron.export', window.values)
