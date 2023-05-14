# 
# -*- coding: UTF-8 -*-

# https://github.com/Cornelius-Figgle/ROSA/
# ROBOTICALLY OBNOXIOUS SERVING ASSISTANT

'''
Manages cli args and config files
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


import argparse
import os
import sys


class ConfigsFromArgs():
    def __init__():
        parser = argparse.ArgumentParser(
            description='An emotional smart assistant that doesn\'t listen to you',
            epilog='Please see https://github.com/Cornelius-Figgle/ROSA for more info',

            fromfile_prefix_chars='@'  # info: https://docs.python.org/3/library/argparse.html#fromfile-prefix-chars 
        )

        parser.add_argument('--hide-title', action='store_true')
        
        return parser.parse_args()