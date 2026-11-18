#!/usr/bin/env python3
"""IQRA' Fly High - video v2 & v3 dari footage yang sama (QR di-blur: assets/footage_qr.mp4).

Permintaan pengguna (lepas v1):
- semua QR/barcode di-blur (pipeline/qrblur.py)
- susunan shot ditukar, ayat USP ditukar, gaya tulisan ditukar -> v1, v2, v3 semua berbeza
- tulisan PUTIH tapi menarik, jangan tutup buku
- setiap scene bertukar: LABEL nama bahagian buku + animasi + effect peralihan

v2 'Gaya Hijau': teks putih outline hijau tua (warna buku), perkataan kuning, masuk melantun perkataan demi perkataan;
    label pil hijau + kilauan; peralihan zoom-blur / flash / spin / whip-up.
v3 'Gaya Marker': teks putih outline ungu gelap, perkataan penting atas sapuan marker koral; baris naik dari bawah (reveal);
    label pil koral jatuh + bintang; peralihan whip / light-leak / zoom-out / iris.
Guna: python3 pipeline/build2.py [v2 v3]  -> videos/<id>/index.html + plan.json (audio/SFX untuk mux2.py)
"""
import json, os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(HERE)
FPS = 30
fr = lambda t: round(round(t * FPS) / FPS, 4)
PHONE = (10.2, 16.1333)                      # julat footage yang ada audio (audio bonus telefon)
FLIPS = [19.05, 20.6, 21.2, 22.25, 34.95, 35.6, 36.3, 46.1, 47.3, 49.05, 50.0]
TOP, BOT = 238, 1418                         # y USP: band atas (atas buku) / bawah kiri (shot telefon)

# clip: (src_mula, src_tamat, label, [(lines, y, align)], label_y)   lines '**x**' = highlight
AUD = 1460                                   # USP shot telefon: ruang antara bawah buku & telefon (kiri bawah)
VIDEOS = {
 "v2": dict(style="hijau", trans=["zoomblur", "flash", "spin", "whipup"], clips=[
    (25.90, 28.33, "HURUF HIJAIYAH", [(["Anak Baru Nak", "**Kenal Huruf?**"], TOP, "c")], 162),
    (3.50, 6.45, "COVER DEPAN", [(["Warna **Menarik,**", "Anak Lebih **Fokus**"], TOP, "c")], 162),
    (0.05, 3.43, "HURUF BERBARIS", [(["Huruf **Besar,**", "Senang **Dibaca**"], TOP, "c")], 162),
    (7.40, 10.17, "KENAL HURUF", [(["Setiap Huruf", "Ada **Gambar**"], TOP, "c")], 162),
    (10.20, 16.13, "AUDIO BONUS", [(["Siap Ada", "**Audio Bonus**"], AUD, "l", 46), (["Dengar Sambil", "**Baca**"], AUD, "l", 46)], 1408),
    (16.20, 18.98, "ILUSTRASI", [(["Gambar **Comel,**", "Penuh **Warna**"], TOP, "c")], 162),
    (23.45, 25.85, "MAKHRAJ HURUF", [(["Belajar **Tempat**", "**Keluar Huruf**"], TOP, "c")], 152),
    (28.45, 31.60, "KANDUNGAN", [(["Dari **Makhraj**", "Sampai **Tanwin**"], TOP, "c")], 162),
    (45.60, 50.70, "ISI BUKU", [(["Kenal, Dengar", "& **Faham!**"], TOP, "l")], 162),
 ]),
 "v3": dict(style="marker", trans=["whip", "leak", "zoomout", "iris"], clips=[
    (16.75, 18.98, "IQRA' FLY HIGH", [(["Kenal Huruf Hijaiyah", "Cara **Seronok!**"], TOP, "c")], 162),
    (25.90, 28.33, "HURUF HIJAIYAH", [(["Huruf **Jelas,**", "Mudah **Dicam**"], TOP, "c")], 162),
    (19.00, 22.28, "CONTOH PERKATAAN", [(["Setiap Huruf Ada", "**Perkataan Arab**"], TOP, "c")], 162),
    (23.45, 25.85, "MAKHRAJ HURUF", [(["Siap Ada", "**Panduan Makhraj**"], TOP, "c")], 152),
    (10.20, 16.13, "AUDIO BONUS", [(["**Bonus Audio**", "Untuk Anak"], AUD, "l", 46), (["Baca Sambil", "**Dengar**"], AUD, "l", 46)], 1408),
    (7.30, 10.17, "KENAL HURUF", [(["Belajar Huruf", "Dengan **Gambar**"], TOP, "c")], 162),
    (0.05, 3.43, "HURUF BERBARIS", [(["Baris **Atas,** **Bawah**", "& **Depan**"], TOP, "c")], 162),
    (3.50, 6.45, "COVER DEPAN", [(["Konsep **Kenal,**", "**Dengar & Faham**"], TOP, "c")], 162),
 ]),
}

