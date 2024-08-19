import sys
from PyQt5.QtWidgets import QApplication
from gui.main_window import MainWindow
from utils.config import load_config

def main():
    config = load_config()
    app = QApplication(sys.argv)
    window = MainWindow(config)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()