#!/usr/bin/env python3
"""Generates the HyperFrames project (index.html + compositions/*.html) for the
Kuasai Algebra TikTok edit. All times below are ABSOLUTE seconds on the edited
A-roll (assets/aroll.mp4); scene files get them converted to local time."""
import json, html, os

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
EDL = os.path.join(HERE, "edl")
DUR = 97.8
W, H = 1080, 1920
ACC = "#FFC21A"  # mustard accent (matches hijab + book cover)

segs = json.load(open(os.path.join(EDL, "map_v2.json")))

# ---------------------------------------------------------------- icons
ICON = {
 "qr": '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="8" y="8" width="3" height="3"/><rect x="13" y="8" width="3" height="3"/><rect x="8" y="13" width="3" height="3"/><path d="M14 14h2v2"/>',
 "play": '<circle cx="12" cy="12" r="9"/><path d="M10 8.5l6 3.5-6 3.5z" fill="#141414"/>',
 "steps": '<path d="M5 6h3M5 12h3M5 18h3"/><path d="M11 6h8M11 12h8M11 18h8"/>',
 "bolt": '<path d="M13 3L5 13.5h6L10 21l8-10.5h-6z" fill="#141414"/>',
 "repeat": '<path d="M4 12a8 8 0 0 1 13.7-5.6L20 9"/><path d="M20 4v5h-5"/><path d="M20 12a8 8 0 0 1-13.7 5.6L4 15"/><path d="M4 20v-5h5"/>',
 "book": '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/>',
 "bag": '<path d="M5 8h14l-1.2 12.5a1.6 1.6 0 0 1-1.6 1.5H7.8a1.6 1.6 0 0 1-1.6-1.5z"/><path d="M9 10V6.5a3 3 0 0 1 6 0V10"/>',
 "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-5.5 6-5.5s6 2.2 6 5.5"/><circle cx="17" cy="9" r="2.6"/><path d="M16 14.6c2.8.2 5 2.2 5 5.4"/>',
 "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 "star": '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z" fill="#141414"/>',
 "screen": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
}
def svg(name):
    return (f'<svg viewBox="0 0 24 24" width="40" height="40" fill="none" stroke="#141414" '
            f'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</svg>')

