# requirements: pip install colour
import api
from dataclasses import dataclass, field
from flask import escape
from colour import Color
import datetime

@dataclass
class Message:
	"""A class representing a chat message"""

	pluginImageUrl: str = ""
	"""str: URL for plugin image (the icon that is displayed in front of the user's name/badges)"""

	sendTime: datetime.datetime = 0
	"""datetime.datetime: time message was sent"""

	sender: str = ""
	"""str: sender of the message"""

	senderColor: Color = Color("#808080")
	"""Color: color of the sender's name in the message"""

	content: str = ""
	"""str: message content"""

	senderBadges : list[str] = field(default_factory=list)
	"""[str]: Badges that should be displayed next to the user's name"""

	def render_as_html(self) -> str:
		"""Render message as HTML

		Returns:
			str: HTML representation of the message
		"""
		badgeHTML = ""
		print(self.senderBadges)
		for badge in self.senderBadges:
			if badge in api._singletonApp.registered_badges:
				badgeHTML += f'<img class="icon-platform message-badge-image" src="{api._singletonApp.registered_badges[badge]}">\n'
		img_tag = f'<img class="icon-platform message-plugin-image" src="{self.pluginImageUrl}">' if len(self.pluginImageUrl) > 0 else ""
		color = self.senderColor if self.senderColor != Color("black") else Color("white")
		return f"""
<div class="message-item">
    <div class="chat-messages reversed">
        <div class="message-info-container">
            <div class="message-info">
                {img_tag}
				{badgeHTML}
                <span class="message-sender" style="color: {color.hex}">{escape(self.sender)}</span>
                <span class="message-time">{self.sendTime}</span>
            </div>
            <div class="message-text"><span class="chat-text-normal">{api._singletonApp.parse_emotes(escape(self.content))}</span></div>
        </div>
    </div>
</div>
"""