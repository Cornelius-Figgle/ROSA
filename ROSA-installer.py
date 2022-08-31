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

def setupLoading():
    label = qt.QLabel(window)
    pixmap = QPixmap(os.path.join(os.path.dirname(__file__), 'ico/hotpot-ai.png'))
    label.setPixmap(pixmap)

    # Optional, resize window to image size
    window.resize(pixmap.width(),pixmap.height())

    window.show()
    app.exec()

def download_file(url):
    local_filename = url.split('/')[-1]
    with get(url, stream=True) as r:
        with open(local_filename, 'wb') as f:
            copyfileobj(r.raw, f)

    return local_filename

def main():
    setupLoading()

#________________________________________________________________________________________________________________________________

if __name__ == '__main__': main()
