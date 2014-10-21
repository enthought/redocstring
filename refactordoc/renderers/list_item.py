from refactordoc.renderers import Renderer
from refactordoc.util import add_indent


class ListItem(Renderer):
    """ A definition item that is rendered as an ordered/unordered list

    """

    templates = {
        "full": "**{0}** (*{1}*) --\n{2}\n\n",
        "only_term": "**{0}**\n\n",
        "no_definition": "**{0}** (*{1}*)\n\n",
        "no_classifiers": "**{0}** --\n{2}\n\n"}

    def to_rst(self, prefix=None):
        """ Renders an item as items in an rst list.

        Arguments
        ---------
        prefix : str
            The prefix to use. For example if the item is part of an
            unnumbered list then ``prefix='-'``.

        Example
        -------

        >>> item = Item('indent', 'int',
        ... ['The indent to use for the description block.'])
        >>> renderer = ListItem(item)
        >>> renderer.to_rst(prefix='-')
        - **indent** (`int`) --
          The indent to use for the description block.

        >>> item = Item('indent', 'int',
        ... ['The indent to use for'
             'the description block.'])
        >>> renderer = ListItem(item)
        >>> renderer.to_rst(prefix='-')
        - **indent** (`int`) --
          The indent to use for
          the description block.


        .. note:: An empty line is added at the end of the list of strings so
            that the results can be concatenated directly and rendered properly
            by sphinx.

        """
        item = self.item
        indent = 0 if (prefix is None) else len(prefix) + 1
        definition = '\n'.join(add_indent(item.definition, indent))
        template = self.templates[item.mode].format(
            item.term, ' or '.join(item.classifiers), definition)
        if prefix is not None:
            template = prefix + ' ' + template
        return template.splitlines()
