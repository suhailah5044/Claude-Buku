#!/usr/bin/env python3
"""Bunyi SFX sintetik (deterministik), TANPA nada 'toing' (pengguna tak suka ting-ting-toing):
- pop    : tap lembut / gelembung pecah (noise ditapis + 'body' rendah pendek) -> 5 info pop-up
- swoosh : angin halus (noise, penapis menyapu naik-turun) -> beberapa caption utama
make_track([(t, jenis), ...], dur) -> numpy float32 mono 48 kHz.
Bunyi digunakan JARANG (bukan setiap caption) supaya tak serabut."""
import numpy as np
SR = 48000

def _lp(x, fc):
    """Penapis lowpass 1-pole dengan fc (Hz) boleh berubah ikut masa (array)."""
    fc = np.broadcast_to(fc, x.shape)
    a = np.exp(-2 * np.pi * fc / SR)
    y = np.empty_like(x); z = 0.0
    for i in range(len(x)):
        z = (1 - a[i]) * x[i] + a[i] * z; y[i] = z
    return y

def pop(seed=0):
    rng = np.random.default_rng(11 + seed)
    t = np.arange(int(0.09 * SR)) / SR
    n = rng.standard_normal(len(t))
    band = _lp(n, 3200) - _lp(n, 900)                      # bandpass ~0.9-3.2 kHz: 'tap' lembut
    burst = band * (1 - np.exp(-t / 0.0008)) * np.exp(-t / 0.012)
    body = np.sin(2 * np.pi * 105 * t) * (1 - np.exp(-t / 0.002)) * np.exp(-t / 0.028) * 0.6
    x = burst / (np.abs(burst).max() + 1e-9) + body
    return (x / np.abs(x).max()).astype(np.float32)

def swoosh(seed=0):
    rng = np.random.default_rng(23 + seed)
    d = 0.34; t = np.arange(int(d * SR)) / SR
    n = rng.standard_normal(len(t))
    u = t / d
    fc = 500 + 5200 * np.sin(np.pi * u) ** 1.6               # sapu naik kemudian turun
    x = _lp(n, fc) - _lp(n, 250)
    env = np.sin(np.pi * u) ** 2.2
    x = x * env
    return (x / np.abs(x).max()).astype(np.float32)

def toing(var=0):
    """'Bubble pop' bernada (versi preview v3) - pengguna MAHU bunyi ni untuk 9 varian ('toing toing')."""
    k = [1.0, 1.12, 0.93][var % 3]
    t = np.arange(int(0.13 * SR)) / SR
    f = (320 + 980 * np.exp(-t / 0.016)) * k
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * (1 - np.exp(-t / 0.0012)) * np.exp(-t / 0.032)
    thump = np.sin(2 * np.pi * 140 * k * t) * np.exp(-t / 0.022) * 0.35
    rng = np.random.default_rng(7 + var)
    click = np.diff(np.concatenate([[0], rng.standard_normal(len(t))])) * np.exp(-t / 0.0018) * 0.10
    x = body + thump + click
    return (x / np.abs(x).max()).astype(np.float32)

KIT = {"pop": [pop(i) for i in range(2)], "swoosh": [swoosh(i) for i in range(2)], "toing": [toing(i) for i in range(3)]}
GAIN = {"pop": 0.30, "swoosh": 0.16, "toing": 0.28}

# ---- Pengguna: setiap footage/angle baru ada bunyi sikit, overlay pun ada SFX, TAPI tukar-tukar (jangan sama) ----
def whoosh(dur=0.32, lo=400, hi=5200, shape=1.6, rise=0.5, seed=0):
    """Whoosh angin: noise ditapis, frekuensi menyapu; rise = kedudukan puncak (0-1)."""
    rng = np.random.default_rng(101 + seed)
    t = np.arange(int(dur * SR)) / SR; u = t / dur
    env = np.where(u < rise, (u / rise) ** 1.4, ((1 - u) / (1 - rise)) ** 2.2)
    fc = lo + (hi - lo) * env ** shape
    n = rng.standard_normal(len(t))
    x = (_lp(n, fc) - _lp(n, 180)) * env
    return (x / (np.abs(x).max() + 1e-9)).astype(np.float32)

def paper(dur=0.26, seed=0):
    """Selak kertas: bunyi gesel + 'flick' kecil (2-7 kHz)."""
    rng = np.random.default_rng(211 + seed)
    t = np.arange(int(dur * SR)) / SR; u = t / dur
    n = rng.standard_normal(len(t))
    band = _lp(n, 7000) - _lp(n, 1800)
    grain = (rng.random(len(t)) < 0.004) * rng.standard_normal(len(t)) * 3
    env = np.sin(np.pi * u) ** 1.3 * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * u + seed) ** 2)
    x = band * env + _lp(grain, 5000) * env
    return (x / (np.abs(x).max() + 1e-9)).astype(np.float32)

def bubble(f0=600, f1=1500, dur=0.11, seed=0):
    t = np.arange(int(dur * SR)) / SR
    f = f0 + (f1 - f0) * (1 - np.exp(-t / 0.02))
    x = np.sin(2 * np.pi * np.cumsum(f) / SR) * (1 - np.exp(-t / 0.002)) * np.exp(-t / 0.03)
    return (x / np.abs(x).max()).astype(np.float32)

def click(fc=2500, seed=0):
    rng = np.random.default_rng(307 + seed)
    t = np.arange(int(0.05 * SR)) / SR; n = rng.standard_normal(len(t))
    x = (_lp(n, fc * 1.6) - _lp(n, fc * 0.6)) * np.exp(-t / 0.006) + np.sin(2 * np.pi * fc * 0.5 * t) * np.exp(-t / 0.01) * 0.5
    return (x / np.abs(x).max()).astype(np.float32)

TR_KIT = [whoosh(0.30, 300, 4800, 1.6, 0.55, 0), paper(0.24, 0), whoosh(0.22, 800, 7000, 1.2, 0.35, 1),
          whoosh(0.38, 250, 3200, 2.0, 0.65, 2), paper(0.30, 1), whoosh(0.26, 600, 6000, 1.4, 0.25, 3),
          whoosh(0.34, 400, 5200, 1.8, 0.5, 4), paper(0.20, 2)]
OV_KIT = [toing(0), pop(0), bubble(520, 1400), click(2600), toing(1), bubble(700, 1800, 0.09), pop(1), click(1900, 1), toing(2)]
KIT["tr"] = TR_KIT; KIT["ov"] = OV_KIT
GAIN["tr"] = 0.11; GAIN["ov"] = 0.24

def make_track(events, dur):
    out = np.zeros(int(dur * SR) + SR, np.float32)
    cnt = {}
    for t, k in sorted(events):
        c = cnt.get(k, 0); cnt[k] = c + 1
        p = KIT[k][c % len(KIT[k])] * GAIN[k]
        i = int(max(0, t - (0.10 if k == "swoosh" else 0.07 if k == "tr" else 0)) * SR)   # whoosh mula sikit awal
        if i < len(out): out[i:i + len(p)] += p[:len(out) - i]
    return out[:int(dur * SR)]

if __name__ == "__main__":
    import wave, sys
    gap = np.zeros(SR // 3, np.float32)
    x = np.concatenate([np.concatenate([p, gap]) for k in KIT for p in KIT[k]])
    w = wave.open(sys.argv[1] if len(sys.argv) > 1 else "sfx_demo.wav", "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x * 0.8 * 32767).astype(np.int16).tobytes()); w.close()
