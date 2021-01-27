from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal
import time


class sleep_thread(QThread):
    def __init__(self, parent=None):
        super().__init__(parent)

    def run(self):
        time.sleep(2)
        if self.parent().turnir and self.parent().is_game_over:
            self.parent().nova_runda_signal.emit()
        elif self.parent().is_game_over:
            self.parent().povratak_na_pocetak_signal.emit()
        else:
            self.parent().sleep_signal.emit()
