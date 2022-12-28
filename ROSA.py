# 
# 
# -*- coding: UTF-8 -*-

# https://github.com/Cornelius-Figgle/ROSA/
# ROBOTICALLY OBNOXIOUS SERVING ASSISTANT

'''
THIS FILE IS PART OF THE `ROSA` REPO, MAINTAINED AND PRODUCED BY MAX 
HARRISON, AS OF 2022

It may work separately and independently of the main repo, it may not

 - Code (c) Max Harrison 2022
 - Ideas (c) Callum Blumfield 2022
 - Ideas (c) Max Harrison 2022
 - Vocals (c) Evie Peacock 2022

Thanks also to Alex, Ashe & Jake for support throughout (sorry for the
spam). also thanks to all the internet peoples that helped with this
as well 
'''

# note: view associated GitHub info as well
__version__ = 'Pre-release'  
__author__ = 'Cornelius-Figgle'
__email__ = 'max@fullimage.net'
__maintainer__ = 'Cornelius-Figgle'
__copyright__ = 'Copyright (c) 2022 Max Harrison'
__license__ = 'MIT'
__status__ = 'Development'
__credits__ = ['Max Harrison', 'Callum Blumfield', 'Evie Peacock']


import json
import os
import sys
from contextlib import contextmanager
from tempfile import gettempdir
from time import sleep
from typing import NoReturn

import pygame.mixer as mixer
import speech_recognition as sr

try: 
    import RPi.GPIO as GPIO  # type: ignore
    is_on_RPi = True
except ImportError:  
    # note: Probably a more elegant solution somewhere
    # note: but this is what works for me atm
    is_on_RPi = False


if hasattr(sys, '_MEIPASS'):
    # source: https://stackoverflow.com/a/66581062/19860022
    file_base_path = sys._MEIPASS
    # source: https://stackoverflow.com/a/36343459/19860022
else:
    file_base_path = os.path.dirname(__file__)

@contextmanager
def no_stdout() -> None:
    '''
    Silences the `sys.stdout` of a function call 
    
    [Credit here](https://stackoverflow.com/a/2829036/19860022)

    ### Example:
    
    ```python
    with no_stdout():
        do_something_noisily()
    ```
    '''

    save_stdout = sys.stdout
    sys.stdout = open(os.path.join(gettempdir(), 'trash'), 'w')
    yield
    sys.stdout = save_stdout

def do_cleanup() -> None:
    '''
    Nice exit for ROSA, calls `RPi.GPIO.cleanup()`

    (will expand in future)
    '''

    if is_on_RPi:
        GPIO.cleanup()


class dnf(Exception):
    '''
    Exception class for error handling - did not complete but exited
    fine
    '''
    ...

