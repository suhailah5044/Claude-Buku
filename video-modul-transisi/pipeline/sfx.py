#!/usr/bin/env python3
"""Bunyi 'bubble pop' sintetik (lembut, crisp, tidak kasar) + trek SFX ikut masa.
make_track(times, dur) -> numpy float32 mono 48 kHz. 3 variasi pitch digilir supaya tak bunyi robotik."""
import numpy as np
SR = 48000
def pop(var=0):
    k = [1.0, 1.12, 0.93][var % 3]
    t = np.arange(int(0.13 * SR)) / SR
    f = (320 + 980 * np.exp(-t / 0.016)) * k                  # sweep turun cepat = 'bloop'
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * (1 - np.exp(-t / 0.0012)) * np.exp(-t / 0.032)
    thump = np.sin(2 * np.pi * 140 * k * t) * np.exp(-t / 0.022) * 0.35
    rng = np.random.default_rng(7 + var)                       # deterministik
    click = np.diff(np.concatenate([[0], rng.standard_normal(len(t))])) * np.exp(-t / 0.0018) * 0.10
    x = body + thump + click
    return (x / np.abs(x).max()).astype(np.float32)
POPS = [pop(i) for i in range(3)]
def make_track(times, dur, gain=0.30):
    out = np.zeros(int(dur * SR) + SR, np.float32)
    for n, t in enumerate(sorted(times)):
        p = POPS[n % 3] * gain; i = int(t * SR)
        if 0 <= i < len(out): out[i:i + len(p)] += p[:len(out) - i]
    return out[:int(dur * SR)]
if __name__ == "__main__":
    import wave, sys
    x = np.concatenate([np.concatenate([p, np.zeros(SR // 3, np.float32)]) for p in POPS])
    w = wave.open(sys.argv[1] if len(sys.argv) > 1 else "pop_demo.wav", "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((x * 0.8 * 32767).astype(np.int16).tobytes()); w.close()
