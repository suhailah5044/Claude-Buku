#!/usr/bin/env python3
"""Jana index.html (HyperFrames) + sfx.json untuk video Fly High.

Gaya (brief pengguna + guideline Iqra'):
- Font teks bergerak: Lilita One (paling hampir font "Vlogger." CapCut), saiz kecil (~50%) supaya buku jadi fokus.
- USP: baris gaya "Style 1" (tile ikon bulat-segi + teks), kuning HANYA untuk perkataan penting, di ruang atas.
- "Kelebihan": kad gaya Style 1 penuh - label kecil, tajuk KELEBIHAN DIA, pil putih, baris ikon, background blur.
- Subtitle VO: Montserrat 900 italic caps, kecil, di bawah (zon berasingan dari USP). Tiada teks "beg kuning".
- Smooth: Ken Burns halus setiap shot, transition blur-zoom lembut pada setiap cut, zoom punch kecil 3 kali.
- SFX lembut dari folder pengguna, bertukar-tukar (cut = swish/whoosh perlahan, overlay = pop/klik/chime).
Masa dalam saat FINAL (selepas susun semula + 1.1x, lihat prep.py)."""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from prep import mapt
DUR = 49.1

# ---------- cut shot (masa asal -> final) ----------
CUTS_ORIG = [1.5333, 5.1667, 6.4, 12.4667, 15.4667, 28.8, 30.8333, 33.0, 33.4333, 34.3667, 35.4, 36.4333, 37.3667,
             39.6333, 41.5, 43.3667, 44.3, 45.6, 49.7333, 50.7667, 51.1, 53.8333]
CUTS = sorted([round(mapt(22.2), 3), 4.182, 22.382] + [round(mapt(t), 3) for t in CUTS_ORIG])

# ---------- subtitle VO (teks dibetulkan; *perkataan* = kuning) ----------
SUBS = [
    (0.00, 0.92, "KITA TENGAH BELAJAR *MEMBACA*"),
    (0.94, 1.82, "MEMANG KENA MULA DARIPADA *ASAS*"),
    (1.84, 2.86, "SEBAB TU BUKU MACAM NI"),
    (2.88, 4.05, "MEMANG *SANGAT-SANGAT* MENARIK"),
    (4.08, 5.28, "KITA MULA KENAL *VOKAL*"),
    (5.30, 6.68, "ADA *A, E, I, O, U*"),
    (6.70, 7.90, "LEPAS TU ADA *LATIHAN* KECIL"),
    (7.92, 9.08, "CONTOHNYA KAT SINI DIA BAGI *A*"),
    (9.10, 10.95, "SURUH ANAK KITA *BULATKAN* DEKAT A"),
    (11.06, 12.70, "E, BULATKAN DEKAT *E*"),
    (12.80, 14.50, "I, BULATKAN DEKAT *I*"),
    (14.60, 16.25, "O, BULATKAN DEKAT *O*"),
    (16.36, 18.15, "DAN U, BULATKAN DEKAT *U*"),
    (18.22, 20.10, "PADA BAHAGIAN *DENGAR DAN TUNJUK*"),
    (20.16, 20.92, "KITA SEBUT BUNYI TU"),
    (20.94, 22.35, "ANAK KITA PULA CARI *HURUF* YANG BETUL"),
    (22.38, 23.90, "INI BUKU KELUARAN *FLY HIGH*"),
    (23.94, 25.25, "SIRI MENGENAL, MEMBACA,"),
    (25.28, 26.00, "MEMBUNYIKAN *SUKU KATA*"),
    (26.02, 27.02, "INI ADA *LIMA TAHAP* TAU"),
    (27.06, 28.00, "DARIPADA ANAK MULA KENAL HURUF"),
    (28.04, 29.68, "SAMPAILAH MEMBACA *AYAT* DAN *CERITA*"),
    (29.72, 30.68, "*BUKU SATU* NI UNTUK ANAK KITA"),
    (30.70, 31.78, "KENAL *HURUF* DAN *BUNYI*"),
    (31.82, 32.68, "*BUKU DUA*, KITA MULA"),
    (32.70, 34.35, "BELAJAR DAN *CANTUM SUKU KATA*"),
    (34.40, 35.22, "MASUK *BUKU 3* DAN *4*"),
    (35.24, 37.40, "ANAK KITA TERUS *PRAKTIS* MEMBACA"),
    (37.44, 38.38, "BILA MASUK *BUKU KELIMA*"),
    (38.40, 39.44, "ANAK KITA MULA MEMBACA *AYAT*"),
    (39.46, 40.58, "*CERITA* DAN *DIALOG*"),
    (40.62, 41.86, "BUKAN SEKADAR KENAL HURUF"),
    (41.88, 43.68, "BELAJAR *LANGKAH DEMI LANGKAH*"),
    (43.72, 44.72, "KALAU IBU AYAH TENGAH CARI"),
    (44.74, 46.22, "BAHAN *LATIHAN MEMBACA* UNTUK ANAK"),
    (46.28, 47.48, "IBU AYAH BOLEH DAPATKAN"),
    (47.50, 48.30, "SET *FLY HIGH* NI"),
]

