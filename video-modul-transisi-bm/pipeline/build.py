#!/usr/bin/env python3
"""Modul Transisi - Bahasa Melayu (KV/KVK), talking head + buku di tangan. Gaya Reel (ikut Kuasai Algebra Dua):
- caption kecil HURUF BESAR Montserrat 800 putih + kuning, tanpa kotak; tajuk Anton di bawahnya (zoom-blur + punch kamera)
- senarai: baris kaca gelap kecil, baris aktif = bar kuning + perkataan kuning
- SEMUA teks di band gelap atas kepala (y 160-370) - tak tutup muka / buku. Warna footage asal (tiada filter).
Masa = saat pada assets/aroll.mp4 (dah 1.1x).  Guna: python3 pipeline/build.py -> index.html + sfx.json"""
import html, json, os, re
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(HERE)
DUR = json.load(open(f"{HERE}/edl.json"))["dur"]; ACC = "#FFC21A"
rich = lambda s: re.sub(r"\*(.+?)\*", r'<b class="hi">\1</b>', html.escape(s))

# (mula, tamat, caption kecil, [(masa, tajuk)], saiz tajuk px, [(masa, baris kecil kedua)])
GROUPS = [
    (0.00, 2.33, "PARENTS, ANAK BAKAL MASUK", [(0.00, "*TAHUN 1*?")], 92, []),
    (2.33, 6.86, "BUKU KEMAHIRAN ASAS", [(4.62, "MEMBACA"), (5.42, "MENULIS"), (6.32, "MENGIRA")], 88, []),
    (6.86, 11.58, "MODUL TRANSISI TAHUN 1", [(9.46, "EDISI *2027*")], 92, []),
    (11.58, 18.39, "DALAM MODUL NI ADA", [], 0, []),
    (18.39, 24.27, "LATIHAN UNTUK BANTU ANAK", [(20.52, "BIASAKAN DIRI")], 84, [(22.64, "SEBELUM MELANGKAH KE *TAHUN 1*")]),
    (24.27, 26.85, "BAHAGIAN", [(25.94, "BAHASA *MELAYU*")], 84, []),
    (26.85, 34.60, "CONTOH LATIHAN", [(28.82, "SUKU KATA *KV*")], 84, [(32.10, "*K* = KONSONAN  ·  *V* = VOKAL")]),
    (34.60, 39.20, "ANAK AKAN BELAJAR", [(35.60, "KENAL *BUNYI* HURUF")], 76, [(36.74, "GABUNG BUNYI JADI *SUKU KATA*")]),
    (39.20, 48.10, "APA MAKSUD SUKU KATA", [(42.00, "*KVK*?")], 88, []),
    (48.10, 51.95, "CONTOHNYA", [], 0, []),
    (51.95, 59.70, "CONTOH SOALAN", [], 0, []),
    (59.70, DUR, "IBU AYAH NAK DAPATKAN", [(61.04, "MODUL *TRANSISI*")], 88, [(63.60, "BOLEH AMBIL *SET* NI!")]),
]
# senarai: (mula, tamat, susun, [(masa, label kecil, teks)])  susun: grid2 (2x2) | line (sebaris)
LISTS = [
    (12.72, 18.39, "grid2", [(12.72, "01", "*SAINS* AWAL"), (13.86, "02", "*MATEMATIK* AWAL"),
                             (16.04, "03", "*ENGLISH*"), (17.30, "04", "BAHASA *MELAYU*")]),
    (42.96, 48.10, "line", [(42.96, "K", "*KONSONAN*"), (44.02, "V", "*VOKAL*"), (45.96, "K", "*KONSONAN*")]),
    (54.44, 59.70, "line", [(54.44, "01", "*KENAL* HURUF"), (55.30, "02", "*SEBUT* BUNYI"), (55.96, "03", "*GABUNG* & BACA")]),
]
# contoh BAS: huruf muncul ikut sebutan; label K/V di bawah (B=konsonan, A=vokal, S=konsonan -> KVK)
BAS = (48.10, 51.95, 50.18, [(50.44, "B", "K"), (51.08, "A", "V"), (51.42, "S", "K")])
# potongan / tukar shot (bunyi whoosh / selak) - sempadan segmen yang visual berubah
CUTS = [2.33, 6.86, 11.58, 13.70, 15.30, 17.05, 18.39, 24.27, 26.85, 34.60, 39.20, 51.95, 59.70]

CAP_TOP = 168
body, js, sfx = [], [], []
ovs = lambda t: sfx.append([round(t, 3), "ov"])
punch = lambda t, k=1.05: js.append(f'tl.fromTo("#cam",{{scale:1}},{{scale:{k},duration:.13,ease:"expo.out",yoyo:true,repeat:1,immediateRender:false}},{t});')

