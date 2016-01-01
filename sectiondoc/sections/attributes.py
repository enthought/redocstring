# -*- coding: utf-8 -*-
#-----------------------------------------------------------------------------
#  License: LICENSE.TXT
#  Author: Ioannis Tziakos
#
#  Copyright (c) 2011-2014, Enthought, Inc.
#  All rights reserved.
#-----------------------------------------------------------------------------
from sectiondoc.items import OrDefinitionItem
from sectiondoc.renderers import Attribute


def attributes(doc, header, renderer=Attribute, item_class=OrDefinitionItem):
    """Render the attributes section to sphinx friendly format.

    """
    items = doc.extract_items(item_class)
    lines = []
    renderer = renderer()
    for item in items:
        renderer.item = item
        lines += renderer.to_rst()
    lines.append('')
    return lines