# ---------- ikon (garis, gaya lucide) ----------
IC = {
    "book": '<path d="M2 4h6a4 4 0 0 1 4 4v13a3 3 0 0 0-3-3H2z"/><path d="M22 4h-6a4 4 0 0 0-4 4v13a3 3 0 0 1 3-3h7z"/>',
    "abc": '<path d="M3 17l3.5-10L10 17"/><path d="M4.3 13.5h4.4"/><path d="M13 7v10h3.2a2.4 2.4 0 0 0 0-4.8H13"/><path d="M13 12.2h2.6a2.3 2.3 0 0 0 0-4.6H13"/>',
    "pencil": '<path d="M17 3a2.8 2.8 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5z"/><path d="M15 5l4 4"/>',
    "stairs": '<path d="M3 20h5v-5h5v-5h5V5h3"/>',
    "users": '<circle cx="9" cy="7" r="4"/><path d="M2 21v-2a4 4 0 0 1 4-4h6a4 4 0 0 1 4 4v2"/><path d="M16 3.1a4 4 0 0 1 0 7.8"/><path d="M22 21v-2a4 4 0 0 0-3-3.9"/>',
    "home": '<path d="M3 10.5L12 3l9 7.5V21H3z"/><path d="M9 21v-6h6v6"/>',
    "check": '<path d="M20 6L9 17l-5-5"/>',
    "layers": '<path d="M12 2l10 5-10 5L2 7z"/><path d="M2 12l10 5 10-5"/><path d="M2 17l10 5 10-5"/>',
    "star": '<path d="M12 2l3.1 6.3 6.9 1-5 4.9 1.2 6.8L12 17.8 5.8 21l1.2-6.8-5-4.9 6.9-1z"/>',
    "chat": '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>',
}
def svg(k, size=40):
    return (f'<svg viewBox="0 0 24 24" width="{size}" height="{size}" fill="none" stroke="currentColor" '
            f'stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">{IC[k]}</svg>')

def hl(t):  # *kata* -> kuning
    out, on = "", False
    for i, p in enumerate(t.split("*")):
        out += (f'<b class="y">{p}</b>' if i % 2 else p)
    return out

els, anims, sfx = [], [], []
track = [10]
def nt():
    track[0] += 1; return track[0]

def SFX(t, f, g):
    sfx.append({"t": round(t, 3), "f": f, "g": g})

