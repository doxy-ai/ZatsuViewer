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

import os
import traceback
import asyncio
import threading
import datetime
import time
from pathlib import Path
from importlib import util
from ring_buffer import RingBuffer
from message import Message
from tkinter import ttk, Tk, W, E
from killableThread import KThread

class App:
	"""
	A class representing the main application.
	"""
	loaded_plugins = []  # A list of loaded plugins
	registered_emotes = {}  # A dictionary of registered emotes
	registered_badges = {}  # A dictionary of registered badges

	maxMessages = 20  # Maximum number of messages to keep in the queue
	messages = RingBuffer(maxMessages)  # A ring buffer of messages

	threads = [] # The threads that should get restarted when configuation changes update

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
			# Terminate or stop the execution of the thread
			thread.kill()

		# for thread in oldThreads:
		# 	while thread.is_alive():
		# 		time.sleep(100)

			# Create a new thread based on the original thread's target function
			# and append it to the list of threads
			self.threads.append(KThread(target=thread.target))
			self.threads[-1].start()


	def go(self):
		"""
		Starts the application by loading plugins and running them.
		"""
		# Load all of the plugins in the folder and call setup on them
		self.load_plugins()

		# Create a tab holder
		root = Tk()
		root.title("ZatsuDachi Configuration")
		frm = ttk.Frame(root)
		frm.grid()
		tab_parent = ttk.Notebook(frm)
		tab_parent.grid(row=0, sticky=W+E)

		# Now add a button that restarts some threads with the given changes
		applyBtn = ttk.Button(frm, text='Apply Changes', command=lambda: self.restart())
		applyBtn.grid(row=1)

		# For each loaded plugin...
		for plugin in self.loaded_plugins:
			# Attempt to setup its gui
			gui = plugin.setupGUI(tab_parent, applyBtn)
			# If there is a gui... start its thread in a way that can be restarted
			if gui != None: 
				tab_parent.add(gui, text=plugin.name) # Add the plugin as a tab!

				self.threads.append(KThread(target=lambda: asyncio.run(plugin.go()))) #TODO: is it worth the effort to check if its a coroutine? or just assume everything is?
				self.threads[-1].start()

			# Otherwise start its thread and forget about it!
			else: threading.Thread(target=lambda: asyncio.run(plugin.go())).start()
			
		# Show the GUI
		frm.pack(expand=1, fill='both')
		root.mainloop()



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
