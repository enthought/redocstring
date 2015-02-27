from sectiondoc.sections import (
    attributes, methods_table, notes_paragraph, item_list, arguments)
from sectiondoc.renderers import Attribute, Method, Argument, ListItem
from sectiondoc.items import OrDefinitionItem, MethodItem
from sectiondoc.styles.doc_render import DocRender
from sectiondoc.styles.style import Style


def class_section(lines):
    return DocRender(
        lines,
        sections={
            'Attributes': (attributes, Attribute, OrDefinitionItem),
            'Methods': (methods_table, Method, MethodItem),
            'Notes': (notes_paragraph, None, None)})


def function_section(lines):
    return DocRender(
        lines,
        sections={
            'Returns': (item_list, ListItem, OrDefinitionItem),
            'Arguments': (arguments, Argument, OrDefinitionItem),
            'Parameters': (arguments, Argument, OrDefinitionItem),
            'Raises': (item_list, ListItem, OrDefinitionItem),
            'Yields': (item_list, ListItem, OrDefinitionItem),
            'Notes': (notes_paragraph, None, None)})


def setup(app):
    style = Style({
        'class': class_section,
        'function': function_section,
        'method': function_section})
    app.setup_extension('sphinx.ext.autodoc')
    app.connect('autodoc-process-docstring', style.render_docstring)
