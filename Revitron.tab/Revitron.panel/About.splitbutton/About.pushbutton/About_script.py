import revitron
from pyrevit import script
from pyrevit import output

__context__ = 'zero-doc'

output.set_stylesheet(revitron.LIB_DIR + '\\css\\output.css')
out = script.get_output()
out.print_image(revitron.LIB_DIR + '/svg/revitron-white.svg')
out.print_html('<strong>Revitron</strong><br><br>A Revit API wrapper written in Python.<br>' +\
	'Check out the <a href="https://revitron-ui.readthedocs.io/">documentation</a>, ' +\
    'the <a href="https://revitron.readthedocs.io/">API reference</a><br>' +\
    'and the repositories on <a href="https://github.com/revitron">GitHub</a> for more infos.<br><br>' +\
    '&copy; Copyright 2020, Marc Anton Dahmen &mdash; MIT license<br>' +\
    'All icons except for the Revitron logo by <a href="https://icons8.com">Icons8</a>')

