import sys
import os
print(os.getcwd())
sys.path.append(os.path.join(os.getcwd(), "nodes"))
print(sys.path)

from node_types import Node


class If_Node(Node):
    def __init__(self):
        super().__init__()

        self.title_text = "If"
        self.type_text = "Logic Nodes"
        self.set_color(title_color=(0, 128, 0))

        self.condition = self.add_pin(name="condition", t=bool)
        self.elsePin = self.add_execution_pin(name="else", is_output=True)
        for pin in self.output_execution_pins():
            pin.execution_show_text = True
        self.build()

    def execute(self):
        if bool(self.condition.get_value()):
            self.execute_next()
        else: self.elsePin.execute_next()
