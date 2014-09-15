from refactordoc.items.definition_item import DefinitionItem
from refactordoc.util import add_indent


class ListItem(DefinitionItem):
    """ A definition item that is rendered as an ordered/unordered list

    """

    _normal = ("**{0}** (*{1}*) --\n"
               "{2}\n\n")
    _only_term = "**{0}**\n\n"
    _no_definition = "**{0}** (*{1}*)\n\n"
    _no_classifier = ("**{0}** --\n"
                      "{2}\n\n")

    def to_rst(self, prefix=None):
        """ Outputs ListItem in rst using as items in an list.

        Arguments
        ---------
        prefix : str
            The prefix to use. For example if the item is part of a numbered
            list then ``prefix='-'``.

        Example
        -------

        >>> item = ListItem('indent', 'int',
        ... ['The indent to use for the description block.'])
        >>> item.to_rst(prefix='-')
        - **indent** (`int`) --
          The indent to use for the description block.

        >>> item = ListItem('indent', 'int',
        ... ['The indent to use for'
             'the description block.'])
        >>> item.to_rst(prefix='-')
        - **indent** (`int`) --
          The indent to use for
          the description block.


        .. note:: An empty line is added at the end of the list of strings so
            that the results can be concatenated directly and rendered properly
            by sphinx.

        """
        indent = 0 if (prefix is None) else len(prefix) + 1
        definition = '\n'.join(add_indent(self.definition, indent))
        template = self.template.format(
            self.term, ' or '.join(self.classifiers), definition)
        if prefix is not None:
            template = prefix + ' ' + template
        return template.splitlines()

    @property
    def template(self):
        if self.classifiers == [] and self.definition == ['']:
            template = self._only_term
        elif self.classifiers == []:
            template = self._no_classifier
        elif self.definition == ['']:
            template = self._no_definition
        else:
            template = self._normal
        return template
