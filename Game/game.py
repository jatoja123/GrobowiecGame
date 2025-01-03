import random
from Game.obiekty import *

class Game:
    won = False
    flow = None

    def setSizeWH(self, w, h):
        self.w = w # [pól]
        self.h = h # [pól]   
        self.n = 1 + 2 * w
        self.m = 1 + 2 * h

    def setSizeNM(self, n, m):
        self.n = n # [tab]
        self.m = m # [tav]   
        self.w = (self.n - 1)/2
        self.h = (self.m - 1)/2

    def __init__(self, flow, w, h, inputGame, mapType, mapInput=""):
        self.setSizeWH(w,h)
        self.flow = flow

        n = self.n
        m = self.m
        self.pola = [[ObiektBase(self) for x in range(n)] for y in range(m)]
        self.odkryte = [[False for x in range(n)] for y in range(m)]
        # ramka X
        self.pola[0] = [Sciana(self) for x in range(n)]
        self.pola[m-1] = [Sciana(self)  for x in range(n)]
        
        # ramka Y
        for y in range(m):
            self.pola[y][0] = Sciana(self) 
            self.pola[y][n-1] = Sciana(self)

        self.portale = [(None, None) for x in range(9)] # Portal A i B dla cyfr 1-9
        self.burzenia = 0
        
        if mapType == 0:
            self.randomMap()
        elif mapType == 1:
            with open(inputGame, "r") as f:
                text = f.read()
                self.readMap(text)
        else:
            self.readMap(mapInput)

        # init pola
        for y in range(m):
            for x in range(n):
                self.pola[y][x].setPos(x, y)
    
    def Znaki2Rodzaje(self, znak):
        if znak >= '1' and znak <= '9': # portal
            idx = int(znak)-int('1')
            para = self.portale[idx]
            portal = Portal(self)
            if not para[0]:
                self.portale[idx] = (portal, None)
            else:
                drugi = para[0]
                drugi.__class__ = Portal
                # połączenie między portalami
                drugi.setDrugiPortal(portal) 
                portal.setDrugiPortal(drugi)
                self.portale[idx] = (drugi, portal)
            return portal
        
        # prezent
        akcje = self.flow.getAkcje()
        for akcja in akcje:
            if znak == akcja.znakUzycia:
                return Prezent(self, znak)

        return {
            'O': PustePole(self, False, False), # puste pole
            'X': PustePole(self, True, False), # poczatek
            '$': PustePole(self, False, True), # koniec
            '^': Kolec(self), # kolec
            '.': PustaSciana(self), # pusta sciana
            '|': Sciana(self), # sciana zwykla pionowa
            '-': Sciana(self), # sciana zwykla pozioma
            'I': Sciana(self, True), # sciana twarda pionowa
            '=': Sciana(self, True), # sciana twarda pozioma
            '[' : Drzwi(self),
            '#' : Bagno(self),
            '%': Pulapka(self),
            '(': TajnePrzejscie(self),
            '{': CzasowePrzejscie(self, False),
            '}': CzasowePrzejscie(self, True),
            '\\': KrzyweZwierciadlo(self)
        }[znak]

    def pole2Tab(self, x, y):
        # 0 0 -> 1 1
        # 1 0 -> 3 1
        nx = 2 * x + 1
        ny = 2 * y + 1
        return (nx, ny)
    
    def tab2Pole(self, x, y):
        nx = int((x - 1) / 2)
        ny = int((y - 1) / 2)
        return (nx, ny)
    
    def turnStart(self):
        pole = self.pola[self.posy][self.posx]
        pole.onStart()
    
    def readMap(self, text):
        lines = text.split('\n')
        self.setSizeNM(len(lines[0]), len(lines))
        print(self.w, self.h)
        n = self.n
        m = self.m
        pola = self.pola
        startx = 0
        starty = 0
        endx = 0
        endy = 0
        y = 0
        for txt in lines:
            for x in range(n):
                curr = txt[x]
                try:
                    pole = self.Znaki2Rodzaje(curr)
                    pola[y][x] = pole
                    if pole.__class__ == PustePole: #wykryj start lub koniec
                        pustePole = pole
                        pustePole.__class__ = PustePole
                        (czyStart, czyKoniec) = pustePole.getStartKoniec()
                        if czyStart:
                            startx = x
                            starty = y
                        elif czyKoniec:
                            endx = x
                            endy = y
                except:
                    print(f'ERRR')
                    pass
            y += 1
        (startpx, startpy) = self.tab2Pole(startx, starty)
        (endpx, endpy) = self.tab2Pole(endx, endy)
        self.setupPoczIKon(startpx, startpy, endpx, endpy)

    def randomMap(self):
        # LOSOWE SCIANY
        scianyPion = 3
        scianyPoz = 3
        w = self.w
        h = self.h
        for i in range(scianyPion):
            px = random.randint(0, w-1)
            py = random.randint(0, h-1)

            (x, y) = self.pole2Tab(px, py)
            self.pola[y+1][x] = Sciana(self) #prawa sciana
        for i in range(scianyPoz):
            px = random.randint(0, w-1)
            py = random.randint(0, h-1)

            (x, y) = self.pole2Tab(px, py)
            self.pola[y][x-1] = Sciana(self) #gorna sciana

        startpx = random.randint(0, w - 1)
        startpy = random.randint(0, h - 1)
        endpx = random.randint(0, w - 1)
        endpy = random.randint(0, h - 1)

        (startx, starty) = self.pole2Tab(startpx, startpy)
        (endx, endy) = self.pole2Tab(endpx, endpy)
        self.pola[starty][startx] = PustePole(self, True, False)
        self.pola[endx][endy] = PustePole(self, False, True)

        self.setupPoczIKon(startpx, startpy, endpx, endpy)
    
    def setupPoczIKon(self, startpx, startpy, endpx, endpy):
        self.startpx = startpx
        self.startpy = startpy
        self.endpx = endpx
        self.endpy = endpy

        # POZYCJE GRACZA
        self.pospx = startpx
        self.pospy = startpy
        self.posx = 0
        self.posy = 0
        self.reloadGraczPoz()

    def reloadGraczPoz(self):
        (self.posx, self.posy) = self.pole2Tab(self.pospx,self.pospy)
        self.odkryte[self.posy][self.posx] = True

    def setGraczP(self, x, y):
        self.pospx = x
        self.pospy = y
        self.reloadGraczPoz()

    def setGracz(self, x, y):
        self.posx = x
        self.posy = y
        (self.pospx, self.pospy) = self.tab2Pole(x,y)
        self.reloadGraczPoz()

    def zabij(self, zerujAkcje = True):
        _,_,px,py,_,_ = self.getPositions()
        self.setGraczP(px,py)
        if zerujAkcje:
            self.flow.akcjeLeft = 0

    def tryWyburzanie(self):
        if self.burzenia > 0:
            self.burzenia -= 1
            return True
        return False

    def getPositions(self):
        return self.pospx, self.pospy, self.startpx, self.startpy, self.endpx, self.endpy

    def getMapa(self, all = False):
        pola = self.pola
        odkryte = self.odkryte
        n = self.n
        m = self.m
        res = ""
        posx = self.posx
        posy = self.posy

        for y in range(m):
            for x in range(n):
                pole = pola[y][x]

                if not all and not odkryte[y][x]:
                    res = res + ' '
                    continue

                if x == posx and y == posy: # GRACZ
                    res = res + '&'
                    continue

                znak = pole.getZnak()
                res = res + znak
            res = res + '\n'
        return res
    
    def getMiddlePole(self):
        odkryteKordyX = []
        odkryteKordyY = []
        for y in range(self.h):
            for x in range(self.w):
                tx, ty = self.pole2Tab(x,y)
                if self.odkryte[ty][tx]:
                    odkryteKordyX.append(tx)
                    odkryteKordyY.append(ty)
        odkryteKordyX.sort()
        odkryteKordyY.sort()

        return (odkryteKordyX[0]+odkryteKordyX[-1])/2, (odkryteKordyY[0]+odkryteKordyY[-1])/2

    # AKCJE
    def tryRuch(self, rx, ry):
        posx = self.posx
        posy = self.posy
        odkryte = self.odkryte
        pola = self.pola

        # sciana na drodze
        scianax = posx + rx
        scianay = posy + ry
        sciana = pola[scianay][scianax]
        odkryte[scianay][scianax] = True
        
        sciana.onEnter()
        if not sciana.canEnter():
            return False
        
        # kolejne pole
        polex = scianax + rx
        poley = scianay + ry

        # czy out of bounds
        if polex < 0 or polex >= self.n or poley < 0 or polex >= self.m:
            return False

        pole = pola[poley][polex]
        odkryte[poley][polex] = True

        pole.onEnter()
        if not pole.canEnter():
            return False
        
        self.pospx += rx
        self.pospy += ry
        self.reloadGraczPoz()
        return True

    def checkWin(self):
        if self.pospx == self.endpx and self.pospy == self.endpy:
            return True
        return False
    
    def kompasuj(self, left):
        odl = max(abs(self.pospx-self.endpx),abs(self.pospy-self.endpy))
        self.flow.addDodatkowyTekst(f"Pozostalo {left} kompasow. Wynik kompasu: {odl}.\n")

    def mapuj(self, zasiegMapowania, left):
        odkryte = self.odkryte
        posx = self.posx
        posy = self.posy
        for y in range(self.m):
            for x in range(self.n):
                dist = abs(posx-x)+abs(posy-y)
                if dist <= zasiegMapowania:
                    odkryte[y][x] = True
        self.flow.addDodatkowyTekst(f"Pozostalo {left} map.\n")

    def addBurzenie(self, left):
       self.burzenia += 1
       self.flow.addDodatkowyTekst(f"Pozostalo {left} wyburzen.\n")

    def usunLosowoOdkryte(self, usun):
        odkryte = self.odkryte
        odkryteList = []
        for y in range(self.m):
            for x in range(self.n):
                if odkryte[y][x]:
                    odkryteList.append((x,y))
        for i in range(usun):
            if len(odkryteList) <= 0:
                break
            toUsun = odkryteList[random.randint(0, len(odkryteList)-1)]
            odkryte[toUsun[1]][toUsun[0]] = False
            odkryteList.remove(toUsun)

    
    