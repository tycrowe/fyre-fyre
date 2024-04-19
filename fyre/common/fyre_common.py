import random


def generate_ip_address() -> str:
    return f'{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}'


class FyreComponent:
    def __init__(self, platform, parent_ui_component):
        self.platform = platform
        self.parent_ui_component = parent_ui_component

