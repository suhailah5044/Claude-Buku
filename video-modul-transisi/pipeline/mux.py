#!/usr/bin/env python3
"""Audio akhir: suara asal A-roll (-11 LUFS, compressor) + bunyi pop (pipeline/sfx.json),
ganti audio render HyperFrames (renderer auto-ubah loudness).
Guna: python3 mux.py render.mp4 out.mp4 [crf] [aroll_offset_s] [pre_s] [sfx.json]
- aroll_offset_s: data-media-start A-roll (varian yang mula di tengah)
- pre_s: saat senyap di depan (varian dengan klip pembuka sebelum A-roll)"""
import sys, subprocess, os, json, wave, tempfile
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sfx import make_track, SR
HERE = os.path.dirname(os.path.abspath(__file__))
src, out = sys.argv[1], sys.argv[2]
crf = sys.argv[3] if len(sys.argv) > 3 and sys.argv[3] != "-" else None
off = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
pre = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0
sfxf = sys.argv[6] if len(sys.argv) > 6 else os.path.join(HERE, "sfx.json")
AR = os.environ.get("AROLL", os.path.join(os.path.dirname(HERE), "assets/aroll.mp4"))
vdur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", src],
                            capture_output=True, text=True).stdout)
raw = subprocess.run(["ffmpeg", "-v", "error", "-ss", str(off), "-i", AR, "-vn", "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                     capture_output=True, check=True).stdout
voice = np.frombuffer(raw, np.float32)
mix = np.zeros(int(vdur * SR), np.float32)
i0 = int(pre * SR); n = min(len(voice), len(mix) - i0); mix[i0:i0 + n] = voice[:n]
mix += make_track(json.load(open(sfxf)) if os.path.exists(sfxf) else [], vdur)[:len(mix)]
tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False).name
w = wave.open(tmp, "w"); w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR)
w.writeframes((np.clip(mix, -1, 1) * 32767).astype(np.int16).tobytes()); w.close()
# Video: HEVC (H.265) kualiti tinggi - lebih tajam dari H.264 pada saiz sama; mesti < 100 MB (had GitHub).
# crf dinaikkan automatik jika fail terlalu besar. crf None = salin video render terus.
LIMIT = 97 * 1024 * 1024
c = None if crf is None else int(crf)
while True:
    v = ["-c:v", "copy"] if c is None else ["-c:v", "libx265", "-crf", str(c), "-preset", "medium", "-pix_fmt", "yuv420p",
                                            "-tag:v", "hvc1", "-x265-params", "log-level=error:aq-mode=3"]
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-i", tmp, "-map", "0:v:0", "-map", "1:a:0",
                    "-af", "alimiter=limit=0.89:level=false", *v, "-c:a", "aac", "-b:a", "192k", "-ac", "2",
                    "-shortest", "-movflags", "+faststart", out], check=True)
    if c is None or os.path.getsize(out) < LIMIT: break
    c += 1
os.unlink(tmp); print("ok", out, "crf", c, round(os.path.getsize(out) / 1048576, 1), "MB")
