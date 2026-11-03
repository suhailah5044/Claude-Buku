#!/usr/bin/env python3
"""9 varian hook untuk Modul Transisi Tahun 1 (2027) dari footage yang sama.

Setiap varian:
- bawa SATU unit ayat Sue ke depan sebagai hook + kad hook (kelihatan dari frame 0),
- ayat pembuka asal ("ibu ayah yang ada anak 6 tahun...") jadi ayat kedua,
- unit lain ikut susunan asal; sesetengah varian buang unit tertentu (versi lebih pendek)
  TETAPI 5 info pop-up wajib kekal (unit 4, 7, 8, 10, 12 tidak dibuang),
- pembukaan berbeza: b-roll (suku kata / flip / subjek / badge video / kandungan) atau muka + zoom punch.
Overlay, b-roll & zoom punch ikut unit masing-masing. Gaya = pipeline/style_v1.py.

Guna:  WORK=/home/user/work python3 pipeline/variants.py [id ...]
Output: variants/<id>/ (index.html, compositions/gfx.html, sfx.json, assets/aroll.mp4)"""
import copy, json, os, shutil, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import style_v1 as S
WORK = os.environ.get("WORK", "/home/user/work")
AROLL = os.environ.get("AROLL", f"{WORK}/aroll.mp4")      # A-roll kualiti penuh (video utama)
OUT = f"{PROJ}/variants"
FPS = 30
fr = lambda t: round(round(t * FPS) / FPS, 4)

SEG = {s["seg"]: (s["start"], s["end"]) for s in S.EDL["segments"]}
GROUPS = [[0], [1, 2], [3], [4], [5], [6], [7], [8], [9], [10, 11], [12], [13, 14], [15, 16, 17], [18]]
SPAN = [(fr(SEG[g[0]][0]), fr(SEG[g[-1]][1])) for g in GROUPS]
SPAN[-1] = (SPAN[-1][0], S.DUR)
gi = lambda seg: next(k for k, g in enumerate(GROUPS) if seg in g)

VARIANTS = [
 dict(id="v01_boleh_baca", hook=[1, 2], H=3.0, label="MAK AYAH, CUBA CHECK", lines=["ANAK DAH", "BOLEH *BACA?*"],
      open=("IMG_1278", 0.0, 2.6, 0.2, (1.08, 1.00), "45% 55%")),
 dict(id="v02_10_minit", hook=[5], H=3.2, label="TAK PERLU BERJAM-JAM", lines=["CUMA *10–15 MINIT*", "SEHARI!"], drop=[9, 13]),
 dict(id="v03_ingat_ready", hook=[3], H=3.2, label="ANAK MASUK TAHUN 1 2027?", lines=["INGAT ANAK", "DAH *READY?*"],
      open=("IMG_1279", 0.0, 2.6, 3.0, (1.00, 1.06), "50% 50%")),
 dict(id="v04_5_subjek", hook=[7], H=3.0, label="MODUL TRANSISI TAHUN 1", lines=["*5 SUBJEK*", "DALAM 1 BUKU!"], drop=[3, 9],
      open=("IMG_1274", 0.0, 2.8, 0.3, (1.00, 1.08), "50% 60%")),
 dict(id="v05_video_tutorial", hook=[10, 11], H=3.2, label="BUKU LATIHAN TAHUN 1", lines=["SIAP *VIDEO TUTORIAL*", "& JAWAPAN!"],
      open=("IMG_1274", 0.0, 3.2, 0.0, (1.00, 1.16), "30% 82%")),
 dict(id="v06_bukan_pandai", hook=[15, 16, 17], H=3.4, label="MAK AYAH, INGAT NI", lines=["BUKAN NAK ANAK", "PANDAI *DALAM SEHARI*"]),
 dict(id="v07_kemahiran_4m", hook=[8], H=3.0, label="SEBELUM MASUK TAHUN 1", lines=["DAH KENAL", "KEMAHIRAN *4M?*"], drop=[5, 13]),
 dict(id="v08_lemah_mana", hook=[13, 14], H=3.2, label="MAK AYAH TAHU TAK?", lines=["ANAK LEMAH", "*DEKAT MANA?*"]),
 dict(id="v09_edisi_2027", hook=[6], H=3.0, label="BARU SAMPAI!", lines=["PERSEDIAAN TAHUN 1", "*EDISI 2027!*"], drop=[9]),
]
REPL = {"hook": "Anak *6 tahun?* 2027 masuk *Tahun 1!*"}   # kad hook asal jadi caption biasa

def plan(v):
    hg = gi(v["hook"][0]); dropg = {gi(x) for x in v.get("drop", [])}
    order = [hg, 0] + [k for k in range(len(GROUPS)) if k not in (hg, 0) and k not in dropg]
    starts, t = {}, 0.0
    for k in order:
        starts[k] = round(t, 4); t += SPAN[k][1] - SPAN[k][0]
    return hg, order, starts, round(t, 3)

