#!/usr/bin/env python3
"""GAYA VARIAN (9 video hook) - Modul Transisi Tahun 1 Edisi 2027.
Pengguna: video pertama lulus (gaya frosted glass, lihat build.py). Untuk 9 varian:
overlay GAYA ASAL (kotak gelap + border kuning mustard, nombor kuning, perkataan penting
warna kuning - 'kuning sikit, terang sikit') tetapi LEBIH KECIL; bunyi 'toing' pada
SETIAP kotak/item (termasuk Membaca/Menulis/Mengira/Menaakul & 5 subjek); render HD.
Modul ini diimport oleh pipeline/variants.py (tidak menulis fail sendiri).
Masa elemen = saat MUTLAK pada assets/aroll.mp4 (video utama)."""
import json, html, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
W, H = 1080, 1920
ACC = "#FFC21A"
EDL = json.load(open(os.path.join(HERE, "edl.json")))
DUR = round(EDL["dur"], 3)

# ------------------------------------------------------------------ elemen
# hook(lines, sub)            kotak kaca besar sikit (frame 0 = thumbnail)
# cap(text)                   satu pil kaca kecil
# card(num, title, sub|items) kotak kaca: tajuk kecil + satu baris / pil item (setiap item pop)
# row(items)                  pil-pil kaca sebaris, setiap satu pop
EL = [
 dict(k="hook", s=0.0, e=4.40, lines=["ANAK DAH *6 TAHUN?*", "2027 MASUK *TAHUN 1!*"]),
 dict(k="cap", s=4.46, e=6.35, text="Anak dah *boleh...?*"),
 dict(k="cap", s=10.65, e=13.15, text="Menulis & *kira nombor?*"),
 dict(k="cap", s=13.24, e=16.35, text="Ingat anak dah *okay?*", sfx="swoosh"),
 dict(k="cap", s=18.80, e=21.28, text="Baru nampak yang *belum kuasai*"),
 dict(k="card", s=21.33, e=25.05, num="1", title="PERSIAPAN AWAL TAHUN 1", sub="Biasakan anak dengan aktiviti belajar"),
 dict(k="cap", s=25.09, e=27.20, text="Bukan paksa *berjam-jam*"),
 dict(k="cap", s=27.25, e=30.25, text="*10–15 minit* sehari pun cukup", sfx="swoosh", big=True),
 dict(k="cap", s=33.00, e=34.90, text="Modul Transisi *Tahun 1 • 2027*"),
 dict(k="card", s=37.42, e=44.20, num="3", title="5 SUBJEK, 1 BUKU", items=[
     ("Bahasa Melayu", 39.46), ("English", 40.60), ("Matematik", 41.24), ("Alam & Manusia", 42.08), ("Bahasa Arab", 43.60)]),
 dict(k="card", s=46.74, e=50.34, num="2", title="KEMAHIRAN 4M", items=[
     ("Membaca", 47.70), ("Menulis", 48.44), ("Mengira", 49.04), ("Menaakul", 49.76)]),
 dict(k="cap", s=50.39, e=52.72, text="Menaakul = *belajar berfikir*", sfx="swoosh"),
 dict(k="card", s=55.39, e=58.05, num="4", title="VIDEO TUTORIAL & JAWAPAN", sub="Senang bimbing anak di rumah"),
 dict(k="card", s=60.30, e=64.30, num="5", title="KENAL PASTI TAHAP ANAK", sub="Mana dah kuasai, mana perlu bantu"),
 dict(k="cap", s=64.36, e=66.00, text="Dah okay? *Teruskan!*"),
 dict(k="cap", s=68.39, e=72.00, text="Bukan nak pandai *dalam sehari*"),
 dict(k="row", s=72.03, e=77.28, items=[("Lebih biasa", 72.81), ("Lebih bersedia", 75.35), ("Lebih yakin", 76.31)]),
 dict(k="cap", s=77.33, e=79.14, text="*Ready* masuk Tahun 1!"),
 dict(k="cap", s=79.18, e=DUR, text="Jom buat *persediaan awal!*", sfx="swoosh", final=True),   # tiada teks bakul/beg kuning (pengguna tolak)
]

