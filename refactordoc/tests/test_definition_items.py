# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  file: test_line_functions.py
#  License: LICENSE.TXT
#  Author: Ioannis Tziakos
#
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from refactordoc.items.definition_item import DefinitionItem
from refactordoc.items.method_item import MethodItem
from refactordoc.items.argument_item import ArgumentItem
from refactordoc.items.attribute_item import AttributeItem
from refactordoc.items.list_item import ListItem
from refactordoc.items.table_row_item import TableRowItem
from refactordoc.tests._compat import unittest


class TestDefinitionItem(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_is_definition(self):
        self.assertFalse(DefinitionItem.is_definition("term"))
        self.assertFalse(DefinitionItem.is_definition("term "))
        self.assertTrue(DefinitionItem.is_definition("term :"))
        self.assertTrue(DefinitionItem.is_definition("term : "))
        self.assertTrue(DefinitionItem.is_definition("term : classifier"))
        self.assertFalse(DefinitionItem.is_definition(":term : classifier"))
        self.assertFalse(DefinitionItem.is_definition("term : classifier:"))

        # special cases
        header_with_object = 'component : class.component.instance'
        self.assertTrue(DefinitionItem.is_definition(header_with_object))

        header_with_trait = 'properies : Dict(Str, Any)'
        self.assertTrue(DefinitionItem.is_definition(header_with_trait))

        header_with_or = 'item : ModelIndex or None'
        self.assertTrue(DefinitionItem.is_definition(header_with_or))

    def test_parse(self):
        item = DefinitionItem.parse(['term', '    Definition.'])
        self.assertEqual(item, DefinitionItem('term', [''], ['Definition.']))

        item = DefinitionItem.parse([
            'term', '    Definition, paragraph 1.',
            '', '    Definition, paragraph 2.'])
        self.assertEqual(
            item,
            DefinitionItem(
                'term', [''], [
                    'Definition, paragraph 1.',
                    '',
                    'Definition, paragraph 2.']))

        item = DefinitionItem.parse(['term :', '    Definition.'])
        self.assertEqual(item, DefinitionItem('term', [''], ['Definition.']))

        item = DefinitionItem.parse(['term : classifier', '    Definition.'])
        self.assertEqual(
            item, DefinitionItem('term', ['classifier'], ['Definition.']))


        item = DefinitionItem.parse(
            ['term : classifier or classifier', '    Definition.'])
        self.assertEqual(
            item,
            DefinitionItem('term',
                ['classifier','classifier'], ['Definition.']))

        item = DefinitionItem.parse(
            ['term : classifier', '    Block.', '        Definition.'])
        self.assertEqual(
            item, DefinitionItem(
                'term', ['classifier'], ['Block.', '    Definition.']))

    def test_to_rst(self):
        rst = """\
lines

    *(list)* --
    A list of string lines rendered in rst.
"""
        item = DefinitionItem(
            'lines', ['list'], ['A list of string lines rendered in rst.'])
        rendered = '\n'.join(item.to_rst())
        self.assertMultiLineEqual(rst, rendered)


class TestAttributeItem(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_to_rst(self):
        # with annotation
        rst = """\
.. attribute:: indent
    :annotation: = int

    The indent to use for the description block.
"""
        item = AttributeItem('indent', ['int'],
                             ['The indent to use for the description block.'])
        rendered = '\n'.join(item.to_rst())
        self.assertMultiLineEqual(rst, rendered)

        # without annotation
        rst = """\
.. attribute:: indent

    The indent to use for the description block.
"""
        item = AttributeItem('indent', [],
                             ['The indent to use for the description block.'])
        rendered = '\n'.join(item.to_rst())
        self.assertMultiLineEqual(rst, rendered)


class TestArgumentItem(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_to_rst_with_one_classifier(self):
        rst = """\
:param indent:
    The indent to use for the description block.
    This is the second paragraph of the argument definition.
:type indent: int"""

        item = ArgumentItem(
            'indent', ['int'], [
                'The indent to use for the description block.',
                'This is the second paragraph of the argument definition.'])
        rendered = '\n'.join(item.to_rst())
        self.assertMultiLineEqual(rst, rendered)

    def test_to_with_two_classifiers(self):
        rst = """\
:param indent:
    The indent to use for the description block.
    This is the second paragraph of the argument definition.
:type indent: int or float"""

        item = ArgumentItem(
            'indent', ['int', 'float'], [
                'The indent to use for the description block.',
                'This is the second paragraph of the argument definition.'])
        rendered = '\n'.join(item.to_rst())
        self.assertMultiLineEqual(rst, rendered)


class TestListItem(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_to_rst_normal(self):
        rst = """\
- **indent** (*int*) --
  The indent to use for the description block.

  This is the second paragraph of the argument definition.
"""
        item = ListItem(
            'indent', ['int'], [
                'The indent to use for the description block.', '',
                'This is the second paragraph of the argument definition.'])
        rendered = '\n'.join(item.to_rst(prefix='-'))
        self.assertMultiLineEqual(rst, rendered)

    def test_to_rst_no_classifier(self):
        rst = """\
- **indent** --
  The indent to use for the description block.
"""
        item = ListItem(
            'indent', [], ['The indent to use for the description block.'])
        rendered = '\n'.join(item.to_rst(prefix='-'))
        self.assertMultiLineEqual(rst, rendered)

    def test_to_rst_only_term(self):
        rst = """\
- **indent**
"""
        item = ListItem('indent', [], [''])
        rendered = '\n'.join(item.to_rst(prefix='-'))
        self.assertMultiLineEqual(rst, rendered)

    def test_to_rst_no_defintition(self):
        rst = """\
- **indent** (*int*)
"""
        item = ListItem('indent', ['int'], [''])
        rendered = '\n'.join(item.to_rst(prefix='-'))
        self.assertMultiLineEqual(rst, rendered)


class TestTableLineItem(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_to_rst(self):
        # with annotation
        rst = """\
function(arg1, arg2)   This is the best fun
"""
        item = TableRowItem(
            'function(arg1, arg2)', 'and', ['This is the best function ever.'])
        rendered = '\n'.join(item.to_rst(columns=(22, 0, 20)))
        self.assertMultiLineEqual(rst, rendered)


class TestMethodItem(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_is_definition(self):
        self.assertTrue(MethodItem.is_definition("term()"))
        self.assertTrue(
            MethodItem.is_definition("term(*args, my_keyword=None)"))
        self.assertFalse(MethodItem.is_definition("term"))
        self.assertFalse(MethodItem.is_definition("term : *args"))

    def test_parse(self):
        item = MethodItem.parse(
            ['method(arguments)', '    Definition in a single line'])
        self.assertEqual(item, MethodItem(
            'method', ['arguments'], ['Definition in a single line']))

    def test_to_rst(self):
        # with annotation
        rst = """\
:meth:`function(arg1, arg2) <function>` This is the best fun
"""
        item = MethodItem('function', ['arg1', 'arg2'],
                          ['This is the best function ever.'])
        rendered = '\n'.join(item.to_rst(columns=(39, 20))) + '\n'
        self.assertMultiLineEqual(rst, rendered)


if __name__ == '__main__':
    unittest.main()
