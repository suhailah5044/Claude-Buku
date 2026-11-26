#!/usr/bin/env python3
"""Audio akhir: VO (acompressor + loudnorm -11 LUFS 2-pass, TP -1) + SFX jarang (sfx.json, bunyi bertukar-tukar).
Tiada muzik. Ganti audio render HyperFrames. Guna: mux.py <render.mp4> <vo.wav> <out.mp4> [crf]"""
import sys, subprocess, os, json, wave, tempfile, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from sfx import make_track, SR
src, vo, out = sys.argv[1:4]; crf = sys.argv[4] if len(sys.argv) > 4 else None
vdur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src], capture_output=True, text=True).stdout)
pre = "highpass=f=75,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2"
r = subprocess.run(["ffmpeg", "-i", vo, "-af", pre + ",loudnorm=I=-11:TP=-1:LRA=9:print_format=json", "-f", "null", "-"], capture_output=True, text=True).stderr
m = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r).group(0))
ln = (f"loudnorm=I=-11:TP=-1:LRA=9:linear=true:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
      f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}")
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", vo, "-af", pre + "," + ln + ",aresample=48000", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
voice = np.frombuffer(raw, np.float32)
mix = np.zeros(int(vdur * SR), np.float32); n = min(len(voice), len(mix)); mix[:n] = voice[:n]
ev = [(t, k) for t, k in json.load(open(f"{HERE}/sfx.json"))]
mix += make_track(ev, vdur)[:len(mix)]
tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
w = wave.open(tmp, "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
v = ["-c:v", "copy"] if crf is None else ["-c:v", "libx264", "-crf", crf, "-preset", "slow", "-pix_fmt", "yuv420p"]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-i", tmp, "-map", "0:v:0", "-map", "1:a:0", "-af", "alimiter=limit=0.89:level=false",
                *v, "-c:a", "aac", "-b:a", "192k", "-ac", "2", "-shortest", "-movflags", "+faststart", out], check=True)
os.unlink(tmp)
L = subprocess.run(["ffmpeg", "-i", out, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
print("ok", out, re.findall(r"I:\s+(-?[\d.]+) LUFS", L)[-1], "LUFS")