# b-roll: (fail, mula, tamat, media_start, kenburns (dari, ke), origin, tag)
# Semasa b-roll: caption lain disorok (buku bersih); hanya tag kaca kecil di tepi atas.
BROLL = [
 ("page:page_abc.png", 6.40, 8.40, 0, (1.00, 1.05), "50% 50%", "Kenal huruf A–Z?"),
 ("IMG_1278", 8.60, 10.60, 0.6, (1.06, 1.00), "45% 55%", "Baca suku kata?"),
 ("IMG_1279", 16.40, 18.75, 0.5, (1.00, 1.06), "50% 50%", "Bila bagi latihan..."),
 ("IMG_1272", 30.30, 32.95, 4.0, (1.00, 1.06), "50% 50%", "Ikut kemampuan anak"),
 ("IMG_1273", 34.95, 37.40, 0.0, (1.08, 1.00), "50% 40%", "Edisi 2027"),
 ("IMG_1276", 44.24, 46.70, 0.0, (1.00, 1.06), "50% 40%", "Latihan merangkumi..."),
 ("IMG_1279", 52.77, 55.34, 7.6, (1.00, 1.06), "50% 50%", "Kenal corak & cari jawapan"),
 ("IMG_1274", 58.05, 60.30, 0.0, (1.00, 1.14), "30% 82%", "Siap video tutorial!"),
 ("IMG_1280", 66.06, 68.34, 0.4, (1.00, 1.06), "50% 50%", "Masih lemah? Praktis lagi!"),
]
PUNCH = [1.52, 22.41, 28.93, 46.74, 56.87, 71.73, 77.88, 84.68]

# ------------------------------------------------------------------ CSS
# Gaya pilihan pengguna = versi PERTAMA (kotak gelap, border kuning mustard, nombor kuning,
# teks putih bold) tetapi LEBIH KECIL. (Frosted glass ditolak: "tak cantik".)
DARK = f"background:rgba(16,15,18,.82);border:3.5px solid {ACC};box-shadow:0 12px 34px rgba(0,0,0,.45),0 0 22px rgba(255,194,26,.22);"
SOUND_ALL = None   # varian: 'toing' pada setiap kemasukan
ENTER = "pop"      # gaya animasi masuk (berbeza setiap varian)
ENTERS = {
 "pop":   ("scale:S0,y:30", 'scale:1,y:0,duration:.45,ease:"back.out(2.2)"'),
 "slide": ("x:-90,scale:.9", 'x:0,scale:1,duration:.5,ease:"power3.out"'),
 "drop":  ("y:-70,scale:.9", 'y:0,scale:1,duration:.65,ease:"bounce.out"'),
 "zoom":  ("scale:1.6", 'scale:1,duration:.42,ease:"expo.out"'),
 "flip":  ("rotationX:-90,transformPerspective:700,y:10", 'rotationX:0,y:0,duration:.55,ease:"back.out(1.6)"'),
}
def rich(t):
    """*perkataan* -> warna kuning mustard"""
    return re.sub(r'\*(.+?)\*', r'<b class="hi">\1</b>', html.escape(t))

