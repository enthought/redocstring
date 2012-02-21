Building your own suite
#######################

While the default refactoring suite is enough for most cases. The user might
need to extent the section repertoire, process other object types, allow more
freedom in defining the definition list or restrict the docstring style to
improve consinstancy through his code.

.. warning:: All the methods below require to change the refactordoc code and
    even thought the changes might be small it is not considered the best way
    since updating refactordoc becomes non-trivial. Future version will remove
    this shortcoming.


Adding sections
###############

New sections to be refactored can be simply added to the ``headers`` dictionary
when an appropriate refactoring method exists. For example in the default
suite that is shipped with refactordoc the
:class:`~refactordoc.function_doc.FunctionDoc` class sets the `Returns`
`Raises` and `Yields` section to use the `_refactor_as_item_list` method
in the class::

    if headers is None:
        headers = {'Returns': 'as_item_list', 'Arguments': 'arguments',
                   'Parameters': 'arguments', 'Raises': 'as_item_list',
                   'Yields': 'as_item_list', 'Notes':'notes'}


When such a method does not

exist then the user has to augment the related class with that will
parse and extract the section definition block(s) and return the
refactored lines to replace the section in the docstring. The
signature of the method should be ``_header_<name>(self, header)

Where ``<name> is the value in the ``headers`` that corresponds to the
``header`` string that is found in the docstring.


.. note:: More to come
