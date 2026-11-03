#!/usr/bin/env python3
"""Jana projek HyperFrames (index.html + compositions/*.html) untuk video TikTok
Modul Transisi Tahun 1 Edisi 2027. Semua masa = saat MUTLAK pada assets/aroll.mp4
(rujuk pipeline/words.json untuk masa setiap perkataan).

Gaya: teks putih Montserrat 800/900 + shadow, aksen mustard #FFC21A. Semua teks di
band atas (y 170-600, bumbung kereta) - tidak tutup muka atau buku. Tiada muzik / SFX."""
import json, html, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.dirname(HERE)
W, H = 1080, 1920
ACC = "#FFC21A"
EDL = json.load(open(os.path.join(HERE, "edl.json")))
DUR = round(EDL["dur"], 3)

ICON = {
 "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 "q": '<path d="M9 9a3 3 0 1 1 4.2 2.75c-.75.35-1.2 1-1.2 1.8V14"/><circle cx="12" cy="18" r=".6" fill="#141414"/>',
 "play": '<circle cx="12" cy="12" r="9"/><path d="M10 8.5l6 3.5-6 3.5z" fill="#141414"/>',
 "repeat": '<path d="M4 12a8 8 0 0 1 13.7-5.6L20 9"/><path d="M20 4v5h-5"/><path d="M20 12a8 8 0 0 1-13.7 5.6L4 15"/><path d="M4 20v-5h5"/>',
 "book": '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/>',
 "pen": '<path d="M4 20l4-1 11-11-3-3L5 16z"/><path d="M14 6l3 3"/>',
 "calc": '<rect x="5" y="3" width="14" height="18" rx="2"/><path d="M8 7h8M8 12h2M14 12h2M8 16h2M14 16h2"/>',
 "bulb": '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/>',
 "star": '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z" fill="#141414"/>',
 "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
}
def svg(name, s=40):
    return (f'<svg viewBox="0 0 24 24" width="{s}" height="{s}" fill="none" stroke="#141414" '
            f'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</svg>')

