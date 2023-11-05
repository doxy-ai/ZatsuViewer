![ZatsuDachi Logo](https://github.com/doxy-ai/ZatsuDachi/blob/master/resources/icon.png)

# ZatsuDachi

ZatsuDachi is a simple streaming chat viewer with an emphasis on supporting a multitude of streaming platforms at once! It uses a plugin based architecture to easily support additional platforms and ships with a web chat display designed to work with OBS browser sources! Additionally it is one of the few programs I am aware of capable of display a horizontal chat (just make the OBS source's height less than 200 pixels!)

Example from: https://vstream.com/c/@doxy_ai
![ZatsuDachi Providing a Horizontal Chat](https://github.com/doxy-ai/ZatsuDachi/blob/master/resources/zatsuExampleDoxy.png)
Example from: https://vstream.com/c/@zovastria
![ZatsuDachi Providing a Normal Vertical Chat](https://github.com/doxy-ai/ZatsuDachi/blob/master/resources/zatsuExampleZova.png)

Huge shout out to DreadExcalibur for the name!

## Supported Platforms

Currently I provide first party support for the following platforms
* Twitch: (plugin can be downloaded here: https://gist.github.com/doxy-ai/8fae7aeb8890f5bed3e2fa7843af9084)
* Youtube: (plugin: https://gist.github.com/doxy-ai/f567236fd6320e721cbd127b11ca7cb0)
* Vstream: (plugin: https://gist.github.com/doxy-ai/364d9804d97c8d37285e7b8671d274d4)
* Kick: (plugin: https://gist.github.com/doxy-ai/f605f31922051151dc044494d1d9af56)

There is also an example of a profanity filter and a pinger which will play a sound notification when you recieve a new message after a break in the `plugins/disabled` folder, moving them up into the `plugins` folder should enable them with no extra configuration necessary!

If you have made a plugin for another platform (or a better version of one of these platforms) feel free to open a pull request!

## Quick Start (Windows Only)

1) Download the latest version of Python 3.12 https://www.python.org/downloads/ (When installing it make sure to check the checkbox on the first page to add python to the path)
2) Download an installer from the latest release: https://github.com/doxy-ai/ZatsuDachi/releases
3) Run the installer selecting the platform plugins you would like to download
4) Sit back and relax as everything is done for you!
5) Run ZatsuDachi from the windows start menu (a terminal window and a GUI should appear)
6) (optional) A URL (something along the lines of http://127.0.0.1:8080) should have been printed in the terminal window shown by step 4. You can paste that URL into a web browser or an OBS browser source to view your chat!

## Quick Start (Other Platforms [Windows too if you're feeling advanced])

1) Download the latest version of Python 3.12 https://www.python.org/downloads/ (When installing it make sure to check the checkbox on the first page to add python to the path)
2) Click the green "Code" button in the top right and select "Download as Zip"
3) Unzip ZatsuDachi somewhere and note where
4) Open a terminal (this can be done by opening the start window on windows and typing cmd)
5) Navigate to where you unzipped ZatsuDachi (cd <the folder from step 3>)
6) Run `pip install colour flask flask_socketio packaging customtkinter requests requests-html userpaths` to install ZatsuDachi's dependencies.
*NOTE: If you are using linux you will need to install libtk using your package manager*
7) (optional) Run `python downloadPlugin.py` to download one of the platform plugins above (this will automatically install its dependencies!)
8) Run `python zatsu.py` in the terminal we opened to launch ZatsuDachi
9) (optional) A URL (something along the lines of http://127.0.0.1:8080) should have been printed by step 8. You can paste that URL into a web browser or an OBS browser source to view your chat!

## Frequently Asked Questions

Q) The app launches but disappears immediately!

A) This usually means that when you installed python you forgot to check the box on the first page to add it to the path... go ahead and try to install it again making sure to check that box!
![Example of where the Python Path box is.](https://github.com/doxy-ai/ZatsuDachi/blob/master/resources/pythonInstall.png)

Q) How do I combine multiple streams from the same platform.

A) One each plugin only supports a single stream... that means you would need to go into the plugin folder and duplicate the appropriate plugin for each additional stream you want to view.

## Setup

General setup guides can be found above!

If you need additional asstance the current best place to get it would be in the discord server: https://discord.gg/XWdrwyRgNQ Feel free to drop a message asking for help!

More specific instructions for some particular topics can be found here:
* Coming soon