TS = "text-shadow:0 2px 6px rgba(0,0,0,.45);"
CSS = f"""
#gfx{{position:absolute;inset:0;font-family:'Montserrat',sans-serif;color:#fff;}}
.clip.slot{{position:absolute;left:0;width:{W}px;text-align:center;}}
.g{{display:inline-block;position:relative;{DARK}{TS}}}
.sh{{display:none;}}
.hi{{color:{ACC};font-weight:inherit;}}
.cap .g{{font-weight:800;font-size:36px;line-height:1.15;padding:12px 28px 14px;border-radius:999px;white-space:nowrap;}}
.cap.big .g{{font-size:42px;padding:14px 32px 16px;}}
.hook .g{{font-weight:900;line-height:1.06;padding:18px 32px 22px;border-radius:30px;border-width:4px;}}
.hook .ln{{display:block;white-space:nowrap;}}
.hook .lab{{display:block;font-weight:800;font-size:24px;letter-spacing:.16em;color:{ACC};margin-bottom:6px;}}
.hook .sub{{display:block;margin-top:8px;font-weight:700;font-size:26px;}}
.card .g{{text-align:left;padding:18px 28px 20px;border-radius:28px;max-width:960px;}}
.head{{display:flex;align-items:center;gap:14px;}}
.num{{width:48px;height:48px;flex:none;border-radius:50%;background:{ACC};color:#141414;font-weight:900;font-size:27px;
  display:flex;align-items:center;justify-content:center;text-shadow:none;}}
.tt{{font-weight:900;font-size:40px;line-height:1.05;white-space:nowrap;}}
.sub{{display:block;margin-top:10px;font-weight:600;font-size:29px;line-height:1.25;color:rgba(255,255,255,.94);}}
.items{{display:flex;flex-wrap:wrap;gap:8px 22px;margin-top:12px;max-width:900px;}}
.it{{display:inline-flex;align-items:center;gap:8px;font-weight:800;font-size:29px;padding:2px 6px;white-space:nowrap;}}  /* tiada kotak dalam kotak */
.it i{{width:30px;height:30px;border-radius:50%;background:{ACC};display:flex;align-items:center;justify-content:center;flex:none;}}
.row .wrap{{display:inline-flex;gap:12px;}}
.row .g{{font-weight:800;font-size:34px;padding:10px 24px 12px;border-radius:999px;white-space:nowrap;}}
.tag .g{{font-weight:800;font-size:30px;padding:9px 24px 11px;border-radius:999px;white-space:nowrap;border-width:2.5px;}}
"""
CHECK = ('<svg viewBox="0 0 24 24" width="22" height="22" fill="none" stroke="#141414" stroke-width="3" '
         'stroke-linecap="round" stroke-linejoin="round"><path d="M5 12.5l4.5 4.5L19 7.5"/></svg>')

SH = '<span class="sh"></span>'
def pop_in(sel, t, js, sfx, s0=.55, sound=None, shine=True):
    """Masuk: naik sikit + scale spring + kilauan kaca menyapu. Bunyi hanya jika `sound`."""
    t = round(t, 3)
    sound = SOUND_ALL or sound
    fr_, to_ = ENTERS[ENTER]
    js.append(f'tl.fromTo("{sel}",{{opacity:0,{fr_.replace("S0", str(s0))}}},{{opacity:1,{to_}}},{t});')
    if sound:
        sfx.append([t, sound])

