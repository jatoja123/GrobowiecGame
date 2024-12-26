from dataclasses import dataclass
from Game.akcje import *


@dataclass
class MapSettings():
    default_w = 5
    default_h = 5
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

@dataclass
class FlowSettings():
    playerCount = 0
    playerMapNames = [] #stąd będzie wczytywał mapy