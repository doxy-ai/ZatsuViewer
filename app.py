import os, traceback, asyncio, threading
from pathlib import Path
from importlib import util
from ring_buffer import RingBuffer
from message import Message


class App:
	loaded_plugins = []
	registered_emotes = {}

	maxMessages = 20 # Number of messages to keep in the queue
	messages = RingBuffer(maxMessages)


	def go(self):
		print("starting inside app")

		# Load all of the plugins in the folder and call setup on them
		self.load_plugins()
		for plugin in self.loaded_plugins:
			threading.Thread(target=lambda: asyncio.run(plugin.go())).start() #TODO: is it worth the effort to check if its a coroutine? or just assume everything is?
			# plugin.test()

		print("finished starting app")


	def recieve_message(self, message: Message):
		self.messages.max = self.maxMessages
		self.messages.append(message)

		# Notify all of the plugins that a message was recieved
		for plugin in self.loaded_plugins:
			plugin.on_message_recieved(self.messages)

	def register_emote(self, emote, url):
		self.registered_emotes[emote] = url

	def parse_emotes(self, message):
		message = str(message)
		for replace in self.registered_emotes:
			message = message.replace(replace, f"<img class=\"chat-text-emoji-image\" src=\"{self.registered_emotes[replace]}\" alt=\"{replace}\"\\>")
		return message

	def load_plugins(self):
		# Get current path
		path = os.path.abspath(__file__)
		pluginPath = os.path.dirname(path) + "/plugins"

		for fname in os.listdir(pluginPath):
			# Load only "real modules"
			if not fname.startswith('.') and not fname.startswith('__') and fname.endswith('.py'):
				try:
					self.loaded_plugins.append(self.load_module(os.path.join(pluginPath, fname)).Plugin())
				except Exception:
					print(fname + " is not a valid plugin!")
					traceback.print_exc()

	# Small utility to automatically load modules
	def load_module(self, path):
		name = os.path.split(path)[-1]
		spec = util.spec_from_file_location(name, path)
		module = util.module_from_spec(spec)
		spec.loader.exec_module(module)
		return module







