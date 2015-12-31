import re

from sectiondoc.items.regex import definition_regex, header_regex
from sectiondoc.items.item import Item
from sectiondoc.util import trim_indent

any_item_regex = re.compile(r"""
\*{0,2}            # no, one or two stars
\w+                # a word followed by
(\s:?)?            # space or ` :`
(.+)?              # a classifier
$                  # match at the end of the line
""", re.VERBOSE)


class AnyItem(Item):
    """ A docstring definition section item.

    In this section item there are it a most one classifier composed
    of multiple words.

    Syntax diagram::

        +-------------------------------------------------+
        | term [ " : " text ]                             |
        +--+----------------------------------------------+---+
           | definition                                       |
           | (body elements)+                                 |
           +--------------------------------------------------+

    Attributes
    ----------
    term : str
        The term usually reflects the name of a parameter or an attribute.

    classifiers : list
        The classifiers of the definition. Commonly used to reflect the type
        of an argument or the signature of a function. Any text after the
        ` : ` till the end of the line is consider a classifier.

    definition : list
        The list of strings that holds the description the definition item.

    .. note::

       AnyItem is probably closer to numpydoc on describing a section item.

    """

    @classmethod
    def is_item(cls, line):
        """ Check if the line is describing a definition item.

        The method is used to check that a line is following the expected
        format for the term and classifier attributes.

        The expected format is::

            +-------------------------------------------------+
            | term [ " : "  text ]                            |
            +-------------------------------------------------+

        Subclasses can restrict or expand this format.

        """
        return any_item_regex.match(line) is not None

    @classmethod
    def parse(cls, lines):
        """Parse a definition item from a set of lines.

        The class method parses the definition list item from the list of
        docstring lines and produces a DefinitionItem with the term,
        classifier and the definition.

        .. note:: The global indention in the definition lines is striped.

        The term definition is assumed to be in one of the following formats::

            term
                Definition.

        ::

            term :
                Definition.

        ::

            term
                Definition, paragraph 1.

                Definition, paragraph 2.

        ::
            term:
                Definition, paragraph 1.

                Definition, paragraph 2.

        ::

            term : classifier
                Definition.

        Arguments
        ---------
        lines
            docstring lines of the definition without any empty lines before or
            after.

        Returns
        -------
        definition : AnyItem

        """
        header = lines[0].strip()
        term, classifier = header_regex.split(header, maxsplit=1) if \
            (' :' in header) else (header, '')
        classifier = classifier.strip()
        classifier = [] if classifier == '' else [classifier]
        trimed_lines = trim_indent(lines[1:]) if (len(lines) > 1) else []
        definition = [line.rstrip() for line in trimed_lines]
        return cls(term.strip(), classifier, definition)
