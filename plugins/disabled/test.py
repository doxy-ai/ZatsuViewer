from api import PluginBase, Message  # Importing the PluginBase and Message classes from the api module
import asyncio  # Importing the asyncio module for asynchronous operations

class Plugin(PluginBase):  # Defining a class named Plugin that extends the PluginBase class
	"""
	A test plugin that extends the PluginBase class from the api module.
	"""
	name = "Test Plugin"  # A class attribute that stores the name of the plugin

	async def go(self):
		"""
		A method that sends three messages, one from 'Dread' and two from 'Zlehn', with a 2-second delay between each message.
		"""
		# Sending a message from 'Dread' using the receive_message method from the PluginBase class
		self.recieve_message(Message(sender = "Dread", content = "Something about Noy-chan"))
		await asyncio.sleep(2)  # Suspending the execution of the coroutine for 2 seconds using asyncio.sleep()

		# Sending 19 messages from 'Zlehn' using a for loop and the receive_message method from the PluginBase class
		for _ in range(19):
			self.recieve_message(Message(sender = "Zlehn", content = "But am not hooman. Am totodile!"))
			await asyncio.sleep(2)  # Suspending the execution of the coroutine for 2 seconds using asyncio.sleep()

		# Sending another message from 'Dread' using the receive_message method from the PluginBase class
		self.recieve_message(Message(sender = "Dread", content = "Something about Noy-chan"))
		await asyncio.sleep(2)  # Suspending the execution of the coroutine for 2 seconds using asyncio.sleep()
