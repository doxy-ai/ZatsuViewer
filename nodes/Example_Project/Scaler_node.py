from PySide6 import QtWidgets

import sys
import os
sys.path.append(os.path.join(os.getcwd(), "nodes"))

from node_types import PureNode
from Example_Project.common_widgets import FloatLineEdit


class Scaler_Node(PureNode):
    def __init__(self):
        super().__init__()

        self.title_text = "Scaler"
        self.type_text = "Constants"
        self.set_color(title_color=(255, 165, 0))

        self.add_pin(name="value", t=float, is_output=True)

        self.build()

    def init_widget(self):
        self.widget = QtWidgets.QWidget()
        self.widget.setFixedWidth(100)
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        self.scaler_line = FloatLineEdit()
        layout.addWidget(self.scaler_line)
        self.widget.setLayout(layout)

        proxy = QtWidgets.QGraphicsProxyWidget()
        proxy.setWidget(self.widget)
        proxy.setParentItem(self)

        super().init_widget()

    def load(self, data):
        super().load(data)

        value = data["value"] if "value" in data else "0"
        self.scaler_line.setText(value)

    def save(self):
        data = super().save()

        data["value"] = self.scaler_line.text()
        # print(f"saving: {self.scaler_line.text()}")
        return data

    def get_value(self, pin):
        pin = self.validate_pin(pin)
        return float(self.scaler_line.text())
