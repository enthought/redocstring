from sectiondoc.items import OrDefinitionItem, MethodItem, Item, AnyItem
from sectiondoc.renderers import (
    Argument, Attribute, Definition, ListItem, Method, TableRow)
from sectiondoc.tests._compat import unittest


class TestOrDefinitionItem(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_is_item(self):
        self.assertFalse(OrDefinitionItem.is_item("term"))
        self.assertFalse(OrDefinitionItem.is_item("term "))
        self.assertTrue(OrDefinitionItem.is_item("term :"))
        self.assertTrue(OrDefinitionItem.is_item("term : "))
        self.assertTrue(OrDefinitionItem.is_item("term : classifier"))
        self.assertFalse(OrDefinitionItem.is_item(":term : classifier"))
        self.assertFalse(OrDefinitionItem.is_item("term : classifier:"))

        # special cases
        header_with_object = 'component : class.component.instance'
        self.assertTrue(OrDefinitionItem.is_item(header_with_object))

        header_with_trait = 'properies : Dict(Str, Any)'
        self.assertTrue(OrDefinitionItem.is_item(header_with_trait))

        header_with_or = 'item : ModelIndex or None'
        self.assertTrue(OrDefinitionItem.is_item(header_with_or))

    def test_parse(self):
        item = OrDefinitionItem.parse(['term', '    Definition.'])
        self.assertEqual(item, OrDefinitionItem('term', [], ['Definition.']))

        item = OrDefinitionItem.parse([
            'term', '    Definition, paragraph 1.',
            '', '    Definition, paragraph 2.'])
        self.assertEqual(
            item,
            OrDefinitionItem(
                'term', [], [
                    'Definition, paragraph 1.',
                    '',
                    'Definition, paragraph 2.']))

        item = OrDefinitionItem.parse(['term :', '    Definition.'])
        self.assertEqual(item, OrDefinitionItem('term', [], ['Definition.']))

        item = OrDefinitionItem.parse(['term : classifier', '    Definition.'])
        self.assertEqual(
            item, OrDefinitionItem('term', ['classifier'], ['Definition.']))

        item = OrDefinitionItem.parse(
            ['term : classifier or classifier', '    Definition.'])
        self.assertEqual(
            item,
            OrDefinitionItem(
                'term',
                ['classifier', 'classifier'], ['Definition.']))

        item = OrDefinitionItem.parse(
            ['term : classifier', '    Block.', '        Definition.'])
        self.assertEqual(
            item, OrDefinitionItem(
                'term', ['classifier'], ['Block.', '    Definition.']))


class TestAnyItem(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_is_item(self):
        self.assertTrue(AnyItem.is_item("term"))
        self.assertTrue(AnyItem.is_item("term "))
        self.assertTrue(AnyItem.is_item("term :"))
        self.assertTrue(AnyItem.is_item("term : "))
        self.assertTrue(AnyItem.is_item("term : classifier"))
        self.assertFalse(AnyItem.is_item(":term : classifier"))
        self.assertTrue(AnyItem.is_item("term : classifier:"))

        # special cases
        header_with_object = 'component : class.component.instance'
        self.assertTrue(AnyItem.is_item(header_with_object))

        header_with_trait = 'properies : Dict(Str, Any)'
        self.assertTrue(AnyItem.is_item(header_with_trait))

        header_with_or = 'item : ModelIndex or None'
        self.assertTrue(AnyItem.is_item(header_with_or))

    def test_parse(self):
        item = AnyItem.parse(['term'])
        self.assertEqual(item, AnyItem('term', [], []))

        item = AnyItem.parse(['term :'])
        self.assertEqual(item, AnyItem('term', [], []))

        item = AnyItem.parse(['term', '    Definition.'])
        self.assertEqual(item, AnyItem('term', [], ['Definition.']))

        item = AnyItem.parse([
            'term', '    Definition, paragraph 1.',
            '', '    Definition, paragraph 2.'])
        self.assertEqual(
            item,
            AnyItem(
                'term', [], [
                    'Definition, paragraph 1.',
                    '',
                    'Definition, paragraph 2.']))

        item = AnyItem.parse(['term :', '    Definition.'])
        self.assertEqual(item, AnyItem('term', [], ['Definition.']))

        item = AnyItem.parse(['term : classifier', '    Definition.'])
        self.assertEqual(
            item, AnyItem('term', ['classifier'], ['Definition.']))

        item = AnyItem.parse(
            ['term : classifier or classifier', '    Definition.'])
        self.assertEqual(
            item,
            AnyItem('term', ['classifier or classifier'], ['Definition.']))

        item = AnyItem.parse(
            ['term : classifier', '    Block.', '        Definition.'])
        self.assertEqual(
            item, AnyItem(
                'term', ['classifier'], ['Block.', '    Definition.']))


class TestDefintionRenderer(unittest.TestCase):

    def test_to_rst(self):
        rst = """\
lines

    *(list)* --
    A list of string lines rendered in rst.
"""
        item = Item(
            'lines', ['list'], ['A list of string lines rendered in rst.'])
        rendered = '\n'.join(Definition(item).to_rst())
        self.assertMultiLineEqual(rst, rendered)


class TestAttributeRenderer(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_to_rst(self):
        # with annotation
        rst = """\
.. attribute:: indent
    :annotation: = int

    The indent to use for the description block.
"""
        item = Item(
            'indent',
            ['int'],
            ['The indent to use for the description block.'])
        rendered = '\n'.join(Attribute(item).to_rst())
        self.assertMultiLineEqual(rst, rendered)

        # without annotation
        rst = """\
.. attribute:: indent

    The indent to use for the description block.
"""
        item = Item(
            'indent', [], ['The indent to use for the description block.'])
        rendered = '\n'.join(Attribute(item).to_rst())
        self.assertMultiLineEqual(rst, rendered)


class TestArgumentRenderer(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_to_rst_with_one_classifier(self):
        rst = """\
:param indent:
    The indent to use for the description block.
    This is the second paragraph of the argument definition.
:type indent: int"""

        item = Item(
            'indent', ['int'], [
                'The indent to use for the description block.',
                'This is the second paragraph of the argument definition.'])
        rendered = '\n'.join(Argument(item).to_rst())
        self.assertMultiLineEqual(rst, rendered)

    def test_to_with_two_classifiers(self):
        rst = """\
:param indent:
    The indent to use for the description block.
    This is the second paragraph of the argument definition.
:type indent: int or float"""

        item = Item(
            'indent', ['int', 'float'], [
                'The indent to use for the description block.',
                'This is the second paragraph of the argument definition.'])
        rendered = '\n'.join(Argument(item).to_rst())
        self.assertMultiLineEqual(rst, rendered)


class TestListItemRenderer(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_to_rst_normal(self):
        rst = """\
- **indent** (*int*) --
  The indent to use for the description block.

  This is the second paragraph of the argument definition.
"""
        item = Item(
            'indent', ['int'], [
                'The indent to use for the description block.', '',
                'This is the second paragraph of the argument definition.'])
        rendered = '\n'.join(ListItem(item).to_rst(prefix='-'))
        self.assertMultiLineEqual(rst, rendered)

    def test_to_rst_no_classifier(self):
        rst = """\
- **indent** --
  The indent to use for the description block.
"""
        item = Item(
            'indent', [], ['The indent to use for the description block.'])
        rendered = '\n'.join(ListItem(item).to_rst(prefix='-'))
        self.assertMultiLineEqual(rst, rendered)

    def test_to_rst_only_term(self):
        rst = """\
- **indent**
"""
        item = Item('indent', [], [''])
        rendered = '\n'.join(ListItem(item).to_rst(prefix='-'))
        self.assertMultiLineEqual(rst, rendered)

    def test_to_rst_no_defintition(self):
        rst = """\
- **indent** (*int*)
"""
        item = Item('indent', ['int'], [''])
        rendered = '\n'.join(ListItem(item).to_rst(prefix='-'))
        self.assertMultiLineEqual(rst, rendered)


class TestTableLineItem(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_to_rst(self):
        # with annotation
        rst = """\
function(arg1, arg2)   This is the best fun
"""
        item = Item(
            'function(arg1, arg2)', 'and', ['This is the best function ever.'])
        rendered = '\n'.join(TableRow(item).to_rst(columns=(22, 0, 20)))
        self.assertMultiLineEqual(rst, rendered)


class TestMethodItem(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_is_item(self):
        self.assertTrue(MethodItem.is_item("term()"))
        self.assertTrue(
            MethodItem.is_item("term(*args, my_keyword=None)"))
        self.assertFalse(MethodItem.is_item("term"))
        self.assertFalse(MethodItem.is_item("term : *args"))

    def test_parse(self):
        item = MethodItem.parse(
            ['method(arguments)', '    Definition in a single line'])
        self.assertEqual(item, MethodItem(
            'method', ['arguments'], ['Definition in a single line']))


class TestMethodRenderer(unittest.TestCase):

    def test_to_rst(self):
        # with annotation
        rst = """\
:meth:`function(arg1, arg2) <function>`  This is the best fun
"""
        item = Item(
            'function', ['arg1', 'arg2'],
            ['This is the best function ever.'])
        rendered = '\n'.join(Method(item).to_rst(columns=(39, 20))) + '\n'
        self.assertMultiLineEqual(rst, rendered)


if __name__ == '__main__':
    unittest.main()
