from refactordoc.rendirexderers.renderer import Renderer


class TableRow(Renderer):
    """ Render an Item that represents a table line.

    """

    def to_rst(self, columns=(0, 0, 0)):
        """ Outputs definition in rst as a line in a table.

        Arguments
        ---------
        columns : tuple
            The three item tuple of column widths for the term, classifiers
            and definition fields of the TableLineItem. When the column width
            is 0 then the field is ignored.

        .. note::
            - The strings attributes are clipped to the column width.

        Example
        -------

        >>> item = Item('function(arg1, arg2)', '',
        ... ['This is the best function ever.'])
        >>> TableRow(item).to_rst(columns=(22, 0, 20))
        function(arg1, arg2)   This is the best fun

        """
        item = self.item
        definition = ' '.join([line.strip() for line in item.definition])
        term = item.term[:columns[0]]
        classifiers = ', '.join(item.classifiers)[:columns[1]]
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
