import tkinter as tk

from fyre.fyre_ui import create_interface
from fyre.parts.platform import Platform

if __name__ == '__main__':
    platform = Platform()
    main_window = create_interface(platform)
    # Start the main loop
    main_window.mainloop()
