from game import Game
import os

clear = lambda: os.system('cls')
Key2Ruch = {'w': (0,-1), 's': (0,1), 'a': (-1,0), 'd': (1,0)}

# --- USTAWIENIA ---
w = 4
h = 4
mapowania = 2
skanowania = 1
akcjeWTurze = 2
tylkoJednoliteAkcje = False # czy jedyne dozwolone akcje to akcje w jednym kierunku np. AA, DD itd

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

        # INPUT gracza
        clear()
        print(f"Ruch {ileRuchow} | Gracz {i} <<")
        print(game.mapa())
        inputAkcje = input('Akcja: ')
        for i in range(len(inputAkcje)):
            if i >= akcjeWTurze:
                break

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
                        print(game.mapa(True))
                        skip = input('...')
                        break
        clear()
        print(f"Ruch {ileRuchow} | Gracz {i}")
        print(game.mapa())
        skip = input('...')
        i += 1
    ileRuchow += 1
        
input('Wszyscy gracze wygrali!')