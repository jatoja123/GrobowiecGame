from Game.game import Game
import os
import asyncio

clear = lambda: os.system('cls')
Key2Ruch = {'w': (0,-1), 's': (0,1), 'a': (-1,0), 'd': (1,0)}

class GameFlow:
    def __init__(self, gameInput, w, h, akcje, limitAkcji, tylkoJednoliteAkcje, limitSkretow):
        self.gameInput = gameInput
        self.w = w
        self.h = h

        self.limitAkcji = limitAkcji
        self.akcje = akcje
        self.tylkoJednoliteAkcje = tylkoJednoliteAkcje
        self.limitSkretow = limitSkretow

        self.dodatkowyTekst = ""
        self.akcjeLeft = 0

        asyncio.run(self.WczytajGraczy())

    async def WczytajGraczy(self):
        # Ile graczy?
        playerCount = int(await self.AskPlayer("Liczba graczy: "))
        self.games = []
        w = self.w
        h = self.h

        for i in range(playerCount):
            filename = await self.AskPlayer(f"Nazwa pliku {i}. gry (rnd aby losowa, input aby recznie wprowadzic):")
            
            mapType = 1
            mapInput = ""
            if filename == 'rnd':
                mapType = 0
            if filename == 'input':
                mapType = 2
                print(f"Wprowadz mape linika po linijce ({h} linijek)")
                mapLines = []
                for x in range(2*h+1):
                    mapLine = await self.AskPlayer(f"Wiersz {x}:")
                    mapLines.append(mapLine)
                mapInput = '\n'.join(mapLines)

            game = Game(self,w,h,filename,mapType,mapInput)
            game.flow = self
            self.games.append(game)

        await self.startFlow()
        await self.AskPlayer(f"Wszyscy gracze wygrali!")


    async def AskPlayer(self, text):
        self.gameInput.Output(text)
        res = await self.gameInput.AskForInput()
        return res

    def addDodatkowyTekst(self, txt):
        self.dodatkowyTekst += txt

    def getAkcjeLeft(self):
        return self.akcjeLeft
    
    def setAkcjeLeft(self, akcje):
        self.akcjeLeft = akcje
    
    def getIleRuchow(self):
        return self.ileRuchow
    
    def getAkcje(self):
        return self.akcje
    
    def setAkcje(self, akcje):
        self.akcje = akcje
    
    async def printuj(self, skip = False, showAllMap = False):
        clear()
        self.gameInput.Output(f"Ruch {self.ileRuchow} | Gracz {self.graczI}")
        self.gameInput.Output(self.game.getMapa(showAllMap))
        if self.dodatkowyTekst != "": self.gameInput.Output(self.dodatkowyTekst)
        self.dodatkowyTekst = ""
        if skip: a = await self.AskPlayer(f"...")
    
    async def startFlow(self):
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
                await self.printuj(False)
                inputAkcje = await self.AskPlayer(f"Akcja: ")
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
                            await self.printuj(True, True)
                            break
                if game.won:
                    continue
                await self.printuj(True)
                self.graczI += 1
            self.ileRuchow += 1