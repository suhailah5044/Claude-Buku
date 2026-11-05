#!/usr/bin/env python3
"""9 varian hook - Kuasai Algebra Dua (gaya Reel AI Edit, saiz font = video utama yang lulus).
Peraturan #14: setiap varian berbeza KESELURUHAN - hook lain, susunan isi lain, panjang lain,
shot footage lain untuk topik sama (putaran pool), ayat caption lain (3 versi), animasi masuk lain.
Semua suara = suara asal pengguna (potong dalam senyap, fade 10 ms, jeda 0.08 s, kemudian 1.1x).
Footage dipilih ikut apa yang disebut (peraturan #19): menambah algebra -> halaman langkah kerja,
topik -> Kandungan, buku/form -> cover, latihan/QR -> Set Latihan (ada QR jawapan bervideo).
Guna: python3 pipeline/variants.py [h01 ...]  -> variants/hNN/ (index.html, sfx.json, assets/)"""
import html, json, os, re, shutil, subprocess, sys, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(HERE)
RAW = os.environ.get("RAW", "/home/user/raw-dua")       # Dua.MOV, tm.mp4 (tone-map), a48.wav
SPD, FPS, GAP, ACC = 1.1, 30, 0.08, "#FFC21A"
rich = lambda s: re.sub(r"\*(.+?)\*", r'<b class="hi">\1</b>', html.escape(s))

