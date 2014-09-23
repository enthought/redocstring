from refactordoc.util import add_indent, fix_star, fix_trailing_underscore
from .definition_item import DefinitionItem


class ArgumentItem(DefinitionItem):
    """ A definition item for function argument sections.

    """
    _normal = (
        ":param {0}:\n"
        "{2}\n"
        ":type {0}: {1}")
    _no_definition = (":param {0}:\n"
                      ":type {0}: {1}")
    _no_classifiers = (
        ":param {0}:\n"
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
        argument_types = ' or '.join(self.classifiers)
        definition = '\n'.join(add_indent(self.definition))
        template = self.template.format(argument, argument_types, definition)
        return template.splitlines()

    @property
    def template(self):
        if self.classifiers == [] and self.definition == ['']:
            template = self._only_term
        elif self.classifiers == []:
            template = self._no_classifiers
        elif self.definition == ['']:
            template = self._no_definition
        else:
            template = self._normal
        return template
