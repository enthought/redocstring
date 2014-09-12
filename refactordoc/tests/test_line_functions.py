# -*- coding: utf-8 -*-
#------------------------------------------------------------------------------
#  file: test_line_functions.py
#  License: LICENSE.TXT
#  Author: Ioannis Tziakos
#
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from refactordoc.util import (
    add_indent, remove_indent, get_indent, fix_star, fix_backspace, is_empty,
    replace_at)
from refactordoc.tests._compat import unittest


class TestLineFunctions(unittest.TestCase):

    def test_add_indent(self):
        input = ["This is the first line", "", "   This is the third line"]
        expected = [
            "   This is the first line", "", "      This is the third line"]
        output = add_indent(input, indent=3)
        self.assertEqual(output, expected)

        expected = [
            "This is the first line", "", "   This is the third line"]
        output = add_indent(input, indent=0)
        self.assertEqual(output, expected)

        expected = [
            "    This is the first line", "", "       This is the third line"]
        output = add_indent(input)
        self.assertEqual(output, expected)

    def test_remove_indent(self):
        input = [
            "   This is the first line", "", "      This is the third line"]
        expected = [
            "This is the first line", "", "This is the third line"]
        output = remove_indent(input)
        self.assertEqual(output, expected)

    def test_get_indent(self):
        output = get_indent('')
        self.assertEqual(output, '')

        output = get_indent('  _dgsdg 44')
        self.assertEqual(output, '  ')

    def test_is_empty(self):
        output = is_empty('                  ')
        self.assertTrue(output)
        output = is_empty('         .         ')
        self.assertFalse(output)

    def test_fix_star(self):
        output = fix_star('*arg')
        self.assertEqual(r'\*arg', output)
        output = fix_star('**sfg')
        self.assertEqual(r'\*\*sfg', output)

    def test_fix_backspace(self):
        output = fix_backspace('Input\Output header')
        self.assertEqual(r'Input\\Output header', output)

    def test_replace_at(self):
        input = ' This is where the new starts'
        expected = ' This is w   3 the new starts'
        output = replace_at('   3', input, 10)
        self.assertEqual(expected, output)

        input = ' This is where the new starts'
        expected = ' This is where the new start '
        output = replace_at('   3', input, 28)
        self.assertEqual(expected, output)

        input = ' This is where the new starts'
        expected = ' This is where the new starts'
        output = replace_at('   3', input, 30)
        self.assertEqual(expected, output)

if __name__ == '__main__':
    unittest.main()
