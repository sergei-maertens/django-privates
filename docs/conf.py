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
from pathlib import Path

import django

current_dir = Path(__file__).parent.parent.resolve()
sys.path.insert(0, str(current_dir))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "testapp.settings")

django.setup()


# -- Project information -----------------------------------------------------

project = "Django Privates"
copyright = "2018, Sergei Maertens"
author = "Sergei Maertens"

# The full version, including alpha/beta/rc tags
release = "1.4.0"


# -- General configuration ---------------------------------------------------

extensions = [
    "sphinx.ext.todo",
    "sphinx.ext.autodoc",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"

# -- Options for todo extension ----------------------------------------------

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = True

linkcheck_ignore = [
    r"https://img.shields.io",  # known to be slow...
    r"https://codecov.io",
]
