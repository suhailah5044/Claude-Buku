#!/usr/bin/env python3
"""Bina 21 video pendek (15-20 s) Matematik SPM Final Boost - Cikgu Yasir, sebagai projek HyperFrames.

Setiap video = 1 INTRO (hook) + 1 TENGAH (isi/USP) + 1 CTA (voiceover pengguna, lihat vo.py),
atau Footage.mov (review penuh) + CTA. Tiada talking head: visual = b-roll buku penuh skrin.
- Setiap kali VO sebut topik/benda dalam buku -> shot buku yang sepadan (2-3 s, fade lembut 0.3 s, ken burns perlahan)
- Hook (kotak gaya #13) kelihatan penuh dari frame 0 (thumbnail)
- Caption pendek, satu pada satu masa, kotak gelap + border kuning, bunyi 'toing' setiap kotak
- Teks di ruang kosong (meja marmar), elak y<150 & y>1550, tiada teks 'bakul/beg kuning'
- Zoom punch kecil pada point penting

Guna:  python3 pipeline/build.py [id ...]       -> videos/<id>/ (index.html, compositions/gfx.html, sfx.json, assets/)
"""
import json, os, shutil, subprocess, sys, re
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import style as S
from shots import SHOT, CUES, ALT, STATIC_ALT, HO, KEY, END_HOLD, SHORT_FILL, NO_FIRST, HOLD_MIN, HO_QUICK, INNER, COVER_FRONT_STATIC, MOVES, TRANS, KEYCUES
from captions import CAPS, HOOKS
import variety as V
W, H, FPS = 1080, 1920, 30
VO = json.load(open(f"{HERE}/vo.json"))
GAP = 0.10   # senyap antara unit VO
OUT = f"{PROJ}/videos"
fr = lambda t: round(round(t * FPS) / FPS, 4)
RAWDUR = {"IMG_1390": 9.20, "IMG_1391": 5.87, "IMG_1392": 22.29, "IMG_1393": 28.90, "IMG_1394": 6.25, "IMG_1395": 18.34,
          "IMG_1396": 11.57, "IMG_1397": 8.57, "IMG_1398": 7.23, "IMG_1399": 8.40, "IMG_1400": 13.65, "IMG_1401": 17.96,
          "IMG_1402": 13.44, "IMG_1403": 12.29, "IMG_1404": 12.24, "IMG_1405": 3.67, "IMG_1406": 6.67, "IMG_1407": 5.15,
          "IMG_1408": 5.34, "IMG_1409": 11.69, "footage_hold": 13.37}
SLOW = 2.0   # b-roll slow-mo 0.5x (pengguna: footage nampak laju) -> masa klip x2; SHOT.ms ditulis dalam masa ASAL klip
CLIPDUR = {k + ".mp4": v * SLOW for k, v in RAWDUR.items()}

VIDEOS = [  # (id, [unit...])
    ("v01", ["i_4557", "t_96DE", "c_4EE9"]),
    ("v02", ["i_4557", "t_3454", "c_E3ED"]),
    ("v03", ["i_189E", "t_E6E5", "c_4EE9"]),
    ("v04", ["i_189E", "t_3454", "c_C62F"]),
    ("v05", ["i_235A", "t_96DE", "c_3EF9"]),
    ("v06", ["i_235A", "t_3454", "c_F20C"]),
    ("v07", ["i_2C72", "t_E6E5", "c_3EF9"]),
    ("v08", ["i_2C72", "t_96DE", "c_4EE9"]),
    ("v09", ["i_48FA", "t_96DE", "c_3EF9"]),
    ("v10", ["i_48FA", "t_3454", "c_E3ED"]),
    ("v11", ["i_70D5", "t_96DE", "c_4EE9"]),
    ("v12", ["i_70D5", "t_3454", "c_C62F"]),
    ("v13", ["i_A559", "t_3454", "c_F20C"]),
    ("v14", ["i_A559", "t_E6E5", "c_4EE9"]),
    ("v15", ["i_BD48", "t_3454", "c_4EE9"]),
    ("v16", ["i_BD48", "t_E6E5", "c_3EF9"]),
    ("v17", ["i_C83B", "t_96DE", "c_4EE9"]),
    ("v18", ["i_C83B", "t_3454", "c_3EF9"]),
    ("v19", ["i_EC6D", "t_3454", "c_4EE9"]),
    ("v20", ["i_EC6D", "t_E6E5", "c_4EE9"]),
    ("v21", ["f_full", "c_E3ED"]),
]

