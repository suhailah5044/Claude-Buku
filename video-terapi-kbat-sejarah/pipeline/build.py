#!/usr/bin/env python3
"""HyperFrames project untuk TikTok Terapi KBAT Sejarah SPM — GAYA ALGEBRA (saiz kecil).
Teks bold putih tanpa kotak + bayang, bar kuning bawah perkataan penting, pil kuning (kick),
chip ikon bulat kuning untuk USP, header gelap beranimasi atas kepala, zoom punch.
Semua masa = saat dalam assets/aroll.mp4 (dah dipotong + 1.1x; lihat edl.py, tx_final.json).
Footage dah diedit pengguna: warna/cahaya TIDAK diubah."""
import html, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
W, H = 1080, 1920
ACC = "#FFC21A"
DUR = 42.24
FONT = "".join(f"@font-face{{font-family:'Montserrat';src:url({{P}}assets/fonts/montserrat-latin-{w}-normal.woff2) format('woff2');font-weight:{w};}}"
               for w in (700, 800, 900))

# shot (final time): free space differs -> y override for elements on the cover close-up
SHOTS = [0, 4.23, 7.088, 10.094, 15.066, 16.985, 23.727, 26.545, 32.143, 38.925, DUR]

ICON = {
 "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 "play": '<circle cx="12" cy="12" r="9"/><path d="M10 8.5l6 3.5-6 3.5z" fill="#141414"/>',
 "steps": '<path d="M5 6h3M5 12h3M5 18h3"/><path d="M11 6h8M11 12h8M11 18h8"/>',
 "book": '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/>',
 "star": '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z" fill="#141414"/>',
 "grid": '<rect x="4" y="4" width="7" height="7" rx="1"/><rect x="13" y="4" width="7" height="7" rx="1"/><rect x="4" y="13" width="7" height="7" rx="1"/><rect x="13" y="13" width="7" height="7" rx="1"/>',
 "fire": '<path d="M12 3c1 3.5 5 5.5 5 10a5 5 0 0 1-10 0c0-2.2 1-3.6 2.2-4.6.2 1.6 1 2.6 2 3C11 9 10.8 6 12 3z" fill="#141414"/>',
}
def svg(name, s=30):
    return (f'<svg viewBox="0 0 24 24" width="{s}" height="{s}" fill="none" stroke="#141414" '
            f'stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</svg>')

FIRE = ('<svg class="fire" viewBox="0 0 24 24" fill="#FF7A1A"><path d="M12 2c1.2 4 6 6.2 6 11.2A6 6 0 0 1 6 13.2c0-2.6 1.2-4.3 2.6-5.4.2 1.9 1.2 3.1 2.4 3.6C10.6 8.2 10.4 4.8 12 2z"/>'
        '<path d="M12 12.5c.5 1.6 2.6 2.4 2.6 4.4a2.6 2.6 0 0 1-5.2 0c0-1 .4-1.7 1-2.2.1.8.5 1.3 1 1.5-.2-1.3-.1-2.6.6-3.7z" fill="#FFC21A"/></svg>')

