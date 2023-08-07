import sys
import os
print(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), "nodes"))
print(sys.path)

from node_types import PureNode


class Add_Node(PureNode):
    def __init__(self):
        super().__init__()

        self.title_text = "Add"
        self.type_text = "Logic Nodes"
        self.set_color(title_color=(0, 128, 0))

        self.A = self.add_pin(name="A")
        self.B = self.add_pin(name="B")
        self.add_pin(name="output", is_output=True)
        self.build()

    def get_value(self, pin):
        pin = self.validate_pin(pin)
        A = self.A.get_value()
        B = self.B.get_value()
        return A + B

class Greater_Node(PureNode):
    def __init__(self):
        super().__init__()

        self.title_text = "Greater"
        self.type_text = "Logic Nodes"
        self.set_color(title_color=(0, 128, 0))

        self.A = self.add_pin(name="A")
        self.B = self.add_pin(name="B")
        self.add_pin(name="output", t=bool, is_output=True)
        self.build()

    def get_value(self, pin):
        pin = self.validate_pin(pin)
        A = self.A.get_value()
        B = self.B.get_value()
        return A > B
