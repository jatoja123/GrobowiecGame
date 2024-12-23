from gameFlow import GameFlow
from akcje import *

# --- INFO ---
# Rodzaje PÓL
#  O   puste
#  X   pole startowe
#  $   pole końcowe
#  ^   kolec - po wejściu zabija (i zeruje akcje)
#  #   bagno - startując na nim masz /2 akcji
#  %   pułapka - startując na niej giniesz (jest ukryta dopóki nie wejdziesz w nią)
#  @   portal - przenosi cię do zlinkowanego portalu (i zeruje akcje)
#  *   prezent - w środku znajduje się dodatkowe użycie jakiejś akcji
#
# Rodzaje ŚCIAN
#  .   brak ściany, przejście
#  | lub -  zwykła ściana - można zburzyć ją po użyciu akcji burzenia
#  I lub =   twarda ściana - nie można jej zburzyć
#  [  drzwi - przejście przez nie zużywa wszystkie akcje
#  (  tajne przejście - można normalnie przejść, ale po użyciu mapowania pokazuje się jak zwykła ściana
#  { lub }  przejście czasowe - można przejść nim tylko na nieparzystym/parzystym ruchu (odpowiednio { i } )
#
# Akcje
#  w,s,a,d   ruch
#  k  kompasowanie - pokazuje odległość od skarbu (max(distx,disty)) 
#  m  mapowanie - ujawnia fragment terenu wokół
#  b  burzenie - kolejne przejście przez zwykłą ścianę zburzy ją
#  r  samobojstwo - zabijasz sie, wracasz na start
# Akcje można stackować np. "wak", różne akcje zużywają różną ilość akcji na turę
#
# Mapmaking
# - NIE zamieniać ścian z polami
# - NIE duplikować startów (X) i końców ($)
# - Aby linkować portale trzeba użyć cyfry (1-9) w dwóch miejscach a nie znaku @
# - Robiąc ściany nie trzeba zachowywać orientacji (wszystkie mogą być '|')


# --- USTAWIENIA ---
w = 5
h = 5
# Akcje inne
akcje = [
    AkcjaMapowanie(2, 1, 2), 
    AkcjaKompasowanie(2, 1),
    AkcjaBurzenie(2, 2),
    AkcjaSamobojstwo(1, 3)
]
# Akcja: Ruch
limitAkcji = 3
tylkoJednoliteAkcje = False # czy jedyne dozwolone akcje to akcje w jednym kierunku np. AA, DD itd
limitSkretow = 1 # -1 zeby brak

flow = GameFlow(w, h, akcje, limitAkcji, tylkoJednoliteAkcje, limitSkretow)