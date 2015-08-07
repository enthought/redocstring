from sectiondoc.renderers.renderer import Renderer
from sectiondoc.util import add_indent, fix_star, fix_trailing_underscore


class Argument(Renderer):
    """ Render an item as a sphinx parameter role.

    """
    templates = {
        "full": ":param {0}:\n{2}\n:type {0}: {1}",
        "no_definition": ":param {0}:\n:type {0}: {1}",
        "no_classifiers": ":param {0}:\n{2}",
        "only_term": ":param {0}:"}

    def to_rst(self):
        """ Render an item as an argument using the ``:param:``
        role.

        Example
        -------

        ::

            >>> item = Item('indent', 'int',
            ... ['The indent to use for the description block.',
                 ''
                 'This is the second paragraph of the argument definition.'])
            >>> renderer = Argument(item)
            >>> renderer.to_rst()
            :param indent:
                The indent to use for the description block.
                This is the second paragraph of the argument definition.
            :type indent: int

        .. note::

            There is no new line added at the last line of the :meth:`to_rst`
            method.

        """
        item = self.item
        argument = fix_star(item.term)
        argument = fix_trailing_underscore(argument)
        argument_types = ' or '.join(item.classifiers)
        definition = '\n'.join(add_indent(item.definition))
        template = self.templates[item.mode].format(
            argument, argument_types, definition)
        return template.splitlines()
