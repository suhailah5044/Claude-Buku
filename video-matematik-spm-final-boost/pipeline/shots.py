"""Perpustakaan shot b-roll + cue setiap unit VO.
SHOT[key] = f (fail assets/broll), ms (media start, s), kb (ken burns dari,ke), o (transform-origin),
            cy (y caption pada shot ni: ruang kosong - meja marmar di atas / tangan di bawah), max (tempoh maksimum ms..hujung klip)
CUES[unit] = [(saat relatif dalam unit, key), ...]  -> shot bertukar dengan fade lembut 0.3 s.
Setiap kali VO sebut benda dalam buku, cue tunjuk shot itu (badge Fokus Soalan / Skema Jawapan /
Bengkel Kalkulator, isi kandungan = topik, halaman rumus, flip latihan, cover)."""
TOP, BOT = 200, 1340   # caption: atas (meja kosong) | bawah (tangan / awan cover), dalam zon selamat 150-1550

SHOT = {
    # cover
    "tbl":     dict(f="IMG_1405.mp4", ms=0.9, kb=(1.00, 1.05), cy=TOP),          # cover atas meja
    "flat":    dict(f="IMG_1390.mp4", ms=5.2, kb=(1.04, 1.00), cy=TOP),          # cover atas meja (lain sudut)
    "hold":    dict(f="IMG_1392.mp4", ms=6.0, kb=(1.00, 1.06), cy=TOP),          # pegang cover atas meja
    "hold2":   dict(f="IMG_1393.mp4", ms=22.0, kb=(1.00, 1.05), cy=TOP),         # angkat cover dekat
    "lift":    dict(f="IMG_1401.mp4", ms=6.4, kb=(1.00, 1.06), cy=TOP),          # cover atas meja -> buka
    "pick":    dict(f="IMG_1400.mp4", ms=3.4, kb=(1.00, 1.05), cy=TOP),          # pegang cover
    "close":   dict(f="IMG_1408.mp4", ms=2.4, kb=(1.00, 1.05), cy=TOP),          # pegang cover dekat (meja kosong atas)
    "footage": dict(f="footage_hold.mp4", ms=0.0, kb=(1.00, 1.04), cy=TOP),      # Footage.mov (review)
    "spine":   dict(f="IMG_1399.mp4", ms=1.2, kb=(1.00, 1.06), cy=TOP),          # spine buku
    # badge cover (USP)
    "badge_fokus": dict(f="IMG_1396.mp4", ms=7.6, kb=(1.00, 1.02), o="40% 40%", cy=BOT),  # 3 badge: FOKUS SOALAN BERPOTENSI TINGGI (awan bawah kosong)
    "badge_skema": dict(f="IMG_1396.mp4", ms=8.3, kb=(1.00, 1.02), o="40% 50%", cy=BOT),  # SKEMA JAWAPAN LENGKAP & TERATUR
    "badge_kalk":  dict(f="IMG_1396.mp4", ms=8.8, kb=(1.00, 1.02), o="40% 60%", cy=BOT),  # jari dekat PERCUMA BENGKEL KALKULATOR
    "kalk2":       dict(f="IMG_1398.mp4", ms=1.0, kb=(1.00, 1.02), o="20% 30%", cy=1470),  # badge PERCUMA BENGKEL KALKULATOR (caption atas tangan, bawah jalur)
    "badges":      dict(f="IMG_1397.mp4", ms=2.9, kb=(1.00, 1.02), o="40% 20%", cy=BOT),  # semua badge (window stabil ~1 s)
    "spm_badge":   dict(f="IMG_1398.mp4", ms=3.6, kb=(1.00, 1.06), o="70% 55%", cy=BOT), # badge 'BERDASARKAN FORMAT TERKINI SPM'
    # isi buku
    "toc":     dict(f="IMG_1403.mp4", ms=4.0, kb=(1.00, 1.06), cy=TOP),          # isi kandungan (topik), jari
    "formula": dict(f="IMG_1404.mp4", ms=0.0, kb=(1.00, 1.06), cy=TOP),          # halaman rumus
    "flip_a":  dict(f="IMG_1395.mp4", ms=2.0, kb=(1.00, 1.05), cy=TOP),          # flip halaman dalam tangan
    "flip_b":  dict(f="IMG_1402.mp4", ms=3.0, kb=(1.00, 1.05), cy=TOP),          # flip tebal (200+ muka surat)
    "flip_c":  dict(f="IMG_1409.mp4", ms=1.6, kb=(1.00, 1.05), cy=TOP),          # flip ke arah kamera
    "pages_a": dict(f="IMG_1391.mp4", ms=0.0, kb=(1.00, 1.06), cy=TOP),          # halaman soalan + grid
    "pages_b": dict(f="IMG_1404.mp4", ms=4.0, kb=(1.00, 1.05), cy=TOP),          # buku terbuka atas meja (graf)
    "pages_c": dict(f="IMG_1401.mp4", ms=9.4, kb=(1.00, 1.05), cy=TOP),          # flip halaman atas meja
    "pages_d": dict(f="IMG_1393.mp4", ms=2.5, kb=(1.00, 1.05), cy=TOP),          # halaman soalan (rajah)
    "pages_e": dict(f="IMG_1392.mp4", ms=14.5, kb=(1.00, 1.05), cy=TOP),         # halaman soalan
    "graph":   dict(f="IMG_1400.mp4", ms=8.8, kb=(1.00, 1.05), cy=TOP),          # flip: graf & carta
}

