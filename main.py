from GUI.mainWindow import MainWindow
import sys
from PyQt6.QtWidgets import (
    QApplication,
)
from Game.gameEngine import GameEngine
from Game.gameFlow import GameFlow
from Game.akcje import *
from Game.gameThread import AsyncGameThread
from Game.obiekty import *
from Input.GUIInput import GUIInput
from Input.consoleInput import *

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
#  \  krzywe zwierciadlo - usuwa kilka losowych odkrytych elementow 
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
# - Aby linkować portale trzeba użyć cyfry (1-9) w dwóch miejscach (a nie znaku @)
# - Robiąc ściany nie trzeba zachowywać orientacji (wszystkie mogą być '|')
# - Aby postawić prezent użyj znaku akcji zamiast '*' - czyli k,m,r,b


class Main():
    def __init__(self, isGUI = True):
        if isGUI:
            window = MainWindow()
            window.show()
            exit_code = app.exec()
            # gameThread.stop() # Stop GameFlow thread
            # gameThread.join()
            sys.exit(exit_code)
        else:
            GameEngine(isGUI=False)

if __name__ == "__main__":
    isGUI = True
    if len(sys.argv) > 1:
        isGUI = not (sys.argv[1] == "console" or sys.argv[1] == "c" )
    app = QApplication(sys.argv)  

    main = Main(isGUI)
        

    