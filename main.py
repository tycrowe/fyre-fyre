import tkinter as tk

from fyre.fyre_ui import create_interface
from fyre.parts.platform import Platform

if __name__ == '__main__':
    platform = Platform()
    main_window = create_interface(platform)
    # Get each server
    from fyre.parts.server import FyreServer
    for server in platform.servers:
        if isinstance(server, FyreServer):
            server.register_service('website', 80)
            server.register_service('email', 25)
            server.register_service('ftp', 21)
            server.register_service('ssh', 22)
            server.register_service('webapp', 8080)
            server.register_service('database', 3306)
    # Start the main loop
    main_window.mainloop()