# ---------------------------------------------------------------- scene specs
# kinds: kick(text) | hl(lines, hi=word, wt=[per-word abs times], punch) |
#        chip(text, icon, y) | eq(text, label) | grid(items[(text,icon,t)])
SCENES = [
 ("s1", 0.0, 17.567, [
   dict(k="hl", s=0.12, e=2.85, lines=["ANAK STRUGGLE", "DENGAN ALGEBRA?"], hi="ALGEBRA?",
        wt=[0.12, 1.30, 1.80, 2.30], punch=True),
   dict(k="kick", s=3.0, e=7.05, text="KEMBANGAN ALGEBRA"),
   dict(k="hl", s=3.7, e=7.05, lines=["JOM TENGOK", "CONTOH NI!"], hi="CONTOH"),
   dict(k="eq", s=7.55, e=10.45, text="5(x − 4)", label="CONTOH DALAM BUKU"),
   dict(k="hl", s=10.7, e=13.25, lines=["MACAM MANA NAK", "KEMBANGKAN?"], hi="KEMBANGKAN?"),
   dict(k="hl", s=13.33, e=14.0, lines=["JANGAN RISAU!"], punch=True),
   dict(k="chip", s=15.45, e=17.5, text="Jalan kira step by step", icon="steps", y=250),
 ]),
 ("s2", 17.567, 41.6, [
   dict(k="kick", s=17.65, e=29.85, text="JALAN KIRA"),
   dict(k="hl", s=18.25, e=22.2, lines=["DARAB DENGAN", "SETIAP SEBUTAN"], hi="SETIAP",
        wt=[18.3, 18.98, 19.42, 20.26]),
   dict(k="eq", s=22.5, e=24.72, text="5 × x = 5x", label="LANGKAH 1"),
   dict(k="eq", s=25.3, e=29.4, text="5 × (−4) = −20", label="LANGKAH 2"),
   dict(k="eq", s=30.85, e=33.5, text="5x − 20", label="JAWAPAN AKHIR ✓"),
   dict(k="hl", s=33.62, e=36.38, lines=["NAMPAK TAK?"], punch=True),
   dict(k="hl", s=36.4, e=41.45, lines=["NOMBOR LUAR ×", "SETIAP SEBUTAN"], hi="SETIAP",
        wt=[36.45, 37.14, 38.94, 39.3]),
 ]),
 ("s3", 41.6, 63.1, [
   dict(k="kick", s=41.7, e=51.95, text="TEKNIK FASTMATHS"),
   dict(k="hl", s=42.15, e=43.7, lines=["KUASAI ALGEBRA"], hi="ALGEBRA"),
   dict(k="hl", s=43.78, e=47.25, lines=["MUDAH & PANTAS"], hi="PANTAS", wt=[44.1, 44.6, 44.84]),
   dict(k="chip", s=45.5, e=47.25, text="Belajar ikut teknik FastMaths", icon="bolt", y=440),
   dict(k="hl", s=48.8, e=51.95, lines=["SUSUN. KIRA. FAHAM."], hi="FAHAM.",
        wt=[48.85, 49.55, 50.9]),
   dict(k="kick", s=52.1, e=63.0, text="BUKAN KEMBANGAN JE!"),
   dict(k="grid", s=53.9, e=63.0, items=[("Asas & Operasi", "check", 54.0), ("Pecahan Algebra", "check", 55.95),
                                          ("Pemfaktoran", "check", 57.5), ("Persamaan Linear", "check", 58.7)]),
 ]),
 ("s4", 63.1, 81.167, [
   dict(k="kick", s=63.2, e=80.95, text="KELEBIHAN BUKU"),
   dict(k="hl", s=63.35, e=65.75, lines=["YANG BESTNYA..."], hi="BESTNYA..."),
   dict(k="hl", s=65.8, e=67.3, lines=["NOTA + LATIHAN", "+ VIDEO"], hi="VIDEO", wt=[65.85, 66.2, 66.44, 66.62, 66.7]),
   dict(k="chip", s=68.3, e=70.85, text="Video tutorial disediakan", icon="play", y=270),
   dict(k="hl", s=70.95, e=72.2, lines=["TAK FAHAM?"], punch=True),
   dict(k="chip", s=72.3, e=74.9, text="Tak faham? Scan QR!", icon="qr", y=270),
   dict(k="hl", s=75.05, e=77.75, lines=["PAUSE. ULANG. FAHAM."], hi="FAHAM.", wt=[75.1, 75.7, 76.8]),
   dict(k="chip", s=75.6, e=77.75, text="Boleh ulang tengok sampai faham", icon="repeat", y=440),
   dict(k="hl", s=78.5, e=80.95, lines=["KELAS ONLINE +", "GROUP SUPPORT"], hi="SUPPORT", wt=[78.6, 79.3, 79.64, 80.0, 80.26]),
 ]),
 ("s5", 81.167, DUR, [
   dict(k="kick", s=81.3, e=85.75, text="SESUAI UNTUK"),
   dict(k="hl", s=81.9, e=84.05, lines=["SEKOLAH MENENGAH"], hi="MENENGAH", wt=[83.3, 83.5]),
   dict(k="hl", s=84.1, e=85.75, lines=["FORM 1 – FORM 5"], punch=True),
   dict(k="hl", s=86.0, e=91.9, lines=["IBU AYAH,", "JUST CONSIDER!"], hi="CONSIDER!"),
   dict(k="hl", s=92.0, e=95.2, lines=["SANGAT BERBALOI"], hi="BERBALOI", punch=True, wt=[92.05, 92.6]),
   dict(k="hl", s=95.3, e=DUR - 0.02, lines=["PAKAI", "BERTAHUN-TAHUN"], hi="BERTAHUN-TAHUN", final=True),
 ]),
]

