import abc
from collections import namedtuple


class Item(namedtuple('Item', ['term', 'classifiers', 'definition'])):
    """ A section item.

    The Item class is responsible to check, parse a docstring
    item into a (term, classifiers, definition) tuple.

    Format diagram::

        +-------------------------------------------------+
        | header                                          |
        +--+----------------------------------------------+---+
           | definition                                       |
           | (body elements)+                                 |
           +--------------------------------------------------+


    Depending only in the type of the list item the header is split into a
    term and one or more classifiers.

    Attributes
    ----------
    term : str
        The term usually reflects the name of a parameter or an attribute.

    classifiers : list
        The classifier(s) of the term. Commonly used to reflect the type
        of an argument or the signature of a function.

    definition : list
        The list of strings that holds the description of the definition item.

    """

    @property
    def mode(self):
        """ Property (`string`), the operational mode of the item based on the
        available info. Possible values are ``{'only_term', 'no_classifiers',
        'no_definition', 'full'}``.


        """
        if self.classifiers == [] and self.definition == ['']:
            mode = 'only_term'
        elif self.classifiers == []:
            mode = 'no_classifiers'
        elif self.definition == ['']:
            mode = 'no_definition'
        else:
            mode = 'full'
        return mode

    @classmethod
    def is_item(cls, line):
        """ Check if the line is describing an item.

        The method is used to check that a line is following the expected
        format for the `term` and `classifiers` attributes.

        """
        raise NotImplementedError()

    @classmethod
    def parse(cls, lines):
        """ Parse a definition item from a set of lines.

        The class method parses the item from the list of docstring lines and
        produces a Item with the term, classifier and the definition.

        .. note:: The global indention in the definition lines is striped

        Arguments
        ---------
        lines :
            docstring lines of the definition without any empty lines before or
            after.

        Returns
        -------
        item : Item

        """
        raise NotImplementedError()
