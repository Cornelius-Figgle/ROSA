# 
# -*- coding: UTF-8 -*-

# https://github.com/Cornelius-Figgle/ROSA/
# ROBOTICALLY OBNOXIOUS SERVING ASSISTANT

'''
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


import os
import sys
from typing import NoReturn

from ROSA import ROSA


def main() -> NoReturn:
    '''
    The main function that handles passing or args and return values.
    Also handles the application loop and errors from functions
    '''

    obj = ROSA.ROSA_(
        json_path = os.path.join(
            os.path.dirname(
                sys.executable
            ),
            'gpio.json'
        )
    )
    # note: https://stackoverflow.com/a/74975328/19860022

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


if __name__ == '__main__': 
    main()
