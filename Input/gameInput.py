import asyncio


class GameInput:
    def __init__(self):
        self.inputEvent = asyncio.Event()
        self.receivedInput = ""
        self.loop = None
        pass

    def OutputText(self, data): #Wydal informacje tekstową do gracza
        pass

    def OutputMap(self, map, mapText, odkryte): #Wydal informacje tekstową do gracza
        pass

    def ClearOutputs(self): # powinno czyścić inputy
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