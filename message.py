# requirements: pip install colour

# Import necessary modules
import api
from dataclasses import dataclass
from flask import escape
from colour import Color
import datetime

# Define a data class for the message object
@dataclass
class Message:
    # Define default values for message properties
    pluginImageUrl: str = ""
    sendTime: datetime.datetime = datetime.datetime.now()
    sender: str = ""
    senderColor: Color = Color("#808080")
    content: str = ""

    # Define a method to render the message as HTML
    def render_as_html(self):
        # Generate img tag if plugin image url is not empty, otherwise use empty string
        img_tag = f'<img src="{self.pluginImageUrl}">' if len(self.pluginImageUrl) > 0 else ""
        # Format message HTML string using string interpolation
        return f"""
<div class="message-item">
    <div class="chat-messages reversed">
        <div class="message-info-container">
            <div class="message-info">
                {img_tag}
                <span class="message-sender" style="color: {self.senderColor.hex}">{escape(self.sender)}</span>
                <span class="message-time">{self.sendTime}</span>
            </div>
            <div class="message-text"><span class="chat-text-normal">{api._singletonApp.parse_emotes(escape(self.content))}</span></div>
        </div>
    </div>
</div>
"""