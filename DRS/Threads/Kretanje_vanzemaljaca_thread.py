from PyQt5.QtCore import Qt, pyqtSlot, QThread, pyqtSignal
import time
import datetime


class kretanje_vanzemaljaca_thread(QThread):

    gasenje_signal = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.gasenje = False
        self.gasenje_signal.connect(self.izlaz)

    @pyqtSlot()
    def izlaz(self):
        self.gasenje = True

    def run(self):
        kretanje_desno = False
        dosao_do_ivice = False
        nova_iteracija = False
        izvrseno_pomeranje_dole = False
        izvrseno_pomeranje_dole_za_vreme = False

        korak = 11

        spavanje_niti = 1
        broj_zivih = len(self.parent().aliensZaPucanje)
        vreme_za_pucanje = 0
        granica_za_pucanje = 1
        nivo = self.parent().nivo


        vreme_izvrsenja = 0.3

        while self.gasenje is False:
            '''if broj_zivih <= 55 and broj_zivih > 45:
                spavanje_niti = 1.3 - vreme_izvrsenja - 0.5
            if broj_zivih <= 45 and broj_zivih > 34:
                spavanje_niti = 1.1 - vreme_izvrsenja
            elif broj_zivih <= 34 and broj_zivih > 23:
                spavanje_niti = 0.9 - vreme_izvrsenja
            elif broj_zivih <= 23 and broj_zivih > 12:
                spavanje_niti = 0.8 - vreme_izvrsenja
            elif broj_zivih <= 12 and broj_zivih > 6:
                granica_za_pucanje = 0.6
                spavanje_niti = 0.6 - vreme_izvrsenja
            elif broj_zivih <= 6 and broj_zivih > 2:
                granica_za_pucanje = 0.4
                spavanje_niti = 0.5 - vreme_izvrsenja
            elif broj_zivih == 2:
                spavanje_niti = 0.4 - vreme_izvrsenja
            elif broj_zivih == 1:
                granica_za_pucanje = 0.5
                spavanje_niti = 0.2 - vreme_izvrsenja'''

            spavanje_niti = 1.3 - vreme_izvrsenja - 0.2 * self.parent().nivo

            if nova_iteracija == False:
                time.sleep(spavanje_niti)
                vreme_za_pucanje += spavanje_niti
            br = 0
            pocetak = datetime.datetime.now()

            indexVanzemaljca = -1
            pronadjenIndexVanzemaljca = False
            brojProlaza = 0

            while(pronadjenIndexVanzemaljca is False and len(self.parent().aliensZaPucanje) != 0):
                indexProvere = (len(self.parent().aliens) - 1)

                if kretanje_desno is False:
                    indexProvere -= 10
                    indexProvere += brojProlaza
                else:
                    indexProvere -= brojProlaza

                for i in range(5):
                    if (self.parent().aliens[indexProvere].postoji):
                        indexVanzemaljca = indexProvere
                        pronadjenIndexVanzemaljca = True
                        break
                    else:
                        indexProvere -= korak

                brojProlaza += 1
            if len(self.parent().aliensZaPucanje) == 0:
                continue

            if nova_iteracija and dosao_do_ivice:
                for i in reversed(self.parent().aliens):
                    self.parent().pomeri_dole_signal.emit(self.parent().aliens.index(i))
                    br += 1
                    if br % 11 == 0:
                        time.sleep(0.05 * spavanje_niti)
            elif kretanje_desno:
                if self.parent().aliens[indexVanzemaljca].x() + 50 * self.parent().razmera_sirina <= 650 * self.parent().razmera_sirina:
                    for i in reversed(self.parent().aliens):
                        self.parent().pomeri_desno_signal.emit(self.parent().aliens.index(i))
                        br += 1
                        if br % 11 == 0:
                            time.sleep(0.05 * spavanje_niti)
                else:
                    kretanje_desno = False
                    dosao_do_ivice = True
            else:
                if self.parent().aliens[indexVanzemaljca].x() - 50 * self.parent().razmera_sirina >= 0:
                    for i in reversed(self.parent().aliens):
                        self.parent().pomeri_levo_signal.emit(self.parent().aliens.index(i))
                        br += 1
                        if br % 11 == 0:
                            time.sleep(0.05 * spavanje_niti)
                else:
                    kretanje_desno = True
                    dosao_do_ivice = True

            if dosao_do_ivice and nova_iteracija:
                izvrseno_pomeranje_dole = True
                izvrseno_pomeranje_dole_za_vreme = True

            if dosao_do_ivice and izvrseno_pomeranje_dole is False:
                nova_iteracija = True
            else:
                nova_iteracija = False
                dosao_do_ivice = False
                izvrseno_pomeranje_dole = False

            dosao_do_dna = False

            if dosao_do_ivice:
                for i in reversed(self.parent().aliens):
                    if i.postoji:
                        if len(self.parent().stitovi) != 0:
                            if i.y() > 560 * self.parent().razmera_visina:
                                dosao_do_dna = True
                                self.parent().game_over_signal.emit(0)
                                break
                        else:
                            if i.y() > 640 * self.parent().razmera_visina:
                                dosao_do_dna = True
                                self.parent().game_over_signal.emit(0)
                                break

            if dosao_do_dna:
                break

            if vreme_za_pucanje >= granica_za_pucanje and self.gasenje is False:
                if self.parent().postoji_projectil_vanzemaljaca is False:
                    self.parent().projektil_vanzemaljaca_kreiranje_signal.emit()
                    vreme_za_pucanje = 0

            broj_zivih = len(self.parent().aliensZaPucanje)

            if izvrseno_pomeranje_dole_za_vreme is False:
                kraj = datetime.datetime.now()
                vreme_izvrsenja = (pocetak - kraj).total_seconds() * -1
            else:
                izvrseno_pomeranje_dole_za_vreme = False
