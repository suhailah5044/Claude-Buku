#!/usr/bin/env python3
"""Bina 21 video pendek (15-20 s) Matematik SPM Final Boost - Cikgu Yasir, sebagai projek HyperFrames.

Setiap video = 1 INTRO (hook) + 1 TENGAH (isi/USP) + 1 CTA (voiceover pengguna, lihat vo.py),
atau Footage.mov (review penuh) + CTA. Tiada talking head: visual = b-roll buku penuh skrin.
- Setiap kali VO sebut topik/benda dalam buku -> shot buku yang sepadan (2-3 s, fade lembut 0.3 s, ken burns perlahan)
- Hook (kotak gaya #13) kelihatan penuh dari frame 0 (thumbnail)
- Caption pendek, satu pada satu masa, kotak gelap + border kuning, bunyi 'toing' setiap kotak
- Teks di ruang kosong (meja marmar), elak y<150 & y>1550, tiada teks 'bakul/beg kuning'
- Zoom punch kecil pada point penting

Guna:  python3 pipeline/build.py [id ...]       -> videos/<id>/ (index.html, compositions/gfx.html, sfx.json, assets/)
"""
import json, os, shutil, subprocess, sys, re
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import style as S
from shots import SHOT, CUES, ALT
from captions import CAPS, HOOKS
import variety as V
W, H, FPS = 1080, 1920, 30
VO = json.load(open(f"{HERE}/vo.json"))
GAP = 0.10   # senyap antara unit VO
OUT = f"{PROJ}/videos"
fr = lambda t: round(round(t * FPS) / FPS, 4)
RAWDUR = {"IMG_1390": 9.20, "IMG_1391": 5.87, "IMG_1392": 22.29, "IMG_1393": 28.90, "IMG_1394": 6.25, "IMG_1395": 18.34,
          "IMG_1396": 11.57, "IMG_1397": 8.57, "IMG_1398": 7.23, "IMG_1399": 8.40, "IMG_1400": 13.65, "IMG_1401": 17.96,
          "IMG_1402": 13.44, "IMG_1403": 12.29, "IMG_1404": 12.24, "IMG_1405": 3.67, "IMG_1406": 6.67, "IMG_1407": 5.15,
          "IMG_1408": 5.34, "IMG_1409": 11.69, "footage_hold": 13.37}
SLOW = 2.0   # b-roll slow-mo 0.5x (pengguna: footage nampak laju) -> masa klip x2; SHOT.ms ditulis dalam masa ASAL klip
CLIPDUR = {k + ".mp4": v * SLOW for k, v in RAWDUR.items()}

VIDEOS = [  # (id, [unit...])
    ("v01", ["i_4557", "t_96DE", "c_4EE9"]),
    ("v02", ["i_4557", "t_3454", "c_E3ED"]),
    ("v03", ["i_189E", "t_E6E5", "c_4EE9"]),
    ("v04", ["i_189E", "t_3454", "c_C62F"]),
    ("v05", ["i_235A", "t_96DE", "c_3EF9"]),
    ("v06", ["i_235A", "t_3454", "c_F20C"]),
    ("v07", ["i_2C72", "t_E6E5", "c_3EF9"]),
    ("v08", ["i_2C72", "t_96DE", "c_4EE9"]),
    ("v09", ["i_48FA", "t_96DE", "c_3EF9"]),
    ("v10", ["i_48FA", "t_3454", "c_E3ED"]),
    ("v11", ["i_70D5", "t_96DE", "c_4EE9"]),
    ("v12", ["i_70D5", "t_3454", "c_C62F"]),
    ("v13", ["i_A559", "t_3454", "c_F20C"]),
    ("v14", ["i_A559", "t_E6E5", "c_4EE9"]),
    ("v15", ["i_BD48", "t_3454", "c_4EE9"]),
    ("v16", ["i_BD48", "t_E6E5", "c_3EF9"]),
    ("v17", ["i_C83B", "t_96DE", "c_4EE9"]),
    ("v18", ["i_C83B", "t_3454", "c_3EF9"]),
    ("v19", ["i_EC6D", "t_3454", "c_4EE9"]),
    ("v20", ["i_EC6D", "t_E6E5", "c_4EE9"]),
    ("v21", ["f_full", "c_E3ED"]),
]

def layout(units):
    off, t = {}, 0.0
    for u in units:
        off[u] = fr(t); t = off[u] + VO[u]["dur"] + GAP
    return off, fr(t - GAP + 0.35)   # 0.35 s hujung (CTA kekal sekejap)

