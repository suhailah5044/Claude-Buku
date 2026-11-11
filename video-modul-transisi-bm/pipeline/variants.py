#!/usr/bin/env python3
"""9 varian hook - Modul Transisi BM (gaya Reel, saiz = video utama).
Peraturan #14: setiap varian berbeza KESELURUHAN - hook lain, susunan & panjang lain, ayat caption lain (3 versi), animasi masuk lain.
Talking head: video + suara dipotong BERSAMA dari assets/aroll.mp4 + assets/vo.wav (dah 1.1x, potongan dalam senyap) - sync kekal.
Masa = saat pada aroll video utama (lihat pipeline/edl.json).
Guna: python3 pipeline/variants.py [h01 ...] -> variants/hNN/ (index.html, sfx.json, assets/)"""
import html, json, os, re, shutil, subprocess, sys, wave
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(HERE)
FPS, ACC = 30, "#FFC21A"
rich = lambda s: re.sub(r"\*(.+?)\*", r'<b class="hi">\1</b>', html.escape(s))
F = lambda t: round(round(t * FPS) / FPS, 4)

# unit = julat pada aroll utama (mula, tamat) - semua sempadan dalam senyap
UNIT = {
    "hook": [(0.000, 2.333)],              # Parents, kalau anak bakal masuk tahun satu,
    "kemah": [(2.333, 11.576)],            # saya nak perkenalkan buku kemahiran asas ... Modul transisi tahun 1 ... edisi 2027
    "edisi": [(6.909, 11.576)],            # Modul transisi tahun satu yang baru ni. Ini edisi 2027.
    "subjek": [(11.576, 18.394)],          # Dalam modul ni ada sains awal, ... bahasa Melayu.
    "sesuai": [(18.394, 24.273)],          # Buku ini sesuai ... sebelum melangkah ke tahun satu.
    "bm": [(24.273, 26.848)],              # Saya nak share dengan ibu ayah bahagian bahasa Melayu ni pula.
    "kv": [(26.848, 34.667)],              # Dekat sini ada contoh latihan KV ... consonant dan juga vocal.
    "bunyi": [(34.667, 38.970)],           # Anak kita akan belajar kenal bunyi huruf, gabungan bunyi ... suku kata.
    "kvk": [(38.970, 48.121)],             # Apa yang dimaksudkan dengan suku kata KVK? K ... V ... K ...
    "bas": [(48.121, 51.757)],             # Jadi dekat sini contohnya, bas. B, A, S.
    "soalan": [(51.757, 59.757)],          # Contoh soalan je begini, dekat sini anak perlu kenal huruf ...
    "cta": [(59.757, 64.939)],             # Kalau ibu ayah nak dapatkan modul transisi ... boleh ambil set yang ini.
}
SUBJ = [(12.72, "01", "*SAINS* AWAL"), (13.86, "02", "*MATEMATIK* AWAL"), (16.04, "03", "*ENGLISH*"), (17.30, "04", "BAHASA *MELAYU*")]
KVK = [(42.96, "K", "*KONSONAN*"), (44.02, "V", "*VOKAL*"), (45.96, "K", "*KONSONAN*")]
STEP = [(54.44, "01", "*KENAL* HURUF"), (55.30, "02", "*SEBUT* BUNYI"), (55.96, "03", "*GABUNG* & BACA")]
BASL = [(50.44, "B", "K"), (51.08, "A", "V"), (51.42, "S", "K")]
# caption 3 versi / unit: sm (mula unit), big=[(masa, teks)], fs, sm2=[(masa, teks)], list=(susun, baris), bas=True, hide=(masa sorok tajuk)
CAPS = {
    "hook": [dict(sm="PARENTS, ANAK BAKAL MASUK", big=[(0.0, "*TAHUN 1*?")], fs=92),
             dict(sm="ANAK BAKAL MASUK", big=[(0.0, "TAHUN 1 *2027*?")], fs=88),
             dict(sm="IBU AYAH, PERHATIAN!", big=[(0.0, "ANAK MASUK *TAHUN 1*?")], fs=84)],
    "kemah": [dict(sm="BUKU KEMAHIRAN ASAS", big=[(4.62, "MEMBACA"), (5.42, "MENULIS"), (6.32, "MENGIRA"), (7.30, "MODUL *TRANSISI*"), (9.46, "EDISI *2027*")], fs=88),
              dict(sm="KEMAHIRAN *MEMBACA · MENULIS · MENGIRA*", big=[(7.30, "MODUL TRANSISI"), (9.46, "EDISI *2027*")], fs=88),
              dict(sm="BUKU KEMAHIRAN ASAS", big=[(4.62, "*3M* ASAS"), (7.30, "MODUL TRANSISI *2027*")], fs=86)],
    "edisi": [dict(sm="MODUL TRANSISI TAHUN 1", big=[(9.46, "EDISI *2027*")], fs=92),
              dict(sm="YANG BARU!", big=[(6.91, "MODUL *TRANSISI*"), (9.46, "EDISI *2027*")], fs=90),
              dict(sm="EDISI TERBARU", big=[(6.91, "MODUL TRANSISI *2027*")], fs=86)],
    "subjek": [dict(sm="DALAM MODUL NI ADA", list=("grid2", SUBJ)),
               dict(sm="*4 SUBJEK* DALAM SATU SET", list=("grid2", SUBJ)),
               dict(sm="APA ADA DALAM MODUL NI?", list=("grid2", SUBJ))],
    "sesuai": [dict(sm="LATIHAN UNTUK BANTU ANAK", big=[(20.52, "BIASAKAN DIRI")], fs=84, sm2=[(22.64, "SEBELUM MELANGKAH KE *TAHUN 1*")]),
               dict(sm="SESUAI JADI LATIHAN", big=[(20.52, "BIASAKAN *ANAK*")], fs=84, sm2=[(22.64, "SEBELUM MASUK *TAHUN 1*")]),
               dict(sm="BANTU ANAK BIASAKAN DIRI", big=[(22.64, "SEBELUM *TAHUN 1*")], fs=84)],
    "bm": [dict(sm="BAHAGIAN", big=[(25.94, "BAHASA *MELAYU*")], fs=84),
           dict(sm="JOM TENGOK", big=[(25.94, "*BAHASA* MELAYU")], fs=84),
           dict(sm="SUBJEK", big=[(25.94, "BAHASA *MELAYU*")], fs=84)],
    "kv": [dict(sm="CONTOH LATIHAN", big=[(28.82, "SUKU KATA *KV*")], fs=84, sm2=[(32.10, "*K* = KONSONAN  ·  *V* = VOKAL")]),
           dict(sm="LATIHAN", big=[(28.82, "SUKU KATA *KV*")], fs=84, sm2=[(32.10, "KONSONAN + *VOKAL*")]),
           dict(sm="ADA CONTOH LATIHAN", big=[(28.82, "*KV*"), (32.10, "KONSONAN + VOKAL")], fs=80)],
    "bunyi": [dict(sm="ANAK AKAN BELAJAR", big=[(35.60, "KENAL *BUNYI* HURUF")], fs=76, sm2=[(36.74, "GABUNG BUNYI JADI *SUKU KATA*")]),
              dict(sm="ANAK BELAJAR", big=[(35.60, "BUNYI HURUF"), (36.74, "JADI *SUKU KATA*")], fs=80),
              dict(sm="KENAL BUNYI HURUF", big=[(36.74, "BENTUK *SUKU KATA*")], fs=80)],
    "kvk": [dict(sm="APA MAKSUD SUKU KATA", big=[(42.00, "*KVK*?")], fs=88, hide=42.8, list=("line", KVK)),
            dict(sm="SUKU KATA", big=[(41.12, "*KVK*?")], fs=88, hide=42.8, list=("line", KVK)),
            dict(sm="KVK TU APA?", list=("line", KVK))],
    "bas": [dict(sm="CONTOHNYA", bas=True), dict(sm="CONTOH", bas=True), dict(sm="MACAM NI", bas=True)],
    "soalan": [dict(sm="CONTOH SOALAN", list=("line", STEP)),
               dict(sm="ANAK PERLU", list=("line", STEP)),
               dict(sm="SOALAN DIA MACAM NI", list=("line", STEP))],
    "cta": [dict(sm="IBU AYAH NAK DAPATKAN", big=[(61.04, "MODUL *TRANSISI*")], fs=88, sm2=[(63.60, "BOLEH AMBIL *SET* NI!")]),
            dict(sm="NAK DAPATKAN?", big=[(61.04, "MODUL TRANSISI *TAHUN 1*")], fs=80, sm2=[(63.60, "AMBIL *SET* NI!")]),
            dict(sm="JOM BUAT PERSEDIAAN AWAL!", big=[(61.04, "MODUL *TRANSISI*")], fs=88, sm2=[(63.60, "BOLEH AMBIL *SET* NI!")])],
}
# hook (unit pertama): teks penuh dari frame 0 untuk thumbnail - (sm, tajuk, saiz)
HOOK = {
    "bunyi": ("ANAK BAKAL MASUK TAHUN 1?", "KENAL *BUNYI* HURUF", 76),
    "kvk": ("ANAK DAH KENAL", "SUKU KATA *KVK*?", 84),
    "edisi": ("BARU KELUAR!", "MODUL TRANSISI *2027*", 84),
    "soalan": ("ANAK MASUK TAHUN 1?", "DAH BOLEH *BACA*?", 88),
    "subjek": ("SATU SET, *4 SUBJEK*", "MODUL *TRANSISI*", 88),
    "sesuai": ("SEBELUM MASUK TAHUN 1", "BIASAKAN *ANAK*", 88),
    "kv": ("TAHUN 1 NANTI", "SUKU KATA *KV*", 88),
}
# (id, [(unit, versi caption)], animasi kecil, tajuk, baris, arah ken burns)
VARS = [
    ("h01", [("bunyi", 0), ("hook", 0), ("kemah", 1), ("subjek", 0), ("kvk", 0), ("bas", 0), ("cta", 0)], "slide", "slam", "pop", 1),
    ("h02", [("kvk", 1), ("bas", 1), ("hook", 1), ("edisi", 0), ("bm", 0), ("kv", 0), ("soalan", 0), ("cta", 1)], "drop", "zoomblur", "drop", -1),
    ("h03", [("edisi", 1), ("subjek", 1), ("sesuai", 0), ("bm", 1), ("kvk", 0), ("bas", 2), ("cta", 2)], "zoom", "stretch", "left", 1),
    ("h04", [("hook", 0), ("sesuai", 1), ("kv", 1), ("bunyi", 2), ("soalan", 1), ("cta", 0)], "flip", "slideup", "right", -1),
    ("h05", [("soalan", 2), ("hook", 2), ("kemah", 0), ("bm", 2), ("kvk", 2), ("bas", 0), ("cta", 1)], "rise", "slam", "drop", 1),
    ("h06", [("subjek", 2), ("hook", 1), ("edisi", 2), ("bunyi", 0), ("kv", 2), ("cta", 2)], "slide", "stretch", "pop", -1),
    ("h07", [("sesuai", 2), ("kemah", 2), ("subjek", 0), ("kvk", 1), ("bas", 1), ("soalan", 0), ("cta", 0)], "drop", "slideup", "right", 1),
    ("h08", [("kv", 0), ("bunyi", 1), ("hook", 0), ("edisi", 0), ("subjek", 1), ("cta", 1)], "zoom", "zoomblur", "left", -1),
    ("h09", [("hook", 2), ("kemah", 1), ("subjek", 2), ("sesuai", 0), ("bm", 0), ("kv", 1), ("cta", 2)], "flip", "slam", "drop", 1),
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

def layout(segs):
    parts, t = [], 0.0
    for uid, ver in segs:
        rngs = []
        for a, b in UNIT[uid]:
            a, b = F(a), F(b); rngs.append((a, b, round(t, 4))); t += b - a
        parts.append((uid, ver, rngs))
    return parts, round(t, 4)

def mapt(rngs, x):
    for a, b, d in rngs:
        if x < b - 1e-6: return round(d + max(0, x - a), 3)
    a, b, d = rngs[-1]; return round(d + b - a, 3)

def make_media(parts, dur, D, work):
    os.makedirs(work, exist_ok=True); lst = []
    w = wave.open(f"{PROJ}/assets/vo.wav"); SR = w.getframerate()
    A = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    au = []
    for k, (uid, ver, rngs) in enumerate(parts):
        for j, (a, b, d) in enumerate(rngs):
            f = f"{work}/u{k:02d}{j}.mp4"; nf = round((b - a) * FPS)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.4f}", "-i", f"{PROJ}/assets/aroll.mp4", "-frames:v", str(nf), "-an",
                            "-color_trc", "bt709", "-color_primaries", "bt709", "-colorspace", "bt709",
                            "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-pix_fmt", "yuv420p", f], check=True)
            lst.append(f"file '{f}'")
            x = A[int(a * SR):int(a * SR) + int(round(nf / FPS * SR))].copy(); fd = int(0.010 * SR)
            x = np.pad(x, (0, int(round(nf / FPS * SR)) - len(x)))
            x[:fd] *= np.linspace(0, 1, fd); x[-fd:] *= np.linspace(1, 0, fd); au.append(x)
    open(f"{work}/list.txt", "w").write("\n".join(lst))
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{work}/list.txt", "-c", "copy", f"{D}/assets/aroll.mp4"], check=True)
    o = wave.open(f"{D}/assets/vo.wav", "w"); o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR)
    o.writeframes((np.clip(np.concatenate(au), -1, 1) * 32767).astype(np.int16).tobytes()); o.close()

