import os

import PyQt5.QtWidgets as qt

#________________________________________________________________________________________________________________________________

app = qt.QApplication([])
window = qt.QWidget()
window.setWindowTitle('ROSA Installer (GUI)')

#________________________________________________________________________________________________________________________________

def selectDir():    
    global installDir
    installDir = qt.QFileDialog.getExistingDirectory(window, 'Select Folder')
    print(installDir)

def main():
    layout = qt.QVBoxLayout()

    if os.name == 'nt': 
        selectDirLabel = qt.QLabel('Please select the install directory. This should be in your home folder, which is usally in C:\\users\\username')
    else: 
        selectDirLabel = qt.QLabel('Please select the install directory. This should be in your home folder, which is usally in /home/username')
    layout.addWidget(selectDirLabel)

    selectDirButton = qt.QPushButton('Select Dir')
    selectDirButton.clicked.connect(lambda: selectDir())
    layout.addWidget(selectDirButton)
    
    window.setLayout(layout)
    
    window.show()
    app.exec()

if __name__ == '__main__': main()
