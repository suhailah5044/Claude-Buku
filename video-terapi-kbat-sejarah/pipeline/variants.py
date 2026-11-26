#!/usr/bin/env python3
"""9 varian hook Terapi KBAT Sejarah (Gaya Algebra, saiz kecil). Setiap varian berbeza KESELURUHAN:
hook (ayat pembuka) lain, susunan & pilihan ayat lain (panjang lain), set ayat caption lain (3 versi),
animasi masuk lain (pop/slide/drop/zoom/flip), SFX tukar-tukar. Semua suara asal pengguna.
Elemen ditakrif dalam masa SUMBER (footage asal, tx_raw.json); A-roll setiap varian dipotong terus dari sumber.
Guna: python3 pipeline/variants.py <src.mov> [id ...]   -> variants/<id>/ (projek HyperFrames)"""
import html, json, os, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__)); MAIN = os.path.dirname(HERE)
OUT = os.path.join(MAIN, "variants")
SRC = sys.argv[1] if len(sys.argv) > 1 else None
_b = open(os.path.join(HERE, "build.py")).read()
G = {"__file__": os.path.join(HERE, "build.py")}
exec(_b[:_b.index("# kinds:")] + _b[_b.index("SCENE_CSS ="):_b.index("def write_scene")], G)
W, H, ACC, FONT, SCENE_CSS, esc, svg, burst_html, hl_html = (G[k] for k in
    ("W", "H", "ACC", "FONT", "SCENE_CSS", "esc", "svg", "burst_html", "hl_html"))
SPEED = 1.1

# ---------------------------------------------------------------- unit (ayat) dalam masa sumber
UNITS = {"ramai": (0.00, 1.80), "hookA": (2.47, 5.29), "sebab": (5.32, 8.65), "fokus": (8.66, 11.88),
         "langkah": (11.89, 15.55), "format": (15.57, 18.04), "video": (18.06, 20.16), "skema": (20.17, 22.80),
         "supaya": (22.84, 27.54), "menarik": (27.55, 30.56), "jenis": (30.57, 35.58), "pes": (35.60, 36.92),
         "rangka": (36.93, 40.35), "vid2": (40.36, 44.82), "cta": (44.83, 48.62)}
PAUSES = [(7.32, 7.49), (8.60, 8.74), (13.46, 13.78), (15.26, 15.63), (17.91, 18.13), (35.52, 35.81),
          (40.15, 40.42), (44.55, 44.88)]
SRC_SHOTS = [5.333, 8.567, 11.933, 17.933, 20.183, 27.6, 30.7, 37.067, 44.967]

def pieces(u):
    a, b = UNITS[u]; out = [[a, b]]
    for p, q in PAUSES:
        lo, hi = p + 0.04, q - 0.04
        nxt = []
        for x, y in out:
            if hi <= x or lo >= y: nxt.append([x, y]); continue
            if lo > x: nxt.append([x, lo])
            if hi < y: nxt.append([hi, y])
        out = nxt
    return [(round(x, 3), round(y, 3)) for x, y in out if y - x > 0.03]

