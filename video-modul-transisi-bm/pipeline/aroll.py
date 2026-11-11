#!/usr/bin/env python3
"""A-roll Modul Transisi (Bahasa Melayu, KV/KVK) dari satu klip talking-head export CapCut (export_1794355878860.mov, 207 s, SDR).
- SEG: take terbaik setiap ayat (ulangan, false start, 'Okay' awal, sembang tepi 'bungkus...' dibuang)
- titik potong di-snap ke tenaga paling rendah (dalam senyap), senyap > 0.1 s -> 0.08 s, fade 10 ms
- WARNA/CAHAYA ASAL (peraturan #20): tiada eq/sharpen/denoise; full range -> tv sahaja, tag bt709
- speed 1.1x (atempo). Output: assets/aroll.mp4 (video sahaja) + assets/vo.wav (48 kHz, belum loudnorm - mux.py buat)
Guna: RAW=<dir ada src.mov + a16.wav> python3 pipeline/aroll.py"""
import os, json, subprocess, re, wave
import numpy as np
RAW = os.environ.get("RAW", "/home/user/raw-mtbm")
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(HERE)
SRC = f"{RAW}/src.mov"
# (mula, tamat, label) - masa asal; mula/tamat di-snap +-SNAP ke tenaga minimum
SEG = [
    (10.20, 12.87, "Parents, kalau anak bakal masuk tahun satu,"),
    (17.20, 22.20, "saya nak perkenalkan buku kemahiran asas membaca, menulis dan juga mengira."),
    (23.64, 28.75, "Modul transisi tahun satu yang baru ni. Ini edisi 2027."),
    (37.73, 46.07, "Dalam modul ni ada sains awal, ada matematik awal, ada bahasa, ada English dan juga bahasa Melayu."),
    (46.07, 50.60, "Buku ini sesuai untuk jadikan latihan untuk bantu anak biasakan diri dengan aktiviti pembelajaran"),
    (52.30, 54.10, "sebelum melangkah ke tahun satu."),
    (57.62, 60.45, "Saya nak share dengan ibu ayah bahagian bahasa Melayu ni pula."),
    (65.80, 72.18, "Dekat sini ada contoh latihan KV, suku kata V plus KV."),
    (74.00, 76.85, "KV ni maksudnya consonant dan juga vocal."),
    (82.92, 87.70, "Anak kita akan belajar kenal bunyi huruf, gabungan bunyi untuk membentuk suku kata."),
    (129.45, 145.85, "Apa yang dimaksudkan dengan suku kata KVK? K ni consonant, V ni pula ialah vocal dan K ni ialah consonant. Jadi dekat sini contohnya, bas. B, A, S."),
    (148.80, 150.63, "Contoh soalan je begini,"),
    (174.24, 181.28, "dekat sini anak kita perlu kenal huruf, sebut bunyi dan gabungkan semuanya untuk membaca satu perkataan."),
    (189.93, 193.98, "Kalau ibu ayah nak dapatkan modul transisi untuk anak tahun satu,"),
    (204.20, 205.71, "boleh ambil set yang ini."),
]
SNAP = {0: (0.06, 0.06), 1: (0, 0.04), 2: (0, 0.04), 4: (0.03, 0.12), 5: (0.2, 0.05), 6: (0.12, 0.08),
        11: (0.15, 0.05), 9: (0, 0.05), 12: (0, 0.05), 13: (0, 0.05), 14: (0.15, 0.05)}
GAP_IN = 0.10; KEEP_GAP = 0.08; PAD = KEEP_GAP / 2; F = 1 / 30

w = wave.open(f"{RAW}/a16.wav"); A = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
def rms(t): i = int(t * 16000); return float(np.sqrt(np.mean(A[max(0, i - 160):i + 160] ** 2)) + 1e-9)
def snap(t, win):
    if win <= 0: return t
    ts = np.arange(t - win, t + win + 1e-6, 0.01)
    return float(ts[np.argmin([rms(x) for x in ts])])

r = subprocess.run(["ffmpeg", "-i", f"{RAW}/a16.wav", "-af", "silencedetect=n=-40dB:d=0.08", "-f", "null", "-"], capture_output=True, text=True).stderr
SIL = list(zip([float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)], [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]))

pieces = []
for si, (s, e, _) in enumerate(SEG):
    ws = SNAP.get(si, (0.05, 0.05))
    s, e = snap(s, ws[0]), snap(e, ws[1])
    cur = s
    for a, b in SIL:
        if b - a > GAP_IN and a > s and b < e:
            pieces.append((cur, a + PAD, si)); cur = b - PAD
    pieces.append((cur, e, si))
pieces = [(round(round(a / F) * F, 4), round(round(b / F) * F, 4), si) for a, b, si in pieces]
pieces = [p for p in pieces if p[1] - p[0] > 0.05]
t = 0.0; segmap = {}
for a, b, si in pieces:
    m = segmap.setdefault(si, {"seg": si, "label": SEG[si][2], "src": a, "start": round(t, 3)})
    t += (b - a) / 1.1; m["end"] = round(t, 3)
json.dump({"pieces": pieces, "segments": list(segmap.values()), "dur": round(t, 3)}, open(f"{HERE}/edl.json", "w"), indent=1, ensure_ascii=False)

import concurrent.futures as cf
PD = f"{RAW}/pieces"; os.makedirs(PD, exist_ok=True)
def cut(i):
    a, b, _ = pieces[i]; d = b - a
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-i", SRC, "-t", f"{d:.3f}",
        "-vf", "fps=30,scale=1080:1920:in_range=pc:out_range=tv,format=yuv420p,setsar=1",
        "-af", f"aformat=sample_rates=48000:channel_layouts=mono,afade=t=in:d=0.01,afade=t=out:st={d-0.01:.3f}:d=0.01,apad,atrim=0:{d:.4f}",
        "-c:v", "libx264", "-crf", "12", "-preset", "fast", "-c:a", "pcm_s16le", f"{PD}/p{i:03d}.mov"], check=True)
with cf.ThreadPoolExecutor(4) as ex: list(ex.map(cut, range(len(pieces))))
open(f"{PD}/list.txt", "w").write("".join(f"file 'p{i:03d}.mov'\n" for i in range(len(pieces))))
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{PD}/list.txt",
    "-vf", "setpts=PTS/1.1,fps=30", "-an", "-color_trc", "bt709", "-color_primaries", "bt709", "-colorspace", "bt709",
    "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-pix_fmt", "yuv420p", "-movflags", "+faststart", f"{PROJ}/assets/aroll.mp4"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{PD}/list.txt", "-vn",
    "-af", "highpass=f=75,afftdn=nr=8:nf=-40,atempo=1.1", "-ar", "48000", "-ac", "1", f"{PROJ}/assets/vo.wav"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{PROJ}/assets/vo.wav", "-ar", "16000", f"{RAW}/final16.wav"], check=True)
print("pieces", len(pieces), "dur", round(t, 2))
