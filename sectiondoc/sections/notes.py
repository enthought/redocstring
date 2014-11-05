# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  file: sections/notes.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2011-14, Enthought, Inc.
#  All rights reserved.
# -----------------------------------------------------------------------------
from refactordoc.util import add_indent


def notes_paragraph(doc, header, renderer=None, item_class=None):
    """Refactor the note section to use the rst ``.. note`` directive.

    The section is expected to be given as a paragraph.

    """
    paragraph = doc.get_next_paragraph()
    lines = ['.. note::']
    lines += add_indent(paragraph)
    return lines
