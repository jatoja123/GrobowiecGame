from game import Game
import os

clear = lambda: os.system('cls')
Key2Ruch = {'w': (0,-1), 's': (0,1), 'a': (-1,0), 'd': (1,0)}

# USTAWIENIA
w = 4
h = 4
mapowania = 2
skanowania = 1

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
        while True: #AŻ dobry input
            clear()
            if game.won:
                continue
            print(f"Ruch {ileRuchow} | Gracz {i}")
            print(game.mapa())
            akcja = input('Akcja: ')

            if akcja == 'o': #SKANOWANIE
                game.skanowania -= 1
                if game.skanowania < 0:
                    continue
                game.skanuj()
            
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
            i += 1
            break
    ileRuchow += 1
        
input('Wszyscy gracze wygrali!')