def layout(units):
    off, t = {}, 0.0
    for u in units:
        off[u] = fr(t); t = off[u] + VO[u]["dur"] + GAP
    return off, fr(t - GAP + 0.35)   # 0.35 s hujung (CTA kekal sekejap)

def make_vo(units, off, dur, path):
    """VO bercantum (unit + senyap), 48 kHz mono. Loudness akhir dibuat dalam mux.py."""
    import numpy as np, wave
    out = np.zeros(int(dur * 48000) + 4800, np.float32)
    for u in units:
        w = wave.open(f"{PROJ}/assets/vo/{u}.wav"); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        i = int(off[u] * 48000); out[i:i + len(a)] += a[:len(out) - i]
    out = out[:int(dur * 48000)]
    w = wave.open(path, "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(48000)
    w.writeframes((np.clip(out, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()

def occ_of(vid):
    """Kali ke-berapa setiap unit muncul (ikut susunan VIDEOS) -> pilih versi caption/b-roll/hook (peraturan #14)."""
    cnt, res = {}, None
    for v, us in VIDEOS:
        o = {u: cnt.get(u, 0) for u in us}
        for u in us: cnt[u] = cnt.get(u, 0) + 1
        if v == vid: res = o
    return res or {}

def unit_cues(u, o):
    alts = V.CUES_ALT.get(u, [])
    return CUES[u] if o == 0 or not alts else alts[(o - 1) % len(alts)]

def unit_caps(u, o):
    caps = [dict(c) for c in CAPS[u]]
    alts = V.TEXT_ALT.get(u, [])
    if o and alts:
        for c, t in zip(caps, alts[(o - 1) % len(alts)]):
            if t is None: continue
            if c["k"] == "card": c["title"] = t
            else: c["text"] = t
    return caps

def place_shots_v3(cues, dur, vno, end_t, caps=()):
    """Maklum balas pengguna (v01): cover masuk DEPAN, TENGAH, BELAKANG sahaja.
    - DEPAN  : hook = pegang cover lama -> buka (HO); hook pendek = cover statik
    - TENGAH : close-up badge cover bila VO sebut USP (KEY)
    - BELAKANG: CTA akhir = pegang cover
    - lain-lain: ISI buku, banyak angle (12 sudut + gerakan kamera), selak-selak, 1.3-2.4 s setiap shot"""
    S_ = SLOW
    cues = sorted(cues)
    segs, kused = [], set()
    for n, (t, k) in enumerate(cues):
        if k not in KEY or (k == "footage" and t > 0.05): continue
        if k in kused and ALT.get(k) in KEY and ALT.get(k) not in kused: k = ALT[k]
        kused.add(k)
        nxt = next((t2 for t2, k2 in cues[n + 1:] if t2 > t + 0.05), dur)
        w = SHOT[k]["win"]; e = min(nxt, t + max(1.6, min(2.6, (w[1] - w[0]) * S_)), t + (w[1] - w[0]) * S_, dur)
        # caption yang mula semasa shot sebutan ni mesti habis atas shot yang sama (teks = gambar)
        c_in = [c for c in caps if t - 0.15 <= c < min(e - 0.05, t + 0.5)]   # hanya caption yang MULA bersama shot ni
        if c_in:
            c_end = next((c for c in caps if c > max(c_in) + 0.05), dur)
            e = min(max(e, c_end), nxt, t + (w[1] - w[0]) * S_, dur)
        if segs and t < segs[-1][1]: t = segs[-1][1]
        if e - t >= 0.6: segs.append((t, e, k))
    gaps, cur = [], 0.0
    for a, b, k in segs:
        if a - cur > 0.05: gaps.append((cur, a))
        cur = b
    if dur - cur > 0.05: gaps.append((cur, dur))
    out = list(segs); used = set()
    irot = INNER[(vno * 5) % len(INNER):] + INNER[:(vno * 5) % len(INNER)]
    def lim(k):
        h = SHOT[k]; act = (h["act"][1] - h["act"][0]) * S_
        hold = min(HOLD_MIN, (h["act"][0] - h["pre"]) * S_)
        return (act + hold + 0.6 * min(1, (h["post"] - h["act"][1]) / 0.3), min(6.0, (h["post"] - h["pre"]) * S_))
    def prev_file(t):
        p = [x for x in out if x[1] <= t + 0.01]
        return SHOT[max(p, key=lambda x: x[1])[2]]["f"] if p else None
    def inner_fill(a, b):
        G = b - a
        if G < 0.6: return []
        n = max(1, round(G / 1.9)); L = G / n; res = []; pf = prev_file(a)
        for i in range(n):
            k = next((k for k in irot if k not in used and SHOT[k]["f"] != pf), None) or next(k for k in irot if SHOT[k]["f"] != pf)
            used.add(k); pf = SHOT[k]["f"]; res.append((a + i * L, a + (i + 1) * L, k))
        return res
    for a, b in gaps:
        final = b >= dur - 0.01
        e_in = end_t if (final and end_t is not None and a < end_t < b - 1.0) else (a if final else b)
        if final and e_in - a < 1.0 and e_in > a: e_in = a
        if a < 0.05:                                  # DEPAN: cover pegang -> buka
            G = e_in - a
            rot = HO[vno % len(HO):] + HO[:vno % len(HO)]
            k = next((k for k in rot if lim(k)[0] <= G), None)
            if k:
                L = min(lim(k)[1], G)
                if 0 < G - L < 1.3: L = max(lim(k)[0], G - 1.3)
                used.add(k); out.append((a, a + L, k)); out += inner_fill(a + L, e_in)
            elif G >= 1.0:
                k = COVER_FRONT_STATIC[vno % len(COVER_FRONT_STATIC)]; used.add(k); out.append((a, e_in, k))
        else:
            out += inner_fill(a, e_in)
        if final:                                     # BELAKANG: pegang cover
            endh = END_HOLD[vno % len(END_HOLD):] + END_HOLD[:vno % len(END_HOLD)]
            k = next(k for k in endh if k not in used); used.add(k); out.append((e_in, b, k))
    out.sort()
    shots, cnt = [], {}
    for n, (a, b, key) in enumerate(out):
        sh = dict(key=key, s=fr(a), e=(fr(out[n + 1][0]) if n + 1 < len(out) else round(b, 4)), **SHOT[key])
        L = (sh["e"] - sh["s"]) / S_
        if "act" in sh:
            a0, b0 = sh["act"]; end = min(sh["post"], b0 + 0.3)
            st = min(max(sh["pre"], end - L), a0)
        else:
            w0, w1 = sh["win"]; room = max(0.0, (w1 - w0) - L)
            if key in INNER: st = w0 + ((vno * 1.7 + cnt.get(key, 0) * 2.3) % (room + 1e-6))
            else: st = min(max(sh["ms"] + 1.0 * cnt.get(key, 0), w0), max(w0, w1 - L))
        cnt[key] = cnt.get(key, 0) + 1
        sh["ms"] = round(st * S_, 3)
        # gerakan kamera & peralihan (power); badge/cover kekal lembut supaya caption tak kena isi
        if key in INNER: sh["mv"] = MOVES[(n + vno) % len(MOVES)]
        else: sh["mv"] = ({"scale": 1.0}, {"scale": 1.04})
        sh["tr"] = TRANS[(n + vno) % len(TRANS)]
        shots.append(sh)
    return shots

def place_shots_ho(cues, dur, vno, end_t):
    """Pengguna: 'cari footage yang hold lama, slow-mo, dia buka'.
    - shot SEBUTAN (KEY: badge, isi kandungan, Footage) kekal tepat pada cue VO
    - ruang antara = SATU shot panjang PEGANG cover -> BUKA lengkap (HO), dipilih ikut panjang ruang
    - penutup CTA (dari caption akhir) = pegang cover lama, statik
    - ruang terlalu pendek untuk buka = halaman terbuka statik"""
    S_ = SLOW
    cues = sorted(cues)
    segs = []                                   # (s, e, key|None)
    kused = set()
    for n, (t, k) in enumerate(cues):
        if k not in KEY: continue
        if k in kused and ALT.get(k) in KEY and ALT.get(k) not in kused: k = ALT[k]   # sebutan berulang -> shot lain
        kused.add(k)
        nxt = next((t2 for t2, _ in cues[n + 1:] if t2 > t + 0.05), dur)
        w = SHOT[k]["win"]; e = min(nxt, t + (w[1] - w[0]) * S_, dur)
        if segs and t < segs[-1][1]: t = segs[-1][1]
        if e - t >= 1.0: segs.append((t, e, k))
    # ruang umum
    gaps, cur = [], 0.0
    for a, b, k in segs:
        if a - cur > 0.05: gaps.append((cur, a))
        cur = b
    if dur - cur > 0.05: gaps.append((cur, dur))
    rot = HO[vno % len(HO):] + HO[:vno % len(HO)] + HO_QUICK   # utamakan footage yang PEGANG lama dulu
    endh = END_HOLD[vno % len(END_HOLD):] + END_HOLD[:vno % len(END_HOLD)]
    used, out = set(), [(a, b, k) for a, b, k in segs]
    def lim(k):   # (min, maks) tempoh: min = aksi buka + bahagian pegang (jika footage ada pegang), maks 6 s
        h = SHOT[k]; act = (h["act"][1] - h["act"][0]) * S_
        hold = min(HOLD_MIN, (h["act"][0] - h["pre"]) * S_)
        return (act + hold + 0.6 * min(1, (h["post"] - h["act"][1]) / 0.3), min(6.0, (h["post"] - h["pre"]) * S_))
    def fill(a, b):
        G = b - a
        if G < 1.0:                                  # terlalu pendek: panjangkan shot sebelumnya
            if out:
                i = max(range(len(out)), key=lambda i: out[i][1] if out[i][1] <= a + 0.01 else -1)
                out[i] = (out[i][0], b, out[i][2])
            return []
        cands = [k for k in rot if k not in used and not (a < 0.05 and k in NO_FIRST)]
        fit = [k for k in cands if lim(k)[0] <= G <= lim(k)[1]]
        fit = [k for k in fit if k not in HO_QUICK] or ([] if G >= 2.0 else fit)   # buka-terus hanya bila ruang < 2 s
        if fit:
            used.add(fit[0]); return [(a, b, fit[0])]
        hold_c = [k for k in cands if k not in HO_QUICK]
        for pool in (hold_c, cands):              # utamakan footage yang PEGANG lama; buka-terus hanya jika perlu
            for k1 in pool:                       # dua shot pegang->buka (fail berbeza)
                for k2 in pool:
                    if k2 == k1 or SHOT[k2]["f"] == SHOT[k1]["f"]: continue
                    (m1, x1), (m2, x2) = lim(k1), lim(k2)
                    if m1 + m2 <= G <= x1 + x2:
                        L = min(max(G * x1 / (x1 + x2), m1, G - x2), x1, G - m2)
                        used.update({k1, k2}); return [(a, a + L, k1), (a + L, b, k2)]
            for k in pool:                        # satu pegang->buka + halaman statik
                m, x = lim(k)
                if m <= G - 1.0:
                    L = min(x, G - 1.0); used.add(k); return [(a, a + L, k)] + fill(a + L, b)
        for k in SHORT_FILL:                     # halaman terbuka statik
            if k in used: continue
            w = SHOT[k]["win"]; cap = (w[1] - w[0]) * S_
            used.add(k)
            if cap >= G: return [(a, b, k)]
            L = min(cap, G - 1.0)
            return [(a, a + L, k)] + fill(a + L, b)
        return [(a, b, "riffle_a")]
    for a, b in gaps:
        if b >= dur - 0.01 and end_t is not None and a < end_t < b - 1.2:   # penutup: pegang cover lama
            if end_t - a >= 1.0: out += fill(a, end_t)
            else: end_t = a
            k = next(k for k in endh if k not in used); used.add(k); out.append((end_t, b, k))
        elif b >= dur - 0.01:
            k = next(k for k in endh if k not in used); used.add(k); out.append((a, b, k))
        else:
            out += fill(a, b)
    out.sort()
    shots, cnt = [], {}
    for n, (a, b, key) in enumerate(out):
        sh = dict(key=key, s=fr(a), e=(fr(b) if n + 1 < len(out) else round(b, 4)), **SHOT[key])
        if n + 1 < len(out): sh["e"] = fr(out[n + 1][0])
        L = (sh["e"] - sh["s"]) / S_
        if "act" in sh:
            a0, b0 = sh["act"]
            end = min(sh["post"], b0 + 0.3)          # buka habis + rehat sekejap atas halaman terbuka
            st = max(sh["pre"], end - L)
            st = min(st, a0)
        else:
            w0, w1 = sh["win"]
            st = min(max(sh["ms"] + 1.0 * cnt.get(key, 0), w0), max(w0, w1 - L))
        cnt[key] = cnt.get(key, 0) + 1
        sh["ms"] = round(st * S_, 3)
        shots.append(sh)
    return shots

def place_shots(cues, dur):
    """Susun shot ikut cue VO. Pengguna: aksi buka buku MESTI lengkap ("kalau nak buka, bagi buka").
    - shot 'act' main aksi (a..b) sepenuhnya: cue seterusnya ditolak ke belakang sampai aksi habis;
      kalau shot lebih panjang, tambah bahagian tenang pre/post (aksi tetap lengkap)
    - shot 'win' (statik) hanya guna julat statik - tak terkena aksi separuh jalan
    - elak shot/fail sama bersebelahan & berulang (ALT)"""
    S_ = SLOW
    sel, used, cur = [], {}, 0.0
    same = lambda k: sel and SHOT[sel[-1][1]]["f"] == SHOT[k]["f"]
    for n0, (t, key) in enumerate(cues):
        if same(key) or key in used:
            alt, tried = key, 0
            while tried < 4:
                alt = ALT.get(alt); tried += 1
                if not alt: break
                if alt not in used and not same(alt): key = alt; break
        s = round(max(t, cur), 4)
        if s > dur - 1.0: break
        a = SHOT[key].get("act")
        t_next = cues[n0 + 1][0] if n0 + 1 < len(cues) else dur
        if a and n0 + 1 < len(cues) and s + (a[1] - a[0]) * S_ > t_next + 0.8:   # aksi tak sempat habis -> shot statik
            k2 = STATIC_ALT.get(key)
            if k2 and not same(k2): key = k2; a = None
        sel.append([s, key]); used[key] = used.get(key, 0) + 1
        cur = s + ((a[1] - a[0]) * S_ if a else 1.0)
    # had atas tempoh: kalau shot lebih panjang dari julat yang ada, tarik shot seterusnya lebih awal
    for n in range(len(sel) - 1):
        s, key = sel[n]; sh = SHOT[key]
        cap = ((sh["post"] - sh["pre"]) if "act" in sh else (sh["win"][1] - sh["win"][0])) * S_
        if sel[n + 1][0] - s > cap + 0.01 and cap >= 0.6:
            sel[n + 1][0] = round(s + cap, 4)
    shots, cnt = [], {}
    for n, (s, key) in enumerate(sel):
        e = sel[n + 1][0] if n + 1 < len(sel) else dur
        sh = dict(key=key, s=fr(s), e=round(fr(e) if n + 1 < len(sel) else e, 4), **SHOT[key])
        L = (sh["e"] - sh["s"]) / S_      # tempoh dalam masa asal klip
        if "act" in sh:
            a, b = sh["act"]
            st = min(max(b - L, sh["pre"]), a)          # utamakan: aksi habis tepat di hujung shot
            if st + L < b: st = max(sh["pre"], b - L)   # shot pendek (hujung video): mula lewat, tetap habis
        else:
            w0, w1 = sh["win"]
            st = min(max(sh["ms"] + 1.0 * cnt.get(key, 0), w0), max(w0, w1 - L))
        cnt[key] = cnt.get(key, 0) + 1
        sh["ms"] = round(st * S_, 3)
        shots.append(sh)
    return shots

def plan(vid, units):
    off, dur = layout(units)
    OCC = occ_of(vid)
    # ---- shot (b-roll penuh skrin) ikut cue setiap unit
    cues = []
    for u in units:
        for t, key in unit_cues(u, OCC.get(u, 0)):
            cues.append((fr(off[u] + t), key))
    cues.sort()
    cues[0] = (0.0, cues[0][1])
    lastu = units[-1]; lc = unit_caps(lastu, OCC.get(lastu, 0))
    end_t = round(off[lastu] + lc[-1]["s"], 3) if lc else None
    kc = sorted((fr(off[u] + t), k) for u in units for t, k in KEYCUES.get(u, []))   # sebutan sebenar sahaja
    cs = sorted(round(off[u] + c["s"], 3) for u in units for c in unit_caps(u, OCC.get(u, 0)))
    shots = place_shots_v3(kc, dur, int(vid[1:]), end_t, cs)
    # ---- caption
    els = []
    hu = units[0]
    hk = dict(V.HOOK_ALT[hu] if OCC.get(hu, 0) and hu in V.HOOK_ALT else HOOKS[hu]); els.append(dict(k="hook", s=0.0, e=hk.pop("e"), nohide=True, **hk))
    for u in units:
        for c in unit_caps(u, OCC.get(u, 0)):
            c = dict(c); c["s"] = round(off[u] + c["s"], 3)
            if "e" in c: c["e"] = round(off[u] + c["e"], 3)
            if "items" in c: c["items"] = [(tx, round(off[u] + x, 3)) for tx, x in c["items"]]
            els.append(c)
    els.sort(key=lambda c: c["s"])
    for n, c in enumerate(els):   # satu benda pada satu masa: tamat bila yang seterusnya mula
        if "e" not in c or (n + 1 < len(els) and c["e"] > els[n + 1]["s"] - 0.02):
            c["e"] = round(els[n + 1]["s"] - 0.02, 3) if n + 1 < len(els) else dur
    els[-1]["e"] = dur; els[-1]["final"] = True
    for c in els:   # y caption = ruang kosong pada shot semasa caption mula
        if "y" not in c:
            sh = next((s for s in shots if s["s"] <= c["s"] + 0.08 < s["e"]), shots[-1])
            c["y"] = sh.get("cy", 200)
            if c["y"] > 1000 and c["k"] == "card": c["y"] = 1425 if not c.get("items") else 1360
    # caption yang merentas shot dengan ruang kosong lain (atas <-> bawah): pecah, bahagian 2 pindah ke ruang kosong shot baru (tanpa bunyi)
    out = []
    for c in els:
        out.append(c)
        if c["k"] != "cap" or c.get("final") and False: continue
        for sh in shots:
            if c["s"] + 0.3 < sh["s"] < c["e"] - 0.5 and abs(sh.get("cy", 200) - c["y"]) > 100:
                c2 = dict(c); c2["s"] = round(sh["s"] + 0.05, 3); c2["y"] = sh.get("cy", 200); c2["sfx"] = "none"; c2.pop("punch", None)
                c["e"] = round(sh["s"] + 0.02, 3); c.pop("final", None)
                out.append(c2); c = c2
    els = out
    punch = [(round(c["s"] + 0.05, 3), 1.065 if c.get("punch") else 1.035) for c in els if c["s"] > 0.05 and c.get("sfx") != "none"]   # zoom punch setiap caption (power)
    return off, dur, shots, els, punch

def CAPS_PUNCH(u):
    return [c["s"] + 0.05 for c in CAPS[u] if c.get("punch")]

def root_html(dur, shots, punch, vo_src="assets/vo.wav"):
    body, js = [], []
    TRJS = {   # peralihan shot (power): masuk laju atas shot sebelumnya
        "zoomblur": lambda i, t: [f'tl.fromTo("{i}",{{opacity:0,scale:1.35,filter:"blur(14px)"}},{{opacity:1,scale:1,filter:"blur(0px)",duration:.28,ease:"expo.out"}},{t});'],
        "whipL":    lambda i, t: [f'tl.fromTo("{i}",{{opacity:1,x:760,filter:"blur(22px)"}},{{x:0,filter:"blur(0px)",duration:.26,ease:"power3.out"}},{t});'],
        "whipR":    lambda i, t: [f'tl.fromTo("{i}",{{opacity:1,x:-760,filter:"blur(22px)"}},{{x:0,filter:"blur(0px)",duration:.26,ease:"power3.out"}},{t});'],
        "spin":     lambda i, t: [f'tl.fromTo("{i}",{{opacity:0,rotation:-9,scale:1.4,filter:"blur(10px)"}},{{opacity:1,rotation:0,scale:1,filter:"blur(0px)",duration:.3,ease:"back.out(1.6)"}},{t});'],
        "flash":    lambda i, t: [f'tl.fromTo("{i}",{{opacity:0,scale:1.15}},{{opacity:1,scale:1,duration:.2,ease:"power2.out"}},{t});',
                                  f'tl.fromTo("#flash",{{opacity:0}},{{opacity:.85,duration:.07,ease:"power1.out",yoyo:true,repeat:1,immediateRender:false}},{t});'],
    }
    for n, sh in enumerate(shots):
        src = f"assets/broll/{sh['f']}"
        d = round(sh["e"] - sh["s"] + (0.3 if n + 1 < len(shots) else 0), 3)   # bertindih 0.3 s (shot baru masuk atas)
        d = min(d, round(dur - sh["s"], 3))
        el = (f'<video id="b{n}" src="{src}" data-start="{sh["s"]}" data-duration="{d}" data-media-start="{sh["ms"]}" '
              f'data-track-index="{2 + n}" class="clip" muted playsinline></video>')
        body.append(f'<div class="bw" id="b{n}w" style="z-index:{2 + n}"><div class="mv" id="b{n}m" style="transform-origin:{sh.get("o", "50% 50%")}">{el}</div></div>')
        if n == 0: js.append(f'tl.set("#b{n}w",{{opacity:1}},0);')
        else: js += TRJS[sh.get("tr", "zoomblur")](f"#b{n}w", sh["s"])
        m0, m1 = sh.get("mv", ({"scale": 1.0}, {"scale": 1.05}))
        f0 = ",".join(f"{k}:{v}" for k, v in m0.items()); f1 = ",".join(f"{k}:{v}" for k, v in m1.items())
        js.append(f'tl.fromTo("#b{n}m",{{{f0}}},{{{f1},duration:{d},ease:"sine.inOut"}},{sh["s"]});')   # gerakan kamera / sudut
    for i, (p, amp) in enumerate(sorted(punch)):
        ir = "" if i == 0 else ",immediateRender:false"
        js.append(f'tl.fromTo("#cam",{{scale:1}},{{scale:{amp},duration:.14,ease:"expo.out",yoyo:true,repeat:1{ir}}},{p});')
    js.append(f'tl.fromTo("#glow",{{x:-240}},{{x:240,duration:{round(dur/2,3)},ease:"sine.inOut",yoyo:true,repeat:1}},0);')
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
#cam {{ position:absolute; inset:0; transform-origin:50% 55%; }}
.bw {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; opacity:0; overflow:hidden; }}
#flash {{ position:absolute; inset:0; background:#fff; opacity:0; z-index:70; pointer-events:none; }}
.mv {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; }}
.bw video, .bw img {{ position:absolute; left:0; top:0; width:{W}px; height:{H}px; object-fit:cover; }}
#scrim {{ position:absolute; left:0; top:0; width:{W}px; height:620px; z-index:60; pointer-events:none;
  background:linear-gradient(180deg,rgba(13,12,11,.30) 0%,rgba(13,12,11,.12) 300px,rgba(13,12,11,0) 600px); }}
