from GUI.mainWindow import MainWindow
import sys
from PyQt6.QtWidgets import (
    QApplication,
)
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
        super().__init__()
        if isGUI:
            self.gameInput = GUIInput()
            self.window = MainWindow(self.gameInput)
            self.gameInput.ConnectToWindow(self.window)
        else:
            self.gameInput = ConsoleInput()
        
        # --- USTAWIENIA ---
        w = 5
        h = 5
        # Akcje inne
        akcje = [
            AkcjaMapowanie(2, 1, 2), 
            AkcjaKompasowanie(2, 1),
            AkcjaBurzenie(1, 2),
            AkcjaSamobojstwo(1, 3)
        ]
        # Akcja: Ruch
        limitAkcji = 3
        tylkoJednoliteAkcje = False # czy jedyne dozwolone akcje to akcje w jednym kierunku np. AA, DD itd
        limitSkretow = 1 # -1 zeby brak

        # Inne
        KrzyweZwierciadlo.usuniecia = 3

        # ustawiaj = input("Chcesz zmienic ustawienia? (y/n) ")
        # if ustawiaj == 'y':
        #     print("Mapa")
        #     h = int(input(f"Wysokosc mapy [{h}] "))
        #     w = int(input(f"Szerokosc mapy [{w}] "))
        #     print("Ruch")
        #     limitAkcji = int(input(f"Akcje w turze [{limitAkcji}] "))
        #     tylkoJednoliteAkcje = bool(input(f"Czy jednolite akcje? [{tylkoJednoliteAkcje}] "))
        #     limitSkretow = int(input(f"Limit skretow [{limitSkretow}] "))
        #     print("Mapowanie")
        #     mUzycia = int(input(f"Mapowanie uzycia [2] "))
        #     mKoszt = int(input(f"Mapowanie koszt [1] "))
        #     mZasieg = int(input(f"Mapowanie zasieg [2] "))
        #     print("Kompasowanie")
        #     kUzycia = int(input(f"Kompasowanie uzycia [2] "))
        #     kKoszt = int(input(f"Kompasowanie koszt [1] "))
        #     print("Burzenie")
        #     bUzycia = int(input(f"Burzenie uzycia [1] "))
        #     bKoszt = int(input(f"Burzenie koszt [2] "))
        #     print("Samobojstwo")
        #     rUzycia = int(input(f"Samobojstwo uzycia [1] "))
        #     rKoszt = int(input(f"Samobojstwo koszt [3] "))
        #     akcje = [
        #         AkcjaMapowanie(mUzycia, mKoszt, mZasieg), 
        #         AkcjaKompasowanie(kUzycia, kKoszt),
        #         AkcjaBurzenie(bUzycia, bKoszt),
        #         AkcjaSamobojstwo(rUzycia, rKoszt)
        #     ]
        #     print("Pola")
        #     KrzyweZwierciadlo.usuniecia = int(input(f"Ile pol wymazuje zwierciadlo? [{KrzyweZwierciadlo.usuniecia}] "))

        self.flow = GameFlow(self.gameInput, w, h, akcje, limitAkcji, tylkoJednoliteAkcje, limitSkretow)

if __name__ == "__main__":
    isGUI = True
    if len(sys.argv) > 1:
        isGUI = not (sys.argv[1] == "console" or sys.argv[1] == "c" )
    app = QApplication(sys.argv)  

    main = Main(isGUI)
    gameThread = AsyncGameThread(main.flow)
    
    if isGUI: 
        main.window.show()
        gameThread.start()

        exit_code = app.exec()
        gameThread.stop() # Stop GameFlow thread
        gameThread.join()
        sys.exit(exit_code)
    else: # Wersja consolowa
        try:
            gameThread.start()
        except (KeyboardInterrupt, SystemExit):
            gameThread.stop() # Stop GameFlow thread
            gameThread.join()
            sys.exit()

    