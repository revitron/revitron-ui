import revitron
from pyrevit import script
from pyrevit import output

__context__ = 'zero-doc'

style = 'body {padding: 20px 40px; color: #121212;} img {max-width: 500px; padding-bottom: 20px} span {display: block; text-align: center;}'
output.get_output().add_style(style)
output.get_output().set_width(510)
output.get_output().set_height(510)
output.get_output().center()
out = script.get_output()
out.print_image(revitron.LIB_DIR + '/svg/revitron-readme.svg')
out.print_html('<h2>Revitron</h2>A Revit API wrapper written in Python.<br>' +\
	'Check out the <a href="https://revitron-ui.readthedocs.io/">documentation</a>, ' +\
    'the <a href="https://revitron.readthedocs.io/">API reference</a><br>' +\
    'and the repositories on <a href="https://github.com/revitron">GitHub</a> for more infos.<br><br>' +\
    '&copy; Copyright 2020, Marc Anton Dahmen &mdash; MIT license<br>' +\
    'All icons except for the Revitron logo by <a href="https://icons8.com">Icons8</a>')

