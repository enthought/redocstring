# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  file: base_doc.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2011-14, Enthought, Inc.
#  All rights reserved.
# -----------------------------------------------------------------------------
import re

from sectiondoc.items import OrDefinitionItem
from sectiondoc.util import is_empty, get_indent
from sectiondoc.sections import rubric


underline_regex = re.compile(r'\s*\S+\s*\Z')


class DocRender(object):
    """ Docstring rendering class.

    The class' main purpose is to parse the docstring and find the
    sections that need to be refactored. The operation take place in
    two stages:

    - The class is instanciated with the appropriate section renderers
    - The ``parse`` method is called to parse and render the sections
      inplace.

    Attributes
    ----------
    docstring : list
        A list of strings (lines) that holds docstrings. The lines are changed
        inplace.

    index : int
        The zero-based line number of the docstring that is currently
        processed.

    sections : dict
        The sections that will be detected and rendered. The dictionary
        maps the section headers for detection to a tuple containing
        the section rendering function and optional values for the item
        renderer and parser.

    """

    def __init__(self, lines, sections=None):
        """

        Arguments
        ---------
        lines : list
            The docstring as a list of strings where to render the sections

        sections : dict
            The sections that will be detected and rendered. The dictionary
            maps the section headers for detection to a tuple containing
            the section rendering function and optional values for the item
            renderer and parser. If on section rendering information is
            provided the default behaviour of the class is to render
            every section using the rubric rendering function.

        """
        try:
            self._docstring = lines.splitlines()
        except AttributeError:
            self._docstring = lines
        self.sections = {} if sections is None else sections
        self.bookmarks = []

    def parse(self):
        """ Parse the docstring.

        The docstring is parsed for sections. If a section is found then
        the corresponding section rendering method is called.

        """
        self.index = 0
        self.seek_to_next_non_empty_line()
        while not self.eod:
            section = self.is_section()
            if len(section) > 0:
                self._render(section)
            else:
                self.index += 1
                self.seek_to_next_non_empty_line()

    def _render(self, section):
        """ Call the section rendering function.

        The header is removed from the docstring and the appropriate
        rendering function is executed.

        """
        self.remove_lines(self.index, 2)  # Remove header
        self.remove_if_empty(self.index)  # Remove space after header
        method, renderer, item_class = self.sections.get(
            section, (rubric, None, None))
        lines = method(self, section, renderer, item_class)
        self.insert_and_move(lines, self.index)

    def extract_items(self, item_type):
        """ Extract the section items from a docstring.

        Parse the items in the description of a section into items of the
        provided itme type. The method starts at the current line index
        position and checks if in the next two lines contain a valid item of
        the desired type. If successful, the lines that belong to the item
        description block (i.e. item header + item body) are popped out from
        the docstring and passed to the ``item_type.parser`` class method to
        get a new instance of ``item_type``.

        The process is repeated until there are no compatible ``item_type``
        items found in the section or we run out of docstring lines,
        The collected item instances are returned

        The exit conditions allow for two valid section item layouts:

        1. No lines between items::

            <header1>
                <description1>

                <more description>
            <header2>
                <description2>

        2. One line between items::

            <header1>
                <description1>

                <more description>

            <header2>
                <description2>


        Arguments
        ---------
        item_type : Item
            An Item type or a subclass. This argument is used to check
            if a line in the docstring is a valid item header and to
            parse the individual list items in the section.

        Returns
        -------
        items : list
            List of the collected item instances of :class:`~.Item` type.

        """
        item_type = OrDefinitionItem if (item_type is None) else item_type
        is_item = item_type.is_item
        item_blocks = []
        while (not self.eod) and \
                (is_item(self.peek()) or is_item(self.peek(1))):
            self.remove_if_empty(self.index)
            item_blocks.append(self.get_next_block())
        items = [item_type.parse(block) for block in item_blocks]
        return items

    def get_next_block(self):
        """ Get the next item block from the docstring.

        The method reads the next item block in the docstring. The first line
        is assumed to be the Item header and the following lines to
        belong to the definition body::

            <header line>
                <definition>

        The end of the field is designated by a line with the same indent
        as the field header or two empty lines are found in sequence.

        """
        item_header = self.pop()
        sub_indent = get_indent(item_header) + ' '
        block = [item_header]
        while not self.eod:
            peek_0 = self.peek()
            peek_1 = self.peek(1)
            if is_empty(peek_0) and not peek_1.startswith(sub_indent):
                break
            elif not is_empty(peek_0) and not peek_0.startswith(sub_indent):
                break
            else:
                line = self.pop()
                block += [line.rstrip()]
        return block

    def is_section(self):
        """ Check if the current line defines a section.

        .. todo:: split and cleanup this method.

        """
        if self.eod:
            return False

        header = self.peek()
        line2 = self.peek(1)

        # check for underline type format
        underline = underline_regex.match(line2)
        if underline is None:
            return ''
        # is the next line an rst section underline?
        striped_header = header.rstrip()
        expected_underline1 = re.sub(r'[A-Za-z\\]|\b\s', '-', striped_header)
        expected_underline2 = re.sub(r'[A-Za-z\\]|\b\s', '=', striped_header)
        if (
                (underline.group().rstrip() == expected_underline1) or
                (underline.group().rstrip() == expected_underline2)):
            return header.strip()
        else:
            return ''

    def insert_lines(self, lines, index):
        """ Insert lines in the docstring.

        Arguments
        ---------
        lines : list
            The list of lines to insert

        index : int
            Index to start the insertion

        """
        docstring = self.docstring
        for line in reversed(lines):
            docstring.insert(index, line)

    def insert_and_move(self, lines, index):
        """ Insert lines and move the current index to the end.

        """
        self.insert_lines(lines, index)
        self.index += len(lines)

    def seek_to_next_non_empty_line(self):
        """ Goto the next non_empty line.

        """
        docstring = self.docstring
        for line in docstring[self.index:]:
            if not is_empty(line):
                break
            self.index += 1

    def get_next_paragraph(self):
        """ Get the next paragraph designated by an empty line.

        """
        lines = []
        while (not self.eod) and (not is_empty(self.peek())):
            line = self.pop()
            lines.append(line)
        return lines

    def read(self):
        """ Return the next line and advance the index.

        """
        index = self.index
        line = self._docstring[index]
        self.index += 1
        return line

    def remove_lines(self, index, count=1):
        """ Removes the lines from the docstring

        """
        docstring = self.docstring
        del docstring[index:(index + count)]

    def remove_if_empty(self, index=None):
        """ Remove the line from the docstring if it is empty.

        """
        if is_empty(self.docstring[index]):
            self.remove_lines(index)

    def bookmark(self):
        """ append the current index to the end of the list of bookmarks.

        """
        self.bookmarks.append(self.index)

    def goto_bookmark(self, bookmark_index=-1):
        """ Move to bookmark.

        Move the current index to the  docstring line given by the
        ``self.bookmarks[bookmark_index]`` and remove it from the
        bookmark list. Default value will pop the last entry.

        Returns
        -------
        bookmark : int

        """
        self.index = self.bookmarks[bookmark_index]
        return self.bookmarks.pop(bookmark_index)

    def peek(self, ahead=0):
        """ Peek ahead a number of lines

        The function retrieves the line that is ahead of the current
        index. If the index is at the end of the list then it returns an
        empty string.

        Arguments
        ---------
        ahead : int
            The number of lines to look ahead.

        """
        position = self.index + ahead
        try:
            line = self.docstring[position]
        except IndexError:
            line = ''
        return line

    def pop(self, index=None):
        """ Pop a line from the dostrings.

        """
        index = self.index if index is None else index
        return self._docstring.pop(index)

    @property
    def eod(self):
        """ End of docstring.

        """
        return self.index >= len(self.docstring)

    @property
    def docstring(self):
        """ Get the docstring lines.

        """
        return self._docstring
