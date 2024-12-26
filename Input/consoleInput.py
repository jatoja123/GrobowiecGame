import asyncio
from Input.gameInput import GameInput
import aioconsole
import os
clear = lambda: os.system('cls')

class ConsoleInput(GameInput):
    def OutputText(self, data):
        print(data)

    def OutputMap(self, map):
        print(map)

    def ClearOutputs(self):
        clear()

    async def AskForInput(self):
        task = asyncio.create_task(super().AskForInput())
        res = await aioconsole.ainput('')
        self.ReceiveInput(res)
        await task
        return task.result()