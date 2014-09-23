# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  file: sections/attributes.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2011-14, Enthought, Inc.
#  All rights reserved.
# -----------------------------------------------------------------------------
from refactordoc.items import AttributeItem


def attributes(doc, header):
    """Refactor the attributes section to sphinx friendly format.

    """
    items = doc.extract_items(AttributeItem)
    lines = []
    for item in items:
        lines += item.to_rst()
    return lines
