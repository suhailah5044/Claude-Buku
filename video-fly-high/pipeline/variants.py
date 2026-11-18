#!/usr/bin/env python3
"""Varian Fly High v03-v12 dari footage sama (permintaan: "generate banyak-banyak, hook paling best di depan").

Setiap varian: susunan segmen VO lain (hook kuat di depan), hook text lain, ayat USP lain (3 versi),
animasi masuk lain (pop/slide/drop/zoom), panjang lain. Tulisan kekal gaya Fly High:
Lilita One, USP + subtitle dalam KOTAK KACA BLUR gelap (jelas atas cover warna-warni),
zon teks: USP y~250 (bukan terlalu atas), subtitle y~1390 (bukan terlalu bawah - elak UI TikTok).
Potongan audio dalam senyap sebenar (dicari dengan tenaga RMS, lihat SEG).

Guna:
  python3 pipeline/variants.py prep <footage.mov> [vNN ...]   # videos/vNN/assets/aroll.mp4 + vo.wav
  python3 pipeline/variants.py build [vNN ...]                # videos/vNN/index.html + sfx.json
"""
import os, sys, json, shutil, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(HERE)
sys.path.insert(0, HERE)
SPEED = 1.1
TM = ("zscale=tin=arib-std-b67:pin=bt2020:min=bt2020nc:rin=tv:t=linear:npl=160,format=gbrpf32le,zscale=p=bt709,"
      "tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")
END = 54.0667
# segmen (video_in, audio_in, out) masa asal; potong pada titik paling senyap
SEG = {
    "V0": (0.0, 0.0, 2.595),         # Kita mula kenal vokal. Ada A, E, I, O, U.
    "V1": (2.595, 2.595, 5.385),     # Lepas tu ada latihan kecil, contohnya kat sini dia bagi A.
    "V2": (5.385, 5.385, 7.37),      # So suruh anak kita bulatkan dekat A.
    "V3": (15.47, 15.43, 20.02),     # Pada bahagian dengar dan tunjuk ... cari huruf yang betul.
    "H1": (20.10, 20.02, 24.52),     # Kita tengah belajar membaca, memang kena mula daripada asas ... sangat menarik.
    "F":  (24.70, 24.52, 28.525),    # Ini buku keluaran Fly High, siri Mengenal, Membaca, Membunyikan Suku Kata.
    "T":  (28.525, 28.525, 32.555),  # Ini ada lima tahap tau ... membaca ayat dan cerita.
    "B1": (32.555, 32.555, 35.075),  # Buku satu ni untuk anak kita kenal huruf dan bunyi.
    "B2": (35.075, 35.075, 37.685),  # Buku dua, kita mula belajar dan cantum suku kata.
    "B34": (37.685, 37.685, 41.175), # Masuk buku ketiga dan keempat ... kemahiran membaca.
    "B5": (41.175, 41.175, 44.53),   # Bila masuk buku kelima pula ... ayat, cerita dan dialog.
    "J":  (44.53, 44.53, 48.05),     # Jadi anak kita bukan sekadar kenal huruf ... langkah demi langkah.
    "C1": (48.05, 48.05, 50.915),    # Kalau ibu ayah tengah cari bahan latihan membaca untuk anak,
    "C2": (50.915, 50.915, END),     # ibu ayah boleh dapatkan set Fly High ni (dekat beg kuning saya - suara sahaja)
    "C":  (48.05, 48.05, END),
}
CUTS_ORIG = [1.5333, 5.1667, 6.4, 12.4667, 15.4667, 22.2, 28.8, 30.8333, 33.0, 33.4333, 34.3667, 35.4, 36.4333,
             37.3667, 39.6333, 41.5, 43.3667, 44.3, 45.6, 49.7333, 50.7667, 51.1, 53.8333]

