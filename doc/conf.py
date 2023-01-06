# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "PyEPR"
copyright = "2011-2023, Antonio Valentino"
author = "Antonio Valentino"


def get_version(filename):
    import re
    from packaging.version import parse as Version

    with open(filename) as fd:
        data = fd.read()

    mobj = re.search(
        r"""^__version__\s*=\s*(?P<quote>['"])(?P<version>.*)(?P=quote)""",
        data,
        re.MULTILINE,
    )
    return Version(mobj.group("version"))


_version = get_version("../src/epr.pyx")

version = _version.base_version
release = str(_version)

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.extlinks",
    "sphinx.ext.ifconfig",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.imgmath",
    "sphinx_rtd_theme",
    "IPython.sphinxext.ipython_console_highlighting",
    "IPython.sphinxext.ipython_directive",
]

templates_path = ["_templates"]
master_doc = "index"
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**/empty.txt",
]
pygments_style = "sphinx"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

# html_theme = 'alabaster'
html_theme = "sphinx_rtd_theme"
html_theme_options = {
    # 'prev_next_buttons_location': 'both',
}
html_static_path = ["_static"]
html_last_updated_fmt = "%b %d, %Y"
html_sidebars = {
    "index": [
        # 'globaltoc.html',
        # 'relations.html',
        # 'sourcelink.html',
        # 'searchbox.html',
        "pypi.html",
        "gha.html",
        "readthedocs.html",
        "codecov.html",
        "ohloh.html",
    ],
}
html_domain_indices = False
html_context = {
    "display_github": True,
    "github_user": "avalentino",
    "github_repo": "pyepr",
    "github_version": "master",
    "conf_py_path": "/doc/",
}

# -- Options for HTMLHelp output ------------------------------------------

htmlhelp_basename = "PyEPRdoc"

# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    "papersize": "a4paper",
    "pointsize": "12pt",
    # 'preamble': '',
    # 'figure_align': 'htbp',
}
latex_documents = [
    (master_doc, "pyepr.tex", "PyEPR Documentation", author, "manual"),
]
latex_domain_indices = False

# -- Options for manual page output ---------------------------------------

man_pages = [(master_doc, "pyepr", "PyEPR Documentation", [author], 1)]

# -- Options for Texinfo output -------------------------------------------

texinfo_documents = [
    (
        master_doc,
        "PyEPR",
        "PyEPR Documentation",
        author,
        "PyEPR",
        "One line description of project.",
        "Miscellaneous",
    ),
]

# -- Options for Epub output ----------------------------------------------

epub_exclude_files = ["search.html"]


# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://docs.scipy.org/doc/numpy", None),
}

# -- Options for extlinks extension ------------------------------------------

extlinks = {
    "issue": ("https://github.com/avalentino/pyepr/issues/%s", "gh-%s"),
}

# -- Options for todo extension ----------------------------------------------

todo_include_todos = True
