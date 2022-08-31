import os
from shutil import copyfileobj

import PyQt5.QtWidgets as qt
from PyQt5.QtGui import QPixmap
from requests import get

#________________________________________________________________________________________________________________________________

app = qt.QApplication([])
window = qt.QWidget()
window.setWindowTitle('ROSA Installer (GUI)')

#________________________________________________________________________________________________________________________________

filesToDownload = [
    'https://github.com/Cornelius-Figgle/ROSA/blob/e2993a9b9145c542e7b4a39eab35f1af2c0c654b/bin/ROSA.exe', 
    'https://github.com/Cornelius-Figgle/ROSA/blob/e2993a9b9145c542e7b4a39eab35f1af2c0c654b/bin/ROSA',
    'https://github.com/Cornelius-Figgle/ROSA/blob/344aed4435f5df357b8ed30255e405293d317f58/gpio.json',
    'https://github.com/Cornelius-Figgle/ROSA/blob/344aed4435f5df357b8ed30255e405293d317f58/bin/README.md'
]

#________________________________________________________________________________________________________________________________

def setupLoading():
    label = qt.QLabel(window)
    pixmap = QPixmap(os.path.join(os.path.dirname(__file__), 'ico/hotpot-ai.png'))
    label.setPixmap(pixmap)

    # Optional, resize window to image size
    window.resize(pixmap.width(),pixmap.height())

    window.show()
    #app.exec()

def download_file(url):
    local_dirname = os.path.join(os.path.dirname(__file__), 'test_dwld')
    local_filename = os.path.join(local_dirname, url.split('/')[-1])

    print(f'creatinf dirs {local_dirname}')

    os.makedirs(local_dirname, exist_ok=True)

    print(f'starting download for {local_filename}')

    with get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            copyfileobj(r.raw, f)

    return local_filename

def main():
    setupLoading()
    for file in filesToDownload: download_file(file)

#________________________________________________________________________________________________________________________________

if __name__ == '__main__': main()
