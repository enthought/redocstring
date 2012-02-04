# -*- coding: UTF-8 -*-
#------------------------------------------------------------------------------
#  file: function_doc.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from base_doc import BaseDoc
from line_functions import get_indent, add_indent
from definition_items import ArgumentItem, ListItem


class FunctionDoc(BaseDoc):
    """Docstring refactoring for functions"""

    def __init__(self, lines, headers=None):

        if headers is None:
            headers = {'Returns': 'as_items_list', 'Arguments': 'arguments',
                       'Parameters': 'arguments', 'Raises': 'as_items_list',
                       'Yields': 'as_items_list', 'Notes':'notes'}

        super(FunctionDoc, self).__init__(lines, headers)
        return

    def _refactor_as_items_list(self, header):
        """Refactor the a section to sphinx friendly item list.

        """
        items = self.extract_items(item_class=ListItem)
        lines = [':{0}:'.format(header.lower())]
        prefix = None if len(items) == 1 else '-'
        for item in items:
            lines += add_indent(item.to_rst(prefix))
        self.insert_and_move(lines, self.index)
        return

    def _refactor_arguments(self, header):
        """Refactor the argument section to sphinx friendly format
        """
        items = self.extract_items(item_class=ArgumentItem)
        lines = []
        for item in items:
            lines += item.to_rst()
        self.insert_and_move(lines, self.index)
        return

    def _refactor_notes(self, header):
        """Refactor the notes section to sphinx friendly format.

        """
        paragraph = self.get_next_paragraph()
        lines = ['.. note::']
        lines += add_indent(paragraph)
        self.insert_and_move(lines, self.index)

