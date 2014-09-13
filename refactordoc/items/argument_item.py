from refactordoc.items.definition_item import DefinitionItem
from refactordoc.util import add_indent, fix_star, fix_trailing_underscore


class ArgumentItem(DefinitionItem):
    """ A definition item for function argument sections.

    """
    _normal = (":param {0}:\n"
               "{2}\n"
               ":type {0}: {1}")
    _no_definition = (":param {0}:\n"
                      ":type {0}: {1}")
    _no_classifier = (":param {0}:\n"
                      "{2}")
    _only_term = ":param {0}:"

    def to_rst(self):
        """ Render ArgumentItem in sphinx friendly rst using the ``:param:``
        role.

        Example
        -------

        ::

            >>> item = ArgumentItem('indent', 'int',
            ... ['The indent to use for the description block.',
                 ''
                 'This is the second paragraph of the argument definition.'])
            >>> item.to_rst()
            :param indent:
                The indent to use for the description block.

                This is the second paragraph of the argument definition.
            :type indent: int

        .. note::

            There is no new line added at the last line of the :meth:`to_rst`
            method.

        """
        argument = fix_star(self.term)
        argument = fix_trailing_underscore(argument)
        argument_type = self.classifier
        definition = '\n'.join(add_indent(self.definition))
        template = self.template.format(argument, argument_type, definition)
        return template.splitlines()

    @property
    def template(self):
        if self.classifier == '' and self.definition == ['']:
            template = self._only_term
        elif self.classifier == '':
            template = self._no_classifier
        elif self.definition == ['']:
            template = self._no_definition
        else:
            template = self._normal
        return template
