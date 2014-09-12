# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  file: test_base_doc.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from refactordoc.base_doc import BaseDoc
from refactordoc.tests._compat import unittest


class TestBaseDoc(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_refactor_header(self):
        docstring =\
""" This is a sample docstring.

My Header
---------
This is just some sample text.
"""

        rst =\
""" This is a sample docstring.

.. rubric:: My Header

This is just some sample text.
"""
        docstring_lines = docstring.splitlines()
        base_doc = BaseDoc(docstring_lines)
        base_doc.parse()
        output = '\n'.join(docstring_lines) + '\n'
        self.assertMultiLineEqual(rst, output)

    def test_refactor_complex_header(self):
        docstring =\
""" This is a sample docstring.

Input\\Output header
-------------------

This is just some sample text.
"""

        rst =\
""" This is a sample docstring.

.. rubric:: Input\\\\Output header

This is just some sample text.
"""
        docstring_lines = docstring.splitlines()
        base_doc = BaseDoc(docstring_lines)
        base_doc.parse()
        output = '\n'.join(docstring_lines) + '\n'
        self.assertMultiLineEqual(rst, output)

if __name__ == '__main__':
    unittest.main()
