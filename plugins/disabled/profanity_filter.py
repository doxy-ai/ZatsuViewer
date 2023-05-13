#requirements: pip install better_profanity
import api
from api import PluginBase
from better_profanity import profanity

class Plugin(PluginBase):
	name = "Profanity Filter Plugin"  
	censor_char='#'

	def should_message_be_sent(self, message):
		message.content = profanity.censor(message.content, censor_char='#')
		if "#" in message.content: return False
		return True # The message should always be sent
		
