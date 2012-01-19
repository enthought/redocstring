# -*- coding: UTF-8 -*-
#------------------------------------------------------------------------------
#  file: fields.py
#  License: LICENSE.TXT
#
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import collections
import re

from line_functions import add_indent, is_empty, remove_indent, replace_at, insert_empty


header_regex = re.compile('\s\:\s?')
definition_regex = re.compile('\*?\*?\w+\s:(\s+|$)')

class DefinitionItem(collections.namedtuple('Field', ('term','classifier','definition'))):
    """ A docstring definition item

    Syntax diagram::

    +----------------------------+
    | term [ " : " classifier ]* |
    +--+-------------------------+--+
       | definition                 |
       | (body elements)+           |
       +----------------------------+

    A Definition item is the base item of a section definition list.
    (please see _http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#sections)

    The Definition class is based on the nametuple class and is responsible
    for to check, parse and refactor a docstring definition item into sphinx
    friently rst.

    Attributes
    ----------
    term : str
        The term ussualy relects the name of a parameter or an attribute.

    classifier: str
        The classifier of the defintion. Commonly used to reflect the type
        of an argument or the signature of a function.

        .. note:: Currently only one classifier is supported.

    definition : str
        The description of the definition item.

    """

    @classmethod
    def is_definition(cls, line):
        """ Check if the line is describing a definition item.

        The method is used to check that a line is following the expected
        format for the term and classifier attributes.

        The expected format is::

        +----------------------------+
        | term [ " : " classifier ]  |
        +----------------------------+

        Subclasses can subclass to restict or expand this format.

        """
        return definition_regex.match(line)

    @classmethod
    def parse(cls, lines):
        """Parse a definition item from a set of lines.

        The field is assumed to be in one of the following formats::

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
        lines :
            docstring lines of the definition without any empty lines before or
            after.

        Returns
        -------
        definition : Definition

        """
        header = lines[0].strip()
        if ' :' in header:
            term, classifier = header_regex.split(header, maxsplit=1)
        else:
            arg_name, signature = header, ''
        if len(lines) > 1:
            lines = [line.rstrip() for line in lines]
            return cls(arg_name.strip(), signature.strip(), lines[1:])
        else:
            return cls(arg_name.strip(), signature.strip(), [''])


    def to_rst(self):
        """ Outputs the Definition in sphinx friendly rst.

        The method renders the definition into a list of lines that follow
        the rst markup. The default behaviour is to render the definition
        as an sphinx definition item::

        <term>

           (<classifier>) --
           <definition>

        Subclasses will ussualy override the method to provide custom made
        behaviour.

        Arguments
        ---------
        indent : int
            The indent to use for the decription block. Default is 4 spaces

        Returns
        -------
        lines : list
            A list of string lines rendered in rst.

        Example
        -------

        >>> Field('Ioannis', 'Ιωάννης', 'Is the greek guy.')
        >>> print Field.to_rst()
        Ioannis

            *(Ιωάννης)* --
            Is the greek guy.

        """
        lines = []
        lines += [self.term]
        iines += ['*({0})*'.format(self.classifier)]
        lines += [self.definition]
        return lines



class AttributeField(Field):
    """ Field that renders the rst output as an attribute """

    def to_rst(self, indent=4):
        """ Outputs field in rst using the ``:param:`` role.

        Arguments
        ---------
        indent : int
            The indent to use for the decription block.

        Example
        -------

        >>> Field('indent', 'int', 'The indent to use for the decription block.')
        >>> print Field.to_rst()
        The indent to use for the description block
        :type indent: int

        """
        lines = []
        _type = self.signature
        annotation = '{0}    :annotation: = {1}'
        type_str = '' if is_empty(_type) else annotation.format(indent * ' ', _type)
        directive = '{0}.. attribute:: {1}'
        lines += [directive.format(indent * ' ', self.name), type_str]
        if type_str != '':
            lines.append('')
        lines += self.desc
        lines.append('')
        return lines


class ArgumentField(Field):
    """ Field for the argument function docstrings """

    def to_rst(self, indent=4):
        """ Outputs field in rst using the ``:param:`` role.

        Arguments
        ---------
        indent : int
            The indent to use for the decription block.

        Example
        -------

        >>> Field('indent', 'int', 'The indent to use for the decription block.')
        >>> print Field.to_rst()
        :param indent: The indent to use for the description block
        :type indent: int

        """
        lines = []
        name = self.name.replace('*','\*')  # Fix cases like *args and **kwargs
        indent_str = ' ' * indent
        param_str = '{0}:param {1}: {2}'.format(indent_str, name, self.desc[0].strip())
        type_str = '{0}:type {1}: {2}'.format(indent_str, name, self.signature)
        lines.append(param_str)
        lines += self.desc[1:]
        if len(self.signature) > 0:
            lines.append(type_str)
        return lines

class ListItemField(Field):
    """ Field that in rst is formated as an item in the list ignoring any
    field.type information.

    """

    def to_rst(self, indent=4, prefix=''):
        """ Outputs field in rst using as items in an list.

        Arguments
        ---------
        indent : int
            The indent to use for the decription block.

        prefix : str
            The prefix to use. For example if the item is part of a numbered
            list then ``prefix='# '``.

        Example
        -------


        Note
        ----
        The field descrption is reformated into a line.

        """
        indent_str = ' ' * indent
        rst_pattern = '{0}{1}**{2}**{3}' if is_empty(self.desc[0]) else \
                       '{0}{1}**{2}** -- {3}'
        description = '' if is_empty(self.desc[0]) else \
                      ' '.join(remove_indent(self.desc))
        return [rst_pattern.format(indent_str, prefix, self.name, description)]


class ListItemWithTypeField(Field):
    """ Field for the return section of the function docstrings """
    def to_rst(self, indent=4, prefix=''):
        indent_str = ' ' * indent
        _type = '' if self.signature == '' else '({0})'.format(self.signature)
        rst_pattern = '{0}{1}**{2}** {3}{4}' if is_empty(self.desc[0]) else \
                       '{0}{1}**{2}** {3} -- {4}'
        description = '' if is_empty(self.desc[0]) else \
                    ' '.join(remove_indent(self.desc))
        return [rst_pattern.format(indent_str, prefix, self.name, _type, description)]


class FunctionField(Field):
    """ A field that represents a function """

    @classmethod
    def is_field(cls, line, indent=''):
        regex = indent + r'\w+\(.*\)\s*'
        match = re.match(regex, line)
        return match

    def to_rst(self, length, first_column, second_column):
                split_result = re.split('\((.*)\)', self.name)
                method_name = split_result[0]
                method_text = ':meth:`{0} <{1}>`'.format(self.name, method_name)
                summary = ' '.join([line.strip() for line in self.desc])
                line = ' ' * length
                line = replace_at(method_text, line, first_column)
                line = replace_at(summary, line, second_column)
                return [line]

MethodField = FunctionField

#------------------------------------------------------------------------------
#  Functions to work with fields
#------------------------------------------------------------------------------

def max_name_length(method_fields):
    """ Find the max length of the function name in a list of method fields.

    Arguments
    ---------
    fields : list
        The list of the parsed fields.

    """
    return max([field[0].find('(') for field in method_fields])

def max_header_length(fields):
    """ Find the max length of the header in a list of fields.

    Arguments
    ---------
    fields : list
        The list of the parsed fields.

    """
    return max([len(field[0]) for field in fields])

def max_desc_length(fields):
    """ Find the max length of the description in a list of fields.

    Arguments
    ---------
    fields : list
        The list of the parsed fields.

    """
    return max([len(' '.join([line.strip() for line in field[2]]))
                for field in fields])