# ---------- USP baris (Style 1) ----------
def row(id_, t0, t1, icon, text, tint="gold", top=200, left=70, anim="pop", snd=None):
    els.append(f'<div id="{id_}" class="clip ov" data-start="{t0:.3f}" data-duration="{t1-t0:.3f}" data-track-index="{nt()}" '
               f'style="top:{top}px;left:{left}px"><div class="row" id="{id_}-in"><div class="tile {tint}" id="{id_}-tl">{svg(icon)}</div>'
               f'<div class="rt">{hl(text)}</div></div></div>')
    if anim == "pop":
        anims.append(f'tl.fromTo("#{id_}-in",{{opacity:0,scale:.86,y:16}},{{opacity:1,scale:1,y:0,duration:.38,ease:"back.out(1.6)"}},{t0:.3f});')
    else:  # slide dari kiri
        anims.append(f'tl.fromTo("#{id_}-in",{{opacity:0,x:-60}},{{opacity:1,x:0,duration:.4,ease:"power3.out"}},{t0:.3f});')
    anims.append(f'tl.fromTo("#{id_}-tl",{{rotation:-14,scale:.6}},{{rotation:0,scale:1,duration:.45,ease:"back.out(2.2)"}},{t0+.05:.3f});')
    anims.append(f'tl.to("#{id_}-in",{{opacity:0,y:-10,duration:.22,ease:"power1.in"}},{t1-.24:.3f});')
    if snd: SFX(t0, *snd)

# ---------- HOOK (frame pertama = thumbnail) ----------
els.append(f'<div id="hook" class="clip ov" data-start="0" data-duration="4.05" data-track-index="{nt()}" style="top:164px;left:70px">'
           f'<div class="kick" id="hook-k">SET FLY HIGH · BUKU 1–5</div>'
           f'<div class="ttl" id="hook-1">BELAJAR MEMBACA</div><div class="ttl" id="hook-2">MULA DARI <b class="y">ASAS</b></div></div>')
anims += [
    'tl.set("#hook-k,#hook-1,#hook-2",{opacity:1},0);',  # nampak dari frame 0
    'tl.fromTo("#hook-k",{x:-24},{x:0,duration:.5,ease:"power3.out"},0);',
    'tl.fromTo("#hook-1",{scale:.94},{scale:1,duration:.5,ease:"back.out(1.6)"},0);',
    'tl.fromTo("#hook-2",{scale:.94},{scale:1,duration:.5,ease:"back.out(1.6)"},0.08);',
    'tl.fromTo("#hook-2 .y",{scale:1},{scale:1.14,duration:.16,ease:"power2.out",yoyo:true,repeat:1},1.54);',
    'tl.to("#hook",{opacity:0,y:-10,duration:.22},3.83);',
]
SFX(1.54, "s04", -17)  # boing comel pada "ASAS"

# ---------- USP sepanjang video ----------
row("u1", 4.10, 7.05, "abc", "Bermula daripada *asas membaca*", "gold", snd=("s03", -15))
row("u2", 7.16, 9.05, "pencil", "*Aktiviti latihan* dalam setiap buku", "teal", anim="slide", snd=("s16", -14))
row("u3", 9.46, 14.40, "check", "Belajar sambil *membuat latihan*", "gold", snd=("s07", -16))
row("u4", 18.30, 22.30, "users", "Sesuai latihan bersama *ibu bapa*", "teal", anim="slide", snd=("s03", -15))

# Fly High tag (pil putih + kilauan)
els.append(f'<div id="tagfh" class="clip ov" data-start="22.40" data-duration="3.55" data-track-index="{nt()}" style="top:200px;left:70px">'
           f'<div class="pill" id="tagfh-in">{svg("book",34)}<span>SET FLY HIGH</span><i class="shine" id="tagfh-sh"></i></div>'
           f'<div class="psub" id="tagfh-sub">Mengenal, Membaca &amp; Membunyikan Suku Kata</div></div>')
anims += [
    'tl.fromTo("#tagfh-in",{opacity:0,scale:.7,rotation:-8},{opacity:1,scale:1,rotation:-2,duration:.45,ease:"back.out(2)"},22.40);',
    'tl.fromTo("#tagfh-sh",{x:-140},{x:420,duration:.7,ease:"power2.inOut"},22.85);',
    'tl.fromTo("#tagfh-sub",{opacity:0,y:10},{opacity:1,y:0,duration:.35,ease:"power2.out"},23.94);',
    'tl.to("#tagfh",{opacity:0,y:-10,duration:.22},25.70);',
]
SFX(22.40, "s14", -18)

