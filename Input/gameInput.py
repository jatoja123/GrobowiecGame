import asyncio

class GameInput:
    def __init__(self):
        self.inputEvent = None
        self.receivedInput = ""
        pass

    def Output(self, data): #Wydal informacje tekstową do gracza
        pass

    def ReceiveInput(self, input): #Otrzymaj input w postaci tekstu
        if not self.inputEvent:
            print(self.inputEvent)
            print("Input received but nothing is waiting")
            return
        self.receivedInput = input
        self.inputEvent.set()
        self.inputEvent = None

    async def AskForInput(self): #Czekaj na input
        if self.inputEvent:
            print("Another event is waiting...")
            return None
        self.inputEvent = asyncio.Event()
        await self.inputEvent.wait()
        return self.receivedInput