from refactordoc.base_doc import BaseDoc
from refactordoc.sections import (
    attributes, methods_table, notes_paragraph, item_list, arguments)

# -----------------------------------------------------------------------------
# Extension definition
# -----------------------------------------------------------------------------


def refactor_class(lines):
    return BaseDoc(
        lines,
        sections={
            'Attributes': attributes,
            'Methods': methods_table,
            'Notes': notes_paragraph})


def refactor_function(lines):
    return BaseDoc(
        lines,
        sections={
            'Returns': item_list,
            'Arguments': arguments,
            'Parameters': arguments,
            'Raises': item_list,
            'Yields': item_list,
            'Notes': notes_paragraph})


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
