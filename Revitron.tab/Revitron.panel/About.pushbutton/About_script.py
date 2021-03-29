import revitron
import os
import datetime
from pyrevit import script
from pyrevit import output

now = datetime.datetime.now()
parent = os.path.dirname 
html = """<div style="padding: 1rem 1rem"><h2>Revitron</h2>A Revit API wrapper written in Python.
Check out the <a href="https://revitron-ui.readthedocs.io/">documentation</a>, the <a href="https://revitron.readthedocs.io/">API reference</a>
and the repositories on <a href="https://github.com/revitron">GitHub</a> for more infos.

&copy; Copyright 2020-{}, Marc Anton Dahmen &mdash; MIT license
All icons except for the Revitron logo by <a href="https://icons8.com">Icons8</a></div>"""

svg = parent(parent(parent(parent(__file__)))) + '/svg/revitron-about.svg'

style = 'img {max-width: 32rem; padding: 0.7rem} span {display: block; text-align: center;}'
output.get_output().add_style(style)
output.get_output().set_width(500)
output.get_output().set_height(500)
out = script.get_output()
out.print_image(svg)
out.print_html(html.format(now.year))
