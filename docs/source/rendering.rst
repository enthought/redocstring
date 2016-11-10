Docstring rendering
*******************


The are five different parts in the pipeline of **sectiondoc** docstring rendering.

Style
#####

The rendering :class:`~Style` maps the objects types provided by
autodoc to :class:`~DocRender` factory instances which are responsible
for rendering the provided docstring.

The DocRender
#############

The DocRender is responsible for doing the actual work. At
initialization the class receives a dictionary mapping section titles
to a tuple containing a rendering function and (optionally) section
item parsing and rendering classes. The actual rendering starts by
executing :meth:`~.DocRender.parse` to detect sections in the
docstring. For each section that is discovered the
:meth:`~.DocRender._render` is called with the name of the discovered
section to further dispatch processing to the associated section
rendering function. If an associated function to the section does not
exist the default is to use :func:`~.rubric`.

Section rendering function
##########################

The rendering fuctions will use the utility methods of the the
DocRender instance to extract the section block. Depedending on the
implementation :meth:`~DocRender.extract_paragraph` is called to
return the paragraph for further processing or
:meth:`~DocRender.extract_items` is called to return the list of
:class:`~.Item` instances. When a list of :class:`~.Item` is collected
the section the rendering function will produce the updated rst
docstring using the appropriate :class:`~.Renderer`.

Item
####

:class:`Item` instances contain the ``term``, ``classfier(s)`` and
``definition`` information of items in a section. Each :class:`Item` type
knows how to parse a set of lines grouping and filtering the information
ready to be rendered into sphinx friendly rst.

Renderer
########

The :class:`Renderer` is used by the section renderer functions to render
a previously contructed :class:`Item` into sphinx friently rst.
