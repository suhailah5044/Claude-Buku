#!/usr/bin/env python3
"""Buat assets/plate.mp4 daripada video asal (voiceover atas halaman buku).
- crop tengah 810x1440 (buang bar hitam) -> 1080x1920
- suara = stem vokal Demucs (muzik latar dibuang)
- jeda > 0.1 s dipendekkan ke 0.08 s, kemudian 1.1x, compressor + -11 LUFS (pengguna minta lebih kuat)
Perlu: $WORK/raw/f1.mov dan $WORK/work/audio/sep_vocals.wav"""
import os, json, subprocess, re
WORK = os.environ["WORK"]
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(HERE)
SRC, VOC = f"{WORK}/raw/f1.mov", f"{WORK}/work/audio/sep_vocals.wav"
START, END = 0.17, 28.71          # 0.0-0.1 ada sticker logo lama; suara mula 0.25
SIL = [(6.67, 6.87), (7.53, 7.67), (10.12, 10.38), (17.60, 17.71), (19.60, 19.70), (21.30, 21.42)]
keep, cur = [], START
for a, b in SIL:
    if b - a > 0.1:
        keep.append((cur, round(a + 0.04, 3))); cur = round(b - 0.04, 3)
keep.append((cur, END))
json.dump(keep, open(f"{HERE}/keep.json", "w"))
fc = []
for i, (a, b) in enumerate(keep):
    fc.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS[v{i}]")
    d = b - a
    fc.append(f"[1:a]atrim={a}:{b},asetpts=PTS-STARTPTS,afade=t=in:d=0.01,afade=t=out:st={d-0.01:.3f}:d=0.01[a{i}]")
n = len(keep)
fc.append("".join(f"[v{i}][a{i}]" for i in range(n)) + f"concat=n={n}:v=1:a=1[cv][ca]")
fc.append("[cv]crop=810:1440:135:240,scale=1080:1920:flags=lanczos,unsharp=5:5:0.6,"
          "eq=contrast=1.04:saturation=1.06,setpts=PTS/1.1,fps=30,format=yuv420p[vo]")
pre = "pan=mono|c0=0.5*c0+0.5*c1,highpass=f=75,afftdn=nr=8:nf=-40,atempo=1.1,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2"
fc.append(f"[ca]{pre}[ao]")
tmp = f"{WORK}/plate_tmp.mp4"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC, "-i", VOC, "-filter_complex", ";".join(fc),
                "-map", "[vo]", "-map", "[ao]", "-c:v", "libx264", "-crf", "16", "-preset", "medium",
                "-c:a", "pcm_s16le", f"{WORK}/plate_tmp.mov"], check=True)
# loudnorm 2-pass
r = subprocess.run(["ffmpeg", "-i", f"{WORK}/plate_tmp.mov", "-af", "loudnorm=I=-11:TP=-1:LRA=9:print_format=json",
                    "-f", "null", "-"], capture_output=True, text=True).stderr
m = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r).group(0))
ln = (f"loudnorm=I=-11:TP=-1:LRA=9:linear=true:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
      f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{WORK}/plate_tmp.mov", "-af", ln + ",aresample=48000",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart",
                f"{PROJ}/assets/plate.mp4"], check=True)
print("keep", keep)
