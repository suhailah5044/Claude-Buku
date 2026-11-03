#!/usr/bin/env python3
"""Ganti audio hasil render HyperFrames (renderer auto-naikkan ke ~-11 LUFS) dengan audio
asal A-roll (-14 LUFS). Guna: python3 mux.py render.mp4 out.mp4 [crf] [aroll_offset_s] [pre_s]
- aroll_offset_s: data-media-start A-roll (varian yang mula di tengah)
- pre_s: saat senyap di depan (varian dengan klip pembuka sebelum A-roll)"""
import sys, subprocess, os
src, out = sys.argv[1], sys.argv[2]
crf = sys.argv[3] if len(sys.argv) > 3 else None
off = float(sys.argv[4]) if len(sys.argv) > 4 else 0.0
pre = float(sys.argv[5]) if len(sys.argv) > 5 else 0.0
AR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets/aroll.mp4")
AR = os.environ.get("AROLL", AR)
af = f"adelay={int(pre*1000)}:all=1," if pre > 0 else ""
v = ["-c:v", "copy"] if crf is None else ["-c:v", "libx264", "-crf", crf, "-preset", "slow", "-pix_fmt", "yuv420p"]
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-ss", str(off), "-i", AR, "-map", "0:v:0", "-map", "1:a:0",
                "-af", af + "alimiter=limit=0.89:level=false,apad", *v, "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
print("ok", out)
