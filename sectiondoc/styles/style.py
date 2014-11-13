class Style(object):

    def __init__(self, rendering_map):
        self.rendering_map = rendering_map

    def render_docstring(self, app, what, name, obj, options, lines):
        renderer_factory = self.rendering_map.get(what, None)
        if renderer_factory is not None:
            docstring_renderer = renderer_factory(lines)
            docstring_renderer.parse()
