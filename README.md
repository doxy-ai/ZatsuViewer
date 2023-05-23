# ZatsuDachi

ZatsuDachi is a simple streaming chat viewer with an emphasis on supporting a multitude of streaming platforms at once! It uses a plugin based architecture to easily support additional platforms and ships with a web chat display designed to work with OBS browser sources!

Huge shout out to DreadExcalibur for the name!

## Supported Platforms

Currently I provide first party support for the following platforms
* Twitch: (plugin can be downloaded here: https://gist.github.com/doxy-ai/c6c20f07cad0a11ec4b620003f12537a)
* Vstream: (plugin: https://gist.github.com/doxy-ai/364d9804d97c8d37285e7b8671d274d4)

(Youtube support will be coming soon)
There is also an example of a profanity filter and a pinger which will play a sound notification when you recieve a new message after a break in the plugins/disabled folder, moving them up into the plugins  folder should enable them with no extra configuration necessary!

## Quick Start

1) Download the latest version of Python 3.10 https://www.python.org/downloads/
2) Click the green "Code" button in the top right and select "Download as Zip"
3) Unzip ZatsuDachi somewhere and note where
4) Open a terminal (this can be done by opening the start window on windows and typing cmd)
5) Navigate to where you unzipped ZatsuDachi (cd <the folder from step 3> on windows)
6) Run `pip install colour flask flask_socketio tk` to install ZatsuDachi's dependencies. 
*NOTE: If you are using linux you will need to install libtk using your package manager*
7) (optional) Download one of the platform plugins above and follow the setup steps at the top of the file!
8) Run `python zatsu.py` in the terminal we opened to launch ZatsuDachi
9) (optional) A URL (something along the lines of http://127.0.0.1:8080) should have been printed by step 8. If you paste that URL into a web browser or an OBS browser source to view your chat! 


## Setup

General setup guides can be found here: https://github.com/doxy-ai/ZatsuDachi/wiki

More specific instructions for some particular topics can be found here:
* Coming soon
