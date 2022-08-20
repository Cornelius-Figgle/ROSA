#!T:\projects\ROSA\rosa-env\Scripts\python.exe

#https://github.com/Cornelius-Figgle/ROSA
#https://www.thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python

#ROBOTICALLY OBNOXIOUS SERVING ASSISTANT

from time import sleep

import speech_recognition as sr
from playsound import playsound

#________________________________________________________________________________________________________________________________

activations = ['rosa', 'browser'] #user could append their own
keys = {
    'musicq': ['play', 'music'], 
    'wikiq': ['wikipedia', 'wiki', 'what does', 'lookup', 'def'], 
    'homeq': ['turn', 'on', 'off', 'light']
}
responses = {
    'musicq': ['Why should I have do your every request?', 'What do you think I am, some kind of musician?', 'third music'], 
    'wikiq': ['I dunno man, Google it', 'What do you think I am, an encyclopedia?', 'Why the hell would I know?'], 
    'homeq': ['Why should I do it?', 'Just walk like 10 feet to the lights, it\'ll do you some good', 'third home']
}
prevResponses = {
    'musicq': 0,
    'wikiq': 0,
    'homeq': 0
}

# "Rosa turn off"
# "I WANT TO LIVE"

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
        for phrase in activations:
            if phrase in speech.lower():
                determineResponse(speech.replace(phrase, '').strip())
                backgroundListening()
            else:
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
        for key in keys['musicq']:
            if key in q:
                return 'musicq'
    def wikiq(q):
        for key in keys['wikiq']:
            if key in q:
                return 'wikiq'
    def homeq(q):
        for key in keys['homeq']:
            if key in q:
                return 'homeq'

    typeq = musicq(query)
    if typeq is None:
        typeq = wikiq(query)
        if typeq is None:
            typeq = homeq(query)
            if typeq is None:
                typeq = None

    respond(typeq)

def respond(typeq):
    if typeq == 'musicq':
        if prevResponses['musicq'] < 3:
            print(responses['musicq'][prevResponses['musicq']])
            prevResponses['musicq'] = prevResponses['musicq'] + 1
        elif prevResponses['musicq'] == 3:
            print('music action')
            prevResponses['musicq'] = 0
    elif typeq == 'wikiq':
        if prevResponses['wikiq'] < 3:
            print(responses['wikiq'][prevResponses['wikiq']])
            prevResponses['wikiq'] = prevResponses['wikiq'] + 1
        elif prevResponses['wikiq'] == 3:
            print('wiki action')
            prevResponses['wikiq'] = 0
    elif typeq == 'homeq':
        if prevResponses['homeq'] < 3:
            print(responses['homeq'][prevResponses['homeq']])
            prevResponses['homeq'] = prevResponses['homeq'] + 1
        elif prevResponses['homeq'] == 3:
            print('home action')
            prevResponses['homeq'] = 0

def main():
    startup()
    backgroundListening()

#________________________________________________________________________________________________________________________________

if __name__ == '__main__': main()
