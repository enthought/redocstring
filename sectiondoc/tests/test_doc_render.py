from sectiondoc.styles import DocRender
from sectiondoc.tests._compat import unittest


class TestDocRender(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    def test_eod(self):
        # given
        doc_render = DocRender([])

        # when/then
        self.assertTrue(doc_render.eod)

        # given
        doc_render = DocRender([''])

        # when/then
        self.assertFalse(doc_render.eod)

        # given
        doc_render = DocRender(['', ''])

        # when/then
        self.assertFalse(doc_render.eod)

    def test_pop(self):
        # given
        doc_render = DocRender(['A', 'B'])

        # when/then
        self.assertEqual(doc_render.pop(), 'A')
        self.assertEqual(doc_render.pop(), 'B')
        with self.assertRaises(IndexError):
            doc_render.pop()

    def test_peek(self):
        # given
        doc_render = DocRender([])

        # when/then
        self.assertEqual(doc_render.peek(), '')

        # given
        doc_render = DocRender(['A', 'B'])

        # when/then
        self.assertEqual(doc_render.peek(), 'A')
        self.assertEqual(doc_render.peek(ahead=1), 'B')
        self.assertEqual(doc_render.peek(ahead=2), '')

    def test_remove_if_empty(self):
        # given
        doc_render = DocRender(['A', ' ', 'B'])

        # when
        doc_render.remove_if_empty()

        # then
        self.assertEqual(doc_render.docstring, ['A', ' ', 'B'])

        # when
        doc_render.remove_if_empty(index=1)

        # then
        self.assertEqual(doc_render.docstring, ['A', 'B'])

        # when
        with self.assertRaises(IndexError):
            doc_render.remove_if_empty(index=2)

    def test_remove_lines(self):
        # given
        doc_render = DocRender(['A', ' ', 'B'])

        # when
        doc_render.remove_lines(1, count=2)

        # then
        self.assertEqual(doc_render.docstring, ['A'])

        # when
        doc_render.remove_lines(index=0, count=3)

        # then
        self.assertEqual(doc_render.docstring, [])

    def test_read(self):
        # given
        doc_render = DocRender(['A', 'B'])

        # when/then
        self.assertEqual(doc_render.read(), 'A')
        self.assertEqual(doc_render.read(), 'B')
        with self.assertRaises(IndexError):
            self.assertIsNone(doc_render.read())

    def test_get_next_paragraph(self):
        # given
        doc_render = DocRender([
            'This is a sample docstring.',
            'and the paragraph continues here',
            '',
            '',
            'This is another sample'])

        # when/then
        self.assertEqual(
            doc_render.get_next_paragraph(),
            ['This is a sample docstring.',
             'and the paragraph continues here'])
        self.assertEqual(
            doc_render.docstring, ['', '', 'This is another sample'])

        # when/then
        self.assertEqual(doc_render.get_next_paragraph(), [])
        self.assertEqual(
            doc_render.docstring, ['', '', 'This is another sample'])

        # when/then
        doc_render.index = 2
        self.assertEqual(
            doc_render.get_next_paragraph(),
            ['This is another sample'])
        self.assertEqual(doc_render.docstring, ['', ''])

        # when/then
        self.assertEqual(
            doc_render.get_next_paragraph(), [])

    def test_seek_to_next_empty_line(self):
        # given
        doc_render = DocRender([
            'This is a sample docstring.',
            'and the paragraph continues here',
            '',
            '',
            'This is another sample'])

        # when
        doc_render.seek_to_next_non_empty_line()

        # then
        self.assertEqual(doc_render.index, 0)

        # when
        doc_render.index = 2
        doc_render.seek_to_next_non_empty_line()

        # then
        self.assertEqual(doc_render.index, 4)

        # when
        doc_render.seek_to_next_non_empty_line()

        # then
        self.assertEqual(doc_render.index, 4)

    def test_insert_lines(self):
        # given
        doc_render = DocRender(['A', 'B'])

        # when
        doc_render.insert_lines(['C', ''], index=0)

        # then
        self.assertEqual(
            doc_render.docstring, ['C', '', 'A', 'B'])
        self.assertEqual(doc_render.index, 0)

        # when
        doc_render.insert_lines(['', '2'], index=2)

        # then
        self.assertEqual(
            doc_render.docstring, ['C', '', '', '2', 'A', 'B'])
        self.assertEqual(doc_render.index, 0)

        # when/then
        with self.assertRaises(IndexError):
            doc_render.insert_lines(['6', '2'], index=10)

    def test_insert_and_move(self):
        # given
        doc_render = DocRender(['A', 'B'])

        # when
        doc_render.insert_and_move(['C', ''], index=0)

        # then
        self.assertEqual(
            doc_render.docstring, ['C', '', 'A', 'B'])
        self.assertEqual(doc_render.index, 2)

        # when
        doc_render.insert_and_move(['', '2'], doc_render.index)

        # then
        self.assertEqual(
            doc_render.docstring, ['C', '', '', '2', 'A', 'B'])
        self.assertEqual(doc_render.index, 4)

        # when/then
        with self.assertRaises(IndexError):
            doc_render.insert_and_move(['6', '2'], index=10)

    def test_is_section(self):
        # given
        doc_render = DocRender([
            "My Header  ",
            "---------     ",
            "MyHeader  ",
            "---------     ",
            "No header",
            "Input\Output header",
            "===================",
            "My Header  ",
            " --------     "])

        # when/then
        doc_render.index = 0
        self.assertTrue(doc_render.is_section())

        # when/then
        doc_render.index = 1
        self.assertFalse(doc_render.is_section())

        # when/then
        doc_render.index = 2
        self.assertFalse(doc_render.is_section())

        # when/then
        doc_render.index = 4
        self.assertFalse(doc_render.is_section())

        # when/then
        doc_render.index = 5
        self.assertTrue(doc_render.is_section())

        # when/then
        doc_render.index = 7
        self.assertFalse(doc_render.is_section())

        # when/then
        doc_render.index = 8
        self.assertFalse(doc_render.is_section())

    def test_get_next_block(self):
        doc_render = DocRender([
            'term1',
            '    Definition1',
            'term2 : classifier',
            '    Definition2',
            '     ',
            'term3',
            '',
            '',
            'term4 : classifier',
            '    Definition3',
            '',
            '    MoreDefinition3',
            ''])

        self.assertEqual(
            doc_render.get_next_block(),
            ['term1', '    Definition1'])
        self.assertEqual(
            doc_render.get_next_block(),
            ['term2 : classifier', '    Definition2'])
        self.assertEqual(
            doc_render.get_next_block(), ['term3'])
        doc_render.index = 2
        self.assertEqual(
            doc_render.get_next_block(),
            ['term4 : classifier',
             '    Definition3', '', '    MoreDefinition3'])

    def test_extract_item_blocks(self):
        # given
        doc_render = DocRender([
            'Section',
            '=======',
            '',
            'Section',
            '=======',
            'term1',
            '    Definition1',
            'term2 : classifier',
            '    Definition2',
            '     ',
            'Section',
            '=======',
            'term4 : classifier',
            '    Definition3',
            '',
            '    MoreDefinition3',
            ''])

        # when/then
        self.assertEqual(doc_render.extract_items(), [])

        # when/then
        doc_render.index = 5
        self.assertEqual(
            doc_render.extract_items(),
            [('term1', [], ['Definition1']),
             ('term2', ['classifier'], ['Definition2'])])

        # when/then
        doc_render.index = 7
        self.assertEqual(
            doc_render.extract_items(),
            [('term4', ['classifier'],
              ['Definition3', '', 'MoreDefinition3'])])

    def test_render_header(self):
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
        doc_render = DocRender(docstring_lines)
        doc_render.parse()
        output = '\n'.join(docstring_lines) + '\n'
        self.assertMultiLineEqual(rst, output)

    def test_render_complex_header(self):
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
        doc_render = DocRender(docstring_lines)
        doc_render.parse()
        output = '\n'.join(docstring_lines) + '\n'
        self.assertMultiLineEqual(rst, output)


if __name__ == '__main__':
    unittest.main()
