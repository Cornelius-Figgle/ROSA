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
__version__ = 'Pre-release'  
__author__ = 'Cornelius-Figgle'
__email__ = 'max@fullimage.net'
__maintainer__ = 'Cornelius-Figgle'
__copyright__ = 'Copyright (c) 2023 Max Harrison'
__license__ = 'MIT'
__status__ = 'Development'
__credits__ = ['Max Harrison', 'Callum Blumfield', 'Evie Peacock']


import os
import sys
import argparse
from typing import NoReturn


def check_tree(work_dir: str, do_installer: bool):
    ...

def main() -> NoReturn:
    parser = argparse.ArgumentParser(
        prog=sys.argv[0],
        description='Compiles the ROSA application to binaries for distribution',
        epilog='''For any further assistance, please refer to the documentation:
            https://github.com/Cornelius-Figgle/ROSA/blob/main/docs/BUILDING.md
            https://github.com/Cornelius-Figgle/ROSA/tree/main/src/build
        ''',
        formatter_class=argparse.RawTextHelpFormatter
    )
    
    parser.add_argument(
        '-i', '--installer',
        action='store_true', default=False,
        required=False,
        help='whether to build to the Windows installer, defaults to `False`'
    )
    parser.add_argument(
        '-w', '--work-dir',
        action='store', default=os.getcwd(), type=str,
        required=False,
        metavar='PATH',
        help='the working directory used for compiling. Should be the project root, defaults to `os.getcwd()`'
    )
    parser.add_argument(
        '--no-check',
        action='store_true', default=False,
        required=False,
        help='skips the directory checks before compilation, defaults to `False`. (Not recommended)'
    )

    args = parser.parse_args()
    
    if not args.no_check:
        state = check_tree(
            work_dir=args.work_dir,
            do_installer=args.installer
        )


if __name__ == '__main__':
    main()