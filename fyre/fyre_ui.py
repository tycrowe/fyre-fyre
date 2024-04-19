import tkinter as tk
import random as r

from tkinter import Frame
from typing import List

from fyre.parts.client import FyreClient
from fyre.parts.server import FyreServer
from fyre.parts.firewall import Fyrewall

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
        frame.grid_propagate(False)

    def add_ui_component(self, ui_component, drags_component: bool = True, min_width: int = 0, min_height: int = 0):
        """
        Adds a UI component to the frame of this component.
        :param min_height:          The minimum height of the frame
        :param min_width:           The minimum width of the frame
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
        self.frame.after_idle(lambda: self.resize_frame_by_ui_components(min_width, min_height))
        return ui_component

    def resize_frame_by_ui_components(self, min_width: int, min_height: int):
        """
        Resizes the frame to fit all of the UI components that have been added to it.
        """
        width = max([component.winfo_width() for component in self.ui_components])
        height = sum([component.winfo_height() for component in self.ui_components])
        self.frame.config(width=max(width, min_width), height=max(height, min_height))

    def has_component(self, other) -> bool:
        """
        Checks if the frame of this component is inside the frame of another component.
        :param other:   The other component to check against
        :return:        True if this component is inside the other component, False otherwise
        """
        current_x_pos, current_y_pos = self.frame.winfo_x(), self.frame.winfo_y()
        other_x_pos, other_y_pos = other.frame.winfo_x(), other.frame.winfo_y()

        current_width, current_height = self.frame.winfo_width(), self.frame.winfo_height()
        other_width, other_height = other.frame.winfo_width(), other.frame.winfo_height()

        # Now, we want to return if the other component is inside the current component
        return current_x_pos <= other_x_pos and current_y_pos <= other_y_pos and \
               current_x_pos + current_width >= other_x_pos + other_width and current_y_pos + current_height >= other_y_pos + other_height

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
    def get_random_coordinates(width, height):
        x, y = r.randint(0, WIN_WIDTH), r.randint(0, WIN_HEIGHT)
        # Ensure the component is within the window
        if x + width > WIN_WIDTH:
            x -= width
        if y + height > WIN_HEIGHT:
            y -= height
        return x, y

    def create_client_component():
        x, y = get_random_coordinates(120, 60)
        client_frame = tk.LabelFrame(win, text="Client", width=120, height=60, borderwidth=2, relief='solid', border=2)
        client_fyre_component = make_draggable_fyre_component(client_frame, x, y)
        client_frame.lift()
        return FyreClient(platform, canvas, client_fyre_component, f'Client {r.randint(0, 100000)}')

    def create_server_component():
        x, y = get_random_coordinates(120, 60)
        server_frame = tk.LabelFrame(win, text="Server", width=120, height=60, borderwidth=2, relief='solid', border=2)
        server_fyre_component = make_draggable_fyre_component(server_frame, x, y)
        server_frame.lift()
        return FyreServer(platform, canvas, server_fyre_component, 'Server')

    def create_firewall_component():
        x, y = get_random_coordinates(250, 250)
        firewall_frame = tk.LabelFrame(win, text="Firewall", width=250, height=250, borderwidth=2, relief='solid', border=2)
        firewall_fyre_component = make_draggable_fyre_component(firewall_frame, x, y)
        firewall_frame.tkraise(canvas)
        return Fyrewall(platform, canvas, firewall_fyre_component, 'Firewall')

    # Create a top-level menu for adding components
    menu = tk.Menu(win)
    win.config(menu=menu)

    # Create a menu for adding components
    add_menu = tk.Menu(menu)
    menu.add_cascade(label="Add", menu=add_menu)
    add_menu.add_command(label="Client", command=lambda: create_client_component())
    add_menu.add_command(label="Server", command=lambda: create_server_component())
    add_menu.add_command(label="Firewall", command=lambda: create_firewall_component())

    create_firewall_component()
    create_client_component()
    create_server_component()


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