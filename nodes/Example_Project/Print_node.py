import sys
import os
sys.path.append(os.path.join(os.getcwd(), "nodes"))

from node_types import Node


class Print_Node(Node):
    def __init__(self):
        super().__init__()

        self.title_text = "Print"
        self.type_text = "Debug Nodes"
        self.set_color(title_color=(160, 32, 240))

        self.input = self.add_pin(name="input", is_output=False)
        self.build()

    def execute(self):
        print(self.input.get_value())
        self.execute_next()
