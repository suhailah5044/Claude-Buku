#!/usr/bin/env python3
"""Builds 9 hook variants of the Kuasai Algebra edit from the same footage.

Each variant moves one spoken "unit" (a sentence of the final cut) to the very
front as the hook, adds a hook title card, and keeps every other unit in the
original order (the original "kalau anak struggle" opener moves to the CTA,
just before "ibu ayah consider", following the original script). Overlays,
b-roll windows and zoom punches travel with the unit they belong to."""
import copy, json, os, shutil, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.join(HERE, "build.py")
MAIN = os.path.dirname(HERE)         # main project (assets/aroll.mp4 = final cut, broll)
OUT = os.path.join(os.path.dirname(MAIN), "variants")
FPS = 30
fr = lambda t: round(round(t * FPS) / FPS, 4)

# ---- current final timeline (seconds on MAIN/assets/aroll.mp4)
UNITS = [("hook", 0.0, 2.47), ("intro1", 2.47, 5.484), ("intro2", 5.484, 8.662), ("intro3", 8.662, 13.574),
         ("nampak", 13.574, 19.102), ("tek1", 19.102, 24.051), ("tek2", 24.051, 28.481), ("tek3", 28.481, 38.16),
         ("leb1", 38.16, 45.088), ("leb2", 45.088, 48.683), ("leb3", 48.683, 51.343), ("leb4", 51.343, 54.282),
         ("cta1", 54.282, 58.58), ("cta2a", 58.58, 62.733), ("cta2b", 62.733, 68.933)]
UNITS = [(n, fr(a), fr(b)) for n, a, b in UNITS]
UNITS[-1] = (UNITS[-1][0], UNITS[-1][1], 68.933)
U = {n: (a, b) for n, a, b in UNITS}
ORDER = [n for n, _, _ in UNITS]

# ---- the 9 angles: hook unit + hook card (times local to the hook unit)
VARIANTS = [
 dict(id="v02_qr",         unit="leb2",   H=3.5,  lines=["TAK FAHAM", "ALGEBRA?"], hi="ALGEBRA?"),
 dict(id="v03_berbaloi",   unit="cta2b",  H=3.0,  lines=["BUKU NI", "SANGAT BERBALOI"], hi="BERBALOI"),
 dict(id="v04_video",      unit="leb1",   H=2.35, lines=["BUKU ALGEBRA", "ADA VIDEO?!"], hi="VIDEO?!"),
 dict(id="v05_form1_5",    unit="cta1",   H=4.2,  lines=["FORM 1 – FORM 5", "WAJIB TENGOK!"], hi="WAJIB"),
 dict(id="v06_pantas",     unit="tek1",   H=2.4,  lines=["ALGEBRA", "CARA PANTAS!"], hi="PANTAS!"),
 dict(id="v07_semua_topik", unit="tek3",  H=1.45, lines=["SEMUA TOPIK", "DALAM 1 BUKU!"], hi="BUKU!"),
 dict(id="v08_soalan",     unit="intro2", H=3.1,  lines=["5(x − 4) = ?"], label="BOLEH JAWAB TAK?", drop_broll=["b1"]),
 dict(id="v09_sampai_faham", unit="leb3", H=2.6,  lines=["BELAJAR", "SAMPAI FAHAM!"], hi="FAHAM!"),
 dict(id="v10_kelas_online", unit="leb4", H=2.9,  lines=["SIAP ADA", "KELAS ONLINE!"], hi="ONLINE!"),
]

# ---- load the main project's elements in final-cut time
src = open(BUILD).read()
cut = src.index("# ---------------------------------------------------------------- scene writer")
HEAD, WRITER = src[:cut], src[cut:]
G = {"__file__": BUILD}
exec(HEAD, G)
ELS = [el for _, _, _, els in G["SCENES"] for el in els]
BROLL0, PUNCH0, SEGS0 = G["BROLL"], G["PUNCH"], G["segs"]

def unit_of(t):
    for n, a, b in UNITS:
        if a <= t < b: return n
    return UNITS[-1][0]

def plan(v):
    order = [v["unit"]] + [n for n in ORDER if n != v["unit"]]
    if v["unit"] != "hook":                       # original opener joins the CTA
        order.remove("hook"); order.insert(order.index("cta2a"), "hook")
    starts, t = {}, 0.0
    for n in order:
        starts[n] = round(t, 4); t += U[n][1] - U[n][0]
    return order, starts, round(t, 3)

