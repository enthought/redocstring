Default
#######

Default style is a stricter implementation of legacy_ where the definition item
description is parsed using the :class:`~sectiondoc.items.DefinitionItem` which
follows the ``rst`` definition more closely.

For class objects the **default** renders 5 types of sections:

==========  ================================  ==============  ===  =====================
Heading     Description                       Parse as        Max  Rendered as
==========  ================================  ==============  ===  =====================
Attributes  Class attributes and their usage  DefinitionItem  --   Sphinx attributes
Arguments   function arguments and type       DefinitionItem  --   Parameters field list
Parameters  function arguments and type       DefinitionItem  --   Parameters field list
Methods     Class methods with summary        MethodItem      --   Table with links to
                                                                   the methods
Notes       Useful notes                      paragraph       1    Note admonition
==========  ================================  ==============  ===  =====================

For functions the **default** renders six types of sections:

==========  ===========================  ==============  ===  =====================
Heading     Description                  Parse as        Max  Rendered as
==========  ===========================  ==============  ===  =====================
Arguments   function arguments and type  DefinitionItem  --   Parameters field list
Parameters  function arguments and type  DefinitionItem  --   Parameters field list
Returns     Return value                 DefinitionItem  --   Unordered list
Raises      Raised exceptions            DefinitionItem  --   Unordered list
Yields      Yield values                 DefinitionItem  --   Unordered list
Notes       Useful notes                 paragraph       1    Note admonition
==========  ===========================  ==============  ===  =====================

.. note::
   All other sections are rendered using the ``.. rubric::`` directive by
   default.

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

  .. hint:: Please check the docstring of the specific definition item
     class to have more information regarding the valid item header
     format.

Examples
********

Argument section
^^^^^^^^^^^^^^^^
::

   Arguments
   ---------
   inputa : str
       The first argument holds the first input!.

       This is the second paragraph.

   inputb : float : int
       The second argument is a float.
       the default value is 0.

       .. note:: this is an optional value.


.. function:: arguments(inputa, inputb)
   :noindex:

   :param inputa:
      The first argument holds the first input!.

      This is the second paragraph.
   :type inputa: str
   :param inputb:
      The second argument is a float.
      the default value is 0.

      .. note:: this is an optional value.
   :type inputb: float or int


Attribute sections
^^^^^^^^^^^^^^^^^^
::

    Attributes
    ----------
    docstring : list
        A list of strings (lines) that holds docstrings. The lines are
        changed inplace.

    index : int
        The zero-based line number of the docstring that is currently
        processed.

.. class:: Attributes()
   :noindex:

   .. attribute:: docstring
       :noindex:
       :annotation: = list

       A list of strings (lines) that holds docstrings

   .. attribute:: index
       :noindex:
       :annotation: = int

       The current zero-based line number of the docstring that is
       proccessed.


Returns sections
^^^^^^^^^^^^^^^^
::

   Returns
   -------
   myvalue : list
       A list of important values.
       But we need to say more things about it.

.. function:: returns()
   :noindex:

   :returns:
       **myvalue** (*list*) --
       A list of important values.
       But we need to say more things about it.

Raises section
^^^^^^^^^^^^^^
::

   Raises
   ------
   TypeError
       This is the first paragraph of the description.
       More description.

   ValueError
       Description of another case where errors are raised.


.. function:: raises()
   :noindex:

   :raises:
       - **TypeError** --
	 This is the first paragraph of the description.
	 More description.

       - **ValueError** --
	 Description of another case where errors are raised.

Method section
^^^^^^^^^^^^^^
::

   Methods
   -------
   extract_fields(indent='', field_check=None)
       Extract the fields from the docstring

   get_field()
       Get the field description.

   get_next_paragraph()
       Get the next paragraph designated by an empty line.


.. class:: MyClass()
   :noindex:

   ====================================================================  ===================================================
   Method                                                                Description
   ====================================================================  ===================================================
   :meth:`extract_fields(indent='', field_check=None) <extract_fields>`  Extract the fields from the docstring
   :meth:`get_field() <get_field>`                                       Get the field description.
   :meth:`get_next_paragraph() <get_next_paragraph>`                     Get the next paragraph designated by an empty line.
   ====================================================================  ===================================================


Notes
^^^^^
::

    Notes
    -----
    Empty strings are not changed.


.. note:: Empty strings are not changed.
