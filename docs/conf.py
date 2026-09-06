# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Version utils -----------------------------------------------------------
def _get_version(filename):
    import re

    from packaging.version import parse as Version

    with open(filename, encoding="utf-8") as fd:
        data = fd.read()

    mobj = re.search(
        r"""^__version__\s*=\s*(?P<quote>['"])(?P<version>.*)(?P=quote)""",
        data,
        re.MULTILINE,
    )
    return Version(mobj.group("version"))


# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "PyEPR"
copyright = "2011-2026, Antonio Valentino"
author = "Antonio Valentino"


_version = _get_version("../src/epr/__init__.py")

version = _version.base_version
release = str(_version)


# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    # "sphinx.ext.autodoc",
    # "sphinx.ext.autosectionlabel",
    # "sphinx.ext.autosummary",
    # "sphinx.ext.coverage",
    "sphinx.ext.doctest",
    # "sphinx.ext.duration",
    "sphinx.ext.extlinks",
    # "sphinx.ext.githubpages",
    # "sphinx.ext.graphviz",
    "sphinx.ext.ifconfig",
    # "sphinx.ext.imgconverter",
    # "sphinx.ext.inheritance_diagram",
    "sphinx.ext.intersphinx",
    # "sphinx.ext.linkcode",  # needs_sphinx = "1.2"
    # "sphinx.ext.napoleon",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    # "sphinx.ext.imgmath",
    # "sphinx.ext.jsmath",
    "sphinx.ext.mathjax",
    "sphinx_rtd_theme",
    "IPython.sphinxext.ipython_console_highlighting",
    "IPython.sphinxext.ipython_directive",
]

try:
    import sphinxcontrib.spelling  # noqa: F401
except ImportError:
    pass
else:
    extensions.append("sphinxcontrib.spelling")

templates_path = ["_templates"]
master_doc = "index"
exclude_patterns = [
    "_build",
    "Thumbs.db",
    ".DS_Store",
    "**/.gitkeep",
]


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
    "conf_py_path": "/docs/",
}


# -- Options for LaTeX output ------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-latex-output

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


# -- Options for linkcheck ------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-the-linkcheck-builder

linkcheck_ignore = [
    f"https://pyepr.readthedocs.io/en/v{version}",
    "https://www.openhub.net",
    "https://www.gnu.org/licenses/gpl-3.0.html",
]


# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#configuration

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "numpy": ("https://docs.scipy.org/doc/numpy", None),
}


# -- Options for extlinks extension ------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/extlinks.html#module-sphinx.ext.extlinks

extlinks = {
    "issue": ("https://github.com/avalentino/pyepr/issues/%s", "gh-%s"),
}


# -- Options for todo extension ----------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/todo.html#configuration

todo_include_todos = True
