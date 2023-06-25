import sys
import requests
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
	"twitch": "https://gist.githubusercontent.com/doxy-ai/257878eed21a88aaf6f37d37d5168319/raw/6c7b3bfbcb633292c284ce42f00ee8447ce820ac/twitch_w_bttv.py",
	"youtube": "https://gist.githubusercontent.com/doxy-ai/f567236fd6320e721cbd127b11ca7cb0/raw/c0ff9d4c450ae002bf45b5e1637af0542fd4ee9d/youtube.py",
	"vstream": "https://gist.githubusercontent.com/doxy-ai/364d9804d97c8d37285e7b8671d274d4/raw/3b0871ded0d382b013bd4cb4e348c85405019bb1/vstream.py"
}

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
			install_package("twitchapi")
			print("Please note that you will need to paste your twitch username into the 'targetChannel' field in " + filename)
			input("Press Enter to confirm and continue...")
		case "youtube":
			install_package("git+https://github.com/KaitoCross/pytchat.git@developing")
		case "vstream":
			install_package("websocket-client")
			install_package("cbor2")

except requests.exceptions.RequestException as e:
	print(f"Error occurred while downloading the file: {e}")
except e:
	print(f"Error occurred while installing dependencies: {e}")