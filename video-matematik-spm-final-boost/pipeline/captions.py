"""Caption setiap unit VO (masa = saat relatif dalam unit, selepas 1.1x; rujuk pipeline/vo.json).
Gaya #13: pendek, satu pada satu masa, *perkataan* = kuning. TIADA teks 'bakul/beg kuning'.
k: cap (pil kecil) | card (tajuk + sub / item ✓) | hook (kad hook unit pertama, penuh dari frame 0)
punch=True -> zoom punch kecil pada footage."""

# Kad hook (hanya bila unit ialah unit PERTAMA video). e = tamat (saat).
HOOKS = {
    "i_189E": dict(e=2.45, label="CALON SPM, INGAT NI", lines=["JANGAN TUNGGU", "*LAST MINUTE!*"]),
    "i_235A": dict(e=2.25, label="BUKU LATIHAN SPM", lines=["SIAP DENGAN", "*SKEMA JAWAPAN!*"]),
    "i_2C72": dict(e=1.85, label="MATEMATIK SPM", lines=["BUKAN SEKADAR", "*BACA TEORI!*"]),
    "i_4557": dict(e=2.50, label="CALON SPM", lines=["SPM DAH", "*MAKIN DEKAT!*"], sub="Persiapan korang macam mana?"),
    "i_48FA": dict(e=1.90, label="TENGAH SUSUN ULANGKAJI?", lines=["MASUKKAN DALAM", "*LIST SPM* KORANG"]),
    "i_70D5": dict(e=1.45, label="CALON SPM", lines=["MASIH ADA MASA", "SEBELUM *SPM!*"]),
    "i_A559": dict(e=1.60, label="CALON SPM", lines=["LATIHAN MATEMATIK", "*MASIH TAK CUKUP?*"]),
    "i_BD48": dict(e=1.25, label="MATEMATIK SPM", lines=["KENAPA SAYA", "*TERTARIK?*"]),
    "i_C83B": dict(e=1.85, label="PARENTS,", lines=["ANAK NAK", "AMBIL *SPM?*"]),
    "i_EC6D": dict(e=2.75, label="BUKU YANG BOLEH KORANG TENGOK", lines=["UNTUK PERSIAPAN", "*MATEMATIK SPM*"]),
    "f_full": dict(e=2.45, label="REVIEW BUKU", lines=["MATEMATIK SPM", "*FINAL BOOST*"]),
}

CAPS = {
    # ---------------- INTRO
    "i_189E": [dict(k="cap", s=2.45, text="Matematik SPM *Final Boost*", punch=True),
               dict(k="cap", s=4.30, text="Latihan & *prepare* sebelum exam")],
    "i_235A": [dict(k="cap", s=2.25, text="Dah jawab? *Terus semak!*", punch=True),
               dict(k="cap", s=3.55, text="Tahu mana *perlu improve*")],
    "i_2C72": [dict(k="cap", s=1.85, text="Kena *banyak latihan!*", punch=True),
               dict(k="cap", s=3.30, text="Bahan *revision* sebelum SPM")],
    "i_4557": [dict(k="cap", s=2.55, text="*Extra praktis* sementara ada masa", punch=True)],
    "i_48FA": [dict(k="cap", s=1.90, text="Matematik SPM *Final Boost*"),
               dict(k="cap", s=3.05, text="Latihan + *skema jawapan lengkap*", punch=True)],
    "i_70D5": [dict(k="cap", s=1.45, text="Buat *lebih banyak latihan*", punch=True),
               dict(k="cap", s=3.85, text="Jangan *sekadar baca*"),
               dict(k="cap", s=4.70, text="Jawab dulu, *baru cek skema*")],
    "i_A559": [dict(k="cap", s=1.60, text="Tambah *1 buku* untuk revision"),
               dict(k="cap", s=3.05, text="Soalan *berpotensi tinggi*", punch=True)],
    "i_BD48": [dict(k="cap", s=1.25, text="Fokus soalan *berpotensi tinggi*", punch=True),
               dict(k="cap", s=3.80, text="Latihan tambahan *final revision*")],
    "i_C83B": [dict(k="cap", s=1.85, text="Consider *Matematik SPM Final Boost*", punch=True),
               dict(k="cap", s=3.70, text="*Extra latihan* di rumah")],
    "i_EC6D": [dict(k="cap", s=2.75, text="Namanya *Final Boost*", punch=True),
               dict(k="cap", s=3.90, text="Bantu calon *ulangkaji & latihan*")],
    # ---------------- TENGAH (USP)
    "t_3454": [dict(k="card", s=0.95, e=4.75, num="✓", title="BONUS RAKAMAN", sub="Bengkel penggunaan kalkulator", punch=True),
               dict(k="cap", s=4.80, text="Cara guna *kalkulator*"),
               dict(k="cap", s=7.65, text="Ulang tengok *bila-bila masa*")],
    "t_96DE": [dict(k="cap", s=0.00, text="Apa yang *menarik?*"),
               dict(k="card", s=2.60, e=5.70, num="✓", title="FOKUS SOALAN", sub="Berpotensi tinggi untuk SPM", punch=True),
               dict(k="cap", s=5.75, text="Bukan latihan *tanpa arah*"),
               dict(k="cap", s=7.40, text="Bahan *final revision*")],
    "t_E6E5": [dict(k="cap", s=0.00, text="Cari *extra material?*"),
               dict(k="cap", s=1.85, text="Persiapan *akhir SPM*"),
               dict(k="card", s=4.00, e=6.90, num="3", title="DALAM BUKU NI", punch=True,
                    items=[("Soalan fokus", 4.15), ("Skema jawapan lengkap", 4.85), ("Bonus bengkel kalkulator", 5.65)]),
               dict(k="cap", s=6.95, text="Bahan tambahan *latihan sendiri*")],
    "f_full": [dict(k="cap", s=1.65, text="Dari *Cikgu Yasir*"),
               dict(k="card", s=2.50, e=6.05, num="✓", title="FOKUS SOALAN", sub="Berpotensi tinggi untuk SPM", punch=True),
               dict(k="card", s=6.10, e=10.05, num="3", title="SIAP DALAM BUKU", punch=True,
                    items=[("Skema jawapan tersusun", 7.15), ("Macam-macam topik", 8.25), ("Rumusan matematik", 9.10)]),
               dict(k="cap", s=10.10, text="Sesuai untuk *final revision*")],
    # ---------------- CTA (tiada teks bakul/beg kuning)
    "c_3EF9": [dict(k="cap", s=0.30, text="Jangan tunggu *last minute!*"),
               dict(k="cap", s=2.05, text="Berminat? *Terus checkout!*", big=True, punch=True)],
    "c_4EE9": [dict(k="cap", s=0.00, text="Cari *final preparation* SPM?"),
               dict(k="cap", s=1.85, text="*Dapatkan* buku ni!", big=True, punch=True)],
    "c_C62F": [dict(k="cap", s=0.00, text="Masih *ada masa* lagi!"),
               dict(k="cap", s=2.35, text="Grab *Final Boost* ni!", big=True, punch=True)],
    "c_E3ED": [dict(k="cap", s=0.00, text="Sesuai untuk *persiapan SPM?*"),
               dict(k="cap", s=2.60, text="Klik & *tengok details!*", big=True, punch=True)],
    "c_F20C": [dict(k="cap", s=0.00, text="Parents *calon SPM*,"),
               dict(k="cap", s=1.75, text="Boleh *consider* buku ni!", big=True, punch=True)],
}
