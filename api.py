# Import necessary modules
from flask import Flask
from flask_socketio import SocketIO
from app import App
from message import Message
from colour import Color
from datetime import datetime

# Initialize Flask and SocketIO instances
flask = Flask(__name__)
socketIO = SocketIO(flask)

# Create an instance of the App class
_singletonApp = App()

# Define a PluginBase class
class PluginBase:
	# Set a default name for the plugin
	name = "base"

	# Define a method that doesn't do anything
	async def go(self):
		pass

	# Define a method that will be called whenever the application receives a new message
	def on_message_recieved(self, messages):
		pass

	# Define a method that can be called to signal to the application that a new message has been received
	def recieve_message(self, message):
		_singletonApp.recieve_message(message)

	# Define a method that can be called to register an emote with the application
	def register_emote(self, emote, url):
		_singletonApp.register_emote(emote, url)