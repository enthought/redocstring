def max_attribute_length(items, attr):
    """ Find the max length of the attribute in a list of DefinitionItems.

    Arguments
    ---------
    items : list
        The list of the DefinitionItem instances (or subclasses).

    attr : str
        Attribute to look at.

    """
    if attr == 'definition':
        maximum = max([len(' '.join(item.definition)) for item in items])
    else:
        maximum = max([len(getattr(item, attr)) for item in items])
    return maximum


def max_attribute_index(items, attr):
    """ Find the index of the attribute with the maximum length in a list of
    DefinitionItems.

    Arguments
    ---------
    items : list
        The list of the DefinitionItems (or subclasses).

    attr : str
        Attribute to look at.

    """
    if attr == 'definition':
        attributes = [len(' '.join(item.definition)) for item in items]
    else:
        attributes = [len(getattr(item, attr)) for item in items]

    maximum = max(attributes)
    return attributes.index(maximum)
