import webbrowser
import tkinter as tk
import threading
import time
from tkinter import ttk
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

	def setupGUI(self, tabParent, applyBtn):
		content = ttk.Frame(tabParent)
		content.grid()

		def ThreadFunc():
			while self._flask == None:
				time.sleep(.1)

			# Provide a link to open chat in the browser
			link = tk.Label(content, text="Open Chat in Browser", fg="blue", cursor="hand2")
			link.grid(row=1, columnspan=2, sticky='nesw')
			link.bind("<Button-1>", lambda e: webbrowser.open_new_tab(f"http://127.0.0.1:{self._flask.port}"))

			# Also provide the link as selectable + copyable text
			ent = tk.Entry(content, state='readonly', fg='black')
			ent.grid(row=2, columnspan=2, sticky='nesw')
			text = tk.StringVar()
			text.set(f"Running on: 127.0.0.1:{self._flask.port}")
			ent.config(textvariable=text, relief='flat')

		threading.Thread(target=ThreadFunc).start()
		
		return content

