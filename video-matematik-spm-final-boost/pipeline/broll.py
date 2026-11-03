#!/usr/bin/env python3
"""assets/broll/*.mp4 (1080x1920, 30 fps, tanpa audio) dari klip iPhone IMG_13xx.
Semua klip = HDR HLG BT.2020 4K (rotate -90) -> tone-map (filter yang pengguna setuju).
Semakan cermin: tulisan cover 'MATEMATIK SPM' dibaca betul -> tiada hflip.
Gambar HEIC (IMG_1388 cover, IMG_1382 halaman) -> PNG 1080x1920."""
import os, glob, subprocess, concurrent.futures as cf
WORK = os.environ.get("WORK", "/home/user/wspm"); OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets/broll")
os.makedirs(OUT, exist_ok=True)
TM = ("fps=30,zscale=w=1080:h=1920:f=lanczos:tin=arib-std-b67:pin=bt2020:min=bt2020nc:rin=tv:t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,"
      "tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,eq=contrast=1.08:saturation=1.12")
def run(f):
    n = os.path.basename(f)[:-4]
    if os.path.exists(f"{OUT}/{n}.mp4") and not os.environ.get("REDO"): return
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f, "-an", "-vf", TM,
                    "-c:v", "libx264", "-crf", "20", "-preset", "medium", "-g", "15", "-movflags", "+faststart", f"{OUT}/{n}.mp4"], check=True)
    print(n, flush=True)
with cf.ThreadPoolExecutor(4) as ex: list(ex.map(run, sorted(glob.glob(f"{WORK}/raw/IMG_*.MOV"))))
try:
    import pillow_heif; pillow_heif.register_heif_opener()
    from PIL import Image, ImageOps
    for n, o in [("IMG_1388.HEIC", "photo_cover.jpg"), ("cta_IMG_1382.HEIC", "photo_page.jpg")]:
        im = ImageOps.fit(Image.open(f"{WORK}/raw/{n}").convert("RGB"), (1080, 1920), Image.LANCZOS); im.save(f"{OUT}/{o}", quality=92)
except Exception as e: print("heic", e)
