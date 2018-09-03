#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""docopt docstrings extension for Sphinx.

Similar to the ``.. custom-literalinclude::`` directive, but it slightly "highlights" the code.

Example
-------

In conf.py declare the extension option ``docopt_docstrings``:

docopt_docstrings = {
    "directive-argument": dinamically_generated_data,
}

The ``dinamically_generated_data`` content can be anything from properties of an imported
module or the return of a function and always have to be of type str (string).

In the .rst files use like follows:

.. docopt-docstring:: directive-argument
"""

import sphinx

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util.nodes import set_source_info

from html import escape as escape_html


container = """<div class="highlight-default notranslate"><div class="highlight">
<pre>%s</pre>
</div></div>
"""


class DocoptDoctring(Directive):

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = True

    def run(self):
        document = self.state.document
        env = document.settings.env

        try:
            text = env.config.docopt_docstrings[self.arguments[0]]

            if not isinstance(text, str):
                msg = "Wrong data type for literal include. Found %s, must be str." % type(text)
                return [document.reporter.error(msg, line=self.lineno)]

            lines = []

            for line in text.strip("\n").splitlines():
                if line.startswith((" ", "\t")):
                    lines.append(escape_html(line))
                else:
                    lines.append('<span class="text-bold">%s</span>' % escape_html(line) if line else "")

            text = "\n".join(lines)

            retnode = nodes.raw("", container % text, format='html')
            set_source_info(self, retnode)
            retnode["classes"] += self.options.get("class", [])
            self.add_name(retnode)

            return [retnode]
        except Exception as err:
            return [document.reporter.error(str(err), line=self.lineno)]


def setup(app):
    app.add_config_value("docopt_docstrings", {}, "html")
    app.add_directive("docopt-docstring", DocoptDoctring)

    return {"version": sphinx.__display_version__, "parallel_read_safe": True}
