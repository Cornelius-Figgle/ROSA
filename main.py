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
<<<<<<< HEAD
            print('rosa? ')
=======
            print('rosa?')
>>>>>>> 03fea28b17328b5d967eb9ccc39d7900e105f7d2
            answer(speech[4:].strip())
    except sr.UnknownValueError:
        print('Google Speech Recognition could not understand audio')
    except sr.RequestError as e:
        print('Could not request results from Google Speech Recognition service; {0}'.format(e))

def answer(query):
    print(query)
    backgroundListening()

def main():
    backgroundListening()

#________________________________________________________________________________________________________________________________

if __name__ == '__main__': main()
