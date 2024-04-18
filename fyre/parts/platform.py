from typing import List


class Platform:
    def __init__(self):
        self.addresses: List[str] = []
        self.clients = []
        self.servers = []

    def register_client(self, client):
        """
        Registers a client with the fyrefyre program.
        :param client: the client to register
        """
        from fyre.parts.client import FyreClient
        if isinstance(client, FyreClient):
            if client.ip not in self.addresses:
                self.addresses.append(client.ip)
                self.clients.append(client)
                return True
            raise ValueError(f"CIP address {client.ip} already exists.")

    def register_server(self, server):
        """
        Registers a server with the fyrefyre program.
        :param server: the server to register
        """
        from fyre.parts.server import FyreServer
        if isinstance(server, FyreServer):
            if server.ip not in self.addresses:
                self.addresses.append(server.ip)
                self.servers.append(server)
                return True
            raise ValueError(f"IP address {server.ip} already exists.")

    def get_server_by_ip(self, ip: str):
        """
        Gets a server by its IP address.
        :param ip: the IP address of the server
        :return: the server object
        """
        from fyre.parts.server import FyreServer
        for server in self.servers:
            if isinstance(server, FyreServer) and server.ip == ip:
                return server
        raise ValueError(f"Server with IP address {ip} not found.")

    def get_client_by_ip(self, ip: str):
        """
        Gets a client by its IP address.
        :param ip: the IP address of the client
        :return: the client object
        """
        from fyre.parts.client import FyreClient
        for client in self.clients:
            if isinstance(client, FyreClient) and client.ip == ip:
                return client
        raise ValueError(f"Client with IP address {ip} not found.")

    def get_fyre_component_by_ip(self, ip: str):
        """
        Gets a fyre component by its IP address.
        :param ip: the IP address of the fyre component
        :return: the fyre component object
        """
        from fyre.parts.client import FyreClient
        from fyre.parts.server import FyreServer
        for client in self.clients:
            if isinstance(client, FyreClient) and client.ip == ip:
                return client.component
        for server in self.servers:
            if isinstance(server, FyreServer) and server.ip == ip:
                return server.component
        raise ValueError(f"Fyre component with IP address {ip} not found.")