STYLE = {
 "hijau": dict(stroke="#1d4a36", hi="#FFD23F", pill="linear-gradient(135deg,#3a9a6c,#23704d)", pilltx="#fff"),
 "marker": dict(stroke="#3a1d38", hi="#FFFFFF", pill="linear-gradient(135deg,#ff7a8f,#f2557a)", pilltx="#fff"),
}

def words(line):
    out, hi = [], False
    for part in line.split("**"):
        for w in part.split(): out.append((w, hi))
        hi = not hi
    return out

def build(vid):
    V = VIDEOS[vid]; st = V["style"]; C = STYLE[st]
    D = f"{PROJ}/videos/{vid}"; os.makedirs(D, exist_ok=True)
    for f in ("hyperframes.json", "package.json"): shutil.copy(f"{PROJ}/{f}", D)
    json.dump({"name": f"iqra-{vid}"}, open(f"{D}/meta.json", "w"))
    if not os.path.exists(f"{D}/assets"): os.symlink("../../assets", f"{D}/assets")
    el, js, ev, phone = [], [], [], []
    S = lambda t: f"{t:.3f}"
    t = 0.0; starts = []
    for i, c in enumerate(V["clips"]):
        starts.append(fr(t)); t = fr(t + (c[1] - c[0]))
    DUR = t
    for i, (a, b, label, usps, ly) in enumerate(V["clips"]):
        T0 = starts[i]; d = b - a; T1 = T0 + d
        last = i == len(V["clips"]) - 1
        ext = 0 if last else 0.5     # klip lama kekal 0.5 s di bawah (peralihan tanpa skrin hitam)
        org = ["50% 45%", "40% 40%", "60% 50%", "50% 60%"][i % 4]
        el.append(f'<div class="bw" id="c{i}w" style="z-index:{2+i}"><div class="mv" id="c{i}m" style="transform-origin:{org}">'
                  f'<video id="c{i}" class="clip" src="assets/footage_qr.mp4" data-start="{S(T0)}" data-duration="{S(d+ext)}" '
                  f'data-media-start="{S(a)}" data-track-index="{2+i}" muted playsinline></video></div></div>')
        js.append(f'tl.set("#c{i}w",{{opacity:1}},{S(T0)});')
        if not last: js.append(f'tl.set("#c{i}w",{{opacity:0}},{S(T1+ext)});')
        k0, k1 = (1.0, 1.06) if i % 2 == 0 else (1.06, 1.0)
        js.append(f'tl.fromTo("#c{i}m",{{scale:{k0}}},{{scale:{k1},duration:{S(d+ext)},ease:"sine.inOut"}},{S(T0)});')
        # --- peralihan masuk ---
        if i > 0:
            tr = V["trans"][(i - 1) % len(V["trans"])]
            w = f"#c{i}w"
            if tr == "zoomblur":
                js.append(f'tl.fromTo("{w}",{{scale:1.35,filter:"blur(16px)",opacity:0}},{{scale:1,filter:"blur(0px)",opacity:1,duration:.38,ease:"expo.out"}},{S(T0)});')
            elif tr == "flash":
                js.append(f'tl.fromTo("#flash",{{opacity:0}},{{opacity:.9,duration:.08,yoyo:true,repeat:1,ease:"power1.out",immediateRender:false}},{S(T0-0.06)});')
                js.append(f'tl.fromTo("{w}",{{scale:1.12}},{{scale:1,duration:.4,ease:"power3.out"}},{S(T0)});')
            elif tr == "spin":
                js.append(f'tl.fromTo("{w}",{{rotation:-8,scale:1.4,filter:"blur(12px)",opacity:0}},{{rotation:0,scale:1,filter:"blur(0px)",opacity:1,duration:.42,ease:"back.out(1.4)"}},{S(T0)});')
            elif tr == "whipup":
                js.append(f'tl.fromTo("{w}",{{y:1920,filter:"blur(24px)"}},{{y:0,filter:"blur(0px)",duration:.34,ease:"power3.out"}},{S(T0)});')
            elif tr == "whip":
                js.append(f'tl.fromTo("{w}",{{x:1080,filter:"blur(26px)"}},{{x:0,filter:"blur(0px)",duration:.32,ease:"power3.out"}},{S(T0)});')
            elif tr == "leak":
                js.append(f'tl.fromTo("{w}",{{opacity:0,scale:1.08}},{{opacity:1,scale:1,duration:.45,ease:"sine.out"}},{S(T0)});')
                js.append(f'tl.fromTo("#leak",{{opacity:0,x:-500}},{{opacity:.85,x:0,duration:.25,ease:"sine.out",immediateRender:false}},{S(T0-0.1)});')
                js.append(f'tl.to("#leak",{{opacity:0,x:500,duration:.45,ease:"sine.in"}},{S(T0+0.15)});')
            elif tr == "zoomout":
                js.append(f'tl.fromTo("{w}",{{scale:.55,rotation:4,opacity:0,filter:"blur(8px)"}},{{scale:1,rotation:0,opacity:1,filter:"blur(0px)",duration:.45,ease:"back.out(1.6)"}},{S(T0)});')
            elif tr == "iris":
                js.append(f'tl.fromTo("{w}",{{clipPath:"circle(0% at 50% 50%)"}},{{clipPath:"circle(75% at 50% 50%)",duration:.45,ease:"power2.inOut"}},{S(T0)});')
            ev.append([round(T0 - 0.1, 3), ["whoosh1", "swoosh2", "syn_whoosh", "paper0"][(i - 1) % 4], 0.17])
        # --- label bahagian buku ---
        lid = f"lb{i}"
        lbl_html = (f'<div class="lab clip" id="{lid}" data-start="{S(T0)}" data-duration="{S(d)}" data-track-index="{40+i}" '
                    f'style="top:{ly}px;left:60px"><div class="pill" id="{lid}p"><span class="dot"></span>{label}<i class="shine" id="{lid}s"></i></div></div>')
        el.append(lbl_html)
        tl0 = 0 if i == 0 else T0 + 0.18
        if i > 0:
            if st == "hijau":
                js.append(f'tl.fromTo("#{lid}p",{{x:-420,opacity:0,skewX:-14}},{{x:0,opacity:1,skewX:0,duration:.45,ease:"back.out(1.8)"}},{S(tl0)});')
            else:
                js.append(f'tl.fromTo("#{lid}p",{{y:-160,opacity:0,rotation:-10}},{{y:0,opacity:1,rotation:0,duration:.55,ease:"bounce.out"}},{S(tl0)});')
            ev.append([round(tl0 + 0.05, 3), ["click1", "pop4"][i % 2], 0.17])
        js.append(f'tl.fromTo("#{lid}s",{{x:-120}},{{x:520,duration:.6,ease:"power2.inOut"}},{S(tl0+0.35)});')
        if not last: js.append(f'tl.to("#{lid}p",{{opacity:0,x:-30,duration:.22,ease:"power2.in"}},{S(T1-0.24)});')
        # --- USP ---
        n_u = len(usps)
        for j, u in enumerate(usps):
            lines, y, al = u[:3]; fs = u[3] if len(u) > 3 else 56
            ua = T0 + (0.0 if i == 0 else 0.42) + j * (d / n_u)
            ub = T0 + (j + 1) * (d / n_u) - (0.05 if last and j == n_u - 1 else 0.22)
            uid = f"u{i}_{j}"
            pos = ("left:60px;text-align:left;" if al == "l" else "left:0;width:1080px;text-align:center;")
            lh, ids, his = [], [], []
            n = 0
            for li, line in enumerate(lines):
                parts = []
                for wd, hi in words(line):
                    wid = f"{uid}w{n}"; n += 1; ids.append(wid)
                    if hi: his.append(wid)
                    inner = f'<span class="mk" id="{wid}m"{' style="transform:scaleX(1) skewX(-8deg)"' if i == 0 else ''}></span><span class="tx">{wd}</span>' if (st == "marker" and hi) else wd
                    parts.append(f'<span class="w{" hi" if hi else ""}" id="{wid}">{inner}</span>')
                lh.append(f'<div class="ln" id="{uid}l{li}"><div class="lni">{"".join(parts)}</div></div>')
            el.append(f'<div class="u clip" id="{uid}" data-start="{S(ua)}" data-duration="{S(ub-ua)}" data-track-index="{60+i*2+j}" '
                      f'style="top:{y}px;{pos}--fs:{fs}px"><div class="in" id="{uid}i">{"".join(lh)}</div></div>')
            if i == 0 and j == 0:
                js.append(f'tl.fromTo("#{uid}i",{{scale:1}},{{scale:1.03,duration:1.2,ease:"sine.inOut",yoyo:true,repeat:1}},0);')
                if st == "marker":
                    js.append(f'tl.set("{",".join("#"+h+"m" for h in his)}",{{scaleX:1}},0);')
            else:
                if st == "hijau":
                    js.append(f'tl.fromTo("{",".join("#"+x for x in ids)}",{{opacity:0,y:46,rotation:(k)=>[-8,6,-5,7,-6][k%5],scale:.6}},'
                              f'{{opacity:1,y:0,rotation:0,scale:1,duration:.5,ease:"back.out(3)",stagger:.07}},{S(ua)});')
                    if his: js.append(f'tl.to("{",".join("#"+h for h in his)}",{{scale:1.08,duration:.16,yoyo:true,repeat:1,ease:"power2.out"}},{S(ua+0.07*n+0.4)});')
                else:
                    for li in range(len(lines)):
                        js.append(f'tl.fromTo("#{uid}l{li} .lni",{{yPercent:110,opacity:0,filter:"blur(6px)"}},{{yPercent:0,opacity:1,filter:"blur(0px)",duration:.5,ease:"power3.out"}},{S(ua+li*0.14)});')
                    if his: js.append(f'tl.fromTo("{",".join("#"+h+"m" for h in his)}",{{scaleX:0}},{{scaleX:1,duration:.32,ease:"power2.out",stagger:.08}},{S(ua+0.3)});')
            js.append(f'tl.fromTo("#{uid}",{{y:0}},{{y:-6,duration:{S((ub-ua)/2)},ease:"sine.inOut",yoyo:true,repeat:1}},{S(ua)});')
            if not (last and j == n_u - 1):
                js.append(f'tl.to("#{uid}i",{{opacity:0,y:-14,filter:"blur(8px)",duration:.22,ease:"power2.in"}},{S(ub-0.22)});')
            if i > 0 or j > 0:
                ev.append([round(ua + 0.02, 3), ["pop1", "pop3", "pop2", "pop0"][(i + j) % 4], 0.24])
        # page flip -> selak kertas
        for f in FLIPS:
            if a + 0.15 < f < b - 0.1: ev.append([round(T0 + f - a - 0.1, 3), f"paper{len(ev) % 3}", 0.10])
        if a < PHONE[1] and b > PHONE[0]:
            s0 = max(a, PHONE[0]); phone.append([round(T0 + s0 - a, 3), s0, round(min(b, PHONE[1]) - s0, 3)])
    ev.append([0.05, "sparkle", 0.15]); ev.append([round(DUR - 2.2, 3), "shimmer", 0.15])
    hook_static = ""
    css = f"""
@font-face {{ font-family:'Chewy'; src:url('assets/fonts/Chewy.ttf') format('truetype'); font-display:block; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1920px; overflow:hidden; background:#000; }}
#root {{ position:relative; width:1080px; height:1920px; overflow:hidden; font-family:'Chewy',cursive; }}
.bw {{ position:absolute; inset:0; opacity:0; overflow:hidden; }}
.mv {{ position:absolute; inset:0; }}
.bw video {{ position:absolute; left:0; top:0; width:1080px; height:1920px; object-fit:cover; }}
#flash {{ position:absolute; inset:0; background:#fff; opacity:0; z-index:30; }}
#leak {{ position:absolute; left:-200px; top:-200px; width:1480px; height:2320px; opacity:0; z-index:30; mix-blend-mode:screen;
  background:radial-gradient(ellipse at 30% 40%, rgba(255,170,110,.85) 0%, rgba(255,120,150,.45) 30%, rgba(255,120,150,0) 60%); }}
.u {{ position:absolute; z-index:50; color:#fff; }}
.in {{ display:inline-block; }}
.ln {{ white-space:nowrap; line-height:1.02; overflow:visible; }}
.lni {{ display:inline-block; }}
.w {{ position:relative; display:inline-block; margin:0 .14em; font-size:var(--fs,56px); letter-spacing:.01em;
     -webkit-text-stroke:.12em {C['stroke']}; paint-order:stroke fill;
     text-shadow:0 .07em 0 {C['stroke']}, 0 .12em .25em rgba(0,0,0,.35); }}
.w.hi {{ color:{C['hi']}; }}
.mk {{ position:absolute; left:-.12em; right:-.12em; top:.06em; bottom:-.06em; border-radius:.2em; transform:scaleX(0) skewX(-8deg);
      transform-origin:0 50%; background:linear-gradient(90deg,#ff7a8f,#f2557a); box-shadow:0 .06em .16em rgba(58,29,56,.35); z-index:-1; }}
.tx {{ position:relative; }}
.lab {{ position:absolute; z-index:55; }}
.pill {{ position:relative; overflow:hidden; display:inline-flex; align-items:center; gap:12px; padding:9px 22px 10px 16px;
        border-radius:999px; background:{C['pill']}; color:{C['pilltx']}; font-size:30px; letter-spacing:.06em;
        box-shadow:0 6px 16px rgba(0,0,0,.28); text-shadow:0 2px 0 rgba(0,0,0,.18); border:2.5px solid rgba(255,255,255,.85); }}
.dot {{ width:16px; height:16px; border-radius:50%; background:#fff; box-shadow:0 0 0 4px rgba(255,255,255,.35); }}
.shine {{ position:absolute; top:-20px; left:0; width:60px; height:110px; transform:rotate(20deg);
         background:linear-gradient(90deg,rgba(255,255,255,0),rgba(255,255,255,.75),rgba(255,255,255,0)); }}
"""
    doc = f"""<!doctype html>
<html lang="ms">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>{css}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
{chr(10).join(e for e in el if e.startswith('<div class="bw"'))}
<div id="flash"></div><div id="leak"></div>
{chr(10).join(e for e in el if not e.startswith('<div class="bw"'))}
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
    open(f"{D}/index.html", "w").write(doc)
    json.dump({"dur": DUR, "phone": phone, "sfx": sorted(ev)}, open(f"{D}/plan.json", "w"), indent=0)
    print(vid, f"{DUR:.2f}s", len(V["clips"]), "klip,", len(ev), "sfx, phone", phone)

if __name__ == "__main__":
    for v in (sys.argv[1:] or list(VIDEOS)): build(v)
