from fyre.common.fyre_common import FyreComponent


class Fyrewall(FyreComponent):
    def __init__(self, platform, canvas, fyre_ui_component, name: str):
        super().__init__(platform, fyre_ui_component)
        self.canvas = canvas
        self.name = name

        self.platform.register_firewall(self)

    def is_component_within_firewall(self, fyre_component: FyreComponent):
        return self.parent_ui_component.is_inside(fyre_component.parent_ui_component)