# 5 TAHAP: tajuk kecil kekal + satu baris buku pada satu masa
els.append(f'<div id="lima" class="clip ov" data-start="26.02" data-duration="14.50" data-track-index="{nt()}" style="top:176px;left:70px">'
           f'<div class="kick" id="lima-k">PEMBELAJARAN BERPERINGKAT</div>'
           f'<div class="ttl sm" id="lima-t"><b class="y">5 TAHAP</b> · BUKU 1–5</div></div>')
anims += [
    'tl.fromTo("#lima-k",{opacity:0,x:-30},{opacity:1,x:0,duration:.4,ease:"power3.out"},26.02);',
    'tl.fromTo("#lima-t",{opacity:0,scale:.8},{opacity:1,scale:1,duration:.42,ease:"back.out(1.8)"},26.20);',
    'tl.to("#lima",{opacity:0,y:-10,duration:.22},40.28);',
]
SFX(26.28, "s04", -18)
BOOKS = [(29.72, 31.78, "1", "Kenal *huruf* &amp; *bunyi*", "gold", ("s16", -14)),
         (31.82, 34.35, "2", "Belajar &amp; *cantum suku kata*", "teal", ("s17", -14)),
         (34.40, 37.40, "3–4", "Terus *praktis* membaca", "gold", ("s18", -14)),
         (37.44, 40.50, "5", "Baca *ayat, cerita &amp; dialog*", "teal", ("s19", -14))]
for i, (a, b, n, txt, tint, snd) in enumerate(BOOKS):
    id_ = f"bk{i}"
    els.append(f'<div id="{id_}" class="clip ov" data-start="{a:.3f}" data-duration="{b-a:.3f}" data-track-index="{nt()}" style="top:318px;left:70px">'
               f'<div class="row" id="{id_}-in"><div class="tile {tint} num" id="{id_}-tl"><small>BUKU</small>{n}</div>'
               f'<div class="rt">{hl(txt)}</div></div></div>')
    anims += [f'tl.fromTo("#{id_}-in",{{opacity:0,x:-50}},{{opacity:1,x:0,duration:.36,ease:"power3.out"}},{a:.3f});',
              f'tl.fromTo("#{id_}-tl",{{scale:.5,rotation:-20}},{{scale:1,rotation:0,duration:.45,ease:"back.out(2.4)"}},{a+.04:.3f});',
              f'tl.to("#{id_}-in",{{opacity:0,x:40,duration:.2,ease:"power1.in"}},{b-.2:.3f});']
    SFX(a, *snd)

# ---------- KELEBIHAN (Style 1: background blur + kad) ----------
K0, K1 = 40.62, 43.66
els.append(f'<div id="kel" class="clip ov" data-start="{K0}" data-duration="{K1-K0:.2f}" data-track-index="{nt()}" style="top:520px;left:96px">'
           f'<div class="kick big" id="kel-k">SET FLY HIGH BUKU 1–5</div>'
           f'<div class="ttl xl" id="kel-t">KELEBIHAN <b class="y">DIA</b></div>'
           f'<div class="pill sm" id="kel-p">{svg("book",30)}<span>BUKU LATIHAN MEMBACA</span><i class="shine" id="kel-sh"></i></div>'
           + "".join(f'<div class="row kr" id="kel-r{i}"><div class="tile {tn}" id="kel-r{i}-tl">{svg(ic)}</div><div class="rt">{hl(tx)}</div></div>'
                     for i, (ic, tn, tx) in enumerate([("stairs", "gold", "Belajar *langkah demi langkah*"),
                                                        ("layers", "teal", "*5 tahap*, set lengkap"),
                                                        ("home", "gold", "Latihan membaca *di rumah*")]))
           + '<i class="spk" id="sp0" style="left:560px;top:40px"></i><i class="spk" id="sp1" style="left:610px;top:118px"></i>'
             '<i class="spk" id="sp2" style="left:-34px;top:96px"></i></div>')
