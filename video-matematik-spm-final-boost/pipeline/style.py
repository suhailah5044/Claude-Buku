#!/usr/bin/env python3
"""Gaya overlay Matematik SPM Final Boost = gaya #13 pengguna (dari Modul Transisi style_v1.py):
kotak GELAP + border kuning mustard #FFC21A, perkataan penting *kuning*, teks putih Montserrat 800/900,
SAIZ KECIL, bunyi 'toing' pada SETIAP kotak/item. Tiada kotak dalam kotak (item = teks + check kuning).
Satu benda atas skrin pada satu masa. Diimport oleh pipeline/build.py."""
import html, re
W, H = 1080, 1920
ACC = "#FFC21A"
DARK = f"background:rgba(16,15,18,.82);border:3.5px solid {ACC};box-shadow:0 12px 34px rgba(0,0,0,.45),0 0 22px rgba(255,194,26,.22);"
SOUND_ALL = None   # varian: 'toing' pada setiap kemasukan
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
ANIM = "pop"   # animasi masuk (peraturan #14: lain setiap video)
ENTRY = {
    "pop":   lambda sel, t, s0: f'tl.fromTo("{sel}",{{opacity:0,scale:{s0},y:30}},{{opacity:1,scale:1,y:0,duration:.45,ease:"back.out(2.2)"}},{t});',
    "slide": lambda sel, t, s0: f'tl.fromTo("{sel}",{{opacity:0,x:-140,skewX:-8}},{{opacity:1,x:0,skewX:0,duration:.42,ease:"power4.out"}},{t});',
    "drop":  lambda sel, t, s0: f'tl.fromTo("{sel}",{{opacity:0,y:-70,rotation:-3}},{{opacity:1,y:0,rotation:0,duration:.55,ease:"bounce.out"}},{t});',
    "zoom":  lambda sel, t, s0: f'tl.fromTo("{sel}",{{opacity:0,scale:1.6,filter:"blur(8px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:.38,ease:"expo.out"}},{t});',
    "flip":  lambda sel, t, s0: f'tl.fromTo("{sel}",{{opacity:0,rotationX:-90,transformPerspective:700,transformOrigin:"50% 0%"}},{{opacity:1,rotationX:0,duration:.5,ease:"back.out(1.6)"}},{t});',
}
def pop_in(sel, t, js, sfx, s0=.55, sound=None, shine=True):
    """Masuk: naik sikit + scale spring + kilauan kaca menyapu. Bunyi hanya jika `sound`."""
    t = round(t, 3)
    sound = SOUND_ALL or sound
    js.append(ENTRY[ANIM](sel, t, s0))
    if sound:
        sfx.append([t, sound])

def build_gfx(els, sid="gfx", t0=0.0, dur=20.0, broll=(), y0=200):
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

