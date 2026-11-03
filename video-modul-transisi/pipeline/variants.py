#!/usr/bin/env python3
"""9 varian hook untuk Modul Transisi Tahun 1 (2027) - SETIAP varian berbeza keseluruhan,
bukan intro sahaja (pengguna: "part tengah-tengah kena olah, ubah-ubah juga"):

1. hook: satu ayat Sue dibawa ke depan + kad hook (frame 0) + pembukaan berbeza (b-roll / muka)
2. SUSUNAN isi berbeza (produk dulu / sebab dulu / semak tahap dulu ...)
3. PANJANG berbeza (buang unit tertentu) - tetapi 5 info pop-up wajib sentiasa ada
4. B-ROLL berbeza untuk topik yang sama (klip / bahagian klip / arah zoom lain)
5. AYAT CAPTION berbeza (3 versi setiap caption) + subtajuk kad berbeza
6. ANIMASI masuk overlay berbeza (pop / slide / drop / zoom / flip) + kedudukan teks
Semua ayat = suara asal Sue (tiada ayat direka). Gaya = pipeline/style_v1.py.

Unit (k) = kumpulan segmen A-roll:
 0 intro "ibu ayah anak 6 tahun"   1 kenal huruf/suku kata/tulis/kira   2 ingat anak dah okay
 3 penting persediaan (kad #1)     4 bukan berjam-jam, 10-15 minit       5 share modul edisi 2027
 6 5 subjek (kad #3)               7 kemahiran 4M (kad #2)               8 menaakul
 9 video tutorial & jawapan (kad #4)  10 teman anak, tahap (kad #5)     11 dah okay / masih lemah
 12 bukan pandai sehari, lebih yakin  13 CTA
Guna:  WORK=/home/user/work python3 pipeline/variants.py [id ...]"""
import copy, json, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import style_v1 as S
WORK = os.environ.get("WORK", "/home/user/work")
AROLL = os.environ.get("AROLL", f"{WORK}/aroll.mp4")
OUT = f"{PROJ}/variants"
FPS = 30
fr = lambda t: round(round(t * FPS) / FPS, 4)

SEG = {s["seg"]: (s["start"], s["end"]) for s in S.EDL["segments"]}
GROUPS = [[0], [1, 2], [3], [4], [5], [6], [7], [8], [9], [10, 11], [12], [13, 14], [15, 16, 17], [18]]
SPAN = [(fr(SEG[g[0]][0]), fr(SEG[g[-1]][1])) for g in GROUPS]
SPAN[-1] = (SPAN[-1][0], S.DUR)
MUST = {3, 6, 7, 9, 10}          # unit yang ada info pop-up wajib

