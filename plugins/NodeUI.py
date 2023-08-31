# Import required packages
from api import PluginBase, Message, Color

from pathlib import Path
import importlib
import inspect
import sys
import os
import time

from PySide6 import QtCore, QtGui, QtWidgets

sys.path.append(os.path.join(os.getcwd(), "thirdparty/python-node-editor"))

from node_editor.gui.node_list import NodeList
from node_editor.gui.node_widget import NodeWidget

# logging.basicConfig(level=logging.DEBUG)

# Define the plugin class
class Plugin(PluginBase):
	# Set plugin name and target stream
	name = "Nodes GUI"
	# Set image URL for the plugin
	# pluginImageURL = "https://brand.twitch.tv/assets/logos/svg/glitch/purple.svg"

	_icon = os.path.join("resources", "icon.ico")
	_windowTitle = "ZatsuDachi"

	# The app
	app = None
	# The launcher
	editor = None
	
	async def go(self):	
		time.sleep(1) # Wait a second to allow other apps to queue main thread work before blocking it!

		def main_thread_execution_loop():
			self.app = QtWidgets.QApplication(sys.argv)
			self.app.setWindowIcon(QtGui.QIcon(Plugin._icon))
			self.editor = NodeEditor()
			print("Starting Node GUI on the main thread, it will now block")
			self.editor.show()
			self.app.exec()
			self.shutdown_application()
		self.add_main_thread_task(main_thread_execution_loop, sys.maxsize)
		

	# def stop(self):
	# 	print("Goodbye World")

class NodeEditor(QtWidgets.QMainWindow):
	OnProjectPathUpdate = QtCore.Signal(Path)

	def __init__(self, parent=None):
		super().__init__(parent)
		self.settings = None
		self.project_path = None
		self.imports = None  # we will store the project import node types here for now.

		icon = QtGui.QIcon(Plugin._icon)
		self.setWindowIcon(icon)

		self.setWindowTitle(Plugin._windowTitle)
		settings = QtCore.QSettings("node-editor", "NodeEditor")

		# create a "File" menu and add an "Export CSV" action to it
		file_menu = QtWidgets.QMenu("File", self)
		self.menuBar().addMenu(file_menu)

		# TODO: Should I be conserned by how long a load is now taking!!??!?
		load_action = QtGui.QAction("Load Project", self)
		load_action.triggered.connect(self.get_project_path)
		file_menu.addAction(load_action)

		save_action = QtGui.QAction("Save Project", self)
		save_action.triggered.connect(self.save_project)
		file_menu.addAction(save_action)

		# Layouts
		main_widget = QtWidgets.QWidget()
		self.setCentralWidget(main_widget)
		main_layout = QtWidgets.QHBoxLayout()
		main_widget.setLayout(main_layout)
		left_layout = QtWidgets.QVBoxLayout()
		left_layout.setContentsMargins(0, 0, 0, 0)

		# Widgets
		self.node_list = NodeList(self) # TODO: Make the node list appear when you right click
		left_widget = QtWidgets.QWidget()
		self.splitter = QtWidgets.QSplitter()
		self.node_widget = NodeWidget(self)

		# Add Widgets to layouts
		self.splitter.addWidget(left_widget)
		self.splitter.addWidget(self.node_widget)
		left_widget.setLayout(left_layout)
		left_layout.addWidget(self.node_list)
		main_layout.addWidget(self.splitter)

		# Load the example project
		example_project_path = (Path(__file__).parent.resolve() / 'Example_project')
		self.load_project(example_project_path)

		# Restore GUI from last state
		if settings.contains("geometry"):
			self.restoreGeometry(settings.value("geometry"))

			s = settings.value("splitterSize")
			self.splitter.restoreState(s)

	def save_project(self):
		file_dialog = QtWidgets.QFileDialog()
		file_dialog.setAcceptMode(QtWidgets.QFileDialog.AcceptSave)
		file_dialog.setDefaultSuffix("json")
		file_dialog.setNameFilter("JSON files (*.json)")
		file_path, _ = file_dialog.getSaveFileName()
		self.node_widget.save_project(file_path)

	def load_project(self, project_path=None):
		if not project_path:
			return

		project_path = Path(project_path)
		if project_path.exists() and project_path.is_dir():
			self.project_path = project_path

			self.imports = {}

			for file in project_path.glob("*.py"):

				if not file.stem.endswith('_node'):
					print('file:', file.stem)
					continue
				spec = importlib.util.spec_from_file_location(file.stem, file)
				module = importlib.util.module_from_spec(spec)
				spec.loader.exec_module(module)

				for name, obj in inspect.getmembers(module):
					if not name.endswith('_Node'):
						continue
					if inspect.isclass(obj):
						self.imports[obj.__name__] = {"class": obj, "module": module}
						#break

			self.node_list.update_project(self.imports)

			# work on just the first json file. add the ablitity to work on multiple json files later
			for json_path in project_path.glob("*.json"):
				self.node_widget.load_scene(json_path, self.imports)
				break

	def get_project_path(self):
		project_path = QtWidgets.QFileDialog.getExistingDirectory(None, "Select Project Folder", "")
		if not project_path:
			return

		self.load_project(project_path)

	def closeEvent(self, event):
		"""
		Handles the close event by saving the GUI state and closing the application.

		Args:
			event: Close event.

		Returns:
			None.
		"""

		# debugging lets save the scene:
		# self.node_widget.save_project("C:/Users/Howard/simple-node-editor/Example_Project/test.json")

		self.settings = QtCore.QSettings("node-editor", "NodeEditor")
		self.settings.setValue("geometry", self.saveGeometry())
		self.settings.setValue("splitterSize", self.splitter.saveState())
		QtWidgets.QWidget.closeEvent(self, event)