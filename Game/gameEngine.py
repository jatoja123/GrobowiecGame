import sys
from Game.akcje import *
from Game.gameFlow import GameFlow
from Game.gameSettings import *
from Game.gameThread import AsyncGameThread
from Game.obiekty import *
from Input.consoleInput import ConsoleInput
from Input.GUIInput import GUIInput


class GameEngine():
    def __init__(self, window = None, mapSettings = MapSettings(), flowSettings = FlowSettings, isGUI = True):
        if isGUI:
            self.gameInput = GUIInput()
            self.gameInput.ConnectToWindow(window)
        else:
            self.gameInput = ConsoleInput()

        flow = GameFlow(self.gameInput, mapSettings, flowSettings)
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
    def Stop(self):
        self.gameThread.stop()
        self.gameThread.join()
    