VARIANTS = [
 dict(id="v01_boleh_baca", hook=1, H=3.0, label="MAK AYAH, CUBA CHECK", lines=["ANAK DAH", "BOLEH *BACA?*"],
      open=("IMG_1278", 0.0, 2.6, 0.2, (1.08, 1.00), "45% 55%"),
      body=[0, 5, 6, 7, 8, 2, 3, 9, 10, 11, 4, 12, 13], enter="pop", y0=200, alt=0, bro=0),
 dict(id="v02_10_minit", hook=4, H=3.2, label="TAK PERLU BERJAM-JAM", lines=["CUMA *10–15 MINIT*", "SEHARI!"],
      body=[1, 2, 3, 5, 7, 6, 9, 10, 0, 13], enter="slide", y0=215, alt=1, bro=1),
 dict(id="v03_ingat_ready", hook=2, H=3.2, label="ANAK MASUK TAHUN 1 2027?", lines=["INGAT ANAK", "DAH *READY?*"],
      open=("IMG_1279", 0.0, 2.6, 3.0, (1.00, 1.06), "50% 50%"),
      body=[0, 1, 3, 10, 11, 5, 6, 7, 8, 9, 12, 4, 13], enter="drop", y0=190, alt=2, bro=2),
 dict(id="v04_5_subjek", hook=6, H=3.0, label="MODUL TRANSISI TAHUN 1", lines=["*5 SUBJEK*", "DALAM 1 BUKU!"],
      open=("IMG_1274", 0.0, 2.8, 0.3, (1.00, 1.08), "50% 60%"),
      body=[5, 7, 9, 1, 3, 10, 12, 13], enter="zoom", y0=205, alt=0, bro=1),
 dict(id="v05_video_tutorial", hook=9, H=3.2, label="BUKU LATIHAN TAHUN 1", lines=["SIAP *VIDEO TUTORIAL*", "& JAWAPAN!"],
      open=("IMG_1274", 0.0, 3.2, 0.0, (1.55, 1.70), "28% 88%"),   # mula terus zoom pada badge (beza dari v04)
      body=[0, 10, 11, 5, 6, 7, 1, 2, 3, 4, 12, 13], enter="flip", y0=200, alt=1, bro=2),
 dict(id="v06_bukan_pandai", hook=12, H=3.4, label="MAK AYAH, INGAT NI", lines=["BUKAN NAK ANAK", "PANDAI *DALAM SEHARI*"],
      body=[0, 3, 4, 1, 2, 5, 6, 7, 8, 9, 10, 11, 13], enter="slide", y0=190, alt=2, bro=0),
 dict(id="v07_kemahiran_4m", hook=7, H=3.0, label="SEBELUM MASUK TAHUN 1", lines=["DAH KENAL", "KEMAHIRAN *4M?*"],
      open=("IMG_1276", 0.0, 2.6, 0.0, (1.00, 1.07), "50% 40%"),
      body=[8, 1, 5, 6, 9, 10, 3, 12, 0, 13], enter="drop", y0=210, alt=0, bro=2),
 dict(id="v08_lemah_mana", hook=11, H=3.2, label="MAK AYAH TAHU TAK?", lines=["ANAK LEMAH", "*DEKAT MANA?*"],
      body=[0, 10, 2, 1, 5, 7, 6, 9, 3, 4, 12, 13], enter="zoom", y0=195, alt=1, bro=0),
 dict(id="v09_edisi_2027", hook=5, H=3.0, label="BARU SAMPAI!", lines=["PERSEDIAAN TAHUN 1", "*EDISI 2027!*"],
      body=[6, 7, 9, 10, 1, 2, 3, 12, 13], enter="flip", y0=215, alt=2, bro=1),
]

