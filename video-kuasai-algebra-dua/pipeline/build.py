#!/usr/bin/env python3
"""Kuasai Algebra (Dua.MOV) - gaya "Reel AI Edit" (rujukan pengguna: iklan VGC 'Footage Raw vs Hasil AI Edit'):
- caption kecil HURUF BESAR Montserrat 800, putih + perkataan kuning, tanpa kotak
- tajuk besar font condensed (Anton) di bawah caption kecil, masuk zoom-blur + zoom punch kamera
- senarai bernombor 01/02/.. : baris gelap lut sinar (kaca gelap), ikon garis, baris aktif = bar kiri kuning + perkataan kuning
Footage = video CapCut pengguna (b-roll buku + VO), tone-map HLG, 1.1x, end card CapCut dibuang.
Masa dalam senarai di bawah = masa ASAL Dua.MOV (dibahagi 1.1 secara automatik).
Guna: python3 pipeline/build.py  -> index.html + sfx.json"""
import html, json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(HERE)
SPD = 1.1; DUR = 22.7; ACC = "#FFC21A"
T = lambda t: round(t / SPD, 3)
rich = lambda s: re.sub(r"\*(.+?)\*", r'<b class="hi">\1</b>', html.escape(s))

# ikon garis (viewBox 24)
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

# (mula, tamat, caption kecil, [(masa, tajuk besar)], saiz tajuk)
GROUPS = [
    (0.00, 3.95, "ANAK DAH MASUK *SEKOLAH MENENGAH*?", [(0.00, "ALGEBRA")], 200),
    (4.06, 4.80, "NAMPAK MACAM *SUSAH*...", [], 0),
    (4.80, 6.88, "TAPI BILA DAH TAHU *TEKNIKNYA*", [(6.06, "LEBIH *MUDAH*")], 170),
    (6.88, 8.74, "BUKU *KUASAI ALGEBRA* NI", [(7.92, "BUKAN TOPIK NI JE!")], 116),
    (8.74, 14.72, "", [(8.74, "DALAMNYA ADA")], 130),
    (14.72, 18.74, "", [(14.72, "SIAP ADA")], 150),
    (18.74, 20.56, "SESUAI UNTUK BELAJAR", [(19.38, "FORM *1 – 5*")], 190),
    (20.56, DUR * SPD, "NAK BANTU ANAK?", [(22.02, "KUASAI ALGEBRA")], 150),
]
# senarai: (mula, tamat, [(masa, nombor, ikon, teks, [masa denyut lagi])])  - nombor ikut buku (Kandungan 01-05)
LISTS = [
    (8.74, 14.72, [(9.18, "01", "asas", "*ASAS & OPERASI* ALGEBRA", [9.92]),
                   (10.82, "02", "pecahan", "*PECAHAN* ALGEBRA", []),
                   (11.98, "03", "kembangan", "*KEMBANGAN* ALGEBRA", []),
                   (12.64, "04", "faktor", "*PEMFAKTORAN* ALGEBRA", []),
                   (13.80, "05", "linear", "*PERSAMAAN LINEAR*", [])]),
    (14.72, 18.74, [(15.16, "01", "nota", "*NOTA* RINGKAS", []),
                    (15.82, "02", "contoh", "*CONTOH*", []),
                    (16.22, "03", "latihan", "*LATIHAN*", []),
                    (16.90, "04", "video", "VIDEO TUTORIAL *QR CODE*", [])]),
]
EXTRA = [(23.20, DUR * SPD, "BOLEH *DAPATKAN* BUKU INI!")]   # baris kecil bawah tajuk CTA (ayat pengguna)
CUTS = [2.23, 3.6, 7.27, 9.7, 11.4, 13.77, 16.2, 17.73, 18.97, 19.67, 21.7, 23.2]   # potongan shot dalam footage asal

CAP_TOP = 250    # caption kecil (bawah menu TikTok)
LIST_TOP = 1200  # senarai (atas UI caption TikTok ~1550)

body, js, sfx = [], [], []
ov = 0
def ovs(t):
    sfx.append([t, "ov"])

for g, (s, e, small, bigs, fs) in enumerate(GROUPS):
    s, e = T(s), min(T(e), DUR)
    body.append(f'<div class="grp" id="g{g}">' + (f'<div class="sm" id="g{g}s">{rich(small)}</div>' if small else ''))
    for b, (bt, txt) in enumerate(bigs):
        body.append(f'<div class="big" id="g{g}b{b}" style="font-size:{round(fs*.54)}px">{rich(txt)}</div>')
    if g == len(GROUPS) - 1:
        for x, (xs, xe, xt) in enumerate(EXTRA):
            body.append(f'<div class="sm sm2" id="x{x}">{rich(xt)}</div>')
    body.append('</div>')
    if s < 0.01:   # hook: penuh dari frame 0 (thumbnail) - denyut kecil sahaja
        js.append(f'tl.fromTo("#g{g}b0",{{scale:1}},{{scale:1.06,duration:.22,ease:"power2.out",yoyo:true,repeat:1}},0.3);')
    else:
        if small: js.append(f'tl.fromTo("#g{g}s",{{opacity:0,y:26,clipPath:"inset(0 0 100% 0)"}},{{opacity:1,y:0,clipPath:"inset(0 0 0% 0)",duration:.32,ease:"power3.out"}},{s});')
        js.append(f'tl.set("#g{g}",{{opacity:1}},{s});')
        if small: ovs(s)
    for b, (bt, txt) in enumerate(bigs):
        bt = T(bt)
        if bt > 0.01:
            js.append(f'tl.fromTo("#g{g}b{b}",{{opacity:0,scale:1.6,filter:"blur(14px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:.34,ease:"expo.out"}},{bt});')
            js.append(f'tl.fromTo("#cam",{{scale:1}},{{scale:1.05,duration:.13,ease:"expo.out",yoyo:true,repeat:1,immediateRender:false}},{bt});')
            ovs(bt)
    if g == len(GROUPS) - 1:
        for x, (xs, xe, xt) in enumerate(EXTRA):
            js.append(f'tl.fromTo("#x{x}",{{opacity:0,y:20}},{{opacity:1,y:0,duration:.3,ease:"back.out(2)"}},{T(xs)});'); ovs(T(xs))
    if e < DUR - 0.05:
        js.append(f'tl.to("#g{g}",{{opacity:0,y:-14,duration:.18,ease:"power2.in"}},{round(e-.18,3)});')
    if s > 0.01:
        js.insert(0, f'tl.set("#g{g}",{{opacity:0}},0);')

for l, (s, e, rows) in enumerate(LISTS):
    s, e = T(s), T(e)
    body.append(f'<div class="list" id="l{l}">')
    for r, (rt, num, ic, txt, _) in enumerate(rows):
        body.append(f'<div class="row" id="l{l}r{r}"><i class="bar"></i><span class="n">{num}</span>'
                    f'<svg viewBox="0 0 24 24" class="ic">{ICON[ic]}</svg><span class="tx">{rich(txt)}</span></div>')
    body.append('</div>')
    js.insert(0, f'tl.set("#l{l} .row",{{opacity:0}},0);')
    for r, (rt, num, ic, txt, pulses) in enumerate(rows):
        t = T(rt) - .05
        js.append(f'tl.fromTo("#l{l}r{r}",{{opacity:0,x:-70,filter:"blur(8px)"}},{{opacity:1,x:0,filter:"blur(0px)",duration:.32,ease:"back.out(1.7)"}},{t});')
        # aktif: bar kuning + perkataan kuning; baris sebelum jadi biasa (putih)
        js.append(f'tl.fromTo("#l{l}r{r} .bar",{{scaleY:0}},{{scaleY:1,duration:.22,ease:"power2.out"}},{t+.1});')
        js.append(f'tl.fromTo("#l{l}r{r} .hi",{{color:"#ffffff"}},{{color:"{ACC}",duration:.2}},{t+.1});')
        if r:
            js.append(f'tl.to("#l{l}r{r-1} .bar",{{scaleY:0,duration:.18}},{t+.1});')
            js.append(f'tl.to("#l{l}r{r-1} .hi",{{color:"#ffffff",duration:.2}},{t+.1});')
            js.append(f'tl.to("#l{l}r{r-1}",{{opacity:.78,duration:.2}},{t+.1});')
        for p in pulses:
            js.append(f'tl.fromTo("#l{l}r{r}",{{scale:1}},{{scale:1.05,duration:.14,ease:"power2.out",yoyo:true,repeat:1,immediateRender:false}},{T(p)});')
        ovs(t)
    js.append(f'tl.to("#l{l}",{{opacity:0,y:20,duration:.2,ease:"power2.in"}},{round(e-.2,3)});')
    js.append(f'tl.fromTo("#bscrim",{{opacity:0}},{{opacity:1,duration:.3,immediateRender:false}},{s});')
    js.append(f'tl.to("#bscrim",{{opacity:0,duration:.3}},{round(e-.25,3)});')

for c in CUTS:
    sfx.append([T(c), "tr"])
js.append(f'tl.fromTo("#bg",{{scale:1.0}},{{scale:1.04,duration:{DUR},ease:"none"}},0);')

FONT = "".join(f"@font-face{{font-family:'{f}';src:url(assets/fonts/{fn}) format('woff2');font-weight:{w};}}"
               for f, fn, w in [("Anton", "anton-latin-400-normal.woff2", 400), ("Montserrat", "montserrat-latin-700-normal.woff2", 700),
                                ("Montserrat", "montserrat-latin-800-normal.woff2", 800), ("Montserrat", "montserrat-latin-900-normal.woff2", 900)])
TS = "text-shadow:0 3px 14px rgba(0,0,0,.85),0 0 3px rgba(0,0,0,.8),0 1px 1px rgba(0,0,0,.6),0 0 22px rgba(0,0,0,.55);"
doc = f"""<!doctype html>
<html lang="ms">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
{FONT}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:#0d0c0b; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; font-family:'Montserrat',sans-serif; color:#fff; }}
#cam {{ position:absolute; inset:0; transform-origin:50% 45%; }}
#bg {{ position:absolute; inset:0; }}
#bg video {{ position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover; }}
#tscrim {{ position:absolute; left:0; top:0; width:1080px; height:820px; z-index:5; pointer-events:none;
  background:linear-gradient(180deg,rgba(8,8,10,.74) 0%,rgba(8,8,10,.6) 430px,rgba(8,8,10,0) 820px); }}
#bscrim {{ position:absolute; left:0; top:960px; width:1080px; height:960px; z-index:5; pointer-events:none; opacity:0;
  background:linear-gradient(0deg,rgba(8,8,10,.55) 0%,rgba(8,8,10,.45) 420px,rgba(8,8,10,0) 960px); }}
#vig {{ position:absolute; inset:0; z-index:4; pointer-events:none; background:radial-gradient(ellipse 80% 70% at 50% 50%,rgba(0,0,0,0) 60%,rgba(0,0,0,.28) 100%); }}
.grp {{ position:absolute; left:0; top:{CAP_TOP}px; width:1080px; text-align:center; z-index:10; }}
.sm {{ font-weight:800; font-size:27px; letter-spacing:.02em; line-height:1.2; {TS} }}
.sm2 {{ margin-top:10px; font-size:26px; }}
.big {{ font-family:'Anton',sans-serif; line-height:1.0; margin-top:6px; letter-spacing:.01em; white-space:nowrap;
  text-shadow:0 6px 26px rgba(0,0,0,.55),0 2px 4px rgba(0,0,0,.4); }}
.hi {{ color:{ACC}; font-weight:inherit; }}
.list {{ position:absolute; left:280px; top:{LIST_TOP}px; width:520px; z-index:10; display:flex; flex-direction:column; gap:7px; }}
.row {{ position:relative; display:flex; align-items:center; gap:10px; height:46px; padding:0 16px 0 16px; border-radius:8px; overflow:hidden;
  background:rgba(14,14,17,.74); backdrop-filter:blur(12px); -webkit-backdrop-filter:blur(12px);
  border:1px solid rgba(255,255,255,.10); box-shadow:0 8px 24px rgba(0,0,0,.30); }}
.row .bar {{ position:absolute; left:0; top:0; width:5px; height:100%; background:{ACC}; transform-origin:50% 50%; transform:scaleY(0); }}
.row .n {{ font-weight:700; font-size:13px; color:rgba(255,255,255,.5); width:18px; }}
.row .ic {{ width:21px; height:21px; flex:none; fill:none; stroke:#fff; stroke-width:1.9; stroke-linecap:round; stroke-linejoin:round; }}
.row .tx {{ font-weight:800; font-size:20px; letter-spacing:.01em; white-space:nowrap; {TS} }}
.row .hi {{ color:#fff; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
<div id="cam">
<div id="bg"><video id="v" src="assets/aroll.mp4" data-start="0" data-duration="{DUR}" data-track-index="2" class="clip" muted playsinline></video></div>
<div id="vig"></div>
</div>
<div id="tscrim"></div><div id="bscrim"></div>
<audio id="vo" src="assets/vo.wav" data-start="0" data-duration="{DUR}" data-track-index="1" data-has-audio="true"></audio>
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
open(f"{PROJ}/index.html", "w").write(doc)
json.dump(sorted(sfx), open(f"{PROJ}/sfx.json", "w"))
print("ok", len(sfx), "sfx")
