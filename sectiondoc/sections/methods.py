# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  file: sections/methods.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2011-14, Enthought, Inc.
#  All rights reserved.
# -----------------------------------------------------------------------------
from sectiondoc.items import MethodItem
from sectiondoc.sections.util import get_column_lengths
from sectiondoc.renderers import Method


def methods_table(doc, header, renderer=Method, item_class=MethodItem):
    """ Render the methods section to sphinx friendly table format.

    """
    items = doc.extract_items(item_class)
    lines = []
    if len(items) > 0:
        columns = get_column_lengths(items)
        border = '{0:=^{1}} {0:=^{2}}'.format('', columns[0], columns[1])
        heading = '{0:<{2}} {1:<{3}}'.format('Method', 'Description',
                                             columns[0], columns[1])
        lines += [border]
        lines += [heading]
        lines += [border]
        renderer = Method()
        for item in items:
            renderer.item = item
            lines += renderer.to_rst(columns)
        lines += [border]
        lines += ['']
    lines = [line.rstrip() for line in lines]
    return lines
