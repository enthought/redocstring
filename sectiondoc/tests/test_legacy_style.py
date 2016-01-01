from sectiondoc.styles.legacy import class_section, function_section
from sectiondoc.tests._compat import unittest


class TestLegacyStyleClass(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_refactor_attributes(self):
        docstring =\
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
"""

        rst = \
            """Base abstract docstring refactoring class.

The class' main purpose is to parse the dosctring and find the
sections that need to be refactored. It also provides a number of
methods to help with the refactoring. Subclasses should provide
the methods responsible for refactoring the sections.

.. attribute:: docstring
    :annotation: = list

    A list of strings (lines) that holds docstrings

.. attribute:: index
    :annotation: = int

    The current zero-based line number of the docstring that is
    proccessed.

"""

        docstring_lines = docstring.splitlines()
        class_doc = class_section(docstring_lines)
        class_doc.parse()
        output = '\n'.join(docstring_lines)
        self.assertMultiLineEqual(rst, output)

    def test_refactor_methods(self):
        docstring = \
            """ This is a sample class docstring

Methods
-------
extract_fields(indent='', field_check=None)
    Extract the fields from the docstring

get_field()
    Get the field description.

get_next_paragraph()
    Get the next paragraph designated by an empty line.

"""

        rst = \
            """ This is a sample class docstring


====================================================================  ===================================================
Method                                                                Description
====================================================================  ===================================================
:meth:`extract_fields(indent='', field_check=None) <extract_fields>`  Extract the fields from the docstring
:meth:`get_field() <get_field>`                                       Get the field description.
:meth:`get_next_paragraph() <get_next_paragraph>`                     Get the next paragraph designated by an empty line.
====================================================================  ===================================================

"""  # noqa

        docstring_lines = docstring.splitlines()
        class_doc = class_section(docstring_lines)
        class_doc.parse()
        output = '\n'.join(docstring_lines)
        self.assertMultiLineEqual(rst, output)

    def test_refactor_notes(self):
        docstring1 =\
            """ This is a sample class docstring

Notes
-----
This is the test.
Wait we have not finished.

This is not a note.
"""

        docstring2 =\
            """ This is a sample class docstring

Notes
-----

This is the test.
Wait we have not finished.

This is not a note.
"""

        rst = \
            """ This is a sample class docstring

.. note::
    This is the test.
    Wait we have not finished.

This is not a note.
"""

        docstring_lines = docstring1.splitlines()
        class_doc = class_section(docstring_lines)
        class_doc.parse()
        output = '\n'.join(docstring_lines) + '\n'
        self.assertMultiLineEqual(rst, output)

        docstring_lines = docstring2.splitlines()
        class_doc = class_section(docstring_lines)
        class_doc.parse()
        output = '\n'.join(docstring_lines) + '\n'
        self.assertMultiLineEqual(rst, output)


class TestOldStyleFunction(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_refactor_returns(self):
        docstring = \
            """ This is a sample function docstring.

Returns
-------
myvalue : list
    A list of important values.
    But we need to say more things about it.
"""

        rst = \
            """ This is a sample function docstring.

:returns:
    **myvalue** (*list*) --
    A list of important values.
    But we need to say more things about it.

"""

        docstring_lines = docstring.splitlines()
        function_doc = function_section(docstring_lines)
        function_doc.parse()
        output = '\n'.join(docstring_lines)
        self.assertMultiLineEqual(rst, output)

    def test_refactor_raises(self):
        docstring = \
            """ This is a sample function docstring.

Raises
------
TypeError :
    This is the first paragraph of the description.
    More description.

ValueError :
    Description of another case where errors are raised.
"""

        rst = \
            """ This is a sample function docstring.

:raises:
    - **TypeError** --
      This is the first paragraph of the description.
      More description.

    - **ValueError** --
      Description of another case where errors are raised.

"""

        docstring_lines = docstring.splitlines()
        function_doc = function_section(docstring_lines)
        function_doc.parse()
        output = '\n'.join(docstring_lines)
        self.assertMultiLineEqual(rst, output)

    def test_refactor_arguments(self):
        docstring =\
            """ This is a sample function docstring

Arguments
---------
inputa : str
    The first argument holds the first input!.

    This is the second paragraph.

inputb : float
    The second argument is a float.
    the default value is 0.

    .. note:: this is an optional value.
"""

        rst = \
            """ This is a sample function docstring

:param inputa:
    The first argument holds the first input!.

    This is the second paragraph.
:type inputa: str
:param inputb:
    The second argument is a float.
    the default value is 0.

    .. note:: this is an optional value.
:type inputb: float

"""

        docstring_lines = docstring.splitlines()
        function_doc = function_section(docstring_lines)
        function_doc.parse()
        output = '\n'.join(docstring_lines) + '\n'
        self.assertMultiLineEqual(rst, output)

    def test_refactor_strange_arguments(self):
        docstring = \
            """ This is a sample function docstring

Parameters
----------
*args :
    Positional arguments with which this constructor was called
    from the enaml source code.

**kwards :
    Keyword arguments with which this constructor was called
    from the enaml source code.

from_ :
    Arguments with trailing underscore.
"""
        rst = \
            """ This is a sample function docstring

:param \*args:
    Positional arguments with which this constructor was called
    from the enaml source code.
:param \*\*kwards:
    Keyword arguments with which this constructor was called
    from the enaml source code.
:param from\_:
    Arguments with trailing underscore.

"""

        docstring_lines = docstring.splitlines()
        function_doc = function_section(docstring_lines)
        function_doc.parse()
        output = '\n'.join(docstring_lines) + '\n'
        self.assertMultiLineEqual(rst, output)

    def test_refactor_notes(self):
        docstring = \
            """ This is a sample function docstring.

Notes
-----
This is the test.
Wait we have not finished.

This should not be included.
"""

        rst = \
            """ This is a sample function docstring.

.. note::
    This is the test.
    Wait we have not finished.

This should not be included.
"""

        docstring_lines = docstring.splitlines()
        function_doc = function_section(docstring_lines)
        function_doc.parse()
        output = '\n'.join(docstring_lines) + '\n'
        self.assertMultiLineEqual(rst, output)

    def test_docstring_cases_1(self):
        docstring1 = \
            """ Sets the selection to the bounds of start and end.

If the indices are invalid, no selection will be made,
and any current selection will be cleared.

Arguments
---------
start : Int
    The start selection index, zero based.

end : Int
    The end selection index, zero based.

Returns
-------
result : None
"""

        docstring2 = \
            """ Sets the selection to the bounds of start and end.

If the indices are invalid, no selection will be made,
and any current selection will be cleared.

Arguments
---------
start : Int
    The start selection index, zero based.
end : Int
    The end selection index, zero based.

Returns
-------
result : None
"""

        rst = \
            """ Sets the selection to the bounds of start and end.

If the indices are invalid, no selection will be made,
and any current selection will be cleared.

:param start:
    The start selection index, zero based.
:type start: Int
:param end:
    The end selection index, zero based.
:type end: Int

:returns:
    **result** (*None*)

"""

        docstring_lines = docstring1.splitlines()
        function_doc = function_section(docstring_lines)
        function_doc.parse()
        output = '\n'.join(docstring_lines)
        self.assertMultiLineEqual(rst, output)

        docstring_lines = docstring2.splitlines()
        function_doc = function_section(docstring_lines)
        function_doc.parse()
        output = '\n'.join(docstring_lines)
        self.assertMultiLineEqual(rst, output)

    def test_docstring_cases_2(self):

        docstring = \
            """ Verify that the requested attribute is properly set

The method compares the attribute value in the Enaml object and
check if it is synchronized with the toolkit widget. The component
attribute is retrieved directly while the widget value is retrieved
through a call to a method function in the test case.

Arguments
---------
component : enaml.widgets.component.Component
    The Enaml component to check.

attribute_name : str
    The string name of the Enaml attribute to check.

value :
    The expected value.

.. note:: It is expected that the user has defined an appropriate
    method get_<attribute_name>(widget) or the extentded version
    get_<attribute_name>(component, widget) in the current test
    case. The extended signature is commonly used because additional
    information on the component's attributes is required to return
    a sensible result (e.g. the component uses Converters to set
    and retrieve the value of the attribute). The assert method
    The get methods can raise assertion errors when it is not
    possible to retrieve a sensible value for the attribute.

"""

        rst = \
            """ Verify that the requested attribute is properly set

The method compares the attribute value in the Enaml object and
check if it is synchronized with the toolkit widget. The component
attribute is retrieved directly while the widget value is retrieved
through a call to a method function in the test case.

:param component:
    The Enaml component to check.
:type component: enaml.widgets.component.Component
:param attribute_name:
    The string name of the Enaml attribute to check.
:type attribute_name: str
:param value:
    The expected value.

.. note:: It is expected that the user has defined an appropriate
    method get_<attribute_name>(widget) or the extentded version
    get_<attribute_name>(component, widget) in the current test
    case. The extended signature is commonly used because additional
    information on the component's attributes is required to return
    a sensible result (e.g. the component uses Converters to set
    and retrieve the value of the attribute). The assert method
    The get methods can raise assertion errors when it is not
    possible to retrieve a sensible value for the attribute.

"""

        docstring_lines = docstring.splitlines()
        function_doc = function_section(docstring_lines)
        function_doc.parse()
        output = '\n'.join(docstring_lines) + '\n'
        self.assertMultiLineEqual(rst, output)


if __name__ == '__main__':
    unittest.main()
