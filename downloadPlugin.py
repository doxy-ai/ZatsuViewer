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
    # "youtube": "http://example.com/file2.txt",
    "vstream": "https://gist.githubusercontent.com/doxy-ai/364d9804d97c8d37285e7b8671d274d4/raw/a578828e9f96996d55cbb21055304d29999dfbf5/vstream.py"
}

# Check if the provided option is valid
if option not in file_urls:
    print("Invalid option provided!") 
    sys.exit(1)

# Download the file
url = file_urls[option]
filename = "plugins/" + url.split("/")[-1]

try:
    response = requests.get(url)
    response.raise_for_status()

    with open(filename, "wb") as file:
        file.write(response.content)

    print(f"File {filename} downloaded successfully!")

    match option:
        case "twitch":
            install_package("twitchapi")
            print("Please note that you will need to paste your twitch username into the 'targetChannel' field in " + filename)
            input("Press Enter to confirm and continue...")
        case "vstream":
            install_package("websocket-client")
            install_package("cbor2")
        case "youtube": pass
        
except requests.exceptions.RequestException as e:
    print(f"Error occurred while downloading the file: {e}")