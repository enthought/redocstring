# -*- coding: UTF-8 -*-
#------------------------------------------------------------------------------
#  file: test_line_functions.py
#  License: LICENSE.TXT
#  Author: Ioannis Tziakos
#
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import unittest
from refactordoc.definition_items import (DefinitionItem, AttributeItem,
                                          ArgumentItem)

class TestDefinitionItem(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_is_definition(self):
        self.assertTrue(DefinitionItem.is_definition("term"))
        self.assertFalse(DefinitionItem.is_definition("term "))
        self.assertFalse(DefinitionItem.is_definition("term :"))
        self.assertFalse(DefinitionItem.is_definition("term : "))
        self.assertTrue(DefinitionItem.is_definition("term : classifier"))
        self.assertFalse(DefinitionItem.is_definition(":term : classifier"))
        self.assertFalse(DefinitionItem.is_definition("term : classifier:"))

    def test_parse(self):
        item = DefinitionItem.parse(['term',
                                     '    Definition.'])
        self.assertEqual(item, DefinitionItem('term', '',
                                             ['Definition.']))

        item = DefinitionItem.parse(['term',
                                     '    Definition, paragraph 1.',
                                     '',
                                     '    Definition, paragraph 2.'])
        self.assertEqual(item, DefinitionItem('term', '',
                                              ['Definition, paragraph 1.',
                                               '',
                                               'Definition, paragraph 2.']))

        item = DefinitionItem.parse(['term : classifier',
                                     '    Definition.'])
        self.assertEqual(item, DefinitionItem('term', 'classifier',
                                              ['Definition.']))

        item = DefinitionItem.parse(['term : classifier',
                                     '    Block.',
                                     '        Definition.'])
        self.assertEqual(item, DefinitionItem('term', 'classifier',
                                              ['Block.',
                                               '    Definition.']))

#    def test_parse_errors(self):


    def test_to_rst(self):
        rst ="""\
lines

    *(list)* --
    A list of string lines rendered in rst.
"""
        item = DefinitionItem('lines', 'list',
                             ['A list of string lines rendered in rst.'])
        rendered = '\n'.join(item.to_rst())
        self.assertMultiLineEqual(rendered, rst)


class TestAttributeItem(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_to_rst(self):
        # with annotation
        rst ="""\
.. attribute:: indent
    :annotation: = int

    The indent to use for the description block.
"""
        item = AttributeItem('indent', 'int',
                             ['    The indent to use for the description block.'])
        rendered = '\n'.join(item.to_rst())
        self.assertMultiLineEqual(rendered, rst)

        # without annotation
        rst ="""\
.. attribute:: indent

    The indent to use for the description block.
"""
        item = AttributeItem('indent', '',
                             ['    The indent to use for the description block.'])
        rendered = '\n'.join(item.to_rst())
        self.assertMultiLineEqual(rendered, rst)

class TestArgumentItem(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_to_rst(self):
        # with annotation
        rst ="""\
:param indent: The indent to use for the description block.

    This is the second paragraph of the argument definition.
:type indent: int
"""
        item = ArgumentItem('indent', 'int',
            ['    The indent to use for the description block.',
             ''
             '    This is the second paragraph of the argument definition.'])
        rendered = '\n'.join(item.to_rst())
        self.assertMultiLineEqual(rendered, rst)

if __name__ == '__main__':
    unittest.main()