def build_gfx(els, sid="gfx", t0=0.0, dur=DUR, broll=(), y0=200):
    """Satu komposisi grafik. Masa elemen mutlak; t0 = offset (untuk varian).
    Pulangkan (html, sfx_times) - sfx_times relatif kepada komposisi."""
    body, js, sfx, SLOTS = [], [], [], []
    NOHIDE = set()
    for n, el in enumerate(els):
        i = f"{sid}-{el['k']}{n}"
        st = round(el["s"] - t0, 3); en = round(min(el["e"], t0 + dur) - t0, 3); d = round(en - st, 3)
        if d <= 0.05 or en <= 0: continue
        k = el["k"]; y = el.get("y", y0); fin = el.get("final")
        SLOTS.append((i, st, en))
        if el.get("nohide"): NOHIDE.add(i)
        if k == "cap":
            body.append(f'<div id="{i}" class="clip slot cap{" big" if el.get("big") else ""}" data-start="{st}" data-duration="{d}" data-track-index="2" style="top:{y}px">'
                        f'<div class="g" id="{i}-in">{SH}{rich(el["text"])}</div></div>')
            pop_in(f"#{i}-in", st, js, sfx, sound=el.get("sfx"))
        elif k == "hook":
            longest = max(len(l) for l in el["lines"])
            longest = max(len(l.replace("*", "")) for l in el["lines"])
            fs = min(60, int(820 / (longest * 0.70)))
            lines = "".join(f'<span class="ln">{rich(l)}</span>' for l in el["lines"])
            lab = f'<span class="lab">{html.escape(el["label"])}</span>' if el.get("label") else ""
            sub = f'<span class="sub">{html.escape(el["sub"])}</span>' if el.get("sub") else ""
            body.append(f'<div id="{i}" class="clip slot hook" data-start="{st}" data-duration="{d}" data-track-index="2" style="top:{y-10}px">'
                        f'<div class="g" id="{i}-in" style="font-size:{fs}px">{SH}{lab}{lines}{sub}</div></div>')
            if st > 0.01:   # hook pembuka mesti penuh pada frame 0 (thumbnail)
                pop_in(f"#{i}-in", st, js, sfx, sound=el.get("sfx"))
            else:
                js.append(f'tl.fromTo("#{i}-in",{{scale:1}},{{scale:1.04,duration:.25,ease:"power2.out",yoyo:true,repeat:1}},0.35);')
        elif k == "card":
            head = f'<div class="head"><span class="num">{html.escape(el["num"])}</span><span class="tt">{html.escape(el["title"])}</span></div>'
            extra = ""
            if el.get("sub"):
                extra = f'<span class="sub" id="{i}-sub">{html.escape(el["sub"])}</span>'
            if el.get("items"):
                extra = '<div class="items">' + "".join(f'<span class="it" id="{i}-g{j}"><i>{CHECK}</i>{html.escape(tx)}</span>'
                                                         for j, (tx, _) in enumerate(el["items"])) + "</div>"
            body.append(f'<div id="{i}" class="clip slot card" data-start="{st}" data-duration="{d}" data-track-index="3" style="top:{y-10}px">'
                        f'<div class="g" id="{i}-in">{SH}{head}{extra}</div></div>')
            pop_in(f"#{i}-in", st, js, sfx, sound="pop")
            js.append(f'tl.fromTo("#{i} .num",{{rotation:-140,scale:.2}},{{rotation:0,scale:1,duration:.5,ease:"back.out(2.2)"}},{round(st+.08,3)});')
            js.append(f'tl.fromTo("#{i} .tt",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:.45,ease:"power3.out"}},{round(st+.15,3)});')
            if el.get("sub"):
                js.append(f'tl.fromTo("#{i}-sub",{{opacity:0,y:10}},{{opacity:1,y:0,duration:.35,ease:"power2.out"}},{round(st+.35,3)});')
            for j, (_, t) in enumerate(el.get("items", [])):
                pop_in(f"#{i}-g{j}", max(st + .35, t - t0 - .05), js, sfx, .3, shine=False)
        elif k == "row":
            pills = "".join(f'<span class="g" id="{i}-g{j}">{SH}{html.escape(tx)}</span>' for j, (tx, _) in enumerate(el["items"]))
            body.append(f'<div id="{i}" class="clip slot row" data-start="{st}" data-duration="{d}" data-track-index="3" style="top:{y}px">'
                        f'<div class="wrap" id="{i}-in">{pills}</div></div>')
            for j, (_, t) in enumerate(el["items"]):
                pop_in(f"#{i}-g{j}", max(st, t - t0 - .05), js, sfx, .5)
        if not fin:
            js.append(f'tl.to("#{i}-in",{{opacity:0,y:-16,scale:.94,duration:.24,ease:"power2.in"}},{round(en-.26,3)});')
    # semasa b-roll: sorok caption lain, tunjuk tag kecil
    for n, (f, bs, be, *_r) in enumerate(broll):
        bs, be = round(bs - t0, 3), round(be - t0, 3)
        if be <= 0 or bs >= dur: continue
        tag = _r[3] if len(_r) > 3 else None
        if tag:
            i = f"{sid}-tag{n}"; ts = round(max(bs + .1, 0), 3)
            body.append(f'<div id="{i}" class="clip slot tag" data-start="{ts}" data-duration="{round(be-ts-.05,3)}" data-track-index="4" style="top:{y0-20}px">'
                        f'<div class="g" id="{i}-in">{SH}{html.escape(tag)}</div></div>')
            pop_in(f"#{i}-in", ts + .12, js, sfx)
            js.append(f'tl.to("#{i}-in",{{opacity:0,duration:.2,ease:"power2.in"}},{round(be-.3,3)});')
        for el_id, est, een in [x for x in SLOTS if x[0] not in NOHIDE]:
            if est < be and een > bs:
                js += [f'tl.to("#{el_id}",{{opacity:0,duration:.18,ease:"power2.in"}},{round(max(est, bs-.05),3)});',
                       f'tl.to("#{el_id}",{{opacity:1,duration:.25,ease:"power2.out"}},{round(be-.3,3)});']
    sfx = sorted(e for e in sfx if 0 <= e[0] < dur)
    doc = f"""<template>
<style>{CSS}</style>
<div id="gfx" data-composition-id="{sid}" data-width="{W}" data-height="{H}" data-layout-allow-overlap>
{chr(10).join(body)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines["{sid}"] = tl;
</script>
</template>
"""
    return doc, sfx

