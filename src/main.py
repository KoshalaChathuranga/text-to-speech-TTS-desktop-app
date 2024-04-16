import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from generate_image import *
from generate_text import *

class WelcomeWindow(QMainWindow):
    def __init__(self):
        super(WelcomeWindow, self).__init__()
        self.setupUi()

    def setupUi(self):
        loadUi("src/ui/WelcomeWindow.ui", self)
        self.GotoImage_input.clicked.connect(self.goto_GenerateFromImage_window)
        self.GotoText_input.clicked.connect(self.goto_GenerateFromText_window)

    def goto_GenerateFromImage_window(self):
        self.second_window = MainWindowImage() 
        self.second_window.show()
        
    def goto_GenerateFromText_window(self):
        self.Third_window = MainWindow_text() 
        self.Third_window.show()

def main():
    app = QApplication(sys.argv)
    window = WelcomeWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
