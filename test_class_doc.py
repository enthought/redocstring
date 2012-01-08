#------------------------------------------------------------------------------
#  file: test_refactor_doc.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import unittest
from class_doc import ClassDoc


class TestClassDoc(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def tearDown(self):
        pass

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

        *(list)*
        A list of strings (lines) that holds docstrings

    .. attribute:: index

        *(int)*
        The current zero-based line number of the docstring that is
        proccessed.
    """

        docstring_lines = docstring.splitlines()
        ClassDoc(docstring_lines)
        output = '\n'.join(docstring_lines)
        self.assertMultiLineEqual(rst, output)

    def test_refactor_methods(self):
        docstring =\
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

    ==================================================================== ===================================================
    Methods                                                              Description
    ==================================================================== ===================================================
    :meth:`extract_fields(indent='', field_check=None) <extract_fields>` Extract the fields from the docstring
    :meth:`get_field() <get_field>`                                      Get the field description.
    :meth:`get_next_paragraph() <get_next_paragraph>`                    Get the next paragraph designated by an empty line.
    ==================================================================== ===================================================

    """

        docstring_lines = docstring.splitlines()
        ClassDoc(docstring_lines)
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
        ClassDoc(docstring_lines)
        output = '\n'.join(docstring_lines)
        self.assertMultiLineEqual(rst, output)

        docstring_lines = docstring2.splitlines()
        ClassDoc(docstring_lines)
        output = '\n'.join(docstring_lines)
        self.assertMultiLineEqual(rst, output)

if __name__ == '__main__':
    unittest.main()
