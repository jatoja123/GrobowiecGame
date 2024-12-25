import asyncio
from gameInput import GameInput
import aioconsole


class ConsoleInput(GameInput):
    def Output(self, data):
        print(data)

    async def AskForInput(self):
        task = asyncio.create_task(super().AskForInput())
        res = await aioconsole.ainput('')
        self.ReceiveInput(res)
        await task
        return task.result()