import sys
import speech_recognition as sr
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtCore import pyqtSlot, QThread, pyqtSignal
import webbrowser

button_style = """
QPushButton {
    background-color: #008CBA;
    color: white;
    padding: 12px 20px;
    border: none;
    border-radius: 6px;
    font-size: 18px;
    cursor: pointer;
    transition: background-color 0.3s, box-shadow 0.3s; /* Added box-shadow transition */
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); /* Subtle box-shadow */
}

QPushButton:hover {
    background-color: #005F7F;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2); /* Slightly elevated on hover */
}

"""

text_edit_style = """
QTextEdit {
    border: 2px solid #008CBA;
    padding: 10px;
    font-size: 16px;
    border-radius: 6px;
    transition: border-color 0.3s; /* Smooth border-color transition */
}

QTextEdit:focus {
    border-color: #005F7F;
}

"""

window_style = """
QMainWindow {
    background-color: #f0f0f0;
    margin: 20px;
    border-radius: 8px;
    border: 1px solid #ccc;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Slightly stronger shadow */
}

"""



class SpeechRecognitionThread(QThread):
    recognition_done = pyqtSignal(str, bool) # Text, isError

    def __init__(self):
        super().__init__()
        self.recognizer = sr.Recognizer()
        self.edge_path = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s"

    def run(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=2)
            audio = self.recognizer.listen(source)
        try:
            result = self.recognizer.recognize_google(audio)
            # Open the recognized text as a URL in Microsoft Edge
            webbrowser.get(self.edge_path).open(result)
            self.recognition_done.emit(f"Opened: {result}", False)
        except Exception as e:
            self.recognition_done.emit(str(e), True)

# Main Speech Application Window
class SpeechApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.speech_thread = SpeechRecognitionThread()
        self.speech_thread.recognition_done.connect(self.on_recognition_done)

    def initUI(self):
        self.setWindowTitle("Speech Recognition App")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet(window_style)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        layout = QVBoxLayout(self.central_widget)

        self.listen_button = QPushButton("Start Listening", self)
        self.listen_button.setStyleSheet(button_style)
        layout.addWidget(self.listen_button)
        self.listen_button.clicked.connect(self.on_listen_click)

        self.text_area = QTextEdit(self)
        self.text_area.setReadOnly(True)
        self.text_area.setStyleSheet(text_edit_style)
        layout.addWidget(self.text_area)

    @pyqtSlot()
    def on_listen_click(self):
        if not self.speech_thread.isRunning():
            self.text_area.setText("Listening...")
            self.speech_thread.start()
        else:
            self.text_area.setText("Recognition already in progress...")

    @pyqtSlot(str, bool)
    def on_recognition_done(self, text, isError):
        if isError:
            self.text_area.setText(f"Error: {text}")
        else:
            self.text_area.setText(f"Recognized: {text}")

def main():
    app = QApplication(sys.argv)
    ex = SpeechApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
