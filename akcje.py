class AkcjaBase:
    znakUzycia = "!"
    def __init__(self, uzycia, kosztAkcji):
        self.uzycia = uzycia
        self.kosztAkcji = kosztAkcji
        pass
    def uzyj(self, game):
        akcje = game.flow.getAkcjeLeft()
        if self.uzycia <= 0 or akcje + 1 < self.kosztAkcji:
            return False
        self.uzycia -= 1
        game.flow.setAkcjeLeft(akcje - self.kosztAkcji + 1)
        return True
    def dodajUzycie(self):
        self.uzycia += 1

class AkcjaMapowanie(AkcjaBase):
    znakUzycia = "m"
    def __init__(self, uzycia, kosztAkcji, zasieg):
        self.zasieg = zasieg
        super().__init__(uzycia, kosztAkcji)
    def uzyj(self, game):
        if super().uzyj(game):
            game.mapuj(self.zasieg, self.uzycia)


class AkcjaKompasowanie(AkcjaBase):
    znakUzycia = "k"
    def uzyj(self, game):
        if super().uzyj(game):
            game.kompasuj(self.uzycia)

class AkcjaBurzenie(AkcjaBase):
    znakUzycia = "b"
    def uzyj(self, game):
        if super().uzyj(game):
            game.addBurzenie(self.uzycia)

class AkcjaSamobojstwo(AkcjaBase):
    znakUzycia = "r"
    def uzyj(self, game):
        if super().uzyj(game):
            game.flow.addDodatkowyTekst(f"Popelniasz samobojstwo.\n")
            game.zabij()