def build_root(dur, broll, punch, segs, gfx_ids, a_start=0.0, extra_html="", extra_js=None, pre=None):
    """Root composition. a_start = data-media-start untuk aroll (varian boleh mula di tengah).
    pre = (fail_klip, tempoh) klip pembuka sebelum A-roll (varian)."""
    off = pre[1] if pre else 0.0
    def bhtml(n, f, s, e, ms, o):
        if f.startswith("page:"):   # kad halaman terapung atas latar kabur
            src = "assets/broll/" + f[5:]
            return (f'<div class="bw page clip" id="b{n}w" data-start="{s}" data-duration="{round(e-s,3)}" data-track-index="{4+n}">'
                    f'<img class="pbg" src="{src}"><div class="pc" id="b{n}"><img src="{src}"></div></div>')
        src = f if f.startswith("assets/") else "assets/broll/" + f + ".mp4"
        return (f'<div class="bw" id="b{n}w" style="transform-origin:{o}"><video id="b{n}" class="clip" src="{src}" '
                f'data-start="{s}" data-duration="{round(e-s,3)}" data-media-start="{ms}" data-track-index="{4+n}" muted playsinline></video></div>')
    broll_html = "\n".join(bhtml(n, f, s, e, ms, o) for n, (f, s, e, ms, kb, o, *_t) in enumerate(broll))
    hosts = "\n".join(
        f'<div id="{g}" data-composition-id="{g}" data-composition-src="compositions/{g}.html" data-start="{gs}" '
        f'data-duration="{gd}" data-track-index="{30+n}" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:20"></div>'
        for n, (g, gs, gd) in enumerate(gfx_ids))
    js = ['tl.set("#cam",{scale:1,transformOrigin:"50% 42%"},0);']
    for n, sg in enumerate(segs):
        base = 1.0   # tiada zoom 1.06x bergilir (besarkan imej = lebih kabur); zoom punch pendek kekal
        dy = CAM_DY(sg[0])
        js.append(f'tl.set("#cam",{{scale:{base},y:{dy}}},{sg[0]});')
        for p in punch:
            if sg[0] <= p < sg[1]:
                js.append(f'tl.fromTo("#cam",{{scale:{base}}},{{scale:{round(base+0.07,3)},duration:.22,ease:"expo.out"}},{p});')
    for n, (f, s, e, ms, (k0, k1), o, *_t) in enumerate(broll):
        if f.startswith("page:"):
            js += [f'tl.fromTo("#b{n}w",{{opacity:0}},{{opacity:1,duration:.3,ease:"power2.out"}},{s});',
                   f'tl.fromTo("#b{n}",{{y:260,rotation:-5,scale:.86}},{{y:0,rotation:0,scale:1,duration:.6,ease:"power3.out"}},{s});',
                   f'tl.to("#b{n}",{{scale:{k1},duration:{round(e-s-.6,3)},ease:"none"}},{round(s+.6,3)});',
                   f'tl.to("#b{n}",{{y:-80,opacity:0,duration:.25,ease:"power2.in"}},{round(e-.27,3)});',
                   f'tl.to("#b{n}w",{{opacity:0,duration:.22,ease:"power1.in"}},{round(e-.22,3)});']
            continue
        if s < 0.05:   # b-roll pembuka varian: penuh dari frame 0 (thumbnail)
            js += [f'tl.set("#b{n}w",{{opacity:1}},0);',
                   f'tl.fromTo("#b{n}w",{{scale:{k0}}},{{scale:{k1},duration:{round(e-s,3)},ease:"none"}},0);',
                   f'tl.to("#b{n}w",{{opacity:0,duration:.22,ease:"power1.in"}},{round(e-.22,3)});']
            continue
        js += [f'tl.set("#b{n}w",{{opacity:1}},{s});',
               f'tl.fromTo("#b{n}w",{{clipPath:"inset(100% 0% 0% 0% round 60px)"}},{{clipPath:"inset(0% 0% 0% 0% round 0px)",duration:.5,ease:"power3.inOut"}},{s});',
               f'tl.fromTo("#b{n}",{{scale:1.12}},{{scale:1,duration:.7,ease:"power3.out"}},{s});',
               f'tl.fromTo("#b{n}w",{{scale:{k0}}},{{scale:{k1},duration:{round(e-s,3)},ease:"none"}},{s});',
               f'tl.to("#b{n}w",{{opacity:0,duration:.22,ease:"power1.in"}},{round(e-.22,3)});']
    js.append(f'tl.fromTo("#glow",{{x:-240}},{{x:240,duration:{round(dur/2,3)},ease:"sine.inOut",yoyo:true,repeat:1}},0);')
    js += extra_js or []
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
#cam {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; z-index:2; }}
#aroll {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; object-fit:cover; }}
#scrim {{ position:absolute; left:0; top:0; width:{W}px; height:560px; z-index:12; pointer-events:none;
  background:linear-gradient(180deg,rgba(13,12,11,.35) 0%,rgba(13,12,11,.15) 260px,rgba(13,12,11,0) 520px); }}