VARS = {  # segmen, (jenis hook = segmen pertama), indeks versi teks
    "v03": ["C1", "T", "B1", "B2", "B34", "B5", "J", "C2"],
    "v04": ["T", "B1", "B2", "B34", "B5", "F", "J", "C"],
    "v05": ["J", "H1", "V0", "V1", "V2", "V3", "F", "C"],
    "v06": ["C1", "H1", "V0", "V1", "V2", "V3", "T", "C2"],
    "v07": ["F", "V0", "V1", "V3", "T", "J", "C"],
    "v08": ["H1", "T", "B1", "B2", "B34", "B5", "J", "C"],
    "v09": ["J", "T", "B1", "B2", "B34", "B5", "C"],
    "v10": ["T", "H1", "V0", "V1", "V3", "J", "C"],
    "v11": ["C1", "J", "F", "T", "B1", "B2", "B34", "B5", "C2"],
    "v12": ["H1", "V0", "V1", "V2", "V3", "F", "T", "J", "C"],
}

def layout(segs):
    """[(nama, vi, ai, ao, final_start)]"""
    out, f = [], 0.0
    for s in segs:
        vi, ai, ao = SEG[s]; out.append((s, vi, ai, ao, f)); f += (ao - ai) / SPEED
    return out, f

def prep(src, vid):
    segs = VARS[vid]; P = f"{PROJ}/videos/{vid}/assets"; os.makedirs(P, exist_ok=True)
    fc = []
    for i, s in enumerate(segs):
        vi, ai, ao = SEG[s]; hold = vi - ai
        pad = f",tpad=start_mode=clone:start_duration={hold:.3f}" if hold > 1e-3 else ""
        fc.append(f"[0:v]trim={vi}:{ao},setpts=PTS-STARTPTS,{TM}{pad}[v{i}]")
        fc.append(f"[0:a]atrim={ai}:{ao},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={ao-ai-0.012:.3f}:d=0.012[a{i}]")
    n = len(segs)
    fc.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[cv][ca]")
    fc.append(f"[cv]setpts=PTS/{SPEED},fps=30[v]")
    voice = ("highpass=f=80,afftdn=nr=8:nf=-42,"
             "equalizer=f=180:t=q:w=1:g=1.5,equalizer=f=3200:t=q:w=1.2:g=2.5,equalizer=f=7000:t=q:w=2:g=-1.5,"
             "deesser=i=0.35,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2")
    fc.append(f"[ca]atempo={SPEED},{voice},aresample=48000[a]")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", ";".join(fc),
                    "-map", "[v]", "-an", "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-pix_fmt", "yuv420p",
                    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709", "-movflags", "+faststart",
                    f"{P}/aroll.mp4", "-map", "[a]", "-ac", "1", f"{P}/vo.wav"], check=True)
    for f in ("LilitaOne.ttf", "Montserrat-Italic.ttf"):
        shutil.copy(f"{PROJ}/assets/{f}", P)
    shutil.copytree(f"{PROJ}/assets/sfx", f"{P}/sfx", dirs_exist_ok=True)
    for f in ("package.json", "hyperframes.json"):
        shutil.copy(f"{PROJ}/{f}", f"{PROJ}/videos/{vid}/")

# ---------- subtitle (masa asal, dari v01: final -> asal) ----------
def _v01_orig(f):
    if f < 4.1818: return 20.02 + f * SPEED
    if f < 22.382: return (f - 4.1818) * SPEED
    return 24.68 + (f - 22.382) * SPEED
from build import SUBS as SUBS_V01, IC, svg, hl  # noqa: E402  (build.py tulis index.html v01 bila diimport - lihat guard)
SUBS = [(_v01_orig(a), _v01_orig(b), t) for a, b, t in SUBS_V01]

