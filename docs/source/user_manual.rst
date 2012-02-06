User Manual
###########

RefactorDoc is a sphinx extension is designed to re-factor the doc-strings of
python objects. The sections are replaced (in-place) by sphinx friendly rst and
the rest of the doc-string is left untouched. Thus the original form remains as
intended by the author.

Summary
*******

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


Section components
******************

Each section is composed into a number of components these components are
described below.

Section header
^^^^^^^^^^^^^^

The start of the section is designated with the section header, which is
a standard rst header. The underline is however restricted to using only
``-`` or ``=``::

    Section
    -------

and::

    Section
    =======

Each section header is followed by a section definition block which can be
either a list of items or one or more definition items.

Definition list
^^^^^^^^^^^^^^^

In general, The number and format of these items depends on the type of
section that is currently parsed. Two of the most common formats are described
bellow:

The *standard definition item* format is based on the item of a variation
of the definition list item as it defined in `restructured text
<http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#sections>`_

::

    +-------------------------------------------------+
    | term [ " : " classifier [ " or " classifier] ]  |
    +--+----------------------------------------------+---+
       | definition                                       |
       | (body elements)+                                 |
       +--------------------------------------------------+

where ``<term>`` is the single word (e.g. my_field) and
``<definition>`` is a indented block of rst code. The item header can
optionally include the ``<classifier>`` attribute. This type of item is
commonly used to describe class attributes and function arguments. In this
documentation we will refer to this format as `variable` item to avoid
confusion with sphinx directives.

A similar definition item format is the method item where the item header is
composed of a function signature::

    +------------------------------+
    | term "(" [  classifier ] ")" |
    +--+---------------------------+---+
       | definition                    |
       | (body elements)+              |
       +-------------------------------+

This item is commonly used to describe provided functions (or methods) and
thus is referred to as the `method item`. The
``<classifier>`` in this case is a list of arguments as it appears in the
signature and ``<definition>`` the method summary (one sentence). All
`method` fields should be separated by a single empty line.

Paragraph
^^^^^^^^^

Instead of a list of items the section can contain a paragraph::

    +-------------------------+
    | definition              |
    | (body elements)+        |
    +-------------------------+

This type of field is used for information sections like ``Notes``.

.. note:: Currently the ``<paragraph>`` is a single unindented block with no
    empty lines. However, this will probably should change in future
    versions of RefactorDoc.

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

