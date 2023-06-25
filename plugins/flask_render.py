from flask import render_template
import api
import webbrowser
import tkinter as tk
from api import PluginBase


messages = None

class Plugin(PluginBase):
	"""A plugin that uses Flask to render HTML templates."""

	name = "Flask Renderer Plugin"
	port = 27315

	async def go(self):
		"""Starts the webserver on another thread."""
		api.socketIO.run(api.flask, host='0.0.0.0', port=self.port, debug=False)

	def on_message_recieved(self, appMessages):
		"""Handles new message events and notifies the page that a new message has arrived.

		Args:
			appMessages (list): A list of message objects.
		"""
		global messages
		messages = appMessages # Should be a reference? So no memory copied?
		api.socketIO.emit("new message", messages[-1].render_as_html()) # Notify the page that a new message has arrived!

	def setupGUI(self, tabParent, applyBtn):
		# Show GUI for changing port
		content = PluginBase.setupGUI(self, tabParent, applyBtn)

		# Provide a link to open chat in the browser
		link = tk.Label(content, text="Open Chat in Browser", fg="blue", cursor="hand2")
		link.grid(row=1, columnspan=2, sticky='nesw')
		link.bind("<Button-1>", lambda e: webbrowser.open_new_tab(f"http://127.0.0.1:{self.port}"))

		# Also provide the link as selectable + copyable text
		ent = tk.Entry(content, state='readonly', fg='black')
		ent.grid(row=2, columnspan=2, sticky='nesw')
		text = tk.StringVar()
		text.set(f"Running on: 127.0.0.1:{self.port}")
		ent.config(textvariable=text, relief='flat')
		
		return content


@api.flask.route("/")
def index():
	"""Renders the index page.

	Returns:
		str: The rendered HTML.
	"""
	return render_template('index.html')

@api.flask.route("/base.css")
def base_css():
	"""Renders the base css.

	Returns:
		str: The rendered css.
	"""
	return render_template('base.css')

@api.flask.route("/horizontal.css")
def horizontal_css():
	"""Renders the horizontal chat css.

	Returns:
		str: The rendered css.
	"""
	return render_template('horizontal.css')

@api.flask.route("/messages")
def messages_endpint():
	"""Returns a list of messages as HTML.

	Returns:
		str: The rendered HTML.
	"""
	if(messages is None):
		return ""

	out = ""
	for message in messages:
		out += message.render_as_html()

	return out