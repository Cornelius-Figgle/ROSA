#pyinstaller --distpath "t:\projects\rosa\bin" --workpath "t:\projects\rosa\bin\build" -F -n ROSA-installer_gui --paths "T:\projects\ROSA\rosa-env\Lib\site-packages" --add-data "T:\projects\ROSA\bin\bin;." --add-data "T:\projects\ROSA\ico;ico" --hidden-import pyi_splash --splash "T:\projects\ROSA\ico\hotpot-ai.png" -i "T:\projects\ROSA\ico\hotpot-ai.ico" "T:\projects\ROSA\WIN_ROSA-installer.py"
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
spam). Extra thanks to all the internet peoples that helped with this
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
__credits__ = ['Max Harrison', 'Callum Blumfield', 'Evelyn May Peacocke']


import os
import pickle
import subprocess
import sys
from pathlib import Path
from threading import Thread

import PyQt5.QtWidgets as qt
from PyQt5.QtCore import Qt as QtCore
from PyQt5.QtGui import QPixmap
from win32com.client import Dispatch

# source: https://stackoverflow.com/a/11422350/19860022

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
    GitHub, then realised I can pkg them into the exe with `pyinstaller`
    
    # source: https://python.plainenglish.io/packaging-data-files-to-pyinstaller-binaries-6ed63aa20538

    So anyway, have fun on Windows,

        - Max, learning to be a dev
    '''

    sys.exit(0)


class license_agree(qt.QWizardPage): 
    '''
    A `PyQt5.QtWidgets.QWizardPage` instance

    Presents an MIT license to the user for them to read through
    '''

    def __init__(self, parent=None) -> None:
        super(license_agree, self).__init__(parent)

        license_layout = qt.QGridLayout()
        title_label = qt.QLabel('End User License Agreement')
        license_text = qt.QLabel(
            '''
            MIT License
            
            Copyright (c) 2022 Max

            Permission is hereby granted, free of charge, to any person 
            obtaining a copy of this software and associated documentation 
            files (the "Software"), to deal in the Software without 
            restriction, including without limitation the rights to use, 
            copy, modify, merge, publish, distribute, sublicense, and/or sell
            copies of the Software, and to permit persons to whom the 
            Software is furnished to do so, subject to the following 
            conditions:
            
            The above copyright notice and this permission notice shall be 
            included in all copies or substantial portions of the Software.

            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, 
            EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES 
            OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND 
            NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
            HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
            WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
            OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
            DEALINGS IN THE SOFTWARE.
            '''
        )
        agree_cb = qt.QLabel('By proceeding, you are agreeing to this' \
            ' license and its terms')

        license_box = qt.QScrollArea()
        license_box.setVerticalScrollBarPolicy(QtCore.ScrollBarAsNeeded)
        license_box.setHorizontalScrollBarPolicy(QtCore.ScrollBarAsNeeded)
        license_box.setWidgetResizable(True)
        license_box.setWidget(license_text)

        license_layout.addWidget(title_label, 0, 0, 1, 2)
        license_layout.addWidget(license_box, 1, 0, 2, 2)
        license_layout.addWidget(qt.QLabel(''), 3, 0)
        license_layout.addWidget(agree_cb, 4, 0, 1, 2)

        self.setLayout(license_layout)

class user_config(qt.QWizardPage):
    '''
    A `PyQt5.QtWidgets.QWizardPage` instance

    Holds checkboxes/input boxes to save config values into 
    dict `install_configs`
    '''

    def __init__(self, parent=None) -> None:
        super(user_config, self).__init__(parent)

        config_layout = qt.QGridLayout()
        shell = Dispatch('WScript.Shell')

        global install_configs; install_configs = {}

        install_configs['program_path'] = os.path.expandvars('%ProgramFiles%')
        install_configs['start_path'] = shell.SpecialFolders('Programs') 
        # old: os.path.expandvars('%AppData%\Microsoft\Windows\Start Menu'))
        install_configs['desk_path'] = shell.SpecialFolders('Desktop') 
        # old: os.path.expanduser('~\Desktop'))

        dir_button = qt.QPushButton('Install Path: ')
        dir_button.clicked.connect(lambda: self.choose_dir(
            dir_label, dir_button, 
            'program_path', 'Install Path: '))
        dir_label = qt.QLineEdit(install_configs['program_path']) 
        # source: https://docs.python.org/3/library/os.path.html#os.path.expandvars
        self.validate_type(
            dir_label, dir_button, 
            'program_path', 'Install Path: ')
        dir_label.textChanged.connect(lambda: self.validate_type(
            dir_label, dir_button,
            'program_path', 'Install Path: '))

        cb1 = qt.QCheckBox('Add shortcut to Start Menu')
        cb1.setChecked(True)
        cb1_button = qt.QPushButton('Start Menu Path: ')
        cb1_button.clicked.connect(lambda: self.choose_dir(
            cb1_label, cb1_button, 
            'start_path', 'Start Menu Path: '))
        cb1_label = qt.QLineEdit(install_configs['start_path'])
        self.validate_type(
            cb1_label, cb1_button, 
            'start_path', 'Start Menu Path: ')
        cb1_label.textChanged.connect(lambda: self.validate_type(
            cb1_label, cb1_button, 
            'start_path', 'Start Menu Path: '))
        cb1.stateChanged.connect(lambda: self.save_check_status(
            cb1, 'start_shortcut'))

        cb2 = qt.QCheckBox('Add shortcut to Desktop')
        cb2.setChecked(False)
        cb2_button = qt.QPushButton('Desktop Path: ')
        cb2_button.clicked.connect(lambda: self.choose_dir(
            cb2_label, cb2_button, 
            'desk_path', 'Desktop Path: '))
        cb2_label = qt.QLineEdit(install_configs['desk_path'])
        self.validate_type(
            cb2_label, cb2_button, 
            'desk_path', 'Desktop Path: ')
        cb2_label.textChanged.connect(lambda: self.validate_type(
            cb2_label, cb2_button, 
            'desk_path', 'Desktop Path: '))
        cb2.stateChanged.connect(lambda: self.save_check_status(
            cb2, 'desk_shortcut'))

        config_layout.addWidget(dir_button, 0, 0)
        config_layout.addWidget(dir_label, 0, 1)

        config_layout.addWidget(qt.QLabel(''), 1, 0)

        config_layout.addWidget(cb1, 2, 0)
        config_layout.addWidget(cb1_button, 3, 0)
        config_layout.addWidget(cb1_label, 3, 1)

        config_layout.addWidget(qt.QLabel(''), 4, 0)

        config_layout.addWidget(cb2, 5, 0)
        config_layout.addWidget(cb2_button, 6, 0)
        config_layout.addWidget(cb2_label, 6, 1)

        self.setLayout(config_layout)

    def path_is_good(self, path: str) -> str | None: 
        '''
        Evaluates whether the given `path` is a useable path. Checks 
        whether the variable is `True`, then if it `exists`, then if 
        the script has Execute/Write access

        Returns `path` if it is valid, else will return `None`
        '''

        if (path and os.path.exists(path) 
        and os.access(path, os.X_OK | os.W_OK)):
            return path
        else:
            return None

    def validate_type(
        self, label: qt.QLineEdit, display: qt.QPushButton, 
        config: str, revert: str) -> bool: 

        '''
        Checks the values from `cbx` and that the given paths in 
        `label` are valid. Sets styles for `display` and `label` if 
        invalid paths (`revert` is passed so that the function can 
        reset the text in `display` if a new path is set later). Also 
        sets the values for `config` in `install_configs` if valid
        paths

        Returns `True` if the past from `label` was set to `config`, 
        returns `False` if it was invalid
        '''

        global install_configs

        try:
            # note: program runs this sometimes when loading so we 
            # note: ignore the errors
            install_configs['start_shortcut'] = self.cb1.isChecked()
            print('CheckBox `cb1` Toggled True')
            install_configs['desk_shortcut'] = self.cb2.isChecked()
            print('CheckBox `cb2` Toggled True')
        except NameError: 
            pass  # note: intelligent cod3
        except AttributeError: 
            pass  # note: big bran m0ve

        path = label.text()
        returned_path = self.path_is_good(path)

        if not returned_path:  # note: invalid path
            display.setText(f'Invalid \'{config}\'')

            display.setStyleSheet('background-color : red')
            f = label.font() ; f.setStrikeOut(True) ; label.setFont(f)

            return False
        else:  # note: if path is fine
            install_configs[config] =  returned_path
            display.setText(revert)

            display.setStyleSheet('background-color : lightgrey')
            f = label.font() ; f.setStrikeOut(False) ; label.setFont(f)

            return True        

    def choose_dir(
        self, label: qt.QLineEdit, display: qt.QPushButton, 
        config: str, revert: str) -> None:

        '''
        Starts a `qt.QFileDialog.getExistingDirectory` instance to 
        choose a dir, then calls `validate_type()` with the passed
        values. Basically just a wrapper for `validate_type()` with
        the dir choosing
        '''

        path = qt.QFileDialog.getExistingDirectory('Select Dir')
        if self.path_is_good(path): 
            label.setText(path) 
            self.validate_type(label, display, config, revert)
        

class install_ROSA(qt.QWizardPage): 
    '''
    A `PyQt5.QtWidgets.QWizardPage` instance

    Elaborate loading screen and runs copy scripts to install program
    '''

    def __init__(self, parent=None) -> None:
        super(install_ROSA, self).__init__(parent)

        install_layout = qt.QGridLayout()

        label = qt.QLabel()  # source: https://stackoverflow.com/a/40294286/19860022
        pixmap = QPixmap(os.path.join(file_base_path, './ico/hotpot-ai.png'))
        label.setPixmap(pixmap)

        self.info_label = qt.QLabel(' ')
        self.info_label.setWordWrap(True)

        #display text to right of imag
        self.bar = qt.QProgressBar()

        install_layout.addWidget(label, 0, 0)
        install_layout.addWidget(self.info_label, 0, 1)
        install_layout.addWidget(self.bar, 1, 0, 1, 2)

        self.setLayout(install_layout)

        self.downloaded_files = {}

    def initializePage(self) -> None:
        # note: this is camelCase b/c it is the name defined in 
        # note: the `PyQt5` module so it needs to be the same
        print(install_configs)

        # note: so can dwld whilst display imag
        fred = Thread(target=self.thread_processes) 
        fred.start()

    def thread_processes(self) -> None:
        '''
        Constructs file paths, copies files and creates shortcuts for 
        said files

        Copying is done by `ROSA-installer_uac.exe`, which should be 
        embedded within this file

        Shortcuts are handled by `create_shortcut.bat`, which should 
        be embedded within this file
        '''

        self.downloaded_files['bin'] = os.path.join(file_base_path, 'ROSA.exe')
        self.downloaded_files['adm'] = os.path.join(file_base_path, 'ROSA-installer_uac.exe')
        self.downloaded_files['bat'] = os.path.join(file_base_path, 'create_shortcut.bat')
        self.downloaded_files['readme'] = os.path.join(file_base_path, 'README.md')
        self.downloaded_files['ico'] = os.path.join(file_base_path, 'ico/hotpot-ai.ico')

        with open(os.path.join(file_base_path, 'install_configs.pickle'), 'wb') as file:
            pickle.dump(install_configs, file)
        with open(os.path.join(file_base_path, 'downloaded_files.pickle'), 'wb') as file:
            pickle.dump(self.downloaded_files, file)

        print(subprocess.run(
            [
                f'"{self.downloaded_files["adm"]}"', 
                f'"{os.path.join(file_base_path, "install_configs.pickle")}"', 
                f'"{os.path.join(file_base_path, "downloaded_files.pickle")}"'
            ], 
            shell=True, check=True, 
            capture_output=True, text=True
        ))

        self.make_shortcut(
            os.path.join(
                install_configs['program_path'], 
                'ROSA', 
                os.path.basename(self.downloaded_files['bin'])
            ), 
            os.path.join(
                install_configs['start_path'], 
                'ROSA'  # note: start menu folder
            )
        )
        self.make_shortcut(
            os.path.join(
                install_configs['program_path'], 
                'ROSA', 
                os.path.basename(self.downloaded_files['readme'])
            ), 
            os.path.join(
                install_configs['start_path'], 
                'ROSA'  # note: start menu folder
            )
        )
        self.make_shortcut(
            os.path.join(
                install_configs['program_path'], 
                'ROSA', 
                os.path.basename(self.downloaded_files['bin'])
            ), 
            install_configs['desk_path']  # note: no folder in desktop
        )

        print('install complete!')
        self.info_label.setText('install complete!') 

    def make_shortcut(self, source, dest_dir, dest_name=None) -> None:
        '''
        Make shortcut of `source` path to file in `dest_dir` target folder
        If `dest_name` is None, will use `source`'s filename

        Basically just a wrapper for `create_shortcut.bat`
        '''

        # note: process user input
        if dest_name is None:
            dest_name = os.path.basename(source)
        dest_path = os.path.join(dest_dir, Path(dest_name).stem) + '.lnk'

        if not os.path.exists(dest_dir):
            print(f'creating dirs "{dest_dir}"')
            self.info_label.setText(f'creating dirs "{dest_dir}"')

            os.makedirs(dest_dir, exist_ok=True)

        print(f'creating shortcut at "{dest_path}"')
        self.info_label.setText(f'creating shortcut at "{dest_path}"')

        print(subprocess.run([
            self.downloaded_files["bat"], 
            source, 
            dest_path, 
            self.downloaded_files["ico"], 
            '"ROBOTICALLY OBNOXIOUS SERVING ASSISTANT -' \
                'An emotional smart assistant that doesn\'t listen to you"'
        ]))

        print(f'created shortcut at "{dest_path}"')
        self.info_label.setText(f'created shortcut at "{dest_path}"')


class main(qt.QWizard):
    '''
    A `PyQt5.QtWidgets.QWizard` instance

    Inits the other pages and the Qt application as a whole
    '''

    def __init__(self, parent=None) -> None:
        super(main, self).__init__(parent)

        self.setStyleSheet('QPushButton { background-color: lightgrey }')
        # info: sets CSS button style for all buttons
    
        self.addPage(license_agree())
        self.addPage(user_config())
        self.addPage(install_ROSA())

        self.setWindowTitle('ROSA Installer (GUI)')

if __name__ == '__main__':
    if '_PYIBoot_SPLASH' in os.environ:
            from pyi_splash import close, update_text  # type: ignore
            update_text('UI Loaded...')
            close()

    app = qt.QApplication(sys.argv)
    wizard = main()
    wizard.show()
    sys.exit(app.exec_())