# ------------------------------------------------------------------ elemen teks
# kick(text) | hl(lines, hi, wt, punch) | chip(text, icon, y) | hook(lines, label, hi)
# info(num, title, body) | infogrid(num, title, items[(text, icon, t)])
EL_RAW = [
 # --- HOOK (kelihatan dari frame 0) ---
 dict(k="hook", s=0.0, e=4.40, label="SESI PERSEKOLAHAN 2027", lines=["ANAK DAH 6 TAHUN?", "NEXT YEAR TAHUN 1!"], hi="1!", y=190),
 # --- semak kemahiran asas ---
 dict(k="infogrid", s=4.46, e=13.15, num="?", title="ANAK DAH BOLEH...", cols=2, items=[
     ("Kenal huruf A–Z", "q", 5.90), ("Baca suku kata", "q", 8.48), ("Menulis", "q", 9.98), ("Kenal nombor & kira", "q", 11.02)]),
 # --- kenapa perlu latihan ---
 dict(k="hl", s=13.24, e=16.30, lines=["INGAT ANAK", "DAH OKAY?"], hi="OKAY?", wt=[13.24, 14.72, 15.86, 16.00]),
 dict(k="hl", s=18.80, e=21.28, lines=["BARU NAMPAK MANA", "BELUM KUASAI"], hi="KUASAI", wt=[17.9, 18.16, 18.80, 20.66, 20.94], punch=True),
 dict(k="info", s=21.33, e=25.05, num="1", title="PERSIAPAN AWAL|TAHUN 1 2027",
      body="Bantu anak biasakan diri dengan aktiviti pembelajaran sebelum masuk sekolah rendah."),
 # --- 10-15 minit sehari ---
 dict(k="hl", s=25.09, e=27.20, lines=["BUKAN PAKSA", "BELAJAR BERJAM-JAM"], hi="BERJAM-JAM", wt=[25.12, 25.35, 25.63, 25.97]),
 dict(k="hl", s=27.25, e=30.02, e_fix=30.25, lines=["10–15 MINIT", "SEHARI PUN CUKUP"], hi="CUKUP", wt=[28.15, 28.60, 28.75, 28.95, 29.10], punch=True),
 # --- produk ---
 dict(k="kick", s=33.00, e=35.05, text="SUE NAK SHARE"),
 dict(k="hl", s=33.05, e=35.05, lines=["MODUL TRANSISI", "TAHUN 1 EDISI 2027"], hi="2027", wt=[33.15, 33.35, 33.6, 33.8, 34.0, 34.2], y=290),
 dict(k="infogrid", s=37.42, e=44.20, num="3", title="5 SUBJEK DALAM SATU BUKU", cols=2, items=[
     ("Bahasa Melayu", "check", 39.46), ("Bahasa Inggeris", "check", 40.60), ("Matematik", "check", 41.24),
     ("Alam dan Manusia", "check", 42.08), ("Bahasa Arab", "check", 43.60)]),
 dict(k="infogrid", s=46.74, e=50.34, num="2", title="KEMAHIRAN 4M", cols=2, items=[
     ("Membaca", "book", 47.70), ("Menulis", "pen", 48.44), ("Mengira", "calc", 49.04), ("Menaakul", "bulb", 49.76)]),
 dict(k="hl", s=50.39, e=52.72, lines=["MENAAKUL =", "BELAJAR BERFIKIR"], hi="BERFIKIR", wt=[50.39, 50.80, 52.15, 52.77]),
 dict(k="info", s=55.39, e=58.05, num="4", title="VIDEO TUTORIAL & JAWAPAN", icon="play",
      body="Bantu ibu ayah membimbing anak semasa membuat latihan di rumah."),
 dict(k="info", s=60.30, e=64.30, num="5", title="KENAL PASTI TAHAP|KEMAHIRAN ANAK",
      body="Tengok bahagian yang anak sudah kuasai dan bahagian yang masih perlu diperbaiki."),
 dict(k="chip", s=64.36, e=66.00, text="Dah okay? Teruskan!", icon="check", y=300),
 # --- mesej ---
 dict(k="hl", s=68.39, e=72.00, lines=["BUKAN NAK ANAK PANDAI", "DALAM SEHARI"], hi="SEHARI",
      wt=[69.79, 70.69, 71.15, 71.35, 71.59, 71.73]),
 dict(k="hl", s=72.03, e=77.28, lines=["LEBIH BIASA.", "LEBIH BERSEDIA.", "LEBIH YAKIN."], hi="YAKIN.",
      wt=[72.81, 73.09, 75.35, 75.61, 76.31, 76.73]),
 dict(k="hl", s=77.33, e=79.14, lines=["MASUK TAHUN 1!"], punch=True, wt=[77.88, 78.50, 78.72]),
 # --- CTA (ayat pengguna sendiri) ---
 dict(k="kick", s=79.18, e=84.60, text="TAHUN 1 • 2027"),
 dict(k="hl", s=79.25, e=81.56, lines=["JOM BUAT", "PERSEDIAAN AWAL!"], hi="AWAL!", wt=[79.46, 79.82, 80.80, 81.0], y=300),
 dict(k="hl", s=81.60, e=84.60, lines=["MODUL TRANSISI", "TAHUN 1 EDISI 2027"], hi="2027", wt=[82.46, 82.76, 83.22, 83.52, 84.20, 84.68], y=300),
 dict(k="hook", s=84.65, e=DUR, label="PREPARE AWAL, ANAK PUN LEBIH READY!", lines=["CHECK DI", "BAKUL KUNING!"], hi="KUNING!", y=200, final=True),
]

EL = [dict(el, e=el.pop("e_fix")) if "e_fix" in el else el for el in EL_RAW]

# b-roll: (fail, mula, tamat, media_start, kenburns (dari, ke), origin)
EL = [dict(el, e=el.pop("e_fix")) if "e_fix" in el else el for el in EL_RAW]

# b-roll: (fail, mula, tamat, media_start, kenburns (dari, ke), origin, tag)
# Semasa b-roll: semua pop-up disorok (buku bersih); hanya tag kecil di tepi atas.
BROLL = [
 ("sr_abc",   6.40,  8.40, 0.3, (1.00, 1.06), "50% 45%", "Kenal huruf A–Z?"),
 ("IMG_1278", 8.60, 10.60, 0.6, (1.06, 1.00), "45% 55%", "Baca suku kata?"),
 ("IMG_1279", 16.40, 18.75, 0.5, (1.00, 1.06), "50% 50%", "Bila bagi latihan..."),
 ("IMG_1272", 30.30, 32.95, 4.0, (1.00, 1.06), "50% 50%", "Ikut kemampuan anak"),
 ("IMG_1273", 34.95, 37.40, 0.0, (1.08, 1.00), "50% 40%", None),            # cover: tiada teks
 ("IMG_1276", 44.24, 46.70, 0.0, (1.00, 1.06), "50% 40%", "Latihan merangkumi..."),
 ("sr_corak", 52.77, 55.34, 0.3, (1.00, 1.05), "50% 50%", "Kenal corak & cari jawapan"),
 ("IMG_1274", 58.05, 60.30, 0.0, (1.00, 1.18), "30% 82%", "Video tutorial & jawapan"),
 ("IMG_1280", 66.06, 68.34, 0.4, (1.00, 1.06), "50% 50%", "Masih lemah? Praktis lagi!"),
]
PUNCH = [1.52, 22.41, 28.93, 46.74, 56.87, 71.73, 77.88, 84.68]

