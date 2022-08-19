import speech_recognition as sr
from playsound import playsound

from time import sleep

#________________________________________________________________________________________________________________________________

activationPhrase = ['ROSA'] #etc
r = sr.Recognizer()
m = sr.Microphone()

#________________________________________________________________________________________________________________________________


def startup():
    print('\n\t\tADJUSTING FOR AMIENBT')
    with m as source: r.adjust_for_ambient_noise(source) # we only need to calibrate once, before we start listening

def backgroundListening():
    # initialize the recognizer
    # this is called from the background thread
    def callback(recog, audio):
        try: 
            speech = recog.recognize_google(audio).upper()
            print(f'\n\t{speech}')
            stop_listening(wait_for_stop=False)
            print('\n\tEND OF REC')
        except: 
            print('\n\t\tError in recording, ended')
            stop_listening(wait_for_stop=False)

    print('\n\t\tLISTENING')
    # start listening in the background (note that we don't have to do this inside a `with` statement)
    stop_listening = r.listen_in_background(m, callback)
    # `stop_listening` is now a function that, when called, stops background listening

    # do some unrelated computations for 5 seconds
    for i in range(0, 20): sleep(100)  # we're still listening even though the main thread is doing other things

    # calling this function requests that the background listener stop listening
    #stop_listening(wait_for_stop=False)

def main(): backgroundListening()


#________________________________________________________________________________________________________________________________

if __name__ == '__main__': main()
