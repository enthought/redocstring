# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  file: sections/attributes.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2011-14, Enthought, Inc.
#  All rights reserved.
# -----------------------------------------------------------------------------
from refactordoc.items import DefinitionItem
from refctordoc.renderers import Attribute


def attributes(doc, header, renderer=None, item_class=DefinitionItem):
    """Refactor the attributes section to sphinx friendly format.

    """

    items = doc.extract_items(item_class=DefinitionItem)
    lines = []
    for item in items:
        lines += renderer(item).to_rst()
    return lines