# ------------------------------------------------------------------ CSS
CSS = f"""
#gfx{{position:absolute;inset:0;font-family:'Montserrat',sans-serif;color:#fff;}}
.clip.slot{{position:absolute;left:0;width:{W}px;text-align:center;}}
.in{{display:inline-block;position:relative;}}
.kick .in{{font-weight:800;font-size:24px;letter-spacing:.2em;padding:7px 20px 7px 24px;border:2.5px solid {ACC};
  border-radius:999px;background:rgba(0,0,0,.30);text-shadow:0 3px 14px rgba(0,0,0,.8),0 1px 3px rgba(0,0,0,.9);}}
.hl .in{{font-weight:900;line-height:1.06;letter-spacing:-.005em;text-shadow:0 3px 14px rgba(0,0,0,.8),0 1px 3px rgba(0,0,0,.9);}}
.ln{{display:block;white-space:nowrap;}}
.w{{display:inline-block;position:relative;margin:0 .12em;isolation:isolate;}}
.bar{{position:absolute;left:-4%;right:-4%;bottom:-.06em;height:.15em;background:{ACC};border-radius:5px;z-index:-1;}}
.card{{display:inline-block;position:relative;text-align:center;max-width:960px;text-shadow:0 3px 14px rgba(0,0,0,.8),0 1px 3px rgba(0,0,0,.9);}}
.head{{display:flex;align-items:center;justify-content:center;gap:14px;}}
.num{{width:48px;height:48px;flex:none;border-radius:50%;background:{ACC};color:#141414;font-weight:900;font-size:27px;
  display:flex;align-items:center;justify-content:center;text-shadow:none;box-shadow:0 2px 10px rgba(0,0,0,.5);}}
.tt{{font-weight:900;font-size:46px;line-height:1.08;text-align:left;}}
.bd{{display:block;margin-top:10px;font-weight:700;font-size:30px;line-height:1.3;color:#fff;}}
.grid{{display:flex;flex-wrap:wrap;justify-content:center;gap:8px 26px;margin-top:12px;max-width:940px;}}
.gi{{display:flex;align-items:center;gap:9px;}}
.gi .ico{{width:36px;height:36px;box-shadow:0 2px 8px rgba(0,0,0,.5);}}
.gi .ct{{font-weight:800;font-size:33px;white-space:nowrap;}}
.ico{{width:52px;height:52px;border-radius:50%;background:{ACC};display:flex;align-items:center;justify-content:center;flex:none;}}
.chip .in{{display:inline-flex;align-items:center;gap:14px;text-shadow:0 3px 14px rgba(0,0,0,.8),0 1px 3px rgba(0,0,0,.9);}}
.chip .ct{{font-weight:900;font-size:50px;white-space:nowrap;}}
.tag .in{{display:inline-flex;align-items:center;gap:10px;font-weight:800;font-size:34px;padding:8px 22px 9px 10px;border-radius:999px;
  background:rgba(16,15,18,.80);border:2.5px solid {ACC};box-shadow:0 6px 18px rgba(0,0,0,.35);}}
.tag .dot{{width:30px;height:30px;border-radius:50%;background:{ACC};flex:none;}}
.hook .in{{font-weight:900;line-height:1.06;text-shadow:0 3px 14px rgba(0,0,0,.8),0 1px 3px rgba(0,0,0,.9);}}
.hook .lab{{display:inline-block;font-weight:800;font-size:24px;letter-spacing:.16em;color:#141414;background:{ACC};
  padding:6px 16px;border-radius:8px;margin-bottom:12px;text-shadow:none;}}
.hook.cta .in{{padding:16px 30px 20px;border-radius:28px;background:rgba(16,15,18,.72);border:3px solid {ACC};}}
"""

