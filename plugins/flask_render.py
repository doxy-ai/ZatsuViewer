from flask import render_template
import api
from api import PluginBase


messages = None

class Plugin(PluginBase):
	"""A plugin that uses Flask to render HTML templates."""

	name = "Flask Renderer Plugin"

	async def go(self):
		"""Starts the webserver on another thread."""
		api.socketIO.run(api.flask, host='0.0.0.0', port=8080, debug=False)

	def on_message_recieved(self, appMessages):
		"""Handles new message events and notifies the page that a new message has arrived.

		Args:
			appMessages (list): A list of message objects.
		"""
		global messages
		messages = appMessages # Should be a reference? So no memory copied?
		api.socketIO.emit("new message", messages[-1].render_as_html()) # Notify the page that a new message has arrived!


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