# ---- segmen suara (masa asal Dua.MOV, titik potong disemak dalam senyap + transcribe semula) ----
SEG = {
    "sm":    [(0.00, 1.62)],            # Kalau anak dah masuk sekolah menengah,
    "intro": [(0.00, 4.785)],           # ... topik menambah algebra ni antara yang kena kuasai, nampak macam susah
    "tk":    [(1.62, 4.785)],           # topik menambah algebra ni antara yang kena kuasai, nampak macam susah
    "ss":    [(4.06, 4.785)],           # nampak macam susah
    "tp":    [(4.785, 6.86)],           # Tapi bila dah tahu tekniknya, lebih mudah kita nak buat
    "tq":    [(4.98, 6.86)],            # Bila dah tahu tekniknya, lebih mudah kita nak buat
    "bk":    [(6.86, 8.53)],            # Buku Kuasai Algebra ni bukan ada topik ni je tau
    "tl":    [(8.53, 14.74)],           # Dalamnya ada asas, ... persamaan linear
    "ft":    [(14.74, 18.76)],          # Siap ada nota ringkas, contoh, latihan dan juga video tutorial melalui QR code
    "fm":    [(18.76, 20.54)],          # Sesuai untuk belajar form 1 sampai form 5
    "cta":   [(20.54, 24.78)],          # Kalau korang tengah cari buku ... boleh dapatkan buku ini dekat beg kuning
    "ca":    [(20.54, 23.03)],          # Kalau korang tengah cari buku untuk bantu anak kuasai algebra
    "cb":    [(23.03, 24.78)],          # boleh dapatkan buku ini dekat beg kuning
    "smfm":  [(0.00, 1.62), (18.76, 20.54)],   # Kalau anak dah masuk sekolah menengah, sesuai untuk belajar form 1 sampai form 5
    "bkft":  [(6.86, 7.95), (14.88, 18.76)],   # Buku Kuasai Algebra ni ada nota ringkas, contoh, latihan ... QR code
}
LIST = {
    0: [(9.18, "01", "asas", "*ASAS & OPERASI* ALGEBRA", [9.92]), (10.82, "02", "pecahan", "*PECAHAN* ALGEBRA", []),
        (11.98, "03", "kembangan", "*KEMBANGAN* ALGEBRA", []), (12.64, "04", "faktor", "*PEMFAKTORAN* ALGEBRA", []),
        (13.80, "05", "linear", "*PERSAMAAN LINEAR*", [])],
    1: [(15.16, "01", "nota", "*NOTA* RINGKAS", []), (15.82, "02", "contoh", "*CONTOH*", []),
        (16.22, "03", "latihan", "*LATIHAN*", []), (16.90, "04", "video", "VIDEO TUTORIAL *QR CODE*", [])],
}
# caption: 3 versi setiap segmen. sm = caption kecil (mula segmen), big = (masa, tajuk, saiz asas), sm2 = (masa, baris kecil kedua), list
CAPS = {
    "intro": [dict(sm="TOPIK *WAJIB KUASAI*", big=(2.32, "MENAMBAH ALGEBRA", 140), sm2=(4.06, "NAMPAK MACAM *SUSAH*...")),
              dict(sm="ANAK DAH MASUK *SEKOLAH MENENGAH*?", big=(3.34, "KENA KUASAI", 160), sm2=(4.06, "NAMPAK MACAM *SUSAH*...")),
              dict(sm="MASUK *SEKOLAH MENENGAH*", big=(1.88, "MENAMBAH ALGEBRA", 140), sm2=(4.06, "NAMPAK *SUSAH*?"))],
    "tk":    [dict(sm="TOPIK *MENAMBAH ALGEBRA*", big=(3.34, "WAJIB KUASAI", 160), sm2=(4.06, "NAMPAK MACAM *SUSAH*?"))] * 3,
    "ss":    [dict(sm="NAMPAK MACAM", big=(4.42, "SUSAH?", 170))] * 3,
    "tp":    [dict(sm="TAPI BILA DAH TAHU *TEKNIKNYA*", big=(6.06, "LEBIH *MUDAH*", 170)),
              dict(sm="BILA DAH TAHU *TEKNIK*", big=(6.14, "*MUDAH*!", 170)),
              dict(sm="TAPI BILA TAHU *TEKNIKNYA*", big=(6.06, "LEBIH MUDAH NAK BUAT", 120))],
    "tq":    [dict(sm="BILA DAH TAHU *TEKNIKNYA*", big=(6.06, "LEBIH *MUDAH*", 170))] * 3,
    "bk":    [dict(sm="BUKU *KUASAI ALGEBRA* NI", big=(7.92, "BUKAN TOPIK NI JE!", 116)),
              dict(sm="BUKAN TOPIK NI *JE* TAU", big=(7.08, "KUASAI ALGEBRA", 140)),
              dict(sm="BUKU *KUASAI ALGEBRA*", big=(8.02, "BUKAN SATU TOPIK", 116))],
    "tl":    [dict(big=(8.53, "DALAMNYA ADA", 104), list=0),
              dict(sm="DALAMNYA ADA", list=0),
              dict(big=(8.53, "ISI KANDUNGAN", 104), list=0)],
    "ft":    [dict(big=(14.74, "SIAP ADA", 118), list=1),
              dict(sm="SIAP ADA", list=1),
              dict(big=(14.74, "SIAP ADA!", 118), list=1)],
    "fm":    [dict(sm="SESUAI UNTUK BELAJAR", big=(19.38, "FORM *1 – 5*", 170)),
              dict(sm="SESUAI UNTUK", big=(19.38, "FORM 1 SAMPAI FORM 5", 110)),
              dict(sm="BELAJAR DARI", big=(19.38, "*FORM 1* – *FORM 5*", 140))],
    "cta":   [dict(sm="NAK BANTU ANAK?", big=(22.02, "KUASAI ALGEBRA", 150), sm2=(23.03, "BOLEH *DAPATKAN* BUKU INI!")),
              dict(sm="TENGAH CARI BUKU?", big=(22.02, "KUASAI ALGEBRA", 150), sm2=(23.03, "BOLEH *DAPATKAN* BUKU INI!")),
              dict(sm="BANTU ANAK", big=(22.02, "KUASAI ALGEBRA", 150), sm2=(23.03, "*DAPATKAN* BUKU INI!"))],
    "ca":    [dict(sm="TENGAH CARI BUKU UNTUK ANAK?", big=(22.02, "KUASAI ALGEBRA", 150))] * 3,
    "cb":    [dict(sm="BOLEH *DAPATKAN*", big=(23.32, "BUKU INI!", 160))] * 3,
    "smfm":  [dict(sm="ANAK DAH MASUK *SEKOLAH MENENGAH*?", big=(19.38, "FORM *1 – 5*", 170))] * 3,
    "bkft":  [dict(sm="BUKU", big=(7.08, "KUASAI ALGEBRA", 150), list=1)] * 3,
}
# shot ikut perkataan (masa asal) -> pool footage
BEATS = [(0.00, "ALG"), (1.62, "ALG"), (4.06, "ALG"), (6.06, "ALG"), (6.86, "COVER"), (7.92, "KAND"), (8.53, "KAND"),
         (10.82, "KAND"), (12.64, "KAND"), (14.74, "NOTA"), (15.82, "ALG"), (16.22, "LAT"), (17.40, "LAT"), (18.76, "COVER"),
         (19.70, "LAT"), (20.54, "LAT"), (22.02, "COVER"), (23.03, "LAT")]
