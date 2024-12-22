from gameFlow import GameFlow

# --- USTAWIENIA ---
w = 5
h = 5
mapowania = 3
skanowania = 2
limitAkcji = 3
tylkoJednoliteAkcje = False # czy jedyne dozwolone akcje to akcje w jednym kierunku np. AA, DD itd

flow = GameFlow(w, h, mapowania, skanowania, limitAkcji, tylkoJednoliteAkcje)