import tkinter as tk
from scapy.all import *

from fyre.parts.client import FyreClient
from fyre.parts.server import FyreServer
from fyre import FyreUIComponent, handle_drag

WIN_WIDTH = 800
WIN_HEIGHT = 600


def make_draggable_fyre_component(frame, x: int, y: int) -> FyreUIComponent:
    """
    Creates a static frame component with a label that can be dragged around the screen. The label will be added to the
    center of the created frame. Both the frame and the label will be draggable, however, the frame will be the only
    part of the component that will actually move.
    :param frame:       The frame object to add the label to
    :param x:           The x-coordinate of the container
    :param y:           The y-coordinate of the container
    :return:            A FyreComponent object that contains the frame and label
    """
    frame.place(x=x, y=y)
    frame.bind('<B1-Motion>', lambda event: handle_drag(frame, event))
    return FyreUIComponent(frame)


def create_interface_components(win: tk.Tk):
    """
    Creates the static components of the interface that do not change.
    :param win: the tkinter window object
    :return:
    """

    client_frame = tk.LabelFrame(win, text="Client", width=120, height=60, borderwidth=2, relief='solid', border=2)
    client_fyre_component = make_draggable_fyre_component(client_frame, 100, 100)
    fyre_client = FyreClient(canvas, client_fyre_component, 'Client')
    platform.register_client(fyre_client)

    server_frame = tk.LabelFrame(win, text="Server", width=120, height=60, borderwidth=2, relief='solid', border=2)
    server_fyre_component = make_draggable_fyre_component(server_frame, 500, 100)
    fyre_server = FyreServer(server_fyre_component, 'Server')
    platform.register_server(fyre_server)

    firewall_frame = tk.LabelFrame(win, text="Firewall", width=250, height=250, borderwidth=2, relief='solid', border=2)
    firewall_fyre_component = make_draggable_fyre_component(firewall_frame, 300, 300)

    server_frame.lift()
    client_frame.lift()


def create_interface() -> tk.Tk:
    """
    Creates a tkinter interface for the user to interact with the program.
    :return: the tkinter window object
    """
    win = tk.Tk()
    win.title('FyreFyre')
    win.geometry(f'{WIN_WIDTH}x{WIN_HEIGHT}')
    win.eval('tk::PlaceWindow . center')
    win.resizable(False, False)

    win.update_idletasks()
    width = win.winfo_width()
    frm_width = win.winfo_rootx() - win.winfo_x()
    win_width = width + 2 * frm_width
    height = win.winfo_height()
    titlebar_height = win.winfo_rooty() - win.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = win.winfo_screenwidth() // 2 - win_width // 2
    y = win.winfo_screenheight() // 2 - win_height // 2
    win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    win.deiconify()

    return win


if __name__ == '__main__':
    main_window = create_interface()
    # Add the canvas to the window
    canvas = tk.Canvas(main_window, width=WIN_WIDTH, height=WIN_HEIGHT)
    canvas.pack()
    # Build UI
    create_interface_components(main_window)
    # Start the main loop
    main_window.mainloop()
