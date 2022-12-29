# pyinstaller --noconfirm --log-level=WARN --clean --distpath ".\bin\bin" --workpath ".\bin\build" --name ROSA --onefile --paths ".\rosa-env\Lib\site-packages" --hidden-import pyi_splash --add-binary ".\responses;.\responses" --splash ".\docs\ico\hotpot-ai.png" --icon ".\docs\ico\hotpot-ai.ico" .\main.py
# pyinstaller --noconfirm --log-level=WARN --clean --distpath "./bin/bin" --workpath "./bin/build" --name ROSA --onefile --paths "./rosa-env/Lib/site-packages" --hidden-import pyi_splash --add-binary "./responses:./responses" --splash "./docs/ico/hotpot-ai.png" --icon "./docs/ico/hotpot-ai.ico" ./main.py
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


import os
import sys
from typing import NoReturn

import ROSA


def main() -> NoReturn:
    '''
    The main function that handles passing or args and return values.
    Also handles the application loop and errors from functions
    '''

    obj_args = {}

    if not hasattr(sys, '_MEIPASS'):
        obj_args['json_path'] = os.path.join(
            os.path.dirname(__file__), 'gpio.json'
        )
    else:
        obj_args['json_path'] = os.path.join(
            os.path.dirname(sys.executable), 'gpio.json'
        )

    obj = ROSA.ROSA_(**obj_args)

    try:
        while True:
            try:
                speech = obj.background_listening()
                if speech:  # note: if req asked
                    typeq = obj.determine_response(speech)
                    obj.respond(typeq, speech)
            except ROSA.dnf:
                ...
    except KeyboardInterrupt:
        if ROSA.is_on_RPi: 
            ROSA.do_cleanup()


if __name__ == '__main__': 
    main()
