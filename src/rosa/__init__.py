#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# https://github.com/Cornelius-Figgle/ROSA/
# ROBOTICALLY OBNOXIOUS SERVING ASSISTANT

'''
ROBOTICALLY OBNOXIOUS SERVING ASSISTANT - an emotional voice assistant
'''

'''
THIS FILE IS PART OF THE `ROSA` REPO, MAINTAINED AND PRODUCED BY MAX 
HARRISON, AS OF 2023

It may work separately and independently of the main repo, it may not

- Code (c) Max Harrison 2023
- Ideas (c) Callum Blumfield 2023
- Ideas (c) Max Harrison 2023
- Vocals (c) Evie Peacock 2023
- Art (c) Ashe Ceaton 2023

Thanks also to everyone else for support throughout (sorry for the
spam). also thanks to all the internet peoples that helped with this
as well 
'''

# note: view associated GitHub info as well
__version__ = 'v0.8.0'  
__author__ = 'Cornelius-Figgle'
__email__ = 'max@fullimage.net'
__maintainer__ = 'Cornelius-Figgle'
__copyright__ = 'Copyright (c) 2023 Max Harrison'
__license__ = 'MIT'
__status__ = 'Development'
__credits__ = ['Max Harrison', 'Callum Blumfield', 'Evie Peacock', 'Ashe Ceaton']


import os
import sys
from typing import NoReturn

from rosa import main as rs


def main() -> NoReturn:
    '''
    The main function that handles passing or args and return values.
    Also handles the application loop and errors from functions
    '''

    obj = rs.Rosa_()

    try:
        while True:
            try:
                speech = obj.background_listening()
                if speech:  # note: if req asked
                    typeq = obj.determine_response(speech)
                    obj.respond(typeq)
            except rs.dnf:
                ...
    except KeyboardInterrupt:
        if rs.is_on_RPi: 
            rs.do_cleanup()