# --- ayat caption: 3 versi (alt 0 = versi video utama)
ALT = {
 "Menulis & *kira nombor?*": ["Menulis & *kira nombor?*", "Boleh tulis? *Boleh kira?*", "*Menulis* & *mengira?*"],
 "Ingat anak dah *okay?*": ["Ingat anak dah *okay?*", "Rasa anak *dah ready?*", "Anak *dah okay* ke?"],
 "Baru nampak yang *belum kuasai*": ["Baru nampak yang *belum kuasai*", "Rupanya ada yang *belum kuasai*", "Baru nampak *kelemahan* dia"],
 "Bukan paksa *berjam-jam*": ["Bukan paksa *berjam-jam*", "Tak perlu *berjam-jam*", "Bukan *paksa* belajar"],
 "*10–15 minit* sehari pun cukup": ["*10–15 minit* sehari pun cukup", "Cukup *10–15 minit* sehari", "Sehari *10–15 minit* je!"],
 "Modul Transisi *Tahun 1 • 2027*": ["Modul Transisi *Tahun 1 • 2027*", "*Edisi 2027* dah ada!", "Modul *Transisi Tahun 1*"],
 "Menaakul = *belajar berfikir*": ["Menaakul = *belajar berfikir*", "Menaakul: *latih anak berfikir*", "Ajar anak *berfikir*"],
 "Dah okay? *Teruskan!*": ["Dah okay? *Teruskan!*", "Yang dah okay, *teruskan*", "Dah kuasai? *Next!*"],
 "Bukan nak pandai *dalam sehari*": ["Bukan nak pandai *dalam sehari*", "Bukan *pandai sekelip mata*", "Bukan nak *paksa pandai*"],
 "*Ready* masuk Tahun 1!": ["*Ready* masuk Tahun 1!", "Lebih *yakin* ke Tahun 1!", "Masuk Tahun 1 *dengan yakin!*"],
 "Jom buat *persediaan awal!*": ["Jom buat *persediaan awal!*", "*Prepare awal* dari sekarang!", "Jom *mula sekarang!*"],
 "INTRO": ["Anak *6 tahun?* 2027 masuk *Tahun 1!*", "*2027* anak masuk *Tahun 1?*", "Anak *6 tahun* tahun ni?"],
}
SUB = {
 "1": ["Biasakan anak dengan aktiviti belajar", "Supaya anak tak kekok masuk sekolah", "Mula biasakan dari sekarang"],
 "4": ["Senang bimbing anak di rumah", "Bantu mak ayah bimbing anak", "Boleh semak jawapan sendiri"],
 "5": ["Mana dah kuasai, mana perlu bantu", "Tahu kekuatan & kelemahan anak", "Fokus pada yang masih lemah"],
}
# --- b-roll alternatif ikut indeks S.BROLL: (fail, media_start, kenburns, origin)
ALTB = [
 [("page:page_abc.png", 0, (1.00, 1.05), "50% 50%"), ("page:page_abc.png", 0, (1.00, 1.09), "50% 25%"), ("page:page_abc.png", 0, (1.06, 1.00), "50% 30%")],
 [("IMG_1278", 0.6, (1.06, 1.00), "45% 55%"), ("IMG_1279", 0.0, (1.00, 1.06), "40% 50%"), ("IMG_1278", 1.6, (1.00, 1.10), "50% 70%")],
 [("IMG_1279", 0.5, (1.00, 1.06), "50% 50%"), ("IMG_1280", 0.0, (1.06, 1.00), "50% 50%"), ("IMG_1272", 1.0, (1.00, 1.07), "50% 40%")],
 [("IMG_1272", 4.0, (1.00, 1.06), "50% 50%"), ("IMG_1277", 0.0, (1.00, 1.06), "50% 30%"), ("IMG_1279", 12.0, (1.06, 1.00), "50% 50%")],
 [("IMG_1273", 0.0, (1.08, 1.00), "50% 40%"), ("IMG_1274", 1.0, (1.08, 1.00), "50% 30%"), ("IMG_1273", 1.0, (1.00, 1.10), "50% 75%")],
 [("IMG_1276", 0.0, (1.00, 1.06), "50% 40%"), ("IMG_1275", 0.0, (1.06, 1.00), "50% 40%"), ("IMG_1277", 0.5, (1.00, 1.06), "50% 40%")],
 [("IMG_1279", 7.6, (1.00, 1.06), "50% 50%"), ("IMG_1272", 8.0, (1.06, 1.00), "50% 50%"), ("IMG_1279", 14.0, (1.00, 1.06), "50% 40%")],
 [("IMG_1274", 0.0, (1.00, 1.14), "30% 82%"), ("IMG_1273", 0.6, (1.00, 1.12), "75% 85%"), ("IMG_1274", 1.2, (1.10, 1.00), "40% 75%")],
 [("IMG_1280", 0.4, (1.00, 1.06), "50% 50%"), ("IMG_1272", 6.0, (1.00, 1.06), "50% 50%"), ("IMG_1279", 9.0, (1.06, 1.00), "50% 50%")],
]

def plan(v):
    assert v["body"][-1] == 13 and v["hook"] not in v["body"]
    order = [v["hook"]] + v["body"]
    missing = MUST - set(order)
    assert not missing, (v["id"], missing)
    starts, t = {}, 0.0
    for k in order:
        starts[k] = round(t, 4); t += SPAN[k][1] - SPAN[k][0]
    return order, starts, round(t, 3)

def grp(t):
    for k, (a, b) in enumerate(SPAN):
        if a - 0.06 <= t < b - 0.06: return k      # elemen yg mula di sempadan ayat ikut ayat seterusnya
    return len(SPAN) - 1

