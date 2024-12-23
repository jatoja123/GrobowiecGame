class AkcjaBase:
    znakUzycia = "!"
    def __init__(self, uzycia, kosztAkcji):
        self.uzycia = uzycia
        self.kosztAkcji = kosztAkcji
        pass
    def uzyj(self, game):
        akcje = game.flow.getAkcje()
        if self.uzycia <= 0 or akcje < self.kosztAkcji:
            return False
        game.flow.setAkcje(akcje - self.kosztAkcji + 1)
        return True

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
