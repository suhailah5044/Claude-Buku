#!/usr/bin/env python3
"""EDL: hook paling kuat ke depan ("Anak dah jawab panjang je, tapi markah dapat sikit je"),
kemudian "Sekarang ramai student hadap masalah yang sama", kemudian selebihnya.
Jeda >= 0.14 s dipendekkan ke 0.08 s. Speed 1.1x. T(src) -> masa dalam video akhir."""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
SPEED = 1.1
PAUSES = [(7.32, 7.49), (8.60, 8.74), (13.46, 13.78), (15.26, 15.63), (17.91, 18.13),
          (35.52, 35.81), (40.15, 40.42), (44.55, 44.88)]
KEEP = [(2.47, 5.29), (0.00, 1.80)]
s = 5.30
for a, b in PAUSES:
    KEEP.append((s, round(a + 0.04, 3))); s = round(b - 0.04, 3)
KEEP.append((s, 48.62))
def T(t):
    acc = 0.0
    for a, b in KEEP:
        if a <= t <= b: return round((acc + t - a) / SPEED, 3)
        acc += b - a
    raise ValueError(t)
DUR = round(sum(b - a for a, b in KEEP) / SPEED, 3)
if __name__ == "__main__":
    json.dump(KEEP, open(f"{HERE}/keep.json", "w")); print(KEEP, DUR)
