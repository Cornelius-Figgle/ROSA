#!T:\projects\ROSA\rosa-env\Scripts\python.exe

#https://www.thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python

from time import sleep

import speech_recognition as sr
from playsound import playsound

#________________________________________________________________________________________________________________________________

activationPhrase = ['ROSA'] #etc
r = sr.Recognizer()
m = sr.Microphone()

#________________________________________________________________________________________________________________________________

def startup():
    print('\n\t\tADJUSTING FOR AMIENBT')
    with m as source: r.adjust_for_ambient_noise(source) # we only need to calibrate once, before we start listening

def main():
    with sr.Microphone() as source:
        # read the audio data from the default microphone
        audio_data = r.record(source, duration=5)
        print("Recognizing...")
        # convert speech to text
        text = r.recognize_google(audio_data)
        print(text)



#________________________________________________________________________________________________________________________________

if __name__ == '__main__': main()
