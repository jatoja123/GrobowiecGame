from dataclasses import dataclass
from Game.akcje import *


@dataclass
class GameSettings():
    w = 5
    h = 5
    akcje = [
        AkcjaMapowanie(2, 1, 2), 
        AkcjaKompasowanie(2, 1),
        AkcjaBurzenie(1, 2),
        AkcjaSamobojstwo(1, 3)
    ]
    limitAkcji = 3
    tylkoJednoliteAkcje = False
    limitSkretow = 1 # -1 zeby brak
    usunieciaZwierciadla = 3