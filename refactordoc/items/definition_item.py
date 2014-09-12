import collections
import re

from refactordoc.util import (
    add_indent, fix_star, trim_indent, NEW_LINE, fix_trailing_underscore)



#: Regex to use for matching the header for the d
header_regex = re.compile(r'\s:\s?')

#:
definition_regex = re.compile(r"""
\*{0,2}            #  no, one or two stars
\w+\s:             #  a word followed by a semicolumn and optionally a space
(
        \s         # just a space
    |              # OR
        \s[\w.]+   # dot separated words
        (\(.*\))?  # with maybe a signature
    |
        \s[\w.]+   # dot separated words
        (\(.*\))?
        \sor       # with an or in between
        \s[\w.]+
        (\(.*\))?
)?
$                  # match at the end of the line
""", re.VERBOSE)


class DefinitionItem(collections.namedtuple(
        'DefinitionItem', ('term', 'classifier', 'definition'))):
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

    classifier: str
        The classifier of the definition. Commonly used to reflect the type
        of an argument or the signature of a function.

        .. note:: Currently only one classifier is supported.

    definition : list
        The list of strings that holds the description the definition item.

    .. note:: A Definition item is based on the item of a section definition
        list as it defined in restructured text
        (_http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#sections).

    """

    @classmethod
    def is_definition(cls, line):
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
        term, classifier = header_regex.split(header, maxsplit=1) if \
                           (' :' in header) else (header, '')
        trimed_lines = trim_indent(lines[1:]) if (len(lines) > 1) else ['']
        definition = [line.rstrip() for line in trimed_lines]
        return cls(term.strip(), classifier.strip(), definition)

    def to_rst(self, **kwards):
        """ Outputs the Definition in sphinx friendly rst.

        The method renders the definition into a list of lines that follow
        the rst markup. The default behaviour is to render the definition
        as an sphinx definition item::

            <term>

               (<classifier>) --
               <definition>

        Subclasses will usually override the method to provide custom made
        behaviour. However the signature of the method should hold only
        keyword arguments which have default values. The keyword arguments
        can be used to pass addition rendering information to subclasses.

        Returns
        -------
        lines : list
            A list of string lines rendered in rst.

        Example
        -------

        ::

            >>> item = DefinitionItem('lines', 'list',
                                ['A list of string lines rendered in rst.'])
            >>> item.to_rst()
            lines

                *(list)* --
                A list of string lines rendered in rst.

        .. note:: An empty line is added at the end of the list of strings so
            that the results can be concatenated directly and rendered properly
            by sphinx.


        """
        postfix = ' --' if (len(self.definition) > 0) else ''
        lines = []
        lines += [self.term]
        lines += [NEW_LINE]
        lines += ['    *({0})*{1}'.format(self.classifier, postfix)]
        lines += add_indent(self.definition)  # definition is all ready a list
        lines += [NEW_LINE]
        return lines
