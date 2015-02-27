from sectiondoc.renderers.renderer import Renderer
from sectiondoc.util import add_indent, NEW_LINE


class Definition(Renderer):
    """ Render an Item instance as a sphinx definition term

    """

    def to_rst(self, **kwards):
        """ Outputs the Item in sphinx friendly rst.

        The method renders the `definition` into a list of lines that
        follow the rst markup of a sphinx definition item::

            <term>

               (<classifier(s)>) --
               <definition>

        Returns
        -------
        lines : list
            A list of string lines rendered in rst.

        Example
        -------

        ::

            >>> item = Item(
                    'lines', 'list',
                    ['A list of string lines rendered in rst.'])
            >>> renderer = Definition(item)
            >>> renderer.to_rst
            lines

                *(list)* --
                A list of string lines rendered in rst.

        .. note:: An empty line is added at the end of the list of strings so
            that the results can be concatenated directly and rendered properly
            by sphinx.


        """
        item = self.item
        postfix = ' --' if (len(item.definition) > 0) else ''
        lines = []
        lines += [item.term]
        lines += [NEW_LINE]
        number_of_classifiers = len(item.classifiers)
        if number_of_classifiers == 1:
            lines += ['    *({0[0]})*{1}'.format(item.classifiers, postfix)]
        elif number_of_classifiers == 2:
            lines += [
                '    *({0[0]} or {0[1]})*{2}'.format(
                    item.classifiers, postfix)]
        lines += add_indent(item.definition)  # definition is already a list
        lines += [NEW_LINE]
        return lines
