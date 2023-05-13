# Requirements: pip install twitchapi

from plugins.credentials.twitch import clientID, clientSecret
from api import PluginBase, Message, Color
from twitchAPI.twitch import Twitch
from twitchAPI.oauth import UserAuthenticator
from twitchAPI.types import AuthScope, ChatEvent
from twitchAPI.chat import Chat, EventData, ChatMessage, ChatSub, ChatCommand
import asyncio


class Plugin(PluginBase):
	name = "Test Plugin"
	targetChannel = "paradoxshorizon"

	pluginImageURL = "https://brand.twitch.tv/assets/logos/svg/glitch/purple.svg"

	async def go(self):
		USER_SCOPE = [AuthScope.CHAT_READ, AuthScope.CHAT_EDIT]

		twitch = await Twitch(clientID, clientSecret)
		auth = UserAuthenticator(twitch, USER_SCOPE)
		token, refresh_token = await auth.authenticate()
		await twitch.set_user_authentication(token, USER_SCOPE, refresh_token)

		# twitch.

		chat = await Chat(twitch)
		chat.register_event(ChatEvent.READY, self.on_ready)
		chat.register_event(ChatEvent.MESSAGE, self.on_message)
		chat.start()

	async def on_ready(self, ready_event: EventData):
		print('Bot is ready for work, joining channels')
		await ready_event.chat.join_room(self.targetChannel)

	async def on_message(self, msg: ChatMessage):
		# Register all of the emotes in the message with the emote replacer
		if msg.emotes is not None:
			for id in msg.emotes:
				start = int(msg.emotes[id][0]["start_position"])
				end = int(msg.emotes[id][0]["end_position"]) + 1
				emote = msg.text[start:end]
				url = f"https://static-cdn.jtvnw.net/emoticons/v2/{id}/default/dark/1.0"
				self.register_emote(emote, url)
		# print(msg.emotes)
		# print(msg.user.badges)
		self.recieve_message(Message(content=msg.text, sender=msg.user.display_name, senderColor=Color(msg.user.color), pluginImageUrl=self.pluginImageURL))
