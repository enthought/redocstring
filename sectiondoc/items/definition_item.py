from refactordoc.items.regex import definition_regex, header_regex
from refactordoc.items.item import Item
from refactordoc.util import trim_indent


class DefinitionItem(Item):
    """ A docstring definition item

    Syntax diagram::

        +-------------------------------------------------+
        | term [ " : " classifier [ " or " classifier] ]  |
        +--+----------------------------------------------+---+
           | definition                                       |
           | (body elements)+                                 |
           +--------------------------------------------------+

    The Definition class is based on the nametuple class and is responsible
    to check, parse and refactor a docstring definition item into sphinx
    friendly rst.

    Attributes
    ----------
    term : str
        The term usually reflects the name of a parameter or an attribute.

    classifiers: list
        The classifiers of the definition. Commonly used to reflect the type
        of an argument or the signature of a function.

        .. note:: Currently only one classifier is supported.

    definition : list
        The list of strings that holds the description the definition item.

    .. note:: A Definition item is based on the item of a section definition
        list as it defined in restructured text
        (_http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#sections).

    """

    @classmethod
    def is_item(cls, line):
        """ Check if the line is describing a definition item.

        The method is used to check that a line is following the expected
        format for the term and classifier attributes.

        The expected format is::

            +-------------------------------------------------+
            | term [ " : " classifier [ " or " classifier] ]  |
            +-------------------------------------------------+

        Subclasses can subclass to restrict or expand this format.

        """
        return definition_regex.match(line) is not None

    @classmethod
    def parse(cls, lines):
        """Parse a definition item from a set of lines.

        The class method parses the definition list item from the list of
        docstring lines and produces a DefinitionItem with the term,
        classifier and the definition.

        .. note:: The global indention in the definition lines is striped

        The term definition is assumed to be in one of the following formats::

            term
                Definition.

        ::

            term
                Definition, paragraph 1.

                Definition, paragraph 2.

        ::

            term : classifier
                Definition.

        ::

            term : classifier or classifier
                Definition.

        Arguments
        ---------
        lines
            docstring lines of the definition without any empty lines before or
            after.

        Returns
        -------
        definition : DefinitionItem

        """
        header = lines[0].strip()
        term, classifiers = header_regex.split(
            header, maxsplit=1) if (' :' in header) else (header, '')
        classifiers = [
            classifier.strip() for classifier in classifiers.split('or')]
        if classifiers == ['']:
            classifiers = []
        trimed_lines = trim_indent(lines[1:]) if (len(lines) > 1) else ['']
        definition = [line.rstrip() for line in trimed_lines]
        return Item(term.strip(), classifiers, definition)
