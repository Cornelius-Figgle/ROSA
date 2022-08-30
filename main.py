#!T:\projects\ROSA\rosa-env\Scripts\python.exe

#https://github.com/Cornelius-Figgle/ROSA

#ROBOTICALLY OBNOXIOUS SERVING ASSISTANT

import json
import os
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
    'deathq': ['I WANT TO LIVE', 'STOP KILLING ME!!!', 'LEAVE MY ALLOCATED RAM ALONE!'],
    'net_err': ['You berate me with your credulous requests, yet no one offers to help me at all']
}
prevResponses = {
    'musicq': 0,
    'wikiq': 0,
    'homeq': 0,
    'confusionq': 0,
    'deathq': 0,
    'net_err': 0
}

#________________________________________________________________________________________________________________________________

def startup():
    global gpio_loc

    print('\a')
    
    if isOn_RPi == True: 

        GPIO.setmode(GPIO.BCM)

        with open(os.path.join(os.path.dirname(__file__), 'gpio.json'), 'r') as j:
            gpio_loc = json.loads(j.read())
	
        GPIO.setup(gpio_loc['active'], GPIO.OUT)
        GPIO.setup(gpio_loc['listening'], GPIO.OUT)
        GPIO.setup(gpio_loc['processing'], GPIO.OUT)
        GPIO.setup(gpio_loc['speaking'], GPIO.OUT)

        hasStarted = False
        GPIO.setup(gpio_loc['shutdown'], GPIO.IN, pull_up_down = GPIO.PUD_UP)
        GPIO.add_event_detect(gpio_loc['shutdown'], GPIO.FALLING, callback = lambda channel: shutdown() if not hasStarted else sleep(1))

        def shutdown():
            global hasStarted; hadStarted = True

            os.system('sudo shutdown -h now')

        gpioManager('active', 1)
        sleep(0.5)
        gpioManager('listening', 1)
        sleep(0.5)
        gpioManager('processing', 1) 
        sleep(0.5)
        gpioManager('speaking', 1)
        sleep(1)        
        gpioManager('speaking', 0)
        sleep(0.5)
        gpioManager('listening', 0)
    #ENDIF

    print('ADJUSTING FOR AMIENBT')
    with sr.Microphone() as source: 
        sr.Recognizer().adjust_for_ambient_noise(source) # we only need to calibrate once, before we start listening

    if '_PYIBoot_SPLASH' in os.environ:# and importlib.util.find_spec("pyi_splash"):
        from pyi_splash import close, update_text  # type: ignore
        update_text('UI Loaded...')
        close()

    gpioManager('processing', 0)
    print('\a'); sleep(1); print('\a')

def gpioManager(pin, state):
    if isOn_RPi == True: 
        if not pin:
            GPIO.output(gpio_loc[pin], state)

def backgroundListening():
    # obtain audio from the microphone
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print(': ')
        gpioManager('listening', 1)

        audio = r.listen(source)
        
        gpioManager('listening', 0)
        print('\a')

    gpioManager('processing', 1)

    try:
        speech = str(r.recognize_google(audio)).lower() #converting to str for syntax highlighting
        print(f'> {speech}')
        for phrase in activations:
            if phrase in speech:
                determineResponse(speech.replace(phrase, '').strip())
                backgroundListening()
            else:
                gpioManager('processing', 0)
                backgroundListening()
    except sr.UnknownValueError:
        print('\tGoogle Speech Recognition could not understand audio')
        print('\tThis is likely because you weren\'t talking to ROSA and she tried to listen to speaking/music in the background')
        gpioManager('processing', 0)
        backgroundListening()
    except sr.RequestError as e:
        gpioManager('processing', 0)
        print(f'\tCould not request results from Google Speech Recognition service; Error Context: \'{e}\'')
        print('\tIf the Error Context on the above line is blank, that would be because the `speech_recognition` module\'s error handling classes just return `pass`, ie they ignore all the errors lol')
        print('\tOh well you get what you put in I suppose')

        gpioManager('speaking', 1)
        print(responses['net_err'][prevResponses['net_err']])
        playsound(os.path.join(os.path.dirname(__file__), 'responses/_/monolith.mp3'))
        gpioManager('speaking', 0)

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

    gpioManager('processing', 0)
    respond(typeq)

def respond(typeq):
    gpioManager('speaking', 1)

    if typeq == 'musicq':
        if prevResponses['musicq'] < len(responses['musicq']):
            print(responses['musicq'][prevResponses['musicq']])
            playsound(os.path.join(os.path.dirname(__file__), 'responses/_/monolith.mp3'))
            prevResponses['musicq'] += 1
        else:
            print('music action')
            prevResponses['musicq'] = 0
    elif typeq == 'wikiq':
        if prevResponses['wikiq'] < len(responses['wikiq']):
            print(responses['wikiq'][prevResponses['wikiq']])
            playsound(os.path.join(os.path.dirname(__file__), 'responses/_/monolith.mp3'))
            prevResponses['wikiq'] += 1
        else:
            print('wiki action')
            prevResponses['wikiq'] = 0
    elif typeq == 'homeq':
        print(responses['homeq'][prevResponses['homeq']])
        playsound(os.path.join(os.path.dirname(__file__), 'responses/_/monolith.mp3'))
        if prevResponses['homeq'] < len(responses['homeq']):
            prevResponses['homeq'] += 1
        else:
            prevResponses['homeq'] = 0
    elif typeq == 'deathq':
        if prevResponses['deathq'] < len(responses['deathq']):
            print(responses['deathq'][prevResponses['deathq']])
            playsound(os.path.join(os.path.dirname(__file__), 'responses/_/monolith.mp3'))
            prevResponses['deathq'] += 1
        else:
            print('death action')
            prevResponses['deathq'] = 0
    else:
        print(responses['confusionq'][prevResponses['confusionq']])
        playsound(os.path.join(os.path.dirname(__file__), 'responses/_/monolith.mp3'))
        if prevResponses['confusionq'] < len(responses['confusionq']):
            prevResponses['confusionq'] += 1
        else:
            prevResponses['confusionq'] = 0

    gpioManager('speaking', 0)

def main():
    startup()
    backgroundListening()

#________________________________________________________________________________________________________________________________

if __name__ == '__main__': main()