# kinds: kick(text) | hl(lines, hi, wt, punch, static, y) | chip(text, icon, y) | tick(text) | sub(text, y)
SCENES = [
 ("s1", 0.0, 4.2, [
   dict(k="kick", s=0.0, e=4.15, text="JAWAB KBAT, MARKAH PENUH? @FIRE", static=True),
   dict(k="hl", s=0.0, e=4.15, lines=["RAMAI STUDENT", "HILANG MARKAH"], hi="MARKAH", static=True, wt=[2.78]),
   dict(k="sub", s=0.0, e=4.15, text="sebab tak kuasai <b>TEKNIK KBAT SEJARAH SPM</b>", y=420, static=True),
 ]),
 ("s2", 4.2, 7.15, [
   dict(k="hl", s=4.22, e=4.76, lines=["SEBAB APA?"], hi="APA?", punch=True, wt=[4.22, 4.64]),
   dict(k="hl", s=4.80, e=7.1, lines=["TAK TAHU TEKNIK JAWAB", "IKUT KEHENDAK SOALAN"], hi="SOALAN",
        wt=[5.02, 5.18, 5.34, 5.78, 6.02, 6.32, 6.74]),
 ]),
 ("s3", 7.15, 10.1, [
   dict(k="kick", s=7.24, e=10.05, text="TEKNIK MENJAWAB"),
   dict(k="hl", s=7.66, e=10.05, lines=["TEKNIK JAWAB KBAT"], hi="KBAT", wt=[7.66, 7.94, 8.60]),
   dict(k="chip", s=9.0, e=10.05, text="Jawab lebih teratur", icon="steps", y=420),
 ]),
 ("s4", 10.1, 13.04, [
   dict(k="kick", s=10.14, e=13.0, text="LANGKAH DEMI LANGKAH"),
   dict(k="hl", s=10.38, e=13.0, lines=["IKUT LANGKAH,", "ISI SETIAP KOTAK"], hi="KOTAK",
        wt=[10.38, 10.66, 12.0, 12.32, 12.58]),
 ]),
 ("s5", 13.04, 15.1, [
   dict(k="hl", s=13.5, e=15.05, lines=["SOALAN", "FORMAT SPM"], hi="SPM", wt=[13.64, 14.04, 14.44], punch=True),
 ]),
 ("s6", 15.1, 17.1, [
   dict(k="hl", s=15.2, e=17.0, lines=["VIDEO PENERANGAN", "PUN ADA!"], hi="ADA!", y=600,
        wt=[15.2, 15.38, 15.96, 16.16]),
   dict(k="sub", s=15.7, e=17.0, text="Belajar <b>step by step</b>", y=750),
 ]),
 ("s7", 17.1, 23.72, [
   dict(k="kick", s=17.12, e=23.68, text="TENGOK CARA PEMERIKSA NAK"),
   dict(k="hl", s=18.4, e=19.55, lines=["SKEMA JAWAPAN", "LENGKAP"], hi="LENGKAP", wt=[18.6, 18.88, 19.32]),
   dict(k="chip", s=19.6, e=22.08, text="Siap dengan contoh jawapan", icon="check", y=300),
   dict(k="hl", s=22.14, e=23.68, lines=["IKUT KEHENDAK", "PEMERIKSA"], hi="PEMERIKSA", punch=True, wt=[22.14, 22.58, 22.84]),
 ]),
 ("s8", 23.72, 26.6, [
   dict(k="kick", s=23.74, e=26.55, text="TERAPI KBAT SEJARAH SPM"),
   dict(k="hl", s=25.5, e=26.55, lines=["SANGAT-SANGAT", "MENARIK!"], hi="MENARIK!", wt=[25.66, 26.18]),
 ]),
 ("s9", 26.6, 32.18, [
   dict(k="kick", s=26.62, e=31.1, text="8 JENIS KBAT"),
   dict(k="tick", s=27.74, e=28.26, text="KBAT FAKTA"),
   dict(k="tick", s=28.28, e=28.56, text="LANGSUNG"),
   dict(k="tick", s=28.58, e=29.16, text="PETIKAN PENDEK"),
   dict(k="tick", s=29.18, e=29.62, text="PETIKAN PANJANG"),
   dict(k="tick", s=29.64, e=30.1, text="POSTER"),
   dict(k="tick", s=30.12, e=30.56, text="LIRIK LAGU"),
   dict(k="tick", s=30.58, e=30.86, text="PUISI"),
   dict(k="tick", s=30.88, e=31.1, text="GRAF"),
   dict(k="hl", s=31.24, e=32.14, lines=["+ RUMUS P.E.S."], hi="P.E.S.", punch=True, wt=[31.24, 31.4, 31.64]),
 ]),
 ("s10", 32.18, 38.9, [
   dict(k="hl", s=32.22, e=34.95, lines=["RANGKA", "STRUKTUR KOTAK"], hi="KOTAK", wt=[32.22, 32.52, 32.85]),
   dict(k="chip", s=33.3, e=34.95, text="Bantu susun idea & jawapan", icon="grid", y=440),
   dict(k="kick", s=35.16, e=38.85, text="SIAP DENGAN VIDEO"),
   dict(k="hl", s=35.9, e=38.85, lines=["AJAR", "STEP BY STEP"], hi="STEP", wt=[36.38, 36.6, 36.74, 36.98]),
   dict(k="chip", s=37.32, e=38.85, text="Penerangan + skema jawapan", icon="book", y=440),
 ]),
 ("s11", 38.9, DUR, [
   dict(k="kick", s=38.94, e=DUR - 0.02, text="PERSEDIAAN SPM", final=True),
   dict(k="hl", s=38.94, e=40.95, lines=["BOOST KBAT", "SEJARAH! @FIRE"], hi="SEJARAH!", punch=True, wt=[38.94, 39.6, 40.5]),
   dict(k="hl", s=41.0, e=DUR - 0.02, lines=["JOM BUAT", "PERSEDIAAN AWAL!"], hi="AWAL!", final=True, wt=[41.0, 41.2, 41.5]),
 ]),
]
PUNCH = [2.78, 4.22, 13.64, 22.14, 31.4, 38.94]