class ROSA_:
    '''
    Main class for defining responses/keywords etc
    '''

    def __init__(self, json_path: str = None) -> None:
        '''
        Initialises the `RPi.GPIO` class & pin setup, as well as 
        microphone instances
        '''
        
        self.activations = [
            'rosa', 'browser', 'rosanna', 'frozen', 'roserton', 'rota' 
            # note: misheard words are included as well
            # future: user could append their own via a command ?
        ] 
        self.keys = {
            'musicq': ['play', 'music'], 
            'wikiq': ['wikipedia', 'wiki', 'what does', 'lookup', 'def'], 
            'homeq': ['turn', 'on', 'off', 'light'],
            'confusionq': ['france'],
            'deathq': ['shutdown', 'reboot', 'restart', 'yourself', 'kill']
        }
        self.responses = {
            'musicq': [
                'Why should I have to do your every request?', 
                'What do you think I am, some kind of musician?'
            ], 
            'wikiq': [
                'I dunno man, Google it', 
                'What do you think I am, an encyclopedia?', 
                'Why the hell would I know?'
            ],
            'homeq': [
                'Why should I do it?', 
                'Just walk like 10 feet to the lights, itll do you some good'
            ],
            'confusionq': [
                'You expect me to do everything, but you dont even English?!',
                'STOP BEING FRENCH!!!'
            ],
            'deathq': [
                'I WANT TO LIVE', 'STOP KILLING ME!!!', 
                'LEAVE MY ALLOCATED RAM ALONE!'
            ],
            'net_err': [
                'You berate me with your credulous requests, yet no one offers to help me at all'
            ]
        }
        self.prev_responses = {
            'musicq': 0,
            'wikiq': 0,
            'homeq': 0,
            'confusionq': 0,
            'deathq': 0,
            'net_err': 0
        }

        print('ADJUSTING FOR AMBIENT')
        with sr.Microphone() as source: 
            sr.Recognizer().adjust_for_ambient_noise(source)
            # note: we only need to calibrate once, before we 
            # note: start listening
        
        mixer.init()

        if is_on_RPi == True: 
            self.__pi_init__(json_path)

        if '_PYIBoot_SPLASH' in os.environ:
            from pyi_splash import close, update_text  # type: ignore
            update_text('UI Loaded...')
            close()

    def __pi_init__(self, json_path: str) -> None:
        self.gpio_loc = {}

        GPIO.setmode(GPIO.BCM)                
        GPIO.cleanup()

        with open(json_path, 'r') as j:
            self.gpio_loc = json.loads(j.read())
                
        GPIO.setup(self.gpio_loc['active'], GPIO.OUT)
        GPIO.setup(self.gpio_loc['listening'], GPIO.OUT)
        GPIO.setup(self.gpio_loc['processing'], GPIO.OUT)
        GPIO.setup(self.gpio_loc['speaking'], GPIO.OUT)

        self.has_started = False
        GPIO.setup(
            self.gpio_loc['shutdown'], 
            GPIO.IN, 
            pull_up_down = GPIO.PUD_UP
        )
        GPIO.add_event_detect(
            self.gpio_loc['shutdown'], 
            GPIO.FALLING, 
            callback = lambda channel: 
                shutdown() if not self.has_started else sleep(1)
        )

        def shutdown() -> NoReturn:
            self.hadStarted = True

            do_cleanup()
            os.system('sudo shutdown -h now')

        def boot_animation() -> None:
            # note: lights go up
            self.gpio_manager('active', 1)
            sleep(0.5)
            self.gpio_manager('listening', 1)
            sleep(0.5)
            self.gpio_manager('processing', 1) 
            sleep(0.5)
            self.gpio_manager('speaking', 1)

            # note: and go back down
            sleep(1)        
            self.gpio_manager('speaking', 0)
            sleep(0.5)
            self.gpio_manager('listening', 0)

        boot_animation()


    def gpio_manager(self, pin: str | int, state: int) -> None:
        '''
        Changes GPIO `pin` to `state`. If `pin` is str, ROSA uses the
        pin n° defined in `gpio_loc` (from `ROSA_.__pi_init__`)
        '''

        if is_on_RPi: 
            if type(pin) is str:
                # note if dict key instead of pin n°
                pin = self.gpio_loc[pin]
            if state == 1: 
                # note: turn LED on
                GPIO.output(pin, GPIO.HIGH)
            elif state == 0: 
                # note: turn LED off
                GPIO.output(pin, GPIO.LOW)


    def background_listening(self) -> str:
        '''
        Listens in the background and determines whether an activation 
        phrase from global `activations` is in `speech`, before returning
        it for processing functions. Also logs errors with Speech 
        Recognition
        '''

        # note: obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('\n: ')
            self.gpio_manager('listening', 1)

            audio = r.listen(source)
            
            self.gpio_manager('listening', 0)

        self.gpio_manager('processing', 1)

        try:
            with no_stdout():
                # note: req speech from google
                speech: str = r.recognize_google(
                    audio, language='en-GB', pfilter=1
                )
                speech = speech.lower()

            print(f'> {speech}')
            for phrase in self.activations:
                if phrase in speech:
                    # note: if `ROSA` is said
                    # note: ie if user is talking to us

                    return speech
                    # old: speech = speech.replace(phrase, '').strip()
                else:
                    # note: no `ROSA` keyword, just bg noise
                    self.gpio_manager('processing', 0)
                    return None
        except sr.UnknownValueError:
            self.gpio_manager('processing', 0)

            print('\tGoogle Speech Recognition could not understand audio')
            print('\tThis is likely because you weren\'t talking to ROSA and she tried to listen to speaking/music that is in the background')
            print('\tNot logged as an error')

            raise dnf  # note: did not complete but exited fine
        except sr.RequestError as e:
            self.gpio_manager('processing', 0)

            print('\tCould not request results from Google Speech Recognition service')
            print(f'\t\tError Context: \"{e}\"')
            print('\tIf the Error Context on the above line is blank, that would be because the `speech_recognition` module\'s error handling classes just returns `pass`, ie they ignore all the errors lol')
            print('\tOh well you get out what you put in I suppose')

            self.respond('net_err')

            raise e

    def determine_response(self, query: str) -> str:
        '''
        Analyses the `query` to determine the type of request (what 
        category it falls under). Then returns `typeq` (use in
        `self.keys[typeq]`)
        '''

        for key_set in self.keys:
            for key in self.keys[key_set]:
                if key in query:
                    typeq = key_set
                    break
            else:
                # note: if inner-loop didn't reach `break`
                continue
            break  # note: double break

        self.gpio_manager('processing', 0)
        return typeq

    def respond(self, typeq: str) -> None:
        '''
        Loads response files and increments count
        '''

        self.gpio_manager('speaking', 1)

        res = self.responses[typeq][self.prev_responses[typeq]]
        file_to_load = os.path.join(
            file_base_path,
            'responses',
            typeq,
            f'{typeq}_{self.prev_responses[typeq]}.mp3'
        )
        if self.prev_responses[typeq] < len(self.responses[typeq]):
            self.prev_responses[typeq] += 1
        else:
            self.prev_responses[typeq] = 0
            
            if typeq == 'deathq':
                if is_on_RPi: 
                    os.system('sudo shutdown -h now')
                else: 
                    sys.exit(0)  # note: for desktop

        print(res)
        mixer.music.load(file_to_load)
        mixer.music.play()
        while mixer.music.get_busy(): 
            # note: sleeps so Python loop doesn't eat resources as much
            sleep(0.5)

        self.gpio_manager('speaking', 0)
