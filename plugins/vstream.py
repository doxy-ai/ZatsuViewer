# Requirements: pip install websocket-client cbor2

# Import required packages
from api import PluginBase, Message, Color
from flask import escape
import asyncio
import json
import websocket
import base64
import uuid
import requests
import cbor2

# Define the plugin class
class Plugin(PluginBase):
	# Set plugin name and target stream
	name = "Vstream Chat Plugin"
	targetStream = "xQHd970tTKKio8WCaungHQ"

	# Set image URL for the plugin
	pluginImageURL = "https://cdn.discordapp.com/attachments/1105538681567203368/1106682813471793223/Icon_black_transparent.png"


	async def go(self):
		"""
		Perform initial setup and establish a WebSocket connection.

		This method sends an HTTP GET request to a specific URL based on `self.targetStream` to obtain the necessary information for establishing the WebSocket connection.
		It then extracts the required data from the response and generates a `videoID` based on `self.targetStream`.
		Finally, it calls the `setup_websocket` method to establish the WebSocket connection with the obtained information.
		"""
		# Send an HTTP GET request to a specific URL based on self.targetStream
		response = requests.get(f"https://vstream.com/v/{self.targetStream}/chat-popout")
		# Raise an exception if the response status code is not successful (200)
		response.raise_for_status()
		# Extract a string between two other strings within the response using the extract_string_between method
		# and parse it as JSON to obtain a dictionary named data
		data = json.loads(self.extract_string_between(response.text, "window.__remixContext = ", ";</script>"))
		# Retrieve the channelID from the data dictionary
		channelID = data["state"]["loaderData"]["routes/v_.$liveStreamID.chat-popout"]["channelID"]
		# Generate a videoID by decoding self.targetStream using base64 and creating a UUID from it
		videoID = uuid.UUID(bytes=base64.b64decode(self.targetStream+"=="))
		# Call the setup_websocket method with the channelID and videoID parameters to establish a WebSocket connection
		self.setup_websocket(channelID, videoID)


	def extract_string_between(self, source, start, end):
		"""
		Extract a string between two other strings within a given source string.

		Args:
			source_string (str): The source string from which to extract the substring.
			start_string (str): The starting string marking the beginning of the desired substring.
			end_string (str): The ending string marking the end of the desired substring.

		Returns:
			str or None: The extracted substring if found, or None if either the start or end string is not found.
		"""
		start_index = source.find(start)
		# If start_string is not found within source_string, return None
		if start_index == -1:
			return None
		# Search for end_string starting from the index immediately after start_string
		end_index = source.find(end, start_index + len(start))
		# If end_string is not found within source_string after start_string, return None
		if end_index == -1:
			return None
		# Return the substring between start_string and end_string
		return source[start_index + len(start):end_index]


	def setup_websocket(self, channelID, videoID):
		"""
		Initialize a WebSocket connection and set up event handlers for different WebSocket events.

		Args:
			channelID (str): The channel ID used in the WebSocket connection URL.
			videoID (UUID): The video ID used in the WebSocket connection URL.
		"""
		# Create a WebSocketApp object with a specific URL based on channelID and videoID
		ws = websocket.WebSocketApp(f'wss://vstream.com/suika/api/room/{channelID}/{videoID}/websocket')
		# Set up an event handler for when a message is received
		ws.on_message = self.on_message
		# Set up an event handler for when the WebSocket connection is opened
		ws.on_open = lambda ws: print("Vstream connection opened!")
		# Set up an event handler for when an error occurs
		ws.on_error = lambda ws, e: print(e)
		# Set up an event handler for when the WebSocket connection is closed
		ws.on_close = lambda ws, status, msg: self.setup_websocket(channelID, videoID)
		# Run the WebSocket connection indefinitely
		ws.run_forever()	

	def on_message(self, ws, message):
		"""
		Process a received message through the WebSocket.

		This method extracts relevant information from the message, constructs a `Message` object, and passes it to the `recieve_message` method.

		Args:
			ws (WebSocket): The WebSocket instance that received the message.
			message (str): The received message.
		"""
		data = cbor2.loads(message)
		if(data[-4] != "ChatCreatedEvent"): return

		chat = data["chat"]

		# Process each chat message
		try:
			# Extract the color of the message sender
			color = Color(rgb=(chat["chatterColor"][0]/255, chat["chatterColor"][1]/255, chat["chatterColor"][2]/255))
			# print(color)
			print(chat)

			# Initialize the message content
			msg = ""
			# Iterate over the nodes of the chat message
			for node in chat["nodes"]:
				# Check the type of the node
				match(node[-4]):
					case "TextChatNode":
						# If the node is a TextChatNode, append the text to the message content
						msg += node["text"]
					
					case "MentionChatNode":
												# If the node is a MentionChatNode, append the username preceded by "@" to the message content
						msg += "@" + node["username"]

					case "EmojiChatNode":
						# If the node is an EmojiChatNode
						if node["emoji"]["size28Src"] == None:
							# If there is no associated image, append the alt text to the message content
							msg += node["emoji"]["altText"]
						else:
							# If there is an associated image, register the emote and append the action text to the message content
							self.register_emote(node["emoji"]["actionText"], node["emoji"]["size28Src"])
							msg += node["emoji"]["actionText"]

			# Create a Message object with the constructed content, sender information, color, and plugin image URL
			self.recieve_message(Message(content=msg, sender=chat["chatter"][5], senderColor=color, pluginImageUrl=self.pluginImageURL))
			print(msg)
		except Exception as e:
			# pass  # Handle any exceptions that occur during message processing
			raise e