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

KIT = {"pop": [pop(i) for i in range(2)], "swoosh": [swoosh(i) for i in range(2)]}
GAIN = {"pop": 0.30, "swoosh": 0.16}

def make_track(events, dur):
    out = np.zeros(int(dur * SR) + SR, np.float32)
    cnt = {}
    for t, k in sorted(events):
        c = cnt.get(k, 0); cnt[k] = c + 1
        p = KIT[k][c % len(KIT[k])] * GAIN[k]
        i = int(max(0, t - (0.10 if k == "swoosh" else 0)) * SR)   # swoosh mula sikit awal
        if i < len(out): out[i:i + len(p)] += p[:len(out) - i]
    return out[:int(dur * SR)]

if __name__ == "__main__":
    import wave, sys
    gap = np.zeros(SR // 3, np.float32)
    x = np.concatenate([np.concatenate([p, gap]) for k in KIT for p in KIT[k]])
    w = wave.open(sys.argv[1] if len(sys.argv) > 1 else "sfx_demo.wav", "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x * 0.8 * 32767).astype(np.int16).tobytes()); w.close()
