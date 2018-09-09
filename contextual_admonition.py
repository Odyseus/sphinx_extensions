#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sphinx

from docutils import nodes
from docutils.parsers.rst import Directive
from docutils.parsers.rst import directives
from docutils.parsers.rst.roles import set_classes


class ContextualAdmonition(Directive):

    final_argument_whitespace = True
    option_spec = {
        "class": directives.class_option,
        "title": directives.unchanged,
        "context": directives.unchanged
    }
    has_content = True

    node_class = nodes.admonition

    def run(self):
        set_classes(self.options)
        self.assert_has_content()
        text = "\n".join(self.content)
        admonition_node = self.node_class(text, **self.options)
        self.add_name(admonition_node)

        title_text = self.options.get(
            "title", "Use a custom title!!! That's the whole point for the extension existence!!!")
        textnodes, messages = self.state.inline_text(title_text, self.lineno)

        title = nodes.title(title_text, "", *textnodes)
        title.source, title.line = (self.state_machine.get_source_and_line(self.lineno))
        admonition_node += title
        admonition_node += messages

        if "classes" not in self.options:
            admonition_node["classes"] += ["admonition-" + self.options.get("context", "info")]

        admonition_node["classes"] += [self.options.get("context", "info")]

        self.state.nested_parse(self.content, self.content_offset, admonition_node)
        return [admonition_node]


def setup(app):
    app.add_directive("contextual-admonition", ContextualAdmonition)

    return {"version": sphinx.__display_version__, "parallel_read_safe": True}
