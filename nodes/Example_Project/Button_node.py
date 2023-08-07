from PySide6 import QtWidgets

import sys
import os
import threading

sys.path.append(os.path.join(os.getcwd(), "nodes"))

from node_types import PlatformNode, EventNode
from pins import DataPin


class Button_Node(PlatformNode):
    def __init__(self):
        super().__init__("Button Platform")
        DataPin.setup_default_colors() #TODO: This should not be happening here!

        self.title_text = "Button"
        self.type_text = "Platforms"
        self.set_color(title_color=(128, 0, 0))

        self.build()

    def init_widget(self):
        self.widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        btn = QtWidgets.QPushButton("Button test")
        btn.clicked.connect(self.btn_cmd)
        layout.addWidget(btn)
        self.widget.setLayout(layout)

        proxy = QtWidgets.QGraphicsProxyWidget()
        proxy.setWidget(self.widget)
        proxy.setParentItem(self)

        super().init_widget()

    def btn_cmd(self):
        print("btn command")
        self.events.on_pressed()




class OnButton_Node(EventNode):
    def __init__(self):
        super().__init__("OnButton Pressed")
        DataPin.setup_default_colors() #TODO: This should not be happening here!

        self.title_text = "On Button"
        self.type_text = "Events"
        self.set_color(title_color=(128, 0, 0))

        self.build()

    def on_connected(self, connection):
        try: self.platform_from_connection(connection).events.on_pressed += self.execute_next
        except AttributeError: pass # platform_from_connection(connection) may return none if the user clicks on the output pin within 1ms of a previous disconnect!

    def on_disconnected(self, connection):
        self.platform_from_connection(connection).events.on_pressed -= self.execute_next
