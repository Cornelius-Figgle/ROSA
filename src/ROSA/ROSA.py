# 
# -*- coding: UTF-8 -*-

# https://github.com/Cornelius-Figgle/ROSA/
# ROBOTICALLY OBNOXIOUS SERVING ASSISTANT

'''
ROSA (or Robotically Obnoxious Serving Assistant), is a smart assistant
(like the Amazon Alexa), except that it doesn't listen to you. The main
code is written primarily for Windows 10 and RaspbianOS, however should
function on most, if not all, operating systems and platforms

ROSA has three main functions inside of the `ROSA_` class, which are
`background_listening`, `determine_response` and `respond`. These
should be called in that order, with the return values from each being
passed into the next function

### Example: 

```python
import ROSA

obj = ROSA.ROSA_()

try:
    while True:
        try:
            speech = obj.background_listening()
            if speech:  # note: if req asked
                typeq = obj.determine_response(speech)
                obj.respond(typeq)
        except ROSA.dnf:
            ...
except KeyboardInterrupt:
    if ROSA.is_on_RPi: 
        ROSA.do_cleanup()
```

=======================================================================

THIS FILE IS PART OF THE `ROSA` REPO, MAINTAINED AND PRODUCED BY MAX 
HARRISON, AS OF 2023

It may work separately and independently of the main repo, it may not

- Code (c) Max Harrison 2023
- Ideas (c) Callum Blumfield 2023
- Ideas (c) Max Harrison 2023
- Vocals (c) Evie Peacock 2023

Thanks also to everyone else for support throughout (sorry for the
spam). also thanks to all the internet peoples that helped with this
as well 
'''

# note: view associated GitHub info as well
__version__ = 'v0.6.0'  
__author__ = 'Cornelius-Figgle'
__email__ = 'max@fullimage.net'
__maintainer__ = 'Cornelius-Figgle'
__copyright__ = 'Copyright (c) 2023 Max Harrison'
__license__ = 'MIT'
__status__ = 'Development'
__credits__ = ['Max Harrison', 'Callum Blumfield', 'Evie Peacock']


import json
import os
import sys
from contextlib import contextmanager
from tempfile import gettempdir
from threading import Thread
from time import sleep
from typing import NoReturn

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = 'true' ; import pygame.mixer as mixer
import speech_recognition as sr

import foreign_potato_master

try:
    import RPi.GPIO as GPIO  # type: ignore
    is_on_RPi = True
except ImportError:
    # note: Probably a more elegant solution somewhere
    # note: but this is what works for me atm
    is_on_RPi = False


file_base_path = os.path.dirname(__file__)
# note: https://stackoverflow.com/a/74975328/19860022

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

    def __init__(
        self, json_path: str = None, write_file: str = sys.stdout) -> None:

        '''
        Initialises the `RPi.GPIO` class & pin setup, as well as 
        microphone instances
        '''

        self.write_file = write_file

        self.title = foreign_potato_master.Text_Decorations.title
        self.symbols = foreign_potato_master.Text_Decorations.symbols

        def loading_screen_thread() -> None:
            '''
            Simple function to print out the title whilst the
            application is setup. Uses `write_file` from the `ROSA`
            class

            ```python
            
            fred = Thread(
                target=loading_screen_thread,
                name='fred (ROSA)'
            )
            fred.start()
            ```
            '''

            if self.write_file is sys.stdout:
                if os.name in ('nt', 'dos'):
                    os.system('cls')
                else:
                    os.system('clear')
                sleep(1)

            for line in self.title: 
                print(line, file=self.write_file)
                sleep(0.5)
            print('\n\n', file=self.write_file)
            sleep(2)

        fred = Thread(
            target=loading_screen_thread,
            daemon=True,
            name='fred (ROSA)'
        )
        fred.start()

        self.activations = foreign_potato_master.Responses.activations
        self.keys = foreign_potato_master.Responses.keys
        self.responses = foreign_potato_master.Responses.responses
        self.prev_responses = foreign_potato_master.Responses.prev_responses

        self.notices = {}
        for attr in dir(foreign_potato_master.Notices):
            if not attr.startswith('__'):
                # note: filters out built-ins attrs
                self.notices[attr] = getattr(foreign_potato_master.Notices, attr)

        
        mixer.init()

        if is_on_RPi == True: 
            self.__pi_init__(json_path)

        if '_PYIBoot_SPLASH' in os.environ:
            from pyi_splash import close, update_text  # type: ignore
            update_text('UI Loaded...')
            close()

        fred.join()
        # note: join `fred` before we print the notice about adjusting
        # for ambient noise

        print(self.notices['adjusting_levels'], file=write_file)
        with sr.Microphone() as source: 
            sr.Recognizer().adjust_for_ambient_noise(source)
            # note: we only need to calibrate once, before we 
            # start listening

        self.gpio_manager('processing', 0)

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
        phrase from `activations` is in `speech`, before returning it
        for processing functions. Also logs errors with 
        `speech_recognition`
        '''

        # note: obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print(self.notices['awaiting_speech'], file=self.write_file)
            self.gpio_manager('listening', 1)
            audio = r.listen(source)
            self.gpio_manager('listening', 0)

        self.gpio_manager('processing', 1)

        try:
            with no_stdout():
                # note: req speech from google
                speech: str = r.recognize_google(
                    audio, language='en-GB', pfilter=0
                )

            print(f'{self.symbols["input"]} {speech}', file=self.write_file)
            speech = speech.lower()
            
            for phrase in self.activations:
                if phrase in speech:
                    # note: if `ROSA` is said
                    # note: ie the user is talking to us

                    return speech
                    # old: speech = speech.replace(phrase, '').strip()
                else:
                    # note: no `ROSA` keyword, just bg noise
                    self.gpio_manager('processing', 0)
                    return None
        except sr.UnknownValueError:
            self.gpio_manager('processing', 0)
            # old: print(self.notices['unrecognised'], file=self.write_file)
            raise dnf  # note: did not complete but exited fine
        except sr.RequestError as e:
            self.gpio_manager('processing', 0)
            print(print(self.notices['net_err'], file=self.write_file))
            self.respond('net_err')
            raise dnf  # note: did not complete but exited fine

    def determine_response(self, query: str) -> str:
        '''
        Analyses the `query` to determine the type of request (what 
        category it falls under). Then returns `typeq` (use in
        `self.keys[typeq]`)
        '''

        print(self.notices['processing_request'], file=self.write_file)

        for key_set in self.keys:
            for key in self.keys[key_set]:
                if key in query:
                    typeq = key_set
                    break
            else:
                # note: if inner-loop didn't reach `break`
                continue
            break  # note: double break
        
        try:
            typeq
        except UnboundLocalError:
            typeq = 'confusionq'

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
            f'{typeq}_{self.prev_responses[typeq]}.mp3'
        )

        if self.prev_responses[typeq] < len(self.responses[typeq]) - 1:
            self.prev_responses[typeq] += 1
        else:
            self.prev_responses[typeq] = 0
            
            if typeq == 'deathq':
                if is_on_RPi: 
                    os.system('sudo shutdown -h now')
                else: 
                    sys.exit(0)  # note: for desktop

        print(f'{self.symbols["output"]} {res}', file=self.write_file)

        mixer.music.load(file_to_load)
        mixer.music.play()
        while mixer.music.get_busy(): 
            # note: sleeps so Python loop doesn't eat resources as much
            sleep(0.5)

        self.gpio_manager('speaking', 0)
