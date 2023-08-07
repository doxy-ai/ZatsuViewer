from events import Events
from thirdparty import node
import pins
import sys
import threading

def run_now_or_soon(condition, function, *args, toWait=.001):
	if condition:
		threading.Timer(toWait, function, args).start()
		return

	function(*args)


class NodeBase(node.Node):
	# Constants
	is_output = True



	def __init__(self):
		super().__init__()

	def add_pin(self, name: str, t: type | None = None, is_output=False):
		pin = pins.DataPin(self, self.scene())
		pin.is_output = is_output
		if is_output: pin.max_connections = sys.maxsize # Infinate number of outs
		pin.set_name(name)
		pin.node = self
		if t is not None: pin.set_type(t)
		self._pins.append(pin)
		return pin

	def add_execution_pin(self, name: str, is_output=False):
		pin = pins.ExecutionPin(self, self.scene())
		pin.is_output = is_output
		if not is_output: pin.max_connections = sys.maxsize # Infinate number of ins
		pin.set_name(name)
		pin.node = self
		self._pins.append(pin)
		return pin

	def add_default_execution_pins(self):
		self.add_execution_pin("execution inputs", False)
		self.add_execution_pin("then", True) #TODO: How do we feel about this name?

	def add_platform_pin(self, is_output=False):
		pin = pins.PlatformPin(self, self.scene())
		pin.is_output = is_output
		pin.max_connections = sys.maxsize # Infinate number of ins and outs
		pin.set_name("platform" if is_output else "platforms")
		pin.node = self
		self._pins.append(pin)
		return pin



	def output_execution_pins(self):
		for pin in self.output_pins():
			if pin.execution:
				yield pin

	def output_platform_pins(self):
		for pin in self.output_pins():
			if isinstance(pin, pins.PlatformPin):
				yield pin

	def output_data_pins(self):
		for pin in self.output_pins():
			if not pin.execution and not isinstance(pin, pins.PlatformPin):
				yield pin

	def input_execution_pins(self):
		for pin in self.input_pins():
			if pin.execution:
				yield pin

	def input_platform_pins(self):
		for pin in self.input_pins():
			if isinstance(pin, pins.PlatformPin):
				yield pin

	def input_data_pins(self):
		for pin in self.input_pins():
			if not pin.execution and not isinstance(pin, pins.PlatformPin):
				yield pin


	def get_pin(self, indexOrPin: int | str | pins.DataPin | None = None):
		match indexOrPin:
			case None:
				if len(self.output_data_pins()) > 1:
					raise RuntimeError("When working with a node with more than 1 output, you must specify which output to get a value for")
				indexOrPin = self.output_data_pins()[0]

			case str():
				indexOrPin = super().get_pin(indexOrPin)

			case int():
				indexOrPin = self._pins[indexOrPin]
		return indexOrPin

	def validate_pin(self, indexOrPin: int | str | pins.DataPin | None = None):
		indexOrPin = self.get_pin(indexOrPin)
		
		if indexOrPin is None:
			raise RuntimeError("Could not find the requested pin!")
		if indexOrPin.node != self:
			raise RuntimeError("Can't get values associated with pins belonging to different nodes")
		if not indexOrPin.is_output:
			raise RuntimeError("Can't get values associated with input pins")
		return indexOrPin

	def get_pin_value(self, indexOrPin: int | str | pins.DataPin | None = None):
		return self.get_pin(indexOrPin).get_value()

	def get_value(self, indexOrPin: int | str | pins.DataPin | None = None):
		return self.validate_pin(indexOrPin)

	def execute(self):
		raise RuntimeError("Base nodes can't be directly executed... they need to be wrapped in another kind of node!")


class PureNode(NodeBase):
	def __init__(self):
		super().__init__()

	def execute(self):
		raise RuntimeError("Pure nodes can't be directly executed!")

class Node(NodeBase):
	def __init__(self):
		super().__init__()
		self.add_default_execution_pins()

	def get_value(self, indexOrPin: int | str | pins.DataPin | None = None):
		pin = self.validate_pin(indexOrPin)
		if pin.value is not None:
			return pin.value
		raise RuntimeError("Execution nodes can't calculate pin values on the fly, set the value of `" + pin.name + "` in your execute function!")

	def execute_next(self):
		self.get_pin("then").execute_next()


class PlatformNode(NodeBase):
	def __init__(self, name): # Name is required to be passed by derived nodes
		super().__init__()
		self.title_text = name #TODO: Correct?
		self.add_platform_pin(NodeBase.is_output)
		self.events = Events()

		#TODO: Add buttons to start/restart and stop platform

	def execute(self):
		raise RuntimeError("Event nodes can't be directly executed!")

class EventNode(NodeBase):
	def __init__(self, name): # Name is required to be passed by derived nodes
		super().__init__()
		self.title_text = name #TODO: Correct?
		platform = self.add_platform_pin()
		self.add_execution_pin(name, NodeBase.is_output)

		platform.on_connected = lambda connection: run_now_or_soon(len(connection.pins()) < 2, self.on_connected, connection)
		platform.on_disconnected = lambda connection: self.on_disconnected(connection)

	# Converts a connection into a node... be aware that this may fail
	def platform_from_connection(self, connection):
		pin = pins.getConnectionOutput(connection)
		if pin is None: return None
		return pin.node

	def on_connected(self, platform):
		pass

	def on_disconnected(self, connection):
		pass

	def execute_next(self):
		for pin in self.output_execution_pins():
			pin.execute_next()
			break

	def execute(self, *args, **kwargs):
		# It is up to the specific platform/event pair to exchange information!
		self.execute_next()