# ---------------------------------------------------------------- elemen setiap unit (masa sumber)
# txt: (set0, set1, set2) — setiap set = (lines, hi). None = tiada dalam set tu.
def HL(s, e, txt, wt, **kw): return dict(k="hl", s=s, e=e, txt=txt, wt=wt, **kw)
ELS = {
 "ramai": [HL(0.0, 1.78, ((["RAMAI STUDENT", "HADAP MASALAH SAMA"], "SAMA"), (["MASALAH", "RAMAI STUDENT"], "STUDENT"),
                         (["KORANG PUN", "SAMA?"], "SAMA?")), [0.30, 0.52, 0.88, 1.12, 1.60])],
 "hookA": [HL(2.5, 5.27, ((["JAWAB PANJANG,", "MARKAH SIKIT?"], "SIKIT?"), (["DAH JAWAB PANJANG..."], "PANJANG..."),
                         (["MARKAH", "SIKIT JE?"], "SIKIT")), [2.84, 3.0, 4.08, 4.82], punch=4.08),
           dict(k="sub", s=4.0, e=5.27, txt=(None, "tapi markah <b>dapat sikit je</b>", None), y=420)],
 "sebab": [HL(5.32, 5.9, ((["SEBAB APA?"], "APA?"),) * 3, [5.40, 5.76], punch=5.40),
           HL(5.94, 8.63, ((["TAK TAHU TEKNIK", "IKUT KEHENDAK SOALAN"], "SOALAN"), (["TAK IKUT", "KEHENDAK SOALAN"], "KEHENDAK"),
                          (["KUNCI: IKUT", "KEHENDAK SOALAN"], "KUNCI:")), [6.38, 6.54, 7.04, 7.38, 7.68, 8.16])],
 "fokus": [dict(k="kick", s=8.7, e=11.86, txt=("TEKNIK MENJAWAB", "FOKUS UTAMA", "USP BUKU NI")),
           HL(9.0, 11.86, ((["TEKNIK JAWAB KBAT"], "KBAT"), (["JAWAB KBAT", "LEBIH TERATUR"], "TERATUR"),
                          (["FOKUS TEKNIK", "MENJAWAB"], "MENJAWAB")), [9.24, 9.56, 10.28, 10.9, 11.22]),
           dict(k="chip", s=10.85, e=11.86, txt=("Jawab lebih teratur", None, "Lebih teratur"), icon="steps", y=420)],
 "langkah": [dict(k="kick", s=11.92, e=15.5, txt=("LANGKAH DEMI LANGKAH", "PANDUAN MENJAWAB", "MUDAH IKUT")),
             HL(12.22, 15.5, ((["IKUT LANGKAH,", "ISI SETIAP KOTAK"], "KOTAK"), (["IKUT LANGKAH", "JE!"], "JE!"),
                             (["ISI SETIAP", "KOTAK JE!"], "KOTAK")), [12.22, 12.54, 14.26, 14.6, 14.9])],
 "format": [HL(16.2, 18.0, ((["SOALAN", "FORMAT SPM"], "SPM"), (["IKUT FORMAT SPM"], "SPM"), None), [16.34, 16.8, 17.26], punch=17.26),
            dict(k="chip", s=16.3, e=18.0, txt=(None, None, "Soalan berformat SPM"), icon="check", y=300)],
 "video": [HL(18.1, 20.14, ((["VIDEO PENERANGAN", "PUN ADA!"], "ADA!"), (["ADA VIDEO", "PENERANGAN!"], "VIDEO"),
                           (["SIAP DENGAN", "VIDEO!"], "VIDEO!")), [18.1, 18.38, 19.04, 19.26], y=600),
           dict(k="sub", s=18.8, e=20.14, txt=("Belajar <b>step by step</b>", "Bagi <b>setiap jenis KBAT</b>", "Belajar <b>step by step</b>"), y=750)],
 "skema": [HL(21.7, 22.78, ((["SKEMA JAWAPAN", "LENGKAP"], "LENGKAP"), (["SIAP SKEMA", "JAWAPAN!"], "JAWAPAN!"), None),
              [21.92, 22.24, 22.7], punch=21.92),
           dict(k="chip", s=21.8, e=22.78, txt=(None, None, "Skema jawapan lengkap"), icon="check", y=300)],
 "supaya": [dict(k="chip", s=23.2, e=25.75, txt=("Siap dengan contoh jawapan", "Tengok cara sebenar jawab", None), icon="book", y=300),
            HL(23.9, 25.75, (None, None, (["TENGOK CARA", "SEBENAR JAWAB"], "SEBENAR")), [23.96, 24.2, 24.48, 25.1]),
            HL(25.8, 27.5, ((["IKUT KEHENDAK", "PEMERIKSA"], "PEMERIKSA"), (["MACAM PEMERIKSA", "NAK!"], "NAK!"),
                           (["CARA", "PEMERIKSA NAK"], "PEMERIKSA")), [25.84, 26.34, 26.58, 27.12], punch=26.58)],
 "menarik": [dict(k="kick", s=27.6, e=30.54, txt=("TERAPI KBAT SEJARAH SPM", "BUKU TERAPI KBAT", "SEJARAH SPM")),
             HL(29.6, 30.54, ((["SANGAT-SANGAT", "MENARIK!"], "MENARIK!"), (["BUKU NI", "SANGAT MENARIK"], "MENARIK"),
                             (["TERAPI KBAT", "SEJARAH SPM"], "SPM")), [29.7, 29.98, 30.3])],
 "jenis": [dict(k="kick", s=30.6, e=35.56, txt=("8 JENIS KBAT", "SEMUA JENIS ADA", "KBAT LENGKAP"))] +
          [dict(k="tick", s=s, e=e, txt=(t,) * 3) for t, s, e in
           [("KBAT FAKTA", 32.02, 32.68), ("LANGSUNG", 32.7, 32.92), ("PETIKAN PENDEK", 32.94, 33.54), ("PETIKAN PANJANG", 33.56, 34.02),
            ("POSTER", 34.04, 34.58), ("LIRIK LAGU", 34.6, 34.9), ("PUISI", 34.92, 35.42), ("GRAF", 35.44, 35.56)]],
 "pes": [HL(35.8, 36.9, ((["+ RUMUS P.E.S."], "P.E.S."), (["SIAP RUMUS P.E.S."], "P.E.S."), (["RUMUS P.E.S.!"], "P.E.S.!")),
            [35.92, 36.22, 36.4], punch=36.22)],
 "rangka": [HL(37.0, 40.33, ((["RANGKA", "STRUKTUR KOTAK"], "KOTAK"), (["STRUKTUR KOTAK"], "KOTAK"), (["RANGKA", "STRUKTUR KOTAK"], "STRUKTUR")),
               [37.12, 37.48, 37.76]),
            dict(k="chip", s=38.5, e=40.33, txt=("Bantu susun idea & jawapan", None, "Susun idea & jawapan"), icon="grid", y=440),
            dict(k="sub", s=38.6, e=40.33, txt=(None, "Bantu anak <b>susun idea & jawapan</b>", None), y=400)],
 "vid2": [dict(k="kick", s=40.4, e=44.8, txt=("SIAP DENGAN VIDEO", "VIDEO PENERANGAN", "BELAJAR SENDIRI")),
          HL(41.4, 44.8, ((["AJAR", "STEP BY STEP"], "STEP"), (["STEP BY STEP"], "STEP"), (["VIDEO", "STEP BY STEP"], "VIDEO")),
             [41.4, 42.14, 42.3, 42.52]),
          dict(k="chip", s=43.0, e=44.8, txt=("Penerangan + skema jawapan",) * 3, icon="book", y=440)],
 "cta": [dict(k="kick", s=44.9, e=99, txt=("PERSEDIAAN SPM", "SEJARAH SPM", "KBAT SEJARAH"), final=True),
         HL(44.9, 46.95, ((["BOOST KBAT", "SEJARAH! @FIRE"], "SEJARAH!"), (["MEMANG", "RECOMMEND!"], "RECOMMEND!"),
                         (["IBU AYAH,", "JUST CONSIDER!"], "CONSIDER!")), [45.0, 45.66, 46.66], punch=45.0),
         HL(47.0, 99, ((["JOM BUAT", "PERSEDIAAN AWAL!"], "AWAL!"), (["BOOST KBAT", "SEJARAH! @FIRE"], "SEJARAH!"),
                      (["JOM BUAT", "PERSEDIAAN AWAL!"], "AWAL!")), [47.0, 47.3, 47.6], final=True)],
}

