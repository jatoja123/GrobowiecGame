import asyncio
import threading


class AsyncGameThread(threading.Thread):
    """
    Wątek, który będzie uruchamiał pętlę asyncio
    i w niej będzie wykonywał logikę GameFlow.
    """
    def __init__(self, flow):
        super().__init__()
        self.flow = flow
        # Tworzymy sobie nową pętlę zdarzeń asyncio:
        self.loop = asyncio.new_event_loop()
        # Flaga, żeby móc np. zatrzymać loop "grzecznie".
        self._stop_event = threading.Event()

    def run(self):
        # Ustawiamy, by pętla asynchroniczna w tym wątku była "obowiązująca".
        asyncio.set_event_loop(self.loop)
        try:
            # Uruchamiamy docelową korutynę
            # (tu: WczytajGraczy + ewentualnie startFlow).
            # Możesz też dać run_forever, jeśli masz pętlę w kodzie asynchronicznym.
            self.flow.gameInput.SetGameThreadLoop(self.loop)
            self.loop.run_until_complete(self.flow.PoczatekGry())
            self.loop.run_until_complete(self.flow.StartFlow())
            self.loop.run_until_complete(self.flow.KoniecGry())
        finally:
            self.loop.close()
    
    def stop(self):
        """
        Opcjonalnie: jeśli chcesz umieć bezpiecznie zatrzymać pętlę w trakcie.
        """
        self._stop_event.set()
        self.loop.call_soon_threadsafe(self.loop.stop())