anims += [
    f'tl.to("#bg",{{filter:"blur(16px) brightness(.62)",scale:1.06,duration:.45,ease:"power2.out"}},{K0});',
    f'tl.to("#bg",{{filter:"blur(0px) brightness(1)",scale:1,duration:.4,ease:"power2.inOut"}},{K1-.35:.2f});',
    f'tl.fromTo("#kel-k",{{opacity:0,y:12}},{{opacity:1,y:0,duration:.35,ease:"power2.out"}},{K0+.10:.2f});',
    f'tl.fromTo("#kel-t",{{opacity:0,scale:.82}},{{opacity:1,scale:1,duration:.45,ease:"back.out(1.8)"}},{K0+.22:.2f});',
    f'tl.fromTo("#kel-p",{{opacity:0,scale:.7,rotation:-8}},{{opacity:1,scale:1,rotation:-2,duration:.42,ease:"back.out(2)"}},{K0+.55:.2f});',
    f'tl.fromTo("#kel-sh",{{x:-140}},{{x:520,duration:.7,ease:"power2.inOut"}},{K0+1.0:.2f});',
]
for i in range(3):
    t = K0 + .95 + i * .42
    anims += [f'tl.fromTo("#kel-r{i}",{{opacity:0,x:-50}},{{opacity:1,x:0,duration:.36,ease:"power3.out"}},{t:.2f});',
              f'tl.fromTo("#kel-r{i}-tl",{{scale:.5,rotation:-20}},{{scale:1,rotation:0,duration:.45,ease:"back.out(2.4)"}},{t+.04:.2f});']
    SFX(t, ["s16", "s17", "s18"][i], -15)
for i in range(3):
    anims.append(f'tl.fromTo("#sp{i}",{{scale:0,rotation:0,opacity:1}},{{scale:1,rotation:90,duration:.35,ease:"back.out(2)",yoyo:true,repeat:3,repeatDelay:.15}},{K0+.4+i*.25:.2f});')
anims.append(f'tl.to("#kel",{{opacity:0,duration:.28}},{K1-.3:.2f});')
SFX(K0 + .22, "s14", -16)   # chime pada tajuk KELEBIHAN
SFX(K0, "s13", -20)

# ---------- CTA ----------
row("u5", 43.74, 46.20, "home", "Bahan *latihan membaca* di rumah", "teal", snd=("s03", -15))
els.append(f'<div id="end" class="clip ov" data-start="46.28" data-duration="{DUR-46.28:.2f}" data-track-index="{nt()}" style="top:176px;left:70px">'
           f'<div class="kick" id="end-k">IBU AYAH,</div>'
           f'<div class="ttl" id="end-t">DAPATKAN SET <b class="y">FLY HIGH</b></div>'
           f'<div class="pill sm" id="end-p">{svg("book",30)}<span>BUKU 1 – 5</span><i class="shine" id="end-sh"></i></div>'
           '<i class="spk" id="sp3" style="left:600px;top:20px"></i><i class="spk" id="sp4" style="left:650px;top:96px"></i></div>')
anims += [
    'tl.fromTo("#end-k",{opacity:0,x:-30},{opacity:1,x:0,duration:.35,ease:"power3.out"},46.28);',
    'tl.fromTo("#end-t",{opacity:0,scale:.8},{opacity:1,scale:1,duration:.45,ease:"back.out(1.8)"},46.40);',
    'tl.fromTo("#end-p",{opacity:0,scale:.7,rotation:-8},{opacity:1,scale:1,rotation:-2,duration:.42,ease:"back.out(2)"},47.20);',
    'tl.fromTo("#end-sh",{x:-140},{x:400,duration:.7,ease:"power2.inOut"},47.70);',
    'tl.fromTo("#sp3",{scale:0,opacity:1},{scale:1,rotation:90,duration:.35,ease:"back.out(2)",yoyo:true,repeat:3,repeatDelay:.15},46.7);',
    'tl.fromTo("#sp4",{scale:0,opacity:1},{scale:1,rotation:90,duration:.35,ease:"back.out(2)",yoyo:true,repeat:3,repeatDelay:.15},46.95);',
]
SFX(46.40, "s00", -17)
SFX(47.20, "s07", -16)

