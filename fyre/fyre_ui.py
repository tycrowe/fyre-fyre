import tkinter as tk

from tkinter import Frame
from typing import List

from fyre.parts.client import FyreClient
from fyre.parts.server import FyreServer

WIN_WIDTH = 800
WIN_HEIGHT = 600


def handle_drag(component, event):
    """
    Handles the dragging of a component on the screen. Moves the component to the new location by the center of the
    component.
    :param component:   The component being dragged
    :param event:       The event that triggered the drag
    """
    x, y = event.x, event.y
    x0, y0 = component.winfo_x(), component.winfo_y()
    xc, yc = component.winfo_width() // 2, component.winfo_height() // 2
    component.place(x=x0 + x - xc, y=y0 + y - yc)


class FyreUIComponent:
    ui_components: List = []

    def __init__(self, frame: Frame):
        self.frame = frame

    def add_ui_component(self, ui_component, drags_component: bool = True):
        """
        Adds a UI component to the frame of this component.
        :param ui_component:        The tkinter UI component to add
        :param drags_component:     True if the component should be draggable, False otherwise
        """
        if len(self.ui_components) == 0:
            ui_component.grid(row=0, column=0)
        else:
            ui_component.grid(row=len(self.ui_components), column=0)
        if drags_component:
            ui_component.bind('<B1-Motion>', lambda event: handle_drag(self.frame, event))
        self.ui_components.append(ui_component)
        self.frame.after_idle(self.resize_frame_by_ui_components)
        return ui_component

    def resize_frame_by_ui_components(self):
        """
        Resizes the frame to fit all of the UI components that have been added to it.
        """
        width = max([component.winfo_width() for component in self.ui_components])
        height = sum([component.winfo_height() for component in self.ui_components])
        self.frame.config(width=width, height=height)

    def is_frame_inside(self, other) -> bool:
        """
        Checks if the frame of this component is inside the frame of another component.
        :param other:   The other component to check against
        :return:        True if this component is inside the other component, False otherwise
        """
        x0, y0 = self.frame.winfo_x(), self.frame.winfo_y()
        x1, y1 = x0 + self.frame.winfo_width(), y0 + self.frame.winfo_height()
        x2, y2 = other.frame.winfo_x(), other.frame.winfo_y()
        x3, y3 = x2 + other.frame.winfo_width(), y2 + other.frame.winfo_height()
        return x0 >= x2 and y0 >= y2 and x1 <= x3 and y1 <= y3

    def draw_line_from_center(self, canvas, other):
        """
        Draws a line from the center of this component to the center of another component.
        :param canvas:  The canvas to draw the line on
        :param other:   The other component to draw the line to
        """

        x0, y0 = self.frame.winfo_x() + self.frame.winfo_width() // 2, self.frame.winfo_y() + self.frame.winfo_height() // 2
        x1, y1 = other.frame.winfo_x() + other.frame.winfo_width() // 2, other.frame.winfo_y() + other.frame.winfo_height() // 2
        canvas.create_line(x0, y0, x1, y1, fill='black', width=2)


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


def create_interface_components(win: tk.Tk, canvas: tk.Canvas, platform):
    """
    Creates the static components of the interface that do not change.
    :param win:         the tkinter window object
    :param canvas:      the canvas object to draw lines on
    :param platform:    the platform object to register components with
    :return:
    """

    client_frame = tk.LabelFrame(win, text="Client", width=120, height=60, borderwidth=2, relief='solid', border=2)
    client_fyre_component = make_draggable_fyre_component(client_frame, 100, 100)
    fyre_client = FyreClient(platform, canvas, client_fyre_component, 'Client')

    server_frame = tk.LabelFrame(win, text="Server", width=120, height=60, borderwidth=2, relief='solid', border=2)
    server_fyre_component = make_draggable_fyre_component(server_frame, 500, 100)
    fyre_server = FyreServer(platform, canvas, server_fyre_component, 'Server')

    firewall_frame = tk.LabelFrame(win, text="Firewall", width=250, height=250, borderwidth=2, relief='solid', border=2)
    firewall_fyre_component = make_draggable_fyre_component(firewall_frame, 300, 300)

    server_frame.lift()
    client_frame.lift()


def create_interface(platform) -> tk.Tk:
    """
    Creates a tkinter interface for the user to interact with the program.
    :param platform: the platform object to register components with
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

    canvas = tk.Canvas(win, width=WIN_WIDTH, height=WIN_HEIGHT)
    canvas.pack()

    create_interface_components(win, canvas, platform)

    return win