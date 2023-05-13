from api import PluginBase, Message, Color
from itertools import chain
import requests, asyncio

class Plugin(PluginBase):
	"""A plugin that adds Better Twitch.tv emotes to messages."""

	name = "Better Twitch.tv Emotes Plugin"
	platform = "twitch"
	# platformID = "818635195" # Can be found from: https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/

	async def go(self):
		"""Registers Better Twitch.tv emotes for the channel."""

		twitch = self.find_plugin("Twitch Chat Plugin")
		while twitch == None:
			await asyncio.sleep(.1) # Need to sleep for a bit to make sure the twitch plugin gets loaded
			twitch = self.find_plugin("Twitch Chat Plugin")

		# Wait for twitch to figure out what the user id is
		while twitch.id == None: await asyncio.sleep(.1)

		globalEmotes = requests.get(f'https://api.betterttv.net/3/cached/emotes/global').json()
		userEmotes = requests.get(f'https://api.betterttv.net/3/cached/users/{self.platform}/{twitch.id}').json()

		for emote in chain(globalEmotes, userEmotes["channelEmotes"], userEmotes["sharedEmotes"]):
			self.register_emote(emote["code"], f"https://cdn.betterttv.net/emote/{emote['id']}/3x.webp")
