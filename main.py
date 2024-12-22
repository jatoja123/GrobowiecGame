from gameFlow import GameFlow

# --- USTAWIENIA ---
w = 4
h = 4
mapowania = 2
skanowania = 1
limitAkcji = 2
tylkoJednoliteAkcje = False # czy jedyne dozwolone akcje to akcje w jednym kierunku np. AA, DD itd

flow = GameFlow(w, h, mapowania, skanowania, limitAkcji, tylkoJednoliteAkcje)