#!T:\projects\ROSA\rosa-env\Scripts\python.exe

#https://github.com/Cornelius-Figgle/ROSA

#ROBOTICALLY OBNOXIOUS SERVING ASSISTANT

import os
from configparser import ConfigParser
from time import sleep

import speech_recognition as sr
from playsound import playsound

try: 
    import RPi.GPIO as GPIO  # type: ignore
    isOn_RPi = True
except:
    isOn_RPi = False

#________________________________________________________________________________________________________________________________

activations = ['rosa', 'browser', 'rosanna', 'frozen'] #user could append their own

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
    'deathq': ['I WANT TO LIVE', 'STOP KILLING ME!!!', 'LEAVE MY ALLOCATED RAM ALONE!']
}
prevResponses = {
    'musicq': 0,
    'wikiq': 0,
    'homeq': 0,
    'confusionq': 0,
    'deathq': 0
}

#________________________________________________________________________________________________________________________________

def startup():
    print('ADJUSTING FOR AMIENBT')
    with sr.Microphone() as source: 
        sr.Recognizer().adjust_for_ambient_noise(source) # we only need to calibrate once, before we start listening
    
    if isOn_RPi == True: 
        GPIO.setmode(GPIO.BCM)
        config = ConfigParser()

        config.read('gpio.ini')

        gpio_loc = {}

        gpio_loc['active'] = config.get('LEDs', 'active')
        gpio_loc['listen'] = config.getboolean('LEDS', 'listening')
        gpio_loc['process'] = config.getint('LEDs', 'processing')
        gpio_loc['out'] = config.getfloat('LEDs', 'speaking')
        gpio_loc['off_sw'] = config.getfloat('switch', 'shutdown')

        GPIO.output(gpio_loc['active'], GPIO.HIGH)
        GPIO.output(gpio_loc['listen'], GPIO.HIGH)
        GPIO.output(gpio_loc['process'], GPIO.HIGH)
        GPIO.output(gpio_loc['out'], GPIO.HIGH)

        sleep(1)
        
        GPIO.output(gpio_loc['listen'], GPIO.LOW)
        GPIO.output(gpio_loc['process'], GPIO.LOW)
        GPIO.output(gpio_loc['out'], GPIO.LOW)

        GPIO.input(gpio_loc['off_sw']) == False

    if '_PYIBoot_SPLASH' in os.environ:# and importlib.util.find_spec("pyi_splash"):
        from pyi_splash import close, update_text  # type: ignore
        update_text('UI Loaded ...')
        close()

def backgroundListening():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(':')
        audio = r.listen(source)

    try:
        speech = str(r.recognize_google(audio)).lower() #converting to str for syntax highlighting
        print(f'> {speech}')
        for phrase in activations:
            if phrase in speech:
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
    def deathq(q):
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

    respond(typeq)

def respond(typeq):
    if typeq == 'musicq':
        if prevResponses['musicq'] < len(responses['musicq']):
            print(responses['musicq'][prevResponses['musicq']])
            playsound(f'{os.path.dirname(__file__)}/responses/_/monolith.mp3')
            prevResponses['musicq'] += 1
        else:
            print('music action')
            prevResponses['musicq'] = 0
    elif typeq == 'wikiq':
        if prevResponses['wikiq'] < len(responses['wikiq']):
            print(responses['wikiq'][prevResponses['wikiq']])
            playsound(f'{os.path.dirname(__file__)}/responses/_/monolith.mp3')
            prevResponses['wikiq'] += 1
        else:
            print('wiki action')
            prevResponses['wikiq'] = 0
    elif typeq == 'homeq':
        print(responses['homeq'][prevResponses['homeq']])
        playsound(f'{os.path.dirname(__file__)}/responses/_/monolith.mp3')
        if prevResponses['homeq'] < len(responses['homeq']):
            prevResponses['homeq'] += 1
        else:
            prevResponses['homeq'] = 0
    elif typeq == 'deathq':
        if prevResponses['deathq'] < len(responses['deathq']):
            print(responses['deathq'][prevResponses['deathq']])
            playsound(f'{os.path.dirname(__file__)}/responses/_/monolith.mp3')
            prevResponses['deathq'] += 1
        else:
            print('death action')
            prevResponses['deathq'] = 0
    else:
        print(responses['confusionq'][prevResponses['confusionq']])
        playsound(f'{os.path.dirname(__file__)}/responses/_/monolith.mp3')
        if prevResponses['confusionq'] < len(responses['confusionq']):
            prevResponses['confusionq'] += 1
        else:
            prevResponses['confusionq'] = 0

def main():
    startup()
    backgroundListening()

#________________________________________________________________________________________________________________________________

if __name__ == '__main__': main()