#glow {{ position:absolute; left:240px; top:-260px; width:600px; height:600px; border-radius:50%; z-index:61; pointer-events:none;
  background:radial-gradient(circle, rgba(255,194,26,.14) 0%, rgba(255,194,26,0) 70%); }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="{dur}" data-width="{W}" data-height="{H}">
<div id="cam">
{chr(10).join(body)}
</div>
<audio id="vo" src="{vo_src}" data-start="0" data-duration="{dur}" data-track-index="1" data-has-audio="true"></audio>
<div id="scrim"></div>
<div id="flash"></div>
<div id="glow"></div>
<div id="gfx" data-composition-id="gfx" data-composition-src="compositions/gfx.html" data-start="0" data-duration="{dur}"
  data-track-index="30" data-track-kind="graphics" data-width="{W}" data-height="{H}" style="z-index:80"></div>
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

def build(vid, units):
    off, dur, shots, els, punch = plan(vid, units)
    P = f"{OUT}/{vid}"
    os.makedirs(f"{P}/assets/broll", exist_ok=True); os.makedirs(f"{P}/compositions", exist_ok=True)
    for f in {s["f"] for s in shots}:
        dst = f"{P}/assets/broll/{f}"
        if os.path.exists(dst): os.unlink(dst)
        if os.path.exists(f"{PROJ}/assets/broll/{f}"): os.link(f"{PROJ}/assets/broll/{f}", dst)
        else: print("  (belum ada)", f)
    for f in ("hyperframes.json", "package.json"):
        shutil.copy(f"{PROJ}/{f}", P)
    json.dump({"name": f"spm-final-boost-{vid}"}, open(f"{P}/meta.json", "w"))
    make_vo(units, off, dur, f"{P}/assets/vo.wav")
    S.SOUND_ALL = "ov"   # bunyi overlay bertukar-tukar (sfx.OV_KIT)
    S.ANIM = V.ANIMS[(int(vid[1:]) - 1) % len(V.ANIMS)]   # animasi masuk lain setiap video (v01 = pop)
    doc, sfx = S.build_gfx(els, dur=dur, y0=200)
    doc = doc.replace("<script>\nconst tl", "<script>\nwindow.__timelines = window.__timelines || {};\nconst tl")
    open(f"{P}/compositions/gfx.html", "w").write(doc)
    open(f"{P}/index.html", "w").write(root_html(dur, shots, punch))
    sfx = sorted(sfx + [[sh["s"], "tr"] for sh in shots[1:]])   # bunyi sikit setiap footage/angle baru (sfx.TR_KIT, bertukar)
    json.dump(sfx, open(f"{P}/sfx.json", "w"))
    json.dump(dict(units=units, offsets=off, dur=dur, shots=shots, els=els), open(f"{P}/plan.json", "w"), ensure_ascii=False, indent=1)
    print(vid, f"{dur:.1f}s", units, "| shots", len(shots), "| caps", len(els), "| sfx", len(sfx), flush=True)

if __name__ == "__main__":
    only = sys.argv[1:]
    for vid, units in VIDEOS:
        if only and vid not in only: continue
        build(vid, units)
