"""Grafik kongsi (disalin dari video-kuasai-algebra/pipeline/build.py)."""
import html, os
W, H = 1080, 1920
ACC = "#FFC21A"
PROJ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# ---------------------------------------------------------------- icons
ICON = {
 "qr": '<rect x="4" y="4" width="16" height="16" rx="2"/><rect x="8" y="8" width="3" height="3"/><rect x="13" y="8" width="3" height="3"/><rect x="8" y="13" width="3" height="3"/><path d="M14 14h2v2"/>',
 "play": '<circle cx="12" cy="12" r="9"/><path d="M10 8.5l6 3.5-6 3.5z" fill="#141414"/>',
 "steps": '<path d="M5 6h3M5 12h3M5 18h3"/><path d="M11 6h8M11 12h8M11 18h8"/>',
 "bolt": '<path d="M13 3L5 13.5h6L10 21l8-10.5h-6z" fill="#141414"/>',
 "repeat": '<path d="M4 12a8 8 0 0 1 13.7-5.6L20 9"/><path d="M20 4v5h-5"/><path d="M20 12a8 8 0 0 1-13.7 5.6L4 15"/><path d="M4 20v-5h5"/>',
 "book": '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/>',
 "bag": '<path d="M5 8h14l-1.2 12.5a1.6 1.6 0 0 1-1.6 1.5H7.8a1.6 1.6 0 0 1-1.6-1.5z"/><path d="M9 10V6.5a3 3 0 0 1 6 0V10"/>',
 "users": '<circle cx="9" cy="8" r="3.2"/><path d="M3 20c0-3.3 2.7-5.5 6-5.5s6 2.2 6 5.5"/><circle cx="17" cy="9" r="2.6"/><path d="M16 14.6c2.8.2 5 2.2 5 5.4"/>',
 "check": '<path d="M5 12.5l4.5 4.5L19 7.5"/>',
 "star": '<path d="M12 3l2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z" fill="#141414"/>',
 "screen": '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M8 20h8M12 16v4"/>',
}
def svg(name):
    return (f'<svg viewBox="0 0 24 24" width="28" height="28" fill="none" stroke="#141414" '
            f'stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round">{ICON[name]}</svg>')

# ---------------------------------------------------------------- scene writer
SCENE_CSS = f"""
#root{{position:absolute;inset:0;font-family:'Montserrat',sans-serif;color:#fff;}}
.clip.slot{{position:absolute;left:0;width:{W}px;text-align:center;}}
.in{{display:inline-block;position:relative;}}
.kick .in{{font-weight:800;font-size:22px;letter-spacing:.2em;padding:7px 18px 7px 22px;border:2px solid {ACC};
  border-radius:999px;background:rgba(0,0,0,.38);}}
.hl .in{{font-weight:900;line-height:1.02;letter-spacing:-.01em;text-shadow:0 6px 28px rgba(0,0,0,.6),0 2px 4px rgba(0,0,0,.5);}}
.hl .ln{{display:block;white-space:nowrap;}}
.w{{display:inline-block;position:relative;margin:0 .12em;isolation:isolate;}}
.bar{{position:absolute;left:-4%;right:-4%;bottom:-.08em;height:.16em;background:{ACC};border-radius:6px;z-index:-1;}}
.chip .in{{display:inline-flex;align-items:center;gap:12px;padding:8px 24px 8px 8px;border-radius:999px;
  background:rgba(16,15,18,.84);border:3px solid {ACC};box-shadow:0 14px 40px rgba(0,0,0,.45);}}
.ico{{width:46px;height:46px;border-radius:50%;background:{ACC};display:flex;align-items:center;justify-content:center;flex:none;}}
.ct{{font-weight:800;font-size:30px;white-space:nowrap;}}
.eq .in{{padding:16px 54px 24px;border-radius:40px;background:rgba(16,15,18,.86);border:4px solid {ACC};
  box-shadow:0 18px 50px rgba(0,0,0,.5);}}
.eq .lab{{display:block;font-weight:800;font-size:28px;letter-spacing:.18em;color:{ACC};margin-bottom:2px;}}
.eq .ex{{display:block;font-weight:900;font-size:104px;line-height:1.05;white-space:nowrap;}}
.hook .in{{padding:22px 40px 28px;border-radius:40px;background:rgba(16,15,18,.88);border:5px solid {ACC};
  box-shadow:0 20px 60px rgba(0,0,0,.55);font-weight:900;line-height:1.04;}}
.hook .ln{{display:block;white-space:nowrap;}}
.hook .lab{{display:block;font-weight:800;font-size:30px;letter-spacing:.16em;color:{ACC};margin-bottom:8px;}}
.work .in{{padding:18px 44px 22px;border-radius:36px;background:rgba(16,15,18,.86);border:4px solid {ACC};
  box-shadow:0 18px 50px rgba(0,0,0,.5);text-align:left;}}
.work .lab{{display:block;font-weight:800;font-size:26px;letter-spacing:.16em;color:{ACC};margin-bottom:6px;text-align:center;}}
.work .row{{display:block;font-weight:800;font-size:64px;line-height:1.18;white-space:nowrap;}}
.grid{{display:grid;grid-template-columns:repeat(2,470px);gap:18px 20px;justify-content:center;}}
.gi{{display:flex;align-items:center;gap:14px;padding:10px 22px 10px 10px;border-radius:999px;background:rgba(16,15,18,.84);
  border:3px solid {ACC};box-shadow:0 10px 30px rgba(0,0,0,.4);}}
.gi .ico{{width:54px;height:54px;}}
.gi .ct{{font-size:34px;}}
.burst{{position:absolute;left:46px;top:50%;width:0;height:0;}}
.burst i{{position:absolute;left:0;top:-3px;width:46px;height:6px;border-radius:3px;background:{ACC};transform-origin:0 50%;}}
"""

