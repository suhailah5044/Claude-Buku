#!/usr/bin/env python3
"""Potong + susun footage ikut keep.json, speed 1.1x (pitch kekal), fade audio 10 ms setiap potongan.
Warna/cahaya footage TIDAK diubah (footage dah diedit pengguna). Guna: aroll.py <src.mov> <out.mp4>"""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
src, out = sys.argv[1], sys.argv[2]
K = json.load(open(f"{HERE}/keep.json"))
f = []
for i, (a, b) in enumerate(K):
    d = b - a
    f.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}]")
    f.append(f"[0:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={d-0.01:.3f}:d=0.01[a{i}]")
f.append("".join(f"[v{i}][a{i}]" for i in range(len(K))) + f"concat=n={len(K)}:v=1:a=1[vc][ac]")
f.append("[vc]setpts=PTS/1.1,fps=30,format=yuv420p[vo]")
f.append("[ac]atempo=1.1,aresample=48000[ao]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-filter_complex", ";".join(f), "-map", "[vo]", "-map", "[ao]",
                "-c:v", "libx264", "-crf", "14", "-preset", "medium", "-color_primaries", "bt709", "-color_trc", "bt709",
                "-colorspace", "bt709", "-c:a", "pcm_s16le", "-movflags", "+faststart", out.replace(".mp4", ".mov") if out.endswith(".mov") else out], check=True)
