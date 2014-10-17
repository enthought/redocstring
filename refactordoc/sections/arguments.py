# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  file: function_doc.py
#  License: LICENSE.TXT
#  Author: Ioannis Tziakos
#
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
# -----------------------------------------------------------------------------
from refactordoc.items import DefinitionItem
from refactordoc.renderers.argument import Argument


def arguments(doc, header, renderer=None, item_class=DefinitionItem):
    """ Refactor the argument section to sphinx friendly format.

    Arguments
    ---------
    doc : BaseDoc
        The docstring container.
    header : string
        This parameter is ignored in this method.

    renderer : Renderer
        A renderer instance to render the items.

    item_class : type
        The item parser class to use. Default is :class:`~.DefinitionItem`.

    """
    items = doc.extract_items(item_class=item_class)
    lines = []
    renderer = Argument if renderer is None else renderer
    for item in items:
        renderer.item = item
        lines += renderer.to_rst()
    return lines