# ---------- subtitle ----------
for i, (a, b, t) in enumerate(SUBS):
    id_ = f"sb{i}"
    els.append(f'<div id="{id_}" class="clip sub" data-start="{a:.3f}" data-duration="{b-a:.3f}" data-track-index="{nt()}">'
               f'<span id="{id_}-in">{hl(t)}</span></div>')
    if i == 0:
        anims.append(f'tl.set("#{id_}-in",{{opacity:1}},0);')
    else:
        anims.append(f'tl.fromTo("#{id_}-in",{{opacity:0,scale:.9,y:8}},{{opacity:1,scale:1,y:0,duration:.16,ease:"back.out(1.6)"}},{a:.3f});')

# ---------- kamera: Ken Burns halus + transition lembut + zoom punch ----------
edges = [0.0] + CUTS + [DUR]
for i in range(len(edges) - 1):
    a, b = edges[i], edges[i + 1]
    if b - a < 0.05: continue
    s0, s1 = (1.0, 1.045) if i % 2 == 0 else (1.045, 1.0)
    anims.append(f'tl.fromTo("#kb",{{scale:{s0}}},{{scale:{s1},duration:{b-a:.3f},ease:"none",immediateRender:false}},{a:.3f});')
for i, c in enumerate(CUTS):
    anims.append(f'tl.fromTo("#tr",{{filter:"blur(7px)",scale:1.035}},{{filter:"blur(0px)",scale:1,duration:.3,ease:"power2.out",immediateRender:false}},{c:.3f});')
for p in (1.54, 26.48, 42.58):
    anims.append(f'tl.fromTo("#cam",{{scale:1}},{{scale:1.035,duration:.16,ease:"power2.out",yoyo:true,repeat:1,immediateRender:false}},{p});')

# SFX cut: bertukar-tukar, perlahan; langkau jika overlay berbunyi berdekatan
TR = [("s13", -21), ("s20", -19), ("s15", -24)]
k = 0
for c in CUTS:
    if any(abs(s["t"] - c) < 0.35 for s in sfx): continue
    f, g = TR[k % 3]; k += 1
    SFX(c - 0.06, f, g)
sfx.sort(key=lambda s: s["t"])