# b-roll windows: (id, file, start, end, media_start, kenburns from->to, origin)
BROLL = [
 ("b1", "IMG_1165", 7.35, 10.5, 1.5, (1.10, 1.00), "50% 30%"),
 ("b2", "IMG_1162", 14.05, 17.1, 2.5, (1.00, 1.10), "45% 40%"),
 ("b3", "IMG_1164", 29.9, 32.95, 0.2, (1.12, 1.02), "40% 40%"),
 ("b4", "IMG_1167", 53.85, 56.9, 2.0, (1.00, 1.08), "50% 45%"),
 ("b5", "IMG_1166", 67.3, 70.3, 0.3, (1.06, 1.00), "50% 50%"),
 ("b6", "IMG_1166", 72.15, 74.85, 3.6, (1.55, 1.85), "33% 64%"),  # push in on the QR code
]
PUNCH = [1.42, 13.38, 34.18, 46.48, 71.0, 84.16, 92.1]

# ---------------------------------------------------------------- remap v1 times -> current cut
_old = json.load(open(os.path.join(EDL, "map_v1.json"))); _oe = json.load(open(os.path.join(EDL, "final_v1.json")))
_ne = json.load(open(os.path.join(EDL, "final_v2.json")))
DUR = round(segs[-1]["start"] + segs[-1]["dur"], 3)
def R(t):
    for i, m in enumerate(_old):
        if t < m["start"] + m["dur"] or i == len(_old) - 1:
            src = round(_oe[i][2] * 30) / 30 + (t - m["start"])
            return round(segs[i]["start"] + src - round(_ne[i][2] * 30) / 30, 3)
def RB(t):  # scene boundaries sit exactly on segment starts
    for i, m in enumerate(_old):
        if abs(t - m["start"]) < 0.05: return segs[i]["start"]
    return R(t)
SCENES = [(sid, RB(a), (DUR if abs(b - 97.8) < .01 else RB(b)),
           [dict(el, s=R(el["s"]), e=(DUR - 0.02 if el.get("final") else R(el["e"])),
                 **({"wt": [R(x) for x in el["wt"]]} if el.get("wt") else {}),
                 **({"items": [(a2, b2, R(c2)) for a2, b2, c2 in el["items"]]} if el.get("items") else {}))
            for el in els]) for sid, a, b, els in SCENES]
BROLL = [(b, f, R(s0), R(e0), ms, kb, o) for b, f, s0, e0, ms, kb, o in BROLL]
PUNCH = [R(x) for x in PUNCH]

# ---------------------------------------------------------------- v3: pauses/fillers removed + 1.1x speed
_keep = json.load(open(os.path.join(EDL, "keep_v4.json")))
_kept = sum(b - a for a, b in _keep)
_DUR3 = 84.367
_scale = _DUR3 / (_kept / 1.1)
def R3(t):
    acc = 0.0
    for a, b in _keep:
        if t < a: return round(acc / 1.1 * _scale, 3)
        if t <= b: return round((acc + t - a) / 1.1 * _scale, 3)
        acc += b - a
    return _DUR3
DUR = _DUR3
SCENES = [(sid, R3(a), (DUR if b >= 101 else R3(b)),
           [dict(el, s=R3(el["s"]), e=(DUR - 0.02 if el.get("final") else R3(el["e"])),
                 **({"wt": [R3(x) for x in el["wt"]]} if el.get("wt") else {}),
                 **({"items": [(a2, b2, R3(c2)) for a2, b2, c2 in el["items"]]} if el.get("items") else {}))
            for el in els]) for sid, a, b, els in SCENES]
BROLL = [(b, f, R3(s0), R3(e0), ms, kb, o) for b, f, s0, e0, ms, kb, o in BROLL]
PUNCH = [R3(x) for x in PUNCH]
segs = [{"start": R3(a), "dur": round(R3(b) - R3(a), 3)} for a, b in _keep]

