import tkinter as tk

from fyre.common.fyre_common import FyreComponent, generate_ip_address


class FyreClient(FyreComponent):
    dialogue = None

    def __init__(self, platform, canvas, fyre_ui_component, name: str, ip: str = None):
        super().__init__(platform, fyre_ui_component)
        self.canvas = canvas
        self.ip = ip if ip else generate_ip_address()
        self.name = name
        self.dialogue = None

        label = tk.Label(text=f'{self.ip}', master=self.parent_ui_component.frame)
        self.parent_ui_component.add_ui_component(label, drags_component=True)

        button = tk.Button(text="Manage", master=self.parent_ui_component.frame, command=self.handle_dialogue_on_click)
        self.parent_ui_component.add_ui_component(button, drags_component=False)

        self.platform.register_client(self)

    def handle_dialogue_on_click(self):
        """
        Handles the dialogue when the client is clicked.
        """
        if self.dialogue:
            self.dialogue.destroy()
        self.dialogue = tk.Toplevel()
        self.dialogue.title(f"{self.name} - {self.ip}: Command Window")
        self.dialogue.resizable(False, False)
        # Position the dialogue window on top of the client
        window_x, window_y = self.parent_ui_component.frame.winfo_rootx(), self.parent_ui_component.frame.winfo_rooty()
        x, y = window_x + self.parent_ui_component.frame.winfo_width() // 2, window_y + self.parent_ui_component.frame.winfo_height() // 2
        self.dialogue.geometry(f'{500}x{250}+{x}+{y}')
        self.dialogue.deiconify()

        # Add a label and text input to the dialogue for the "curl" command
        label = tk.Label(self.dialogue, text="Curl To:")
        label.grid(row=0, column=0, padx=10, pady=10)
        text_input = tk.Entry(self.dialogue, )
        text_input.grid(row=0, column=1, padx=10, pady=10)
        button = tk.Button(self.dialogue, text="Submit", command=lambda: self.handle_curl(text_input.get()))
        button.grid(row=0, column=2, padx=10, pady=10)

        self.dialogue.mainloop()
