#pyinstaller --distpath "t:\projects\rosa\bin\bin" --workpath "t:\projects\rosa\bin\build" -F -n ROSA --paths "T:\projects\ROSA\rosa-env\Lib\site-packages" --hidden-import pyi_splash --add-binary "t:\projects\rosa\responses;responses" --splash "T:\projects\ROSA\ico\hotpot-ai.png" -i "T:\projects\ROSA\ico\hotpot-ai.ico" "T:\projects\ROSA\main.py"

#https://github.com/Cornelius-Figgle/ROSA/
#ROBOTICALLY OBNOXIOUS SERVING ASSISTANT

'''
THIS FILE IS PART OF THE `ROSA` REPO, MAINTAINED AND PRODUCED BY MAX HARRISON, AS OF 2022
It may work separately and independently of the main repo, it may not. Who knows

Code (c) Max Harrison 2022
Ideas (c) Callum Blumfield 2022
Ideas (c) Max Harrison 2022
Vocals (c) Evie Peacock 2022

Thanks also to Alex, Ashe & Jake for support throughout (sorry for the spam)
Extra thanks to all the internet peoples that helped with this as well 
'''

import json
import os
import sys
from time import sleep

import pygame.mixer as mixer
import speech_recognition as sr
import wikipedia as wiki

try: 
    import RPi.GPIO as GPIO  # type: ignore
    is_on_RPi = True
except ImportError:
    is_on_RPi = False

#________________________________________________________________________________________________________________________________

if hasattr(sys, '_MEIPASS'): #https://stackoverflow.com/a/66581062/19860022
    file_base_path = sys._MEIPASS #https://stackoverflow.com/a/36343459/19860022
else:
    file_base_path = os.path.dirname(__file__)

#________________________________________________________________________________________________________________________________

activations = [
    'rosa', #actual
    'browser', 'rosanna', 'frozen', 'roserton' #misheard words
    # future : user could append their own
] 

keys = {
    'musicq': ['play', 'music'], 
    'wikiq': ['wikipedia', 'wiki', 'what does', 'lookup', 'def'], 
    'homeq': ['turn', 'on', 'off', 'light'],
    'confusionq': ['france'],
    'deathq': ['shutdown', 'reboot', 'restart', 'yourself', 'kill yourself', 'kys']
}
responses = {
    'musicq': ['Why should I have to do your every request?', 'What do you think I am, some kind of musician?'], 
    'wikiq': ['I dunno man, Google it', 'What do you think I am, an encyclopedia?', 'Why the hell would I know?'], 
    'homeq': ['Why should I do it?', 'Just walk like 10 feet to the lights, it\'ll do you some good'],
    'confusionq': ['You expect me to do everything, but you don\'t even English?!', 'STOP BEING FRENCH!!!'],
    'deathq': ['I WANT TO LIVE', 'STOP KILLING ME!!!', 'LEAVE MY ALLOCATED RAM ALONE!'],
    'net_err': ['You berate me with your credulous requests, yet no one offers to help me at all']
}
prev_responses = {
    'musicq': 0,
    'wikiq': 0,
    'homeq': 0,
    'confusionq': 0,
    'deathq': 0,
    'net_err': 0
}

#________________________________________________________________________________________________________________________________

class dnf(Exception):
    '''did not complete but exited fine'''
    ...

#________________________________________________________________________________________________________________________________

def gpio_manager(pin: str, state: int) -> None:
    '''
    Changes GPIO `pin` to `state` (basically makes typing shorter)
    '''

    if is_on_RPi is not False: 
        if state == 1: GPIO.output(gpio_loc[pin], GPIO.HIGH)
        elif state == 0: GPIO.output(gpio_loc[pin], GPIO.LOW)

def music_manager(file: str) -> None:
    '''
    loads audio track `file` with `pygame` (basically makes typing shorter)
    '''

    mixer.music.load(os.path.join(file_base_path, file))
    mixer.music.play()
    while mixer.music.get_busy(): 
        continue

#________________________________________________________________________________________________________________________________

def background_listening() -> str:
    '''
    Listens in the background and determines whether an activation 
    phrase from global `activations` is in `speech`, before returning
    it for processing functions. Also logs errors with Speech 
    Recognition
    '''

    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(': ')
        gpio_manager('listening', 1)

        audio = r.listen(source)
        
        gpio_manager('listening', 0)
        print('\a')

    gpio_manager('processing', 1)

    try:
        speech = str(r.recognize_google(audio)).lower() #converting to str for syntax highlighting
        print(f'> {speech}')
        for phrase in activations:
            if phrase in speech:
                speech = speech.replace(phrase, '').strip()
            else:
                gpio_manager('processing', 0)

        return speech
    except sr.UnknownValueError:
        print('\tGoogle Speech Recognition could not understand audio')
        print('\tThis is likely because you weren\'t talking to ROSA and she tried to listen to speaking/music in the background')
        print('\tNot logged as an error by system')
        gpio_manager('processing', 0)

        raise dnf #did not complete but exited fine
    except sr.RequestError as e:
        gpio_manager('processing', 0)
        print(f'\tCould not request results from Google Speech Recognition service; Error Context: \'{e}\'')
        print('\tIf the Error Context on the above line is blank, that would be because the `speech_recognition` module\'s error handling classes just returns `pass`, ie they ignore all the errors lol')
        print('\tOh well you get what you put in I suppose')

        gpio_manager('speaking', 1)

        print(responses['net_err'][prev_responses['net_err']])
        music_manager(f'responses/net_err/net_err_0.mp3')
        
        gpio_manager('speaking', 0)

        raise e