POOL = {   # julat dalam footage asal (antara potongan CapCut), (mula, tamat, kelajuan)
    "ALG":   [(0.03, 2.20, 1), (3.63, 7.24, 1), (17.76, 18.94, 1), (2.27, 3.57, 1)],
    "KAND":  [(7.30, 9.67, 1), (9.73, 11.37, 1), (11.43, 13.74, 1), (13.80, 16.17, 1), (16.23, 17.70, 1)],
    "NOTA":  [(16.23, 17.70, 1), (13.80, 16.17, 1)],
    "COVER": [(19.05, 19.47, 1)],   # cover: main ke frame paling tajam (19.45 s) kemudian pegang (tiada slow-mo blend - kabur)
    "LAT":   [(19.70, 21.67, 1), (21.73, 23.17, 1), (23.23, 24.45, 1)],
}
# (id, [(segmen, versi)], animasi kecil, animasi tajuk, animasi baris, arah ken burns)
VARS = [
    ("h01", [("ss", 0), ("tp", 0), ("bk", 0), ("tl", 1), ("ft", 0), ("cta", 0)], "slide", "slam", "right", 1),
    ("h02", [("fm", 0), ("intro", 1), ("bk", 2), ("tl", 0), ("cta", 1)], "drop", "zoomblur", "pop", -1),
    ("h03", [("bk", 0), ("tl", 2), ("ft", 1), ("fm", 2), ("cta", 2)], "zoom", "stretch", "drop", 1),
    ("h04", [("ft", 0), ("intro", 0), ("tp", 2), ("cta", 0)], "flip", "slideup", "left", -1),
    ("h05", [("ca", 0), ("ft", 2), ("tl", 0), ("fm", 1), ("cb", 0)], "rise", "slam", "pop", 1),
    ("h06", [("tk", 0), ("tp", 0), ("tl", 2), ("fm", 0), ("cta", 2)], "slide", "stretch", "drop", -1),
    ("h07", [("smfm", 0), ("tl", 1), ("ft", 0), ("cta", 0)], "drop", "slideup", "right", 1),
    ("h08", [("tq", 0), ("ft", 1), ("bk", 1), ("tl", 0), ("cta", 1)], "zoom", "zoomblur", "left", -1),
    ("h09", [("bkft", 0), ("fm", 1), ("intro", 2), ("cta", 2)], "flip", "slam", "pop", 1),
]
SM_IN = {
    "rise":  '{opacity:0,y:26,clipPath:"inset(0 0 100% 0)"},{opacity:1,y:0,clipPath:"inset(0 0 0% 0)",duration:.32,ease:"power3.out"}',
    "slide": '{opacity:0,x:-140,skewX:-14},{opacity:1,x:0,skewX:0,duration:.34,ease:"back.out(1.8)"}',
    "drop":  '{opacity:0,y:-60},{opacity:1,y:0,duration:.45,ease:"bounce.out"}',
    "zoom":  '{opacity:0,scale:1.8,filter:"blur(8px)"},{opacity:1,scale:1,filter:"blur(0px)",duration:.3,ease:"expo.out"}',
    "flip":  '{opacity:0,rotationX:-100,transformPerspective:500,transformOrigin:"50% 0%"},{opacity:1,rotationX:0,duration:.42,ease:"back.out(2)"}',
}
BIG_IN = {
    "zoomblur": '{opacity:0,scale:1.6,filter:"blur(14px)"},{opacity:1,scale:1,filter:"blur(0px)",duration:.34,ease:"expo.out"}',
    "slam":     '{opacity:0,scale:2.6,rotation:-6},{opacity:1,scale:1,rotation:0,duration:.3,ease:"power4.in"}',
    "stretch":  '{opacity:0,scaleX:.2,scaleY:1.5},{opacity:1,scaleX:1,scaleY:1,duration:.4,ease:"elastic.out(1,.55)"}',
    "slideup":  '{opacity:0,y:70,clipPath:"inset(0 0 100% 0)"},{opacity:1,y:0,clipPath:"inset(0 0 0% 0)",duration:.36,ease:"power4.out"}',
}
ROW_IN = {
    "left":  '{opacity:0,x:-70,filter:"blur(8px)"},{opacity:1,x:0,filter:"blur(0px)",duration:.32,ease:"back.out(1.7)"}',
    "right": '{opacity:0,x:80,filter:"blur(8px)"},{opacity:1,x:0,filter:"blur(0px)",duration:.32,ease:"back.out(1.7)"}',
    "pop":   '{opacity:0,scale:.4},{opacity:1,scale:1,duration:.34,ease:"back.out(2.6)"}',
    "drop":  '{opacity:0,y:-40,rotationX:-70,transformPerspective:500},{opacity:1,y:0,rotationX:0,duration:.36,ease:"back.out(2)"}',
}
ICON = {
    "asas": '<rect x="3" y="13" width="8" height="8" rx="1.5"/><rect x="13" y="13" width="8" height="8" rx="1.5"/><rect x="8" y="3" width="8" height="8" rx="1.5"/>',
    "pecahan": '<circle cx="12" cy="5.5" r="1.6"/><line x1="4" y1="12" x2="20" y2="12"/><circle cx="12" cy="18.5" r="1.6"/>',
    "kembangan": '<path d="M9 4H4v5M15 4h5v5M9 20H4v-5M15 20h5v-5"/>',
    "faktor": '<path d="M8 4c-3 3-3 13 0 16M16 4c3 3 3 13 0 16"/><line x1="10" y1="12" x2="14" y2="12"/>',
    "linear": '<line x1="5" y1="9" x2="19" y2="9"/><line x1="5" y1="15" x2="19" y2="15"/>',
    "nota": '<path d="M6 3h9l4 4v14H6z"/><path d="M15 3v4h4M9 12h7M9 16h7"/>',
    "contoh": '<path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-4 10.5c.8.8 1 1.5 1 2.5h6c0-1 .2-1.7 1-2.5A6 6 0 0 0 12 3z"/>',
    "latihan": '<path d="M4 20l1-5L16 4l4 4L9 19z"/><path d="M14 6l4 4"/>',
    "video": '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><path d="M14 14h3v3h-3zM19 19h2v2h-2zM14 20h2M20 14v3"/>',
}
TITLE_SCALE = .54                  # sama dengan video utama (pengguna minta kecil)
TITLE_MAX = 92                     # px