# ---------- teks (3 versi) ----------
HOOKS = {
    "C1": [("IBU AYAH,", ["CARI BAHAN", "LATIHAN *MEMBACA*?"]), ("ANAK UMUR 4–6 TAHUN?", ["BAHAN LATIHAN", "*MEMBACA* DI RUMAH"]),
           ("IBU AYAH, TENGAH CARI", ["BUKU LATIHAN", "*MEMBACA* ANAK?"])],
    "T":  [("SET FLY HIGH · BUKU 1–5", ["*5 TAHAP*", "BELAJAR MEMBACA"]), ("DARI KENAL HURUF", ["SAMPAI BACA", "*AYAT & CERITA*"]),
           ("BELAJAR MEMBACA", ["ADA *5 TAHAP*", "DALAM 1 SET"])],
    "J":  [("SET FLY HIGH · BUKU 1–5", ["BUKAN SEKADAR", "KENAL *HURUF*"]), ("ANAK BELAJAR MEMBACA", ["*LANGKAH*", "DEMI LANGKAH"]),
           ("BUKU LATIHAN MEMBACA", ["BUKAN SEKADAR", "KENAL *HURUF*"])],
    "H1": [("SET FLY HIGH · BUKU 1–5", ["BELAJAR MEMBACA", "MULA DARI *ASAS*"]), ("NAK AJAR ANAK MEMBACA?", ["MULA DARI *ASAS*"]),
           ("BELAJAR MEMBACA", ["KENA MULA", "DARI *ASAS*"])],
    "F":  [("SET FLY HIGH · BUKU 1–5", ["MENGENAL, MEMBACA &", "MEMBUNYIKAN *SUKU KATA*"]), ("BUKU 1–5", ["SET *FLY HIGH*", "UNTUK ANAK 4–6 TAHUN"]),
           ("SET FLY HIGH", ["BELAJAR *SUKU KATA*", "DARI ASAS"])],
}
HOOK_KEY = {"C1": 1.05, "T": 0.75, "J": 1.0, "H1": 1.2, "F": 1.5}  # saat (asal, dari mula segmen) zoom punch
USP = {  # segmen: (ikon, [3 versi]); masa mula relatif (asal)
    "V0": ("abc", 0.0, ["Bermula daripada *asas membaca*", "Mula dari *asas*: kenal vokal", "Belajar membaca *dari asas*"]),
    "V1": ("pencil", 0.15, ["*Aktiviti latihan* dalam setiap buku", "Ada *latihan* dalam setiap buku", "Belajar sambil *buat latihan*"]),
    "V2": ("check", 0.3, ["Belajar sambil *membuat latihan*", "Anak *bulatkan* huruf yang betul", "Aktiviti *bulatkan huruf*"]),
    "V3": ("users", 0.1, ["Sesuai latihan bersama *ibu bapa*", "Ibu ayah sebut, *anak cari*", "Belajar *bersama ibu bapa*"]),
    "H1": ("abc", 0.2, ["Bermula daripada *asas membaca*", "Belajar membaca *dari asas*", "Mula dari *asas*"]),
    "C1": ("home", 0.1, ["Bahan *latihan membaca* di rumah", "Latihan membaca *di rumah*", "Bantu anak *bina asas membaca*"]),
}
BOOKROWS = {"B1": ("1", ["Kenal *huruf* &amp; *bunyi*", "Kenal *huruf dan bunyi*", "*Huruf* &amp; *bunyi*"]),
            "B2": ("2", ["Belajar &amp; *cantum suku kata*", "*Cantum suku kata*", "Mula *cantum suku kata*"]),
            "B34": ("3–4", ["Terus *praktis* membaca", "*Praktis* kemahiran membaca", "Latih *kemahiran membaca*"]),
            "B5": ("5", ["Baca *ayat, cerita &amp; dialog*", "*Ayat, cerita &amp; dialog*", "Mula baca *ayat &amp; cerita*"])}
KEL = [[("stairs", "gold", "Belajar *langkah demi langkah*"), ("layers", "teal", "*5 tahap*, set lengkap"), ("home", "gold", "Latihan membaca *di rumah*")],
       [("abc", "gold", "Mula dari *asas membaca*"), ("stairs", "teal", "*Berperingkat*, Buku 1–5"), ("pencil", "gold", "*Aktiviti latihan* setiap buku")],
       [("layers", "teal", "*Lima buku* dalam satu set"), ("pencil", "gold", "Belajar sambil *buat latihan*"), ("users", "teal", "Sesuai bersama *ibu bapa*")]]
ENDS = [("IBU AYAH,", "DAPATKAN SET *FLY HIGH*", "BUKU 1 – 5"), ("JOM MULA DARI ASAS", "SET *FLY HIGH*", "BUKU 1 – 5"),
        ("SESUAI UMUR 4–6 TAHUN", "SET *FLY HIGH*", "LIMA BUKU SATU SET")]
