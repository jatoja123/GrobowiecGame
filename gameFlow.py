from game import Game
import os

clear = lambda: os.system('cls')
Key2Ruch = {'w': (0,-1), 's': (0,1), 'a': (-1,0), 'd': (1,0)}

class GameFlow:
    def __init__(self, w, h, akcje, limitAkcji, tylkoJednoliteAkcje, limitSkretow):
        self.limitAkcji = limitAkcji
        self.akcje = akcje
        self.tylkoJednoliteAkcje = tylkoJednoliteAkcje
        self.limitSkretow = limitSkretow

        self.dodatkowyTekst = ""
        self.akcjeLeft = 0

        # Ile graczy?
        playerCount = int(input("Liczba graczy: "))
        self.games = []

        for i in range(playerCount):
            filename = input(f"Nazwa pliku {i}. gry (rnd aby losowa, input aby recznie wprowadzic):")
            mapType = 1
            mapInput = ""
            if filename == 'rnd':
                mapType = 0
            if filename == 'input':
                mapType = 2
                print(f"Wprowadz mape linika po linijce ({h} linijek)")
                mapLines = []
                for x in range(2*h+1):
                    mapLine = input(f"Wiersz {x}:")
                    mapLines.append(mapLine)
                mapInput = '\n'.join(mapLines)

            game = Game(w,h,filename,mapType,mapInput)
            game.flow = self
            self.games.append(game)

        self.startFlow()
        input('Wszyscy gracze wygrali!')

    def setAkcje(self, akcje):
        self.akcjeLeft = akcje

    def addDodatkowyTekst(self, txt):
        self.dodatkowyTekst += txt

    def getAkcje(self):
        return self.akcjeLeft
    
    def getIleRuchow(self):
        return self.ileRuchow
    
    def printuj(self, skip = False, showAllMap = False):
        clear()
        print(f"Ruch {self.ileRuchow} | Gracz {self.graczI}")
        print(self.game.getMapa(showAllMap))
        if self.dodatkowyTekst != "": print(self.dodatkowyTekst)
        self.dodatkowyTekst = ""
        if skip: input("...")
    
    def startFlow(self):
        self.ileRuchow = 0
        games = self.games
        while True:
            if sum([1 if g.won else 0 for g in games]) == len(games):
                break
            self.graczI = 0
            for game in games:
                self.game = game
                if game.won:
                    self.graczI += 1
                    continue

                self.akcjeLeft = self.limitAkcji

                # Poczatek tury
                game.turnStart()
                
                # INPUT gracza
                self.printuj(False)
                inputAkcje = input('Akcja: ')
                poprzednieRuchy = []
                zrobioneSkrety = 0

                for i in range(len(inputAkcje)):
                    if self.akcjeLeft <= 0:
                        break
                    self.akcjeLeft -= 1
                    if i > 0 and self.tylkoJednoliteAkcje and inputAkcje[i-1] != inputAkcje[i]:
                        break
                    
                    akcja = inputAkcje[i]

                    znalezionoAkcje = False
                    for rodzajAkcji in self.akcje:
                        if rodzajAkcji.znakUzycia == akcja:
                            rodzajAkcji.uzyj(game)
                            znalezionoAkcje = True
                            break
                    if znalezionoAkcje:
                        continue

                    # RUCH
                    if not akcja in Key2Ruch:
                        self.addDodatkowyTekst(f"Nieprawidlowa akcja '{akcja}'\n")
                        continue
                    (rx, ry) = Key2Ruch[akcja]

                    poprzednieRuchy.append((rx, ry))
                    if zrobioneSkrety != -1 and len(poprzednieRuchy) > 1 and poprzednieRuchy[-1] != poprzednieRuchy[-2]: #ruch ze skrętem
                        zrobioneSkrety += 1
                        if zrobioneSkrety > self.limitSkretow:
                            self.addDodatkowyTekst(f"Limit skretow to {self.limitSkretow}\n")
                            continue

                    if game.tryRuch(rx, ry):
                        if game.checkWin():
                            game.won = True
                            self.addDodatkowyTekst(f" !! WIN WIN WIN WIN ({self.ileRuchow} ruchow) WIN WIN WIN WIN !!")
                            self.printuj(True, True)
                            break
                if game.won:
                    continue
                self.printuj(True)
                self.graczI += 1
            self.ileRuchow += 1