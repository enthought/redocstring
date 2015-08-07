Styles
------

SectionDoc comes with the following predefined rendering styles

.. toctree::
    :maxdepth: 1

    legacy_style

.. note::

  The default rendering style is currently :mod:`~.legacy`


Extending
---------

Custom styles can be created by instanciating a :class:`~.Style` to
map a :class:`~.DocRender` factory for each type of object rendered by
autodoc. For example adding the following functions in you conf.py
defines a rendering style for functions and methods::

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
          'function': function_section,
          'method': function_section})
      app.setup_extension('sphinx.ext.autodoc')
      app.connect('autodoc-process-docstring', style.render_docstring)

Specifically the :class:`~.Style` instance will map the ``function``
and ``method`` docstrings to the dostring rendering funtion
``function_section``. The :class:`~DocRender` will then detect the
sections ``Returns, Arguments, Parameters, Raises, Yields, Notes`` and
use the mapped combination of section rendering function, Item description
and item rendering type to render the detected section in-place.

The rendering styles can be further extented by implemeting new Item,
Renderer instances or section rendering functions.
