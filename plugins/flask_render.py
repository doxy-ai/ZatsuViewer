from flask import render_template
import api
from api import PluginBase


messages = None

class Plugin(PluginBase):
	name = "Flask Renderer"

	async def go(self):
		# Start the webserver on another thread
		api.socketIO.run(api.flask, host='0.0.0.0', port=8080, debug=False)

	def on_message_recieved(self, appMessages):
		global messages
		messages = appMessages # Should be a reference? So no memory copied?
		api.socketIO.emit("new message", messages[-1].render_as_html()) # Notify the page that a new message has arrived!


@api.flask.route("/")
def index():
	return render_template('index.html')

@api.flask.route("/messages")
def messages_endpint():
	if(messages is None): return ""

	out = ""
	for message in messages:
		out += message.render_as_html()
	return out