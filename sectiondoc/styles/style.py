class Style(object):

    def __init__(self, refactoring_map):
        self.refactoring_map = refactoring_map

    def refactor_docstring(self, app, what, name, obj, options, lines):
        renderer_factory = self.refactoring_map.get(what, None)
        if renderer_factory is not None:
            docstring_renderer = renderer_factory(lines)
            docstring_renderer.parse()
