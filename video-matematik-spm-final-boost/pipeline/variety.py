"""Peraturan #14: setiap video mesti berbeza KESELURUHAN (bukan intro je).
Unit VO yang sama dipakai dalam beberapa video -> setiap kali (occ = kali ke-berapa unit itu muncul) dapat:
- ayat caption lain (3 versi: occ 0 = asal dalam captions.py, occ 1/2 = di bawah)
- hook lain (intro dipakai 2x)
- set b-roll lain untuk topik yang sama (shot masih ikut apa yang disebut)
- animasi masuk caption lain (ANIMS, ikut nombor video)
Semua ayat suara = suara asal pengguna. v01 (dah lulus) = occ 0 + 'pop'."""

ANIMS = ["pop", "slide", "drop", "zoom", "flip"]

HOOK_ALT = {
    "i_189E": dict(e=2.45, label="SPM DAH DEKAT", lines=["LAST MINUTE", "*BARU NAK CARI?*"]),
    "i_235A": dict(e=2.25, label="DAH SIAP JAWAB?", lines=["TERUS SEMAK", "*SKEMA JAWAPAN!*"]),
    "i_2C72": dict(e=1.85, label="TIPS MATEMATIK SPM", lines=["BACA TEORI JE", "*TAK CUKUP!*"]),
    "i_4557": dict(e=2.50, label="CALON SPM", lines=["DAH READY", "UNTUK *SPM?*"], sub="Persiapan korang macam mana?"),
    "i_48FA": dict(e=1.90, label="SENARAI ULANGKAJI SPM", lines=["TAMBAH BUKU NI", "*DALAM LIST!*"]),
    "i_70D5": dict(e=1.45, label="SEBELUM SPM", lines=["GUNA PELUANG", "*SELAGI ADA MASA*"]),
    "i_A559": dict(e=1.60, label="MATEMATIK SPM", lines=["RASA LATIHAN", "*TAK CUKUP?*"]),
    "i_BD48": dict(e=1.25, label="BUKU MATEMATIK SPM", lines=["NI SEBAB", "*SAYA TERTARIK*"]),
    "i_C83B": dict(e=1.85, label="PARENTS,", lines=["ANAK BAKAL", "AMBIL *SPM?*"]),
    "i_EC6D": dict(e=2.75, label="CALON SPM", lines=["PERSIAPAN", "*MATEMATIK* KORANG?"]),
}

# TEXT_ALT[unit][occ-1] = senarai teks ganti ikut indeks caption (None = kekal); kad: tajuk
TEXT_ALT = {
    "i_189E": [["Buku *Final Boost* boleh bantu", "Latihan, *ready* untuk exam"]],
    "i_235A": [["Semak *mana betul*", "Kenal pasti *mana nak improve*"]],
    "i_2C72": [["Kena *buat latihan!*", "Salah satu *bahan revision*"]],
    "i_4557": [["Selagi *masih ada masa*"]],
    "i_48FA": [["*Final Boost* untuk SPM", "Ada *skema jawapan lengkap*"]],
    "i_70D5": [["*Lebih banyak* latihan", "Bukan *baca je*", "Cuba jawab, *kemudian cek skema*"]],
    "i_A559": [["*Tambah satu lagi* buku", "Fokus *soalan berpotensi tinggi*"]],
    "i_BD48": [["Soalan *berpotensi tinggi* SPM", "Untuk *final revision*"]],
    "i_C83B": [["Boleh consider *Final Boost*", "Revision *dekat rumah*"]],
    "i_EC6D": [["*Final Boost* namanya", "Untuk *ulangkaji & latihan*"]],
    "t_3454": [["Ada *bonus rakaman* kalkulator", "Tengok semula *cara guna*", "Ulang *bila-bila masa je*"],
               ["*Percuma* bengkel kalkulator", "Belajar ikut *penerangan rakaman*", "Boleh *ulang tengok*"]],
    "t_96DE": [["Yang *menarik* pasal buku ni", "Soalan *berpotensi tinggi SPM*", "Latihan *ada arah*", "Salah satu bahan *final revision*"],
               ["Kenapa *buku ni?*", "*Fokus* soalan berpotensi tinggi", "Tak lagi latihan *tanpa arah*", "Sesuai untuk *final revision*"]],
    "t_E6E5": [["Nak *extra material?*", "Untuk *persiapan akhir*", "ADA DALAM BUKU", "Latihan *sendiri sebelum exam*"],
               ["*Extra material* untuk SPM?", "Boleh *consider* buku ni", "KANDUNGAN BUKU", "Bahan *tambahan* latihan"]],
    "c_4EE9": [["*Final preparation* SPM?", "Boleh *dapatkan* buku ni!"],
               ["Tengah cari *bahan SPM?*", "*Grab* buku ni!"]],
    "c_3EF9": [["Jangan *last minute* tau!", "Berminat? *Checkout* terus!"],
               ["*Mula awal*, bukan last minute", "*Terus checkout* kalau berminat!"]],
    "c_E3ED": [["Sesuai untuk *SPM korang?*", "Tengok *details* buku ni!"],
               ["*Persiapan SPM?*", "Klik & *tengok details!*"]],
    "c_C62F": [["*Masih sempat* lagi!", "Grab *Matematik SPM Final Boost!*"]],
    "c_F20C": [["*Parents* calon SPM,", "*Extra revision* untuk anak!"]],
}