#glow {{ position:absolute; left:240px; top:-260px; width:600px; height:600px; border-radius:50%; z-index:13; pointer-events:none;
  background:radial-gradient(circle, rgba(255,194,26,.16) 0%, rgba(255,194,26,0) 70%); }}
.bw {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; z-index:8; opacity:0; }}
.bw video {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; object-fit:cover; }}
.page {{ background:#0d0c0b; overflow:hidden; }}
.page .pbg {{ position:absolute; left:-60px; top:-60px; width:{W+120}px; height:{H+120}px; object-fit:cover; filter:blur(30px) brightness(.55); }}
.page .pc {{ position:absolute; left:90px; top:330px; width:900px; border-radius:22px; overflow:hidden;
  box-shadow:0 30px 70px rgba(0,0,0,.55), 0 0 0 4px rgba(255,255,255,.9); }}
.page .pc img {{ display:block; width:900px; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{dur}" data-width="{W}" data-height="{H}">
<div id="cam"><video id="aroll" class="clip" src="assets/aroll.mp4" data-start="{off}" data-duration="{round(dur-off,3)}" data-media-start="{a_start}" data-track-index="1" playsinline data-has-audio="true"></video></div>
{extra_html}
{broll_html}
<div id="scrim"></div>
<div id="glow"></div>
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

SEGS = [(s["start"], s["end"]) for s in EDL["segments"]]
# klip dfe55 (61-79 s): duduk lebih tinggi dalam frame -> turunkan A-roll supaya teks di atas kepala
def CAM_DY(t, lo=68.3, hi=79.1):
    return 110 if lo <= t < hi else 0

# (tiada __main__: lihat pipeline/variants.py)
