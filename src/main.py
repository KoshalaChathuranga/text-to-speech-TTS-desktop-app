import os
import sys
import pyttsx3
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QInputDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import QUrl

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi(r'src\ui\Main Window.ui', self)
        
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)    
        self.engine.setProperty('volume', 0.9) 
        
        self.current_user_input = None
        self.current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        self.Convert_button.clicked.connect(self.print_text)
        self.Save_button.clicked.connect(self.save_to_file)
        
    def print_text(self):
        self.current_user_input = self.User_input.toPlainText()
        
        print(self.current_user_input)
        self.text_to_speech(self.current_user_input)
        
    def text_to_speech(self, text):        
        self.engine.say(text)
        self.engine.runAndWait()
        
    def save_to_file(self):
        self.current_user_input = self.User_input.toPlainText()
        if self.current_user_input in (None, "Start writing or Paste here...!"):
            QMessageBox.warning(self, 'Warning', 'Please enter text to save.')
            return

        suggested_filename = f"{self.current_datetime}.mp3"
        print("suggested_filename: ", suggested_filename)

        filename, _ = QInputDialog.getText(self, 'Save File', 'Enter file name:', QLineEdit.Normal, suggested_filename)
        if not filename:
            return

        output_file = os.path.join("data", f"{filename}.mp3") 
        print("output_file: ", output_file)
        
        self.engine.save_to_file(self.current_user_input, output_file)
        self.engine.runAndWait()

        QMessageBox.information(self, 'Success', f'File saved as {output_file}')

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
