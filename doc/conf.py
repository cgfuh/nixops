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

sys.path.insert(0, os.path.abspath(".."))


# -- Project information -----------------------------------------------------

project = "NixOps"
copyright = "2020, NixOps Contributors"
author = "NixOps Contributors"

# The full version, including alpha/beta/rc tags
release = "2.0"


# -- General configuration ---------------------------------------------------

# The document name of the “master” document, that is, the document
# that contains the root toctree directive. Default is 'index'.
# Changed in version 2.0: The default is changed to 'index' from
# 'contents'. But, RTD seems to not be using 2.0.
master_doc = "index"

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["sphinx.ext.autodoc"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "alabaster"

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]


def setup(app):
    from nixops.plugins.manager import PluginManager
    from sphinx.directives.other import TocTree  # type: ignore
    from docutils.parsers.rst import Directive
    from docutils import nodes

    class NixopsPluginsDirective(Directive):
        has_content = True

        def run(self):
            plugin_docs = list(PluginManager.docs())
            if not plugin_docs:
                return []

            ret = [nodes.title("", "Plugins")]
            for plugin_name, path in plugin_docs:
                ret.extend(
                    TocTree(
                        name=plugin_name,
                        arguments=[],
                        options={"caption": plugin_name.capitalize(), "maxdepth": 2},
                        content=[path],
                        lineno=None,
                        content_offset=None,
                        block_text=None,
                        state=self.state,
                        state_machine=self.state_machine,
                    ).run()
                )

            return ret

    app.add_directive("nixops_plugins_doc", NixopsPluginsDirective)
