class Style(object):

    def __init__(self, refactoring_map):
        self.refactoring_map = refactoring_map

    def refactor_docstring(self, app, what, name, obj, options, lines):
        docstring_renderer = self.refactoring_map.get(what, None)
        if docstring_renderer is not None:
            docstring_renderer(lines)
            docstring_renderer.parse()
