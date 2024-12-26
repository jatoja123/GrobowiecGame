import asyncio
from Input.gameInput import GameInput
import os
clear = lambda: os.system('cls')

class ConsoleInput(GameInput):
    def OutputText(self, data):
        print(data)

    def OutputMap(self, map, mapText, odkryte):
        print(mapText)

    def ClearOutputs(self):
        clear()

    async def AskForInput(self):
        res = input('')
        return res