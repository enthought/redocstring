from sectiondoc.renderers.renderer import Renderer


class Method(Renderer):
    """ Render method items as a table row.
    """

    def to_rst(self, columns=(0, 0)):
        """ Outputs definition in rst as a line in a table.

        Arguments
        ---------
        columns : tuple
            The two item tuple of column widths for the `:meth:` role column
            and the definition (i.e. summary) of the MethodItem

        .. note:: The string attributes are clipped to the column width.

        Example
        -------

        ::

            >>> item = MethodItem('function', 'arg1, arg2',
            ... ['This is the best function ever.'])
            >>> renderer = Method(item)
            >>> renderer.to_rst(columns=(40, 20))
            :meth:`function <function(arg1, arg2)>` This is the best fun

        """
        item = self.item
        definition = ' '.join([line.strip() for line in item.definition])
        method_role = ':meth:`{0}({1}) <{0}>`'.format(
            item.term, ', '.join(item.classifiers))
        table_line = '{0:<{first}} {1:<{second}}'
        lines = []
        lines += [table_line.format(method_role[:columns[0]],
                                    definition[:columns[1]], first=columns[0],
                                    second=columns[1])]
        return lines