# ---------------------------------------------------------------- 9 varian
V = [
 dict(id="v02_sebab_apa", hook="sebab", H=3.0, kick="KENAPA MARKAH SIKIT?", lines=["SEBAB APA", "MARKAH SIKIT?"], hi="SIKIT?",
      order=["sebab", "hookA", "fokus", "langkah", "skema", "supaya", "jenis", "pes", "rangka", "video", "cta"], set=1, anim="slide"),
 dict(id="v03_skema", hook="skema", H=2.6, kick="KBAT SEJARAH SPM", lines=["ADA SKEMA", "JAWAPAN LENGKAP!"], hi="LENGKAP!",
      order=["skema", "supaya", "hookA", "sebab", "fokus", "rangka", "pes", "jenis", "video", "menarik", "cta"], set=2, anim="drop"),
 dict(id="v04_menarik", hook="menarik", H=2.9, kick="BUKU KBAT SEJARAH", lines=["SANGAT-SANGAT", "MENARIK!"], hi="MENARIK!",
      order=["menarik", "jenis", "pes", "rangka", "hookA", "ramai", "sebab", "langkah", "skema", "supaya", "vid2", "cta"], set=0, anim="zoom"),
 dict(id="v05_8_jenis", hook="jenis", H=2.4, kick="TERAPI KBAT SEJARAH", lines=["8 JENIS KBAT", "DALAM 1 BUKU!"], hi="BUKU!",
      order=["jenis", "pes", "hookA", "sebab", "fokus", "langkah", "format", "video", "skema", "supaya", "cta"], set=1, anim="flip"),
 dict(id="v06_rumus_pes", hook="pes", H=1.3, kick="TEKNIK KBAT SPM", lines=["RUMUS P.E.S.", "UNTUK KBAT!"], hi="P.E.S.",
      order=["pes", "rangka", "langkah", "ramai", "hookA", "sebab", "skema", "supaya", "vid2", "menarik", "cta"], set=2, anim="pop"),
 dict(id="v07_video", hook="video", H=2.1, kick="KBAT SEJARAH SPM", lines=["BUKU LATIHAN", "ADA VIDEO?!"], hi="VIDEO?!",
      order=["video", "skema", "supaya", "hookA", "ramai", "sebab", "langkah", "rangka", "pes", "jenis", "menarik", "cta"], set=0, anim="slide"),
 dict(id="v08_ikut_langkah", hook="langkah", H=3.4, kick="JAWAB KBAT SEJARAH", lines=["IKUT LANGKAH,", "ISI KOTAK JE!"], hi="KOTAK",
      order=["langkah", "rangka", "pes", "hookA", "sebab", "fokus", "format", "jenis", "video", "skema", "cta"], set=1, anim="drop"),
 dict(id="v09_masalah_sama", hook="ramai", H=1.8, kick="PELAJAR SPM", lines=["MASALAH RAMAI", "STUDENT SPM"], hi="SPM",
      order=["ramai", "hookA", "sebab", "supaya", "skema", "fokus", "langkah", "rangka", "menarik", "jenis", "vid2", "cta"], set=2, anim="zoom"),
 dict(id="v10_pemeriksa", hook="supaya", H=2.9, kick="RAHSIA MARKAH PENUH", lines=["JAWAB IKUT CARA", "PEMERIKSA NAK!"], hi="PEMERIKSA",
      order=["supaya", "fokus", "langkah", "rangka", "pes", "hookA", "ramai", "sebab", "skema", "video", "cta"], set=0, anim="flip"),
]

