import asyncio
from Input.gameInput import GameInput

class GUIInput(GameInput):
    def __init__(self):
        super().__init__()
    def OutputText(self, data):
        # wyświetlaj output tekstowy
        print(f"Outputing: \n{data}")
        self.window.OutputText(data)
    
    def OutputMap(self, map):
        # Printuj mape
        pass

    def ClearOutputs(self):
        pass

    def ConnectToWindow(self, window):
        self.window = window

    # uruchamiaj ReceiveInput kiedy gracz wybeirze input przyciskami / wpisze cos
        