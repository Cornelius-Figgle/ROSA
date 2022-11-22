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
__credits__ = ['Max Harrison', 'Callum Blumfield', 'Evie Peacock']


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
    GitHub, then realised I can pkg them into the exe with pyinstaller
    
    # source: https://python.plainenglish.io/packaging-data-files-to-pyinstaller-binaries-6ed63aa20538

    So anyway, have fun on Windows,

        - Max, learning to be a dev
    '''

    sys.exit(0)


class license_agree(qt.QWizardPage): 
    '''
    A `PyQt5.QtWidgets.QWizardPage` instance

    Presents the license to the user for them to agree to
    '''

    def __init__(self, parent=None) -> None:
        super(license_agree, self).__init__(parent)

        licenseLayout = qt.QGridLayout()
        titleLabel = qt.QLabel('End User License Agreement')
        licenseText = qt.QLabel(
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
        agreeCb = qt.QLabel('By proceeding, you are agreeing to this' \
            ' license and its terms')

        licenseBox = qt.QScrollArea()
        licenseBox.setVerticalScrollBarPolicy(QtCore.ScrollBarAsNeeded)
        licenseBox.setHorizontalScrollBarPolicy(QtCore.ScrollBarAsNeeded)
        licenseBox.setWidgetResizable(True)
        licenseBox.setWidget(licenseText)

        licenseLayout.addWidget(titleLabel, 0, 0, 1, 2)
        licenseLayout.addWidget(licenseBox, 1, 0, 2, 2)
        licenseLayout.addWidget(qt.QLabel(''), 3, 0)
        licenseLayout.addWidget(agreeCb, 4, 0, 1, 2)

        self.setLayout(licenseLayout)

class user_config(qt.QWizardPage):
    '''
    A `PyQt5.QtWidgets.QWizardPage` instance

    Holds checkboxes/input boxes to save config values
    '''

    def __init__(self, parent=None) -> None:
        super(user_config, self).__init__(parent)

        configLayout = qt.QGridLayout()
        shell = Dispatch('WScript.Shell')

        global install_configs; install_configs = {}

        install_configs['programPath'] = os.path.expandvars('%ProgramFiles%')
        install_configs['startPath'] = shell.SpecialFolders('Programs') #os.path.expandvars('%AppData%\Microsoft\Windows\Start Menu'))
        install_configs['deskPath'] = shell.SpecialFolders('Desktop') #os.path.expanduser('~\Desktop'))

        dirButton = qt.QPushButton('Install Path: ')
        dirButton.clicked.connect(lambda: self.chooseDir(dirLabel, dirButton, 'programPath', 'Install Path: '))
        dirLabel = qt.QLineEdit(install_configs['programPath']) #https://docs.python.org/3/library/os.path.html#os.path.expandvars
        self.validateType(dirLabel, dirButton, 'programPath', 'Program Files Path: ')
        dirLabel.textChanged.connect(lambda: self.validateType(dirLabel, dirButton, 'programPath', 'Install Path: '))

        cb1 = qt.QCheckBox('Add shortcut to Start Menu')
        cb1.setChecked(True)
        cb1Button = qt.QPushButton('Start Menu Path: ')
        cb1Button.clicked.connect(lambda: self.chooseDir(cb1Label, cb1Button, 'startPath', 'Start Menu Path: '))
        cb1Label = qt.QLineEdit(install_configs['startPath'])
        self.validateType(cb1Label, cb1Button, 'startPath', 'Start Menu Path: ')
        cb1Label.textChanged.connect(lambda: self.validateType( cb1Label, cb1Button, 'startPath', 'Start Menu Path: '))
        cb1.stateChanged.connect(lambda: self.saveCheckStatus(cb1, 'startShortcut'))

        cb2 = qt.QCheckBox('Add shortcut to Desktop')
        cb2.setChecked(False)
        cb2Button = qt.QPushButton('Desktop Path: ')
        cb2Button.clicked.connect(lambda: self.chooseDir(cb2Label, cb2Button, 'deskPath', 'Desktop Path: '))
        cb2Label = qt.QLineEdit(install_configs['deskPath'])
        self.validateType(cb2Label, cb2Button, 'deskPath', 'Desktop Path: ')
        cb2Label.textChanged.connect(lambda: self.validateType(cb2Label, cb2Button, 'deskPath', 'Desktop Path: '))
        cb2.stateChanged.connect(lambda: self.saveCheckStatus(cb1, 'startShortcut'))

        configLayout.addWidget(dirButton, 0, 0)
        configLayout.addWidget(dirLabel, 0, 1)

        configLayout.addWidget(qt.QLabel(''), 1, 0)

        configLayout.addWidget(cb1, 2, 0)
        configLayout.addWidget(cb1Button, 3, 0)
        configLayout.addWidget(cb1Label, 3, 1)

        configLayout.addWidget(qt.QLabel(''), 4, 0)

        configLayout.addWidget(cb2, 5, 0)
        configLayout.addWidget(cb2Button, 6, 0)
        configLayout.addWidget(cb2Label, 6, 1)

        self.setLayout(configLayout)

    def pathIsGood(self, path: str) -> str | None: return path if path and os.path.exists(path) and os.access(path, os.X_OK | os.W_OK) else None

    def validateType(self, label, display, config, revert) -> bool: 
        global install_configs

        try:
            install_configs['startShortcut'] = True if self.cb1.isChecked() else False
            install_configs['deskShortcut'] = True if self.cb2.isChecked() else False
        except NameError: pass #intelligent cod3
        except AttributeError: pass #big bran m0ve

        path = label.text()
        path = self.pathIsGood(path)
        if not path:
            display.setText(f'Invalid \'{config}\'')

            display.setStyleSheet('background-color : red')
            #f = wizard.button(qt.QWizard.WizardButton.NextButton).font() ; f.setStrikeOut(True) ; wizard.button(qt.QWizard.WizardButton.NextButton).setFont(f)
            f = label.font() ; f.setStrikeOut(True) ; label.setFont(f)

            return False
        else:
            install_configs[config] = path
            display.setText(revert)

            display.setStyleSheet('background-color : lightgrey')
            #f = wizard.button(qt.QWizard.WizardButton.NextButton).font() ; f.setStrikeOut(False) ; wizard.button(qt.QWizard.WizardButton.NextButton).setFont(f)
            f = label.font() ; f.setStrikeOut(False) ; label.setFont(f)

            return True        

    def chooseDir(self, label, display, config, revert) -> None: 
        path = qt.QFileDialog.getExistingDirectory('Select Dir')
        if self.pathIsGood(path): 
            label.setText(path) 
            self.validateType(label, display, config, revert)

    def saveCheckStatus(self, cb: qt.QCheckBox, config) -> None:
        global install_configs
        install_configs[config] = True if cb.isChecked() else False
        print(f'CheckBox \'{cb}\' Toggled')

class install_ROSA(qt.QWizardPage): 
    def __init__(self, parent=None) -> None:
        super(install_ROSA, self).__init__(parent)

        installLayout = qt.QGridLayout()

        label = qt.QLabel() #https://stackoverflow.com/a/40294286/19860022
        pixmap = QPixmap(os.path.join(file_base_path, './ico/hotpot-ai.png'))
        label.setPixmap(pixmap)

        self.infoLabel = qt.QLabel(' ')
        self.infoLabel.setWordWrap(True)

        #display text to right of imag
        self.bar = qt.QProgressBar()

        installLayout.addWidget(label, 0, 0)
        installLayout.addWidget(self.infoLabel, 0, 1)
        installLayout.addWidget(self.bar, 1, 0, 1, 2)

        self.setLayout(installLayout)

        self.downloaded_files = {}

    def initializePage(self) -> None:
        print(install_configs)

        fred = Thread(target=self.threadProcesses) #so can dwld whilst display imag
        fred.start()

    def threadProcesses(self) -> None:
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
            [f'"{self.downloaded_files["adm"]}"', f'"{os.path.join(file_base_path, "install_configs.pickle")}"', f'"{os.path.join(file_base_path, "downloaded_files.pickle")}"'], 
            shell=True, check=True, 
            capture_output=True, text=True
        ))

        self.make_shortcut(os.path.join(install_configs['programPath'], 'ROSA', os.path.basename(self.downloaded_files['bin'])), os.path.join(install_configs['startPath'], 'ROSA'))
        self.make_shortcut(os.path.join(install_configs['programPath'], 'ROSA', os.path.basename(self.downloaded_files['readme'])), os.path.join(install_configs['startPath'], 'ROSA'))
        self.make_shortcut(os.path.join(install_configs['programPath'], 'ROSA', os.path.basename(self.downloaded_files['bin'])), install_configs['deskPath'])

        print('install complete!')
        self.infoLabel.setText('install complete!') 

    def make_shortcut(self, source, dest_dir, dest_name=None) -> None:
        '''
        Make shortcut of `source` path to file in `dest_dir` target folder
        If `dest_name` is None, will use `source`'s filename
        '''

        # process user input
        if dest_name is None:
            dest_name = os.path.basename(source)
        dest_path = os.path.join(dest_dir, Path(dest_name).stem) + '.lnk'

        if not os.path.exists(dest_dir):
            print(f'creating dirs "{dest_dir}"')
            self.infoLabel.setText(f'creating dirs "{dest_dir}"')

            os.makedirs(dest_dir, exist_ok=True)

        print(f'creating shortcut at "{dest_path}"')
        self.infoLabel.setText(f'creating shortcut at "{dest_path}"')

        os.system(f'{self.downloaded_files["bat"]} "{source}" "{dest_path}" "{self.downloaded_files["ico"]}" "ROBOTICALLY OBNOXIOUS SERVING ASSISTANT - An emotional smart assistant that doesnt listen to you"')
        
        print(f'{source}\n-->\n{dest_path}') # print status
        self.infoLabel.setText(f'{source}\n-->\n{dest_path}')

        print(f'created shortcut at "{dest_path}"')
        self.infoLabel.setText(f'created shortcut at "{dest_path}"')


class main(qt.QWizard):
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