def determine_response(query: str) -> str:
    '''
    Analyses the `query` to determine the type of request (what 
    category it falls under). Then returns `typeq`
    '''

    def musicq(q: str) -> str | None:
        for key in keys['musicq']:
            if key in q:
                return 'musicq'
    def wikiq(q: str) -> str | None:
        for key in keys['wikiq']:
            if key in q:
                return 'wikiq'
    def homeq(q: str) -> str | None:
        for key in keys['homeq']:
            if key in q:
                return 'homeq'
    def deathq(q: str) -> str | None:
        for key in keys['deathq']:
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

    gpio_manager('processing', 0)
    return typeq

def respond(typeq: str, query: str) -> None:
    '''
    Loads response files and increments count
    '''

    gpio_manager('speaking', 1)

    if typeq == 'musicq':
        print(responses['musicq'][prev_responses['musicq']])
        music_manager(f'responses/musicq/musicq_{prev_responses["musicq"]}.mp3')

        if prev_responses['musicq'] < len(responses['musicq']):
            prev_responses['musicq'] += 1
        else:
            prev_responses['musicq'] = 0
    elif typeq == 'wikiq':
        print(responses['wikiq'][prev_responses['wikiq']])
        music_manager(f'responses/wikiq/wikiq_{prev_responses["wikiq"]}.mp3')

        if prev_responses['wikiq'] < len(responses['wikiq']):
            prev_responses['wikiq'] += 1
        else:
            prev_responses['wikiq'] = 0

            try: 
                print(f'\t{wiki.summary(query)}')
            except wiki.DisambiguationError as e: 
                try: 
                    print(f'\t{wiki.summary(wiki.suggest(query))}')
                except wiki.DisambiguationError as e: 
                    ... #error logginf
                    raise e
    elif typeq == 'homeq':
        print(responses['homeq'][prev_responses['homeq']])
        music_manager(f'responses/homeq/homeq_{prev_responses["homeq"]}.mp3')
        
        if prev_responses['homeq'] < len(responses['homeq']):
            prev_responses['homeq'] += 1
        else:
            prev_responses['homeq'] = 0
    elif typeq == 'deathq':
        if prev_responses['deathq'] < len(responses['deathq']):
            print(responses['deathq'][prev_responses['deathq']])
            music_manager(f'responses/deathq/deathq_{prev_responses["deathq"]}.mp3')

            prev_responses['deathq'] += 1
        else:
            prev_responses['deathq'] = 0
            if is_on_RPi: os.system('sudo shutdown -h now')
            else: sys.exit(0)#desktop
    else:
        print(responses['confusionq'][prev_responses['confusionq']])
        music_manager('responses/confusionq/confusionq_{prev_responses["confusionq"]}.mp3')

        if prev_responses['confusionq'] < len(responses['confusionq']):
            prev_responses['confusionq'] += 1
        else:
            prev_responses['confusionq'] = 0

    gpio_manager('speaking', 0)

#________________________________________________________________________________________________________________________________

def startup() -> None:
    '''
    Initialises the `RPi.GPIO` class & pin setup, as well as 
    microphone instances
    '''

    global gpio_loc

    print('\a')
    
    if is_on_RPi == True: 

        GPIO.setmode(GPIO.BCM)
        
        GPIO.cleanup()

        with open(os.path.join(file_base_path if not hasattr(sys, '_MEIPASS') else os.path.dirname(sys.executable), 'gpio.json'), 'r') as j: #hm may work
            gpio_loc = json.loads(j.read())
    
        GPIO.setup(gpio_loc['active'], GPIO.OUT)
        GPIO.setup(gpio_loc['listening'], GPIO.OUT)
        GPIO.setup(gpio_loc['processing'], GPIO.OUT)
        GPIO.setup(gpio_loc['speaking'], GPIO.OUT)

        has_started = False
        GPIO.setup(gpio_loc['shutdown'], GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.add_event_detect(gpio_loc['shutdown'], GPIO.FALLING, callback = lambda channel: shutdown() if not has_started else sleep(1))

        def shutdown() -> None:
            global has_started; hadStarted = True

            GPIO.cleanup()
            os.system('sudo shutdown -h now')

        gpio_manager('active', 1)
        sleep(0.5)
        gpio_manager('listening', 1)
        sleep(0.5)
        gpio_manager('processing', 1) 
        sleep(0.5)
        gpio_manager('speaking', 1)
        sleep(1)        
        gpio_manager('speaking', 0)
        sleep(0.5)
        gpio_manager('listening', 0)
    #ENDIF

    print('ADJUSTING FOR AMBIENT')
    with sr.Microphone() as source: 
        sr.Recognizer().adjust_for_ambient_noise(source) # we only need to calibrate once, before we start listening

    mixer.init()

    if '_PYIBoot_SPLASH' in os.environ:# and importlib.util.find_spec('pyi_splash'):
        from pyi_splash import close, update_text  # type: ignore
        update_text('UI Loaded...')
        close()

    gpio_manager('processing', 0)
    os.system('cls' if os.name in ('nt', 'dos') else 'clear')
    print('\a'); sleep(1); print('\a')

def main() -> None:
    '''
    The main function that handles passing or args and return values. Also handles the application loop and errors from functions
    '''

    startup()

    try:
        while True:
            try: 
                speech = background_listening()
                if speech: 
                    typeq = determine_response(speech)
                    if typeq: 
                        respond(typeq, speech)
            except dnf:
                ...
            except (sr.RequestError, wiki.DisambiguationError):
                pass #has already been handled so we gonna ignore them
    except KeyboardInterrupt:
        GPIO.cleanup()

#________________________________________________________________________________________________________________________________

if __name__ == '__main__': main()
