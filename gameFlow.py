from game import Game
import os

clear = lambda: os.system('cls')
Key2Ruch = {'w': (0,-1), 's': (0,1), 'a': (-1,0), 'd': (1,0)}

class GameFlow:
    currGame = None
    akcjaI = 0
    currLimitAkcji = 0

    def __init__(self, w, h, mapowania, skanowania, limitAkcji, tylkoJednoliteAkcje):
        GameFlow.currLimitAkcji = limitAkcji

        # Ile graczy?
        playerCount = int(input("Liczba graczy: "))
        games = []

        for i in range(playerCount):
            filename = input(f"Nazwa pliku {i}. gry (rnd aby losowa):")
            game = Game(w,h,filename,filename == 'rnd')
            game.mapowania = mapowania
            game.skanowania = skanowania
            games.append(game)

        ileRuchow = 0
        while True:
            if sum([1 if g.won else 0 for g in games]) == len(games):
                break
            i = 0
            for game in games:
                if game.won:
                    i += 1
                    continue

                GameFlow.currGame = game

                # INPUT gracza
                clear()
                print(f"Ruch {ileRuchow} | Gracz {i} <<")
                print(game.getMapa())
                inputAkcje = input('Akcja: ')
                for i in range(len(inputAkcje)):
                    if i >= GameFlow.currLimitAkcji:
                        break

                    GameFlow.akcjaI = i

                    if i > 0 and tylkoJednoliteAkcje and inputAkcje[i-1] != inputAkcje[i]:
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
                                clear()
                                print(f"WIN WIN WIN WIN ({ileRuchow} ruchow) WIN WIN WIN WIN")
                                print(game.getMapa(True))
                                skip = input('...')
                                break
                clear()
                print(f"Ruch {ileRuchow} | Gracz {i}")
                print(game.getMapa())
                skip = input('...')
                i += 1
            ileRuchow += 1
                
        input('Wszyscy gracze wygrali!')