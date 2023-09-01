import sys, os
from colour import Color
from PySide6 import QtCore, QtGui

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "thirdparty", "python-node-editor")))
from node_editor import pin

def color2QT(c: Color):
	return QtGui.QColor(c.red * 255, c.green * 255, c.blue * 255)

def getConnectionInput(connection):
	for pin in connection.pins():
		if not pin.is_output:
			return pin

def getConnectionOutput(connection):
	for pin in connection.pins():
		if pin.is_output:
			return pin


class DataPin(pin.Pin):
	defaultColor = Color("cyan")

	typeColors = {}
	def set_type_color(t: type, c: Color):
		DataPin.typeColors[t.__name__] = c

	def setup_default_colors():
		DataPin.set_type_color(bool, Color("#FF9B9B"))
		DataPin.set_type_color(str, Color("#FFFEC4"))
		DataPin.set_type_color(int, Color("#AEFF79"))
		DataPin.set_type_color(float, Color("#AEFF79"))

	def __init__(self, parent, scene):
		super().__init__(parent, scene)
		self.color = DataPin.defaultColor
		self.type = None
		self.value = None

	def can_connect_to(self, pin):
		# Can only connect to pins of the same type (takes untyped pins into account!)
		if self.type is not None and pin.type is not None:
			return self.type == pin.type

		return super().can_connect_to(pin)

	def set_color(self, color: Color):
		self.color = color

	def set_is_array(self, isArrayPin: bool):
		if isArrayPin:
			path = QtGui.QPainterPath()
			for x in range(0, 3): #0, 1, 2
				for y in range(0, 3): #0, 1, 2
					path.moveTo(0, 0)
					path.addRect(x * 2, y * 2, 1, 1)
			self.setPath(path)

		else:
			path = QtGui.QPainterPath()
			path.addEllipse(-self.radius_, -self.radius_, 2 * self.radius_, 2 * self.radius_)
			self.setPath(path)

	def on_connected(self, connection):
		if self.type is not None:
			connection.color = color2QT(self.color)

	def set_type(self, dtype: type):
		self.type = dtype
		print(dtype.__name__)

		if dtype in [list, dict, tuple]:
			self.set_is_array(True)

		if dtype.__name__ in DataPin.typeColors:
			self.set_color(DataPin.typeColors[dtype.__name__])
		else: self.set_color(DataPin.defaultColor)

	def paint(self, painter, option=None, widget=None):
		if self.is_connected():
			painter.setBrush(color2QT(self.color))
		else: painter.setBrush(QtCore.Qt.NoBrush)

		# Draw icon
		painter.drawPath(self.path())

		# Draw text
		if not self.execution or self.execution_show_text:
			painter.setPen(QtCore.Qt.NoPen)
			painter.setBrush(QtCore.Qt.white)
			painter.drawPath(self.text_path)

	def get_index_in_node(self) -> int | None:
		for index, pin in enumerate(self.node.__pins):
			if pin == self:
				return index
		return None



	def get_value(self):
		# If there is a value cached in the pin... just return that
		if self.value is not None:
			return self.value

		# If we are an input node... get the value associated with out output node
		if not self.is_output:
			for connection in self.connections:
				return connection.other_pin(self).get_value()
		
		# Otherwise request a value from the parent
		return self.node.get_value(self)

class PlatformPin(DataPin):
	def __init__(self, parent, scene):
		super().__init__(parent, scene)

		self.set_execution(True)
		self.execution_show_text = True
		self.set_color(Color("yellow"))
		self.type = type(PlatformPin) # Just a dummy type to ensure that platform pins can only connect to eachother!
		path = QtGui.QPainterPath()
		points = []
		points.append(QtCore.QPointF(0, -5))
		points.append(QtCore.QPointF(6, 5))
		points.append(QtCore.QPointF(-6, 5))
		points.append(QtCore.QPointF(0, -5))
		path.addPolygon(QtGui.QPolygonF(points))
		self.setPath(path)

	def on_connected(self, connection):
		connection.color = color2QT(self.color)
		connection.thickness = 3

	def get_platforms(self):
		return [con.other_pin(self).node for con in self.connections]

class ExecutionPin(pin.Pin):
	def __init__(self, parent, scene):
		super().__init__(parent, scene)
		self.set_execution(True)

	def paint(self, painter, option=None, widget=None):
		super().paint(painter, option, widget)

		# Draw text
		if self.is_output and len(tuple(self.node.output_data_pins())):
			painter.setPen(QtCore.Qt.NoPen)
			painter.setBrush(QtCore.Qt.white)
			painter.drawPath(self.text_path)

	def can_connect_to(self, pin):
		if not isinstance(pin, ExecutionPin):
			return False

		# Execution pins can only connect to execution pins!
		if pin.execution != self.execution:
			return False
		
		return super().can_connect_to(pin)

	def execute_next(self):
		for connection in self.connections:
			connection.other_pin(self).node.execute()