def html_doc(parts, dur, anim):
    sm_in, big_in, row_in, kb = anim
    body, js, sfx = [], [], []
    ov = lambda t: sfx.append([round(t, 3), "ov"])
    punch = lambda t: js.append(f'tl.fromTo("#cam",{{scale:1}},{{scale:1.05,duration:.13,ease:"expo.out",yoyo:true,repeat:1,immediateRender:false}},{t});')
    for g, (uid, ver, rngs) in enumerate(parts):
        c = dict(CAPS[uid][ver]); hook = g == 0
        s = rngs[0][2]; e = dur if g == len(parts) - 1 else parts[g + 1][2][0][2]
        if hook and uid in HOOK:      # hook: caption khas penuh dari frame 0, isi lain (senarai/BAS) masih ikut masa
            hs, hb, hf = HOOK[uid]; first_t = min([t for t, _ in c.get("big", [])] + [t for t, *_ in c.get("list", (0, []))[1]] + ([BASL[0][0]] if c.get("bas") else []) + [1e9])
            c = dict(c, sm=hs, big=[(rngs[0][0], hb)] + [(t, x) for t, x in c.get("big", []) if mapt(rngs, t) > 1.0], fs=hf)
            if c.get("list") or c.get("bas"): c["hide"] = max(first_t - .1, rngs[0][0] + .5)
        bigs, fs = c.get("big", []), c.get("fs", 88)
        body.append(f'<div class="grp" id="g{g}"><div class="sm" id="g{g}s">{rich(c["sm"])}</div>')
        body.append('<div class="bigs">' + "".join(f'<div class="big" id="g{g}b{b}" style="font-size:{fs}px">{rich(t)}</div>' for b, (_, t) in enumerate(bigs)) + '</div>')
        for x, (_, t) in enumerate(c.get("sm2", [])): body.append(f'<div class="sm sm2" id="g{g}x{x}">{rich(t)}</div>')
        body.append('</div>')
        if hook:
            js.append(f'tl.fromTo("#g{g}",{{scale:1}},{{scale:1.06,duration:.22,ease:"power2.out",yoyo:true,repeat:1}},0.35);')
        else:
            js.insert(0, f'tl.set("#g{g}",{{opacity:0}},0);'); js.append(f'tl.set("#g{g}",{{opacity:1}},{s});')
            js.append(f'tl.fromTo("#g{g}s",{SM_IN[sm_in]},{s});'); ov(s)
        for b, (bt, _) in enumerate(bigs):
            t = max(s, mapt(rngs, bt))
            if b: js.append(f'tl.to("#g{g}b{b-1}",{{opacity:0,scale:.85,filter:"blur(8px)",duration:.12}},{t});')
            if t > 0.01:
                js.insert(0, f'tl.set("#g{g}b{b}",{{opacity:0}},0);')
                js.append(f'tl.fromTo("#g{g}b{b}",{BIG_IN[big_in]},{t});'); punch(t); ov(t)
        if c.get("hide") is not None and bigs:
            js.append(f'tl.to("#g{g} .bigs",{{opacity:0,scale:.8,filter:"blur(8px)",duration:.14}},{mapt(rngs, c["hide"])});')
        for x, (xt, _) in enumerate(c.get("sm2", [])):
            t = mapt(rngs, xt)
            js.insert(0, f'tl.set("#g{g}x{x}",{{opacity:0}},0);')
            js.append(f'tl.fromTo("#g{g}x{x}",{{opacity:0,y:18}},{{opacity:1,y:0,duration:.3,ease:"back.out(2)"}},{t});'); ov(t)
        if g < len(parts) - 1:
            js.append(f'tl.to("#g{g}",{{opacity:0,y:-14,duration:.18,ease:"power2.in"}},{round(e - .18, 3)});')
        if c.get("list"):
            lay, rows = c["list"]
            body.append(f'<div class="list {lay}" id="l{g}">' + "".join(
                f'<div class="row" id="l{g}r{r}"><i class="bar"></i><span class="n">{html.escape(n)}</span><span class="tx">{rich(t)}</span></div>'
                for r, (_, n, t) in enumerate(rows)) + '</div>')
            js.insert(0, f'tl.set("#l{g} .row",{{opacity:0}},0);')
            for r, (rt, _, _) in enumerate(rows):
                t = round(max(s + .1, mapt(rngs, rt) - .05), 3)
                js.append(f'tl.fromTo("#l{g}r{r}",{ROW_IN[row_in]},{t});')
                js.append(f'tl.fromTo("#l{g}r{r} .bar",{{scaleY:0}},{{scaleY:1,duration:.22,ease:"power2.out"}},{t + .1});')
                js.append(f'tl.fromTo("#l{g}r{r} .hi",{{color:"#ffffff"}},{{color:"{ACC}",duration:.2}},{t + .1});')
                if r:
                    js.append(f'tl.to("#l{g}r{r-1} .bar",{{scaleY:0,duration:.18}},{t + .1});')
                    js.append(f'tl.to("#l{g}r{r-1} .hi",{{color:"#ffffff",duration:.2}},{t + .1});')
                    js.append(f'tl.to("#l{g}r{r-1}",{{opacity:.8,duration:.2}},{t + .1});')
                ov(t)
            if g < len(parts) - 1: js.append(f'tl.to("#l{g}",{{opacity:0,y:-14,duration:.18,ease:"power2.in"}},{round(e - .18, 3)});')
        if c.get("bas"):
            bt = mapt(rngs, 50.18)
            body.append(f'<div class="bas" id="bas{g}"><div class="word" id="basw{g}">BAS</div><div class="lets">' +
                        "".join(f'<div class="let" id="bl{g}{i}"><span class="L">{ch}</span><span class="t">{k}</span></div>' for i, (_, ch, k) in enumerate(BASL)) + '</div></div>')
            js.insert(0, f'tl.set("#bas{g}",{{opacity:0}},0);tl.set("#bas{g} .let",{{opacity:0}},0);')
            js.append(f'tl.set("#bas{g}",{{opacity:1}},{bt});')
            js.append(f'tl.fromTo("#basw{g}",{BIG_IN[big_in].replace(".34", ".2").replace(".36", ".2").replace(".4,", ".2,").replace(".3,", ".2,")},{bt});'); punch(bt); ov(bt)
            js.append(f'tl.set("#basw{g}",{{opacity:0}},{round(mapt(rngs, BASL[0][0]) - .03, 3)});')
            for i, (t, _, _) in enumerate(BASL):
                js.append(f'tl.fromTo("#bl{g}{i}",{{opacity:0,y:30,scale:.6}},{{opacity:1,y:0,scale:1,duration:.3,ease:"back.out(2.2)"}},{mapt(rngs, t)});'); ov(mapt(rngs, t))
            if g < len(parts) - 1: js.append(f'tl.to("#bas{g}",{{opacity:0,y:-14,duration:.18,ease:"power2.in"}},{round(e - .18, 3)});')
        if g: sfx.append([round(s, 3), "tr"])
    a, b = (1.0, 1.03) if kb > 0 else (1.03, 1.0)
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
    make_media(parts, dur, D, os.environ.get("WORK", "/home/user/raw-mtbm") + f"/var/{vid}")
    if not os.path.exists(f"{D}/assets/fonts"): shutil.copytree(f"{PROJ}/assets/fonts", f"{D}/assets/fonts")
    for f in ("package.json", "hyperframes.json"): shutil.copy(f"{PROJ}/{f}", D)
    doc, sfx = html_doc(parts, dur, anim)
    open(f"{D}/index.html", "w").write(doc); json.dump(sfx, open(f"{D}/sfx.json", "w"))
    json.dump({"segments": segs, "dur": dur}, open(f"{D}/plan.json", "w"), indent=1)
    print(vid, "dur", dur)

if __name__ == "__main__":
    for v in (sys.argv[1:] or [v[0] for v in VARS]): build(v)