# ---------------------------------------------------------------- scene writer
SCENE_CSS = f"""
#root{{position:absolute;inset:0;font-family:'Montserrat',sans-serif;color:#fff;}}
.clip.slot{{position:absolute;left:0;width:{W}px;text-align:center;}}
.in{{display:inline-block;position:relative;}}
.kick .in{{font-weight:800;font-size:30px;letter-spacing:.2em;padding:10px 26px 10px 30px;border:3px solid {ACC};
  border-radius:999px;background:rgba(0,0,0,.38);}}
.hl .in{{font-weight:900;line-height:1.02;letter-spacing:-.01em;text-shadow:0 6px 28px rgba(0,0,0,.6),0 2px 4px rgba(0,0,0,.5);}}
.hl .ln{{display:block;white-space:nowrap;}}
.w{{display:inline-block;position:relative;margin:0 .12em;isolation:isolate;}}
.bar{{position:absolute;left:-4%;right:-4%;bottom:-.08em;height:.16em;background:{ACC};border-radius:6px;z-index:-1;}}
.chip .in{{display:inline-flex;align-items:center;gap:18px;padding:14px 34px 14px 14px;border-radius:999px;
  background:rgba(16,15,18,.84);border:3px solid {ACC};box-shadow:0 14px 40px rgba(0,0,0,.45);}}
.ico{{width:64px;height:64px;border-radius:50%;background:{ACC};display:flex;align-items:center;justify-content:center;flex:none;}}
.ct{{font-weight:800;font-size:42px;white-space:nowrap;}}
.eq .in{{padding:16px 54px 24px;border-radius:40px;background:rgba(16,15,18,.86);border:4px solid {ACC};
  box-shadow:0 18px 50px rgba(0,0,0,.5);}}
.eq .lab{{display:block;font-weight:800;font-size:28px;letter-spacing:.18em;color:{ACC};margin-bottom:2px;}}
.eq .ex{{display:block;font-weight:900;font-size:104px;line-height:1.05;white-space:nowrap;}}
.grid{{display:grid;grid-template-columns:repeat(2,470px);gap:18px 20px;justify-content:center;}}
.gi{{display:flex;align-items:center;gap:14px;padding:10px 22px 10px 10px;border-radius:999px;background:rgba(16,15,18,.84);
  border:3px solid {ACC};box-shadow:0 10px 30px rgba(0,0,0,.4);}}
.gi .ico{{width:54px;height:54px;}}
.gi .ct{{font-size:34px;}}
.burst{{position:absolute;left:46px;top:50%;width:0;height:0;}}
.burst i{{position:absolute;left:0;top:-3px;width:46px;height:6px;border-radius:3px;background:{ACC};transform-origin:0 50%;}}
"""

def hl_html(i, el):
    words = [w for ln in el["lines"] for w in ln.split(" ")]
    longest = max(len(l) for l in el["lines"])
    fs = 96 if len(el["lines"]) == 1 else 84
    fs = min(fs, int(900 / (longest * 0.72)))
    out, wi = [], 0
    for ln in el["lines"]:
        parts = []
        for w in ln.split(" "):
            bar = f'<span class="bar" id="{i}-bar"></span>' if w == el.get("hi") else ""
            parts.append(f'<span class="w" id="{i}-w{wi}">{bar}{html.escape(w)}</span>')
            wi += 1
        out.append(f'<span class="ln">{" ".join(parts)}</span>')
    top = 268 if len(el["lines"]) == 2 else 300
    return f'<div class="in" id="{i}-in" style="font-size:{fs}px">{"".join(out)}</div>', top, len(words)

def burst_html(i):
    return f'<div class="burst" id="{i}-burst">' + "".join(
        f'<i style="rotate:{a}deg"></i>' for a in range(0, 360, 45)) + "</div>"

