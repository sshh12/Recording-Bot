import speech_recognition as sr
import wave
import sys
import os

class Bot(object):

    def __init__(self, datapath, voiceapi_cred_file, frame_threshold=60000, clearfiles=True):
        """
        Initialize a bot.

        Parameters
        ----------
        datapath : str
            Path for voice files
        voiceapi_cred_file : str
            Path for cred json
        frame_threshold : int
            Number a frames and audio file must be to be considered a voice
        clearfiles : bool
            True will clear files after each run
        """
        self.datapath = datapath
        self.clearfiles = clearfiles

        with open(voiceapi_cred_file, 'r') as cred:
            self.API_JSON = cred.read()

        self.frame_threshold = frame_threshold

    def message(self, msg):
        """Sends a message in the Discord text channel."""
        print("msg:" + msg)

    def play(self, fn):
        """Plays an audio file into the Discord voice channel."""
        print("play:" + fn)
        
    def run(self):
        """Converts input to .wav and runs the bot's process."""
        if len(sys.argv) == 5:

            pcmfn = sys.argv[2]
            opusfn = pcmfn.replace(".pcm_raw", ".opus_hex")
            wavefn = os.path.join(self.datapath, sys.argv[4] + '.wav')

            memberid = sys.argv[3]
            timestamp = sys.argv[4]

            with open(pcmfn, 'rb') as pcm:
                pcmdata = pcm.read()

            with wave.open(wavefn, 'wb') as wavfile: # Converts pcm to wave
                wavfile.setparams((2, 2, 48000, 0, 'NONE', 'NONE'))
                wavfile.writeframes(pcmdata)
                frames = wavfile.getnframes()

            if frames > self.frame_threshold: # Checks for minimum time requirement
                
                r = sr.Recognizer()
                with sr.AudioFile(wavefn) as source:
                    audio = r.record(source)
                result = r.recognize_google_cloud(audio, credentials_json=self.API_JSON).strip()

                try:
                    self.process(result, memberid, timestamp, wavefn)
                except Exception as e:
                    print(e)

            if self.clearfiles:
                os.remove(pcmfn)
                os.remove(wavefn)

        else:
            raise Exception("Bot must be run with commands passed from main.js")

    def process(self, text, memberid, timestamp, wavefn): # Override
        """Does something once the file has been converted."""
        pass

                

                
