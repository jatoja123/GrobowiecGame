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
    def __init__(self, game, twarda = False):
        super().__init__(game)
        self.zburzone = False
        self.twarda = twarda
    def getZnak(self):
        if self.zburzone:
            return ','
        x = self.x
        y = self.y
        if x%2==1 and y%2==0:
            return '=' if self.twarda else '-'
        elif x%2==0 and y%2==1:
            return 'I' if self.twarda else '|'
        else:
            return '+'
    def canEnter(self):
        if self.twarda:
            return False
        if self.zburzone:
            return True
        wyburza = self.game.tryWyburzanie()
        if wyburza:
            self.zburzone = True
            self.game.flow.addDodatkowyTekst("Bum!\n")
            return True
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
        self.game.zabij()
        self.game.flow.addDodatkowyTekst("Kolec. Ouch Ouch.\n")

class Drzwi(ObiektBase):
    def getZnak(self):
        return '['
    def canEnter(self):
        return True
    def onEnter(self):
        self.game.flow.setAkcjeLeft(0)
        self.game.flow.addDodatkowyTekst("Otwierasz drzwi.\n")
        
class Bagno(ObiektBase):
    def getZnak(self):
        return '#'
    def canEnter(self):
        return True
    def onStart(self):
        self.game.flow.addDodatkowyTekst("Stoisz na bagnie.\n")
        self.game.flow.setAkcjeLeft(self.game.flow.getAkcjeLeft/2)

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
        self.game.flow.setAkcjeLeft(0)
        self.game.flow.addDodatkowyTekst("Portal. *ziuuum*\n")

class Pulapka(ObiektBase):
    def __init__(self, game):
        super().__init__(game)
        self.odkryte = False
    def getZnak(self):
        if self.odkryte:
            return '%'
        return 'O'
    def canEnter(self):
        return True
    def onStart(self):
        self.game.zabij(False)
        self.game.flow.addDodatkowyTekst("Wpadles w pulapke. Ouch Ouch.\n")
        self.odkryte = True

class TajnePrzejscie(ObiektBase):
    def __init__(self, game):
        super().__init__(game)
        self.odkryte = False
    def getZnak(self):
        if self.odkryte:
            return '('
        return '|'
    def onEnter(self):
        self.odkryte = True
    def canEnter(self):
        return True

class CzasowePrzejscie(ObiektBase):
    def __init__(self, game, otwarteNaParzyste):
        super().__init__(game)
        self.otwarteNaParzyste = otwarteNaParzyste
    def getZnak(self):
        if self.otwarteNaParzyste:
            return '{'
        return '}'
    def onEnter(self):
        czyOk = self.canEnter()
        if not czyOk:
            self.game.flow.addDodatkowyTekst("Nie mozesz teraz przejsc...\n")
    def canEnter(self):
        ktoryRuch = self.game.flow.getIleRuchow()
        if (self.otwarteNaParzyste and ktoryRuch%2==0) or (not self.otwarteNaParzyste and ktoryRuch%2==1):
            return True
        return False
    
class Prezent(ObiektBase):
    def __init__(self, game, rodzaj):
        super().__init__(game)
        self.odkryte = False
        self.rodzaj = rodzaj
    def getZnak(self):
        if self.odkryte:
            return 'O'
        return '*'
    def canEnter(self):
        return True
    def onEnter(self):
        self.odkryte = True
        akcje = self.game.flow.getAkcje()
        for akcja in akcje:
            if akcja.znakUzycia == self.rodzaj:
                akcja.dodajUzycie()
                self.game.flow.addDodatkowyTekst(f"Znalazles prezent! ({self.rodzaj})\n")
                break
        self.game.flow.setAkcje(akcje)

class KrzyweZwierciadlo(ObiektBase):
    usuniecia = 3 #default
    def getZnak(self):
        return '\\'
    def onEnter(self):
        self.game.usunLosowoOdkryte(KrzyweZwierciadlo.usuniecia)
        self.game.flow.addDodatkowyTekst(f"Uhh... Zapomnialem cos? ({KrzyweZwierciadlo.usuniecia})\n")
    def canEnter(self):
        return True