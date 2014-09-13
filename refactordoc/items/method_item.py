import re

from refactordoc.items.definition_item import DefinitionItem
from refactordoc.util import trim_indent


function_regex = re.compile(r'\w+\(.*\)\s*')
signature_regex = re.compile('\((.*)\)')


class MethodItem(DefinitionItem):
    """ A TableLineItem subclass to parse and render class methods.

    """
    @classmethod
    def is_definition(cls, line):
        """ Check if the definition header is a function signature.

        """
        match = function_regex.match(line)
        return match

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
        term, classifier, _ = signature_regex.split(header)
        definition = trim_indent(lines[1:]) if (len(lines) > 1) else ['']
        return cls(term, classifier, definition)

    def to_rst(self, columns=(0, 0)):
        """ Outputs definition in rst as a line in a table.

        Arguments
        ---------
        columns : tuple
            The two item tuple of column widths for the :meth: role column
            and the definition (i.e. summary) of the MethodItem

        .. note:: The strings attributes are clipped to the column width.

        Example
        -------

        ::

            >>> item = MethodItem('function', 'arg1, arg2',
            ... ['This is the best function ever.'])
            >>> item.to_rst(columns=(40, 20))
            :meth:`function <function(arg1, arg2)>` This is the best fun

        """
        definition = ' '.join([line.strip() for line in self.definition])
        method_role = ':meth:`{0}({1}) <{0}>`'.format(self.term,
                                                      self.classifier)
        table_line = '{0:<{first}} {1:<{second}}'

        lines = []
        lines += [table_line.format(method_role[:columns[0]],
                                    definition[:columns[1]], first=columns[0],
                                    second=columns[1])]
        return lines

    @property
    def signature(self):
        return '{0}({1})'.format(self.term, self.classifier)
