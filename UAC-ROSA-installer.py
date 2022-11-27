# pyinstaller --distpath "t:\projects\rosa\bin\bin" --workpath "t:\projects\rosa\bin\build" -F -n ROSA-installer_uac --paths "T:\projects\ROSA\rosa-env\Lib\site-packages" --uac-admin --hidden-import pyi_splash --splash "T:\projects\ROSA\ico\hotpot-ai.png" -i "T:\projects\ROSA\ico\hotpot-ai.ico" "T:\projects\ROSA\UAC-ROSA-installer.py"
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
import pickle
import shutil
import sys

if hasattr(sys, '_MEIPASS'):
    # source: https://stackoverflow.com/a/66581062/19860022
    file_base_path = sys._MEIPASS
    # source: https://stackoverflow.com/a/36343459/19860022
else:
    file_base_path = os.path.dirname(__file__)

if os.name != 'nt':
    '''
    Ok so, originally this was intended to be cross-platform. It was 
    hard and confusing and messy. I also realised, *nix users generally 
    install stuff themselves, and my installer is probably incorrect 
    for their specific system anyways.

    I summed this up with:

        'cod3 is way nicer to look at without 6 thousand `if` 
        statements for cross-platform code that doesn't function properly'

    So. `git clone https://GitHub.com/Cornelius-Figgle/ROSA.git` 
    works. I may also add ROSA to package managers en la futuro 
    (especially the RPi one: (`apt` iirc)

    Btw, I was previously using `requests` to download the files from 
    GitHub, then realised I can pkg them into the exe with pyinstaller
    
    # source: https://python.plainenglish.io/packaging-data-files-to-pyinstaller-binaries-6ed63aa20538

    So anyway, have fun on Windows,

        - Max, learning to be a dev
    '''

    sys.exit(0)


def uac_procs(install_configs: dict, downloaded_files: dict) -> None:
    '''
    creates folders and moves the files that need to be moved for
    the ROSA installation. Equivalent to the following commands:

    `mkdir "C:\Program Files\ROSA"`

    `move "%userprofile%\AppData\Local\Temp\_MEI????\ROSA.exe" "C:\Program Files\ROSA\ROSA.exe"`

    `move "%userprofile%\AppData\Local\Temp\_MEI????\README.md" "C:\Program Files\ROSA\README.md"`
    '''

    # shell: mkdir "C:\Program Files\ROSA"
    os.mkdir(
        os.path.join(
            install_configs['program_path'],
            'ROSA'
        )
    )

    # shell: move "%userprofile%\AppData\Local\Temp\_MEI????\ROSA.exe" "C:\Program Files\ROSA\ROSA.exe"
    shutil.move(
        downloaded_files['bin'], 
        os.path.join(
            install_configs['program_path'], 
            'ROSA', 
            os.path.basename(downloaded_files['bin'])
        )
    )

    # shell: move "%userprofile%\AppData\Local\Temp\_MEI????\README.md" "C:\Program Files\ROSA\README.md"
    shutil.move(
        downloaded_files['readme'], 
        os.path.join(
            install_configs['program_path'], 
            'ROSA', 
            os.path.basename(downloaded_files['readme'])
        )
    )

def main(config_pk: str, dwld_pk: str) -> None:
    '''
    main function to handle `pickle` loading from the `cli params`
    '''

    print('starting pickle loads')

    with open(config_pk, 'rb') as file:
        # old: os.path.join(file_base_path, 'install_configs.pickle'), 'rb') as file:
        install_configs = pickle.load(file)
    
    with open(dwld_pk, 'rb') as file: 
        # old: os.path.join(file_base_path, 'downloaded_files.pickle'), 'rb') as file:
        downloaded_files = pickle.load(file)
    
    print('finished pickle loads')

    for i in install_configs:
        print(f'install_configs[{i}] is {install_configs[i]}')
    for i in downloaded_files:
        print(f'downloaded_files[{i}] is {downloaded_files[i]}')

    uac_procs(install_configs, downloaded_files)


if __name__ == '__main__':
    if '_PYIBoot_SPLASH' in os.environ:
        from pyi_splash import close, update_text  # type: ignore
        update_text('UI Loaded...')
        close()

    print('starting UAC script')
    try:  # note: load from cli params
        main(sys.argv[1], sys.argv[2])
    except IndexError:  # note: fallback for files in cur dir
        main(
            os.path.join(
                os.path.dirname(sys.executable), 
                'install_configs.pickle'
            ), 
            os.path.join(
                os.path.dirname(sys.executable), 
                'downloaded_files.pickle'
            )
        )
