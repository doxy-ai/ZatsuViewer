from events import Events
import sys, os
from zatsu.app import KThread # Should we go dirrect to thirdparty here?
from zatsu.message import Message
from PySide6 import QtWidgets
import asyncio

# sys.path.insert(0, os.path.dirname(__file__))
from zatsu.nodes.node_types import PlatformNode
# from zatsu.nodes.pins

class ChatOnlyPlatformNode(PlatformNode):
	has_target_stream_field = True
	auto_start = False
	default_stream = "doxy_ai"

	def __init__(self, name):
		super().__init__(name)
		self.is_running = False
		self.keep_alive = True
		self.thread = None

	def default_widget(self):
		layout = QtWidgets.QVBoxLayout()
		layout.setContentsMargins(0, 0, 0, 0)

		self.connect_button = QtWidgets.QPushButton("Connect")
		self.connect_button.clicked.connect(self.connect_button_pressed)
		layout.addWidget(self.connect_button)

		self.disconect_button = QtWidgets.QPushButton("Disconnect")
		self.disconect_button.hide()
		self.disconect_button.clicked.connect(self.disconnect_button_pressed)
		layout.addWidget(self.disconect_button)

		if self.has_target_stream_field:
			self.target_stream = QtWidgets.QLineEdit(self.default_stream)
			layout.addWidget(self.target_stream)

		if self.auto_start:
			self.connect_button_pressed()

		return layout

	def init_widget(self):
		self.widget = QtWidgets.QWidget()
		self.widget.setLayout(self.default_widget())

		proxy = QtWidgets.QGraphicsProxyWidget()
		proxy.setWidget(self.widget)
		proxy.setParentItem(self)

		super().init_widget()

	def get_target_stream(self):
		if self.has_target_stream_field: #TODO: This function needs to be elaborated upon!
			return self.target_stream.text()

		return self.default_stream

	def load(self, data):
		super().load(data)

		if self.has_target_stream_field:
			target_stream = data["target_stream"] if "target_stream" in data else self.default_stream
			self.target_stream.setText(target_stream)

	def save(self):
		data = super().save()

		if self.has_target_stream_field:
			data["target_stream"] = self.target_stream.text()
			return data

	def stop_impl(self):
		self.keep_alive = False
		self.stop()
		self.thread.kill()
		self.thread.join()

	def connect_button_pressed(self):
		self.connect_button.setText("...")
		if self.is_running:
			self.stop_impl()
			self.connect_button.setText("Connect")
			self.disconect_button.hide()
		else:
			self.connect_button.setText("Restart")
			self.disconect_button.show()

		print("A")
		self.keep_alive = True
		thread = KThread(target=lambda: asyncio.run(self.go()))
		thread.start()

	def disconnect_button_pressed(self):
		self.disconect_button.setText("...")
		self.stop_impl()
		self.connect_button.setText("Connect")
		self.disconect_button.setText("Disconnect")
		self.disconect_button.hide()

	async def go(self):
		print("Go button pressed")

	def stop(self):
		print("Stop/restart button pressed")

	def recieve_message(self, message: Message):
		message.originatingPlatform = self
		self.events.on_message(message)
