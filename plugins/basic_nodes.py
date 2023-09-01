# Import required packages
from zatsu.api import PluginBase, Message, Color
from zatsu.nodes.node_types import *
from zatsu.nodes.pins import *


# Define the plugin class
class Plugin(PluginBase):
	# Set plugin name and target stream
	name = "Default Set of Nodes"
	# Set image URL for the plugin
	# pluginImageURL = "https://brand.twitch.tv/assets/logos/svg/glitch/purple.svg"


	async def go(self):
		# Setup Pin colors
		DataPin.setup_default_colors()
		DataPin.set_type_color(Message, Color("#FBCEB1"))

		nodes = self.find_plugin("Nodes GUI")
		nodes.register_node(self._loaded_module, PrintNode)
		nodes.register_node(self._loaded_module, OnMessageNode)

class PrintNode(Node):
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
		
class OnMessageNode(EventNode):
	def __init__(self):
		super().__init__("On Message")

		self.title_text = "On Message"
		self.type_text = "Events"
		self.set_color(title_color=(128, 0, 0))

		self.message = self.add_pin("Message", Message, EventNode.is_output)

		self.build()

	def on_connected(self, connection):
		try: self.platform_from_connection(connection).events.on_message += self.message_recieved
		except AttributeError: pass # platform_from_connection(connection) may return none if the user clicks on the output pin within 1ms of a previous disconnect!

	def on_disconnected(self, connection):
		self.platform_from_connection(connection).events.on_message -= self.message_recieved

	def message_recieved(self, message):
		self.message.value = message
		self.execute_next()



