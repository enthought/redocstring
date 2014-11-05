
# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
#  file: sections/util.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2011-14, Enthought, Inc.
#  All rights reserved.
# -----------------------------------------------------------------------------
from refactordoc.items.util import max_attribute_length, max_attribute_index


def get_column_lengths(items):
    """ Helper function to estimate the column widths for the refactoring of
    the ``Methods`` section.

    The method finds the index of the item that has the largest function
    name (i.e. self.term) and the largest signature. If the indexes are not
    the same then checks to see which of the two items have the largest
    string sum (i.e. self.term + self.signature).

    Parameters
    ----------
    items : list
        A list of MethodItems

    Returns
    -------
    widths : tuple
        A tuple of the first_column and second_column maximum widths.

    """
    name_index = max_attribute_index(items, 'term')
    signature_index = max_attribute_index(items, 'signature')
    if signature_index != name_index:
        index = signature_index
        item1_width = len(items[index].term + items[index].signature)
        index = name_index
        item2_width = len(items[index].term + items[index].signature)
        first_column = max(item1_width, item2_width)
    else:
        index = name_index
        first_column = len(items[index].term + items[index].signature)

    first_column += 11  # Add boilerplate characters
    second_column = max_attribute_length(items, 'definition')
    return (first_column, second_column)
