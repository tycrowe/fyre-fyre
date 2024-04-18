import random


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



class FyreComponent:
    def __init__(self, platform: Platform, parent_ui_component: FyreUIComponent):
        self.platform = platform
        self.parent_ui_component = parent_ui_component



class FyreUIComponent:
    ui_components: List = []

    def __init__(self, frame: Frame):
        self.frame = frame

    def add_ui_component(self, component, drags_component: bool = True):
        """
        Adds a UI component to the frame of this component.
        :param component:       The component to add to the frame
        :param drags_component: True if the component should be draggable, False otherwise
        """
        if len(self.ui_components) == 0:
            component.grid(row=0, column=0)
        else:
            component.grid(row=len(self.ui_components), column=0)
        if drags_component:
            component.bind('<B1-Motion>', lambda event: handle_drag(self.frame, event))
        self.ui_components.append(component)
        self.frame.after_idle(self.resize_frame_by_ui_components)
        return component

    def resize_frame_by_ui_components(self):
        """
        Resizes the frame to fit all of the UI components that have been added to it.
        """
        width = max([component.winfo_width() for component in self.ui_components])
        height = sum([component.winfo_height() for component in self.ui_components])
        self.frame.config(width=width, height=height)

    def is_frame_inside(self, other: 'FyreComponent') -> bool:
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

    def draw_line_from_center(self, other: 'FyreComponent'):
        """
        Draws a line from the center of this component to the center of another component.
        :param other:   The other component to draw the line to
        :param canvas:  The canvas to draw the line on
        """
        x0, y0 = self.frame.winfo_x() + self.frame.winfo_width() // 2, self.frame.winfo_y() + self.frame.winfo_height() // 2
        x1, y1 = other.frame.winfo_x() + other.frame.winfo_width() // 2, other.frame.winfo_y() + other.frame.winfo_height() // 2
        canvas.create_line(x0, y0, x1, y1, fill='black', width=2)


