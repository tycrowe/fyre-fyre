import tkinter as tk

from fyre.common.fyre_common import FyreComponent, generate_ip_address


class FyreService:
    def __init__(self, server, name: str, port: int):
        self.server = server
        self.name = name
        self.port = port
        self.status = 'stopped'  # Default status
        self.allowed_ips = []

    def start(self):
        self.status = 'running'

    def stop(self):
        self.status = 'stopped'

    def add_ip(self, ip: str):
        self.allowed_ips.append(ip)


class FyreServer(FyreComponent):
    def __init__(self, platform, canvas, fyre_ui_component, name: str, ip: str = None):
        super().__init__(platform, fyre_ui_component)
        self.canvas = canvas
        self.ip = ip if ip else generate_ip_address()
        self.name = name
        self.status = 'running'  # Default status
        self.services = {}  # Dictionary to hold services and their statuses

        # Adding a label to display IP address on the server's component UI
        label = tk.Label(text=f'IP: {self.ip} | Status: {self.status}', master=self.parent_ui_component.frame)
        self.parent_ui_component.add_ui_component(label, drags_component=True, min_width=200)

        self.platform.register_server(self)

    def register_service(self, service_name: str, port: int):
        """
        Starts a service on the server.
        :param service_name: the name of the service
        :param port: the port number for the service
        """
        if service_name not in self.services:
            service = FyreService(self, service_name, port)
            service.start()
            self.services[service_name] = service
            # self.parent_ui_component.add_ui_component(
            #     tk.Label(text=f"Service: {service_name} | Port: {port} | Status: {service.status}",
            #              master=self.parent_ui_component.frame), drags_component=True)
