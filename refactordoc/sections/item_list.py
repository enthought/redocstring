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
from refactordoc.items import DefinitionItem
from refactordoc.renderers import ListItem


def item_list(doc, header, renderer=None, item_class=DefinitionItem):
    """ Refactor the section to sphinx friendly item list.

    Arguments
    ---------
    doc : BaseDoc
        The docstring container.

    header : str
        The header name that is used for the fields (i.e. ``:<header>:``).

    renderer : Renderer
        A renderer instance to render the items.

    item_class : type
        The item parser class to use. Default is :class:`~.DefinitionItem`.

    """
    items = doc.extract_items(item_class=item_class)
    lines = [':{0}:'.format(header.lower())]
    prefix = None if len(items) == 1 else '-'
    renderer = ListItem if renderer is None else renderer
    for item in items:
        renderer.item = item
        lines += add_indent(renderer.to_rst(prefix))
    return lines
