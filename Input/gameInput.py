import asyncio


class GameInput:
    def __init__(self):
        self.inputEvent = asyncio.Event()
        self.receivedInput = ""
        self.loop = None
        pass

    def Output(self, data): #Wydal informacje tekstową do gracza
        pass

    def SetGameThreadLoop(self, loop):
        self.loop = loop

    def ReceiveInput(self, input): #Otrzymaj input w postaci tekstu
        if not self.loop:
            print("No loop!")
            return
        self.receivedInput = input
        #self.inputEvent.set()
        self.loop.call_soon_threadsafe(self.inputEvent.set)
        
    async def AskForInput(self): #Czekaj na input
        await self.inputEvent.wait()
        self.inputEvent.clear()
        return self.receivedInput