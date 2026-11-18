#!/usr/bin/env python3
"""A-roll + VO untuk video Fly High (footage dah diedit pengguna di CapCut, VO + cut siap).

- Susunan baru (hook kuat di depan): segmen "Kita tengah belajar membaca memang kena mula daripada asas,
  sebab tu buku macam ni memang sangat-sangat menarik" (asal 20.02-24.62) dipindah ke DEPAN,
  kemudian 0-20.02 (vokal + dengar & tunjuk), kemudian 24.68-hujung (Fly High, 5 tahap, CTA).
  Potong hanya dalam senyap / pada cut shot asal.
- HLG (Dolby Vision 8.4) -> SDR: tone-map mobius TANPA eq/sharpen (kekal warna buku asal).
- Speed 1.1x (video + suara, pitch kekal).
- Suara "macam pakai mic": highpass, denoise ringan, EQ presence + warmth, de-ess, compressor.
  Loudness akhir dibuat dalam mux.py.
Guna: python3 pipeline/prep.py <footage.mov>"""
import os, sys, subprocess, json
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(HERE)
SRC = sys.argv[1] if len(sys.argv) > 1 else None
SPEED = 1.1
# (video_in, video_out, audio_in, audio_out) dalam masa asal
SEGS = [
    (20.10, 24.62, 20.02, 24.62),   # hook: "Kita tengah belajar membaca... sangat-sangat menarik."
    (0.00, 20.02, 0.00, 20.02),     # vokal + dengar & tunjuk
    (24.68, 54.0667, 24.68, 54.0667),  # Fly High, 5 tahap, kelebihan, CTA
]
TM = ("zscale=tin=arib-std-b67:pin=bt2020:min=bt2020nc:rin=tv:t=linear:npl=160,format=gbrpf32le,zscale=p=bt709,"
      "tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p")

def mapt(t):
    """masa asal -> masa final (selepas susun semula + 1.1x). Guna masa audio."""
    off = 0.0
    for vi, vo, ai, ao in SEGS:
        if ai - 1e-6 <= t <= ao + 1e-6:
            return (off + t - ai) / SPEED
        off += ao - ai
    return None

if __name__ == "__main__":
    fc = []; n = len(SEGS)
    for i, (vi, vo, ai, ao) in enumerate(SEGS):
        hold = (ao - ai) - (vo - vi)
        pad = f",tpad=start_mode=clone:start_duration={hold:.3f}" if hold > 1e-3 else ""
        fc.append(f"[0:v]trim={vi}:{vo},setpts=PTS-STARTPTS,{TM}{pad}[v{i}]")
        fc.append(f"[0:a]atrim={ai}:{ao},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={ao-ai-0.012:.3f}:d=0.012[a{i}]")
    fc.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[cv][ca]")
    fc.append(f"[cv]setpts=PTS/{SPEED},fps=30[v]")
    voice = ("highpass=f=80,afftdn=nr=8:nf=-42,"
             "equalizer=f=180:t=q:w=1:g=1.5,equalizer=f=3200:t=q:w=1.2:g=2.5,equalizer=f=7000:t=q:w=2:g=-1.5,"
             "deesser=i=0.35,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2")
    fc.append(f"[ca]atempo={SPEED},{voice},aresample=48000[a]")
    os.makedirs(f"{PROJ}/assets", exist_ok=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-filter_complex", ";".join(fc),
                    "-map", "[v]", "-an", "-c:v", "libx264", "-crf", "12", "-preset", "medium", "-pix_fmt", "yuv420p",
                    "-color_primaries", "bt709", "-color_trc", "bt709", "-colorspace", "bt709",
                    "-movflags", "+faststart", f"{PROJ}/assets/aroll.mp4",
                    "-map", "[a]", "-ac", "1", f"{PROJ}/assets/vo.wav"], check=True)
    for f in ("aroll.mp4", "vo.wav"):
        d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                            f"{PROJ}/assets/{f}"], capture_output=True, text=True).stdout.strip()
        print(f, d)
