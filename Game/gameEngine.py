import sys
from Game.akcje import *
from Game.gameFlow import GameFlow
from Game.gameThread import AsyncGameThread
from Game.obiekty import *
from Input.consoleInput import ConsoleInput
from Input.GUIInput import GUIInput


class GameEngine():
    def __init__(self, window = None, isGUI = True):
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
        # --------

        if isGUI:
            self.gameInput = GUIInput()
            self.gameInput.ConnectToWindow(window)
        else:
            self.gameInput = ConsoleInput()

        flow = GameFlow(self.gameInput, w, h, akcje, limitAkcji, tylkoJednoliteAkcje, limitSkretow)
        self.gameThread = AsyncGameThread(flow)

        if isGUI:
            self.gameThread.start()
        else:
            try:
                self.gameThread.start()
            except (KeyboardInterrupt, SystemExit):
                self.gameThread.stop() # Stop GameFlow thread
                self.gameThread.join()
                sys.exit()
    