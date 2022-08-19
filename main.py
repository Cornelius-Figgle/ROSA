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

def main():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print('Say something!')
        audio = r.listen(source)

    # recognize speech using Google Speech Recognition
    try:
        # for testing purposes, we're just using the default API key to use another API key, use `r.recognize_google(audio, key='GOOGLE_SPEECH_RECOGNITION_API_KEY')` instead of `r.recognize_google(audio)`
        print('Google Speech Recognition thinks you said ' + r.recognize_google(audio))
    except sr.UnknownValueError:
        print('Google Speech Recognition could not understand audio')
    except sr.RequestError as e:
        print('Could not request results from Google Speech Recognition service; {0}'.format(e))

#________________________________________________________________________________________________________________________________

if __name__ == '__main__': main()
