Old Style
#########

The base implementation of Sectiondoc provides rendering for class and
function/method doc-strings. A number of known (i.e. predefined) sections are
processed by the :func:`~.function_section` and :func:`~FunctionDoc` classes
and all unknown sections are rendered using the ``.. rubric::`` directive by
default.

For class objects the **old style** renders three types of sections:

========== ================================ ============ === =====================
Heading    Description                      Item         Max Rendered as
========== ================================ ============ === =====================
Methods    Class methods with summary       MethodItem   --  Table with links to
                                                             the method
Attributes Class attributes and their usage Attribute    --  Sphinx attributes
Arguments  function arguments and type      ArgumentItem --  Parameters field list
Parameters function arguments and type      ArgumentItem --  Parameters field list
Notes      Useful notes                     paragraph    1   Note admonition
========== ================================ ============ === =====================

For functions the **old style** renders four types of sections:

========== =========================== ============ === =====================
Heading    Description                 Item         Max Rendered as
========== =========================== ============ === =====================
Arguments  function arguments and type ArgumentItem --  Parameters field list
Parameters function arguments and type ArgumentItem --  Parameters field list
Returns    Return value                ListItem     --  Unordered list
Raises     Raised exceptions           ListItem     --  Unordered list
Yileds     Yield values                ListItem     --  Unordered list
Notes      Useful notes                paragraph    1   Note admonition
========== =========================== ============ === =====================


layout rules
************

To be able to detect and render the sections properly the docstrings should follow
the following rules:

- Between the section header and the first section item there can be at
  most only one empty line.

- The end of the section is designated by one of the following:

  - The allowed number of items by the section has been parsed.
  - Two consecutive empty lines are found.
  - The line is not identified as a possible header of the section item.

  .. hint:: Please check the doc-string of the specific definition item
     class to have more information regarding the  valid item header
     format.

Examples
********

Argument sections
^^^^^^^^^^^^^^^^^
::

    Arguments
    ---------
    new_lines : list
        The list of lines to insert

    index : int
        Index to start the insertion


.. automethod:: sectiondoc.styles.doc_render.DocRender.insert_lines
    :noindex:


Attribute sections
------------------
::

    Attributes
    ----------
    docstring : list
        A list of strings (lines) that holds docstrings. The lines are changed
        inplace.

    index : int
        The zero-based line number of the docstring that is currently
        processed.

    sections : dict
        The sections that will be detected and rendered. The dictionary
        maps the section headers for detection to a tuple containing
        the section rendering function and optional values for the item
        renderer and parser.

.. autoclass:: sectiondoc.styles.doc_render.DocRender
    :noindex:
    :no-members:

Returns sections
----------------
::

    Returns
    -------
    result : list
        A new list of left striped strings.

.. autofunction:: sectiondoc.util.remove_indent
    :noindex:

Raises section
--------------

.. todo:: Add example


Notes
-----
::

    Notes
    -----
    Empty strings are not changed.

.. autofunction:: sectiondoc.util.add_indent
    :noindex:
