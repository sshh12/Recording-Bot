from recordingbot import Bot

class TranscribeBot(Bot):

    def process(self, text, memberid, timestamp, wavefn):

        self.message(text)

if __name__ == "__main__":

    bot = TranscribeBot('voicedata', 'voiceapi.json')
    bot.run()
