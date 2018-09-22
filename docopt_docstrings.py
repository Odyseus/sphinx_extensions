#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import re
import sphinx

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.util.nodes import set_source_info

from html import escape as escape_html

bold_markdown_re = re.compile(r"\*\*([^\*\*]*)\*\*")
bold_rendered_markdown_placeholder = r'<span class="text-bold">\1</span>'

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
                line = escape_html(line)
                line = re.sub(bold_markdown_re, bold_rendered_markdown_placeholder, line)

                if line.startswith((" ", "\t")):
                    lines.append(line)
                else:
                    lines.append('<span class="text-bold">%s</span>' %
                                 line if line else "")

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
