from sectiondoc.renderers.renderer import Renderer
from sectiondoc.util import add_indent


class Attribute(Renderer):
    """ Render an Item instance using the sphinx attribute directive.

    """

    templates = {
        "full": ".. attribute:: {0}\n    :annotation: = {1}\n\n{2}\n\n",
        "no_definition": ".. attribute:: {0}\n    :annotation: = {1}\n\n",
        "no_classifiers": ".. attribute:: {0}\n\n{2}\n\n",
        "only_term": ".. attribute:: {0}\n\n"}

    def to_rst(self):
        """ Return the attribute info using the attribute sphinx markup.


        Examples
        --------

        ::

            >>> item = Item('indent', 'int',
            ... ['The indent to use for the description block.'])
            >>> Attribute(item).to_rst()
            .. attribute:: indent
                :annotation: = `int`

                The indent to use for the description block
            >>>

        ::

            >>> item = Item('indent', '',
            ... ['The indent to use for the description block.'])
            >>> Attribute(item).to_rst()
            .. attribute:: indent

                The indent to use for the description block
            >>>

        .. note:: An empty line is added at the end of the list of strings so
            that the results can be concatenated directly and rendered properly
            by sphinx.

        """
        item = self.item
        definition = '\n'.join(add_indent(item.definition))
        template = self.templates[item.mode].format(
            item.term, ' or '.join(item.classifiers), definition)
        return template.splitlines()
