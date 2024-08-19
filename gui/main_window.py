from PyQt5.QtWidgets import (QMainWindow, QVBoxLayout, QPushButton, QTextEdit, 
                             QFileDialog, QWidget, QListWidget, QHBoxLayout, 
                             QApplication)
from PyQt5.QtCore import QThread, pyqtSignal
from utils.transcriber import Transcriber

class TranscriptionThread(QThread):
    transcription_done = pyqtSignal(str, str)

    def __init__(self, transcriber, audio_files):
        super().__init__()
        self.transcriber = transcriber
        self.audio_files = audio_files

    def run(self):
        for file in self.audio_files:
            transcription = self.transcriber.transcribe(file)
            self.transcription_done.emit(file, transcription)

class MainWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.transcriber = Transcriber(config['OPENAI_API_KEY'])
        self.audio_files = []
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Audio Transcriber')
        self.setGeometry(100, 100, 800, 600)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        # File selection
        file_layout = QHBoxLayout()
        self.select_button = QPushButton('Select Audio File(s)')
        self.select_button.clicked.connect(self.select_audio_files)
        file_layout.addWidget(self.select_button)
        
        self.file_list = QListWidget()
        file_layout.addWidget(self.file_list)
        
        layout.addLayout(file_layout)

        # Transcribe button
        self.transcribe_button = QPushButton('Transcribe')
        self.transcribe_button.clicked.connect(self.transcribe_audio)
        self.transcribe_button.setEnabled(False)
        layout.addWidget(self.transcribe_button)

        # Text area
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

        # Copy and Clear buttons
        button_layout = QHBoxLayout()
        self.copy_button = QPushButton('Copy Text')
        self.copy_button.clicked.connect(self.copy_text)
        button_layout.addWidget(self.copy_button)

        self.clear_button = QPushButton('Clear Text')
        self.clear_button.clicked.connect(self.clear_text)
        button_layout.addWidget(self.clear_button)

        layout.addLayout(button_layout)

        central_widget.setLayout(layout)

    def select_audio_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Audio File(s)", "", "Audio Files (*.mp3 *.wav *.ogg)")
        if files:
            self.audio_files.extend(files)
            self.update_file_list()
            self.transcribe_button.setEnabled(True)

    def update_file_list(self):
        self.file_list.clear()
        for file in self.audio_files:
            self.file_list.addItem(file.split('/')[-1])  # Only show filename, not full path

    def transcribe_audio(self):
        self.transcribe_button.setEnabled(False)
        self.text_edit.clear()
        self.text_edit.setText("Transcribing...")

        self.thread = TranscriptionThread(self.transcriber, self.audio_files)
        self.thread.transcription_done.connect(self.update_transcription)
        self.thread.start()

    def update_transcription(self, file, transcription):
        current_text = self.text_edit.toPlainText()
        if current_text == "Transcribing...":
            current_text = ""
        new_text = f"{current_text}\n\nFile: {file.split('/')[-1]}\n{transcription}"
        self.text_edit.setText(new_text.strip())
        if file == self.audio_files[-1]:  # If it's the last file
            self.transcribe_button.setEnabled(True)

    def copy_text(self):
        QApplication.clipboard().setText(self.text_edit.toPlainText())

    def clear_text(self):
        self.text_edit.clear()
        self.audio_files.clear()
        self.update_file_list()
        self.transcribe_button.setEnabled(False)
