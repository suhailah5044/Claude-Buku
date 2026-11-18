#!/usr/bin/env python3
"""Audio akhir: audio asal footage (hanya audio bonus dari telefon 10.2-16.1 s; selebihnya senyap) dinaikkan ke ~-12 LUFS
(diukur pada segmen itu sahaja) + SFX lembut (sfx.json). Tiada muzik. Video render disalin semula H.264 < 100 MB.
Guna: python3 pipeline/mux.py <render.mp4> <out.mp4>"""
import sys, os, json, subprocess, wave, re, tempfile
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(HERE)
sys.path.insert(0, f"{PROJ}/../video-matematik-spm-final-boost/pipeline")
from sfx import paper, whoosh   # sintetik (selak kertas lembut, whoosh)
SR = 48000
src, out = sys.argv[1], sys.argv[2]

def rd(p):
    w = wave.open(p); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    return a if w.getnchannels() == 1 else a.reshape(-1, w.getnchannels()).mean(1)

vdur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                            capture_output=True, text=True).stdout)
# 1) audio telefon: ukur loudness segmen 10.2-16.13 s, naikkan ke -12 LUFS, limiter
r = subprocess.run(["ffmpeg", "-ss", "10.2", "-t", "5.93", "-i", f"{PROJ}/assets/phone.wav", "-af", "ebur128", "-f", "null", "-"],
                   capture_output=True, text=True).stderr
I = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1]); g = -12.0 - I
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f"{PROJ}/assets/phone.wav", "-af",
                      f"highpass=f=80,volume={g:.2f}dB,alimiter=limit=0.89:level=false", "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"],
                     capture_output=True, check=True).stdout
phone = np.frombuffer(raw, np.float32)
mix = np.zeros(int(vdur * SR), np.float32); n = min(len(phone), len(mix)); mix[:n] = phone[:n]
# 2) SFX
KIT = {f[:-4]: rd(f"{PROJ}/assets/sfx/{f}") for f in os.listdir(f"{PROJ}/assets/sfx") if f.endswith(".wav")}
for i in range(3): KIT[f"paper{i}"] = paper(0.24 + 0.03 * i, i)
KIT["syn_whoosh"] = whoosh(0.32, 300, 4200, 1.6, 0.55, 5)
for t, k, gain in json.load(open(f"{PROJ}/sfx.json")):
    p = KIT[k] * gain; i = int(max(0, t) * SR)
    if i < len(mix): mix[i:i + len(p)] += p[:len(mix) - i]
tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
w = wave.open(tmp, "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
crf = 18
while True:
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-i", tmp, "-map", "0:v:0", "-map", "1:a:0",
                    "-c:v", "libx264", "-crf", str(crf), "-preset", "slow", "-pix_fmt", "yuv420p",
                    "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                    "-af", "alimiter=limit=0.89:level=false", "-c:a", "aac", "-b:a", "192k", "-ac", "2",
                    "-shortest", "-movflags", "+faststart", out], check=True)
    if os.path.getsize(out) < 95 * 1048576: break
    crf += 1
os.unlink(tmp)
print("ok", out, f"phone gain {g:+.1f} dB, crf {crf}, {os.path.getsize(out)/1048576:.1f} MB")
