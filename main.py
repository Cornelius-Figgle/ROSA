#!T:\projects\ROSA\rosa-env\Scripts\python.exe

#https://github.com/Cornelius-Figgle/ROSA
#https://www.thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python

from time import sleep

import speech_recognition as sr
from playsound import playsound

#________________________________________________________________________________________________________________________________

def startup():
    print('ADJUSTING FOR AMIENBT')
    with sr.Microphone() as source: 
        sr.Recognizer().adjust_for_ambient_noise(source) # we only need to calibrate once, before we start listening

def backgroundListening():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(':')
        audio = r.listen(source)

    try:
        speech = str(r.recognize_google(audio)) #converting to str for syntax highlighting
        if 'rosa' in speech.lower():
            print('rosa? ')
            determineResponse(speech.replace('rosa', '').strip())
            backgroundListening()
        else:
            print(speech)
            backgroundListening()
    except sr.UnknownValueError:
        print('Google Speech Recognition could not understand audio')
        backgroundListening()
    except sr.RequestError as e:
        print('Could not request results from Google Speech Recognition service; {0}'.format(e))
        backgroundListening()

def determineResponse(query):
    print(query)
    def musicq(q):
        keys = ['play', 'music']
        for key in keys:
            if key in q:
                return 'musicq'
    def wikiq(q):
        keys = ['wikipedia', 'wiki', 'what does', 'lookup', 'def']
        for key in keys:
            if key in q:
                return 'wikiq'
    def homeq(q):
        keys = ['turn', 'on', 'off']
        for key in keys:
            if key in q:
                return 'homeq'

    typeq = musicq(query)
    if typeq is None:
        typeq = wikiq(query)
        if typeq is None:
            typeq = homeq(query)
            if typeq is None:
                typeq = None

    print(typeq)
    respond(typeq)

def respond(typeq):
    pass

def main():
    backgroundListening()

#________________________________________________________________________________________________________________________________

if __name__ == '__main__': main()