CSS = """
@font-face{font-family:'Lilita';src:url('assets/LilitaOne.ttf') format('truetype');}
@font-face{font-family:'MontI';src:url('assets/Montserrat-Italic.ttf') format('truetype');font-weight:100 900;font-style:italic;}
*{margin:0;padding:0;box-sizing:border-box;}
html,body{width:1080px;height:1920px;overflow:hidden;background:#111;}
#root{position:relative;width:1080px;height:1920px;overflow:hidden;font-family:'Lilita',sans-serif;color:#fff;}
#cam,#bg,#tr,#kb{position:absolute;inset:0;transform-origin:50% 50%;}
#av{position:absolute;left:0;top:0;width:1080px;height:1920px;object-fit:cover;}
.ov{position:absolute;z-index:20;}
.y{color:#FFC21A;font-weight:inherit;display:inline-block;}
.sh{text-shadow:0 3px 0 rgba(0,0,0,.55),0 0 14px rgba(0,0,0,.55);}
.kick{font-family:'Lilita';font-size:27px;letter-spacing:.09em;color:#FFC21A;text-shadow:0 2px 0 rgba(0,0,0,.6),0 0 12px rgba(0,0,0,.6);margin-bottom:2px;}
.kick.big{font-size:30px;}
.ttl{font-family:'Lilita';font-size:66px;line-height:1.02;white-space:nowrap;transform-origin:0 50%;
  text-shadow:0 4px 0 rgba(0,0,0,.55),0 0 18px rgba(0,0,0,.55);}
.ttl.sm{font-size:50px;}
.ttl.xl{font-size:78px;margin-bottom:22px;}
.row{display:flex;align-items:center;gap:20px;transform-origin:0 50%;}
.row.kr{margin-top:22px;}
.tile{width:80px;height:80px;flex:none;border-radius:20px;display:flex;align-items:center;justify-content:center;
  backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);box-shadow:0 6px 18px rgba(0,0,0,.35);}
.tile.gold{background:rgba(196,150,40,.55);border:2.5px solid rgba(255,214,110,.75);color:#FFE7A0;}
.tile.teal{background:rgba(40,140,150,.55);border:2.5px solid rgba(120,225,232,.75);color:#B9F6FA;}
.tile.num{flex-direction:column;font-size:34px;line-height:.9;color:#fff;}
.tile.num small{font-size:14px;letter-spacing:.08em;opacity:.9;margin-bottom:3px;}
.rt{font-family:'Lilita';font-size:44px;white-space:nowrap;text-shadow:0 3px 0 rgba(0,0,0,.55),0 0 14px rgba(0,0,0,.6);}
.pill{position:relative;overflow:hidden;display:inline-flex;align-items:center;gap:12px;background:#fff;color:#1b1b1b;
  font-family:'Lilita';font-size:40px;padding:10px 26px 10px 20px;border-radius:18px;transform:rotate(-2deg);
  box-shadow:0 8px 22px rgba(0,0,0,.35);}
.pill.sm{font-size:34px;padding:8px 22px 8px 16px;border-radius:16px;margin-top:6px;}
.pill svg{color:#1b1b1b;}
.shine{position:absolute;top:-20px;left:0;width:60px;height:140px;transform:rotate(20deg);
  background:linear-gradient(90deg,rgba(255,255,255,0),rgba(255,230,150,.85),rgba(255,255,255,0));}
.psub{font-family:'Lilita';font-size:32px;margin-top:14px;text-shadow:0 3px 0 rgba(0,0,0,.55),0 0 12px rgba(0,0,0,.6);}
.spk{position:absolute;width:30px;height:30px;transform:scale(0);
  background:#FFC21A;clip-path:polygon(50% 0,61% 39%,100% 50%,61% 61%,50% 100%,39% 61%,0 50%,39% 39%);
  filter:drop-shadow(0 0 6px rgba(255,194,26,.8));}
.sub{position:absolute;left:0;width:1080px;top:1488px;text-align:center;z-index:30;}
.sub span{display:inline-block;max-width:940px;font-family:'MontI';font-style:italic;font-weight:900;font-size:38px;
  letter-spacing:.03em;word-spacing:.12em;line-height:1.18;text-transform:uppercase;
  text-shadow:0 3px 0 rgba(0,0,0,.6),0 0 14px rgba(0,0,0,.65);}
"""

html = f"""<!doctype html>
<html lang="ms">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1080, height=1920" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
<style>{CSS}</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{DUR}" data-width="1080" data-height="1920">
<div id="cam"><div id="bg"><div id="tr"><div id="kb">
<video id="av" class="clip" src="assets/aroll.mp4" data-start="0" data-duration="{DUR}" data-media-start="0" data-track-index="0" muted playsinline></video>
</div></div></div></div>
{chr(10).join(els)}
</div>
<script>
window.__timelines = window.__timelines || {{}};
const tl = gsap.timeline({{paused:true}});
{chr(10).join(anims)}
tl.set({{}},{{}},{DUR});
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""
open(f"{PROJ}/index.html", "w").write(html)
json.dump(sfx, open(f"{PROJ}/sfx.json", "w"), indent=0)
print("ok", len(els), "elements", len(sfx), "sfx", "cuts:", CUTS)
