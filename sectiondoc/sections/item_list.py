# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  License: LICENSE.TXT
#  Author: Ioannis Tziakos
#
#  Copyright (c) 2011-14, Enthought, Inc.
#  All rights reserved.
# -----------------------------------------------------------------------------
from sectiondoc.util import add_indent
from sectiondoc.items import OrDefinitionItem
from sectiondoc.renderers import ListItem


def item_list(doc, header, renderer=ListItem, item_class=OrDefinitionItem):
    """ Render the section to sphinx friendly item list.

    Arguments
    ---------
    doc : DocRender
        The docstring container.

    header : str
        The header name that is used for the fields (i.e. ``:<header>:``).

    renderer : Renderer
        A renderer instance to render the items.

    item_class : type
        The item parser class to use. Default is :class:`~.OrDefinitionItem`.

    """
    items = doc.extract_items(item_class)
    lines = [':{0}:'.format(header.lower())]
    prefix = None if len(items) == 1 else '-'
    renderer = renderer()
    for item in items:
        renderer.item = item
        lines += add_indent(renderer.to_rst(prefix))
    lines.append('')
    return lines
