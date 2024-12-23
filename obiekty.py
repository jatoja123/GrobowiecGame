class ObiektBase:
    def __init__(self, game):
        self.game = game
    def setPos(self, x, y):
        self.x = x
        self.y = y
    def getPos(self):
        return self.x, self.y
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
        _,_,px,py,_,_ = self.game.getPositions()
        self.game.setGraczP(px,py)
        self.game.flow.akcjeLeft = 0
        self.game.flow.addDodatkowyTekst("Kolec. Ouch Ouch.")

class Drzwi(ObiektBase):
    def getZnak(self):
        return '['
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

class Portal(ObiektBase):
    def __init__(self, game):
        super().__init__(game)
        self.drugiPortal = None
    def setDrugiPortal(self, portal):
        self.drugiPortal = portal
    def getZnak(self):
        if not self.drugiPortal:
            return 'O' #Puste pole jeśli nie ma połaczenia
        return '@'
    def canEnter(self):
        return False
    def onEnter(self):
        if not self.drugiPortal:
            return
        x, y = self.drugiPortal.getPos()
        self.game.setGracz(x,y)
        self.game.flow.akcjeLeft = 0
        self.game.flow.addDodatkowyTekst("Portal. *ziuuum*")