# ---------------------------------------------------------------- animasi masuk (5 gaya)
ENTER = {
 "pop":   ('{opacity:0,y:34,scale:.55,filter:"blur(8px)"}', '{opacity:1,y:0,scale:1,filter:"blur(0px)",duration:.3,ease:"back.out(2.2)"}'),
 "slide": ('{opacity:0,x:-80,filter:"blur(8px)"}', '{opacity:1,x:0,filter:"blur(0px)",duration:.32,ease:"expo.out"}'),
 "drop":  ('{opacity:0,y:-70,rotation:-8}', '{opacity:1,y:0,rotation:0,duration:.42,ease:"back.out(3)"}'),
 "zoom":  ('{opacity:0,scale:2.3,filter:"blur(12px)"}', '{opacity:1,scale:1,filter:"blur(0px)",duration:.3,ease:"expo.out"}'),
 "flip":  ('{opacity:0,rotationX:-95,transformPerspective:600,transformOrigin:"50% 100%"}', '{opacity:1,rotationX:0,duration:.38,ease:"back.out(1.8)"}'),
}

def write_scene(path, sid, s0, els, anim):
    a0, a1 = ENTER[anim]
    body, js = [], []
    ins = lambda t: round(max(0, t - s0), 3)
    for n, el in enumerate(els):
        i = f"{sid}-{el['k']}{n}"; k = el["k"]
        st, en = ins(el["s"]), ins(el["e"]); d = round(en - st, 3)
        fin = el.get("final")
        if k == "kick":
            body.append(f'<div id="{i}" class="clip slot kick" data-start="{st}" data-duration="{d}" data-track-index="1" style="top:196px">'
                        f'<div class="in" id="{i}-in">{esc(el["text"])}</div></div>')
            if el.get("static"):
                js.append(f'tl.fromTo("#{i}-in",{{scale:1.12}},{{scale:1,duration:.4,ease:"expo.out"}},{st});')
            else:
                js.append(f'tl.fromTo("#{i}-in",{{opacity:0,clipPath:"inset(0 50% 0 50% round 999px)"}},{{opacity:1,clipPath:"inset(0 0% 0 0% round 999px)",duration:.4,ease:"expo.out"}},{st});')
            if not fin: js.append(f'tl.to("#{i}-in",{{opacity:0,duration:.18,ease:"power2.in"}},{round(en-.2,3)});')
        elif k == "sub":
            body.append(f'<div id="{i}" class="clip slot sub" data-start="{st}" data-duration="{d}" data-track-index="4" style="top:{el["y"]}px">'
                        f'<div class="in" id="{i}-in">{el["text"]}</div></div>')
            js.append(f'tl.fromTo("#{i}-in",{a0},{a1},{st});')
            js.append(f'tl.to("#{i}-in",{{opacity:0,duration:.18,ease:"power2.in"}},{round(en-.2,3)});')
        elif k == "tick":
            body.append(f'<div id="{i}" class="clip slot tick" data-start="{st}" data-duration="{d}" data-track-index="2" style="top:272px">'
                        f'<div class="in" id="{i}-in">{esc(el["text"])}</div></div>')
            js.append(f'tl.fromTo("#{i}-in",{a0},{a1.replace("duration:.3", "duration:.16").replace("duration:.32", "duration:.16").replace("duration:.38", "duration:.18").replace("duration:.42", "duration:.2")},{st});')
        elif k == "hl":
            inner, top, nw = hl_html(i, el)
            body.append(f'<div id="{i}" class="clip slot hl" data-start="{st}" data-duration="{d}" data-track-index="2" style="top:{top}px">{inner}</div>')
            wt = el.get("wt") or [el["s"]]
            if el.get("static"):
                js.append(f'tl.fromTo("#{i}-in",{{scale:1.1}},{{scale:1,duration:.45,ease:"expo.out"}},{st});')
                js.append(f'tl.set("#{i}-bar",{{scaleX:1}},0);')
            else:
                wt = (wt + [wt[-1] + 0.07 * (j + 1) for j in range(nw)])[:nw]
                for j in range(nw):
                    t = round(max(st, min(ins(max(wt[j], el["s"])), en - 0.4)), 3)
                    js.append(f'tl.fromTo("#{i}-w{j}",{a0},{a1},{t});')
                if el.get("hi"):
                    js.append(f'tl.fromTo("#{i}-bar",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:.34,ease:"expo.out"}},{round(min(ins(max(wt)) + .1, en - .3), 3)});')
                if el.get("punch") is not None:
                    js.append(f'tl.fromTo("#{i}-in",{{scale:1.3}},{{scale:1,duration:.36,ease:"expo.out"}},{st});')
            if not fin:
                for j in range(nw):
                    js.append(f'tl.to("#{i}-w{j}",{{opacity:0,y:-18,filter:"blur(6px)",duration:.15,ease:"power2.in"}},{round(en-.18,3)});')
        elif k == "chip":
            body.append(f'<div id="{i}" class="clip slot chip" data-start="{st}" data-duration="{d}" data-track-index="3" style="top:{el["y"]}px">'
                        f'<div class="in" id="{i}-in">{burst_html(i)}<span class="ico" id="{i}-ico">{svg(el["icon"])}</span>'
                        f'<span class="ct" id="{i}-ct">{esc(el["text"])}</span></div></div>')
            js += [f'tl.fromTo("#{i}-in",{a0},{a1},{st});',
                   f'tl.fromTo("#{i}-ico",{{rotation:-120,scale:.3}},{{rotation:0,scale:1,duration:.48,ease:"back.out(2)"}},{round(st+.05,3)});',
                   f'tl.fromTo("#{i}-ct",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:.38,ease:"power3.out"}},{round(st+.1,3)});',
                   f'tl.fromTo("#{i}-burst i",{{scaleX:0,x:22,opacity:1}},{{scaleX:1,x:44,opacity:0,duration:.45,ease:"expo.out"}},{round(st+.08,3)});',
                   f'tl.to("#{i}-in",{{opacity:0,scale:.85,duration:.18,ease:"power2.in"}},{round(en-.2,3)});']
    doc = f"""<template>
<style>{FONT.replace('{P}', '../')}{SCENE_CSS}</style>
<div id="root" data-composition-id="{sid}" data-width="{W}" data-height="{H}" data-layout-allow-overlap>
{chr(10).join(body)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines["{sid}"] = tl;
</script>
</template>
"""
    open(f"{path}/compositions/{sid}.html", "w").write(doc)

