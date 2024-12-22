class ObiektBase:
    def __init__(self, game):
        self.game = game
    def setPos(self, x, y):
        self.x = x
        self.y = y
    def getZnak(self):
        return '!'
    def canEnter(self):
        return True
    def onEnter(self):
        pass
    def onStart(self):
        pass

class Sciana(ObiektBase):
    def getZnak(self):
        x = self.x
        y = self.y
        if x%2==1 and y%2==0:
            return '-'
        elif x%2==0 and y%2==1:
            return '|'
        else:
            return '+'
    def canEnter(self):
        return False

class PustaSciana(ObiektBase):
    def getZnak(self):
        return '.'
    def canEnter(self):
        return True

class PustePole(ObiektBase):
    def __init__(self, game, czyStart, czyKoniec):
        super().__init__(game)
        self.czyStart = czyStart
        self.czyKoniec = czyKoniec

    def getStartKoniec(self):
        return (self.czyStart, self.czyKoniec)

    def getZnak(self):
        if self.czyStart:
            return 'X'
        elif self.czyKoniec:
            return '$'
        else:
            return '0'
    
    def canEnter(self):
        return True

class Kolec(ObiektBase):
    def getZnak(self):
        return '^'
    def canEnter(self):
        return False
    def onEnter(self):
        _,_,x,y,_,_ = self.game.getPositions()
        print(x,y)
        self.game.setGracz(x,y)
        self.game.flow.akcjeLeft = 0
        self.game.flow.addDodatkowyTekst("Kolec. AŁ.")

class Drzwi(ObiektBase):
    def getZnak(self):
        return '∏'
    def canEnter(self):
        return True
    def onEnter(self):
        self.game.flow.akcjeLeft = 0
        self.game.flow.addDodatkowyTekst("Otwierasz drzwi.")
        
class Bagno(ObiektBase):
    def getZnak(self):
        return '#'
    def canEnter(self):
        return True
    def onStart(self):
        self.game.flow.addDodatkowyTekst("Stoisz na bagnie.")
        self.game.flow.akcjeLeft /= 2

