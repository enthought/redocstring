from refactordoc.items.item import Item
from refactordoc.items.regex import function_regex, signature_regex
from refactordoc.util import trim_indent


class MethodItem(Item):
    """ A MethodItem that knows how to parse methods

    """

    @property
    def signature(self):
        return '{0}({1})'.format(self.term, ', '.join(self.classifiers))

    @classmethod
    def is_item(cls, line):
        """ Check if the definition header is a function signature.

        """
        return function_regex.match(line)

    @classmethod
    def parse(cls, lines):
        """Parse a method definition item from a set of lines.

        The class method parses the method signature and definition from the
        list of docstring lines and produces a MethodItem where the term
        is the method name and the classifier is arguments

        .. note:: The global indention in the definition lines is striped

        The method definition item is assumed to be as follows::

            +------------------------------+
            | term "(" [  classifier ] ")" |
            +--+---------------------------+---+
               | definition                    |
               | (body elements)+              |
               +--------------------- ---------+

        Arguments
        ---------
        lines :
            docstring lines of the method definition item without any empty
            lines before or after.

        Returns
        -------
        definition : MethodItem

        """
        header = lines[0].strip()
        term, classifiers, _ = signature_regex.split(header)
        classifiers = [classifiers.strip()]
        definition = trim_indent(lines[1:]) if (len(lines) > 1) else ['']
        return cls(term, classifiers, definition)
