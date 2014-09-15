from refactordoc.items.definition_item import DefinitionItem


class TableRowItem(DefinitionItem):
    """ A Definition Item that represents a table line.

    """

    def to_rst(self, columns=(0, 0, 0)):
        """ Outputs definition in rst as a line in a table.

        Arguments
        ---------
        columns : tuple
            The three item tuple of column widths for the term, classifiers
            and definition fields of the TableLineItem. When the column width
            is 0 then the field is empty.

        .. note::
            - The strings attributes are clipped to the column width.

        Example
        -------

        >>> item = TableRowItem('function(arg1, arg2)', '',
        ... ['This is the best function ever.'])
        >>> item.to_rst(columns=(22, 0, 20))
        function(arg1, arg2)   This is the best fun

        """
        definition = ' '.join([line.strip() for line in self.definition])
        term = self.term[:columns[0]]
        classifiers = ', '.join(self.classifiers)[:columns[1]]
        definition = definition[:columns[2]]

        first_column = '' if columns[0] == 0 else '{0:<{first}} '
        second_column = '' if columns[1] == 0 else '{1:<{second}} '
        third_column = '' if columns[2] == 0 else '{2:<{third}}'
        table_line = ''.join((first_column, second_column, third_column))

        lines = []
        lines += [table_line.format(term, classifiers, definition,
                  first=columns[0], second=columns[1], third=columns[2])]
        lines += ['']
        return lines
