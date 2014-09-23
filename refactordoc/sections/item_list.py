# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  file: sections/item_list.py
#  License: LICENSE.TXT
#  Author: Ioannis Tziakos
#
#  Copyright (c) 2011-14, Enthought, Inc.
#  All rights reserved.
# -----------------------------------------------------------------------------
from refactordoc.util import add_indent
from refactordoc.items.list_item import ListItem


def item_list(doc, header):
    """ Refactor the a section to sphinx friendly item list.

    Arguments
    ---------
    doc : BaseDoc
        The docstring container.

    header : str
        The header name that is used for the fields (i.e. ``:<header>:``).

    """
    items = doc.extract_items(item_class=ListItem)
    lines = [':{0}:'.format(header.lower())]
    prefix = None if len(items) == 1 else '-'
    for item in items:
        lines += add_indent(item.to_rst(prefix))
    return lines
