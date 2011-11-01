User Manual
===========

RefactorDoc refactors the docstrings of classes and functions. However
unlike numpydoc only sections are replaced (inplace) by sphinx friendly
rst and the rest of the docstring is left untouched. Thus the original
form remains untouched.

To help the extension module to detect those sections the docstring author
needs to follow the following rules:

    - Sections are defined using ``-`` or ``=``::

        Section
        -------

      or::

        Section
        =======

      Each section is followed by on or more fields. Which format are
      accepted depend on the type of section that is currently parsed.

      .. note:: Both section definitions will be treated the same and
        there is no concept of subsection (not yet!).

    - Field blocks (i.e. the items that belong to each section) start
      immediately after section definition with not indention. The fields
      can take the following formats::

        Section
        -------
        <name> : [<type>]
            [<description>]

      where ``<name>`` is the single word (e.g. my_field) and
      ``<description>`` is a indented block of rst code. The ``<type>``
      attribute is optional. This type of field is commonly used to
      describe class attributes and function arguments. In this
      documentation we will refer to this format as `variable` field. All
      `variable` fields should be separated by a single empty line.

      A similar field format is::

        Section
        -------
        <signature>
            [<description>]

      This field is commonly used to describe methods that are provided by
      a class ans thus is refered to as the `method` field. The
      ``<signature>`` in this case is a method signature and
      ``<description>`` the method summary (one sentence). All
      `method` fields should be separated by a single empty line.

      Finally the `paragraph` field, defined as::

        Section
        -------
        [paragraphs]

      This type of field is used for info sections like ``Notes``.

      .. note:: Currently the ``<paragraph>`` is a single unindented block
        with no empty lines. However, this should change in the next
        versions of RefactorDoc.

Classes
-------

The current parser extension supports the following headings for classes:

========== ================= ==========
Heading    Description       Field type
========== ================= ==========
Methods    Class methods     method
Attributes Set of attributes variable
Notes      Useful notes      paragraph
See Also   References        paragraph
========== ================= ==========

Example
~~~~~~~

::

    """Base abstract docstring refactoring class.

    The class' main purpose is to parse the dosctring and find the
    sections that need to be refactored. It also provides a number of
    methods to help with the refactoring. Subclasses should provide
    the methods responsible for refactoring the sections.

    Attributes
    ----------
    docstring : list
        A list of strings (lines) that holds docstrings

    index : int
        The current zero-based line number of the docstring that is
        proccessed.

    verbose : bool
        When set the class prints a lot of info about the proccess
        during runtime.

    headers : dict
        The sections that the class refactors. Each entry in the
        dictionary should have as key the name of the section in the
        form that it appears in the docstrings. The value should be
        the postfix of the method, in the subclasses, that is
        responsible for refactoring (e.g. {'Methods': 'method'}).

    Methods
    -------
    extract_fields(indent='', field_check=None)
        Extract the fields from the docstring

    get_field()
        Get the field description.

    get_next_paragraph()
        Get the next paragraph designated by an empty line.

    is_section()
        Check if the line defines a section.

    parse_field(lines)
        Parse a field description.

    peek(count=0)
        Peek ahead

    read()
        Return the next line and advance the index.

    insert_lines(lines, index)
        Insert refactored lines

    remove_lines(index, count=1)
        Removes the lines for the docstring

    seek_to_next_non_empty_line()
        Goto the next non_empty line
    """

.. currentmodule:: refactor_doc

The output can be seen at :func:`~BaseDocstring`

Functions
---------

The current parser extension supports the following headings for functions:

========= ==========================================================
Heading   Description
========= ==========================================================
Arguments Set of function arguments and their usage
Returns   Return values of the function
Raises    Errors and the cases in which they are raised
Yields    Successive results of the generator
========= ==========================================================


Example
~~~~~~~

::

    """Extract the fields from the docstring

        Parse the fields into tuples of name, type and description in a
        list of strings. The strings are also removed from the list.

        Arguments
        ---------
        indent : str, optional
            the indent argument is used to make sure that only the lines
            with the same indent are considered when checking for a
            field header line. The value is used to define the field
            checking function.

        field_check : function
            Optional function to use for checking if the next line is a
            field. The signature of the function is ``foo(line)`` and it
            should return ``True`` if the line contains a valid field
            The default function is checking for fields of the following
            formats::

                <name> : <type>
                <name> :

            Where the name has to be one word.

        Returns
        -------
        parameters : list of tuples
            list of parsed parameter tuples as returned from the
            :meth:`~BaseDocstring.parse_field` method.

        """

The output can be seen at
:func:`~BaseDocstring.extract_fields`