import random

from scapy.layers.inet import TCP, IP
from scapy.packet import Raw


def generate_ip_address() -> str:
    return f'{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}'


class FyreComponent:
    def __init__(self, platform, parent_ui_component):
        self.platform = platform
        self.parent_ui_component = parent_ui_component

    def __str__(self):
        return f"{self.__class__.__name__} {self.parent_ui_component}"

    def send_packet(self, ip: str, port: int, sport: int, content):
        packet = IP(dst=ip)/TCP(sport=sport, dport=port,flags='S')/Raw(load=content)
        typehint, destination = self.platform.get_fyre_component_by_ip(ip)
        if destination:
            destination.receive_packet(packet)
        else:
            raise ValueError(f"Destination IP {ip} not found.")

    def receive_packet(self, packet):
        firewall = self.platform.determine_if_component_is_within_firewall(self)
        if firewall:
            firewall.process_packet(packet)
        else:
            self.process_packet(packet)

    def process_packet(self, packet):
        print(f"Packet processed by {self}: {packet.summary()}")
