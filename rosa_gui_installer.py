import os

import PyQt5.QtWidgets as qt

#________________________________________________________________________________________________________________________________

app = qt.QApplication([])

#________________________________________________________________________________________________________________________________

def main():
    print(os.name)
    window = qt.QWidget()
    layout = qt.QVBoxLayout()
    layout.addWidget(qt.QPushButton('Top'))
    layout.addWidget(qt.QPushButton('Bottom'))
    window.setLayout(layout)
    window.show()
    app.exec()

if __name__ == '__main__': main()
