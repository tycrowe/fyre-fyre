import tkinter as tk

from fyre.common.fyre_common import FyreComponent, generate_ip_address


class FyreServer(FyreComponent):
    def __init__(self, platform, canvas, fyre_ui_component, name: str, ip: str = None):
        super().__init__(platform, fyre_ui_component)
        self.canvas = canvas
        self.ip = ip if ip else generate_ip_address()
        self.name = name

        # Services
        self.running_services = []

        label = tk.Label(text=f'{self.ip}', master=self.parent_ui_component.frame)
        self.parent_ui_component.add_ui_component(label, drags_component=True)

        self.platform.register_server(self)
