Architecture
************

.. warning:: Since and due to writing this part of the documentation a number
    of improvements have become apparent and will be implemented in the next
    version of refactordoc (i.e. 0.4). Please see the todo section for more
    info.

The are three different parts in the pipeline of **refactordoc**.

(i) The autodoc event hook and object refactoring dispatch;
(ii) The docstring section detection and method dispatching and;
(iii) The second component parsing and refactor of the detected sections;

The entry function
##################

The entry function ``setup`` is located in the ``__init__.py`` file. Through
the setup function refactor doc is loading the autodoc extention and hooks
the :func:`~refactordoc.refactor_docstring` function to the
``autodoc-process-docstring`` event.

The :func:`~refactordoc.refactor_docstring` function receives the  list of
lines that compose the dostrings and based on the ``object`` initializes a
new class instance to do the main work. The final item in the process is to
execute the parse method of the created class.

The refactoring class
#####################

The refactoring classes are responsible for doing the actual work. These classes
are derived from the :class:`~refactordoc.BaseDoc` class. After initialization
refactoring takes place by executing the :meth:`~refactordoc.BaseDoc.parse`
method. The method looks for section headers by parsing the lines of the
docstring. For each section that is discovered the
:meth:`~refactordoc.BaseDoc._refactor` method is called with the name of
the discovered section to dispatch processing to the associated refactoring
method. The dispatcher constructs the name of the refactoring function by
looking up the ``headers`` dictionary for a key equal to the header string
found. If a key is found then the refactoring method name is composed from the
prefix ``_header_`` and the retrieved value. If a key with the header name is
not found then the default :meth:`~refactordoc.BaseDoc._refactor_header` is
used.

The refactoring methods
#######################

Depending on the section the associated method parses and extracts the section
definition block using the provided by the :class:`~refactordoc.BaseDoc` class
utility methods.

When the definition block is a paragraph the
:meth:`~refactordoc.BaseDoc.extract_paragraph` will return the paragraph for
further processing. When the definition block is a list of definition items.
These items are parsed and extracted (i.e removed from the docstring) with the
help of the :meth:`~refactordoc.BaseDoc.extract_items` and a
:class:`~refactordoc.defintion_items.DefintionItem` (or a subclass). The list
of items that is returned holds all the information to produce a sequence of
sphinx friendly rst.

After collecting the information in the section the refactoring method is
ready to produce the updated rst and return a list of lines to the
dispatching method so that they can be re-inserted in the docstring.
