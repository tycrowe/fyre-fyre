import tkinter as tk

from fyre import FyreComponent, generate_ip_address


class FyreServer(FyreComponent):
    def __init__(self, platform, component, canvas, name: str, ip: str = None):
        super().__init__(platform, component)
        self.canvas = canvas
        self.component = component
        self.ip = ip if ip else generate_ip_address()
        self.name = name

        # Services
        self.running_services = []

        label = tk.Label(text=f'{self.ip}', master=self.component.frame)
        self.component.add_ui_component(label, drags_component=True)