def build(v):
    hg, order, starts, DUR = plan(v)
    H = v["H"]
    def grp(t):
        for k, (a, b) in enumerate(SPAN):
            if a - 0.06 <= t < b - 0.06: return k      # toleransi: elemen yg mula di sempadan ayat ikut ayat seterusnya
        return len(SPAN) - 1
    M = lambda k, t: round(starts[k] + t - SPAN[k][0], 3)
    els = []
    for el in S.EL:
        k = grp(el["s"])
        if k not in starts: continue
        p = copy.deepcopy(el)
        a, b = SPAN[k]
        ns, ne = M(k, el["s"]), M(k, min(el["e"], b))
        if p["k"] == "hook" and k == 0:
            p = dict(k="cap", text=REPL["hook"])
        if k == hg:
            ns = max(ns, H + 0.05)
            if ne - ns < 1.0: continue
        p["s"], p["e"] = ns, ne
        clamp = lambda x: min(max(M(k, x), ns), ne)
        if p.get("items"): p["items"] = [(tx, clamp(x)) for tx, x in p["items"]]
        if p.get("final") or k == order[-1] and b - min(el["e"], b) < 0.5:
            p["e"], p["final"] = DUR, True
        els.append(p)
    els.insert(0, dict(k="hook", s=0.0, e=H, label=v["label"], lines=v["lines"], nohide=True))
    els.sort(key=lambda p: p["s"])
    # b-roll ikut unit
    op = v.get("open")
    broll = []
    if op:
        f, ms, d, *_r = op
        broll.append((f, 0.0, d, ms, op[4], op[5], None))
    for f, s, e, ms, kb, o, tag in S.BROLL:
        k = grp(s)
        if k not in starts: continue
        ns, ne = M(k, s), M(k, min(e, SPAN[k][1]))
        if op and (ns < op[2] + 0.3 or (k == hg and f == op[0])): continue     # elak bertindih/berulang dgn pembuka
        if k == hg and ns < H + 0.1: tag = None                                 # jangan tindih kad hook
        broll.append((f, ns, ne, ms, kb, o, tag))
    broll.sort(key=lambda x: x[1])
    punch = sorted({M(grp(p), p) for p in S.PUNCH if grp(p) in starts} | {0.45})
    segs, dy = [], {}
    for sg in S.EDL["segments"]:
        k = grp(sg["start"] + 1e-3)
        if k not in starts: continue
        a = M(k, sg["start"]); b = M(k, min(sg["end"], SPAN[k][1]))
        segs.append((a, b)); dy[a] = 110 if 68.3 <= sg["start"] < 79.1 else 0
    segs.sort()
    return order, starts, DUR, els, broll, punch, segs, dy

def make_aroll(order, path):
    """Potong setiap unit ke fail berasingan (sempadan frame -> A/V sync), kemudian concat."""
    tmp = f"{WORK}/vtmp"; shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    for n, k in enumerate(order):
        a, b = SPAN[k]
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.4f}", "-i", AROLL, "-t", f"{b-a:.4f}",
                        "-af", f"afade=t=in:d=0.008,afade=t=out:st={b-a-0.01:.4f}:d=0.01,apad,atrim=0:{b-a:.4f}",
                        "-c:v", "libx264", "-crf", "14", "-preset", "fast", "-r", "30", "-c:a", "pcm_s16le", f"{tmp}/u{n:02d}.mov"], check=True)
    open(f"{tmp}/list.txt", "w").write("".join(f"file 'u{n:02d}.mov'\n" for n in range(len(order))))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{tmp}/list.txt", "-c:v", "libx264", "-crf", "16",
                    "-preset", "medium", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-movflags", "+faststart", path], check=True)

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
        if not os.path.exists(f"{P}/assets/aroll.mp4") or os.environ.get("REDO_AROLL"):
            make_aroll(order, f"{P}/assets/aroll.mp4")
        S.CAM_DY = lambda t, dy=dy: dy.get(t, 0)
        doc, sfx = S.build_gfx(els, dur=DUR, broll=broll)
        open(f"{P}/compositions/gfx.html", "w").write(doc)
        open(f"{P}/index.html", "w").write(S.build_root(DUR, broll, punch, segs, [("gfx", 0, DUR)]))
        json.dump(sfx, open(f"{P}/sfx.json", "w"))
        json.dump(dict(order=[GROUPS[k] for k in order], dur=DUR, hook=v), open(f"{P}/variant.json", "w"), ensure_ascii=False, indent=1)
        print(v["id"], f"{DUR:.1f}s", "units", [GROUPS[k][0] for k in order], "| sfx", len(sfx), "| broll", len(broll), flush=True)
