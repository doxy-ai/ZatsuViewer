from api import PluginBase, Message
import asyncio

class Plugin(PluginBase):
	name = "Test Plugin"

	async def go(self):
		self.recieve_message(Message(sender = "Dread", content = "Something about Noy-chan"))
		await asyncio.sleep(2)

		for _ in range(19):
			self.recieve_message(Message(sender = "Zlehn", content = "But am not hooman. Am totodile!"))
			await asyncio.sleep(2)

		self.recieve_message(Message(sender = "Dread", content = "Something about Noy-chan"))
		await asyncio.sleep(2)


