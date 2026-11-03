#!/usr/bin/env python3
"""Sediakan assets/broll/*.mp4 (1080x1920, 30 fps, tanpa audio).
- Klip iPhone IMG_* = HDR HLG BT.2020 -> tone-map (filter yang pengguna setuju), autorotate potret.
- Screen recording PDF: crop kawasan halaman (buang status bar & bar 'Ask Gemini').
- sr_abc: halaman Prabaca statik -> halaman penuh atas latar kabur (tiada bahagian dipotong)."""
import os, subprocess, concurrent.futures as cf
WORK = os.environ.get("WORK", "/home/user/work"); OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets/broll")
os.makedirs(OUT, exist_ok=True)
TM = ("zscale=tin=arib-std-b67:pin=bt2020:min=bt2020nc:rin=tv:t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,"
      "tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,eq=contrast=1.08:saturation=1.12")
J = []
for n in ["IMG_1272", "IMG_1273", "IMG_1274", "IMG_1275", "IMG_1276", "IMG_1277", "IMG_1278", "IMG_1279", "IMG_1280"]:
    J.append([f"{WORK}/raw/{n}.MOV", "-vf", f"{TM},scale=1080:1920:flags=lanczos,fps=30", f"{OUT}/{n}.mp4"])
SR = f"{WORK}/raw/screenrec.mp4"
for name, ss, d in [("sr_vokal", 15.4, 3.4), ("sr_tulis", 18.2, 3.2), ("sr_kenal", 22.6, 3.0), ("sr_math", 43.6, 3.6), ("sr_arab", 60.6, 3.6), ("sr_corak", 36.8, 3.2)]:
    J.append(["-ss", str(ss), "-t", str(d), "-i", SR, "-vf",
              "crop=1294:2300:13:300,scale=1080:1920:flags=lanczos,fps=30,format=yuv420p", f"{OUT}/{name}.mp4"])
J.append(["-ss", "8.3", "-t", "3.0", "-i", SR, "-filter_complex",
          "[0:v]crop=1320:1820:0:310,split[a][b];[a]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
          "boxblur=40:2,eq=brightness=-0.12[bg];[b]scale=1060:-2:flags=lanczos[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2-20,fps=30,format=yuv420p",
          f"{OUT}/sr_abc.mp4"])
def run(j):
    if j[0].startswith("/"): j = ["-i"] + j
    subprocess.run(["ffmpeg", "-v", "error", "-y", *j[:-1], "-an", "-c:v", "libx264", "-crf", "18", "-preset", "medium",
                    "-movflags", "+faststart", j[-1]], check=True)
with cf.ThreadPoolExecutor(3) as ex: list(ex.map(run, J))
print("ok", len(J))