for g, (s, e, small, bigs, fs, sm2) in enumerate(GROUPS):
    body.append(f'<div class="grp" id="g{g}"><div class="sm" id="g{g}s">{rich(small)}</div>')
    body.append('<div class="bigs">' + "".join(f'<div class="big" id="g{g}b{b}" style="font-size:{fs}px">{rich(t)}</div>' for b, (_, t) in enumerate(bigs)) + '</div>')
    for x, (_, t) in enumerate(sm2):
        body.append(f'<div class="sm sm2" id="g{g}x{x}">{rich(t)}</div>')
    body.append('</div>')
    if s < 0.01:   # hook: penuh dari frame 0 (thumbnail)
        js.append(f'tl.fromTo("#g{g}b0",{{scale:1}},{{scale:1.08,duration:.22,ease:"power2.out",yoyo:true,repeat:1}},0.35);')
    else:
        js.insert(0, f'tl.set("#g{g}",{{opacity:0}},0);')
        js.append(f'tl.set("#g{g}",{{opacity:1}},{s});')
        js.append(f'tl.fromTo("#g{g}s",{{opacity:0,y:26,clipPath:"inset(0 0 100% 0)"}},{{opacity:1,y:0,clipPath:"inset(0 0 0% 0)",duration:.32,ease:"power3.out"}},{s});')
        ovs(s)
    for b, (bt, _) in enumerate(bigs):
        if b: js.append(f'tl.to("#g{g}b{b-1}",{{opacity:0,scale:.85,filter:"blur(8px)",duration:.12}},{bt});')
        if bt > 0.01:
            js.insert(0, f'tl.set("#g{g}b{b}",{{opacity:0}},0);')
            js.append(f'tl.fromTo("#g{g}b{b}",{{opacity:0,scale:1.6,filter:"blur(14px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:.34,ease:"expo.out"}},{bt});')
            punch(bt); ovs(bt)
    for x, (xt, _) in enumerate(sm2):
        js.insert(0, f'tl.set("#g{g}x{x}",{{opacity:0}},0);')
        js.append(f'tl.fromTo("#g{g}x{x}",{{opacity:0,y:18}},{{opacity:1,y:0,duration:.3,ease:"back.out(2)"}},{xt});'); ovs(xt)
    if e < DUR - 0.05:
        js.append(f'tl.to("#g{g}",{{opacity:0,y:-14,duration:.18,ease:"power2.in"}},{round(e - .18, 3)});')

for l, (s, e, lay, rows) in enumerate(LISTS):
    body.append(f'<div class="list {lay}" id="l{l}">')
    for r, (rt, num, txt) in enumerate(rows):
        body.append(f'<div class="row" id="l{l}r{r}"><i class="bar"></i><span class="n">{html.escape(num)}</span><span class="tx">{rich(txt)}</span></div>')
    body.append('</div>')
    js.insert(0, f'tl.set("#l{l} .row",{{opacity:0}},0);')
    for r, (rt, num, txt) in enumerate(rows):
        t = round(rt - .05, 3)
        js.append(f'tl.fromTo("#l{l}r{r}",{{opacity:0,y:-24,filter:"blur(8px)"}},{{opacity:1,y:0,filter:"blur(0px)",duration:.32,ease:"back.out(1.7)"}},{t});')
        js.append(f'tl.fromTo("#l{l}r{r} .bar",{{scaleY:0}},{{scaleY:1,duration:.22,ease:"power2.out"}},{t + .1});')
        js.append(f'tl.fromTo("#l{l}r{r} .hi",{{color:"#ffffff"}},{{color:"{ACC}",duration:.2}},{t + .1});')
        if r:
            js.append(f'tl.to("#l{l}r{r-1} .bar",{{scaleY:0,duration:.18}},{t + .1});')
            js.append(f'tl.to("#l{l}r{r-1} .hi",{{color:"#ffffff",duration:.2}},{t + .1});')
            js.append(f'tl.to("#l{l}r{r-1}",{{opacity:.8,duration:.2}},{t + .1});')
        ovs(t)
    js.append(f'tl.to("#l{l}",{{opacity:0,y:-14,duration:.18,ease:"power2.in"}},{round(e - .18, 3)});')

# senarai KVK ambil tempat tajuk 'KVK?' (elak tindih)
js.append('tl.to("#g8b0",{opacity:0,scale:.8,filter:"blur(8px)",duration:.14},42.8);')
s, e, bt, lets = BAS
body.append('<div class="bas" id="bas"><div class="word" id="basw">BAS</div><div class="lets">' +
            "".join(f'<div class="let" id="bl{i}"><span class="L">{c}</span><span class="t">{k}</span></div>' for i, (_, c, k) in enumerate(lets)) + '</div></div>')
