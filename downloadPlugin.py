#!/usr/bin/env python
import sys
import requests
from requests_html import HTMLSession
import pip

def install_package(package):
	if hasattr(pip, 'main'):
		pip.main(['install', package])
	else:
		pip._internal.main(['install', package])



# Check if the correct number of arguments is provided
if len(sys.argv) != 2:
	print("Usage: python downloadPlugin.py [option]")
	print("Options: twitch, youtube, or vstream")
	sys.exit(1)

# Retrieve the option from the command line argument
option = sys.argv[1]

# Define the file URLs based on the provided option
file_urls = {
	"twitch": "https://gist.github.com/doxy-ai/8fae7aeb8890f5bed3e2fa7843af9084",
	"youtube": "https://gist.github.com/doxy-ai/f567236fd6320e721cbd127b11ca7cb0",
	"vstream": "https://gist.github.com/doxy-ai/364d9804d97c8d37285e7b8671d274d4"
}

# Scrape the latest version of the plugin from the link
session = HTMLSession()
file_urls = {key:list(session.get(url).html.find('.file-actions', first=True).absolute_links)[0] for (key,url) in file_urls.items()}

# Check if the provided option is valid
if option not in file_urls:
	print("Invalid option provided!")
	sys.exit(1)

# Figure out where the file should be downloaded
url = file_urls[option]
filename = "plugins/" + url.split("/")[-1]

try:
	#Download the file
	response = requests.get(url)
	response.raise_for_status()

	#Save the downloaded file
	with open(filename, "wb") as file:
		file.write(response.content)
	print(f"File {filename} downloaded successfully!")

	# Depending on the option, install additional packages and provide instructions
	match option:
		case "twitch":
			install_package("irc")
		case "youtube":
			install_package("git+https://github.com/KaitoCross/pytchat.git@developing")
		case "vstream":
			install_package("websocket-client")
			install_package("cbor2")

except requests.exceptions.RequestException as e:
	print(f"Error occurred while downloading the file: {e}")
except e:
	print(f"Error occurred while installing dependencies: {e}")
