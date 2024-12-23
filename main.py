from gameFlow import GameFlow

# --- USTAWIENIA ---
w = 5
h = 5
mapowania = 3
zasiegMapowania = 2
skanowania = 2
limitAkcji = 3
tylkoJednoliteAkcje = False # czy jedyne dozwolone akcje to akcje w jednym kierunku np. AA, DD itd
limitSkretow = 1 # -1 zeby brak

flow = GameFlow(w, h, mapowania, zasiegMapowania, skanowania, limitAkcji, tylkoJednoliteAkcje, limitSkretow)