def load_audio():
    w = wave.open(f"{RAW}/a48.wav"); return np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768

def layout(segs):
    """Pulangkan senarai bahagian: (segmen, versi, julat asal, dst_mula) + fungsi peta masa asal->dst."""
    parts, t = [], 0.0
    for k, (sid, ver) in enumerate(segs):
        rngs = []
        for a, b in SEG[sid]:
            rngs.append((a, b, t)); t += (b - a) / SPD
        parts.append((sid, ver, rngs))
        t += GAP / SPD
    return parts, round(t - GAP / SPD + 0.35, 3)

def mapt(rngs, x):
    for a, b, d in rngs:
        if x < b - 1e-6: return round(d + max(0, x - a) / SPD, 3)
    a, b, d = rngs[-1]; return round(d + (b - a) / SPD, 3)

def make_vo(parts, dur, path):
    A = load_audio(); SR = 48000
    pieces = []
    for k, (sid, ver, rngs) in enumerate(parts):
        for a, b, d in rngs:
            x = A[int(a * SR):int(b * SR)].copy(); f = int(0.010 * SR)
            x[:f] *= np.linspace(0, 1, f); x[-f:] *= np.linspace(1, 0, f)
            pieces.append(x)
        pieces.append(np.zeros(int(GAP * SR), np.float32))
    raw = np.concatenate(pieces[:-1])
    tmp = path + ".raw.wav"
    w = wave.open(tmp, "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(raw, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", f"atempo={SPD},apad", "-t", str(dur), "-ac", "1", "-ar", "48000", path], check=True)
    os.unlink(tmp)

