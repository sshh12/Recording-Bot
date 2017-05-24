from recordingbot import Bot

class RepeatBot(Bot):

    def process(self, text, memberid, timestamp, wavefn):

        self.play(wavefn)

if __name__ == "__main__":

    bot = RepeatBot('voicedata', 'voiceapi.json')
    bot.run()
