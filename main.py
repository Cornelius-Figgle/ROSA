import speech_recognition as sr
#from wikipedia import 
import wikipedia
from playsound import playsound

from qol_mth import sleep

#________________________________________________________________________________________________________________________________

activationPhrase = ['ROSA'] #etc

def backgroundListening():
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
        playsound('/responses/turn.mp3')
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

#________________________________________________________________________________________________________________________________

backgroundListening()
#if_gate_spam(input('query? '))