def plan_shots(parts, dur, vno):
    """Shot ikut BEATS dalam setiap julat; pool berputar (vno) supaya varian guna shot lain untuk topik sama."""
    beats = []
    for sid, ver, rngs in parts:
        for a, b, d in rngs:
            inside = [(t, p) for t, p in BEATS if a - 1e-6 <= t < b - 0.3]
            first = [p for t, p in BEATS if t <= a + 1e-6][-1]
            if not inside or inside[0][0] > a + 0.05: inside = [(a, first)] + inside
            for t, p in inside: beats.append((mapt(rngs, max(t, a)), p))
    beats.sort()
    m = []                                       # gabung shot terlalu pendek (< 0.8 s)
    for i, (t, p) in enumerate(beats):
        nxt = beats[i + 1][0] if i + 1 < len(beats) else dur
        if m and (t - m[-1][0] < 0.8 or nxt - t < 0.5) and i: continue
        m.append((t, p))
    rot = {k: (vno * 2 + len(k)) for k in POOL}
    shots, last = [], None
    for i, (t, p) in enumerate(m):
        need = (m[i + 1][0] if i + 1 < len(m) else dur) - t
        while need > 0.02:
            if p == "COVER" and shots and shots[-1][3] == "COVER": p = "LAT"
            n = len(POOL[p]); cand = [POOL[p][(rot[p] + q) % n] for q in range(n)]; rot[p] += 1
            cand = [c for c in cand if (c[0], c[1]) != last] or cand
            fit = [c for c in cand if (c[1] - c[0]) / c[2] >= need]          # utamakan shot yang cukup panjang
            s, e, sp = (fit or sorted(cand, key=lambda c: -(c[1] - c[0]) / c[2]))[0]
            avail = (e - s) / sp
            if p == "COVER": avail = max(avail, 1.6)                 # frame akhir dipegang (tpad clone)
            take = min(need, avail)
            if 0 < need - take < 0.6 and take > 1.2: take = need - 0.6 if p != "COVER" else take   # elak sisa < 0.6 s
            slack = avail - take
            off = 0 if p == "COVER" else (slack * ((vno * 37 + i * 13) % 100) / 100) * sp
            shots.append([round(t, 3), round(take, 3), (round(s + off, 3), sp), p])
            last = (s, e); t += take; need -= take
            if need > 0.02 and p == "COVER": p = "LAT"
    return shots