def build(v):
    order, starts, DUR = plan(v)
    hu = v["unit"]
    M = lambda n, t: round(starts[n] + t - U[n][0], 3)
    last = order[-1]
    els = []
    for el in ELS:
        for n in ORDER:                            # split each element into per-unit portions
            a, b = U[n]
            s, e = max(el["s"], a), min(el["e"], b)
            if e - s < 0.05: continue
            ns, ne = M(n, s), M(n, e)
            if n == hu and ns < v["H"]: continue   # hook card owns the opening seconds
            p = copy.deepcopy(el); p["s"], p["e"] = ns, ne
            if s > el["s"] and p["k"] not in ("kick",): p["s"] = ns  # (portion continues mid-element)
            clamp = lambda x: min(max(M(n, min(max(x, a), b)), ns), ne)
            if p.get("wt"): p["wt"] = [clamp(x) for x in p["wt"]]
            if p.get("rows"): p["rows"] = [(tx, clamp(x)) for tx, x in p["rows"]]
            if p.get("items"): p["items"] = [(tx, ic, clamp(x)) for tx, ic, x in p["items"]]
            p.pop("final", None)
            if n == last and b - e < 1.0:
                p["e"], p["final"] = round(DUR - 0.02, 3), True
            els.append(p)
    # merge portions of the same element that stay adjacent (kickers spanning units)
    els.sort(key=lambda p: p["s"]); merged = []
    for p in els:
        q = merged[-1] if merged else None
        if q and q["k"] == p["k"] == "kick" and q.get("text") == p.get("text") and abs(q["e"] - p["s"]) < 0.06:
            q["e"] = p["e"]
        else: merged.append(p)
    els = merged
    hook = dict(k="hook", s=0.0, e=round(v["H"], 3), lines=v["lines"])
    if v.get("hi"): hook["hi"] = v["hi"]
    if v.get("label"): hook["label"] = v["label"]
    els.insert(0, hook)
    # b-roll windows travel with their unit
    broll = []
    for b, f, s, e, ms, kb, o in BROLL0:
        if b in v.get("drop_broll", []): continue
        n = unit_of(s); a, bb = U[n]
        broll.append((b, f, M(n, s), M(n, min(e, bb)), ms, kb, o))
    broll.sort(key=lambda x: x[2])
    punch = sorted([M(unit_of(p), p) for p in PUNCH0 if not (unit_of(p) == hu and M(hu, p) < v["H"])] + [0.45])
    cuts = sorted(set([starts[n] for n in order] + [M(unit_of(sg["start"]), sg["start"]) for sg in SEGS0]))
    segs = [{"start": c, "dur": round((cuts[i + 1] if i + 1 < len(cuts) else DUR) - c, 3)} for i, c in enumerate(cuts)]
    # scenes: split at unit starts that no element straddles
    splits = [0.0] + [starts[n] for n in order[1:] if not any(p["s"] < starts[n] - 1e-3 and p["e"] > starts[n] + 1e-3 for p in els)] + [DUR]
    scenes = []
    for k in range(len(splits) - 1):
        a, b = splits[k], splits[k + 1]
        se = [p for p in els if a - 1e-3 <= p["s"] < b - 1e-3]
        if se: scenes.append((f"{v['id'][:3]}s{k:02d}", a, b, se))
    return order, starts, DUR, scenes, broll, punch, segs

def make_aroll(order, path):
    ins, fc = [], ""
    for k, n in enumerate(order):
        a, b = U[n]; d = b - a
        fc += (f"[0:v]trim=start={a}:end={b},setpts=PTS-STARTPTS[v{k}];"
               f"[0:a]atrim=start={a}:end={b},asetpts=PTS-STARTPTS,afade=t=in:d=0.008,afade=t=out:st={d-0.01:.4f}:d=0.01[a{k}];")
    fc += "".join(f"[v{k}][a{k}]" for k in range(len(order))) + f"concat=n={len(order)}:v=1:a=1[v][a]"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{MAIN}/assets/aroll.mp4", "-filter_complex", fc, "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "medium", "-crf", "15", "-g", "30", "-r", "30", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", path], check=True)

if __name__ == "__main__":
    only = sys.argv[1:]
    for v in VARIANTS:
        if only and v["id"] not in only: continue
        order, starts, DUR, scenes, broll, punch, segs = build(v)
        P = f"{OUT}/{v['id']}"
        if os.path.exists(f"{P}/compositions"): shutil.rmtree(f"{P}/compositions")
        os.makedirs(f"{P}/assets/broll", exist_ok=True)
        for f in os.listdir(f"{MAIN}/assets/broll"):
            dst = f"{P}/assets/broll/{f}"
            if not os.path.exists(dst): os.link(f"{MAIN}/assets/broll/{f}", dst)
        for f in ("hyperframes.json", "package.json", "meta.json"):
            shutil.copy(f"{MAIN}/{f}", P)
        if not os.path.exists(f"{P}/assets/aroll.mp4") or "--reaudio" in os.environ.get("FLAGS", ""):
            make_aroll(order, f"{P}/assets/aroll.mp4")
        G2 = dict(G); G2.update(PROJ=P, SCENES=scenes, BROLL=broll, PUNCH=punch, segs=segs, DUR=DUR)
        exec(WRITER, G2)
        json.dump(dict(order=order, starts=starts, dur=DUR, hook=v), open(f"{P}/variant.json", "w"), ensure_ascii=False, indent=1)
        print(v["id"], DUR, " → ".join(order), "| scenes", len(scenes), "| els", sum(len(s[3]) for s in scenes))
