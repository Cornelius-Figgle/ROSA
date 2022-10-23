#!T:/projects/ROSA/rosa-env/Scripts/python.exe

#https://github.com/Cornelius-Figgle/ROSA

#ROBOTICALLY OBNOXIOUS SERVING ASSISTANT

import json
import os
import sys
from time import sleep

import pygame.mixer as mixer
import speech_recognition as sr
import wikipedia as wiki

try: 
	import RPi.GPIO as GPIO  # type: ignore
	isOn_RPi = True
except ImportError:
	isOn_RPi = False

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
prevResponses = {
	'musicq': 0,
	'wikiq': 0,
	'homeq': 0,
	'confusionq': 0,
	'deathq': 0,
	'net_err': 0
}

#________________________________________________________________________________________________________________________________

def startup() -> None:
	global gpio_loc

	print('\a')
	
	if isOn_RPi == True: 

		GPIO.setmode(GPIO.BCM)
		
		GPIO.cleanup()

		with open(os.path.join(file_base_path, 'gpio.json'), 'r') as j: #hm may work
			gpio_loc = json.loads(j.read())
	
		GPIO.setup(gpio_loc['active'], GPIO.OUT)
		GPIO.setup(gpio_loc['listening'], GPIO.OUT)
		GPIO.setup(gpio_loc['processing'], GPIO.OUT)
		GPIO.setup(gpio_loc['speaking'], GPIO.OUT)

		hasStarted = False
		GPIO.setup(gpio_loc['shutdown'], GPIO.IN, pull_up_down = GPIO.PUD_UP)
		GPIO.add_event_detect(gpio_loc['shutdown'], GPIO.FALLING, callback = lambda channel: shutdown() if not hasStarted else sleep(1))

		def shutdown() -> None:
			global hasStarted; hadStarted = True

			GPIO.cleanup()
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

	print('ADJUSTING FOR AMBIENT')
	with sr.Microphone() as source: 
		sr.Recognizer().adjust_for_ambient_noise(source) # we only need to calibrate once, before we start listening

	mixer.init()

	if '_PYIBoot_SPLASH' in os.environ:# and importlib.util.find_spec('pyi_splash'):
		from pyi_splash import close, update_text  # type: ignore
		update_text('UI Loaded...')
		close()

	gpioManager('processing', 0)
	os.system('cls' if os.name in ('nt', 'dos') else 'clear')
	print('\a'); sleep(1); print('\a')

def gpioManager(pin: str, state: int) -> None:
	if isOn_RPi is not False: 
		if state == 1: GPIO.output(gpio_loc[pin], GPIO.HIGH)
		elif state == 0: GPIO.output(gpio_loc[pin], GPIO.LOW)

def backgroundListening() -> None:
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
		mixer.music.load(os.path.join(file_base_path, 'responses/net_err/net_err_0.mp3')); mixer.music.play()
		while mixer.music.get_busy(): continue
		gpioManager('speaking', 0)

		backgroundListening()
	except KeyboardInterrupt:
		GPIO.cleanup()

def determineResponse(query: str) -> None:
	def musicq(q) -> str | None:
		for key in keys['musicq']:
			if key in q:
				return 'musicq'
	def wikiq(q) -> str | None:
		for key in keys['wikiq']:
			if key in q:
				return 'wikiq'
	def homeq(q) -> str | None:
		for key in keys['homeq']:
			if key in q:
				return 'homeq'
	def deathq(q) -> str | None:
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
	respond(typeq, query)

def respond(typeq: str, query: str) -> None:
	gpioManager('speaking', 1)

	if typeq == 'musicq':
		print(responses['musicq'][prevResponses['musicq']])
		mixer.music.load(os.path.join(file_base_path, f'responses/musicq/musicq_{prevResponses["musicq"]}.mp3')); mixer.music.play()
		while mixer.music.get_busy(): continue
		if prevResponses['musicq'] < len(responses['musicq']):
			prevResponses['musicq'] += 1
		else:
			prevResponses['musicq'] = 0
	elif typeq == 'wikiq':
		print(responses['wikiq'][prevResponses['wikiq']])
		mixer.music.load(os.path.join(file_base_path, f'responses/wikiq/wikiq_{prevResponses["wikiq"]}.mp3')); mixer.music.play()
		while mixer.music.get_busy(): continue
		if prevResponses['wikiq'] < len(responses['wikiq']):
			prevResponses['wikiq'] += 1
		else:
			prevResponses['wikiq'] = 0

			try: print(f'\t{wiki.summary(query)}')
			except wiki.DisambiguationError: 
				try: print(f'\t{wiki.summary(wiki.suggest(query))}')
				except wiki.DisambiguationError: pass #error logginf
	elif typeq == 'homeq':
		print(responses['homeq'][prevResponses['homeq']])
		mixer.music.load(os.path.join(file_base_path, f'responses/homeq/homeq_{prevResponses["homeq"]}.mp3')); mixer.music.play()
		while mixer.music.get_busy(): continue
		if prevResponses['homeq'] < len(responses['homeq']):
			prevResponses['homeq'] += 1
		else:
			prevResponses['homeq'] = 0
	elif typeq == 'deathq':
		if prevResponses['deathq'] < len(responses['deathq']):
			print(responses['deathq'][prevResponses['deathq']])
			mixer.music.load(os.path.join(file_base_path, f'responses/deathq/deathq_{prevResponses["deathq"]}.mp3')); mixer.music.play()
			while mixer.music.get_busy(): continue
			prevResponses['deathq'] += 1
		else:
			if os.name == 'nt': sys.exit(0) #os.system('shutdown /p')
			elif os.name == 'posix': os.system('sudo shutdown -h now')
			prevResponses['deathq'] = 0
	else:
		print(responses['confusionq'][prevResponses['confusionq']])
		mixer.music.load(os.path.join(file_base_path, f'responses/confusionq/confusionq_{prevResponses["confusionq"]}.mp3')); mixer.music.play()
		while mixer.music.get_busy(): continue
		if prevResponses['confusionq'] < len(responses['confusionq']):
			prevResponses['confusionq'] += 1
		else:
			prevResponses['confusionq'] = 0

	gpioManager('speaking', 0)

def main() -> None:
	startup()
	backgroundListening()

#________________________________________________________________________________________________________________________________

if __name__ == '__main__': main()
