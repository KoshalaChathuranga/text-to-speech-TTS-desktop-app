import os
import sys
import pyttsx3
from datetime import datetime
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit, QInputDialog
from PyQt5.uic import loadUi
from PyQt5.QtCore import QTimer

class MainWindow_text(QMainWindow):
    def __init__(self):
        super(MainWindow_text, self).__init__()
        loadUi(r'src\ui\MainWindow.ui', self)
        
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)    
        self.engine.setProperty('volume', 0.9) 
        
        self.current_user_input = None
        self.current_datetime = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        self.Convert_button.clicked.connect(self.convert_textTospeech)
        self.Save_button.clicked.connect(self.save_to_file)
        self.Play_button.clicked.connect(self.read_text)
        self.Pause_button.clicked.connect(self.pause_reading)
        self.Stop_button.clicked.connect(self.stop_reading)
        self.Rewind_button.clicked.connect(self.rewind_reading)
        
        self.is_paused = False

        self.progress_timer = QTimer(self)
        self.progress_timer.timeout.connect(self.update_progress_bar)

    def convert_textTospeech(self):
        self.current_user_input = self.User_input.toPlainText()
        if self.current_user_input in (None, "Start writing or Paste here...!"):
            QMessageBox.warning(self, 'Warning', 'Please enter text to save.')
            return
        else:
            self.get_text_duration()
            self.read_text()

    def read_text(self):
        try:
            self.current_user_input = self.User_input.toPlainText()
            
            if self.is_paused:
                self.engine.resume()
                self.is_paused = False
            else:
                self.progress_timer.start(100)  
                self.engine.say(self.current_user_input)
                self.engine.runAndWait()
                self.progress_timer.stop()  
        except Exception as e:
            QMessageBox.critical(self, 'read_text', f'An error occurred: {str(e)}')

    def pause_reading(self):
        try:
            self.engine.pause()
            self.is_paused = True
        except Exception as e:
            QMessageBox.critical(self, 'pause_reading', f'An error occurred: {str(e)}')

    def stop_reading(self):
        try:
            self.engine.stop()
            self.is_paused = False
            self.progressBar.setValue(0)  # Reset progress bar value
        except Exception as e:
            QMessageBox.critical(self, 'stop_reading', f'An error occurred: {str(e)}')

    def rewind_reading(self):
        try:
            # Restart reading from the beginning
            self.engine.stop()
            self.is_paused = False
            self.progressBar.setValue(0.0)  # Reset progress bar value
            self.read_text()
        except Exception as e:
            QMessageBox.critical(self, 'rewind_reading', f'An error occurred: {str(e)}')

    def get_text_duration(self):
        try:
            words = self.current_user_input.split()
            speech_rate = 150
            duration_seconds = len(words) / (speech_rate / 60)
            print("Estimated duration:", duration_seconds, "seconds")
            self.Duration.setText(str(duration_seconds))
        except Exception as e:
            QMessageBox.critical(self, 'get_text_duration', f'An error occurred: {str(e)}')
        
    def save_to_file(self):
        try:
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
        except Exception as e:
            QMessageBox.critical(self, 'save_to_file', f'An error occurred: {str(e)}')

    def update_progress_bar(self):
        try:
            progress = self.engine.getProperty('rate') * self.engine.getProperty('volume')
            progress = int(progress)

            self.progressBar.setValue(progress)
        except Exception as e:
            QMessageBox.critical(self, 'update_progress_bar', f'An error occurred: {str(e)}')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow_text()
    window.show()
    sys.exit(app.exec_())