def make_video(shots, dur, path, work):
    os.makedirs(work, exist_ok=True); lst = []
    total_f = round(dur * FPS); used = 0
    for k, (t, d, (src, sp), p) in enumerate(shots):
        nf = round((t + d) * FPS) - used if k < len(shots) - 1 else total_f - used
        if nf <= 0: continue
        used += nf
        f = f"{work}/s{k:02d}.mp4"
        vf = f"setpts={1/sp}*(PTS-STARTPTS),fps={FPS}"
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(src), *(["-t", str(round(POOL["COVER"][0][1] - src, 3))] if p == "COVER" else []), "-i", f"{RAW}/tm.mp4", "-vf", vf + ",tpad=stop_mode=clone:stop_duration=2",
                        "-frames:v", str(nf), "-an", "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", f], check=True)
        lst.append(f"file '{f}'")
    open(f"{work}/list.txt", "w").write("\n".join(lst))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{work}/list.txt", "-c", "copy", path], check=True)

def html_doc(parts, shots, dur, anim):
    sm_in, big_in, row_in, kb = anim
    body, js, sfx = [], [], []
    ov = lambda t: sfx.append([round(t, 3), "ov"])
    for g, (sid, ver, rngs) in enumerate(parts):
        c = CAPS[sid][ver]; hook = g == 0
        s = rngs[0][2]; e = mapt(rngs, rngs[-1][1]) + (GAP / SPD if g < len(parts) - 1 else 1)
        e = min(e, dur)
        body.append(f'<div class="grp" id="g{g}">')
        if c.get("sm"): body.append(f'<div class="sm" id="g{g}s">{rich(c["sm"])}</div>')
        if c.get("big"):
            bt, txt, fs = c["big"]; px = min(TITLE_MAX, round(fs * TITLE_SCALE))
            body.append(f'<div class="big" id="g{g}b" style="font-size:{px}px">{rich(txt)}</div>')
        if c.get("sm2"): body.append(f'<div class="sm sm2" id="g{g}x">{rich(c["sm2"][1])}</div>')
        body.append('</div>')
        if hook:   # hook penuh pada frame 0 (thumbnail) - sm2 & list masih ikut masa
            js.append(f'tl.fromTo("#g{g}",{{scale:1}},{{scale:1.05,duration:.22,ease:"power2.out",yoyo:true,repeat:1}},0.3);')
        else:
            js.insert(0, f'tl.set("#g{g}",{{opacity:0}},0);'); js.append(f'tl.set("#g{g}",{{opacity:1}},{s});')
            if c.get("sm"): js.append(f'tl.fromTo("#g{g}s",{SM_IN[sm_in]},{s});'); ov(s)
            if c.get("big"):
                bt = max(s, mapt(rngs, c["big"][0]))
                js.append(f'tl.fromTo("#g{g}b",{BIG_IN[big_in]},{bt});')
                js.append(f'tl.fromTo("#cam",{{scale:1}},{{scale:1.05,duration:.13,ease:"expo.out",yoyo:true,repeat:1,immediateRender:false}},{bt});'); ov(bt)
        if c.get("sm2"):
            xt = mapt(rngs, c["sm2"][0])
            js.append(f'tl.fromTo("#g{g}x",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.3,ease:"back.out(2)"}},{xt});'); ov(xt)
        if g < len(parts) - 1:
            js.append(f'tl.to("#g{g}",{{opacity:0,y:-14,duration:.18,ease:"power2.in"}},{round(e-.2,3)});')
        if "list" in c:
            rows = LIST[c["list"]]
            body.append(f'<div class="list" id="l{g}">')
            for r, (rt, num, ic, txt, _) in enumerate(rows):
                body.append(f'<div class="row" id="l{g}r{r}"><i class="bar"></i><span class="n">{num}</span>'
                            f'<svg viewBox="0 0 24 24" class="ic">{ICON[ic]}</svg><span class="tx">{rich(txt)}</span></div>')
            body.append('</div>')
            js.insert(0, f'tl.set("#l{g} .row",{{opacity:0}},0);')
            for r, (rt, num, ic, txt, pulses) in enumerate(rows):
                t = max(s + .1, mapt(rngs, rt) - .05)
                js.append(f'tl.fromTo("#l{g}r{r}",{ROW_IN[row_in]},{t});')
                js.append(f'tl.fromTo("#l{g}r{r} .bar",{{scaleY:0}},{{scaleY:1,duration:.22,ease:"power2.out"}},{t+.1});')
                js.append(f'tl.fromTo("#l{g}r{r} .hi",{{color:"#ffffff"}},{{color:"{ACC}",duration:.2}},{t+.1});')
                if r:
                    js.append(f'tl.to("#l{g}r{r-1} .bar",{{scaleY:0,duration:.18}},{t+.1});')
                    js.append(f'tl.to("#l{g}r{r-1} .hi",{{color:"#ffffff",duration:.2}},{t+.1});')
                    js.append(f'tl.to("#l{g}r{r-1}",{{opacity:.78,duration:.2}},{t+.1});')
                for p in pulses:
                    js.append(f'tl.fromTo("#l{g}r{r}",{{scale:1}},{{scale:1.05,duration:.14,ease:"power2.out",yoyo:true,repeat:1,immediateRender:false}},{mapt(rngs,p)});')
                ov(t)
            if g < len(parts) - 1:
                js.append(f'tl.to("#l{g}",{{opacity:0,y:20,duration:.2,ease:"power2.in"}},{round(e-.22,3)});')
    for t, d, src, p in shots[1:]:
        sfx.append([t, "tr"])
    a, b = (1.0, 1.05) if kb > 0 else (1.05, 1.0)
    js.append(f'tl.fromTo("#bg",{{scale:{a}}},{{scale:{b},duration:{dur},ease:"none"}},0);')
    src = open(f"{PROJ}/index.html").read()
    css = src[src.index("<style>"):src.index("</style>") + 8]
    doc = f"""<!doctype html>
<html lang="ms">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
{css}
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{dur}" data-width="1080" data-height="1920">
<div id="cam">
<div id="bg"><video id="v" src="assets/aroll.mp4" data-start="0" data-duration="{dur}" data-track-index="2" class="clip" muted playsinline></video></div>
</div>
<audio id="vo" src="assets/vo.wav" data-start="0" data-duration="{dur}" data-track-index="1" data-has-audio="true"></audio>
{chr(10).join(body)}
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
    return doc, sorted(sfx)

def build(vid):
    n = [v[0] for v in VARS].index(vid); _, segs, *anim = VARS[n]
    D = f"{PROJ}/variants/{vid}"; os.makedirs(f"{D}/assets", exist_ok=True)
    parts, dur = layout(segs)
    make_vo(parts, dur, f"{D}/assets/vo.wav")
    shots = plan_shots(parts, dur, n + 1)
    make_video(shots, dur, f"{D}/assets/aroll.mp4", f"/home/user/work-dua/{vid}")
    if not os.path.exists(f"{D}/assets/fonts"): shutil.copytree(f"{PROJ}/assets/fonts", f"{D}/assets/fonts")
    for f in ("package.json", "hyperframes.json"): shutil.copy(f"{PROJ}/{f}", D)
    doc, sfx = html_doc(parts, shots, dur, anim)
    open(f"{D}/index.html", "w").write(doc); json.dump(sfx, open(f"{D}/sfx.json", "w"))
    json.dump({"segments": segs, "dur": dur, "shots": shots}, open(f"{D}/plan.json", "w"), indent=1)
    print(vid, "dur", dur, "shots", [(s[0], s[3]) for s in shots])

if __name__ == "__main__":
    for v in (sys.argv[1:] or [v[0] for v in VARS]): build(v)
