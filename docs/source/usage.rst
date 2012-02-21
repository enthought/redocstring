Default refactoring
*******************

The base implementation of RefactorDoc provides refactoring for class and
function doc-strings. A number of known (i.e. predefined) sections are processed
by the ClassDoc and FunctionDoc classes and all unknown sections are re-factored
using the ``.. rubric::`` directive by default.

For class objects the :class:`~refactordoc.class_doc.ClassDoc` includes code to
re-factor three types of sections.

========== ================================ ========== === ====================
Heading    Description                      Item       Max Rendered as
========== ================================ ========== === ====================
Methods    Class methods with summary       MethodItem --  Table with links to
                                                           the method
Attributes Class attributes and their usage Attribute  --  Sphinx attributes
Notes      Useful notes                     paragraph  1   Note admonition
========== ================================ ========== === ====================

For function objects the :class:`~refactordoc.function_doc.FunctionDoc` includes
code to re-factor three types of sections.

========= =========================== ============ === =====================
Heading   Description                 Item         Max Rendered as
========= =========================== ============ === =====================
Arguments function arguments and type ArgumentItem --  Parameters field list
Returns   Return value                ListItem     --  Unordered list
Raises    Raised exceptions           ListItem     --  Unordered list
Notes     Useful notes                paragraph    1   Note admonition
========= =========================== ============ === =====================


Usage rules
***********

To be able to re-factor the sections properly the doc-strings should follow
theses rules:

.. admonition:: Rules

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
    """

.. automethod:: refactordoc.base_doc.BaseDoc.insert_lines
    :noindex:


Method sections
^^^^^^^^^^^^^^^
::

    Methods
    -------
    _refactor_attributes(self, header):
        Re-factor the attributes section to sphinx friendly format.

    _refactor_methods(self, header):
        Re-factor the methods section to sphinx friendly format.

    _refactor_notes(self, header):
        Re-factor the note section to use the rst ``.. note`` directive.


.. note:: The table that is created in this example does not have the links
    enabled because the methods are not rendered by autodoc (the
    ``:no-members`` option is set).

.. autoclass:: refactordoc.class_doc.ClassDoc
    :noindex:
    :no-members:

Attribute sections
------------------
::

    Attributes
    ----------
    docstring : list
        A list of strings (lines) that holds doc-strings

    index : int
        The current zero-based line number of the doc-string that is currently
        processed.

    headers : dict
        The sections that the class re-factors. Each entry in the
        dictionary should have as key the name of the section in the
        form that it appears in the doc-strings. The value should be
        the postfix of the method, in the subclasses, that is
        responsible for refactoring (e.g. {'Methods': 'method'}).

.. autoclass:: refactordoc.base_doc.BaseDoc
    :noindex:
    :no-members:

Returns sections
----------------
::

    Returns
    -------
    result : list
        A new list of left striped strings.

.. autofunction:: refactordoc.line_functions.remove_indent
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

.. autofunction:: refactordoc.line_functions.add_indent
    :noindex:

