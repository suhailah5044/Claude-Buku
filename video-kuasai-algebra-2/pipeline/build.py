#!/usr/bin/env python3
"""Jana index.html + compositions/s1.html untuk Kuasai Algebra (versi voiceover).
Masa di bawah = saat pada assets/plate.mp4 (dah dipotong + 1.1x)."""
import os, sys, json, html, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gfx
from gfx import W, H, ACC, PROJ
DUR = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                            f"{PROJ}/assets/plate.mp4"], capture_output=True, text=True).stdout)
DUR = round(DUR, 3)

# hook: teks dari frame 0 (thumbnail); footage di-zoom 0-4.5 s supaya teks lama yang dibakar dalam footage (y 240-700, hingga 4.4 s)
HOOK_END = 4.95
HOOK = [  # (start, end, label, lines, highlight)
    (0.0, 3.78, "DAH BANYAK KALI BUAT LATIHAN...", ["ANAK MASIH", "TAK FAHAM", "ALGEBRA?"], "ALGEBRA?"),
    (3.78, HOOK_END, "KADANG-KADANG...", ["BUKAN TAK", "BOLEH BUAT"], "BUAT"),
]
ELS = [
    dict(k="hl", s=4.96, e=7.12, lines=["CUMA TAK TAHU", "NAK START!"], hi="START!", wt=[4.96, 5.96, 6.2, 6.4, 6.6]),
    dict(k="kick", s=7.16, e=8.88, text="KEMBANGAN ALGEBRA"),
    dict(k="hl", s=7.3, e=8.88, lines=["MASIH STRUGGLE?"], hi="STRUGGLE?", wt=[7.38, 7.54]),
    dict(k="kick", s=8.92, e=11.48, text="JOM CUBA BUKU NI"),
    dict(k="hl", s=9.85, e=11.48, lines=["KUASAI ALGEBRA"], hi="ALGEBRA", punch=True, wt=[9.9, 10.42]),
    dict(k="chip", s=12.3, e=14.1, text="Nota penerangan lengkap", icon="book", y=250),
    dict(k="chip", s=13.35, e=14.1, text="Jalan kira jelas", icon="steps", y=370),
    dict(k="hl", s=14.12, e=16.0, lines=["TAK FAHAM LAGI?"], punch=True, wt=[14.82, 14.98, 15.24]),
    dict(k="chip", s=16.04, e=17.0, text="Scan QR je!", icon="qr", y=270),
    dict(k="hl", s=17.04, e=19.06, lines=["TERUS ADA", "VIDEO GUIDE"], hi="VIDEO", wt=[17.88, 18.16, 18.5, 19.0]),
    dict(k="kick", s=19.12, e=22.6, text="SESUAI UNTUK"),
    dict(k="hl", s=19.6, e=20.98, lines=["SEKOLAH MENENGAH"], hi="MENENGAH"),
    dict(k="hl", s=21.02, e=22.6, lines=["FORM 1 – FORM 5"], punch=True),
    dict(k="hook", s=22.8, e=DUR - 0.02, lines=["MEMANG", "RECOMMEND!"], hi="RECOMMEND!", final=True, y=240),
]
PUNCH = [6.6, 9.9, 14.98, 21.06, 22.66]

gfx.write_scene("s1", 0.0, DUR, ELS)

# ---- sisip kotak hook ke dalam s1.html
hb, hj = [], []
hb.append(f'<div id="hk" class="clip" data-start="0" data-duration="{HOOK_END + 0.25}" data-track-index="5" '
          f'style="position:absolute;left:40px;top:150px;width:1000px;height:470px">'
          '')
for n, (s, e, lab, lines, hi) in enumerate(HOOK):
    ws, wi = [], 0
    for ln in lines:
        parts = []
        for w in ln.split(" "):
            bar = f'<span class="bar" id="hk{n}-bar"></span>' if w == hi else ""
            parts.append(f'<span class="w" id="hk{n}-w{wi}">{bar}{html.escape(w)}</span>'); wi += 1
        ws.append(f'<span style="display:block;white-space:nowrap">{" ".join(parts)}</span>')
    fs = 120 if len(lines) == 3 else 124
    hb.append(f'<div id="hk{n}" style="position:absolute;inset:0;display:flex;flex-direction:column;justify-content:center;'
              f'align-items:center;text-align:center;opacity:{1 if n == 0 else 0}">'
              f'<span style="font-weight:800;font-size:32px;letter-spacing:.14em;color:{ACC};margin-bottom:10px;text-shadow:0 2px 10px rgba(0,0,0,.8)">{html.escape(lab)}</span>'
              f'<span style="font-weight:900;font-size:{fs}px;line-height:1.0;letter-spacing:-.01em;text-shadow:0 6px 30px rgba(0,0,0,.75),0 2px 6px rgba(0,0,0,.6)">{"".join(ws)}</span></div>')
    if n == 0:
        hj.append('tl.to("#hk",{scale:1.04,duration:.14,ease:"power2.out",yoyo:true,repeat:1},.3);')
        for j in range(wi):
            hj.append(f'tl.fromTo("#hk0-w{j}",{{y:0}},{{y:-14,duration:.13,ease:"power2.out",yoyo:true,repeat:1}},{round(.45 + .08 * j, 3)});')
        hj.append(f'tl.fromTo("#hk0-bar",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:.4,ease:"expo.out"}},.75);')
        hj.append(f'tl.to("#hk0",{{opacity:0,y:-30,duration:.16,ease:"power2.in"}},{round(e - .16, 3)});')
    else:
        hj.append(f'tl.fromTo("#hk{n}",{{opacity:0,y:40}},{{opacity:1,y:0,duration:.22,ease:"expo.out"}},{s});')
        hj.append(f'tl.to("#hk",{{scale:1.05,duration:.12,ease:"power2.out",yoyo:true,repeat:1}},{s});')
        hj.append(f'tl.fromTo("#hk{n}-bar",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:.35,ease:"expo.out"}},{round(s + .4, 3)});')
hb.append('</div>')
hj.append(f'tl.to("#hk",{{opacity:0,scale:.85,filter:"blur(10px)",duration:.22,ease:"power2.in"}},{HOOK_END});')
p = f"{PROJ}/compositions/s1.html"
doc = open(p).read()
doc = doc.replace("\n</div>\n<script>", "\n" + "\n".join(hb) + "\n</div>\n<script>", 1)
doc = doc.replace('window.__timelines["s1"]', "\n".join(hj) + '\nwindow.__timelines["s1"]', 1)
open(p, "w").write(doc)

# ---- root
js = ['tl.set("#zw",{scale:1.6},0);',
      'tl.to("#zw",{scale:1.38,duration:.45,ease:"none"},.15);',
      'tl.to("#zw",{scale:1,duration:.4,ease:"power2.inOut"},4.52);']
js += ['tl.fromTo("#plate",{scale:1},{scale:1.07,duration:%s,ease:"none"},0);' % DUR]
for p_ in PUNCH:
    js.append(f'tl.to("#pw",{{scale:1.07,duration:.18,ease:"expo.out"}},{p_});')
    js.append(f'tl.to("#pw",{{scale:1,duration:.6,ease:"power2.inOut"}},{round(p_ + .3, 3)});')
js.append(f'tl.fromTo("#glow",{{x:-260}},{{x:260,duration:{DUR/2},ease:"sine.inOut",yoyo:true,repeat:1}},0);')
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
#pw {{ position:absolute; inset:0; z-index:1; transform-origin:50% 55%; }}
#zw {{ position:absolute; inset:0; transform-origin:50% 100%; }}
#plate {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; object-fit:cover; transform-origin:50% 60%; }}
#scrim {{ position:absolute; left:0; top:0; width:{W}px; height:760px; z-index:4; pointer-events:none;
  background:linear-gradient(180deg,rgba(13,12,11,.88) 0%,rgba(13,12,11,.55) 360px,rgba(13,12,11,0) 740px); }}
#glow {{ position:absolute; left:240px; top:-260px; width:600px; height:600px; border-radius:50%; z-index:5;
  background:radial-gradient(circle, rgba(255,194,26,.20) 0%, rgba(255,194,26,0) 70%); }}
#vig {{ position:absolute; inset:0; z-index:6; pointer-events:none;
  background:radial-gradient(ellipse at 50% 55%, rgba(0,0,0,0) 60%, rgba(0,0,0,.35) 100%); }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="{W}" data-height="{H}">
<div id="pw"><div id="zw"><video id="plate" class="clip" src="assets/plate.mp4" data-start="0" data-duration="{DUR}" data-track-index="1" playsinline data-has-audio="true"></video></div></div>
<div id="scrim"></div>
<div id="glow"></div>
<div id="vig"></div>
<div id="s1" data-composition-id="s1" data-composition-src="compositions/s1.html" data-start="0" data-duration="{DUR}" data-track-index="10" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:20"></div>
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
open(f"{PROJ}/index.html", "w").write(index)
print("ok", DUR)
