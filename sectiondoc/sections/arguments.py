# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  License: LICENSE.TXT
#  Author: Ioannis Tziakos
#
#  Copyright (c) 2011-14, Enthought, Inc.
#  All rights reserved.
# -----------------------------------------------------------------------------
from sectiondoc.items import OrDefinitionItem
from sectiondoc.renderers.argument import Argument


def arguments(doc, header, renderer=Argument, item_class=OrDefinitionItem):
    """ Render the argument section to sphinx friendly format.

    Arguments
    ---------
    doc : DocRender
        The docstring container.
    header : string
        This parameter is ignored in this method.

    renderer : Renderer
        A renderer instance to render the items.

    item_class : type
        The item parser class to use. Default is :class:`~.orDefinitionItem`.

    """
    items = doc.extract_items(item_class)
    lines = []
    renderer = renderer()
    for item in items:
        renderer.item = item
        lines += renderer.to_rst()
    return lines