CUES = {
    "i_189E": [(0, "hold"), (2.40, "close"), (4.30, "flip_a")],
    "i_235A": [(0, "pages_b"), (1.60, "badge_skema"), (3.50, "pages_c")],
    "i_2C72": [(0, "flip_b"), (1.85, "pages_b"), (3.30, "hold2"), (5.20, "spine")],
    "i_4557": [(0, "tbl"), (2.55, "hold"), (4.00, "flip_c")],
    "i_48FA": [(0, "flip_c"), (1.90, "lift"), (3.05, "badge_skema"), (4.80, "pages_c")],
    "i_70D5": [(0, "spine"), (1.45, "pages_b"), (3.85, "flip_a")],
    "i_A559": [(0, "pages_a"), (1.60, "hold"), (3.05, "badge_fokus")],
    "i_BD48": [(0, "flat"), (1.25, "badge_fokus"), (3.80, "flip_b")],
    "i_C83B": [(0, "footage"), (1.85, "close"), (3.70, "pages_d"), (5.50, "flip_a")],
    "i_EC6D": [(0, "lift"), (2.75, "close"), (3.90, "flip_c"), (5.90, "pages_c")],
    "t_3454": [(0, "hold2"), (0.95, "badge_kalk"), (2.90, "kalk2"), (6.20, "pages_e"), (7.65, "flip_b")],
    "t_96DE": [(0, "hold"), (2.60, "badge_fokus"), (4.30, "spm_badge"), (5.75, "flip_b"), (7.40, "pages_b")],
    "t_E6E5": [(0, "flip_c"), (1.85, "spm_badge"), (4.00, "flat"), (6.95, "pages_c")],
    "f_full": [(0, "footage"), (2.50, "badge_fokus"), (4.30, "spm_badge"), (6.10, "pages_d"), (8.20, "toc"), (9.10, "formula"), (10.10, "flip_c")],
    "c_3EF9": [(0, "hold2"), (2.05, "tbl")],
    "c_4EE9": [(0, "pick"), (1.85, "tbl")],
    "c_C62F": [(0, "flip_b"), (2.35, "hold2")],
    "c_E3ED": [(0, "spm_badge"), (2.60, "flat")],
    "c_F20C": [(0, "hold"), (1.75, "lift")],
}
# Shot pengganti bila shot sama bersebelahan (sempadan unit) atau diguna semula dalam video yang sama
ALT = {"hold": "pick", "hold2": "lift", "flip_b": "flip_a", "flip_c": "pages_c", "pages_b": "graph", "pages_c": "pages_a",
       "tbl": "flat", "flat": "tbl", "lift": "hold", "spm_badge": "badges", "badge_fokus": "badges", "close": "footage",
       "pick": "hold", "flip_a": "flip_c", "spine": "pick", "pages_d": "pages_e", "pages_e": "pages_d", "pages_a": "graph"}
