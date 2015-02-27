import abc


class Renderer(object):
    """ An item renderer.
    """

    def __init__(self, item=None):
        self.item = item

    @abc.abstractmethod
    def to_rst(self, **kwards):
        """ Outputs the `item` in sphinx friendly rst.

        The method renders the passed into a list of lines that follow
        the rst markup.

        Subclasses need to override the method to provide their custom made
        behaviour. However the signature of the method should hold only
        keyword arguments which always have default values.

        Returns
        -------
        lines : list
            A list of string lines rendered in rst.

        """
