"""Perpustakaan shot b-roll + cue setiap unit VO.
SHOT[key] = f (fail assets/broll), ms (media start, s), kb (ken burns dari,ke), o (transform-origin),
            cy (y caption pada shot ni: ruang kosong - meja marmar di atas / tangan di bawah), max (tempoh maksimum ms..hujung klip)
CUES[unit] = [(saat relatif dalam unit, key), ...]  -> shot bertukar dengan fade lembut 0.3 s.
Setiap kali VO sebut benda dalam buku, cue tunjuk shot itu (badge Fokus Soalan / Skema Jawapan /
Bengkel Kalkulator, isi kandungan = topik, halaman rumus, flip latihan, cover)."""
TOP, BOT = 200, 1340   # caption: atas (meja kosong) | bawah (tangan / awan cover), dalam zon selamat 150-1550

# win=(w0,w1): julat STATIK (masa asal klip) - shot boleh guna mana-mana bahagian, tak terkena aksi separuh jalan
# act=(a,b): AKSI LENGKAP (buka buku / selak) - WAJIB main dari a hingga b (pengguna: "kalau nak buka, bagi buka");
#            pre/post = julat tenang sebelum/selepas aksi yang boleh ditambah bila shot lebih panjang
SHOT = {
    # cover
    "tbl":     dict(f="IMG_1405.mp4", ms=1.0, win=(1.0, 3.6), kb=(1.00, 1.05), cy=TOP),          # cover atas meja
    "flat":    dict(f="IMG_1390.mp4", ms=5.2, win=(3.0, 9.0), kb=(1.04, 1.00), cy=TOP),          # cover atas meja (lain sudut)
    "hold":    dict(f="IMG_1392.mp4", ms=6.0, win=(5.5, 11.8), kb=(1.00, 1.06), cy=TOP),         # pegang cover atas meja
    "hold2":   dict(f="IMG_1393.mp4", ms=22.0, win=(21.5, 28.7), kb=(1.00, 1.05), cy=TOP),       # angkat cover dekat
    "pick":    dict(f="IMG_1400.mp4", ms=2.6, win=(1.6, 4.3), kb=(1.00, 1.05), cy=TOP),          # pegang cover
    "close":   dict(f="IMG_1408.mp4", ms=2.4, win=(2.2, 5.2), kb=(1.00, 1.05), cy=TOP),          # pegang cover dekat (meja kosong atas)
    "footage": dict(f="footage_hold.mp4", ms=0.0, win=(0.0, 13.3), kb=(1.00, 1.04), cy=TOP),     # Footage.mov (review)
    "spine":   dict(f="IMG_1399.mp4", ms=1.2, win=(1.0, 8.3), kb=(1.00, 1.06), cy=TOP),          # spine buku
    # AKSI BUKA (lengkap)
    "lift":    dict(f="IMG_1401.mp4", act=(7.35, 8.9), pre=6.2, post=8.95, kb=(1.00, 1.04), cy=TOP),   # cover atas meja -> DIBUKA (graf)
    "flip_c":  dict(f="IMG_1409.mp4", act=(0.0, 1.45), pre=0.0, post=1.95, kb=(1.00, 1.04), cy=TOP),   # cover dalam tangan -> DIBUKA
    "flip_b":  dict(f="IMG_1402.mp4", act=(3.0, 4.4), pre=2.0, post=4.7, kb=(1.00, 1.04), cy=TOP),     # cover -> selak tebal -> TERBUKA
    "flip_a":  dict(f="IMG_1395.mp4", act=(0.0, 1.15), pre=0.0, post=1.3, kb=(1.00, 1.04), cy=TOP),    # cover dalam tangan -> DIBUKA (rajah bulatan)
    "pages_e": dict(f="IMG_1392.mp4", act=(11.9, 13.1), pre=11.0, post=13.9, kb=(1.00, 1.04), cy=TOP), # cover atas meja -> DIBUKA (soalan)
    "pages_c": dict(f="IMG_1401.mp4", act=(8.9, 9.8), pre=8.75, post=10.2, kb=(1.00, 1.04), cy=TOP),   # selak 1 muka surat lengkap
    # selak berterusan dalam tangan (riffle) - boleh potong bila-bila
    "riffle_a": dict(f="IMG_1395.mp4", ms=2.0, win=(1.3, 16.0), kb=(1.00, 1.04), cy=TOP),
    "riffle_c": dict(f="IMG_1409.mp4", ms=3.2, win=(3.0, 10.0), kb=(1.00, 1.04), cy=TOP),
    # badge cover (USP)
    "badge_fokus": dict(f="IMG_1396.mp4", ms=7.6, win=(7.6, 10.6), kb=(1.00, 1.02), o="40% 40%", cy=BOT),  # 3 badge: FOKUS SOALAN BERPOTENSI TINGGI
    "badge_skema": dict(f="IMG_1396.mp4", ms=8.3, win=(7.6, 10.6), kb=(1.00, 1.02), o="40% 50%", cy=BOT),  # SKEMA JAWAPAN LENGKAP & TERATUR
    "badge_kalk":  dict(f="IMG_1396.mp4", ms=8.8, win=(7.6, 10.6), kb=(1.00, 1.02), o="40% 60%", cy=BOT),  # jari dekat PERCUMA BENGKEL KALKULATOR
    "kalk2":       dict(f="IMG_1398.mp4", ms=1.0, win=(0.6, 2.6), kb=(1.00, 1.02), o="20% 30%", cy=1470),  # badge PERCUMA BENGKEL KALKULATOR
    "badges":      dict(f="IMG_1397.mp4", ms=2.9, win=(2.8, 3.9), kb=(1.00, 1.02), o="40% 20%", cy=BOT),  # semua badge
    "spm_badge":   dict(f="IMG_1398.mp4", ms=3.6, win=(3.4, 7.0), kb=(1.00, 1.06), o="70% 55%", cy=BOT),  # badge 'BERDASARKAN FORMAT TERKINI SPM'
    # isi buku (statik)
    "toc":     dict(f="IMG_1403.mp4", ms=4.0, win=(3.0, 12.0), kb=(1.00, 1.06), cy=TOP),        # isi kandungan (topik), jari
    "formula": dict(f="IMG_1404.mp4", ms=0.0, win=(0.0, 0.9), kb=(1.00, 1.06), cy=TOP),         # halaman rumus
    "pages_a": dict(f="IMG_1392.mp4", ms=13.15, win=(13.1, 13.9), kb=(1.00, 1.05), cy=TOP),     # buku terbuka atas meja (soalan)
    "pages_b": dict(f="IMG_1404.mp4", ms=4.0, win=(3.8, 6.6), kb=(1.00, 1.05), cy=TOP),         # buku terbuka atas meja (graf)
    "pages_d": dict(f="IMG_1393.mp4", ms=2.5, win=(2.0, 7.5), kb=(1.00, 1.05), cy=TOP),         # halaman soalan (rajah)
    "graph":   dict(f="IMG_1391.mp4", ms=1.3, win=(1.25, 2.6), kb=(1.00, 1.05), cy=TOP),        # halaman grid terbuka
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
# Shot statik ganti bila aksi tak sempat habis sebelum sebutan seterusnya
STATIC_ALT = {"lift": "hold", "flip_c": "riffle_c", "flip_b": "riffle_a", "flip_a": "riffle_a", "pages_e": "pages_d", "pages_c": "pages_b"}
# Shot pengganti bila shot sama bersebelahan (sempadan unit) atau diguna semula dalam video yang sama
ALT = {"hold": "pick", "hold2": "lift", "flip_b": "riffle_a", "flip_c": "riffle_c", "riffle_a": "riffle_c", "riffle_c": "riffle_a", "pages_b": "graph", "pages_c": "pages_a",
       "tbl": "flat", "flat": "tbl", "lift": "hold", "spm_badge": "badges", "badge_fokus": "badges", "close": "footage",
       "pick": "hold", "flip_a": "riffle_a", "spine": "pick", "pages_d": "pages_e", "pages_e": "pages_d", "pages_a": "graph"}

# ---- Pengguna: "cari footage yang hold lama, slow-mo, dia buka" ----
# HO = shot panjang PEGANG cover lama -> BUKA sampai habis (act lengkap, pre = bahagian pegang).
# Mengisi ruang antara shot 'sebutan' (badge/isi kandungan) - satu shot panjang, bukan potongan pendek.
SHOT.update({
    "ho_1392": dict(f="IMG_1392.mp4", act=(11.9, 13.1), pre=9.6, post=13.9, kb=(1.00, 1.05), cy=TOP),  # pegang cover atas meja -> buka (soalan)
    "ho_1400": dict(f="IMG_1400.mp4", act=(4.3, 6.5), pre=1.6, post=6.6, kb=(1.00, 1.04), cy=TOP),     # pegang cover -> buka (selak)
    "ho_1402": dict(f="IMG_1402.mp4", act=(2.0, 4.4), pre=0.8, post=4.7, kb=(1.00, 1.04), cy=TOP),     # pegang cover -> selak tebal terbuka
    "ho_1401": dict(f="IMG_1401.mp4", act=(7.35, 8.9), pre=6.2, post=8.95, kb=(1.00, 1.04), cy=TOP),   # cover atas meja -> buka (graf)
    "ho_1390": dict(f="IMG_1390.mp4", act=(1.45, 2.05), pre=0.25, post=2.1, kb=(1.00, 1.04), cy=TOP),   # pegang cover atas meja -> buka (rumus)
    "ho_1409": dict(f="IMG_1409.mp4", act=(0.0, 1.45), pre=0.0, post=1.95, kb=(1.00, 1.04), cy=TOP),   # cover dalam tangan -> buka
    "ho_1395": dict(f="IMG_1395.mp4", act=(0.0, 1.15), pre=0.0, post=1.3, kb=(1.00, 1.04), cy=TOP),    # cover dalam tangan -> buka
})
HO = ["ho_1392", "ho_1400", "ho_1401", "ho_1390"]
HO_QUICK = ["ho_1409", "ho_1395"]   # buka terus (tiada pegang) - pilihan terakhir   # ho_1402 dibuang: cover terlalu tinggi masa pegang (caption kena cover)
NO_FIRST = {"ho_1409"}   # cover rapat ke atas frame -> tak sesuai untuk hook (frame 0)
HOLD_MIN = 1.2           # saat (output) minimum bahagian PEGANG sebelum buka
# shot 'sebutan' = dikekalkan tepat pada cue (benda yang VO sebut). Lain-lain = shot umum -> diganti HO panjang.
KEY = {"badge_fokus", "badge_skema", "badge_kalk", "kalk2", "badges", "spm_badge", "toc", "formula", "footage"}
# penutup CTA: pegang cover lama (statik, tak dibuka)
END_HOLD = ["hold2", "tbl", "close", "flat", "hold", "pick"]
# ruang pendek (< HO terpendek): halaman terbuka statik / selak berterusan
SHORT_FILL = ["pages_b", "pages_d", "graph", "riffle_a", "riffle_c", "pages_a"]

# ---- Pengguna (v01 lulus, maklum balas): "cover masuk depan, tengah, belakang je. Yang lain isi-isi,
#      banyak angle (ke sana, ke sini, ke tepi, ke kanan), selak-selak. Animation nak power." ----
# INNER = isi buku dari pelbagai sudut (julat statik/selak berterusan; tiada cover, tiada iklan buku lain, tiada cover belakang)
SHOT.update({
    "in_1392":  dict(f="IMG_1392.mp4", ms=14.0, win=(13.2, 21.5), cy=TOP),   # atas meja, pandangan atas, selak
    "in_1393":  dict(f="IMG_1393.mp4", ms=3.0,  win=(2.0, 9.6),  cy=TOP),    # meja, sudut condong, tangan
    "in_1395a": dict(f="IMG_1395.mp4", ms=1.5,  win=(1.3, 8.5),  cy=TOP),    # dalam tangan, condong kanan, selak
    "in_1395b": dict(f="IMG_1395.mp4", ms=9.0,  win=(8.5, 16.2), cy=TOP),
    "in_1400":  dict(f="IMG_1400.mp4", ms=6.8,  win=(6.6, 12.8), cy=TOP),    # dalam tangan, condong kiri, selak
    "in_1401":  dict(f="IMG_1401.mp4", ms=14.3, win=(14.2, 17.5), cy=TOP),    # atas meja, selak muka surat
    "in_1402":  dict(f="IMG_1402.mp4", ms=8.2,  win=(8.0, 11.6), cy=TOP),    # dalam tangan, tebal, selak laju (sebelum 8 s nampak cover belakang hitam)
    "in_1403":  dict(f="IMG_1403.mp4", ms=1.0,  win=(0.0, 12.0), cy=TOP),    # isi kandungan + jari (diagonal)
    "in_1404a": dict(f="IMG_1404.mp4", ms=0.5,  win=(0.0, 6.6),  cy=TOP),    # atas meja, rumus/graf
    "in_1404b": dict(f="IMG_1404.mp4", ms=7.0,  win=(6.6, 12.0), cy=TOP),
    "in_1409":  dict(f="IMG_1409.mp4", ms=3.4,  win=(3.3, 9.8), cy=TOP),    # selak ke arah kamera
    "in_1391":  dict(f="IMG_1391.mp4", ms=0.0,  win=(0.0, 4.0),  cy=TOP),    # grid, selak
})
INNER = ["in_1401", "in_1395a", "in_1404a", "in_1400", "in_1393", "in_1409", "in_1392", "in_1402", "in_1391", "in_1395b", "in_1404b", "in_1403"]
COVER_FRONT_STATIC = ["tbl", "flat", "hold", "close"]     # hook pendek (tak muat buka): cover statik
# gerakan kamera digital (sudut berbeza): (dari, ke) {scale, x, y, rotation}
MOVES = [
    ({"scale": 1.00}, {"scale": 1.12}),                                   # push in
    ({"scale": 1.14, "x": 60}, {"scale": 1.14, "x": -60}),                # pan kiri
    ({"scale": 1.12}, {"scale": 1.00}),                                   # pull out
    ({"scale": 1.14, "x": -60}, {"scale": 1.14, "x": 60}),                # pan kanan
    ({"scale": 1.12, "rotation": -2.5}, {"scale": 1.12, "rotation": 2.5}),  # condong
    ({"scale": 1.14, "y": 50}, {"scale": 1.14, "y": -50}),                # naik
]
TRANS = ["zoomblur", "whipL", "spin", "whipR", "flash"]   # peralihan shot laju (power)

# ---- Pengguna: "kadang-kadang apa yang kau sebut tak sama apa yang kau tunjuk" ----
# KEYCUES = shot SEBUTAN ikut masa PERKATAAN dalam pipeline/vo.json (saat relatif unit, selepas 1.1x).
# Hanya benda yang betul-betul disebut; selain ini = isi buku (soalan/latihan) pelbagai sudut.
KEYCUES = {
    "i_235A": [(1.60, "badge_skema")],                    # "skema jawapan" 1.7
    "i_48FA": [(3.95, "badge_skema")],                    # "skema jawapan lengkap" 4.1
    "i_70D5": [(5.95, "badge_skema")],                    # "baru cek skema" 6.1
    "i_A559": [(3.05, "badge_fokus")],                    # "soalan fokus berpotensi tinggi" 3.3
    "i_BD48": [(1.20, "badge_fokus")],                    # "fokus pada soalan berpotensi tinggi" 1.3
    "i_C83B": [(0.00, "footage")],                        # pegang buku (hook)
    "t_3454": [(0.95, "badge_kalk"), (4.80, "kalk2")],    # "bonus rakaman bengkel kalkulator" 1.0 / "cara penggunaan kalkulator" 4.9
    "t_96DE": [(2.60, "badge_fokus"), (4.55, "spm_badge")],   # "fokus pada soalan" 2.7 / "tinggi untuk SPM" 4.7
    "t_E6E5": [(1.85, "spm_badge"), (4.05, "badges")],    # "persiapan akhir SPM" 1.9 / "soalan fokus, skema, bonus bengkel" 4.1-6.4
    "f_full": [(0.00, "footage"), (3.20, "badge_fokus"), (5.55, "spm_badge"), (7.10, "badge_skema"), (8.45, "toc"), (9.25, "formula")],
}

# halaman JAWAPAN / ANSWERS sebenar (IMG_1401 13.0-14.0 s) -> bila VO sebut "skema jawapan"
SHOT["jawapan"] = dict(f="IMG_1401.mp4", ms=12.95, win=(12.9, 14.05), kb=(1.00, 1.04), cy=TOP)
KEY.add("jawapan"); ALT["jawapan"] = "badge_skema"
for _u, _c in KEYCUES.items():
    KEYCUES[_u] = [(t, "jawapan" if k == "badge_skema" else k) for t, k in _c]
