import random
import os

# POLA
# 0 - puste pole
# 1 - start
# 2 - koniec
RodzajePol = ['O','X','$']
# ŚCIANY
# 0 - brak
# 1 - ściana
RodzajeScian = ['.','#']

class Game:
    won = False
    def __init__(self, w, h, inputGame, randomize):
        self.w = w # [pól]
        self.h = h # [pól]   
        self.n = 1 + 2 * w
        self.m = 1 + 2 * h

        n = self.n
        m = self.m
        self.pola = [[0 for x in range(n)] for y in range(m)]
        self.odkryte = [[False for x in range(n)] for y in range(m)]
        # ramka X
        self.pola[0] = [1 for x in range(n)]
        self.pola[n-1] = [1 for x in range(n)]
        
        # ramka Y
        for y in range(m):
            self.pola[y][0] = 1
            self.pola[y][m-1] = 1
        
        if randomize:
            self.randomMap()
        else:
            self.readMap(inputGame)

    def pole2Tab(self, x, y):
        # 0 0 -> 1 1
        # 1 0 -> 3 1
        nx = 2 * x + 1
        ny = 2 * y + 1
        return (nx, ny)
    
    def readMap(self, input):
        global RodzajePol, RodzajeScian
        n = self.n
        m = self.m
        pola = self.pola
        startpx = 0
        startpy = 0
        endpx = 0
        endpy = 0
        with open(input, "r") as f:
            for (line, y) in f:
                txt = line.strip()
                for x in range(n):
                    curr = txt[x]
                    pi = RodzajePol.index(curr)
                    si = RodzajeScian.index(curr)
                    if pi >= 0:
                        pola[y][x] = pi
                        if pi == 1: #ZNALEZIONO START
                            startpx = x
                            startpy = y
                        elif pi == 2: #ZNALEZIONO KONIEC
                            endpx = x
                            endpy = y
                    elif si >= 0:
                        pola[y][x] = si
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
            self.pola[y+1][x] = 1 #prawa sciana
        for i in range(scianyPoz):
            px = random.randint(0, w-1)
            py = random.randint(0, h-1)

            (x, y) = self.pole2Tab(px, py)
            self.pola[y][x-1] = 1 #gorna sciana

        startpx = random.randint(0, w - 1)
        startpy = random.randint(0, h - 1)
        endpx = random.randint(0, w - 1)
        endpy = random.randint(0, h - 1)
        self.setupPoczIKon(startpx, startpy, endpx, endpy)
    
    def setupPoczIKon(self, startpx, startpy, endpx, endpy):
        self.startpx = startpx
        self.startpy = startpy
        self.endpx = endpx
        self.endpy = endpy

        # START I KONIEC
        (startx, starty) = self.pole2Tab(startpx, startpy)
        (endx, endy) = self.pole2Tab(endpx, endpy)
        self.pola[starty][startx] = 1
        self.pola[endy][endx] = 2
        # POZYCJE GRACZA
        self.pospx = startpx
        self.pospy = startpy
        self.posx = 0
        self.posy = 0
        self.reloadGraczPoz()

    def reloadGraczPoz(self):
        (self.posx, self.posy) = self.pole2Tab(self.pospx,self.pospy)
        self.odkryte[self.posy][self.posx] = True

    def mapa(self, all = False):
        global RodzajePol
        global RodzajeScian
        pola = self.pola
        odkryte = self.odkryte
        n = self.n
        m = self.m
        res = ""
        posx = self.posx
        posy = self.posy

        for y in range(m):
            for x in range(n):
                if not odkryte[y][x]:
                    res = res + ' '
                    continue

                if x == posx and y == posy: # GRACZ
                    res = res + '@'
                    continue

                sciana = False
                if y%2==0 or x%2==0:
                    sciana = True
                znak = '!'
                if sciana: # TO ŚCIANA
                    znak = RodzajeScian[pola[y][x]]
                    if znak == '#': # ZAMIEŃ ZWYKŁĄ ŚCIANĘ NA ŚCIANĘ Z ODPOWIEDNIĄ ORIENTACJĄ
                        if y%2==0 and x%2 != 0:
                            znak = '-'
                        elif y%2!=0 and x%2 == 0:
                            znak = '|'
                        else:
                            znak = '+'
                else: # TO POLE
                    znak = RodzajePol[pola[y][x]]
                res = res + znak
            res = res + '\n'
        return res

    # AKCJE
    def tryRuch(self, rx, ry):
        posx = self.posx
        posy = self.posy
        odkryte = self.odkryte
        pola = self.pola

        # sciana na drodze
        nextx = posx + rx
        nexty = posy + ry
        odkryte[nexty][nextx] = True
        
        if pola[nexty][nextx] != 0:
            return False
        # kolejne pole ok
        nextx = nextx + rx
        nexty = nexty + ry
        odkryte[nexty][nextx] = True

        self.pospx += rx
        self.pospy += ry
        self.reloadGraczPoz()
        return True

    def checkWin(self):
        if self.pospx == self.endpx and self.pospy == self.endpy:
            return True
        return False