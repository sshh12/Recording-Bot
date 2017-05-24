import os
import wave

datapath = 'voicedata'
conversationfn = 'conv.txt'
responce_delay = 2000

class Recording(object):

    def __init__(self, fn):

        self.fn = fn
        
        self.userid, self.timestamp, self.text = self.fn[:-4].split("!")

        self.timestamp = int(self.timestamp)
        self.text = self.text.replace("_", " ")

        with wave.open(os.path.join(datapath, self.fn), 'rb') as wav:
            self.frames = wav.getnframes()
            self.framerate = wav.getframerate()

        self.length = 1000 * wav.getnframes() / wav.getframerate()

        self.stop = self.timestamp
        self.start = self.timestamp - self.length

def main():

    recordings = [Recording(fn) for fn in os.listdir(datapath) if "!" in fn]

    with open(conversationfn, 'w') as conv:

        for a in recordings:

            for b in recordings:

                if a == b or a.userid == b.userid or a.stop <= b.start:
                    continue

                delay = a.stop - b.start

                if delay <= responce_delay:
                    conv.write("#".join([a.text, b.fn]) + "\n")
            

if __name__ == "__main__":
    main()
