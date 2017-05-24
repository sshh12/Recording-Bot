from recordingbot import Bot

class SayBot(Bot):

    def process(self, text, memberid, timestamp, wavefn):

        newfn = "{}!{}!{}".format(memberid, timestamp, text.replace(" ", "_") + ".wav")
        
        os.rename(wavefn, os.path.join(self.datapath, newfn))

        if text.startswith("say"):

            for fn in os.listdir('voicedata'):

                if "!" in fn:

                    file_text = fn.split("!")[-1][:-4].replace("_", " ")
                    
                    if file_text in text:

                        self.play(fn)

if __name__ == "__main__":

    bot = SayBot('voicedata', 'voiceapi.json')
    bot.run()
