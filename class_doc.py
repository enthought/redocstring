#------------------------------------------------------------------------------
#  file: refactor_doc.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import re
from base_doc import (BaseDoc, get_indent, replace_at, max_header_length,
                      max_desc_length, add_indent, is_method_field)

def max_name_length(method_fields):
    """ Find the max length of the function name in a list of method fields.

    Arguments
    ---------
    fields : list
        The list of the parsed fields.

    """
    return max([field[0].find('(') for field in method_fields])


class ClassDoc(BaseDoc):
    """Docstring refactoring for classes"""

    def __init__(self, lines, headers=None, verbose=False):

        if headers is None:
            headers = {'Attributes': 'attributes', 'Methods': 'methods',
                       'See Also': 'header', 'Abstract Methods': 'methods',
                       'Notes':'notes'}

        super(ClassDoc, self).__init__(lines, headers, verbose)
        return

    def _refactor_attributes(self, header):
        """Refactor the attributes section to sphinx friendly format"""

        if self.verbose:
            print '{0} Section'.format(header)

        index = self.index
        self.remove_lines(index, 2)
        indent = get_indent(self.peek())
        parameters = self.extract_fields(indent)

        descriptions = []
        for arg_name, arg_type, desc in parameters:
            descriptions.append(indent + '.. attribute:: {0}'.\
                                format(arg_name))
            description_indent = get_indent(desc[0])
            descriptions.append('')
            if arg_type != '':
                arg_type = description_indent + '*({0})*'.format(arg_type)
                descriptions.append(arg_type)
            for line in desc:
                descriptions.append('{0}'.format(line))
            descriptions.append('')

        self.insert_lines(descriptions[:-1], index)
        self.index += len(descriptions)
        return

    def _refactor_methods(self, header):
        """Refactor the methods section to sphinx friendly format.

        """
        if self.verbose:
            print '{0} section'.format(header)

        index = self.index
        self.remove_lines(index, 2)
        indent = get_indent(self.peek())
        method_fields = self.extract_fields(indent, is_method_field)

        lines = []
        if len(method_fields) > 0 :
            name_length = max_name_length(method_fields)
            method_length = max_header_length(method_fields)
            desc_length = max_desc_length(method_fields)
            first_column_start = len(indent)
            first_column_length = method_length + name_length + 7
            second_column_start = first_column_start + first_column_length + 1
            table_line = '{0}{1} {2}'.format(indent, '=' * first_column_length,
                                             '=' * desc_length)
            empty_line = table_line.replace('=', ' ')
            headings_line = empty_line[:]
            headings_line = replace_at(
                                        'Methods', headings_line,
                                        first_column_start)
            headings_line = replace_at(
                                        'Description', headings_line,
                                        second_column_start)
            lines.append(table_line)
            lines.append(headings_line)
            lines.append(table_line)
            for arg_name, arg_type, desc in method_fields:
                split_result = re.split('\((.*)\)', arg_name)
                name = split_result[0]
                method_text = ':meth:`{0} <{1}>`'.format(arg_name, name)
                summary = ' '.join([line.strip() for line in desc])
                line = empty_line[:]
                line = replace_at(method_text, line, first_column_start)
                line = replace_at(summary, line, second_column_start)
                lines.append(line)
            lines.append(table_line)

        lines = [line.rstrip() for line in lines]
        self.insert_lines(lines, index)
        self.index += len(lines)
        return

    def _refactor_notes(self, header):
        """Refactor the note section to use the rst ``.. note`` directive.

        """
        if self.verbose:
            print '{0} Section'.format(header)
        descriptions = []
        index = self.index
        self.remove_lines(index, 2)
        indent = get_indent(self.peek())
        paragraph = self.get_next_paragraph()
        if self.verbose:
            print 'PARAGRAPH'
            print ''.join(paragraph)
        descriptions.append(indent + '.. note::')
        descriptions += add_indent(paragraph)
        self.insert_lines(descriptions, index)
        self.index += len(descriptions)
        return descriptions
