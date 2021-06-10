from revitron import REVITRON_VERSION
from revitronui import REVITRON_UI_VERSION
import os
import datetime
from pyrevit import script
from pyrevit import output

now = datetime.datetime.now()
parent = os.path.dirname 
html = """<h1>Revitron</h1>
Library {} &mdash; UI {}

A Revit API wrapper for pyRevit written in Python.
Check out the <a href="https://revitron-ui.readthedocs.io/">user guide</a>, the <a href="https://revitron.readthedocs.io/">API reference</a>
and <a href="https://github.com/revitron">GitHub</a> for more infos.

<small>&copy; Copyright 2020-{}, Marc Anton Dahmen &mdash; MIT license
All icons except for the Revitron logo by <a href="https://icons8.com">Icons8</a></small>"""

svg = parent(parent(parent(parent(__file__)))) + '/svg/revitron-about.svg'

style = """
body {background-color: #2c3e50; color: #ffffff; text-align: center;}
a {color: inherit;}
img {max-width: 28rem;} 
span {display: block; text-align: center;}
small {display: block; color: #959ea7; padding-top: 2rem;}
"""
output.get_output().add_style(style)
output.get_output().set_width(500)
output.get_output().set_height(500)
out = script.get_output()
out.print_image(svg)
out.print_html(html.format(REVITRON_VERSION, REVITRON_UI_VERSION, now.year))
