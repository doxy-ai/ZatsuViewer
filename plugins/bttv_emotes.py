from api import PluginBase, Message, Color
import requests

class Plugin(PluginBase):
	name = "Better Twitch.tv Emotes Plugin"

	platform = "twitch"
	platformID = "818635195" # Can be found from: https://www.streamweasels.com/tools/convert-twitch-username-to-user-id/


	async def go(self):
		globalEmotes = requests.get(f'https://api.betterttv.net/3/cached/emotes/global').json()
		userEmotes = requests.get(f'https://api.betterttv.net/3/cached/users/{self.platform}/{self.platformID}').json()

		for emote in globalEmotes:
			self.register_emote(emote["code"], f"https://cdn.betterttv.net/emote/{emote['id']}/3x.webp")
		for emote in userEmotes["channelEmotes"]:
			self.register_emote(emote["code"], f"https://cdn.betterttv.net/emote/{emote['id']}/3x.webp")
		for emote in userEmotes["sharedEmotes"]:
			self.register_emote(emote["code"], f"https://cdn.betterttv.net/emote/{emote['id']}/3x.webp")