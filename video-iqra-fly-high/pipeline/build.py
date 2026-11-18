#!/usr/bin/env python3
"""IQRA' Fly High - footage dah diedit pengguna (CapCut, 50.8 s, tanpa VO) + overlay USP + SFX lembut.

- Footage: HLG -> SDR terus (peraturan #20: tiada filter warna/cahaya/sharpen). Masa & potongan asal dikekalkan.
- Overlay USP: font Chewy (padan screenshot 'Vlogger.' CapCut), putih + outline coklat gelap + bayang,
  perkataan penting kuning mustard, saiz sederhana ('50%'), satu USP pada satu masa, di ruang kosong (meja/tepi).
- Gerak (ikut contoh TikTok): perkataan masuk blur-in berperingkat, terapung perlahan, keluar blur-out;
  bintang kecil berkelip pada perkataan kuning (soft highlight).
- Kamera: zoom perlahan setiap shot + blur lembut 0.25 s pada setiap potongan (smooth transition).
- SFX (folder Drive pengguna): whoosh/swoosh pada potongan, pop setiap USP, sparkle pada tajuk,
  selak kertas lembut (sintetik) pada setiap page flip. Audio telefon (audio bonus) dikekalkan.

Guna: python3 pipeline/build.py   -> index.html + sfx.json
"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(HERE)
DUR = 50.7667
CUTS = [3.4667, 6.5, 10.2, 16.1333, 23.4, 25.8667, 28.3667, 34.1, 36.5667, 43.6667]
FLIPS = [19.05, 20.6, 21.2, 22.25, 34.95, 35.6, 36.3, 45.3, 46.1, 47.3, 49.05, 50.0]   # puncak gerakan selak halaman

# (id, mula, tamat, [baris], top_y, align, saiz_px)  -- **kata** = kuning
USPS = [
    ("hook", 0.0, 3.30, ["IQRA' **Fly High**", "Kenal • Dengar • Faham"], 200, "c", 92),
    ("u1", 3.62, 6.38, ["Warna **Menarik,**", "Anak Lebih **Fokus**"], 190, "c", 60),
    ("u2", 7.00, 10.05, ["Kenal Huruf", "Melalui **Gambar**"], 190, "c", 60),
    ("u3", 10.40, 13.05, ["**Bonus Audio**", "Disediakan"], 1415, "l", 60),
    ("u4", 13.25, 15.98, ["Baca Sambil", "**Dengar Audio**"], 1415, "l", 60),
    ("u5", 16.35, 18.90, ["Ilustrasi **Comel**", "& **Berwarna**"], 190, "c", 60),
    ("u6", 19.20, 22.15, ["Contoh Perkataan", "**Bahasa Arab**"], 190, "c", 60),
    ("u7", 23.55, 25.75, ["Panduan", "**Makhraj Huruf**"], 180, "c", 60),
    ("u8", 26.00, 28.25, ["Huruf Hijaiyah", "**Besar & Jelas**"], 190, "c", 60),
    # 36.6-43.7 cover dipegang: TIADA overlay (cover dah ada tajuk; produk jadi fokus)
    ("u9", 44.30, DUR, ["Konsep **Kenal,**", "**Dengar** & **Faham**"], 175, "l", 58),
]

def words(line):
    out, hi = [], False
    for part in line.split("**"):
        for w in part.split():
            out.append((w, hi))
        hi = not hi
    return out

def html():
    el, js = [], []
    S = lambda t: f"{t:.3f}"
    # kamera: zoom perlahan per shot + blur lembut di potongan
    bounds = [0.0] + CUTS + [DUR]
    for i in range(len(bounds) - 1):
        a, b = bounds[i], bounds[i + 1]
        s0, s1 = (1.0, 1.035) if i % 2 == 0 else (1.035, 1.0)
        js.append(f'tl.fromTo("#cam",{{scale:{s0}}},{{scale:{s1},duration:{S(b-a)},ease:"sine.inOut",immediateRender:{"true" if i==0 else "false"}}},{S(a)});')
    for c in CUTS:
        js.append(f'tl.fromTo("#v",{{filter:"blur(9px)"}},{{filter:"blur(0px)",duration:.26,ease:"power2.out",immediateRender:false}},{S(c)});')
    for uid, a, b, lines, y, al, px in USPS:
        style = f"top:{y}px;font-size:{px}px;" + ("left:60px;text-align:left;" if al == "l" else "left:0;width:1080px;text-align:center;")
        ln_html = []
        hi_ids = []
        n = 0
        for li, line in enumerate(lines):
            ws = words(line)
            small = uid in ("hook",) and li == 1
            cls = "ln sm" if small else "ln"
            parts = []
            for w, hi in ws:
                wid = f"{uid}w{n}"; n += 1
                parts.append(f'<span class="w{" hi" if hi else ""}" id="{wid}">{w}</span>')
                if hi: hi_ids.append(wid)
            ln_html.append(f'<div class="{cls}">{"".join(parts)}</div>')
        spark = f'<svg class="spk" id="{uid}s" viewBox="0 0 40 40"><path d="M20 0 C22 14 26 18 40 20 C26 22 22 26 20 40 C18 26 14 22 0 20 C14 18 18 14 20 0Z"/></svg>'
        el.append(f'<div class="u clip" id="{uid}" data-start="{S(a)}" data-duration="{S(b-a)}" data-track-index="{10+len(el)}" style="{style}">'
                  f'<div class="in" id="{uid}i">{"".join(ln_html)}{spark}</div></div>')
        sel = ",".join(f"#{uid}w{k}" for k in range(n))
        t_in = a if uid != "hook" else 0.0
        if uid == "hook":   # thumbnail: hook penuh dari frame 0, gerak 'breathing' sahaja
            js.append(f'tl.fromTo("#{uid}i",{{scale:1.0}},{{scale:1.03,duration:1.6,ease:"sine.inOut",yoyo:true,repeat:1}},0);')
        else:
            js.append(f'tl.fromTo("{sel}",{{opacity:0,y:28,scale:.55,filter:"blur(12px)"}},{{opacity:1,y:0,scale:1,filter:"blur(0px)",duration:.5,ease:"back.out(2)",stagger:.07}},{S(t_in)});')
            js.append(f'tl.fromTo("#{uid}",{{y:0}},{{y:-7,duration:{S((b-a)/2)},ease:"sine.inOut",yoyo:true,repeat:1}},{S(a)});')
        t_hi = t_in + 0.08 * n + 0.45 if uid != "hook" else 0.5
        if hi_ids:
            hs = ",".join("#" + h for h in hi_ids)
            js.append(f'tl.to("{hs}",{{scale:1.06,duration:.18,ease:"power2.out",yoyo:true,repeat:1}},{S(t_hi)});')
        js.append(f'tl.fromTo("#{uid}s",{{scale:0,rotation:-60,opacity:0}},{{scale:1,rotation:0,opacity:1,duration:.4,ease:"back.out(3)",immediateRender:{"false" if uid=="hook" else "true"}}},{S(t_hi if uid!="hook" else 0)});')
        js.append(f'tl.to("#{uid}s",{{scale:.55,rotation:45,duration:.5,ease:"sine.inOut",yoyo:true,repeat:{max(1, int((b-a-1.0)/0.5) // 2 * 2 - 1)}}},{S(t_hi+0.45)});')
        if b < DUR - 0.05:
            js.append(f'tl.to("#{uid}i",{{opacity:0,y:-18,filter:"blur(10px)",duration:.3,ease:"power2.in"}},{S(b-0.3)});')
    return el, js

def build():
    el, js = html()
    doc = f"""<!doctype html>
