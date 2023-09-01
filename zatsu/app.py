"""
This module contains the App class which is responsible for loading and running plugins, receiving messages, registering emotes, and parsing emotes in messages.

Usage: create an instance of the App class and call the go method.

The `loaded_plugins` list holds instances of loaded plugins. `registered_emotes` is a dictionary that maps emote names to their URLs.

Attributes:
maxMessages (int): The maximum number of messages to keep in the queue.
messages (RingBuffer): A RingBuffer object that holds the messages in the queue.

Methods:
go(): Starts the application and loads all the plugins.
recieve_message(message: Message): Receives a Message object and adds it to the message queue. Notifies all of the plugins that a message was received.
register_emote(emote, url): Registers an emote with the application by adding it to the registered_emotes dictionary.
parse_emotes(message): Replaces emote names in a message with their corresponding URLs.
load_plugins(): Loads all the plugins in the "plugins" folder and calls their setup method.
load_module(path): Loads a module from the given file path.
"""

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "thirdparty")))
import traceback
import asyncio
import threading
import datetime
import time
import shutil
import userpaths
from pathlib import Path
from importlib import util
from ring_buffer import RingBuffer
from zatsu.message import Message
from killableThread import KThread
from tkinter import ttk, Tk, W, E, N
from queue import PriorityQueue

class App:
	"""
	A class representing the main application.
	"""
	loaded_plugins = []  # A list of loaded plugins
	registered_emotes = {}  # A dictionary of registered emotes
	registered_badges = {}  # A dictionary of registered badges

	is_running = True

	maxMessages = 20  # Maximum number of messages to keep in the queue
	messages = RingBuffer(maxMessages)  # A ring buffer of messages

	threads = [] # The threads that should get restarted when configuation changes update
	mainThreadWorkQueue = PriorityQueue()

	def stop(self):
		# Iterate over each thread in the original list
		for thread in self.threads:
			plugin = self.find_plugin(thread.name)
			# Terminate or stop the execution of the thread
			plugin.stop()
			thread.kill()
			thread.join()

		self.threads = []

	def restart(self):
		"""
		Restart the threads associated with the object.
		
		This method clears the existing threads, kills each thread in the original list,
		creates new threads based on the original threads, and starts the newly created threads.
		"""
		# Create a copy of the current list of threads and clear the existing threads
		oldThreads = self.threads
		self.threads = []

		# Iterate over each thread in the original list
		for thread in oldThreads:
			plugin = self.find_plugin(thread.name)
			# Terminate or stop the execution of the thread
			plugin.stop()
			thread.kill()
			thread.join()
			
			# Create a new thread based on the original thread's target function
			# and append it to the list of threads
			print(f"Restarting {plugin.name}")
			plugin._keepAlive = True
			self.threads.append(KThread(target=lambda: asyncio.run(plugin.go()), name=plugin.name))

		# Start all the new threads
		for thread in self.threads:
			thread.start()



	def go(self):
		"""
		Starts the application by loading plugins and running them.
		"""
		# Load all of the plugins in the folder and call setup on them
		self.load_plugins()

		# For each loaded plugin...
		for plugin in self.loaded_plugins:
			self.threads.append(KThread(target=lambda: asyncio.run(plugin.go()), name=plugin.name)) #TODO: is it worth the effort to check if its a coroutine? or just assume everything is?
			self.threads[-1].start()


	def process_main_thread_tasks(self):
		while self.is_running and not self.mainThreadWorkQueue.empty():
			task = self.mainThreadWorkQueue.get()
			task[1]() # Assumes the work provided is a tuple of a priority and the actual task (the format the api gives us!)
			self.mainThreadWorkQueue.task_done()


	def shutdown(self):
		self.is_running = False


	def recieve_message(self, message: Message):
		"""
		Receives a message and adds it to the message queue. Notifies all plugins that a message has been received.

		Args:
			message: A message to be received and added to the message queue.
		"""
		if message.sendTime == 0: message.sendTime = datetime.datetime.now()
		for plugin in self.loaded_plugins:
			if not plugin.should_message_be_sent(message): 
				return

		self.messages.max = self.maxMessages
		self.messages.append(message)

		# Notify all of the plugins that a message was received
		for plugin in self.loaded_plugins:
			plugin.on_message_recieved(self.messages)



	def register_emote(self, emote, url):
		"""
		Registers an emote with the specified URL.

		Args:
			emote: The emote to register.
			url: The URL of the image for the emote.
		"""
		self.registered_emotes[emote] = url

	def register_badge(self, badge, url):
		"""
		Registers a badge with the specified URL.

		Args:
			badge: The badge to register.
			url: The URL of the image for the badge.
		"""
		self.registered_badges[badge] = url

	def parse_emotes(self, message):
		"""
		Parses emotes in a message and replaces them with their HTML equivalent.

		Args:
			message: The message to parse emotes in.

		Returns:
			The message with parsed emotes.
		"""
		message = str(message)
		for replace in self.registered_emotes:
			message = message.replace(replace, f"<img class=\"chat-text-emoji-image\" src=\"{self.registered_emotes[replace]}\" alt=\"{replace}\"\\>")
		return message



	def load_plugins(self):
		"""
		Loads all valid plugins in the plugins folder.
		"""
		# Get current path
		path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
		documents = userpaths.get_my_documents()
		pluginPaths = [
			os.path.join(path, "plugins"),
			os.path.join(documents, "ZatsuDachi", "plugins")
		]

		# Create the plugins folder in documents if it doesn't already exist!
		if not os.path.exists(pluginPaths[1]):
			os.makedirs(pluginPaths[1])
			shutil.copy2(os.path.abspath(os.path.join(path, "..", "downloadPlugin.py")), os.path.join(documents, "ZatsuDachi"))

		for pluginPath in pluginPaths:
			for fname in os.listdir(pluginPath):
				# Load only "real modules"
				if not fname.startswith('.') and not fname.startswith('__') and fname.endswith('.py'):
					try:
						module = self.load_module(os.path.join(pluginPath, fname))
						plugin = module.Plugin()
						plugin._loaded_module = module
						self.loaded_plugins.append(plugin)
					except Exception:
						print(fname + " is not a valid plugin!")
						traceback.print_exc()
		
		# Sort the plugins alphabetically (but with URL Settings always being first!)
		self.loaded_plugins.sort(key=lambda p: p.name if p.name != "URL Settings Display" else "\0URL Settings")

	def load_module(self, path):
		"""
		Utility method to automatically load a module.

		Args:
			path: The path of the module to load.

		Returns:
			The loaded module.
		"""
		name = os.path.split(path)[-1]
		spec = util.spec_from_file_location(name, path)
		module = util.module_from_spec(spec)
		spec.loader.exec_module(module)
		return module

	def find_plugin(self, name):
		for plugin in self.loaded_plugins:
			if plugin.name == name:
				return plugin
		return null
