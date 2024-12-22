from game import Game
import os

clear = lambda: os.system('cls')
Key2Ruch = {'w': (0,-1), 's': (0,1), 'a': (-1,0), 'd': (1,0)}

class GameFlow:
    def __init__(self, w, h, mapowania, skanowania, limitAkcji, tylkoJednoliteAkcje):
        self.tylkoJednoliteAkcje = tylkoJednoliteAkcje
        self.limitAkcji = limitAkcji
        self.dodatkowyTekst = ""
        self.akcjeLeft = 0

        # Ile graczy?
        playerCount = int(input("Liczba graczy: "))
        self.games = []

        for i in range(playerCount):
            filename = input(f"Nazwa pliku {i}. gry (rnd aby losowa):")
            game = Game(w,h,filename,filename == 'rnd')
            game.mapowania = mapowania
            game.skanowania = skanowania
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

                for i in range(len(inputAkcje)):
                    if self.akcjeLeft <= 0:
                        break
                    self.akcjeLeft -= 1

                    if i > 0 and self.tylkoJednoliteAkcje and inputAkcje[i-1] != inputAkcje[i]:
                        break
                    
                    akcja = inputAkcje[i]
                    if akcja == 'o': #SKANOWANIE
                        game.skanowania -= 1
                        if game.skanowania < 0:
                            continue
                        game.skanuj()
                        break
                    
                    elif akcja == 'm': #MAPOWANIE
                        game.mapowania -= 1
                        if game.mapowania < 0:
                            continue
                        game.mapuj()

                    else: # RUCH
                        if not akcja in Key2Ruch:
                            continue
                        (rx, ry) = Key2Ruch[akcja]

                        if game.tryRuch(rx, ry):
                            if game.checkWin():
                                game.won = True
                                self.addDodatkowyTekst(f" !! WIN WIN WIN WIN ({self.ileRuchow} ruchow) WIN WIN WIN WIN !!")
                                self.printuj(True, True)
                                break
                self.printuj(True)
                self.graczI += 1
            self.ileRuchow += 1