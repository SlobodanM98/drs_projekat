from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal
import time


class kretanje_projektila_vanzemaljaca_thread(QThread):

    gasenje_signal = pyqtSignal()

    def __init__(self, parent=None, projectile=None):
        super().__init__(parent)
        self.projectile = projectile
        self.gasenje = False
        self.gasenje_signal.connect(self.izlaz)

    @pyqtSlot()
    def izlaz(self):
        self.gasenje = True

    def run(self):
        while self.projectile.y() > 0 and self.gasenje is False:
            if self.parent().nivo < 3:
                time.sleep(0.05 - 0.01 * self.parent().nivo)
            else:
                time.sleep(0.02)
            if self.projectile.y() > 750 * self.parent().razmera_visina and self.projectile.y() < 800 * self.parent().razmera_visina:
                self.parent().projektil_vanzemaljaca_kretanje_signal.emit(0)
                break
            else:
                self.parent().projektil_vanzemaljaca_kretanje_signal.emit(1)
