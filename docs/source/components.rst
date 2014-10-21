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
either a list of items or one or more definition items. In general, The number
and format of these items depends on the type of section that is currently
parsed.

Definition list
^^^^^^^^^^^^^^^

Two of the most common formats are described bellow:

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