# CUES_ALT[unit][occ-1] = set b-roll lain (topik sama)
CUES_ALT = {
    "i_189E": [[(0, "flat"), (2.40, "footage"), (4.30, "pages_c")]],
    "i_235A": [[(0, "pages_c"), (1.60, "badge_skema"), (3.50, "pages_d")]],
    "i_2C72": [[(0, "flip_a"), (1.85, "pages_d"), (3.30, "lift"), (5.20, "pick")]],
    "i_4557": [[(0, "flat"), (2.55, "pick"), (4.00, "flip_a")]],
    "i_48FA": [[(0, "pages_a"), (1.90, "hold2"), (3.05, "badge_skema"), (4.80, "graph")]],
    "i_70D5": [[(0, "pages_c"), (1.45, "flip_c"), (3.85, "pages_d")]],
    "i_A559": [[(0, "flip_b"), (1.60, "lift"), (3.05, "badge_fokus")]],
    "i_BD48": [[(0, "tbl"), (1.25, "badge_fokus"), (3.80, "pages_e")]],
    "i_C83B": [[(0, "hold"), (1.85, "close"), (3.70, "pages_b"), (5.50, "flip_c")]],
    "i_EC6D": [[(0, "flat"), (2.75, "footage"), (3.90, "flip_a"), (5.90, "pages_a")]],
    "t_3454": [[(0, "lift"), (0.95, "kalk2"), (2.90, "badge_kalk"), (6.20, "pages_a"), (7.65, "flip_c")],
               [(0, "pick"), (0.95, "badge_kalk"), (3.40, "kalk2"), (6.20, "graph"), (7.65, "flip_a")]],
    "t_96DE": [[(0, "pick"), (2.60, "badge_fokus"), (4.30, "spm_badge"), (5.75, "flip_a"), (7.40, "pages_c")],
               [(0, "spine"), (2.60, "spm_badge"), (4.30, "badge_fokus"), (5.75, "flip_c"), (7.40, "toc")]],
    "t_E6E5": [[(0, "flip_a"), (1.85, "spm_badge"), (4.00, "tbl"), (6.95, "pages_b")],
               [(0, "pages_e"), (1.85, "close"), (4.00, "lift"), (6.95, "graph")]],
    "c_4EE9": [[(0, "hold"), (1.85, "tbl")], [(0, "flip_c"), (1.85, "lift")]],
    "c_3EF9": [[(0, "pick"), (2.05, "flat")], [(0, "flip_a"), (2.05, "hold2")]],
    "c_E3ED": [[(0, "close"), (2.60, "tbl")], [(0, "spm_badge"), (2.60, "lift")]],
    "c_C62F": [[(0, "flip_c"), (2.35, "tbl")]],
    "c_F20C": [[(0, "footage"), (1.75, "flat")]],
}
