from game import Game
import os

clear = lambda: os.system('cls')
Key2Ruch = {'w': (0,-1), 's': (0,1), 'a': (-1,0), 'd': (1,0)}

w = 4
h = 4

# Ile graczy?
playerCount = int(input("Liczba graczy: "))

games = []

for i in range(playerCount):
    filename = input(f"Nazwa pliku {i}. gry (rnd aby losowa):")
    games.append(Game(w,h,filename,filename == 'rnd'))

ileRuchow = 0
while True:
    if sum([1 if g.won else 0 for g in games]) == len(games):
        break
    i = 0
    for game in games:
        clear()
        if game.won:
            continue
        print(f"Ruch {ileRuchow} | Gracz {i}")
        print(game.mapa())
        ruch = input('Ruszaj sie:')
        if not ruch in Key2Ruch:
            continue
        (rx, ry) = Key2Ruch[ruch]

        if game.tryRuch(rx, ry):
            if game.checkWin():
                game.won = True
                clear()
                print(f"WIN WIN WIN WIN ({ileRuchow} ruchow) WIN WIN WIN WIN")
                print(game.mapa(True))
                skip = input('Kliknij cos...')
        i += 1
    ileRuchow += 1
        
input('Wszyscy gracze wygrali!\nKliknij aby wyjsc...')