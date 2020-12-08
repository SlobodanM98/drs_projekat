from PyQt5.QtWidgets import QWidget, QApplication
from Models.Window import Window
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())