def words_html(i, lines, hi):
    out, wi = [], 0
    for ln in lines:
        parts = []
        for w in ln.split(" "):
            bar = f'<span class="bar" id="{i}-bar"></span>' if w == hi else ""
            parts.append(f'<span class="w" id="{i}-w{wi}">{bar}{html.escape(w)}</span>'); wi += 1
        out.append(f'<span class="ln">{" ".join(parts)}</span>')
    return "".join(out), wi

def build_gfx(els, sid="gfx", t0=0.0, dur=DUR, broll=()):
    """Satu komposisi grafik. els guna masa mutlak; t0 = offset (untuk varian)."""
    body, js = [], []
    SLOTS = []
    for n, el in enumerate(els):
        i = f"{sid}-{el['k']}{n}"
        st = round(el["s"] - t0, 3); en = round(min(el["e"], t0 + dur) - t0, 3); d = round(en - st, 3)
        if d <= 0.05: continue
        k = el["k"]; y = el.get("y")
        SLOTS.append((i, st, en))
        fin = el.get("final")
        if k == "kick":
            body.append(f'<div id="{i}" class="clip slot kick" data-start="{st}" data-duration="{d}" data-track-index="1" style="top:{y or 190}px">'
                        f'<div class="in" id="{i}-in">{html.escape(el["text"])}</div></div>')
            js.append(f'tl.fromTo("#{i}-in",{{opacity:0,clipPath:"inset(0 50% 0 50% round 999px)"}},{{opacity:1,clipPath:"inset(0 0% 0 0% round 999px)",duration:.42,ease:"expo.out"}},{st});')
            js.append(f'tl.to("#{i}-in",{{opacity:0,duration:.2,ease:"power2.in"}},{round(en-.22,3)});')
        elif k == "hl":
            inner, nw = words_html(i, el["lines"], el.get("hi"))
            longest = max(len(l) for l in el["lines"])
            fs = 70 if len(el["lines"]) == 1 else (64 if len(el["lines"]) == 2 else 56)
            fs = min(fs, int(900 / (longest * 0.70)))
            top = y or (300 if len(el["lines"]) == 1 else (250 if len(el["lines"]) == 2 else 200))
            body.append(f'<div id="{i}" class="clip slot hl" data-start="{st}" data-duration="{d}" data-track-index="2" style="top:{top}px">'
                        f'<div class="in" id="{i}-in" style="font-size:{fs}px">{inner}</div></div>')
            wt = [x - t0 for x in (el.get("wt") or [])] or [st + 0.07 * j for j in range(nw)]
            wt = (wt + [wt[-1] + 0.08 * (j + 1) for j in range(nw)])[:nw]
            for j in range(nw):
                t = round(max(st, min(wt[j], en - 0.6)), 3)
                js.append(f'tl.fromTo("#{i}-w{j}",{{opacity:0,y:46,scale:.55,filter:"blur(10px)"}},{{opacity:1,y:0,scale:1,filter:"blur(0px)",duration:.34,ease:"back.out(2.2)"}},{t});')
            if el.get("hi"):
                js.append(f'tl.fromTo("#{i}-bar",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:.38,ease:"expo.out"}},{round(min(max(wt)+.12, en-.5),3)});')
            if el.get("punch"):
                js.append(f'tl.fromTo("#{i}-in",{{scale:1.3}},{{scale:1,duration:.38,ease:"expo.out"}},{st});')
            if not fin:
                js.append(f'tl.to("#{i}-in",{{opacity:0,y:-22,filter:"blur(8px)",duration:.18,ease:"power2.in"}},{round(en-.2,3)});')
        elif k == "chip":
            body.append(f'<div id="{i}" class="clip slot chip" data-start="{st}" data-duration="{d}" data-track-index="3" style="top:{y or 300}px">'
                        f'<div class="in" id="{i}-in"><span class="ico" id="{i}-ico">{svg(el["icon"], 32)}</span>'
                        f'<span class="ct" id="{i}-ct">{html.escape(el["text"])}</span></div></div>')
            js += [f'tl.fromTo("#{i}-in",{{opacity:0,scale:.4,y:30}},{{opacity:1,scale:1,y:0,duration:.42,ease:"back.out(2.4)"}},{st});',
                   f'tl.fromTo("#{i}-ico",{{rotation:-120,scale:.3}},{{rotation:0,scale:1,duration:.5,ease:"back.out(2)"}},{round(st+.05,3)});',
                   f'tl.fromTo("#{i}-ct",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:.4,ease:"power3.out"}},{round(st+.12,3)});',
                   f'tl.to("#{i}-in",{{opacity:0,scale:.85,duration:.2,ease:"power2.in"}},{round(en-.22,3)});']
        elif k == "hook":
            inner, nw = words_html(i, el["lines"], el.get("hi"))
            longest = max(len(l) for l in el["lines"])
            fs = min(78, int(860 / (longest * 0.70)))
            lab = f'<span class="lab">{html.escape(el["label"])}</span><br>' if el.get("label") else ""
            body.append(f'<div id="{i}" class="clip slot hook{' cta' if fin else ''}" data-start="{st}" data-duration="{d}" data-track-index="2" style="top:{y or 200}px">'
                        f'<div class="in" id="{i}-in" style="font-size:{fs}px">{lab}{inner}</div></div>')
            if st > 0.01:  # hook pertama mesti penuh pada frame 0 (thumbnail)
                js.append(f'tl.fromTo("#{i}-in",{{opacity:0,scale:1.3,rotation:-2}},{{opacity:1,scale:1,rotation:0,duration:.45,ease:"back.out(1.8)"}},{st});')
            for j in range(nw):
                js.append(f'tl.fromTo("#{i}-w{j}",{{y:0}},{{y:-10,duration:.12,ease:"power2.out",yoyo:true,repeat:1}},{round(st+.45+.07*j,3)});')
            if el.get("hi"):
                js.append(f'tl.fromTo("#{i}-bar",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:.4,ease:"expo.out"}},{round(st+.55,3)});')
            if not fin:
                js.append(f'tl.to("#{i}-in",{{opacity:0,scale:.9,filter:"blur(8px)",duration:.22,ease:"power2.in"}},{round(en-.24,3)});')
        elif k in ("info", "infogrid"):
            ic = f'<span class="num" id="{i}-num">{svg(el["icon"], 30) if el.get("icon") else html.escape(el["num"])}</span>'
            head = f'<div class="head">{ic}<span class="tt" id="{i}-tt">{"<br>".join(html.escape(x) for x in el["title"].split("|"))}</span></div>'
            extra = ""
            if k == "info":
                extra = f'<span class="bd" id="{i}-bd">{html.escape(el["body"])}</span>'
            else:
                cols = el.get("cols", 2)
                items = "".join(f'<div class="gi" id="{i}-g{j}"><span class="ico">{svg(icn, 24)}</span><span class="ct">{html.escape(tx)}</span></div>'
                                for j, (tx, icn, _) in enumerate(el["items"]))
                extra = f'<div class="grid" style="grid-template-columns:repeat({cols},auto)">{items}</div>'
            body.append(f'<div id="{i}" class="clip slot info" data-start="{st}" data-duration="{d}" data-track-index="3" style="top:{y or 180}px">'
                        f'<div class="card" id="{i}-in">{head}{extra}</div></div>')
            js += [f'tl.fromTo("#{i}-in",{{opacity:0,scale:.55,y:40}},{{opacity:1,scale:1,y:0,duration:.45,ease:"back.out(2)"}},{st});',
                   f'tl.fromTo("#{i}-num",{{rotation:-140,scale:.2}},{{rotation:0,scale:1,duration:.5,ease:"back.out(2.2)"}},{round(st+.08,3)});',
                   f'tl.fromTo("#{i}-tt",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:.45,ease:"power3.out"}},{round(st+.15,3)});']
            if k == "info":
                js.append(f'tl.fromTo("#{i}-bd",{{opacity:0,y:16}},{{opacity:1,y:0,duration:.4,ease:"power2.out"}},{round(st+.45,3)});')
            else:
                for j, (_, _, t) in enumerate(el["items"]):
                    js.append(f'tl.fromTo("#{i}-g{j}",{{opacity:0,scale:.3,y:20}},{{opacity:1,scale:1,y:0,duration:.4,ease:"back.out(2.6)"}},{round(max(st+.3, t - t0 - .05),3)});')
            js.append(f'tl.to("#{i}-in",{{opacity:0,scale:.9,duration:.22,ease:"power2.in"}},{round(en-.24,3)});')
    # sorok pop-up semasa b-roll; tag kecil ganti
    for n, (f, bs, be, *_rest) in enumerate(broll):
        bs, be = round(bs - t0, 3), round(be - t0, 3)
        tag = _rest[3] if len(_rest) > 3 else None
        if tag:
            i = f"{sid}-tag{n}"; d = round(be - bs - 0.1, 3)
            body.append(f'<div id="{i}" class="clip slot tag" data-start="{round(bs+.1,3)}" data-duration="{d}" data-track-index="4" style="top:170px">'
                        f'<div class="in" id="{i}-in"><span class="dot"></span>{html.escape(tag)}</div></div>')
            js += [f'tl.fromTo("#{i}-in",{{opacity:0,y:-20,scale:.8}},{{opacity:1,y:0,scale:1,duration:.35,ease:"back.out(2)"}},{round(bs+.15,3)});',
                   f'tl.to("#{i}-in",{{opacity:0,duration:.2,ease:"power2.in"}},{round(be-.3,3)});']
    hide = []
    for el_id, est, een in SLOTS:
        for (f, bs, be, *_r) in broll:
            bs, be = bs - t0, be - t0
            if est < be and een > bs:
                hide += [f'tl.to("#{el_id}",{{opacity:0,duration:.18,ease:"power2.in"}},{round(max(est, bs-.05),3)});',
                         f'tl.to("#{el_id}",{{opacity:1,duration:.25,ease:"power2.out"}},{round(be-.3,3)});']
    js += hide
    return f"""<template>
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

def build_root(dur, broll, punch, segs, gfx_ids, a_start=0.0, extra_html="", extra_js=None, pre=None):
    """Root composition. a_start = data-media-start untuk aroll (varian boleh mula di tengah).
    pre = (fail_klip, tempoh) klip pembuka sebelum A-roll (varian)."""
    off = pre[1] if pre else 0.0
    broll_html = "\n".join(
        f'<div class="bw" id="b{n}w" style="transform-origin:{o}"><video id="b{n}" class="clip" src="{f if f.startswith("assets/") else "assets/broll/" + f + ".mp4"}" '
        f'data-start="{s}" data-duration="{round(e-s,3)}" data-media-start="{ms}" data-track-index="{4+n}" muted playsinline></video></div>'
        for n, (f, s, e, ms, kb, o, *_t) in enumerate(broll))
    hosts = "\n".join(
        f'<div id="{g}" data-composition-id="{g}" data-composition-src="compositions/{g}.html" data-start="{gs}" '
        f'data-duration="{gd}" data-track-index="{30+n}" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:20"></div>'
        for n, (g, gs, gd) in enumerate(gfx_ids))
    js = ['tl.set("#cam",{scale:1,transformOrigin:"50% 42%"},0);']
    for n, sg in enumerate(segs):
        base = 1.0 if n % 2 == 0 else 1.06
        dy = CAM_DY(sg[0])
        js.append(f'tl.set("#cam",{{scale:{base},y:{dy}}},{sg[0]});')
        for p in punch:
            if sg[0] <= p < sg[1]:
                js.append(f'tl.fromTo("#cam",{{scale:{base}}},{{scale:{round(base+0.07,3)},duration:.22,ease:"expo.out"}},{p});')
    for n, (f, s, e, ms, (k0, k1), o, *_t) in enumerate(broll):
        js += [f'tl.fromTo("#b{n}w",{{opacity:0}},{{opacity:1,duration:.3,ease:"power2.out"}},{s});',
               f'tl.fromTo("#b{n}w",{{scale:{k0}}},{{scale:{k1},duration:{round(e-s,3)},ease:"none"}},{s});',
               f'tl.to("#b{n}w",{{opacity:0,duration:.3,ease:"power2.in"}},{round(e-.32,3)});']
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
  background:linear-gradient(180deg,rgba(13,12,11,.55) 0%,rgba(13,12,11,.30) 280px,rgba(13,12,11,0) 560px); }}
#glow {{ position:absolute; left:240px; top:-260px; width:600px; height:600px; border-radius:50%; z-index:13; pointer-events:none;
  background:radial-gradient(circle, rgba(255,194,26,.16) 0%, rgba(255,194,26,0) 70%); }}
.bw {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; z-index:8; opacity:0; }}
.bw video {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; object-fit:cover; }}
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

if __name__ == "__main__":
    os.makedirs(f"{PROJ}/compositions", exist_ok=True)
    open(f"{PROJ}/compositions/gfx.html", "w").write(build_gfx(EL, broll=BROLL))
    open(f"{PROJ}/index.html", "w").write(build_root(DUR, BROLL, PUNCH, SEGS, [("gfx", 0, DUR)]))
    print("ok dur", DUR, "elements", len(EL), "broll", len(BROLL))