def write_scene(sid, s0, s1, els):
    body, js = [], []
    ins = lambda t: round(t - s0, 3)
    for n, el in enumerate(els):
        i = f"{sid}-{el['k']}{n}"
        st, en = ins(el["s"]), ins(el["e"])
        d = round(en - st, 3)
        k = el["k"]
        if k == "kick":
            body.append(f'<div id="{i}" class="clip slot kick" data-start="{st}" data-duration="{d}" data-track-index="1" style="top:196px">'
                        f'<div class="in" id="{i}-in">{html.escape(el["text"])}</div></div>')
            js.append(f'tl.fromTo("#{i}-in",{{opacity:0,clipPath:"inset(0 50% 0 50% round 999px)"}},{{opacity:1,clipPath:"inset(0 0% 0 0% round 999px)",duration:.42,ease:"expo.out"}},{st});')
            js.append(f'tl.to("#{i}-in",{{opacity:0,duration:.2,ease:"power2.in"}},{round(en-.22,3)});')
        elif k == "hl":
            inner, top, nw = hl_html(i, el)
            body.append(f'<div id="{i}" class="clip slot hl" data-start="{st}" data-duration="{d}" data-track-index="2" style="top:{top}px">{inner}</div>')
            wt = el.get("wt") or [el["s"] + 0.07 * j for j in range(nw)]
            wt = (wt + [wt[-1] + 0.07 * (j + 1) for j in range(nw)])[:nw]
            for j in range(nw):
                t = round(max(st, min(ins(max(wt[j], el["s"])), en - 0.56)), 3)
                js.append(f'tl.fromTo("#{i}-w{j}",{{opacity:0,y:46,scale:.55,filter:"blur(10px)"}},{{opacity:1,y:0,scale:1,filter:"blur(0px)",duration:.34,ease:"back.out(2.2)"}},{t});')
            if el.get("hi"):
                js.append(f'tl.fromTo("#{i}-bar",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:.38,ease:"expo.out"}},{round(ins(max(wt))+.12,3)});')
            if el.get("punch"):
                js.append(f'tl.fromTo("#{i}-in",{{scale:1.35}},{{scale:1,duration:.38,ease:"expo.out"}},{st});')
            if not el.get("final"):
                for j in range(nw):
                    js.append(f'tl.to("#{i}-w{j}",{{opacity:0,y:-22,filter:"blur(8px)",duration:.16,ease:"power2.in"}},{round(en-.2+0.0*j,3)});')
        elif k == "chip":
            body.append(f'<div id="{i}" class="clip slot chip" data-start="{st}" data-duration="{d}" data-track-index="3" style="top:{el["y"]}px">'
                        f'<div class="in" id="{i}-in">{burst_html(i)}<span class="ico" id="{i}-ico">{svg(el["icon"])}</span>'
                        f'<span class="ct" id="{i}-ct">{html.escape(el["text"])}</span></div></div>')
            js += [f'tl.fromTo("#{i}-in",{{opacity:0,scale:.4,y:30}},{{opacity:1,scale:1,y:0,duration:.42,ease:"back.out(2.4)"}},{st});',
                   f'tl.fromTo("#{i}-ico",{{rotation:-120,scale:.3}},{{rotation:0,scale:1,duration:.5,ease:"back.out(2)"}},{round(st+.05,3)});',
                   f'tl.fromTo("#{i}-ct",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:.4,ease:"power3.out"}},{round(st+.12,3)});',
                   f'tl.fromTo("#{i}-burst i",{{scaleX:0,x:30,opacity:1}},{{scaleX:1,x:58,opacity:0,duration:.5,ease:"expo.out"}},{round(st+.08,3)});',
                   f'tl.to("#{i}-in",{{opacity:0,scale:.85,duration:.2,ease:"power2.in"}},{round(en-.22,3)});']
        elif k == "eq":
            body.append(f'<div id="{i}" class="clip slot eq" data-start="{st}" data-duration="{d}" data-track-index="3" style="top:250px">'
                        f'<div class="in" id="{i}-in">{burst_html(i)}<span class="lab">{html.escape(el["label"])}</span>'
                        f'<span class="ex" id="{i}-ex">{html.escape(el["text"])}</span></div></div>')
            js += [f'tl.fromTo("#{i}-in",{{opacity:0,scale:1.7,filter:"blur(14px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:.34,ease:"expo.out"}},{st});',
                   f'tl.fromTo("#{i}-burst i",{{scaleX:0,x:20,opacity:1}},{{scaleX:1.3,x:70,opacity:0,duration:.55,ease:"expo.out"}},{round(st+.12,3)});',
                   f'tl.to("#{i}-in",{{opacity:0,scale:.9,filter:"blur(8px)",duration:.2,ease:"power2.in"}},{round(en-.22,3)});']
        elif k == "grid":
            items = "".join(f'<div class="gi" id="{i}-g{j}"><span class="ico">{svg(ic)}</span><span class="ct">{html.escape(tx)}</span></div>'
                            for j, (tx, ic, _) in enumerate(el["items"]))
            body.append(f'<div id="{i}" class="clip slot gridw" data-start="{st}" data-duration="{d}" data-track-index="3" style="top:272px">'
                        f'<div class="grid" id="{i}-in">{items}</div></div>')
            for j, (_, _, t) in enumerate(el["items"]):
                js.append(f'tl.fromTo("#{i}-g{j}",{{opacity:0,scale:.3,y:24}},{{opacity:1,scale:1,y:0,duration:.4,ease:"back.out(2.6)"}},{ins(t)});')
            js.append(f'tl.to("#{i}-in",{{opacity:0,y:-16,duration:.22,ease:"power2.in"}},{round(en-.24,3)});')
    doc = f"""<template>
<style>{SCENE_CSS}</style>
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
    os.makedirs(f"{PROJ}/compositions", exist_ok=True)
    open(f"{PROJ}/compositions/{sid}.html", "w").write(doc)

for sid, s0, s1, els in SCENES:
    write_scene(sid, s0, s1, els)

# ---------------------------------------------------------------- root
GLYPHS = [("×", 70, 70, 74), ("x²", 905, 60, 64), ("+", 210, 150, 58), ("=", 800, 170, 66), ("( )", 470, 40, 52),
          ("−", 980, 260, 70), ("÷", 30, 300, 60), ("5x", 640, 120, 50), ("a", 350, 250, 46), ("b", 720, 300, 46)]
glyph_html = "\n".join(f'<span class="gl" data-layout-ignore id="gl{n}" style="left:{x}px;top:{y}px;font-size:{s}px">{html.escape(g)}</span>'
                       for n, (g, x, y, s) in enumerate(GLYPHS))
broll_html = "\n".join(
    f'<div class="bw" id="{b}w" style="transform-origin:{o}"><video id="{b}" class="clip" src="assets/broll/{f}.mp4" '
    f'data-start="{s}" data-duration="{round(e-s,3)}" data-media-start="{ms}" data-track-index="{3+n}" muted playsinline></video></div>'
    for n, (b, f, s, e, ms, kb, o) in enumerate(BROLL))
hosts = "\n".join(
    f'<div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{s0}" '
    f'data-duration="{round(s1-s0,3)}" data-track-index="{10+n}" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:20"></div>'
    for n, (sid, s0, s1, _) in enumerate(SCENES))

# sfx: pop on every chip / eq / grid item, whoosh on every b-roll entrance
sfx = []
for sid, s0, s1, els in SCENES:
    for el in els:
        if el["k"] in ("chip", "eq"):
            sfx.append(("pop", el["s"]))
        if el["k"] == "grid":
            sfx += [("pop", t) for _, _, t in el["items"]]
        if el.get("punch"):
            sfx.append(("pop", el["s"]))
sfx += [("whoosh", b[2] - 0.15) for b in BROLL]
sfx.sort(key=lambda x: x[1])
sfx_html = "\n".join(
    f'<audio id="sfx{n}" class="clip" src="assets/audio/{k}.mp3" data-start="{round(max(t,0),3)}" '
    f'data-duration="{0.5 if k=="whoosh" else 0.6}" data-track-index="{40 if k=="pop" else 41}" data-volume="{0.32 if k=="pop" else 0.45}"></audio>'
    for n, (k, t) in enumerate(sfx))

root_js = []
root_js.append('tl.set("#cam",{y:140,scale:1,transformOrigin:"50% 32%"},0);')
for n, sg in enumerate(segs):
    base = 1.0 if n % 2 == 0 else 1.07
    root_js.append(f'tl.set("#cam",{{scale:{base}}},{sg["start"]});')
    for p in PUNCH:
        if sg["start"] <= p < sg["start"] + sg["dur"]:
            root_js.append(f'tl.fromTo("#cam",{{scale:{base}}},{{scale:{round(base+0.08,3)},duration:.2,ease:"expo.out"}},{p});')
for b, f, s, e, ms, (k0, k1), o in BROLL:
    root_js += [f'tl.fromTo("#{b}w",{{opacity:0}},{{opacity:1,duration:.32,ease:"power2.out"}},{s});',
                f'tl.fromTo("#{b}w",{{scale:{k0}}},{{scale:{k1},duration:{round(e-s,3)},ease:"none"}},{s});',
                f'tl.to("#{b}w",{{opacity:0,duration:.32,ease:"power2.in"}},{round(e-.34,3)});']
# slow drift of header glyphs + glow (constant motion for the animated header)
for n, (g, x, y, s) in enumerate(GLYPHS):
    dx = (-1) ** n * (40 + 9 * n)
    dy = (-1) ** (n // 2) * (14 + 3 * n)
    rot = (-1) ** (n + 1) * (25 + 6 * n)
    root_js.append(f'tl.fromTo("#gl{n}",{{x:0,y:0,rotation:0}},{{x:{dx},y:{dy},rotation:{rot},duration:{DUR},ease:"none"}},0);')
root_js.append(f'tl.fromTo("#glow",{{x:-260}},{{x:260,duration:{DUR/2},ease:"sine.inOut",yoyo:true,repeat:1}},0);')
# glyph flash on every punch
for n, p in enumerate(PUNCH):
    ir = "" if n == 0 else ",immediateRender:false"
    root_js.append(f'tl.fromTo(".gl",{{opacity:.34}},{{opacity:.13,duration:.6,ease:"power2.out"{ir}}},{p});')

index = f"""<!doctype html>
<html lang="ms">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#0d0c0b; }}
#root {{ position:relative; width:{W}px; height:{H}px; overflow:hidden; font-family:'Montserrat',sans-serif; }}
#hdr {{ position:absolute; left:0; top:0; width:{W}px; height:700px; z-index:1;
  background:linear-gradient(180deg,#17140f 0%,#120f0c 55%,#0d0c0b 100%); }}
#glow {{ position:absolute; left:240px; top:-220px; width:600px; height:600px; border-radius:50%; z-index:2;
  background:radial-gradient(circle, rgba(255,194,26,.22) 0%, rgba(255,194,26,0) 70%); }}
#cam {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; z-index:3;
  -webkit-mask-image:linear-gradient(180deg,transparent 0,#000 200px); mask-image:linear-gradient(180deg,transparent 0,#000 200px); }}
#aroll {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; object-fit:cover; }}
#scrim {{ position:absolute; left:0; top:0; width:{W}px; height:620px; z-index:4; pointer-events:none;
  background:linear-gradient(180deg,rgba(13,12,11,.92) 0%,rgba(13,12,11,.6) 300px,rgba(13,12,11,0) 600px); }}
.gl {{ position:absolute; z-index:5; color:{ACC}; opacity:.13; font-weight:800; }}
.bw {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; z-index:8; opacity:0; }}
.bw video {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; object-fit:cover; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}">
<div id="hdr"></div>
<div id="glow"></div>
<div id="cam"><video id="aroll" class="clip" src="assets/aroll.mp4" data-start="0" data-duration="{DUR}" data-track-index="1" playsinline data-has-audio="true"></video></div>
<div id="scrim"></div>
{glyph_html}
{broll_html}
{hosts}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(root_js)}
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
open(f"{PROJ}/index.html", "w").write(index)
print("ok", len(sfx), "sfx")
