#requirements: pip install playsound
import zatsu.api, playsound
from zatsu.api import PluginBase, datetime

class Plugin(PluginBase):
    """
    A plugin that plays an audio alert when a certain time threshold between messages is exceeded.
    """
    name = "Audio Alert Plugin"  # A string representing the name of the plugin
    soundFilePath = "resources/14409__acclivity__chimebar_f.wav"  # A string representing the file path of the audio file to be played
    quietThreshold = 60.  # A float representing the time threshold in seconds for triggering the plugin

    def on_message_recieved(self, appMessages):
        """
        Callback method called when new messages are received by the application.
        
        This method checks the time difference between the most recent message and the previous one. 
        If the time difference is greater than the threshold, an audio alert is played.
        
        Args:
            appMessages (list): A list of messages received by the application.
        """
        if len(appMessages) < 2:
            return

        # Calculate the time difference between the current message and the previous one
        messageDelta = appMessages[-1].sendTime - appMessages[-2].sendTime

        if messageDelta.total_seconds() > self.quietThreshold:
            # Play the audio file
            playsound.playsound(self.soundFilePath, False)

            # Print a message to indicate that the plugin is working (commented out)
            # print("should play a sound")
