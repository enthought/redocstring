# -*- coding: UTF-8 -*-
#------------------------------------------------------------------------------
#  file: fields.py
#  License: LICENSE.TXT
#  Author: Ioannis Tziakos
#
#  Copyright (c) 2011, Enthought, Inc.
#  All rights reserved.
#------------------------------------------------------------------------------
import collections
import re

from line_functions import add_indent, is_empty, remove_indent, replace_at, fix_star


header_regex = re.compile(r'\s:\s')
definition_regex = re.compile(r'\*?\*?\w+(\s:\s\w+)?$')

class DefinitionItem(collections.namedtuple('Field', ('term','classifier','definition'))):
    """ A docstring definition item

    Syntax diagram::

    +----------------------------+
    | term [ " : " classifier ]  |
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

    definition : list
        The list of strings that holdes the description the defintion item.

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

        Subclasses can subclass to restrict or expand this format.

        """
        return definition_regex.match(line) is not None

    @classmethod
    def parse(cls, lines):
        """Parse a definition item from a set of lines.

        The class method parses the defintion list item from the list of
        docstring lines and produces a DefinitionItem with the term,
        classifier and the definition.

        .. note:: The indention in the definition lines is not striped

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
        definition : DefinitionItem

        """
        header = lines[0].strip()
        term, classifier = header_regex.split(header, maxsplit=1) if \
                           (' :' in header) else (header, '')
        definition = [line.rstrip() for line in lines[1:]] if \
                     (len(lines) > 1) else ['']
        return cls(term.strip(), classifier.strip(), definition)


    def to_rst(self, **kwards):
        """ Outputs the Definition in sphinx friendly rst.

        The method renders the definition into a list of lines that follow
        the rst markup. The default behaviour is to render the definition
        as an sphinx definition item::

        <term>

           (<classifier>) --
           <definition>

        Subclasses will ussualy override the method to provide custom made
        behaviour. However the singature of the method should hold only
        kword arguments which have default values. The keyword arguments
        can be used to pass addition rendering information to subclasses.

        Returns
        -------
        lines : list
            A list of string lines rendered in rst.

        Example
        -------

        >>> item = DefintionItem('lines', 'list', 'A list of string lines rendered in rst.')
        >>> print item.to_rst()
        lines

            *(list)* --
            A list of string lines rendered in rst.

        """
        postfix = ' --' if (len(self.definition) > 0) else ''
        lines = []
        lines += [self.term]
        lines += ['']
        lines += ['    *({0})*{1}'.format(self.classifier, postfix)]
        lines += self.definition  # definition is all ready a list
        lines += ['']
        return lines


class AttributeItem(DefinitionItem):
    """ Definition that renders the rst output using the attribute directive.
    """

    def to_rst(self, ):
        """ Return the attribute info ousing the attrbiute sphinx markup.

        Examples
        --------

        >>> item = AttributeItem('indent', 'int',
        ... ['    The indent to use for the decription block.'])
        >>> print item.to_rst()
        .. attribute:: indent
            :annotation: = int

            The indent to use for the description block
        >>>


        >>> item = AttributeItem('indent', '',
        ... ['    The indent to use for the decription block.'])
        >>> print item.to_rst()
        .. attribute:: indent

            The indent to use for the description block
        >>>

        """
        attr_type = self.classifier
        directive = '.. attribute:: {0}'
        annotation = '' if is_empty(attr_type) else '    :annotation: = {0}'
        definition = self.definition if (annotation == '') \
                     else [''] + self.definition
        lines = []
        lines += [directive.format(self.term)]
        lines += [annotation.format(attr_type)]
        lines += definition
        lines += ['']
        return lines


class ArgumentItem(DefinitionItem):
    """ A definition item for function argument sections """

    def to_rst(self):
        """ Render ArgumentItem in sphinx friendly rst using the
        ``:param:`` role.

        Example
        -------

        >>> item = ArgumentItem('indent', 'int',
        ... ['    The indent to use for the description block.',
             ''
             '    This is the second paragraph of the argument definition.'])
        >>> print item.to_rst()
        :param indent: The indent to use for the description block.

            This is the second paragraph of the argument definition.
        :type indent: int

        """
        argument = fix_star(self.term)
        argumemt_type = self.classifier
        type_role = [''] if (_type == '') else \
                    [':type {0}: {1}'.format(parameter, argumemt_type)]
        header =  ':param {0}: ' + self.definition[0].strip()
        definition = [''] + self.definition[1:]
        footer = parameter_type if (argument_type == '') else \
                 parameter_type + ['']

        lines = []
        lines += [header.format(parameter)]
        lines += definition
        lines += footer
        return lines

class ListItemField(DefinitionItem):
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


class ListItemWithTypeField(DefinitionItem):
    """ Field for the return section of the function docstrings """
    def to_rst(self, indent=4, prefix=''):
        indent_str = ' ' * indent
        _type = '' if self.signature == '' else '({0})'.format(self.signature)
        rst_pattern = '{0}{1}**{2}** {3}{4}' if is_empty(self.desc[0]) else \
                       '{0}{1}**{2}** {3} -- {4}'
        description = '' if is_empty(self.desc[0]) else \
                    ' '.join(remove_indent(self.desc))
        return [rst_pattern.format(indent_str, prefix, self.name, _type, description)]


class FunctionField(DefinitionItem):
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

def max_name_length(method_definition_items):
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
