import json
import tkinter as tk

from scapy.layers.inet import TCP, IP
from scapy.packet import Packet

from fyre.common.fyre_common import FyreComponent


class Fyrewall(FyreComponent):
    def __init__(self, platform, canvas, fyre_ui_component, name: str):
        super().__init__(platform, fyre_ui_component)
        self.canvas = canvas
        self.name = name
        self.allowed_ports = []
        self.blocked_ips = []
        self.add_configuration_buttons()
        self.platform.register_firewall(self)

    def add_allowed_port(self, port: int):
        self.allowed_ports.append(port)

    def add_blocked_ip(self, ip: str):
        self.blocked_ips.append(ip)

    def is_component_within_firewall(self, fyre_component: FyreComponent):
        return self.parent_ui_component.has_component(fyre_component.parent_ui_component)

    def process_packet(self, packet: Packet):
        print(f"Packet received by {self.name}! Firewall will now process it.")
        port = packet[TCP].dport
        print(f"Packet is destined for port {port}. Determining if port is allowed...")

        if port not in self.allowed_ports:
            print(f"Port {port} is not allowed. Dropping packet.")
            return

        if packet[IP].src in self.blocked_ips:
            print(f"Source IP {packet[IP].src} is blocked. Dropping packet.")
            return

        # Read dictionary from Raw layer of packet
        print(f"Packet content: {packet.load.decode()}")

    def add_configuration_buttons(self):
        """
        Adds buttons to the top of the UI frame for managing the firewall configuration.
        :return:
        """
        button = tk.Button(text="Manage", master=self.parent_ui_component.frame, command=lambda: self.open_configuration_window())
        self.parent_ui_component.add_ui_component(button, drags_component=False, min_width=250, min_height=250)

    def open_configuration_window(self):
        """
        Opens a configuration window for the firewall.
        :return:
        """
        def save_configuration():
            """
            Saves the configuration of the firewall.
            :return:
            """
            data = text.get("1.0", tk.END)
            try:
                config = json.loads(data)
                self.allowed_ports = config["allowed_ports"]
                self.blocked_ips = config["blocked_ips"]
                print(f"Configuration saved for {self.name}.")
                config_window.destroy()
            except json.JSONDecodeError:
                print("Invalid JSON configuration.")

        # Create a new top-level window for the firewall configuration
        config_window = tk.Toplevel()
        config_window.title(f"{self.name} Configuration")
        config_window.resizable(False, False)
        # Position the configuration window on top of the firewall
        window_x, window_y = self.parent_ui_component.frame.winfo_rootx(), self.parent_ui_component.frame.winfo_rooty()
        x, y = window_x + self.parent_ui_component.frame.winfo_width() // 2, window_y + self.parent_ui_component.frame.winfo_height() // 2
        config_window.geometry(f'{500}x{250}+{x}+{y}')
        config_window.deiconify()

        # Show an editable text field that shows the configuration in a json format
        text = tk.Text(config_window)
        text.pack()
        config_as_json = {
            "allowed_ports": self.allowed_ports,
            "blocked_ips": self.blocked_ips
        }

        text.insert(tk.END, json.dumps(config_as_json, indent=4))

        # Add a menu for saving the configuration
        save_menu = tk.Menu(config_window)
        config_window.config(menu=save_menu)
        save_menu.add_command(label="Save", command=save_configuration)

        config_window.mainloop()


