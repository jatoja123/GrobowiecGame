from Game.game import Game
from Game.obiekty import KrzyweZwierciadlo

Key2Ruch = {'w': (0,-1), 's': (0,1), 'a': (-1,0), 'd': (1,0)}

class GameFlow:
    def __init__(self, gameInput, mapSettings, flowSettings):
        self.flowSettings = flowSettings
        self.gameInput = gameInput

        # Ustawienia gry jednolite dla wszystkich map
        self.w = mapSettings.default_w
        self.h = mapSettings.default_h
        self.limitAkcji = mapSettings.limitAkcji
        self.akcje = mapSettings.akcje
        self.tylkoJednoliteAkcje = mapSettings.tylkoJednoliteAkcje
        self.limitSkretow = mapSettings.limitSkretow
        KrzyweZwierciadlo.usuniecia = mapSettings.usunieciaZwierciadla

        self.dodatkowyTekst = ""
        self.akcjeLeft = 0

    async def PoczatekGry(self):
        self.games = []
        if len(self.flowSettings.playerMapNames) == 0:
            await self.ReadFlowSettings()
        else:
            for mapName in self.flowSettings.playerMapNames:
                game = Game(self, self.w, self.h, mapName, 1) # wczytaj mape z pliku
                game.flow = self
                self.games.append(game)
        
            
    async def ReadFlowSettings(self):
        # Ile graczy?
        playerCount = int(await self.AskPlayer("Liczba graczy: "))
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
                self.gameInput.OutputText(f"Wprowadz mape linika po linijce ({h} linijek)")
                mapLines = []
                for x in range(2*h+1):
                    mapLine = await self.AskPlayer(f"Wiersz {x}:")
                    mapLines.append(mapLine)
                mapInput = '\n'.join(mapLines)

            game = Game(self,w,h,filename,mapType,mapInput)
            game.flow = self
            self.games.append(game)

    async def KoniecGry(self):
        await self.AskPlayer(f"Wszyscy gracze wygrali!")

    async def AskPlayer(self, text):
        self.gameInput.OutputText(text)
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
        self.gameInput.ClearOutputs()
        self.gameInput.OutputText(f"Ruch {self.ileRuchow} | Gracz {self.graczI}")
        self.gameInput.OutputMap( self.game.pola, self.game.getMapa(showAllMap), self.game.odkryte)
        
        if self.dodatkowyTekst != "": self.gameInput.OutputText(self.dodatkowyTekst)
        self.dodatkowyTekst = ""
        if skip: a = await self.AskPlayer(f"...")
    
    async def StartFlow(self):
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