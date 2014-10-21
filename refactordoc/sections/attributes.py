# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  file: sections/attributes.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2011-14, Enthought, Inc.
#  All rights reserved.
# -----------------------------------------------------------------------------
from refactordoc.items import DefinitionItem
from refactordoc.renderers import Attribute


def attributes(doc, header, renderer=Attribute, item_class=DefinitionItem):
    """Refactor the attributes section to sphinx friendly format.

    """

    items = doc.extract_items(item_class)
    lines = []
    renderer = renderer()
    for item in items:
        renderer.item = item
        lines += renderer.to_rst()
    return lines
