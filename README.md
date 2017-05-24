# Recording Bot
A bot built to record and transcribe audio fragments from Discord.

Some functions taken from [podbot](https://github.com/Fiddlekins/podbot).

## Dependencies
+ [NodeJS](https://nodejs.org/)
+ [Python3](https://www.python.org/)
+ [SpeechRecognition](https://pypi.python.org/pypi/SpeechRecognition/)
+ [Discord.js](https://discord.js.org)
+ [node-opus](https://www.npmjs.com/package/node-opus)

## Usage

#### Install
+ Set up the [Cloud Speech Api](https://cloud.google.com/speech/) and download credentials json.
+ Create a [Discord Bot](https://discordapp.com/developers/).
+ ```git clone https://github.com/sshh12/Recording-Bot.git```
+ ```npm install```
+ ```pip install -r requirements.txt```

#### Run
+ In ```main.js```, change ```pythonapp``` to the name of one of the bot_\*.py scripts
+ Change ```token``` to the Discord bot token
+ ```node main.js```

#### Scripts
Depending on what you want to do with the recordings, you can select or write a python
app and point ```main.js``` to it.
+ ```bot_transcribe.py``` transcribes the speech of a user to their text channel.
+ ```bot_repeat.py``` plays back each audio file.
+ ```bot_conversation.py``` records conversations (prompt -> response) then replays response the next time
it hears the same prompt. This requires ```create_conversation_log.py``` to preprocess audio files.
+ ```bot_say.py``` plays lastest audio file with transcription of X when user says "say X".