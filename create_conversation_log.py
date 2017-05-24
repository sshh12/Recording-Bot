import os
import wave

datapath = 'voicedata'
conversationfn = 'conv.txt'
response_delay = 2000 # Max time between people to be considered a prompt and response

class Recording(object):

    def __init__(self, fn):
        """
        An object that represents an audio file that passed through the api

        Parameters
        ----------
        fn : str
            Path to the audio file
        """
        self.fn = fn
        
        self.userid, self.timestamp, self.text = self.fn[:-4].split("!")

        self.timestamp = int(self.timestamp)
        self.text = self.text.replace("_", " ")

        with wave.open(os.path.join(datapath, self.fn), 'rb') as wav:
            self.frames = wav.getnframes()
            self.framerate = wav.getframerate()

        self.length = 1000 * wav.getnframes() / wav.getframerate() # Time in millis

        self.stop = self.timestamp # Timestamps are based on end of recording
        self.start = self.timestamp - self.length

def main():

    recordings = [Recording(fn) for fn in os.listdir(datapath) if "!" in fn]

    with open(conversationfn, 'w') as conv:

        for a in recordings:

            for b in recordings:

                if a == b or a.userid == b.userid or a.stop <= b.start:
                    continue

                delay = a.stop - b.start # Time between prompt end and responce start

                if delay <= response_delay:
                    conv.write("#".join([a.text, b.fn]) + "\n") # Writes prompt and responce filename for every valid conversation
            

if __name__ == "__main__":
    main()
