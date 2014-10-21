from refactordoc.base_doc import BaseDoc
from refactordoc.sections import (
    attributes, methods_table, notes_paragraph, item_list, arguments)
from refactordoc.renderers import Attribute, Method, Argument, ListItem
from refactordoc.items import DefinitionItem, MethodItem


def refactor_class(lines):
    return BaseDoc(
        lines,
        sections={
            'Attributes': (attributes, Attribute, DefinitionItem),
            'Methods': (methods_table, Method, MethodItem),
            'Notes': (notes_paragraph, None, None)})


def refactor_function(lines):
    return BaseDoc(
        lines,
        sections={
            'Returns': (item_list, ListItem, DefinitionItem),
            'Arguments': (arguments, Argument, DefinitionItem),
            'Parameters': (arguments, Argument, DefinitionItem),
            'Raises': (item_list, ListItem, DefinitionItem),
            'Yields': (item_list, ListItem, DefinitionItem),
            'Notes': (notes_paragraph, None, None)})


def refactor_docstring(app, what, name, obj, options, lines):

    if 'class' in what:
        refactor = refactor_class(lines)
    elif 'function' in what or 'method' in what:
        refactor = refactor_function(lines)
    else:
        refactor = None

    if refactor is not None:
        refactor.parse()


def setup(app):
    app.setup_extension('sphinx.ext.autodoc')
    app.connect('autodoc-process-docstring', refactor_docstring)