def build(v):
    order, starts, DUR = plan(v)
    hg, H, alt = v["hook"], v["H"], v["alt"]
    M = lambda k, t: round(starts[k] + t - SPAN[k][0], 3)
    els = []
    for el in S.EL:
        k = grp(el["s"])
        if k not in starts: continue
        p = copy.deepcopy(el)
        a, b = SPAN[k]
        ns, ne = M(k, el["s"]), M(k, min(el["e"], b))
        if p["k"] == "hook" and k == 0:
            p = dict(k="cap", text=ALT["INTRO"][alt])
        if p.get("text") in ALT: p["text"] = ALT[p["text"]][alt]
        if p["k"] == "card" and p.get("sub") and p["num"] in SUB: p["sub"] = SUB[p["num"]][alt]
        if k == hg:
            ns = max(ns, H + 0.05)
            if ne - ns < 1.0: continue
        p["s"], p["e"] = ns, ne
        clamp = lambda x: min(max(M(k, x), ns), ne)
        if p.get("items"): p["items"] = [(tx, clamp(x)) for tx, x in p["items"]]
        p.pop("final", None)
        if k == order[-1] and b - min(el["e"], b) < 0.5:
            p["e"], p["final"] = DUR, True
        els.append(p)
    els.insert(0, dict(k="hook", s=0.0, e=H, label=v["label"], lines=v["lines"], nohide=True))
    els.sort(key=lambda p: p["s"])
    op = v.get("open")
    broll = []
    if op:
        broll.append((op[0], 0.0, op[2], op[3], op[4], op[5], None))
    for i, (f, s, e, ms, kb, o, tag) in enumerate(S.BROLL):
        k = grp(s)
        if k not in starts: continue
        f, ms, kb, o = ALTB[i][(v["bro"] + i) % len(ALTB[i])]
        ns, ne = M(k, s), M(k, min(e, SPAN[k][1]))
        if op and (ns < op[2] + 0.3 or (k == hg and f == op[0])): continue
        if k == hg and ns < H + 0.1: tag = None
        broll.append((f, ns, ne, ms, kb, o, tag))
    broll.sort(key=lambda x: x[1])
    punch = {M(grp(p), p) for p in S.PUNCH if grp(p) in starts} | {0.45}
    if v["alt"] != 0:                                   # varian lain: punch pada permulaan unit juga
        punch |= {round(starts[k] + 0.15, 3) for k in order[2::2]}
    segs, dy = [], {}
    for sg in S.EDL["segments"]:
        k = grp(sg["start"] + 1e-3)
        if k not in starts: continue
        a = M(k, sg["start"]); b = M(k, min(sg["end"], SPAN[k][1]))
        segs.append((a, b)); dy[a] = 110 if 68.3 <= sg["start"] < 79.1 else 0
    segs.sort()
    return order, starts, DUR, els, broll, sorted(punch), segs, dy

def make_aroll(order, path):
    """Potong setiap unit ke fail berasingan (sempadan frame -> A/V sync), kemudian concat."""
    tmp = f"{WORK}/vtmp"; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    for n, k in enumerate(order):
        a, b = SPAN[k]
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.4f}", "-i", AROLL, "-t", f"{b-a:.4f}",
                        "-af", f"afade=t=in:d=0.008,afade=t=out:st={b-a-0.01:.4f}:d=0.01,apad,atrim=0:{b-a:.4f}",
                        "-c:v", "libx264", "-crf", "14", "-preset", "veryfast", "-r", "30", "-c:a", "pcm_s16le", f"{tmp}/u{n:02d}.mov"], check=True)
    open(f"{tmp}/list.txt", "w").write("".join(f"file 'u{n:02d}.mov'\n" for n in range(len(order))))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{tmp}/list.txt", "-c:v", "libx264", "-crf", "16",
                    "-preset", "fast", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", path], check=True)

if __name__ == "__main__":
    only = sys.argv[1:]
    S.SOUND_ALL = "toing"
    for v in VARIANTS:
        if only and v["id"] not in only: continue
        order, starts, DUR, els, broll, punch, segs, dy = build(v)
        P = f"{OUT}/{v['id']}"
        os.makedirs(f"{P}/assets/broll", exist_ok=True); os.makedirs(f"{P}/compositions", exist_ok=True)
        for f in os.listdir(f"{PROJ}/assets/broll"):
            dst = f"{P}/assets/broll/{f}"
            if os.path.exists(dst): os.unlink(dst)
            os.link(f"{PROJ}/assets/broll/{f}", dst)
        for f in ("hyperframes.json", "package.json"):
            shutil.copy(f"{PROJ}/{f}", P)
        json.dump({"name": v["id"]}, open(f"{P}/meta.json", "w"))
        neworder = [GROUPS[k] for k in order]
        if os.environ.get("SKIP_AROLL") is None:
            make_aroll(order, f"{P}/assets/aroll.mp4")
        S.CAM_DY = lambda t, dy=dy: dy.get(t, 0)
        S.ENTER = v["enter"]
        doc, sfx = S.build_gfx(els, dur=DUR, broll=broll, y0=v["y0"])
        open(f"{P}/compositions/gfx.html", "w").write(doc)
        open(f"{P}/index.html", "w").write(S.build_root(DUR, broll, punch, segs, [("gfx", 0, DUR)]))
        json.dump(sfx, open(f"{P}/sfx.json", "w"))
        json.dump(dict(order=neworder, dur=DUR, hook=v), open(f"{P}/variant.json", "w"), ensure_ascii=False, indent=1)
        print(v["id"], f"{DUR:.1f}s", "order", order, "| enter", v["enter"], "| sfx", len(sfx), "| broll", [b[0] for b in broll], flush=True)