GLYPHS = [("A+", 60, 60, 66), ("?", 905, 50, 70), ("SPM", 200, 150, 40), ("✓", 800, 165, 56), ("KBAT", 450, 34, 38),
          ("!", 990, 250, 64), ("P.E.S.", 18, 300, 34), ("1957", 640, 110, 40), ("?", 340, 250, 46), ("A+", 720, 290, 42)]

def build(v):
    path = os.path.join(OUT, v["id"]); os.makedirs(f"{path}/compositions", exist_ok=True)
    keep, starts, PU, t = [], {}, {}, 0.0          # keep: (src_a, src_b, out_start)
    for u in v["order"]:
        starts[u] = round(t, 4); PU[u] = []
        for a, b in pieces(u):
            keep.append((a, b, round(t, 4))); PU[u].append((a, b, t)); t += (b - a) / SPEED
    DUR = round(t, 3)
    def T(x, u):
        last = PU[u][0][2]
        for a, b, o in PU[u]:
            if x < a: return round(last if x < PU[u][0][0] else o, 3)
            if x <= b: return round(o + (x - a) / SPEED, 3)
            last = o + (b - a) / SPEED
        return round(last, 3)
    uend = lambda u: round(starts[u] + sum(b - a for a, b in pieces(u)) / SPEED, 3)
    # ---- elemen
    scenes, punch, sfx = [], [], []
    S = v["set"]
    for n, u in enumerate(v["order"]):
        u0, u1 = starts[u], uend(u)
        if u == "cta": u1 = DUR
        els = []
        if u == v["hook"]:
            hk = min(v["H"], u1 - u0)
            els += [dict(k="kick", s=u0, e=u0 + hk - .02, text=v["kick"], static=True),
                    dict(k="hl", s=u0, e=u0 + hk - .02, lines=v["lines"], hi=v["hi"], static=True)]
            sfx.append((0.0, "ov"))
        for el in ELS[u]:
            txt = el["txt"][S] if len(el["txt"]) > S else el["txt"][0]
            if txt is None: continue
            s = T(el["s"], u); e = DUR - 0.02 if el["e"] >= 99 else T(el["e"], u)
            if u == v["hook"]:
                if e <= u0 + v["H"] + 0.3: continue
                s = max(s, u0 + v["H"])
            if e - s < 0.25: continue
            p = {kk: vv for kk, vv in el.items() if kk not in ("txt",)}
            p["s"], p["e"] = round(s, 3), round(e, 3)
            if el["k"] == "hl": p["lines"], p["hi"] = txt
            else: p["text"] = txt
            if p.get("wt"): p["wt"] = [T(x, u) for x in p["wt"]]
            if el.get("punch") is not None:
                pt = T(el["punch"], u)
                if pt >= p["s"]: punch.append(pt)
            if el["k"] in ("hl", "chip") and not (u == v["hook"] and False):
                sfx.append((p["s"], "tr" if len(sfx) % 2 else "ov"))
            els.append(p)
        scenes.append((f"s{n+1}", round(u0, 3), round(u1 if n < len(v["order"]) - 1 else DUR, 3), els))
    # tick: bunyi pada 2 sahaja
    for u in v["order"]:
        if u == "jenis" and u != v["hook"]:
            sfx += [(T(32.02, u), "ov"), (T(33.56, u), "ov")]
    sfx.sort(); dedup = []
    for t_, k_ in sfx:
        if not dedup or t_ - dedup[-1][0] > 0.6: dedup.append((round(t_, 3), k_))
    json.dump(dedup, open(f"{path}/sfx.json", "w")); json.dump(keep, open(f"{path}/keep.json", "w"))
    for sid, s0, s1, els in scenes:
        write_scene(path, sid, s0, els, v["anim"])
    # ---- segment kamera (setiap potongan / shot sumber)
    cuts = sorted({round(o, 3) for _, _, o in keep} |
                  {T(c, u) for u in v["order"] for c in SRC_SHOTS if UNITS[u][0] < c < UNITS[u][1]} | {DUR})
    segs = [(a, b) for a, b in zip(cuts, cuts[1:]) if b - a > 0.05]
    js = ['tl.set("#cam",{y:140,scale:1,transformOrigin:"50% 32%"},0);']
    for n, (a, b) in enumerate(segs):
        base = 1.0 if n % 2 == 0 else 1.045
        cur = lambda x: round(base + 0.03 * (x - a) / (b - a), 3)
        ps = [p for p in sorted(punch) if a <= p < b - .55]
        t0 = a
        for p in ps:   # push-in perlahan -> punch -> sambung push-in (tiada tween bertindih)
            if p > t0: js.append(f'tl.fromTo("#cam",{{scale:{cur(t0)}}},{{scale:{cur(p)},duration:{round(p-t0,3)},ease:"none"}},{round(t0,3)});')
            js += [f'tl.fromTo("#cam",{{scale:{cur(p)}}},{{scale:{round(cur(p)+.07,3)},duration:.14,ease:"expo.out"}},{p});',
                   f'tl.fromTo("#cam",{{scale:{round(cur(p)+.07,3)}}},{{scale:{cur(p+.5)},duration:.36,ease:"power2.out"}},{round(p+.14,3)});']
            t0 = round(p + .5, 3)
        js.append(f'tl.fromTo("#cam",{{scale:{cur(t0)}}},{{scale:{round(base+0.03,3)},duration:{round(b-t0,3)},ease:"none"}},{round(t0,3)});')
    seed = int(v["id"][1:3])
    gl = []
    for n, (g, x, y, s) in enumerate(GLYPHS):
        x2 = (x + seed * 97 * (n + 1)) % 1000; gl.append(f'<span class="gl" data-layout-ignore id="gl{n}" style="left:{x2}px;top:{y}px;font-size:{s}px">{html.escape(g)}</span>')
        js.append(f'tl.fromTo("#gl{n}",{{x:0,y:0,rotation:0}},{{x:{(-1)**(n+seed)*(40+9*n)},y:{(-1)**(n//2)*(14+3*n)},rotation:{(-1)**(n+1)*(20+6*n)},duration:{DUR},ease:"none"}},0);')
    js.append(f'tl.fromTo("#glow",{{x:-260}},{{x:260,duration:{DUR/2},ease:"sine.inOut",yoyo:true,repeat:1}},0);')
    for n, p in enumerate(sorted(punch)):
        js.append(f'tl.fromTo(".gl",{{opacity:.34}},{{opacity:.12,duration:.6,ease:"power2.out"{"" if n == 0 else ",immediateRender:false"}}},{p});')
    hosts = "\n".join(f'<div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{s0}" '
                      f'data-duration="{round(s1-s0,3)}" data-track-index="{10+n}" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:20"></div>'
                      for n, (sid, s0, s1, _) in enumerate(scenes))
    idx = open(os.path.join(MAIN, "index.html")).read()
    head = idx[:idx.index("<body>")]
    page = f"""{head}<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}">
<div id="hdr"></div>
<div id="glow"></div>
<div id="cam"><video id="aroll" class="clip" src="assets/aroll.mp4" data-start="0" data-duration="{DUR}" data-track-index="1" playsinline data-has-audio="true"></video></div>
<div id="scrim"></div>
{chr(10).join(gl)}
{hosts}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
    open(f"{path}/index.html", "w").write(page)
    for f in ("package.json", "hyperframes.json", "meta.json"):
        open(f"{path}/{f}", "w").write(open(os.path.join(MAIN, f)).read())
    os.makedirs(f"{path}/assets", exist_ok=True)
    if not os.path.exists(f"{path}/assets/fonts"): os.symlink("../../../assets/fonts", f"{path}/assets/fonts")
    if SRC:   # A-roll dari sumber
        f = []
        for i, (a, b, _) in enumerate(keep):
            f += [f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}]",
                  f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={b-a-0.01:.3f}:d=0.01[a{i}]"]
        f.append("".join(f"[v{i}][a{i}]" for i in range(len(keep))) + f"concat=n={len(keep)}:v=1:a=1[vc][ac]")
        f += ["[vc]setpts=PTS/1.1,fps=30,format=yuv420p[vo]", "[ac]atempo=1.1,aresample=48000[ao]"]
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-filter_complex", ";".join(f), "-map", "[vo]", "-map", "[ao]",
                        "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-color_primaries", "bt709", "-color_trc", "bt709",
                        "-colorspace", "bt709", "-c:a", "aac", "-b:a", "256k", "-movflags", "+faststart", f"{path}/assets/aroll.mp4"], check=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{path}/assets/aroll.mp4", "-vn", "-ac", "1", "-ar", "48000", f"{path}/assets/vo.wav"], check=True)
    print(v["id"], DUR, "s", len(dedup), "sfx", flush=True)

if __name__ == "__main__":
    ids = sys.argv[2:]
    for v in V:
        if not ids or v["id"] in ids: build(v)