js.insert(0, 'tl.set("#bas",{opacity:0},0);tl.set("#bas .let",{opacity:0},0);')
js.append(f'tl.set("#bas",{{opacity:1}},{bt});')
js.append(f'tl.fromTo("#basw",{{opacity:0,scale:1.6,filter:"blur(14px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:.2,ease:"expo.out"}},{bt});'); punch(bt); ovs(bt)
js.append(f'tl.set("#basw",{{opacity:0}},{round(lets[0][0] - .03, 3)});')
for i, (t, c, k) in enumerate(lets):
    js.append(f'tl.fromTo("#bl{i}",{{opacity:0,y:30,scale:.6}},{{opacity:1,y:0,scale:1,duration:.3,ease:"back.out(2.2)"}},{t});'); ovs(t)
js.append(f'tl.to("#bas",{{opacity:0,y:-14,duration:.18,ease:"power2.in"}},{round(e - .18, 3)});')

for c in CUTS:
    sfx.append([c, "tr"])
js.append(f'tl.fromTo("#bg",{{scale:1.0}},{{scale:1.03,duration:{DUR},ease:"none"}},0);')

FONT = "".join(f"@font-face{{font-family:'{f}';src:url(assets/fonts/{fn}) format('woff2');font-weight:{w};}}"
               for f, fn, w in [("Anton", "anton-latin-400-normal.woff2", 400), ("Montserrat", "montserrat-latin-700-normal.woff2", 700),
                                ("Montserrat", "montserrat-latin-800-normal.woff2", 800), ("Montserrat", "montserrat-latin-900-normal.woff2", 900)])
TS = "text-shadow:0 2px 6px rgba(0,0,0,.9),0 0 3px rgba(0,0,0,.9),0 0 14px rgba(0,0,0,.75),0 0 28px rgba(0,0,0,.55);"
TSB = "text-shadow:0 2px 6px rgba(0,0,0,.85),0 0 16px rgba(0,0,0,.7),0 6px 30px rgba(0,0,0,.6);"
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
.grp {{ position:absolute; left:0; top:{CAP_TOP}px; width:1080px; text-align:center; z-index:10; }}
.sm {{ font-weight:800; font-size:27px; letter-spacing:.02em; line-height:1.2; {TS} }}
.sm2 {{ margin-top:10px; font-size:25px; }}
.bigs {{ position:relative; display:grid; }}
.big {{ grid-area:1/1; font-family:'Anton',sans-serif; line-height:1.0; margin-top:6px; letter-spacing:.01em; white-space:nowrap; {TSB} }}
.hi {{ color:{ACC}; font-weight:inherit; }}
.list {{ position:absolute; z-index:10; display:grid; gap:8px; }}
.list.grid2 {{ left:150px; top:{CAP_TOP + 50}px; width:780px; grid-template-columns:1fr 1fr; }}
.list.line {{ left:60px; top:{CAP_TOP + 50}px; width:960px; grid-template-columns:1fr 1fr 1fr; }}
.row {{ position:relative; display:flex; align-items:center; justify-content:center; gap:10px; height:46px; padding:0 14px; border-radius:8px; overflow:hidden;
  background:rgba(14,14,17,.74); backdrop-filter:blur(12px); -webkit-backdrop-filter:blur(12px);
  border:1px solid rgba(255,255,255,.10); box-shadow:0 8px 24px rgba(0,0,0,.30); }}
.row .bar {{ position:absolute; left:0; top:0; width:5px; height:100%; background:{ACC}; transform-origin:50% 50%; transform:scaleY(0); }}
.row .n {{ font-weight:700; font-size:13px; color:rgba(255,255,255,.55); }}
.list.line .n {{ font-family:'Anton',sans-serif; font-weight:400; font-size:24px; color:#fff; }}
.row .tx {{ font-weight:800; font-size:20px; letter-spacing:.01em; white-space:nowrap; {TS} }}
.row .hi {{ color:#fff; }}
.bas {{ position:absolute; left:0; top:{CAP_TOP + 40}px; width:1080px; text-align:center; z-index:10; }}
.bas .word {{ position:absolute; left:0; right:0; top:0; font-family:'Anton',sans-serif; font-size:96px; line-height:1; {TSB} }}
.bas .lets {{ display:flex; justify-content:center; gap:46px; }}
.bas .let {{ display:flex; flex-direction:column; align-items:center; }}
.bas .L {{ font-family:'Anton',sans-serif; font-size:90px; line-height:1; {TSB} }}
.bas .t {{ margin-top:4px; font-weight:800; font-size:24px; color:{ACC}; {TS} }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
<div id="cam">
<div id="bg"><video id="v" src="assets/aroll.mp4" data-start="0" data-duration="{DUR}" data-track-index="2" class="clip" muted playsinline></video></div>
</div>
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
print("ok", len(sfx), "sfx", DUR)