ANIMS = ["pop", "slide", "drop", "zoom"]
TOP, HOOKTOP, SUBTOP, KELTOP = 252, 232, 1392, 560

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
.kick{font-size:27px;letter-spacing:.09em;color:#FFC21A;text-shadow:0 2px 0 rgba(0,0,0,.6),0 0 12px rgba(0,0,0,.6);margin-bottom:2px;}
.kick.big{font-size:30px;}
.ttl{font-size:66px;line-height:1.02;white-space:nowrap;transform-origin:0 50%;text-shadow:0 4px 0 rgba(0,0,0,.55),0 0 18px rgba(0,0,0,.55);}
.ttl.sm{font-size:50px;}
.ttl.xl{font-size:78px;margin-bottom:22px;}
.gl{background:rgba(18,18,22,.42);backdrop-filter:blur(18px) saturate(1.2);-webkit-backdrop-filter:blur(18px) saturate(1.2);
  border:1.5px solid rgba(255,255,255,.22);box-shadow:0 10px 28px rgba(0,0,0,.28);border-radius:24px;}
.gl.box{display:inline-block;padding:14px 28px 18px;}
.row{display:flex;align-items:center;gap:20px;transform-origin:0 50%;}
.row.gl{display:inline-flex;padding:10px 28px 10px 10px;}
.row.kr{margin-top:16px;}
.tile{width:72px;height:72px;flex:none;border-radius:17px;display:flex;align-items:center;justify-content:center;box-shadow:0 6px 18px rgba(0,0,0,.3);}
.tile.gold{background:rgba(196,150,40,.6);border:2.5px solid rgba(255,214,110,.8);color:#FFE7A0;}
.tile.teal{background:rgba(40,140,150,.6);border:2.5px solid rgba(120,225,232,.8);color:#B9F6FA;}
.tile.num{flex-direction:column;font-size:32px;line-height:.9;color:#fff;}
.tile.num small{font-size:13px;letter-spacing:.08em;opacity:.9;margin-bottom:3px;}
.rt{font-size:44px;white-space:nowrap;text-shadow:0 3px 0 rgba(0,0,0,.55),0 0 14px rgba(0,0,0,.6);}
.pill{position:relative;overflow:hidden;display:inline-flex;align-items:center;gap:12px;background:#fff;color:#1b1b1b;
  font-size:40px;padding:10px 26px 10px 20px;border-radius:18px;transform:rotate(-2deg);box-shadow:0 8px 22px rgba(0,0,0,.35);}
.pill.sm{font-size:34px;padding:8px 22px 8px 16px;border-radius:16px;margin-top:6px;}
.shine{position:absolute;top:-20px;left:0;width:60px;height:140px;transform:rotate(20deg);
  background:linear-gradient(90deg,rgba(255,255,255,0),rgba(255,230,150,.85),rgba(255,255,255,0));}
.psub{font-size:32px;margin-top:12px;display:inline-block;padding:8px 20px;border-radius:16px;text-shadow:0 2px 0 rgba(0,0,0,.5);}
.spk{position:absolute;width:30px;height:30px;transform:scale(0);background:#FFC21A;
  clip-path:polygon(50% 0,61% 39%,100% 50%,61% 61%,50% 100%,39% 61%,0 50%,39% 39%);filter:drop-shadow(0 0 6px rgba(255,194,26,.8));}
.sub{position:absolute;left:0;width:1080px;top:SUBTOPpx;text-align:center;z-index:30;}
.sub span{display:inline-block;max-width:940px;font-family:'MontI';font-style:italic;font-weight:900;font-size:36px;
  letter-spacing:.03em;word-spacing:.12em;line-height:1.18;text-transform:uppercase;padding:9px 22px 11px;border-radius:18px;
  text-shadow:0 2px 0 rgba(0,0,0,.55),0 0 10px rgba(0,0,0,.45);}
""".replace("SUBTOP", str(SUBTOP))

def build(vid):
    segs = VARS[vid]; k = int(vid[1:]) % 3; L, DUR = layout(segs)
    DUR = round(DUR, 3)
    def F(t, seg):  # masa asal dalam segmen -> final
        for s, vi, ai, ao, f0 in L:
            if s == seg: return f0 + (t - ai) / SPEED
    def segrange(seg):
        for s, vi, ai, ao, f0 in L:
            if s == seg: return f0, f0 + (ao - ai) / SPEED
    els, anims, sfx = [], [], []
    tr = [10]
    def nt(): tr[0] += 1; return tr[0]
    def SFX(t, f, g): sfx.append({"t": round(t, 3), "f": f, "g": g})
    an_i = [k]
    def enter(sel, t0):
        a = ANIMS[an_i[0] % 4]; an_i[0] += 1
        if a == "pop":   anims.append(f'tl.fromTo("{sel}",{{opacity:0,scale:.86,y:16}},{{opacity:1,scale:1,y:0,duration:.38,ease:"back.out(1.6)"}},{t0:.3f});')
        if a == "slide": anims.append(f'tl.fromTo("{sel}",{{opacity:0,x:-70}},{{opacity:1,x:0,duration:.4,ease:"power3.out"}},{t0:.3f});')
        if a == "drop":  anims.append(f'tl.fromTo("{sel}",{{opacity:0,y:-40}},{{opacity:1,y:0,duration:.45,ease:"bounce.out"}},{t0:.3f});')
        if a == "zoom":  anims.append(f'tl.fromTo("{sel}",{{opacity:0,scale:1.35,filter:"blur(8px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:.36,ease:"expo.out"}},{t0:.3f});')
    POPS = [("s03", -15), ("s16", -14), ("s07", -16), ("s17", -14), ("s18", -14), ("s19", -14)]
    pi = [k]
    def pop(): p = POPS[pi[0] % len(POPS)]; pi[0] += 1; return p
    def row(id_, t0, t1, icon, text, tint, top=TOP, num=None):
        tile = (f'<div class="tile {tint} num" id="{id_}-tl"><small>BUKU</small>{num}</div>' if num else
                f'<div class="tile {tint}" id="{id_}-tl">{svg(icon)}</div>')
        els.append(f'<div id="{id_}" class="clip ov" data-start="{t0:.3f}" data-duration="{t1-t0:.3f}" data-track-index="{nt()}" '
                   f'style="top:{top}px;left:70px"><div class="row gl" id="{id_}-in">{tile}<div class="rt">{hl(text)}</div></div></div>')
        enter(f"#{id_}-in", t0)
        anims.append(f'tl.fromTo("#{id_}-tl",{{rotation:-14,scale:.6}},{{rotation:0,scale:1,duration:.45,ease:"back.out(2.2)"}},{t0+.05:.3f});')
        anims.append(f'tl.to("#{id_}-in",{{opacity:0,y:-10,duration:.2,ease:"power1.in"}},{t1-.22:.3f});')
        SFX(t0, *pop())
    tints = ["gold", "teal"]
    first = segs[0]
    # ---- HOOK ----
    a0, a1 = segrange(first)
    hk = [v for v in VARS if VARS[v][0] == first].index(vid) % 3  # versi hook berbeza antara varian hook sama
    kick, lines = HOOKS[first][hk]
    hk_end = a1 - 0.05
    els.append(f'<div id="hook" class="clip ov" data-start="0" data-duration="{hk_end:.3f}" data-track-index="{nt()}" style="top:{HOOKTOP}px;left:70px">'
               f'<div class="gl box" id="hook-g"><div class="kick" id="hook-k">{kick}</div>'
               + "".join(f'<div class="ttl" id="hook-{i}">{hl(l)}</div>' for i, l in enumerate(lines)) + '</div></div>')
    anims.append('tl.set("#hook-g,#hook-k' + "".join(f',#hook-{i}' for i in range(len(lines))) + '",{opacity:1},0);')
    anims.append('tl.fromTo("#hook-k",{x:-24},{x:0,duration:.5,ease:"power3.out"},0);')
    for i in range(len(lines)):
        anims.append(f'tl.fromTo("#hook-{i}",{{scale:.94}},{{scale:1,duration:.5,ease:"back.out(1.6)"}},{.08*i:.2f});')
    pk = min(a0 + HOOK_KEY[first] / SPEED, a1 - .4)
    anims.append(f'tl.fromTo("#hook .y",{{scale:1}},{{scale:1.14,duration:.16,ease:"power2.out",yoyo:true,repeat:1}},{pk:.2f});')
    anims.append(f'tl.to("#hook",{{opacity:0,y:-10,duration:.22}},{hk_end-.24:.3f});')
    SFX(pk, "s04", -17)
    punches = [pk]
    # ---- kad kelebihan: pada J (bukan hook), jika J hook -> pada F ----
    kel_seg = "J" if (first != "J" and "J" in segs) else ("F" if "F" in segs and first != "F" else None)
    # ---- overlay setiap segmen ----
    bk_list = [s for s in segs[1:] if s in BOOKROWS] + ([] if first != "T" else [])
    for idx, s in enumerate(segs):
        if idx == 0: continue
        s0, s1 = segrange(s)
        if s == kel_seg:
            K0, K1 = s0 + .02, s1 - .02
            rows = KEL[k]
            els.append(f'<div id="kel" class="clip ov" data-start="{K0:.3f}" data-duration="{K1-K0:.3f}" data-track-index="{nt()}" style="top:{KELTOP}px;left:96px">'
                       f'<div class="kick big" id="kel-k">SET FLY HIGH BUKU 1–5</div><div class="ttl xl" id="kel-t">KELEBIHAN <b class="y">DIA</b></div>'
                       f'<div class="pill sm" id="kel-p">{svg("book",30)}<span>BUKU LATIHAN MEMBACA</span><i class="shine" id="kel-sh"></i></div><br>'
                       + "".join(f'<div class="row kr gl" id="kel-r{i}"><div class="tile {tn}" id="kel-r{i}-tl">{svg(ic)}</div><div class="rt">{hl(tx)}</div></div><br>'
                                 for i, (ic, tn, tx) in enumerate(rows))
                       + '<i class="spk" id="sp0" style="left:560px;top:40px"></i><i class="spk" id="sp1" style="left:610px;top:118px"></i>'
                         '<i class="spk" id="sp2" style="left:-34px;top:96px"></i></div>')
            anims += [f'tl.to("#bg",{{filter:"blur(16px) brightness(.62)",scale:1.06,duration:.45,ease:"power2.out"}},{K0:.3f});',
                      f'tl.to("#bg",{{filter:"blur(0px) brightness(1)",scale:1,duration:.35,ease:"power2.inOut"}},{K1-.33:.3f});',
                      f'tl.fromTo("#kel-k",{{opacity:0,y:12}},{{opacity:1,y:0,duration:.35,ease:"power2.out"}},{K0+.1:.3f});',
                      f'tl.fromTo("#kel-t",{{opacity:0,scale:.82}},{{opacity:1,scale:1,duration:.45,ease:"back.out(1.8)"}},{K0+.22:.3f});',
                      f'tl.fromTo("#kel-p",{{opacity:0,scale:.7,rotation:-8}},{{opacity:1,scale:1,rotation:-2,duration:.42,ease:"back.out(2)"}},{K0+.5:.3f});',
                      f'tl.fromTo("#kel-sh",{{x:-140}},{{x:520,duration:.7,ease:"power2.inOut"}},{K0+.95:.3f});',
                      f'tl.to("#kel",{{opacity:0,duration:.26}},{K1-.28:.3f});']
            for i in range(3):
                t = K0 + .85 + i * .38
                enter(f"#kel-r{i}", t)
                anims.append(f'tl.fromTo("#kel-r{i}-tl",{{scale:.5,rotation:-20}},{{scale:1,rotation:0,duration:.45,ease:"back.out(2.4)"}},{t+.04:.3f});')
                SFX(t, ["s16", "s17", "s18"][i], -15)
            for i in range(3):
                anims.append(f'tl.fromTo("#sp{i}",{{scale:0,rotation:0,opacity:1}},{{scale:1,rotation:90,duration:.35,ease:"back.out(2)",yoyo:true,repeat:3,repeatDelay:.15}},{K0+.4+i*.25:.3f});')
            SFX(K0 + .22, "s14", -16); punches.append(K0 + 1.6)
        elif s in USP:
            ic, rel, txts = USP[s]
            row(f"u{idx}", s0 + rel / SPEED, s1 - .05, ic, txts[k], tints[idx % 2])
        elif s == "F":
            els.append(f'<div id="tagfh" class="clip ov" data-start="{s0+.02:.3f}" data-duration="{s1-s0-.07:.3f}" data-track-index="{nt()}" style="top:{TOP}px;left:70px">'
                       f'<div class="pill" id="tagfh-in">{svg("book",34)}<span>SET FLY HIGH</span><i class="shine" id="tagfh-sh"></i></div><br>'
                       f'<div class="psub gl" id="tagfh-sub">Mengenal, Membaca &amp; Membunyikan Suku Kata</div></div>')
            anims += [f'tl.fromTo("#tagfh-in",{{opacity:0,scale:.7,rotation:-8}},{{opacity:1,scale:1,rotation:-2,duration:.45,ease:"back.out(2)"}},{s0+.02:.3f});',
                      f'tl.fromTo("#tagfh-sh",{{x:-140}},{{x:420,duration:.7,ease:"power2.inOut"}},{s0+.5:.3f});',
                      f'tl.fromTo("#tagfh-sub",{{opacity:0,y:10}},{{opacity:1,y:0,duration:.35,ease:"power2.out"}},{s0+1.4:.3f});',
                      f'tl.to("#tagfh",{{opacity:0,y:-10,duration:.22}},{s1-.3:.3f});']
            SFX(s0 + .02, "s14", -18)
        elif s in ("C2", "C"):
            e0 = F(50.915 + .05, s) if s == "C" else s0 + .05
            if s == "C":  # bahagian "kalau ibu ayah cari bahan" -> USP rumah dulu
                ic, rel, txts = USP["C1"]; row(f"u{idx}", s0 + .1, e0 - .08, ic, txts[k], tints[idx % 2])
            kk, tt, pp = ENDS[k]
            els.append(f'<div id="end" class="clip ov" data-start="{e0:.3f}" data-duration="{DUR-e0:.3f}" data-track-index="{nt()}" style="top:{HOOKTOP}px;left:70px">'
                       f'<div class="gl box" id="end-g"><div class="kick" id="end-k">{kk}</div><div class="ttl" id="end-t">{hl(tt)}</div></div><br>'
                       f'<div class="pill sm" id="end-p">{svg("book",30)}<span>{pp}</span><i class="shine" id="end-sh"></i></div>'
                       '<i class="spk" id="sp3" style="left:600px;top:20px"></i><i class="spk" id="sp4" style="left:650px;top:96px"></i></div>')
            enter("#end-g", e0)
            anims += [f'tl.fromTo("#end-t",{{opacity:0,scale:.8}},{{opacity:1,scale:1,duration:.45,ease:"back.out(1.8)"}},{e0+.12:.3f});',
                      f'tl.fromTo("#end-p",{{opacity:0,scale:.7,rotation:-8}},{{opacity:1,scale:1,rotation:-2,duration:.42,ease:"back.out(2)"}},{e0+.9:.3f});',
                      f'tl.fromTo("#end-sh",{{x:-140}},{{x:400,duration:.7,ease:"power2.inOut"}},{e0+1.4:.3f});',
                      f'tl.fromTo("#sp3",{{scale:0,opacity:1}},{{scale:1,rotation:90,duration:.35,ease:"back.out(2)",yoyo:true,repeat:3,repeatDelay:.15}},{e0+.4:.3f});',
                      f'tl.fromTo("#sp4",{{scale:0,opacity:1}},{{scale:1,rotation:90,duration:.35,ease:"back.out(2)",yoyo:true,repeat:3,repeatDelay:.15}},{e0+.65:.3f});']
            SFX(e0 + .12, "s00", -17); SFX(e0 + .9, "s07", -16)
    # ---- 5 TAHAP: header + baris buku (satu pada satu masa) ----
    run = [s for s in segs if s in ("T", "B1", "B2", "B34", "B5")]
    if run:
        hs = [s for s in run if not (s == "T" and first == "T")]
        if hs:
            h0 = segrange(hs[0])[0]; h1 = segrange(hs[-1])[1]
            # header hanya jika segmen berturutan
            els.append(f'<div id="lima" class="clip ov" data-start="{h0+.02:.3f}" data-duration="{h1-h0-.06:.3f}" data-track-index="{nt()}" style="top:{HOOKTOP}px;left:70px">'
                       f'<div class="gl box" id="lima-g"><div class="kick" id="lima-k">PEMBELAJARAN BERPERINGKAT</div>'
                       f'<div class="ttl sm" id="lima-t"><b class="y">5 TAHAP</b> · BUKU 1–5</div></div></div>')
            enter("#lima-g", h0 + .02)
            anims.append(f'tl.to("#lima",{{opacity:0,y:-10,duration:.22}},{h1-.28:.3f});')
            if "T" in hs: punches.append(F(28.525 + .62, "T"))
        for i, s in enumerate([s for s in run if s in BOOKROWS]):
            b0, b1 = segrange(s); n, txts = BOOKROWS[s]
            row(f"bk{i}", b0 + .03, b1 - .04, None, txts[k], tints[i % 2], top=HOOKTOP + 142, num=n)
    # ---- subtitle (dalam kotak kaca) ----
    si = 0
    for s, vi, ai, ao, f0 in L:
        for a, b, t in SUBS:
            if ai - .05 <= a < ao - .1:
                fa = f0 + (max(a, ai) - ai) / SPEED; fb = f0 + (min(b, ao) - ai) / SPEED
                id_ = f"sb{si}"; si += 1
                els.append(f'<div id="{id_}" class="clip sub" data-start="{fa:.3f}" data-duration="{fb-fa:.3f}" data-track-index="{nt()}">'
                           f'<span class="gl" id="{id_}-in">{hl(t)}</span></div>')
                if fa < .05: anims.append(f'tl.set("#{id_}-in",{{opacity:1}},0);')
                else: anims.append(f'tl.fromTo("#{id_}-in",{{opacity:0,scale:.9,y:8}},{{opacity:1,scale:1,y:0,duration:.16,ease:"back.out(1.6)"}},{fa:.3f});')
    # ---- kamera ----
    cuts = set()
    for s, vi, ai, ao, f0 in L:
        if f0 > 0: cuts.add(round(f0, 3))
        for c in CUTS_ORIG:
            if vi + .15 < c < ao - .15: cuts.add(round(f0 + (c - ai) / SPEED, 3))
    cuts = sorted(cuts)
    edges = [0.0] + cuts + [DUR]
    for i in range(len(edges) - 1):
        a, b = edges[i], edges[i + 1]
        s0_, s1_ = (1.0, 1.045) if i % 2 == 0 else (1.045, 1.0)
        anims.append(f'tl.fromTo("#kb",{{scale:{s0_}}},{{scale:{s1_},duration:{b-a:.3f},ease:"none",immediateRender:false}},{a:.3f});')
    for c in cuts:
        anims.append(f'tl.fromTo("#tr",{{filter:"blur(7px)",scale:1.035}},{{filter:"blur(0px)",scale:1,duration:.3,ease:"power2.out",immediateRender:false}},{c:.3f});')
    for p in punches:
        anims.append(f'tl.fromTo("#cam",{{scale:1}},{{scale:1.035,duration:.16,ease:"power2.out",yoyo:true,repeat:1,immediateRender:false}},{p:.3f});')
    TRS = [("s13", -21), ("s20", -19), ("s15", -24)]; j = k
    for c in cuts:
        if any(abs(x["t"] - c) < 0.35 for x in sfx): continue
        f, g = TRS[j % 3]; j += 1; SFX(c - .06, f, g)
    sfx.sort(key=lambda x: x["t"])
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
    P = f"{PROJ}/videos/{vid}"; os.makedirs(P, exist_ok=True)
    open(f"{P}/index.html", "w").write(html)
    json.dump(sfx, open(f"{P}/sfx.json", "w"), indent=0)
    json.dump({"segs": segs, "dur": DUR, "hook": HOOKS[first][hk]}, open(f"{P}/plan.json", "w"), ensure_ascii=False)
    print(vid, f"{DUR:.1f}s", "+".join(segs), "| hook:", " / ".join(HOOKS[first][hk][1]))

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "prep":
        src = sys.argv[2]; vids = sys.argv[3:] or list(VARS)
        for v in vids: prep(src, v); print("prep", v)
    else:
        for v in (sys.argv[2:] or list(VARS)): build(v)
