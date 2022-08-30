#!T:\projects\ROSA\rosa-env\Scripts\python.exe

#https://github.com/Cornelius-Figgle/ROSA

#ROBOTICALLY OBNOXIOUS SERVING ASSISTANT

from logging import shutdown
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

activations = ['rosa', 'browser', 'rosanna', 'frozen'] # future: user could append their own

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
    global gpio_loc

    print('\a')
    
    if isOn_RPi == True: 
        GPIO.setmode(GPIO.BCM)
        config = ConfigParser()

        config.read(f'{os.path.dirname(__file__)}/gpio.ini')

        gpio_loc = {}

        gpio_loc['active'] = config.get('LEDs', 'active')
        gpio_loc['listen'] = config.get('LEDS', 'listening')
        gpio_loc['process'] = config.get('LEDs', 'processing')
        gpio_loc['out'] = config.get('LEDs', 'speaking')
        gpio_loc['off_sw'] = config.get('switch', 'shutdown')

        for pin in gpio_loc:
            if pin == 'None':
                gpio_loc[pin] = None
	
        GPIO.setup(gpio_loc['active'], GPIO.OUT)
        GPIO.setup(gpio_loc['listen'], GPIO.OUT)
        GPIO.setup(gpio_loc['process'], GPIO.OUT)
        GPIO.setup(gpio_loc['out'], GPIO.OUT)

        hasStarted = False
        GPIO.setup(gpio_loc['off_sw'], GPIO.IN)
        GPIO.add_event_detect(gpio_loc['off_sw'], GPIO.RISING, callback = lambda channel: shutdown() if hasStarted == False else sleep(1))

        def shutdown():
            global hasStarted; hadStarted = True
            os.system('sudo shutdown -h now')

        gpioManager('active', 1)
        gpioManager('listen', 1)
        gpioManager('process', 1) 
        gpioManager('out', 1)

        sleep(1)
        
        gpioManager('listen', 0)
        gpioManager('out', 0)

    print('ADJUSTING FOR AMIENBT')
    with sr.Microphone() as source: 
        sr.Recognizer().adjust_for_ambient_noise(source) # we only need to calibrate once, before we start listening

    if '_PYIBoot_SPLASH' in os.environ:# and importlib.util.find_spec("pyi_splash"):
        from pyi_splash import close, update_text  # type: ignore
        update_text('UI Loaded...')
        close()

    gpioManager('process', 0)
    print('\a'); sleep(1); print('\a')

def gpioManager(pin, state):
    if isOn_RPi == True: 
        if pin != None:
            if state == 1: GPIO.output(gpio_loc[pin], GPIO.HIGH)
            elif state == 0: GPIO.output(gpio_loc[pin], GPIO.LOW)

def backgroundListening():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(':')
        gpioManager('listen', 1)

        audio = r.listen(source)
        
        gpioManager('listen', 0)
        print('\a')

    gpioManager('process', 1)

    try:
        speech = str(r.recognize_google(audio)).lower() #converting to str for syntax highlighting
        print(f'> {speech}')
        for phrase in activations:
            if phrase in speech:
                determineResponse(speech.replace(phrase, '').strip())
                backgroundListening()
            else:
                gpioManager('process', 0)
                backgroundListening()
    except sr.UnknownValueError:
        print('Google Speech Recognition could not understand audio')
        gpioManager('process', 0)
        backgroundListening()
    except sr.RequestError as e:
        print('Could not request results from Google Speech Recognition service; {0}'.format(e))
        gpioManager('process', 0)
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

    gpioManager('process', 0)
    respond(typeq)

def respond(typeq):
    gpioManager('out', 1)

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

    gpioManager('out', 0)

def main():
    startup()
    backgroundListening()

#________________________________________________________________________________________________________________________________

if __name__ == '__main__': main()