def hl_html(i, el):
    words = [w for ln in el["lines"] for w in ln.split(" ")]
    longest = max(len(l) for l in el["lines"])
    fs = el.get("fs") or (64 if len(el["lines"]) == 1 else 58)
    fs = min(fs, int(860 / (longest * 0.72)))
    out, wi = [], 0
    for ln in el["lines"]:
        parts = []
        for w in ln.split(" "):
            bar = f'<span class="bar" id="{i}-bar"></span>' if w == el.get("hi") else ""
            parts.append(f'<span class="w" id="{i}-w{wi}">{bar}{html.escape(w)}</span>')
            wi += 1
        out.append(f'<span class="ln">{" ".join(parts)}</span>')
    top = el.get("top", 200)
    return f'<div class="in" id="{i}-in" style="font-size:{fs}px">{"".join(out)}</div>', top, len(words)

def burst_html(i):
    return f'<div class="burst" id="{i}-burst">' + "".join(
        f'<i style="rotate:{a}deg"></i>' for a in range(0, 360, 45)) + "</div>"

def write_scene(sid, s0, s1, els):
    body, js = [], []
    ins = lambda t: round(t - s0, 3)
    for n, el in enumerate(els):
        i = f"{sid}-{el['k']}{n}"
        st, en = ins(el["s"]), ins(el["e"])
        d = round(en - st, 3)
        k = el["k"]
        if k == "kick":
            body.append(f'<div id="{i}" class="clip slot kick" data-start="{st}" data-duration="{d}" data-track-index="1" style="top:{el.get('top', 150)}px">'
                        f'<div class="in" id="{i}-in">{html.escape(el["text"])}</div></div>')
            js.append(f'tl.fromTo("#{i}-in",{{opacity:0,clipPath:"inset(0 50% 0 50% round 999px)"}},{{opacity:1,clipPath:"inset(0 0% 0 0% round 999px)",duration:.42,ease:"expo.out"}},{st});')
            js.append(f'tl.to("#{i}-in",{{opacity:0,duration:.2,ease:"power2.in"}},{round(en-.22,3)});')
        elif k == "hl":
            inner, top, nw = hl_html(i, el)
            body.append(f'<div id="{i}" class="clip slot hl" data-start="{st}" data-duration="{d}" data-track-index="2" style="top:{top}px">{inner}</div>')
            wt = el.get("wt") or [el["s"] + 0.07 * j for j in range(nw)]
            wt = (wt + [wt[-1] + 0.07 * (j + 1) for j in range(nw)])[:nw]
            for j in range(nw):
                t = round(max(st, min(ins(max(wt[j], el["s"])), en - 0.56)), 3)
                js.append(f'tl.fromTo("#{i}-w{j}",{{opacity:0,y:46,scale:.55,filter:"blur(10px)"}},{{opacity:1,y:0,scale:1,filter:"blur(0px)",duration:.34,ease:"back.out(2.2)"}},{t});')
            if el.get("hi"):
                js.append(f'tl.fromTo("#{i}-bar",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:.38,ease:"expo.out"}},{round(ins(max(wt))+.12,3)});')
            if el.get("punch"):
                js.append(f'tl.fromTo("#{i}-in",{{scale:1.35}},{{scale:1,duration:.38,ease:"expo.out"}},{st});')
            if not el.get("final"):
                for j in range(nw):
                    js.append(f'tl.to("#{i}-w{j}",{{opacity:0,y:-22,filter:"blur(8px)",duration:.16,ease:"power2.in"}},{round(en-.2+0.0*j,3)});')
        elif k == "chip":
            body.append(f'<div id="{i}" class="clip slot chip" data-start="{st}" data-duration="{d}" data-track-index="3" style="top:{el["y"]}px">'
                        f'<div class="in" id="{i}-in">{burst_html(i)}<span class="ico" id="{i}-ico">{svg(el["icon"])}</span>'
                        f'<span class="ct" id="{i}-ct">{html.escape(el["text"])}</span></div></div>')
            js += [f'tl.fromTo("#{i}-in",{{opacity:0,scale:.4,y:30}},{{opacity:1,scale:1,y:0,duration:.42,ease:"back.out(2.4)"}},{st});',
                   f'tl.fromTo("#{i}-ico",{{rotation:-120,scale:.3}},{{rotation:0,scale:1,duration:.5,ease:"back.out(2)"}},{round(st+.05,3)});',
                   f'tl.fromTo("#{i}-ct",{{clipPath:"inset(0 100% 0 0)"}},{{clipPath:"inset(0 0% 0 0)",duration:.4,ease:"power3.out"}},{round(st+.12,3)});',
                   f'tl.fromTo("#{i}-burst i",{{scaleX:0,x:30,opacity:1}},{{scaleX:1,x:58,opacity:0,duration:.5,ease:"expo.out"}},{round(st+.08,3)});',
                   f'tl.to("#{i}-in",{{opacity:0,scale:.85,duration:.2,ease:"power2.in"}},{round(en-.22,3)});']
        elif k == "eq":
            body.append(f'<div id="{i}" class="clip slot eq" data-start="{st}" data-duration="{d}" data-track-index="3" style="top:250px">'
                        f'<div class="in" id="{i}-in">{burst_html(i)}<span class="lab">{html.escape(el["label"])}</span>'
                        f'<span class="ex" id="{i}-ex">{html.escape(el["text"])}</span></div></div>')
            js += [f'tl.fromTo("#{i}-in",{{opacity:0,scale:1.7,filter:"blur(14px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:.34,ease:"expo.out"}},{st});',
                   f'tl.fromTo("#{i}-burst i",{{scaleX:0,x:20,opacity:1}},{{scaleX:1.3,x:70,opacity:0,duration:.55,ease:"expo.out"}},{round(st+.12,3)});',
                   f'tl.to("#{i}-in",{{opacity:0,scale:.9,filter:"blur(8px)",duration:.2,ease:"power2.in"}},{round(en-.22,3)});']
        elif k == "hook":
            longest = max(len(l) for l in el["lines"])
            fs = min(104 if len(el["lines"]) > 1 else 112, int(880 / (longest * 0.70)))
            lines, wi = [], 0
            for ln in el["lines"]:
                ws = []
                for w in ln.split(" "):
                    bar = f'<span class="bar" id="{i}-bar"></span>' if w == el.get("hi") else ""
                    ws.append(f'<span class="w" id="{i}-w{wi}">{bar}{html.escape(w)}</span>'); wi += 1
                lines.append(f'<span class="ln">{" ".join(ws)}</span>')
            lab = f'<span class="lab">{html.escape(el["label"])}</span>' if el.get("label") else ""
            body.append(f'<div id="{i}" class="clip slot hook" data-start="{st}" data-duration="{d}" data-track-index="2" style="top:{el.get("y", 230)}px">'
                        f'<div class="in" id="{i}-in" style="font-size:{fs}px">{lab}{"".join(lines)}</div></div>')
            js.append(f'tl.fromTo("#{i}-in",{{scale:1.32,rotation:-2}},{{scale:1,rotation:0,duration:.45,ease:"back.out(1.8)"}},{st});')
            for j in range(wi):
                js.append(f'tl.fromTo("#{i}-w{j}",{{y:0}},{{y:-10,duration:.12,ease:"power2.out",yoyo:true,repeat:1}},{round(st+.45+.06*j,3)});')
            if el.get("hi"):
                js.append(f'tl.fromTo("#{i}-bar",{{scaleX:0,transformOrigin:"0% 50%"}},{{scaleX:1,duration:.4,ease:"expo.out"}},{round(st+.5,3)});')
            if not el.get("final"):
                js.append(f'tl.to("#{i}-in",{{opacity:0,scale:.9,filter:"blur(8px)",duration:.22,ease:"power2.in"}},{round(en-.24,3)});')
        elif k == "work":
            rows = "".join(f'<span class="row" id="{i}-r{j}">{html.escape(tx)}</span>' for j, (tx, _) in enumerate(el["rows"]))
            body.append(f'<div id="{i}" class="clip slot work" data-start="{st}" data-duration="{d}" data-track-index="3" style="top:220px">'
                        f'<div class="in" id="{i}-in"><span class="lab">{html.escape(el["label"])}</span>{rows}</div></div>')
            js.append(f'tl.fromTo("#{i}-in",{{opacity:0,scale:.6,y:30}},{{opacity:1,scale:1,y:0,duration:.4,ease:"back.out(2)"}},{st});')
            for j, (_, t) in enumerate(el["rows"]):
                js.append(f'tl.fromTo("#{i}-r{j}",{{opacity:0,x:-40,filter:"blur(8px)"}},{{opacity:1,x:0,filter:"blur(0px)",duration:.35,ease:"expo.out"}},{max(st, ins(t))});')
            js.append(f'tl.to("#{i}-in",{{opacity:0,scale:.9,duration:.2,ease:"power2.in"}},{round(en-.22,3)});')
        elif k == "grid":
            items = "".join(f'<div class="gi" id="{i}-g{j}"><span class="ico">{svg(ic)}</span><span class="ct">{html.escape(tx)}</span></div>'
                            for j, (tx, ic, _) in enumerate(el["items"]))
            body.append(f'<div id="{i}" class="clip slot gridw" data-start="{st}" data-duration="{d}" data-track-index="3" style="top:272px">'
                        f'<div class="grid" id="{i}-in">{items}</div></div>')
            for j, (_, _, t) in enumerate(el["items"]):
                js.append(f'tl.fromTo("#{i}-g{j}",{{opacity:0,scale:.3,y:24}},{{opacity:1,scale:1,y:0,duration:.4,ease:"back.out(2.6)"}},{ins(t)});')
            js.append(f'tl.to("#{i}-in",{{opacity:0,y:-16,duration:.22,ease:"power2.in"}},{round(en-.24,3)});')
    doc = f"""<template>
<style>{SCENE_CSS}</style>
<div id="root" data-composition-id="{sid}" data-width="{W}" data-height="{H}" data-layout-allow-overlap>
{chr(10).join(body)}
</div>
<script>
const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
window.__timelines["{sid}"] = tl;
</script>
</template>
"""
    os.makedirs(f"{PROJ}/compositions", exist_ok=True)
    open(f"{PROJ}/compositions/{sid}.html", "w").write(doc)

