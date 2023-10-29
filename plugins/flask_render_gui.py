import webbrowser
import tkinter as tk
import threading
import time
import customtkinter as ctk
from api import PluginBase


messages = None

class Plugin(PluginBase):
	"""A plugin that shows a gui allowing users to use zatsudachi entirely from the GUI
		This was added as a seperate plugin since adding the GUI thread into the flask plugin seams to influence its ability to reload
	"""

	name = "URL Settings Display"
	_flask = None

	async def go(self):
		self._flask = self.find_plugin("Flask Renderer Plugin")
		while self._flask == None:
			await asyncio.sleep(.1) # Need to sleep for a bit to make sure the flask plugin gets loaded
			self._flask = self.find_plugin("Flask Renderer Plugin")

	def setupGUI(self, content, applyBtn):
		content.grid_columnconfigure(0, weight=1)

		def ThreadFunc():
			while self._flask == None:
				time.sleep(.1)

			# Provide a link to open chat in the browser
			link = ctk.CTkButton(content, text="Open Chat in Browser", cursor="hand2")
			link.grid(row=1, sticky='nesw')
			link.bind("<Button-1>", lambda e: webbrowser.open_new_tab(f"http://127.0.0.1:{self._flask.port}"))

			# Also provide the link as selectable + copyable text
			text = ctk.StringVar()
			text.set(f"Running on: 127.0.0.1:{self._flask.port}")
			ent = ctk.CTkEntry(content, textvariable=text, state='readonly')
			ent.grid(row=2, pady=6, sticky='nesw')

		threading.Thread(target=ThreadFunc).start()
		
		return content

