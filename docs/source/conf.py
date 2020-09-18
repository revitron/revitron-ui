# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
import datetime
import revitron_sphinx_theme

master_doc = 'index'

# -- Project information -----------------------------------------------------

project = 'Revitron UI'
copyright = '{}, Marc Anton Dahmen'.format(datetime.datetime.now().year)
author = 'Marc Anton Dahmen'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinxext.opengraph'
]

# Open Graph extension config. https://pypi.org/project/sphinxext-opengraph/
ogp_site_url = "https://revitron-ui.readthedocs.io/"
ogp_image = "https://raw.githubusercontent.com/revitron/revitron-ui/master/docs/source/_static/revitron-ui.png"
ogp_description_length = 300

ogp_custom_meta_tags = [
    '<meta name="twitter:card" content="summary_large_image">',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = []

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
#html_theme = 'alabaster'

html_theme = 'revitron_sphinx_theme'
html_theme_options = {
    'navigation_depth': 5,
    'logo_mobile': 'revitron-ui-mobile.svg',
    'github_url': 'https://github.com/revitron/revitron-ui'
}

html_logo = '_static/revitron-ui.svg'
html_title = 'Revitron UI'
html_favicon = '_static/favicon.ico'

html_context = {
    'landing_page': {
        'menu': [
            {'title': 'Revitron', 'url': 'https://revitron.readthedocs.io/en/latest/'},
            {'title': 'Tools', 'url': 'tools.html'},
            {'title': 'RPM', 'url': 'https://github.com/revitron/rpm-ui/blob/master/README.md'}
        ]
    }
}

html_sidebars = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

html_css_files = ['custom.css']

html_js_files = []