# -*- coding: utf-8 -*-
#
# rstoolbox documentation build configuration file, created by
# sphinx-quickstart on Thu Jan 18 11:39:05 2018.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#

import sphinx_bootstrap_theme
import matplotlib as mpl
mpl.use("Agg")
from rstoolbox._version import get_versions


# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.coverage',
              'sphinx.ext.githubpages',
              'sphinx.ext.intersphinx',
              'sphinx.ext.autosummary',
              'sphinx.ext.mathjax',
              'IPython.sphinxext.ipython_directive',
              'IPython.sphinxext.ipython_console_highlighting']

# Generate the API documentation when building
autosummary_generate = True

# Include the example source for plots in API docs
plot_include_source = True
plot_formats = [("png", 90)]
plot_html_show_formats = False
plot_html_show_source_link = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates', '_templates/autosummary']
numpydoc_show_inherited_class_members = False

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = u'rstoolbox'
copyright = u'2018, Jaume Bonet'
author = u'Jaume Bonet'

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
version = get_versions()['version'].split("+")[0]
# The full version, including alpha/beta/rc tags.
release = get_versions()['version'].split("+")[0]

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

intersphinx_mapping = {'python': ('http://docs.python.org/2', None),
                       'numpy': ('http://docs.scipy.org/doc/numpy/', None),
                       'pandas': ('http://pandas.pydata.org/pandas-docs/stable/', None),
                       'matplotlib': ('http://matplotlib.sourceforge.net/', None),
                       'seaborn': ('https://seaborn.pydata.org/', None),
                       'networkx': ('https://networkx.github.io', None),
                       'libconfig': ('http://jaumebonet.cat/libconfig/', None)}


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'bootstrap'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
html_theme_options = {
    'source_link_position': "footer",
    'bootswatch_theme': "paper",
    'nosidebar': True,
    'navbar_sidebarrel': False,
    'bootstrap_version': "3",
    'navbar_links': [
        ("Scripts", "scripts"),
        ("Tutorial", "tutorial"),
        ("API", "api"),
    ],
}
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
# html_sidebars = {
#     '**': [
#         'relations.html',  # needs 'show_related': True theme option to display
#         'searchbox.html',
#     ]
# }


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'rstoolboxdoc'
html_show_sourcelink = False


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'rstoolbox.tex', u'rstoolbox Documentation',
     u'Jaume Bonet', 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'rstoolbox', u'rstoolbox Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'rstoolbox', u'rstoolbox Documentation',
     author, 'rstoolbox', 'A toolbox to manage and select Rosetta output designs.',
     'Protein design and decoy evaluation'),
]


def setup(app):
    app.add_javascript('functions.js')
    app.add_stylesheet('style.css')