# SFX (jarang & bertukar-tukar) -> dicampur dalam mux.py
SFX = [(0.0, "ov"), (4.22, "tr"), (7.66, "ov"), (10.38, "tr"), (13.64, "ov"), (15.15, "tr"), (18.6, "ov"),
       (22.14, "tr"), (25.66, "ov"), (27.74, "ov"), (29.18, "ov"), (31.4, "ov"), (32.22, "tr"), (36.0, "ov"),
       (38.94, "tr"), (41.0, "ov")]
json.dump(SFX, open(f"{HERE}/sfx.json", "w"))

SCENE_CSS = f"""
#root{{position:absolute;inset:0;font-family:'Montserrat',sans-serif;color:#fff;}}
.clip.slot{{position:absolute;left:0;width:{W}px;text-align:center;}}
.in{{display:inline-block;position:relative;}}
.kick .in{{font-weight:800;font-size:22px;letter-spacing:.18em;padding:8px 20px 8px 24px;border:2.5px solid {ACC};
  border-radius:999px;background:rgba(0,0,0,.38);text-shadow:0 2px 6px rgba(0,0,0,.5);}}
.hl .in{{font-weight:900;line-height:1.04;letter-spacing:-.005em;text-shadow:0 4px 18px rgba(0,0,0,.75),0 2px 3px rgba(0,0,0,.6);}}
.hl .ln{{display:block;white-space:nowrap;}}
.w{{display:inline-block;position:relative;margin:0 .11em;isolation:isolate;}}
.bar{{position:absolute;left:-4%;right:-4%;bottom:-.06em;height:.16em;background:{ACC};border-radius:5px;z-index:-1;}}
.sub .in{{font-weight:800;font-size:28px;text-shadow:0 3px 12px rgba(0,0,0,.8),0 1px 2px rgba(0,0,0,.7);}}
.sub b{{color:{ACC};font-weight:900;}}
.tick .in{{font-weight:900;font-size:50px;color:{ACC};text-shadow:0 4px 16px rgba(0,0,0,.8),0 2px 3px rgba(0,0,0,.6);}}
.chip .in{{display:inline-flex;align-items:center;gap:12px;padding:8px 24px 8px 8px;border-radius:999px;
  background:rgba(16,15,18,.78);border:2.5px solid {ACC};box-shadow:0 10px 28px rgba(0,0,0,.4);}}
.ico{{width:44px;height:44px;border-radius:50%;background:{ACC};display:flex;align-items:center;justify-content:center;flex:none;}}
.ct{{font-weight:800;font-size:29px;white-space:nowrap;}}
.fire{{display:inline-block;width:1.05em;height:1.05em;vertical-align:-.16em;}}
.kick .fire{{width:1.3em;height:1.3em;vertical-align:-.3em;margin-left:.1em;}}
.burst{{position:absolute;left:30px;top:50%;width:0;height:0;}}
.burst i{{position:absolute;left:0;top:-2px;width:30px;height:4px;border-radius:2px;background:{ACC};transform-origin:0 50%;}}
"""

