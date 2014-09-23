# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  file: function_doc.py
#  License: LICENSE.TXT
#  Author: Ioannis Tziakos
#
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
# -----------------------------------------------------------------------------
from refactordoc.items.argument_item import ArgumentItem


def arguments(doc, header):
    """ Refactor the argument section to sphinx friendly format.

    Arguments
    ---------
    doc : BaseDoc
        The docstring container.
    header : string
        This parameter is ignored in this method.

    """
    items = doc.extract_items(item_class=ArgumentItem)
    lines = []
    for item in items:
        lines += item.to_rst()
    return lines