<html lang="ms">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>
@font-face {{ font-family:'Chewy'; src:url('assets/fonts/Chewy.ttf') format('truetype'); font-display:block; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; font-family:'Chewy',cursive; }}
#cam {{ position:absolute; inset:0; transform-origin:50% 50%; }}
#v {{ position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover; }}
.u {{ position:absolute; z-index:50; color:#fff; pointer-events:none; }}
.in {{ position:relative; display:inline-block; }}
.ln {{ white-space:nowrap; line-height:1.04; letter-spacing:.01em; }}
.ln.sm {{ font-size:.5em; margin-top:10px; letter-spacing:.04em; }}
.w {{ display:inline-block; margin:0 .15em; -webkit-text-stroke:.11em #3a2414; paint-order:stroke fill;
     text-shadow:0 .06em 0 #3a2414, 0 .1em .22em rgba(0,0,0,.38); }}
.w.hi {{ color:#FFC21A; }}
.spk {{ position:absolute; width:.5em; height:.5em; right:-.42em; top:-.28em; fill:#FFC21A;
       filter:drop-shadow(0 2px 3px rgba(58,36,20,.6)); }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
<div id="cam"><video id="v" class="clip" src="assets/footage.mp4" data-start="0" data-duration="{DUR}" data-media-start="0" data-track-index="1" muted playsinline></video></div>
{chr(10).join(el)}
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
    # SFX: (masa, nama_fail | 'paper:i' | 'whoosh:i', gain)
    ev = []
    tr = ["whoosh1", "swoosh2", "syn_whoosh"]
    for i, c in enumerate(CUTS):
        ev.append((round(c - 0.12, 3), tr[i % 3], 0.16))
    pops = ["pop1", "pop3", "pop2", "pop4", "pop0"]
    k = 0
    for uid, a, b, *_ in USPS:
        if uid == "hook":
            ev.append((0.05, "sparkle", 0.16))
        elif uid == "end":
            ev.append((a, "shimmer", 0.18)); ev.append((a + 0.5, "sparkle", 0.12))
        else:
            ev.append((a + 0.02, pops[k % len(pops)], 0.26)); k += 1
    for i, f in enumerate(FLIPS):
        ev.append((round(f - 0.10, 3), f"paper{i % 3}", 0.10))
    json.dump(sorted(ev), open(f"{PROJ}/sfx.json", "w"), indent=0)
    print("ok", len(USPS), "overlay,", len(ev), "sfx")

if __name__ == "__main__":
    build()
