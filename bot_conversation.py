from recordingbot import Bot
import os


conversationfn = 'conv.txt' # create this file on first run
converations = {}


with open(conversationfn, 'r') as conv: # run create_conversation_log.py to generate this

    for line in conv.read().split("\n"):

        if "#" in line:
            
            text, fn = line.split("#")
            converations.update({text : fn})
            

class ConversationBot(Bot):

    def process(self, text, memberid, timestamp, wavefn):

        newfn = "{}!{}!{}".format(memberid, timestamp, text.replace(" ", "_") + ".wav")
        
        os.rename(wavefn, os.path.join(self.datapath, newfn))

        if text in converations:
            self.play(converations[text])

if __name__ == "__main__":

    bot = ConversationBot('voicedata', 'voiceapi.json')
    bot.run()
