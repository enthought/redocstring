import re

from sectiondoc.items.item import Item
from sectiondoc.util import trim_indent

definition_item_regex = re.compile(r"""
\*{0,2}                        # no, one or two stars
\w+                            # a word followed by
(
     \s:\s
     (
      [\w.]+                   # . separated words
     |
      \w+(\(.*\))?             # maybe a signature
     )
)*
$                              # match at the end of the line
""", re.VERBOSE)


class DefinitionItem(Item):
    """ A docstring definition section item.

    In this section definition item, multiple classifiers can be
    provided as shown in the diagram below.

    Syntax diagram::

        +-----------------------------+
        | term [ " : " classifier ]*  |
        +--+--------------------------+---+
           | definition                   |
           | (body elements)+             |
           +------------------------------+

    Attributes
    ----------
    term : str
        The term usually reflects the name of a parameter or an attribute.

    classifiers : list
        The classifiers of the definition. Commonly used to reflect the type
        of an argument or the signature of a function. Multiple classifiers
        are allowed separated by colons `` : ``.

    definition : list
        The list of strings that holds the description the definition item.

    """

    @classmethod
    def is_item(cls, line):
        """ Check if the line is describing a definition item.

        The method is used to check that a line is following the expected
        format for the term and classifier attributes.

        The expected format is::

            +----------------------------+
            | term [ " : " classifier ]* |
            +----------------------------+

        Subclasses can restrict or expand this format.

        """
        return definition_item_regex.match(line.rstrip()) is not None

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

            term : classifier : classifier
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
        components = [
            component.strip()
            for component in header.split(":") if component != '']
        term = components[0]
        if len(components) > 1:
            classifiers = components[1:]
        else:
            classifiers = []
        trimed_lines = trim_indent(lines[1:]) if (len(lines) > 1) else ['']
        definition = [line.rstrip() for line in trimed_lines]
        return Item(term.strip(), classifiers, definition)