def esc(t):
    return html.escape(t).replace("@FIRE", FIRE)

def hl_html(i, el):
    longest = max(len(l) for l in el["lines"])
    fs = 64 if len(el["lines"]) == 1 else 58
    fs = min(fs, int(820 / (longest * 0.74)))
    out, wi = [], 0
    for ln in el["lines"]:
        parts = []
        for w in ln.split(" "):
            bar = f'<span class="bar" id="{i}-bar"></span>' if w == el.get("hi") else ""
            parts.append(f'<span class="w" id="{i}-w{wi}">{bar}{esc(w)}</span>')
            wi += 1
        out.append(f'<span class="ln">{" ".join(parts)}</span>')
    top = el.get("y", 268 if len(el["lines"]) == 2 else 290)
    return f'<div class="in" id="{i}-in" style="font-size:{fs}px">{"".join(out)}</div>', top, wi

def burst_html(i):
    return f'<div class="burst" id="{i}-burst">' + "".join(f'<i style="rotate:{a}deg"></i>' for a in range(0, 360, 45)) + "</div>"

def write_scene(sid, s0, s1, els):
    body, js = [], []
    ins = lambda t: round(max(0, t - s0), 3)
    for n, el in enumerate(els):
        i = f"{sid}-{el['k']}{n}"
        st, en = ins(el["s"]), ins(el["e"])
        d = round(en - st, 3)
        k = el["k"]
        out_js = None if el.get("final") else en
        if k == "kick":
            body.append(f'<div id="{i}" class="clip slot kick" data-start="{st}" data-duration="{d}" data-track-index="1" style="top:{el.get("y", 196)}px">'
                        f'<div class="in" id="{i}-in">{esc(el["text"])}</div></div>')
            if el.get("static"):
                js.append(f'tl.fromTo("#{i}-in",{{scale:1.12}},{{scale:1,duration:.4,ease:"expo.out"}},{st});')
            else:
                js.append(f'tl.fromTo("#{i}-in",{{opacity:0,clipPath:"inset(0 50% 0 50% round 999px)"}},{{opacity:1,clipPath:"inset(0 0% 0 0% round 999px)",duration:.4,ease:"expo.out"}},{st});')
            if out_js: js.append(f'tl.to("#{i}-in",{{opacity:0,duration:.18,ease:"power2.in"}},{round(en-.2,3)});')
        elif k == "sub":
            body.append(f'<div id="{i}" class="clip slot sub" data-start="{st}" data-duration="{d}" data-track-index="4" style="top:{el["y"]}px">'
                        f'<div class="in" id="{i}-in">{el["text"]}</div></div>')
            if not el.get("static"):
                js.append(f'tl.fromTo("#{i}-in",{{opacity:0,y:18,filter:"blur(6px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.32,ease:"power3.out"}},{st});')
            js.append(f'tl.to("#{i}-in",{{opacity:0,y:-10,duration:.18,ease:"power2.in"}},{round(en-.2,3)});')
        elif k == "tick":
            body.append(f'<div id="{i}" class="clip slot tick" data-start="{st}" data-duration="{d}" data-track-index="2" style="top:272px">'
                        f'<div class="in" id="{i}-in">{esc(el["text"])}</div></div>')
            js.append(f'tl.fromTo("#{i}-in",{{opacity:0,y:30,scale:.7,filter:"blur(6px)"}},{{opacity:1,y:0,scale:1,filter:"blur(0px)",duration:.16,ease:"back.out(2.4)"}},{st});')
        elif k == "hl":
            inner, top, nw = hl_html(i, el)
            body.append(f'<div id="{i}" class="clip slot hl" data-start="{st}" data-duration="{d}" data-track-index="2" style="top:{top}px">{inner}</div>')
            wt = el.get("wt") or [el["s"]]
            if el.get("static"):
                # thumbnail: teks penuh dari frame pertama; punch kecil pada masa perkataan disebut
                js.append(f'tl.fromTo("#{i}-in",{{scale:1.1}},{{scale:1,duration:.45,ease:"expo.out"}},{st});')
                for t in wt:
                    js.append(f'tl.fromTo("#{i}-in",{{scale:1.08}},{{scale:1,duration:.35,ease:"expo.out",immediateRender:false}},{ins(t)});')
                if el.get("hi"):
                    js.append(f'tl.set("#{i}-bar",{{scaleX:1}},0);')
            else:
                wt = (wt + [wt[-1] + 0.07 * (j + 1) for j in range(nw)])[:nw]
                for j in range(nw):
                    t = round(max(st, min(ins(max(wt[j], el["s"])), en - 0.4)), 3)
                    js.append(f'tl.fromTo("#{i}-w{j}",{{opacity:0,y:34,scale:.55,filter:"blur(8px)"}},{{opacity:1,y:0,scale:1,filter:"blur(0px)",duration:.3,ease:"back.out(2.2)"}},{t});')
                if el.get("hi"):
                    js.append(f'tl.fromTo("#{i}-bar",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:.34,ease:"expo.out"}},{round(min(ins(max(wt)) + .1, en - .3), 3)});')
                if el.get("punch"):
                    js.append(f'tl.fromTo("#{i}-in",{{scale:1.3}},{{scale:1,duration:.36,ease:"expo.out"}},{st});')
            if out_js:
                for j in range(nw):
                    js.append(f'tl.to("#{i}-w{j}",{{opacity:0,y:-18,filter:"blur(6px)",duration:.15,ease:"power2.in"}},{round(en-.18,3)});')
        elif k == "chip":
            body.append(f'<div id="{i}" class="clip slot chip" data-start="{st}" data-duration="{d}" data-track-index="3" style="top:{el["y"]}px">'
                        f'<div class="in" id="{i}-in">{burst_html(i)}<span class="ico" id="{i}-ico">{svg(el["icon"])}</span>'
                        f'<span class="ct" id="{i}-ct">{esc(el["text"])}</span></div></div>')
            js += [f'tl.fromTo("#{i}-in",{{opacity:0,scale:.4,y:24}},{{opacity:1,scale:1,y:0,duration:.4,ease:"back.out(2.4)"}},{st});',
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
    os.makedirs(f"{PROJ}/compositions", exist_ok=True)
    open(f"{PROJ}/compositions/{sid}.html", "w").write(doc)

for sid, s0, s1, els in SCENES:
    write_scene(sid, s0, s1, els)

# ---------------------------------------------------------------- root
GLYPHS = [("A+", 60, 60, 66), ("?", 905, 50, 70), ("SPM", 200, 150, 40), ("✓", 800, 165, 56), ("KBAT", 450, 34, 38),
          ("!", 990, 250, 64), ("P.E.S.", 18, 300, 34), ("1957", 640, 110, 40), ("?", 340, 250, 46), ("A+", 720, 290, 42)]
glyph_html = "\n".join(f'<span class="gl" data-layout-ignore id="gl{n}" style="left:{x}px;top:{y}px;font-size:{s}px">{html.escape(g)}</span>'
                       for n, (g, x, y, s) in enumerate(GLYPHS))
hosts = "\n".join(
    f'<div id="{sid}" data-composition-id="{sid}" data-composition-src="compositions/{sid}.html" data-start="{s0}" '
    f'data-duration="{round(s1-s0,3)}" data-track-index="{10+n}" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:20"></div>'
    for n, (sid, s0, s1, _) in enumerate(SCENES))

root_js = ['tl.set("#cam",{y:140,scale:1,transformOrigin:"50% 32%"},0);']
for n in range(len(SHOTS) - 1):
    a, b = SHOTS[n], SHOTS[n + 1]
    base = 1.0 if n % 2 == 0 else 1.04
    root_js.append(f'tl.fromTo("#cam",{{scale:{base}}},{{scale:{round(base+0.03,3)},duration:{round(b-a,3)},ease:"none"}},{a});')  # slow push-in
    for p in PUNCH:
        if a <= p < b:
            pb = round(base + 0.03 * (p - a) / (b - a), 3)
            root_js.append(f'tl.to("#cam",{{scale:{round(pb+0.07,3)},duration:.14,ease:"expo.out"}},{p});')
            root_js.append(f'tl.to("#cam",{{scale:{round(base+0.03*(min(p+.5,b)-a)/(b-a),3)},duration:.36,ease:"power2.out"}},{round(p+.14,3)});')
            root_js.append(f'tl.fromTo("#cam",{{scale:{round(base+0.03*(min(p+.5,b)-a)/(b-a),3)}}},{{scale:{round(base+0.03,3)},duration:{round(max(b-p-.5,.05),3)},ease:"none",immediateRender:false}},{round(min(p+.5,b-.05),3)});')
for n, (g, x, y, s) in enumerate(GLYPHS):
    dx = (-1) ** n * (40 + 9 * n); dy = (-1) ** (n // 2) * (14 + 3 * n); rot = (-1) ** (n + 1) * (20 + 6 * n)
    root_js.append(f'tl.fromTo("#gl{n}",{{x:0,y:0,rotation:0}},{{x:{dx},y:{dy},rotation:{rot},duration:{DUR},ease:"none"}},0);')
root_js.append(f'tl.fromTo("#glow",{{x:-260}},{{x:260,duration:{DUR/2},ease:"sine.inOut",yoyo:true,repeat:1}},0);')
for n, p in enumerate(PUNCH):
    ir = "" if n == 0 else ",immediateRender:false"
    root_js.append(f'tl.fromTo(".gl",{{opacity:.34}},{{opacity:.12,duration:.6,ease:"power2.out"{ir}}},{p});')

index = f"""<!doctype html>
<html lang="ms">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
{FONT.replace('{P}', '')}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:#0d0c0b; }}
#root {{ position:relative; width:{W}px; height:{H}px; overflow:hidden; font-family:'Montserrat',sans-serif; }}
#hdr {{ position:absolute; left:0; top:0; width:{W}px; height:520px; z-index:1;
  background:linear-gradient(180deg,#17140f 0%,#120f0c 55%,#0d0c0b 100%); }}
#glow {{ position:absolute; left:240px; top:-220px; width:600px; height:600px; border-radius:50%; z-index:2;
  background:radial-gradient(circle, rgba(255,194,26,.22) 0%, rgba(255,194,26,0) 70%); }}
#cam {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; z-index:3;
  -webkit-mask-image:linear-gradient(180deg,transparent 0,#000 190px); mask-image:linear-gradient(180deg,transparent 0,#000 190px); }}
#aroll {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; object-fit:cover; }}
#scrim {{ position:absolute; left:0; top:0; width:{W}px; height:520px; z-index:4; pointer-events:none;
  background:linear-gradient(180deg,rgba(13,12,11,.9) 0%,rgba(13,12,11,.45) 260px,rgba(13,12,11,0) 500px); }}
.gl {{ position:absolute; z-index:5; color:{ACC}; opacity:.12; font-weight:800; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}">
<div id="hdr"></div>
<div id="glow"></div>
<div id="cam"><video id="aroll" class="clip" src="assets/aroll.mp4" data-start="0" data-duration="{DUR}" data-track-index="1" playsinline data-has-audio="true"></video></div>
<div id="scrim"></div>
{glyph_html}
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
print("ok", len(SFX), "sfx")
