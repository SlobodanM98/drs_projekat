from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal
import time


class kretanje_projektila_thread(QThread):

    gasenje_signal = pyqtSignal()

    def __init__(self, parent=None, projectile=None, index=None):
        super().__init__(parent)
        self.projectile = projectile
        self.index = index
        self.gasenje = False
        self.gasenje_signal.connect(self.izlaz)

    @pyqtSlot()
    def izlaz(self):
        self.gasenje = True

    def run(self):
        while self.projectile.y() > 0 and self.gasenje is False:
            time.sleep(0.03)
            if self.projectile.y() < 100 * self.parent().razmera_visina and self.projectile.y() > 0:
                self.parent().projektil_kretanje_signal.emit([0, self.index])
                break
            else:
                self.parent().projektil_kretanje_signal.emit([1, self.index])
