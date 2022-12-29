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


class Responses:
	activations: list[str] = [
		'rosa', 'browser', 'rosanna', 'frozen', 'roserton', 'rota' 
		# note: misheard words are included as well
		# future: user could append their own via a command ?
	] 
	keys: dict[str, list[str]] = {
		'musicq': ['play', 'music'], 
		'wikiq': ['wikipedia', 'wiki', 'what does', 'lookup', 'def'], 
		'homeq': ['turn', 'on', 'off', 'light'],
		'confusionq': ['france'],
		'deathq': ['shutdown', 'reboot', 'restart', 'yourself', 'kill']
	}
	responses: dict[str, list[str]] = {
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
	prev_responses: dict[str, int] = {
		'musicq': 0,
		'wikiq': 0,
		'homeq': 0,
		'confusionq': 0,
		'deathq': 0,
		'net_err': 0
	}

class Text_Decorations:
	title: str = [
		'          _____                   _______                   _____                    _____          ',
		'         /\    \                 /::\    \                 /\    \                  /\    \         ',
		'        /::\    \               /::::\    \               /::\    \                /::\    \        ',
		'       /::::\    \             /::::::\    \             /::::\    \              /::::\    \       ',
		'      /::::::\    \           /::::::::\    \           /::::::\    \            /::::::\    \      ',
		'     /:::/\:::\    \         /:::/¯¯\:::\    \         /:::/\:::\    \          /:::/\:::\    \     ',
		'    /:::/__\:::\    \       /:::/    \:::\    \       /:::/__\:::\    \        /:::/__\:::\    \    ',
		'   /::::\   \:::\    \     /:::/    / \:::\    \      \:::\   \:::\    \      /::::\   \:::\    \   ',
		'  /::::::\   \:::\    \   /:::/____/   \:::\____\   ___\:::\   \:::\    \    /::::::\   \:::\    \  ',
		' /:::/\:::\   \:::\____\ |:::|    |     |:::|    | /\   \:::\   \:::\    \  /:::/\:::\   \:::\    \ ',
		'/:::/  \:::\   \:::|    ||:::|____|     |:::|    |/::\   \:::\   \:::\____\/:::/  \:::\   \:::\____\\',
		'\::/   |::::\  /:::|____| \:::\    \   /:::/    / \:::\   \:::\   \::/    /\::/    \:::\  /:::/    /',
		' \/____|:::::\/:::/    /   \:::\    \ /:::/    /   \:::\   \:::\   \/____/  \/____/ \:::\/:::/    / ',
		'       |:::::::::/    /     \:::\    /:::/    /     \:::\   \:::\    \               \::::::/    /  ',
		'       |::|\::::/    /       \:::\__/:::/    /       \:::\   \:::\____\               \::::/    /   ',
		'       |::| \::/____/         \::::::::/    /         \:::\  /:::/    /               /:::/    /    ',
		'       |::|  ¯|                \::::::/    /           \:::\/:::/    /               /:::/    /     ',
		'       |::|   |                 \::::/    /             \::::::/    /               /:::/    /      ',
		'       \::|   |                  \::/____/               \::::/    /               /:::/    /       ',
		'        \:|   |                   ¯¯                      \::/    /                \::/    /        ',
		'         \|___|                                            \/____/                  \/____/         '
	]
	symbols: dict[str, str] = {
		'base': '|',
		'input': '| < |',
		'output': '| > |',
		'error': '| ! |'
	}

class Notices:
	unrecognised: str = (
		f'{Text_Decorations.symbols["error"]} Google Speech Recognition could not understand audio\n'
		f'{Text_Decorations.symbols["error"]} This is likely because you weren\'t talking to ROSA and she tried to listen to speaking/music that is in the background\n'
		f'{Text_Decorations.symbols["error"]} Not logged as an error',
	)
	net_err: str = (
		f'{Text_Decorations.symbols["error"]} Could not request results from Google Speech Recognition service'
	)