#------------------------------------------------------------------------------
#  file: function.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
from base_doc import (BaseDoc, get_indent, is_empty, remove_indent,
                      add_indent, Field)


class ArgumentField(Field):

    def rst(self, indent=''):
        lines = []
        name = self.name.replace('*','\*')
        param_str = indent + ':param {0}: {1}'.format(name, self.desc[0].strip())
        type_str = indent + ':type {0}: {1}'.format(name, self.type)
        lines.append(param_str)
        for line in self.desc[1:]:
            lines.append('{0}'.format(line))
        if len(self.type) > 0:
            lines.append(type_str)
        return lines


class FunctionDoc(BaseDoc):
    """Docstring refactoring for functions"""

    def __init__(self, lines, headers=None, verbose=False):

        if headers is None:
            headers = {'Returns': 'returns', 'Arguments': 'arguments',
                       'Parameters': 'arguments', 'Raises': 'raises',
                       'Yields': 'returns', 'Notes':'notes'}

        super(FunctionDoc, self).__init__(lines, headers, verbose)
        return

    def _refactor_returns(self, header):
        """Refactor the return section to sphinx friendly format"""

        if self.verbose:
            print 'Returns section refactoring'

        descriptions = []
        index = self.index
        self.remove_lines(index, 2)
        indent = get_indent(self.peek())
        fields = self.extract_fields(indent)

        if self.verbose:
            print 'Return items'
            print fields

        # generate sphinx friendly rst
        descriptions = []
        descriptions.append(indent + ':returns:')
        if len(fields) == 1:
            name_format = '**{0}** '
        else:
            name_format = '- **{0}** '

        for arg_name, arg_type, desc in fields:
            arg_name = indent + '    ' + name_format.format(arg_name)
            if arg_type != '':
                arg_type = '({0})'.format(arg_type)
            else:
                arg_type = ''
            if not is_empty(desc[0]):
                arg_type = arg_type + ' - '
            paragraph = ' '.join(remove_indent(desc))
            descriptions.append(arg_name + arg_type + paragraph)

        self.insert_lines(descriptions, index)
        self.index += len(descriptions)
        return

    def _refactor_raises(self, header):
        """Refactor the raises section to sphinx friendly format"""

        if self.verbose:
            print 'Raised section refactoring'

        descriptions = []
        index = self.index
        self.remove_lines(index, 2)
        indent = get_indent(self.peek())
        fields = self.extract_fields(indent)

        if self.verbose:
            print 'Raised Errors'
            print fields

        descriptions = []
        descriptions.append(indent + ':raises:')
        if len(fields) == 1:
            name_format = '**{0}** '
        else:
            name_format = '- **{0}** '

        for arg_name, arg_type, desc in fields:
            if not is_empty(desc[0]):
                arg_name = name_format.format(arg_name) + '- '
            else:
                arg_name = name_format.format(arg_name)
            arg_name = indent + '    ' + arg_name
            paragraph = ' '.join(remove_indent(desc))
            descriptions.append(arg_name + paragraph)

        self.insert_lines(descriptions, index)
        self.index += len(descriptions)
        return

    def _refactor_arguments(self, header):
        """Refactor the argument section to sphinx friendly format
        """
        index = self.index
        self.remove_lines(index, 2)
        indent = get_indent(self.peek())
        fields = self.extract_fields(indent)

        lines = []
        for field in fields:
            argument_field = ArgumentField._make(field)
            lines += argument_field.rst(indent)

        self.insert_lines(lines, index)
        self.index += len(lines)
        return

    def _refactor_notes(self, header):
        """Refactor the argument section to sphinx friendly format.

        """
        if self.verbose:
            print 'Refactoring Notes'

        descriptions = []
        index = self.index
        self.remove_lines(index, 2)
        indent = get_indent(self.peek())
        paragraph = self.get_next_paragraph()
        descriptions.append(indent + '.. note::')
        descriptions += add_indent(paragraph)
        self.insert_lines(descriptions, index)
        self.index += len(descriptions)
        return descriptions

