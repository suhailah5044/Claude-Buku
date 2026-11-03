#!/usr/bin/env python3
"""Sediakan unit voiceover (VO) -> assets/vo/<unit>.wav + pipeline/vo.json (perkataan, masa selepas 1.1x).

Footage VO: folder INTRO (10 hook), TENGAH (3 isi), CTA (5 penutup) + Footage.mov (review penuh 13 s).
Klip IMG_13xx = b-roll SENYAP (Whisper keluar "Terima kasih kerana menonton") -> tidak digunakan untuk audio.

Setiap unit:
- buang senyap depan/belakang, jeda > 0.10 s dipendekkan ke 0.08 s (potong di tengah senyap)
- "So," dalam tengah_96DE dikekalkan: tiada senyap sebenar di sekelilingnya (potong = suara putus)
- fade 10 ms setiap potongan, speed 1.1x (atempo, pitch kekal), highpass + afftdn + compressor
- loudness akhir dibuat per video (mux.py) supaya semua video sama kuat
Kemudian setiap unit ditranscribe SEMULA (condition_on_previous_text=False) untuk semak ulangan & masa perkataan."""
import os, sys, json, subprocess, wave
import numpy as np
WORK = os.environ.get("WORK", "/home/user/wspm")
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(HERE)
sys.path.insert(0, WORK)
OUT = f"{PROJ}/assets/vo"; os.makedirs(OUT, exist_ok=True)
SR = 48000
UNITS = {  # unit: (fail mentah, potongan tambahan [(a,b)] dibuang)
    "i_189E": ("intro_189E9064.mov", []),   # Jangan tunggu last minute...
    "i_235A": ("intro_235AD8A1.mov", []),   # Best tahu kalau ada buku latihan yang siap dengan skema jawapan...
    "i_2C72": ("intro_2C72F044.mov", []),   # Matematik ni bukan baca teori semata-mata...
    "i_4557": ("intro_45577C8C.mov", []),   # SPM dah makin dekat ni...
    "i_48FA": ("intro_48FAC4C8.mov", []),   # Untuk yang tengah susun bahan ulangkaji SPM...
    "i_70D5": ("intro_70D5453E.mov", []),   # Selagi masih ada masa sebelum SPM...
    "i_A559": ("intro_A559F3F9.mov", []),   # Kalau rasa latihan matematik masih tak cukup...
    "i_BD48": ("intro_BD488AAF.mov", []),   # Saya tertarik dengan buku ni...
    "i_C83B": ("intro_C83BD5C9.mov", []),   # Parents yang ada anak ambil SPM...
    "i_EC6D": ("intro_EC6D47AA.mov", []),   # Ini antara buku yang boleh korang tengok...
    "t_3454": ("tengah_3454C4A0.mov", []),  # bonus rakaman bengkel kalkulator
    "t_96DE": ("tengah_96DE338B.mov", []),  # fokus soalan berpotensi tinggi ("So," DIKEKALKAN: tiada senyap untuk potong)
    "t_E6E5": ("tengah_E6E521C9.mov", []),  # extra material: soalan fokus, skema, bengkel
    "c_3EF9": ("cta_3EF9C023.mov", []),     # Jangan tunggu last minute... kalau berminat terus checkout
    "c_4EE9": ("cta_4EE9DBE1.mov", []),     # Kalau korang tengah cari final preparation...
    "c_C62F": ("cta_C62F1689.mov", []),     # Masih ada masa lagi ni...
    "c_E3ED": ("cta_E3EDA374.mov", []),     # Kalau rasa buku ni sesuai...
    "c_F20C": ("cta_F20CC7C4.mov", []),     # Parents yang ada anak bakal ambil SPM...
    "f_full": ("Footage.mov", []),          # review penuh (13 s)
}
GAP_IN, KEEP = 0.10, 0.08

def load(f):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f"{WORK}/raw/{f}", "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()

def gaps(x):
    h = SR // 100; d = 20 * np.log10(np.sqrt((x[:len(x)//h*h].reshape(-1, h) ** 2).mean(1)) + 1e-7)
    th = max(np.percentile(d, 8) + 8, np.percentile(d, 95) - 32)
    low = d < th; out = []; i = 0
    while i < len(low):
        if low[i]:
            j = i
            while j < len(low) and low[j]: j += 1
            out.append((i * 0.01, j * 0.01)); i = j
        else: i += 1
    return out, len(d) * 0.01

def pieces(x, extra):
    g, dur = gaps(x)
    a0 = 0.0; b0 = dur
    if g and g[0][0] == 0: a0 = max(0, g[0][1] - 0.04)
    if g and g[-1][1] >= dur - 0.02: b0 = g[-1][0] + 0.06
    cuts = [(a + KEEP / 2, b - KEEP / 2) for a, b in g if b - a > GAP_IN and a > a0 + 0.01 and b < b0 - 0.01] + extra
    cuts.sort(); P = []; cur = a0
    for a, b in cuts:
        P.append((cur, a)); cur = b
    P.append((cur, b0))
    return [(round(a, 3), round(b, 3)) for a, b in P if b - a > 0.03]

def fade(y, ms=10):
    n = min(len(y) // 2, int(SR * ms / 1000)); r = np.linspace(0, 1, n, dtype=np.float32)
    y[:n] *= r; y[-n:] *= r[::-1]; return y

def proc(u):
    f, extra = UNITS[u]
    x = load(f); P = pieces(x, extra)
    y = np.concatenate([fade(x[int(a * SR):int(b * SR)].copy()) for a, b in P])
    tmp = f"{WORK}/vo_{u}_cut.wav"
    w = wave.open(tmp, "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
    w.writeframes((np.clip(y, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af",
                    "highpass=f=75,afftdn=nr=8:nf=-40,atempo=1.1,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2",
                    "-ar", str(SR), "-ac", "1", "-c:a", "pcm_s16le", f"{OUT}/{u}.wav"], check=True)
    return P

if __name__ == "__main__":
    from faster_whisper import WhisperModel
    m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=4)
    only = sys.argv[1:]
    J = json.load(open(f"{HERE}/vo.json")) if os.path.exists(f"{HERE}/vo.json") else {}
    for u in UNITS:
        if only and u not in only: continue
        P = proc(u)
        wf = wave.open(f"{OUT}/{u}.wav"); a = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).astype(np.float32) / 32768
        dur = len(a) / SR
        a16 = a[::3]   # 48k -> 16k
        segs, _ = m.transcribe(a16, language="ms", beam_size=5, word_timestamps=True, condition_on_previous_text=False, temperature=0)
        words = [{"w": w.word.strip(), "s": round(w.start, 3), "e": round(w.end, 3)} for s in segs for w in s.words]
        J[u] = {"src": UNITS[u][0], "pieces": P, "dur": round(dur, 3), "words": words}
        print(f"{u} {dur:5.2f}s | " + " ".join(f"{w['w']}[{w['s']:.2f}]" for w in words), flush=True)
    json.dump(J, open(f"{HERE}/vo.json", "w"), ensure_ascii=False, indent=1)
