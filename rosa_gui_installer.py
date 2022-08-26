import os

import PyQt5.QtWidgets as qt

#________________________________________________________________________________________________________________________________

app = qt.QApplication([])

#________________________________________________________________________________________________________________________________

def selectDir(window):    
    global installDir
    installDir = qt.QFileDialog.getExistingDirectory(window, 'Select Folder')
    print(installDir)

def main():
    print(os.name)
    window = qt.QWidget()
    layout = qt.QVBoxLayout()
    button = qt.QPushButton('Top')
    layout.addWidget(button)
    button.clicked.connect(lambda: selectDir(window))
    window.setLayout(layout)
    
    window.show()
    app.exec()

if __name__ == '__main__': main()
