# pyinstaller --distpath "t:\projects\rosa\bin\bin" --workpath "t:\projects\rosa\bin\build" -F -n ROSA --paths "T:\projects\ROSA\rosa-env\Lib\site-packages" --hidden-import pyi_splash --add-binary "t:\projects\rosa\responses;responses" --splash "T:\projects\ROSA\docs\ico\hotpot-ai.png" -i "T:\projects\ROSA\docs\ico\hotpot-ai.ico" "T:\projects\ROSA\main.py"
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
    # note: Probably a more elegant solution somewhere but 
    # note: this is what works for me atm
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

    Example:
    ```
    with no_stdout():
        do_something_noisily()
    ```
    '''

    save_stdout = sys.stdout
    sys.stdout = open(os.path.join(gettempdir(), 'trash'), 'w')
    yield
    sys.stdout = save_stdout

class dnf(Exception):
    '''
    Exception class for error handling

    did not complete but exited fine
    '''
    ...

class ROSA(object):
    '''
    Main class for defining responses/keywords etc
    '''

    def __init__(self, *args: object) -> None:
        super().__init__(*args)
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
            'musicq': ['Why should I have to do your every request?', 
                'What do you think I am, some kind of musician?'], 
            'wikiq': ['I dunno man, Google it', 
                'What do you think I am, an encyclopedia?', 
                'Why the hell would I know?'],
            'homeq': ['Why should I do it?', 
                'Just walk like 10 feet to the lights, itll do you some' \
                ' good'],
            'confusionq': ['You expect me to do everything, but you dont' \
                ' even English?!', 'STOP BEING FRENCH!!!'],
            'deathq': ['I WANT TO LIVE', 'STOP KILLING ME!!!', 
                'LEAVE MY ALLOCATED RAM ALONE!'],
            'net_err': ['You berate me with your credulous requests, yet no' \
                ' one offers to help me at all']
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
            self.gpio_loc = {}

            GPIO.setmode(GPIO.BCM)                
            GPIO.cleanup()

            if not hasattr(sys, '_MEIPASS'):  
                _path_to_use = os.path.join(
                    file_base_path, 
                    'gpio.json'
                )
            else:
                _path_to_use = os.path.join(
                    os.path.dirname(sys.executable),
                    'gpio.json'
                )
            with open(_path_to_use, 'r') as j:
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

                GPIO.cleanup()
                os.system('sudo shutdown -h now')

            self.gpio_manager('active', 1)
            sleep(0.5)
            self.gpio_manager('listening', 1)
            sleep(0.5)
            self.gpio_manager('processing', 1) 
            sleep(0.5)
            self.gpio_manager('speaking', 1)
            sleep(1)        
            self.gpio_manager('speaking', 0)
            sleep(0.5)
            self.gpio_manager('listening', 0)

        if '_PYIBoot_SPLASH' in os.environ:
            from pyi_splash import close, update_text  # type: ignore
            update_text('UI Loaded...')
            close()

        os.system('cls' if os.name in ('nt', 'dos') else 'clear'); sleep(1)


    def gpio_manager(self, pin: str, state: int) -> None:
        '''
        Changes GPIO `pin` to `state` (basically makes typing shorter)
        '''

        if is_on_RPi is not False: 
            if state == 1: GPIO.output(self.gpio_loc[pin], GPIO.HIGH)
            elif state == 0: GPIO.output(self.gpio_loc[pin], GPIO.LOW)

    def music_manager(self, file: str) -> None:
        '''
        loads audio track `file` with `pygame` (basically makes typing shorter)
        '''

        mixer.music.load(os.path.join(file_base_path, file))
        mixer.music.play()
        while mixer.music.get_busy(): 
            continue


    def background_listening(self) -> str:
        '''
        Listens in the background and determines whether an activation 
        phrase from global `activations` is in `speech`, before returning
        it for processing functions. Also logs errors with Speech 
        Recognition
        '''

        # NOTE: obtain audio from the microphone
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print('\n: ')
            self.gpio_manager('listening', 1)

            audio = r.listen(source)
            
            self.gpio_manager('listening', 0)

        self.gpio_manager('processing', 1)

        try:
            with no_stdout():
                speech: str = r.recognize_google(audio, pfilter=1)
                speech = speech.lower()

            print(f'> {speech}')
            for phrase in self.activations:
                if phrase in speech:
                    speech = speech.replace(phrase, '').strip()
                else:
                    self.gpio_manager('processing', 0)

            return speech
        except sr.UnknownValueError:
            self.gpio_manager('processing', 0)

            print('\tGoogle Speech Recognition could not understand audio')
            print('\tThis is likely because you weren\'t talking to ROSA and' \
                'she tried to listen to speaking/music in the background')
            print('\tNot logged as an error by system')

            raise dnf  # NOTE: did not complete but exited fine
        except sr.RequestError as e:
            self.gpio_manager('processing', 0)

            print(f'\tCould not request results from Google Speech' \
                'Recognition service; Error Context: \'{e}\'')
            print('\tIf the Error Context on the above line is blank, that' \
            'would be because the `speech_recognition` module\'s error handling' \
            'classes just returns `pass`, ie they ignore all the errors lol')
            print('\tOh well you get what you put in I suppose')

            self.gpio_manager('speaking', 1)

            print(self.responses['net_err'][self.prev_responses['net_err']])
            self.music_manager(f'responses/net_err/net_err_0.mp3')

            self.gpio_manager('speaking', 0)

            raise e

    def determine_response(self, query: str) -> str:
        '''
        Analyses the `query` to determine the type of request (what 
        category it falls under). Then returns `typeq`
        '''

        def musicq(q: str) -> str | None:
            for key in self.keys['musicq']:
                if key in q:
                    return 'musicq'
        def wikiq(q: str) -> str | None:
            for key in self.keys['wikiq']:
                if key in q:
                    return 'wikiq'
        def homeq(q: str) -> str | None:
            for key in self.keys['homeq']:
                if key in q:
                    return 'homeq'
        def deathq(q: str) -> str | None:
            for key in self.keys['deathq']:
                if key in q:
                    return 'deathq'

        typeq = musicq(query)
        if typeq is None:
            typeq = wikiq(query)
            if typeq is None:
                typeq = homeq(query)
                if typeq is None:
                    typeq = deathq(query)
                    if typeq is None:
                        typeq = 'confusionq'

        self.gpio_manager('processing', 0)
        return typeq

    def respond(self, typeq: str, query: str) -> None:
        '''
        Loads response files and increments count
        '''

        self.gpio_manager('speaking', 1)

        if typeq == 'musicq':
            print(self.responses['musicq'][self.prev_responses['musicq']])
            self.music_manager(f'responses/musicq/musicq_{self.prev_responses["musicq"]}.mp3')

            if self.prev_responses['musicq'] < len(self.responses['musicq']):
                self.prev_responses['musicq'] += 1
            else:
                self.prev_responses['musicq'] = 0
        elif typeq == 'wikiq':
            print(self.responses['wikiq'][self.prev_responses['wikiq']])
            self.music_manager(f'responses/wikiq/wikiq_{self.prev_responses["wikiq"]}.mp3')

            if self.prev_responses['wikiq'] < len(self.responses['wikiq']):
                self.prev_responses['wikiq'] += 1
            else:
                self.prev_responses['wikiq'] = 0
        elif typeq == 'homeq':
            print(self.responses['homeq'][self.prev_responses['homeq']])
            self.music_manager(f'responses/homeq/homeq_{self.prev_responses["homeq"]}.mp3')
            
            if self.prev_responses['homeq'] < len(self.responses['homeq']):
                self.prev_responses['homeq'] += 1
            else:
                self.prev_responses['homeq'] = 0
        elif typeq == 'deathq':
            if self.prev_responses['deathq'] < len(self.responses['deathq']):
                print(self.responses['deathq'][self.prev_responses['deathq']])
                self.music_manager(f'responses/deathq/deathq_{self.prev_responses["deathq"]}.mp3')

                self.prev_responses['deathq'] += 1
            else:
                self.prev_responses['deathq'] = 0
                if is_on_RPi: os.system('sudo shutdown -h now')
                else: sys.exit(0)#desktop
        else:
            print(self.responses['confusionq'][self.prev_responses['confusionq']])
            self.music_manager(f'responses/confusionq/confusionq_{self.prev_responses["confusionq"]}.mp3')

            if self.prev_responses['confusionq'] < len(self.responses['confusionq']):
                self.prev_responses['confusionq'] += 1
            else:
                self.prev_responses['confusionq'] = 0

        self.gpio_manager('speaking', 0)


def main() -> NoReturn:
    '''
    The main function that handles passing or args and return values.
    Also handles the application loop and errors from functions
    '''

    obj = ROSA()

    try:
        while True:
            try: 
                speech = obj.background_listening()
                if speech:  # note: if not error
                    typeq = obj.determine_response(speech)
                    if typeq:  # note: if not error
                        obj.respond(typeq, speech)
            except dnf:
                ...
    except KeyboardInterrupt:
        if is_on_RPi: GPIO.cleanup()
        sys.exit(0)


if __name__ == '__main__': main()
