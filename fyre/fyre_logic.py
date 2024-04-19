from scapy.all import *
from scapy.layers.inet import TCP, IP


def create_packet(ip, port, body, headers) -> Packet:
    # Create a web request with the given body using scapy
    return IP(dst=ip) / TCP(dport=port) / body / headers
