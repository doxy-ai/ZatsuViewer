# Import necessary modules
from flask import Flask
from flask_socketio import SocketIO
from app import App
from message import Message
from colour import Color
from datetime import datetime
from tkinter import ttk, Tk

# Initialize Flask and SocketIO instances
flask = Flask(__name__)
socketIO = SocketIO(flask)

# Create an instance of the App class
_singletonApp = App()

class PluginBase:
	"""
	Base class for creating plugins for the chat application.

	Attributes:
		name (str): The name of the plugin.
	"""

	name = "base"

	async def go(self):
		"""
		A method that will be called whenever the plugin is loaded.
		This method gets called in a seperate thread so it is perfectly fine to start infinate loops here if nessicary!
		"""
		pass

	def on_message_recieved(self, messages):
		"""
		A method that will be called whenever the application receives a new message.

		Args:
			messages (list of Message): A ring buffer of Message objects.
		"""
		pass

	def should_message_be_sent(self, message) -> bool:
		"""
		A method that will be called whenever the application receives a new message, is used to determine if the message should be displayed or not

		Args:
			message: The message being examined
		"""
		return True


	def _updateKey(self, key, entry):
		"""
		Update the value of a class field with the value from the entry.

		Args:
			key (str): The name of the key to update.
			entry: An instance of some class representing the user input entry.
		"""
		newValue = entry.get()
		if getattr(self, key) != newValue:
			print(f"Updating {key}")
			setattr(self, key, newValue)

	def setupGUI(self, tabParent, applyButton):
		"""
		Set up the graphical user interface (GUI) based on the class attributes.

		Args:
			tabParent: An form in a tab field representing the parent container for the GUI elements.

		Returns:
			ttk.Frame: The frame containing the GUI elements.
		"""
		def camel2Title(old):
			"""
			Convert a string from camel case to title case with spaces.

			Args:
				old (str): The string to convert.

			Returns:
				str: The converted string.
			"""
			out = ""
			for i, char in enumerate(old):
				if char.isupper() or char == '_':
					out += ' '
				out += char.upper() if i == 0 else char
			return out

		# Create a frame to hold the GUI elements
		content = ttk.Frame(tabParent)
		content.grid()

		row = 0
		for key in type(self).__dict__.keys():
			if key[0] == "_": continue  # Skip keys starting with underscore
			if key == "name": continue  # Skip the key "name"
			if key == "pluginImageURL": continue  # Skip the key "pluginImageURL"
			if callable(type(self).__dict__[key]): continue  # Skip if the value is a function

			# Create a label with the title-cased key and place it in the grid
			ttk.Label(content, text=camel2Title(key)).grid(row=row, sticky='nesw')

			# Create a text entry and insert the value associated with the field
			entry = ttk.Entry(content)
			entry.insert(10, type(self).__dict__[key])
			entry.grid(row=row, column=1, sticky='nesw')

			# Bind hitting enter or moving your mouse out of the field to update the field with the entry value
			entry.bind("<Return>", lambda _, key=key: self._updateKey(key, entry))
			entry.bind("<Leave>", lambda _, key=key: self._updateKey(key, entry))

			row += 1  # Increment the row counter

		return content


	def recieve_message(self, message):
		"""
		A method that can be called to signal to the application that a new message has been received.

		Args:
			message (Message): A Message object to be received by the application.
		"""
		_singletonApp.recieve_message(message)

	def register_emote(self, emote, url):
		"""
		A method that can be called to register an emote with the application.

		Args:
			emote (str): The name of the emote.
			url (str): The URL where the emote can be found.
		"""
		_singletonApp.register_emote(emote, url)
	
	def register_badge(self, badge, url):
		"""
		A method that can be called to register a badge with the application.

		Args:
			badge (str): The name of the badge.
			url (str): The URL where the badge can be found.
		"""
		_singletonApp.register_badge(badge, url)

	def register_badge_if_not_registered(self, badge, url):
		"""
		A method that can be called to register a badge with the application.
		Only registers the badge if the badge has not previously been registered

		Args:
			badge (str): The name of the badge.
			url (str): The URL where the badge can be found.
		"""
		if badge not in _singletonApp.registered_badges:
			self.register_badge(badge, url)

	def find_plugin(self, name):
		return _singletonApp.find_plugin(name)
