import os
import random
import sys

KOKO_MIN = 3
KOKO_MAX = 5
PELAAJA_1 = "x"
PELAAJA_2 = "o"
VAPAA_RUUTU = "_"


class Pelilauta:
    def __init__(self, koko: int):
        self.koko = koko
        self.ruudukko = [[VAPAA_RUUTU for x in range(koko)] for y in range(koko)]

    def piirrä(self):
        """Piirretään pelilauta"""
        print(" _" * self.koko)        
        x = 0
        while x < self.koko:
            y = 0
            while y < self.koko:
                if y < self.koko - 1:
                    print(f"|{self.ruudukko[x][y]}", end="")
                else:
                    print(f"|{self.ruudukko[x][y]}|")
                y += 1
            x += 1

    def voittorivi(self):
        """Tarkistetaan onko voittoa"""
        tarkistuslista = []
        tarkistuslista += [i for i in self.ruudukko] # Rivit
        tarkistuslista += map(list, zip(*self.ruudukko)) # Sarakkeet
        tarkistuslista += [[self.ruudukko[i][i] for i in range(self.koko)]] # Ylävasen -> alaoikea
        tarkistuslista += [[self.ruudukko[self.koko - 1 - i][i] for i in range(self.koko - 1, -1, -1)]] # Alavasen -> yläoikea
        for rivi in tarkistuslista:
            if len(set(rivi)) == 1 and rivi != [VAPAA_RUUTU for x in range(self.koko)]:
                return True


class Peli:
    def __init__(self):
        self.pelaajat = [PELAAJA_1, PELAAJA_2]
        random.shuffle(self.pelaajat)
        self.pelaa()

    def pelaaja(self, vuoro: int):
        """Valitaan pelaaja"""
        if vuoro % 2 == 0:
            pelaaja = self.pelaajat[0]
        else:
            pelaaja = self.pelaajat[1]
        return pelaaja
        
    def otsikko(self):
        """Piirretään otsikko"""
        if os.name == "nt":
            os.system("cls") 
        else:
            os.system("clear")
        print("+------------+")
        print("| Ristinolla |")
        print("+------------+")

    def pelaa(self):
        """Pelilooppi"""

        # Kysytään ruudukon kokoa
        while True:
            self.otsikko()
            try:
                koko = int(input(f"\nValitse ruudukon koko ({KOKO_MIN}-{KOKO_MAX}): "))
            except ValueError:
                input("Syötä vain numeroita! (Jatka painamalla ENTER) ")
                continue

            # Tarkistetaan ruudukon koko
            if koko in range(KOKO_MIN, KOKO_MAX + 1):
                lauta = Pelilauta(koko)
                break
            else:
                input(f"Arvon täytyy olla väliltä {KOKO_MIN}-{KOKO_MAX}! (Jatka painamalla ENTER) ")
                continue
        
        # Kysytään mille riville/sarakkeelle pelataan
        vuoro = 1
        while True:
            self.otsikko()
            lauta.piirrä()
            print(f"\nPelaajan {self.pelaaja(vuoro)} vuoro!\n")
            try:
                rivi = int(input(f"Valitse rivi (1-{lauta.koko}): "))
                sarake = int(input(f"Valitse sarake (1-{lauta.koko}): "))
            except ValueError:
                input("Syötä vain numeroita! (Jatka painamalla ENTER) ")
                continue

            # Tarkistetaan onko paikka kelvollinen
            if 0 < rivi <= lauta.koko and 0 < sarake <= lauta.koko:
                if lauta.ruudukko[rivi - 1][sarake - 1] == VAPAA_RUUTU:
                    lauta.ruudukko[rivi - 1][sarake - 1] = self.pelaaja(vuoro)
                else:
                    input("Paikka on jo varattu! (Jatka painamalla ENTER) ")
                    continue
            else:
                input(f"Arvon täytyy olla väliltä 1-{lauta.koko}! (Jatka painamalla ENTER) ")
                continue
            
            # Näytetään tilanne ja tarkistetaan onko voittoa
            self.otsikko()
            lauta.piirrä()
            if lauta.voittorivi():
                print(f"\nPelaaja {self.pelaaja(vuoro)} on voittanut!\n")
                self.uusi_peli()

            # Jos ruudukko on täynnä eikä voittoa -> tasapeli
            if vuoro == lauta.koko * lauta.koko:
                print("\nTasapeli!\n")
                self.uusi_peli()

            vuoro += 1

    def uusi_peli(self):
        """Ehdotetaan uutta peliä"""
        if input("Pelaa uudestaan? (k/e): ").lower() == "k":
            self.pelaa()
        else:
            sys.exit()


Peli()