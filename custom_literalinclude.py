#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Custom literal include extension for Sphinx.

Similar to the ``.. literalinclude::`` directive, but instead of including the content of
an entire file (or defining line numbers), it includes dinamically generated data.

Example
-------

In conf.py declare the extension option ``custom_literalincludes``:

custom_literalincludes = {
    "directive-argument": dinamically_generated_data,
}

The ``dinamically_generated_data`` content can be anything from properties of an imported
module or the return of a function and always have to be of type str (string).

In the .rst files use like follows:

.. custom-literalinclude:: directive-argument
"""

import sphinx

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util.nodes import set_source_info


class CustomLiteralInclude(Directive):

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True

    def run(self):
        document = self.state.document
        env = document.settings.env

        try:
            text = env.config.custom_literalincludes[self.arguments[0]]

            if not isinstance(text, str):
                msg = "Wrong data type for literal include. Found %s, must be str." % type(text)
                return [document.reporter.error(msg, line=self.lineno)]

            retnode = nodes.literal_block(text, text)
            set_source_info(self, retnode)
            retnode["classes"] += self.options.get("class", [])
            self.add_name(retnode)

            return [retnode]
        except Exception as err:
            return [document.reporter.error(str(err), line=self.lineno)]


def setup(app):
    app.add_config_value("custom_literalincludes", {}, "html")
    app.add_directive("custom-literalinclude", CustomLiteralInclude)

    return {"version": sphinx.__display_version__, "parallel_read_safe": True}
