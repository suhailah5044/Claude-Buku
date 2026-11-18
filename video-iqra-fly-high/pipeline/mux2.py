#!/usr/bin/env python3
"""Audio v2/v3: audio bonus telefon (plan.json 'phone': [t_out, src_mula, dur]) ~-12 LUFS + SFX lembut (plan.json 'sfx').
Guna: python3 pipeline/mux2.py <render.mp4> <vid> <out.mp4> [--preview]   (--preview: 720p, saiz kecil)"""
import sys, os, json, subprocess, wave, re, tempfile
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(HERE)
sys.path.insert(0, f"{PROJ}/../video-matematik-spm-final-boost/pipeline")
from sfx import paper, whoosh
SR = 48000
src, vid, out = sys.argv[1], sys.argv[2], sys.argv[3]
preview = "--preview" in sys.argv
plan = json.load(open(f"{PROJ}/videos/{vid}/plan.json"))

def rd(p):
    w = wave.open(p); a = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    return a if w.getnchannels() == 1 else a.reshape(-1, w.getnchannels()).mean(1)

vdur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                            capture_output=True, text=True).stdout)
mix = np.zeros(int(vdur * SR), np.float32)
r = subprocess.run(["ffmpeg", "-ss", "10.2", "-t", "5.93", "-i", f"{PROJ}/assets/phone.wav", "-af", "ebur128", "-f", "null", "-"],
                   capture_output=True, text=True).stderr
g = -12.0 - float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r)[-1])
for t_out, s0, d in plan["phone"]:
    raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(s0), "-t", str(d), "-i", f"{PROJ}/assets/phone.wav", "-af",
                          f"highpass=f=80,volume={g:.2f}dB,afade=t=in:d=0.03,afade=t=out:st={d-0.06:.3f}:d=0.06,alimiter=limit=0.89:level=false",
                          "-f", "f32le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True, check=True).stdout
    a = np.frombuffer(raw, np.float32); i = int(t_out * SR); mix[i:i + len(a)] += a[:len(mix) - i]
KIT = {f[:-4]: rd(f"{PROJ}/assets/sfx/{f}") for f in os.listdir(f"{PROJ}/assets/sfx") if f.endswith(".wav")}
for i in range(3): KIT[f"paper{i}"] = paper(0.24 + 0.03 * i, i)
KIT["syn_whoosh"] = whoosh(0.32, 300, 4200, 1.6, 0.55, 5)
for t, k, gain in plan["sfx"]:
    p = KIT[k] * gain; i = int(max(0, t) * SR)
    if i < len(mix): mix[i:i + len(p)] += p[:len(mix) - i]
tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
w = wave.open(tmp, "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
vf = ["-vf", "scale=720:1280:flags=lanczos", "-crf", "23", "-preset", "fast"] if preview else ["-crf", "18", "-preset", "slow"]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-i", tmp, "-map", "0:v:0", "-map", "1:a:0", "-c:v", "libx264", *vf,
                "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                "-af", "alimiter=limit=0.89:level=false", "-c:a", "aac", "-b:a", "192k", "-ac", "2",
                "-shortest", "-movflags", "+faststart", out], check=True)
os.unlink(tmp)
L = subprocess.run(["ffmpeg", "-i", out, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
print("ok", out, f"{os.path.getsize(out)/1048576:.1f} MB", re.findall(r"I:\s+(-?[\d.]+) LUFS", L)[-1], "LUFS")
