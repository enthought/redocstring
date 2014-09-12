from refactordoc.items.definition_item import DefinitionItem
from refactordoc.util import add_indent


class AttributeItem(DefinitionItem):
    """ Definition that renders the rst output using the attribute directive.

    """
    _normal = (".. attribute:: {0}\n"
               "    :annotation: = {1}\n"
               "\n"
               "{2}\n\n")
    _no_definition = (".. attribute:: {0}\n"
                      "    :annotation: = {1}\n\n")
    _no_classifier = (".. attribute:: {0}\n\n"
                      "{2}\n\n")
    _only_term = ".. attribute:: {0}\n\n"

    def to_rst(self, ):
        """ Return the attribute info using the attribute sphinx markup.

        Examples
        --------

        ::

            >>> item = AttributeItem('indent', 'int',
            ... ['The indent to use for the description block.'])
            >>> item.to_rst()
            .. attribute:: indent
                :annotation: = int

                The indent to use for the description block
            >>>

        ::

            >>> item = AttributeItem('indent', '',
            ... ['The indent to use for the description block.'])
            >>> item.to_rst()
            .. attribute:: indent

                The indent to use for the description block
            >>>

        .. note:: An empty line is added at the end of the list of strings so
            that the results can be concatenated directly and rendered properly
            by sphinx.

        """
        definition = '\n'.join(add_indent(self.definition))
        template = self.template.format(self.term, self.classifier, definition)
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
