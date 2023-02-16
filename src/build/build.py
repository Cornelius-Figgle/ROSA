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


import argparse
import os
import ntpath
import sys
from typing import NoReturn

import PyInstaller.__main__ as pyinstaller_


class TreeError(FileNotFoundError):
    '''
    Files missing in tree, see `check_tree()` for more info
    '''


def check_tree(work_dir: str, do_installer: bool) -> list:
    build_tree = {
        # note: the prefix of './' has intentionally been left off
        # note: to allow for external paths from `work_dir`

        'main_app' : [
            'src/build/README.md',
            'src/ROSA/responses/',
            'src/ROSA/__init__.py',
            'src/ROSA/foreign_potato_master.py',
            'src/ROSA/main.py',
            'src/ROSA/ROSA.py'
        ],
        'installer_extras' : [
            'src/build/create_shortcut.vbs',
            'src/ROSA_installer/ROSA_installer_gui.py',
            'src/ROSA_installer/ROSA_installer_uac.py'
        ]
    }

    error_list = []
    for path in build_tree['main_app']:
        path_to_check = os.path.join(work_dir, path)
        if (not os.path.exists(path_to_check)
            or not os.access(path, os.X_OK | os.W_OK)):
            
            error_list.append(ntpath.normpath(path_to_check))
    if do_installer:
        for path in build_tree['installer_extras']:
            path_to_check = os.path.join(work_dir, path)
            if (not os.path.exists(path_to_check)
                or not os.access(path, os.X_OK | os.W_OK)):
            
                error_list.append(ntpath.normpath(path_to_check))

    return error_list

def compile_src(work_dir: str, do_installer: bool) -> None:
    windows_main_args = [
        os.path.join(work_dir, 'src\\ROSA\\main.py'),
        '--name', 'ROSA', '--onefile',
        '--noconfirm', '--log-level=WARN', '--clean', '--console',
        #'--hidden-import', 'pyi_splash'
        #'--splash', os.path.join(work_dir, 'docs\\ico\\hotpot-ai.png'),
        '--icon', os.path.join(work_dir, 'docs\\ico\\hotpot-ai.ico'),
        '--distpath', os.path.join(work_dir, 'bin'),
        '--workpath', os.path.join(work_dir, 'build'),
        '--paths', os.path.join(work_dir, '.venv\\Lib\\site-packages'),
        '--add-binary', os.path.join(work_dir, 'src\\ROSA\\responses;.\\responses'),
        '--add-data', os.path.join(work_dir, 'src\\build\\README.md;.\\README.md')
    ]
    windows_installer_uac_args = [
        os.path.join(work_dir, 'src\\ROSA_installer\\ROSA_installer_uac.py'),
        '--name', 'ROSA_installer_uac', '--onefile', '--uac-admin',
        '--noconfirm', '--log-level=WARN', '--clean', '--windowed',
        '--icon', os.path.join(work_dir, 'docs\\ico\\hotpot-ai.ico'),
        '--distpath', os.path.join(work_dir, 'bin'),
        '--workpath', os.path.join(work_dir, 'build'),
        '--paths', os.path.join(work_dir, '.venv\\Lib\\site-packages'),
        '--add-data', os.path.join(work_dir, 'src\\build\\README.md;.\\README.md')
    ]
    windows_installer_main_args = [
        os.path.join(work_dir, 'src\\ROSA_installer\\ROSA_installer_gui.py'),
        '--name', 'ROSA_installer_gui', '--onefile',
        '--noconfirm', '--log-level=WARN', '--clean', '--windowed',
        #'--hidden-import', 'pyi_splash'
        #'--splash', os.path.join(work_dir, 'docs\\ico\\hotpot-ai.png'),
        '--icon', os.path.join(work_dir, 'docs\\ico\\hotpot-ai.ico'),
        '--distpath', os.path.join(work_dir, 'bin'),
        '--workpath', os.path.join(work_dir, 'build'),
        '--paths', os.path.join(work_dir, '.venv\\Lib\\site-packages'),
        '--add-data', os.path.join(work_dir, 'docs\\ico;.\\ico'),
        '--add-data', os.path.join(work_dir, 'src\\build\\create_shortcut.vbs;.\\create_shortcut.vbs'),
        '--add-data', os.path.join(work_dir, 'src\\build\\README.md;.\\README.md'),
        '--add-data', os.path.join(work_dir, 'bin\\ROSA.exe;.\\ROSA.exe'),
        '--add-data', os.path.join(work_dir, 'bin\\ROSA_installer_uac.exe;.\\ROSA_installer_uac.exe')
    ]
    posix_main_args = [
        os.path.join(work_dir, 'src/ROSA/main.py'),
        '--name', 'ROSA', '--onefile',
        '--noconfirm', '--log-level=WARN', '--clean', '--console',
        #'--hidden-import', 'pyi_splash'
        #'--splash', os.path.join(work_dir, 'docs/ico/hotpot-ai.png'),
        '--icon', os.path.join(work_dir, 'docs/ico/hotpot-ai.ico'),
        '--distpath', os.path.join(work_dir, 'bin'),
        '--workpath', os.path.join(work_dir, 'build'),
        '--paths', os.path.join(work_dir, '.venv/Lib/site-packages'),
        '--add-binary', os.path.join(work_dir, 'src/ROSA/responses:./responses'),
        '--add-data', os.path.join(work_dir, 'src/build/README.md:./README.md'),
    ]

    if os.name in ('nt', 'dos'):
        pyinstaller_.run(windows_main_args)
        if do_installer:
            pyinstaller_.run(windows_installer_uac_args)
            pyinstaller_.run(windows_installer_main_args)
    elif os.name in ('posix'):
        pyinstaller_.run(posix_main_args)

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
        help='whether to build to the Windows installer, defaults to `False` (does nothing on *nix )'
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
        tree_state = check_tree(
            work_dir=args.work_dir,
            do_installer=args.installer
        )
        if tree_state:
            raise TreeError(tree_state)

    compile_src(
        work_dir=args.work_dir,
        do_installer=args.installer
    )


if __name__ == '__main__':
    main()