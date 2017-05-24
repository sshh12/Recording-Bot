# Recording Bot
A bot built to record and transcribe audio fragments from Discord.

Some js code taken from [podbot](https://github.com/Fiddlekins/podbot).

## Dependencies
+ [NodeJS](https://nodejs.org/)
+ [Python3](https://www.python.org/)
+ [SpeechRecognition](https://pypi.python.org/pypi/SpeechRecognition/)
+ [Discord.js](https://discord.js.org)
+ [node-opus](https://www.npmjs.com/package/node-opus)

## Usage
#### Installing
+ Clone repo.
+ ```npm install```
+ ```pip install -r requirements.txt```
#### Run
+ In ```main.js```, change ```pythonapp``` to the name of one of the bot_\*.py scripts
+ Change ```token``` to the Discord bot token
+ ```node main.js```