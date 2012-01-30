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

from line_functions import (add_indent, is_empty, remove_indent, replace_at,
                            fix_star, trim_indent, NEW_LINE)

header_regex = re.compile(r'\s:\s')
definition_regex = re.compile(r'\*?\*?\w+(\s:\s\w+)?$')
function_regex=re.compile(r'\w+\(.*\)\s*')
signature_regex = re.compile('\((.*)\)')

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

        >>> item = DefintionItem('lines', 'list',
                                 ['A list of string lines rendered in rst.'])
        >>> print item.to_rst()
        lines

            *(list)* --
            A list of string lines rendered in rst.

        """
        postfix = ' --' if (len(self.definition) > 0) else ''
        lines = []
        lines += [self.term]
        lines += [NEW_LINE]
        lines += ['    *({0})*{1}'.format(self.classifier, postfix)]
        lines += add_indent(self.definition)  # definition is all ready a list
        lines += [NEW_LINE]
        return lines


class AttributeItem(DefinitionItem):
    """ Definition that renders the rst output using the attribute directive.
    """

    def to_rst(self, ):
        """ Return the attribute info ousing the attrbiute sphinx markup.

        Examples
        --------

        >>> item = AttributeItem('indent', 'int',
        ... ['The indent to use for the decription block.'])
        >>> print item.to_rst()
        .. attribute:: indent
            :annotation: = int

            The indent to use for the description block
        >>>


        >>> item = AttributeItem('indent', '',
        ... ['The indent to use for the decription block.'])
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
        lines += add_indent(definition)
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
        ... ['The indent to use for the description block.',
             ''
             'This is the second paragraph of the argument definition.'])
        >>> print item.to_rst()
        :param indent: The indent to use for the description block.

            This is the second paragraph of the argument definition.
        :type indent: int

        """
        argument = fix_star(self.term)
        argument_type = self.classifier
        type_role = [''] if (argument_type == '') else \
                    [':type {0}: {1}'.format(argument, argument_type)]
        header =  ':param {0}: ' + self.definition[0].strip()
        definition = [''] + self.definition[1:]
        footer = type_role if (argument_type == '') else type_role + ['']

        lines = []
        lines += [header.format(argument)]
        lines += add_indent(definition)
        lines += footer
        return lines

class ListItem(DefinitionItem):
    """ A defintion item that is rendered as an ordered/unordered list

    """

    def to_rst(self, prefix=''):
        """ Outputs ListItem in rst using as items in an list.

        Arguments
        ---------
        prefix : str
            The prefix to use. For example if the item is part of a numbered
            list then ``prefix='#'``.

        Example
        -------

        >>> item = ListItem('indent', 'int',
        ... ['The indent to use for the description block.'])
        >>> item.to_rst(prefix='-')
        - indent (`int`) -- The indent to use for the descirption block.

        >>> item = ListItem('indent', 'int',
        ... ['The indent to use for'
             'the description block.'])
        >>> item.to_rst(prefix='-')
        - indent (`int`) -- The indent to use for the descirption block.

        """
        header = '' if prefix == '' else '{0} '.format(prefix)
        indent = len(header)
        header += '{0}' if self.classifier == '' else '{0} (`{1}`)'
        header += '' if self.definition[0] == '' else ' --'
        header += '' if len(self.definition) > 1 else ' {2}'
        definition = self.definition + [''] if len(self.definition) > 1 else ['']
        lines = []
        lines += [header.format(self.term, self.classifier, self.definition[0])]
        lines += add_indent(definition, indent=indent)
        return lines


class TableLineItem(DefinitionItem):
    """ A Definition Item that represents a table line.

    """

    def to_rst(self, columns=(0, 0, 0)):
        """ Outputs definition in rst as a line in a table.

        Arguments
        ---------
        columns : tuple
            The three item tuple of column widths for the term, classifier
            and definition fields of the TableLineItem. When the column width
            is 0 then the field

        .. note:: The strings attributes are cliped to the column width.

        Example
        -------

        >>> item = TableLineItem('function(arg1, arg2)', '',
        ... ['This is the best function ever.'])
        >>> item.to_rst(columns=(22, 0, 20))
        function(arg1, arg2)   This is the best fun

        """
        definition = ' '.join([line.strip() for line in self.definition])
        term = self.term[:columns[0]]
        classifier = self.classifier[:columns[1]]
        definition = definition[:columns[2]]

        first_column = '' if columns[0] == 0 else '{0:<{first}} '
        second_column = '' if columns[1] == 0 else '{1:<{second}} '
        third_column = '' if columns[2] == 0 else '{2:<{third}}'
        table_line = ''.join((first_column, second_column, third_column))

        lines = []
        lines += [table_line.format(term, classifier, definition,
                  first=columns[0], second=columns[1], third=columns[2])]
        lines += ['']
        return lines

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

        The class method parses the method signature and defintion from the
        list of docstring lines and produces a MethodItem where the term
        is the method name and the classifier is arguments

        .. note:: The global indention in the definition lines is striped

        The method definition item is assumed to be as follows::

        method(arguments)
            Definition in a single line.


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

    def to_rst(self, columns=(0,0)):
        """ Outputs definition in rst as a line in a table.

        Arguments
        ---------
        columns : tuple
            The two item tuple of column widths for the :meth: role column
            and the definition (i.e. summary) of the MethodItem

        .. note:: The strings attributes are cliped to the column width.

        Example
        -------

        >>> item = MethodItem('function', 'arg1, arg2',
        ... ['This is the best function ever.'])
        >>> item.to_rst(columns=(40, 20))
        :meth:`function <function(arg1, arg2)>` This is the best fun

        """
        definition = ' '.join([line.strip() for line in self.definition])
        method_role = ':meth:`{0} <{0}({1})>`'.format(self.term, self.classifier)
        table_line = '{0:<{first}} {1:<{second}}'

        lines = []
        lines += [table_line.format(method_role[:columns[0]],
                                    definition[:columns[1]], first=columns[0],
                                    second=columns[1])]
        lines += ['']
        return lines


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
