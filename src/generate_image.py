import os
import sys
import pyttsx3
import pytesseract
from PIL import Image
from PyQt5.QtWidgets import QMainWindow, QApplication, QFileDialog, QMessageBox
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QTimer
from PyQt5.uic import loadUi

class MainWindowImage(QMainWindow):
    def __init__(self):
        super(MainWindowImage, self).__init__()
        loadUi(r"src/ui/SecondWindow.ui", self)
        
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)    
        self.engine.setProperty('volume', 0.9) 
        
        self.open_button.clicked.connect(self.browsefiles)
        self.Convert_button_2.clicked.connect(self.convert_textTospeech)
        
        self.is_paused = False
       

    def browsefiles(self):
        fname, _ = QFileDialog.getOpenFileName(self, 'Open file', r'C:\Users\kosala\Desktop\text-to-speech (TTS) desktop app')
        self.file_path = fname
        
        if self.file_path:
            pixmap = QPixmap(self.file_path).scaled(self.label.size(), aspectRatioMode=True)
            self.label.setPixmap(pixmap)
            self.OCR_result()
    
    def OCR_result(self):
        img = Image.open(self.file_path)
        results = pytesseract.image_to_string(img)
        self.User_input.setPlainText(str(results))
        print(results)
    
    def convert_textTospeech(self):
        self.current_user_input = self.User_input.toPlainText()
        if self.current_user_input in (None, "Start writing or Paste here...!"):
            QMessageBox.warning(self, 'Warning', 'Please enter text to save.')
            return
        else:
            self.read_text()

    def read_text(self):
        try:
            self.current_user_input = self.User_input.toPlainText()
            
            if self.is_paused:
                self.engine.resume()
                self.is_paused = False
            else:
                self.engine.say(self.current_user_input)
                self.engine.runAndWait()  
        except Exception as e:
            QMessageBox.critical(self, 'read_text', f'An error occurred: {str(e)}')
         
def main():
    app = QApplication(sys.argv)
    window = MainWindowImage()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
