from sectiondoc.items.item import Item
from sectiondoc.items.regex import function_regex, signature_regex
from sectiondoc.util import trim_indent


class MethodItem(Item):
    """ A MethodItem for method descriptions.

    """

    @property
    def signature(self):
        return '{0}({1})'.format(self.term, ', '.join(self.classifiers))

    @classmethod
    def is_item(cls, line):
        """ Check if the definition header is a function signature.

        The expected header has the following format::

          +------------------------------+
          | term "(" [  classifier ] ")" |
          +------------------------------+

        """
        return function_regex.match(line)

    @classmethod
    def parse(cls, lines):
        """ Parse a method definition item from a set of lines.

        Parse the method signature and definition from the list of docstring
        lines and produce a MethodItem where the `term` is the method name and
        the classifier is arguments.

        .. note:: The global indention in the definition lines is striped

        The format of the method definition item is expected to be as follows::

          +------------------------------+
          | term "(" [  classifier ] ")" |
          +--+---------------------------+---+
             | definition                    |
             | (body elements)+              |
             +-------------------------------+

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
