#!/usr/bin/env python3
"""Audio akhir satu video: VO (videos/<id>/assets/vo.wav) dinormalkan (pilihan pengguna 'kuat lagi':
loudnorm -9 2-pass, +3.6 dB, alimiter 0.89 ~ -9.6 LUFS) + bunyi 'toing' (sfx.json) setiap kotak caption,
ganti audio render HyperFrames (renderer ubah loudness sendiri). Tiada muzik.
Guna: python3 pipeline/mux.py <render.mp4> <vid> <out.mp4> [crf]"""
import sys, subprocess, os, json, wave, tempfile, re
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from sfx import make_track, SR
src, vid, out = sys.argv[1], sys.argv[2], sys.argv[3]
crf = sys.argv[4] if len(sys.argv) > 4 else None
P = f"{PROJ}/videos/{vid}"
vdur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                            capture_output=True, text=True).stdout)
# 1) VO -> loudnorm 2-pass
r = subprocess.run(["ffmpeg", "-i", f"{P}/assets/vo.wav", "-af", "loudnorm=I=-9:TP=-1:LRA=7:print_format=json", "-f", "null", "-"],
                   capture_output=True, text=True).stderr
m = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r).group(0))
ln = (f"loudnorm=I=-9:TP=-1:LRA=7:linear=true:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
      f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}")
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f"{P}/assets/vo.wav", "-af",
                      ln + ",volume=3.6dB,alimiter=limit=0.89:attack=2:release=60:level=false,aresample=48000",
                      "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True, check=True).stdout
voice = np.frombuffer(raw, np.float32)
mix = np.zeros(int(vdur * SR), np.float32); n = min(len(voice), len(mix)); mix[:n] = voice[:n]
mix += make_track(json.load(open(f"{P}/sfx.json")), vdur)[:len(mix)]
tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
w = wave.open(tmp, "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
# Video final: HEVC (hvc1) - lebih tajam dari H.264 pada saiz sama; < 100 MB (had GitHub). crf None = salin video render.
c = None if crf is None else int(crf)
while True:
    v = ["-c:v", "copy"] if c is None else ["-c:v", "libx265", "-crf", str(c), "-preset", "medium", "-pix_fmt", "yuv420p",
                                            "-tag:v", "hvc1", "-x265-params", "log-level=error:aq-mode=3"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-i", tmp, "-map", "0:v:0", "-map", "1:a:0",
                    "-af", "alimiter=limit=0.89:level=false", *v, "-c:a", "aac", "-b:a", "192k", "-ac", "2",
                    "-shortest", "-movflags", "+faststart", out], check=True)
    if c is None or os.path.getsize(out) < 97 * 1048576: break
    c += 1
os.unlink(tmp)
L = subprocess.run(["ffmpeg", "-i", out, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
print("ok", out, re.findall(r"I:\s+(-?[\d.]+) LUFS", L)[-1], "LUFS")