def make_vo(units, off, dur, path):
    """VO bercantum (unit + senyap), 48 kHz mono. Loudness akhir dibuat dalam mux.py."""
    import numpy as np, wave
    out = np.zeros(int(dur * 48000) + 4800, np.float32)
    for u in units:
        w = wave.open(f"{PROJ}/assets/vo/{u}.wav"); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        i = int(off[u] * 48000); out[i:i + len(a)] += a[:len(out) - i]
    out = out[:int(dur * 48000)]
    w = wave.open(path, "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(48000)
    w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()

def occ_of(vid):
    """Kali ke-berapa setiap unit muncul (ikut susunan VIDEOS) -> pilih versi caption/b-roll/hook (peraturan #14)."""
    cnt, res = {}, None
    for v, us in VIDEOS:
        o = {u: cnt.get(u, 0) for u in us}
        for u in us: cnt[u] = cnt.get(u, 0) + 1
        if v == vid: res = o
    return res or {}

def unit_cues(u, o):
    alts = V.CUES_ALT.get(u, [])
    return CUES[u] if o == 0 or not alts else alts[(o - 1) % len(alts)]

def unit_caps(u, o):
    caps = [dict(c) for c in CAPS[u]]
    alts = V.TEXT_ALT.get(u, [])
    if o and alts:
        for c, t in zip(caps, alts[(o - 1) % len(alts)]):
            if t is None: continue
            if c["k"] == "card": c["title"] = t
            else: c["text"] = t
    return caps

def plan(vid, units):
    off, dur = layout(units)
    OCC = occ_of(vid)
    # ---- shot (b-roll penuh skrin) ikut cue setiap unit
    cues = []
    for u in units:
        for t, key in unit_cues(u, OCC.get(u, 0)):
            cues.append((fr(off[u] + t), key))
    cues.sort()
    cues[0] = (0.0, cues[0][1])
    shots, used = [], {}
    for n, (t, key) in enumerate(cues):
        e = cues[n + 1][0] if n + 1 < len(cues) else dur
        if e - t < 0.4: continue
        same = lambda k: shots and SHOT[shots[-1]["key"]]["f"] == SHOT[k]["f"]
        if same(key) or key in used:   # elak shot sama bersebelahan / berulang
            alt, tried = key, 0
            while tried < 4:
                alt = ALT.get(alt); tried += 1
                if not alt: break
                if alt not in used and not same(alt): key = alt; break
        sh = dict(key=key, s=t, e=round(e, 3), **SHOT[key])
        sh["ms"] = round((sh["ms"] + 1.0 * used.get(key, 0)) * SLOW, 3)   # guna semula -> mula sikit lewat; x SLOW (slow-mo)
        cd = CLIPDUR.get(sh["f"])
        if cd: sh["ms"] = round(max(0.0, min(sh["ms"], cd - (sh["e"] - sh["s"]) - 0.45)), 3)
        used[key] = used.get(key, 0) + 1
        shots.append(sh)
    # ---- caption
    els = []
    hu = units[0]
    hk = dict(V.HOOK_ALT[hu] if OCC.get(hu, 0) and hu in V.HOOK_ALT else HOOKS[hu]); els.append(dict(k="hook", s=0.0, e=hk.pop("e"), nohide=True, **hk))
    for u in units:
        for c in unit_caps(u, OCC.get(u, 0)):
            c = dict(c); c["s"] = round(off[u] + c["s"], 3)
            if "e" in c: c["e"] = round(off[u] + c["e"], 3)
            if "items" in c: c["items"] = [(tx, round(off[u] + x, 3)) for tx, x in c["items"]]
            els.append(c)
    els.sort(key=lambda c: c["s"])
    for n, c in enumerate(els):   # satu benda pada satu masa: tamat bila yang seterusnya mula
        if "e" not in c or (n + 1 < len(els) and c["e"] > els[n + 1]["s"] - 0.02):
            c["e"] = round(els[n + 1]["s"] - 0.02, 3) if n + 1 < len(els) else dur
    els[-1]["e"] = dur; els[-1]["final"] = True
    for c in els:   # y caption = ruang kosong pada shot semasa caption mula
        if "y" not in c:
            sh = next((s for s in shots if s["s"] <= c["s"] + 0.08 < s["e"]), shots[-1])
            c["y"] = sh.get("cy", 200)
            if c["y"] > 1000 and c["k"] == "card": c["y"] = 1425 if not c.get("items") else 1360
    # caption yang merentas shot dengan ruang kosong lain (atas <-> bawah): pecah, bahagian 2 pindah ke ruang kosong shot baru (tanpa bunyi)
    out = []
    for c in els:
        out.append(c)
        if c["k"] != "cap" or c.get("final") and False: continue
        for sh in shots:
            if c["s"] + 0.3 < sh["s"] < c["e"] - 0.5 and abs(sh.get("cy", 200) - c["y"]) > 300:
                c2 = dict(c); c2["s"] = round(sh["s"] + 0.05, 3); c2["y"] = sh.get("cy", 200); c2["sfx"] = "none"; c2.pop("punch", None)
                c["e"] = round(sh["s"] + 0.02, 3); c.pop("final", None)
                out.append(c2); c = c2
    els = out
    punch = [round(off[u] + c["s"] + 0.05, 3) for u in units for c in CAPS[u] if c.get("punch")]
    return off, dur, shots, els, punch

def CAPS_PUNCH(u):
    return [c["s"] + 0.05 for c in CAPS[u] if c.get("punch")]

def root_html(dur, shots, punch, vo_src="assets/vo.wav"):
    body, js = [], []
    for n, sh in enumerate(shots):
        src = f"assets/broll/{sh['f']}"
        d = round(sh["e"] - sh["s"] + (0.3 if n + 1 < len(shots) else 0), 3)   # bertindih 0.3 s untuk fade lembut
        d = min(d, round(dur - sh["s"], 3))
        if src.endswith(".jpg"):
            el = f'<img id="b{n}" src="{src}" alt="">'
        else:
            el = (f'<video id="b{n}" src="{src}" data-start="{sh["s"]}" data-duration="{d}" data-media-start="{sh["ms"]}" '
                  f'data-track-index="{2 + n}" class="clip" muted playsinline></video>')
        body.append(f'<div class="bw" id="b{n}w" style="z-index:{2 + n};transform-origin:{sh.get("o", "50% 50%")}">{el}</div>')
        k0, k1 = sh.get("kb", (1.0, 1.06))
        if n == 0:
            js.append(f'tl.set("#b{n}w",{{opacity:1}},0);')
        else:
            js.append(f'tl.fromTo("#b{n}w",{{opacity:0}},{{opacity:1,duration:.3,ease:"sine.inOut"}},{sh["s"]});')
        js.append(f'tl.fromTo("#b{n}w",{{scale:{k0}}},{{scale:{k1},duration:{d},ease:"none"}},{sh["s"]});')
    for i, p in enumerate(sorted(punch)):
        ir = "" if i == 0 else ",immediateRender:false"
        js.append(f'tl.fromTo("#cam",{{scale:1}},{{scale:1.045,duration:.16,ease:"expo.out",yoyo:true,repeat:1{ir}}},{p});')
    js.append(f'tl.fromTo("#glow",{{x:-240}},{{x:240,duration:{round(dur/2,3)},ease:"sine.inOut",yoyo:true,repeat:1}},0);')
    return f"""<!doctype html>
<html lang="ms">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#0d0c0b; }}
#root {{ position:relative; width:{W}px; height:{H}px; overflow:hidden; font-family:'Montserrat',sans-serif; }}
#cam {{ position:absolute; inset:0; transform-origin:50% 55%; }}
.bw {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; opacity:0; overflow:hidden; }}
.bw video, .bw img {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; object-fit:cover; }}
#scrim {{ position:absolute; left:0; top:0; width:{W}px; height:620px; z-index:60; pointer-events:none;
  background:linear-gradient(180deg,rgba(13,12,11,.30) 0%,rgba(13,12,11,.12) 300px,rgba(13,12,11,0) 600px); }}
#glow {{ position:absolute; left:240px; top:-260px; width:600px; height:600px; border-radius:50%; z-index:61; pointer-events:none;
  background:radial-gradient(circle, rgba(255,194,26,.14) 0%, rgba(255,194,26,0) 70%); }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{dur}" data-width="{W}" data-height="{H}">
<div id="cam">
{chr(10).join(body)}
</div>
<audio id="vo" src="{vo_src}" data-start="0" data-duration="{dur}" data-track-index="1" data-has-audio="true"></audio>
<div id="scrim"></div>
<div id="glow"></div>
<div id="gfx" data-composition-id="gfx" data-composition-src="compositions/gfx.html" data-start="0" data-duration="{dur}"
  data-track-index="30" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:80"></div>
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

def build(vid, units):
    off, dur, shots, els, punch = plan(vid, units)
    P = f"{OUT}/{vid}"
    os.makedirs(f"{P}/assets/broll", exist_ok=True); os.makedirs(f"{P}/compositions", exist_ok=True)
    for f in {s["f"] for s in shots}:
        dst = f"{P}/assets/broll/{f}"
        if os.path.exists(dst): os.unlink(dst)
        if os.path.exists(f"{PROJ}/assets/broll/{f}"): os.link(f"{PROJ}/assets/broll/{f}", dst)
        else: print("  (belum ada)", f)
    for f in ("hyperframes.json", "package.json"):
        shutil.copy(f"{PROJ}/{f}", P)
    json.dump({"name": f"spm-final-boost-{vid}"}, open(f"{P}/meta.json", "w"))
    make_vo(units, off, dur, f"{P}/assets/vo.wav")
    S.SOUND_ALL = "toing"
    S.ANIM = V.ANIMS[(int(vid[1:]) - 1) % len(V.ANIMS)]   # animasi masuk lain setiap video (v01 = pop)
    doc, sfx = S.build_gfx(els, dur=dur, y0=200)
    doc = doc.replace("<script>\nconst tl", "<script>\nwindow.__timelines = window.__timelines || {};\nconst tl")
    open(f"{P}/compositions/gfx.html", "w").write(doc)
    open(f"{P}/index.html", "w").write(root_html(dur, shots, punch))
    json.dump(sfx, open(f"{P}/sfx.json", "w"))
    json.dump(dict(units=units, offsets=off, dur=dur, shots=shots, els=els), open(f"{P}/plan.json", "w"), ensure_ascii=False, indent=1)
    print(vid, f"{dur:.1f}s", units, "| shots", len(shots), "| caps", len(els), "| sfx", len(sfx), flush=True)

if __name__ == "__main__":
    only = sys.argv[1:]
    for vid, units in VIDEOS:
        if only and vid not in only: continue
        build(vid, units)
