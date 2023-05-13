# Requirements: pip install twitchapi

# Import required packages
from plugins.credentials.twitch import clientID, clientSecret
from api import PluginBase, Message, Color
from twitchAPI.twitch import Twitch
from twitchAPI.helper import first
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
import asyncio

class Plugin(PluginBase):
	"""
	A plugin that connects to the Twitch API and listens to chat messages in a specified Twitch channel.
	"""
	instance = None

	# Set plugin name and target channel
	name = "Twitch Chat Plugin"
	targetChannel = "paradoxshorizon"
	id = None

	# Set image URL for the plugin
	pluginImageURL = "https://brand.twitch.tv/assets/logos/svg/glitch/purple.svg"

	async def go(self):
		"""
		Asynchronous method that runs the plugin and connects to the Twitch chat.
		"""
		instance = self

		# Define user authentication scope and authenticate the user
		USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]
		twitch = await Twitch(clientID, clientSecret)
		# Find the user's ID
		user = await first(twitch.get_users(logins=self.targetChannel))
		self.id = user.id

		# Authenticate for chat
		auth = UserAuthenticator(twitch, USER_SCOPE)
		token, refresh_token = await auth.authenticate()
		await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

		# Connect to the chat and register events
		chat = await Chat(twitch)
		chat.register_event(ChatEvent.READY, self.on_ready)
		chat.register_event(ChatEvent.MESSAGE, self.on_message)
		chat.start()

		self.register_badge_if_not_registered("broadcaster", "https://static-cdn.jtvnw.net/badges/v1/5527c58c-fb7d-422d-b71b-f309dcb85cc1/3")
		self.register_badge_if_not_registered("moderator", "https://static-cdn.jtvnw.net/badges/v1/3267646d-33f0-4b17-b3df-f923a41db1d0/3")
		self.register_badge_if_not_registered("vip", "https://static-cdn.jtvnw.net/badges/v1/b817aba4-fad8-49e2-b88a-7cc744dfa6ec/3")
		self.register_badge_if_not_registered("founder", "https://static-cdn.jtvnw.net/badges/v1/511b78a9-ab37-472f-9569-457753bbe7d3/3")

		# Every 30 minutes make sure that the access token is refreshed
		while True:
			await asyncio.sleep(1800)
			# await asyncio.sleep(15)
			await twitch.refresh_used_token()
			print("Twitch access token refreshed")


	async def on_ready(self, ready_event: EventData):
		"""
		Asynchronous method that is called when the bot is ready to join a channel.
		"""
		print('Bot is ready for work, joining twitch channel')
		await ready_event.chat.join_room(self.targetChannel)

	async def on_message(self, msg: ChatMessage):
		"""
		Asynchronous method that is called when a chat message is received in the target channel.
		"""
		print(msg.text)

		# Register all of the emotes in the message with the emote replacer
		if msg.emotes is not None:
			for id in msg.emotes:
				start = int(msg.emotes[id][0]["start_position"])
				end = int(msg.emotes[id][0]["end_position"]) + 1
				emote = msg.text[start:end]
				url = f"https://static-cdn.jtvnw.net/emoticons/v2/{id}/default/dark/1.0"
				self.register_emote(emote, url)

		# print(msg.emotes)
		# print(list(msg.user.badges.keys()))

		# Notify the app of the new message!
		badges = list(msg.user.badges.keys()) if msg.user.badges is not None else []
		self.recieve_message(Message(content=msg.text, sender=msg.user.display_name, senderColor=Color(msg.user.color), senderBadges=badges, pluginImageUrl=self.pluginImageURL))
