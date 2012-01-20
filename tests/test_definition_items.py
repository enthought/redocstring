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
from refactordoc.definition_items import DefinitionItem

class TestDefinitionItem(unittest.TestCase):

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
                                             ['    Definition.']))

        item = DefinitionItem.parse(['term',
                                     '    Definition, paragraph 1.',
                                     '',
                                     '    Definition, paragraph 2.'])
        self.assertEqual(item, DefinitionItem('term', '',
                                              ['    Definition, paragraph 1.',
                                               '',
                                               '    Definition, paragraph 2.']))

        item = DefinitionItem.parse(['term : classifier',
                                     '    Definition.'])
        self.assertEqual(item, DefinitionItem('term', 'classifier',
                                              ['    Definition.']))

    def test_to_rst(self):
        item = DefinitionItem('lines', 'list',
                             ['    A list of string lines rendered in rst.'])
        rendered = '\n'.join(item.to_rst())
        rst ="""\
lines

    *(list)* --
    A list of string lines rendered in rst."""
        self.assertMultiLineEqual(rendered, rst)

if __name__ == '__main__':
    unittest.main()
