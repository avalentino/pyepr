# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
sys.path.insert(0, os.path.abspath('sphinxext'))

# -- Project information -----------------------------------------------------

project = 'PyEPR'
copyright = '2011-2019, Antonio Valentino'
author = 'Antonio Valentino'

def get_version(filename='../src/epr.pyx', release=False):
    import re
    from distutils.version import LooseVersion

    s = open(filename).read()
    mobj = re.search("^__version__ = '(?P<version>.*)'$", s, re.MULTILINE)
    mobj.group('version')

    v = LooseVersion(mobj.group('version'))

    if release:
        return v.vstring
    else:
        return '.'.join(map(str, v.version[:3]))

# The short X.Y version.
version = get_version()

# The full version, including alpha/beta/rc tags.
release = get_version(release=True)

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    # 'sphinx.ext.autodoc',
    # 'sphinx.ext.autosectionlabel',
    # 'sphinx.ext.autosummary',
    # 'sphinx.ext.coverage',
    # 'sphinx.ext.doctest',
    'sphinx.ext.extlinks',
    # 'sphinx.ext.githubpages',
    # 'sphinx.ext.graphviz',
    'sphinx.ext.ifconfig',
    # 'sphinx.ext.imgconverter',
    # 'sphinx.ext.inheritance_diagram',
    'sphinx.ext.intersphinx',
    # 'sphinx.ext.linkcode',
    # 'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.viewcode',

    # Math support for HTML outputs in Sphinx
    'sphinx.ext.imgmath',
    # 'sphinx.ext.mathjax',
    # 'sphinx.ext.jsmath',

    # Additional extensions
    'ipython_console_highlighting',
    # 'IPython.sphinxext.ipython_console_highlighting',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The master toctree document.
master_doc = 'index'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    'sphinxext',
    '**/empty.txt',
]

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
html_theme = 'pydoctheme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    'collapsiblesidebar': True,
}

# Add any paths that contain custom themes here, relative to this directory.
html_theme_path = ['.']

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If this is not None, a ‘Last updated on:’ timestamp is inserted at every
# page bottom, using the given strftime() format.
# The empty string is equivalent to '%b %d, %Y'
# (or a locale-dependent equivalent).
html_last_updated_fmt = '%b %d, %Y'

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# This is required for the alabaster theme
# refs: http://alabaster.readthedocs.io/en/latest/installation.html#sidebars
html_sidebars = {
   'index': [
        'globaltoc.html',
        'relations.html',
        'sourcelink.html',
        'searchbox.html',
        'ohloh.html',
        'pypi.html',
        'travis-ci.html',
        'appveyor.html',
        'readthedocs.html',
        'codecov.html',
    ],
}

# If false, no module index is generated.
html_domain_indices = False

# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'PyEPRdoc'

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    'papersize': 'a4paper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    'pointsize': '12pt',

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
    (master_doc, 'pyepr.tex', u'PyEPR Documentation',
     author, 'manual'),
]

# If false, no module index is generated.
latex_domain_indices = False

# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'pyepr', u'PyEPR Documentation',
     [author], 1)
]

# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'PyEPR', u'PyEPR Documentation',
     author, 'PyEPR', 'One line description of project.',
     'Miscellaneous'),
]

# -- Options for Epub output ----------------------------------------------

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']


# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy':  ('https://docs.scipy.org/doc/numpy', None),
}

# -- Options for autodoc extension -------------------------------------------
#autoclass_content = 'both'
#autodoc_default_flags = ['members', 'undoc-members', 'show-inheritance']
#                        #,'inherited-members']

# Auto summary generation
#autosummary_generate = ['reference']

# -- Options for extlinks extension ------------------------------------------
# External links configuration
extlinks = {
    'issue': ('https://github.com/avalentino/pyepr/issues/%s', 'gh-'),
}

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True
