from msvcrt import getwch
from os import curdir, name, path
from subprocess import run
from sys import executable
from urllib.request import urlretrieve

from qol_mth import clearConsole, sleep

'''
``playsound`` needs no mp3 tags 
``text from aud file needs .wav
'''


'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''
https://www.thepythoncode.com/article/using-speech-recognition-to-convert-speech-to-text-python
'''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''''

clearConsole()

working_dir = path.abspath(curdir)

if name == 'nt': #win
    print('\n\tRun shell installations? y/n')
    if 'y' in getwch(): 
        clearConsole()

        url = 'https://aka.ms/vs/16/release/vs_buildtools.exe'
        destination = f'{working_dir}/installations/Microsoft C++ Build Tools.exe'
        download = urlretrieve(url, destination)
        

        run([executable, '-m','ensurepip','--upgrade']) ; clearConsole()
        run([executable, '-m','pip','install', '--upgrade', 'setuptools']) ; clearConsole()
        run([executable, '-m','pip','install','pipwin']) ; clearConsole()
        run([executable,'-m','pip', 'install', 'playsound']) ; clearConsole()
        run([executable,'-m','pip', 'install', 'SpeechRecognition']) ; clearConsole()
        run([executable,'-m','pip', 'install', 'pydub']) ; clearConsole()
        run([executable,'-m','pip', 'install', 'wikipedia']) ; clearConsole()
        run([executable,'-m','pip', 'install', 'Sentience-CraigR8806']) ; clearConsole()
        run([executable,'-m','pipwin', 'install', 'pyaudio']) ; clearConsole()
    print(working_dir)# ; getwch()
elif name == 'posix': #ie slightly not dos
    print('\n\tRun shell installations? y/n')
    if 'y' in getwch(): #commands are the same lol
        clearConsole()
        run([executable, '-m','ensurepip','--upgrade']) ; clearConsole()
        run([executable, '-m','pip','install', '--upgrade', 'setuptools']) ; clearConsole()
        run([executable, '-m','pip','install','pipwin']) ; clearConsole()
        run([executable,'-m','pip', 'install', 'playsound']) ; clearConsole()
        run([executable,'-m','pip', 'install', 'SpeechRecognition']) ; clearConsole()
        run([executable,'-m','pip', 'install', 'pydub']) ; clearConsole()
        run([executable,'-m','pip', 'install', 'wikipedia']) ; clearConsole()
        run([executable,'-m','pip', 'install', 'Sentience-CraigR8806']) ; clearConsole()
        run([executable,'-m','pipwin', 'install', 'pyaudio']) ; clearConsole()
    print(working_dir)# ; getwch()
else: quit() #basically it can return 'nt' 'posix' or 'java' and idk what causes java but ye this just stops program having seizuerur if it can't indentify os for whatever reason

import speech_recognition as sr
#from wikipedia import 
import wikipedia
from playsound import playsound

activationPhrase = ['ROSA', 'ROZA'] #etc



def backgroundListening():
    clearConsole()
    # initialize the recognizer
       
    # this is called from the background thread
    def callback(recog, audio):
        try: 
            speech = recog.recognize_google(audio).upper()
            print(f'\n\t{speech}')
            stop_listening(wait_for_stop=False)
            print('\n\tEND OF REC')
            if_gate_spam(speech)
        except: 
            print('\n\t\tError in recording, ended')
            stop_listening(wait_for_stop=False)

    r = sr.Recognizer()
    m = sr.Microphone()
    print('\n\t\tADJUSTING FOR AMIENBT')
    with m as source: r.adjust_for_ambient_noise(source)  # we only need to calibrate once, before we start listening
    print('\n\t\tLISTENING')
    # start listening in the background (note that we don't have to do this inside a `with` statement)
    stop_listening = r.listen_in_background(m, callback)
    # `stop_listening` is now a function that, when called, stops background listening

    # do some unrelated computations for 5 seconds
    for i in range(0,20): sleep(0.1)  # we're still listening even though the main thread is doing other things

    # calling this function requests that the background listener stop listening
    #stop_listening(wait_for_stop=False)

#backgroundListening()

def if_gate_spam(speech):
    speech = speech.upper()
    if 'TURN' in speech: 
        playsound(working_dir + '/responses/turn.mp3')
        for i in range(0, 4): sleep(0.5)
    if 'WIKI' in speech or 'SEARCH' in speech:
        try: speech = speech.replace('WIKIPEDIA ', '')
        except: pass
        try: speech = speech.replace('WIKI ', '')
        except: pass
        try: speech = speech.replace('SEARCH ', '')
        except: pass
        try: print(wikipedia.summary(speech, sentences=4))
        except: print('error')

backgroundListening()
#if_gate_spam(input('query? '))


getwch()
