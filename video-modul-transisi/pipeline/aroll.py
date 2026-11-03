#!/usr/bin/env python3
"""Jana assets/aroll.mp4 daripada 3 klip talking-head (9c573 -> 4ed94 -> dfe55).
- SEG: take terbaik setiap ayat (ulangan, false start, 'Okay' di awal dibuang)
- dalam setiap SEG, senyap > 0.1 s (-38 dB) dipendekkan ke 0.08 s (potong di tengah senyap)
- fade 10 ms setiap potongan, speed 1.1x (atempo, pitch kekal), highpass + afftdn + compressor, loudnorm 2-pass -11 LUFS / TP -1 (pengguna minta audio kuat)
Perlu: $WORK/raw/<klip>.mov dan $WORK/audio/<klip>.wav (16 kHz mono, untuk silencedetect)."""
import os, json, subprocess, re
WORK = os.environ.get("WORK", "/home/user/work")
HERE = os.path.dirname(os.path.abspath(__file__)); PROJ = os.path.dirname(HERE)
SEG = [  # (klip, mula, tamat, label)
    ("9c573", 9.90, 14.80, "hook: ibu ayah yang ada anak 6 tahun, next year nak masuk tahun 1 kan?"),
    ("9c573", 15.22, 19.44, "Kak Su nak cakap dekat rumah, anak dah kenal huruf A to Z ke belum"),
    ("9c573", 22.40, 28.61, "suku kata mudah / menulis / nombor & kiraan asas"),
    ("9c573", 30.29, 39.47, "sebab kadang-kadang kita ingat anak dah okey ... mana yang belum kuasai"),
    ("9c573", 46.17, 50.80, "sebab tu saya rasa penting ... persediaan daripada sekarang"),
    ("9c573", 53.90, 62.96, "kita bukan nak paksa anak belajar berjam-jam ... ikut kemampuan anak"),
    ("9c573", 68.95, 73.82, "saya nak share satu modul transisi tahun 1 edisi 2027"),
    ("9c573", 76.30, 84.06, "dalam satu buku ni ada 5 subjek ..."),
    ("9c573", 87.85, 95.20, "kemahiran 4M: membaca, menulis, mengira, menaakul"),
    ("4ed94", 8.76, 14.31, "menaakul bantu anak belajar berfikir, kenal corak, cari jawapan"),
    ("4ed94", 30.00, 32.92, "paling menarik modul ni siap dengan video tutorial sekali"),
    ("4ed94", 35.90, 37.42, "dan juga jawapan"),
    ("dfe55", 12.95, 18.37, "mak ayah boleh teman anak ... tahap penguasaan anak"),
    ("dfe55", 18.45, 20.35, "mana yang dah okey, kita teruskan"),
    ("dfe55", 23.40, 25.96, "mana yang masih lemah, kita bantu praktis lagi"),
    ("dfe55", 41.42, 51.45, "persediaan awal ni bukan bermaksud ... lebih yakin"),
    ("dfe55", 52.42, 53.04, "bila anak tu"),
    ("dfe55", 53.14, 54.59, "melangkah ke tahun 1 (buang 'tu' berulang)"),
    ("dfe55", 62.95, 71.61, "CTA: jadi kalau anak korang next year masuk tahun 1 ... bakul kuning"),
]
CLIPS = {"9c573": "9c573.mov", "4ed94": "4ed94.mov", "dfe55": "dfe55.mov"}
GAP_IN = 0.10; KEEP_GAP = 0.08; PAD = KEEP_GAP / 2

def silences(clip):
    r = subprocess.run(["ffmpeg", "-i", f"{WORK}/audio/{clip}.wav", "-af", "silencedetect=n=-38dB:d=0.08", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    st = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", r)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", r)]
    return list(zip(st, en))

SIL = {c: silences(c) for c in CLIPS}
pieces = []  # (klip, a, b, seg_index)
for si, (c, s, e, _) in enumerate(SEG):
    cur = s
    for a, b in SIL[c]:
        if b - a > GAP_IN and a > s and b < e:
            pieces.append((c, cur, round(a + PAD, 3), si)); cur = round(b - PAD, 3)
    pieces.append((c, cur, e, si))
F = 1 / 30  # snap ke grid frame supaya tempoh audio = video (tiada drift A/V)
pieces = [(c, round(round(a / F) * F, 4), round(round(b / F) * F, 4), si) for c, a, b, si in pieces]
pieces = [p for p in pieces if p[2] - p[1] > 0.05]

# peta masa: setiap SEG -> masa mula/tamat dalam aroll (selepas 1.1x)
t = 0.0; segmap = {}
for c, a, b, si in pieces:
    d = (b - a) / 1.1
    m = segmap.setdefault(si, {"seg": si, "label": SEG[si][3], "start": round(t, 3)})
    t += d; m["end"] = round(t, 3)
json.dump({"pieces": pieces, "segments": list(segmap.values()), "dur": round(t, 3)},
          open(f"{HERE}/edl.json", "w"), indent=1, ensure_ascii=False)

import concurrent.futures as cf
PD = f"{WORK}/pieces"; os.makedirs(PD, exist_ok=True)
def cut(i):
    c, a, b, _ = pieces[i]; d = b - a
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{a:.3f}", "-i", f"{WORK}/raw/{CLIPS[c]}", "-t", f"{d:.3f}",
        "-vf", "fps=30,scale=1080:1920:in_range=pc:out_range=tv,format=yuv420p,setsar=1",
        "-af", f"aformat=sample_rates=48000:channel_layouts=mono,afade=t=in:d=0.01,afade=t=out:st={d-0.01:.3f}:d=0.01,apad,atrim=0:{d:.4f}",
        "-c:v", "libx264", "-crf", "14", "-preset", "fast", "-c:a", "pcm_s16le", f"{PD}/p{i:03d}.mov"], check=True)
with cf.ThreadPoolExecutor(4) as ex: list(ex.map(cut, range(len(pieces))))
n = len(pieces)
open(f"{PD}/list.txt", "w").write("".join(f"file 'p{i:03d}.mov'\n" for i in range(n)))
tmp = f"{WORK}/aroll_tmp.mov"
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", f"{PD}/list.txt",
    "-vf", "setpts=PTS/1.1,fps=30", "-af", "highpass=f=75,afftdn=nr=8:nf=-40,atempo=1.1,acompressor=threshold=-20dB:ratio=3:attack=5:release=80:makeup=2",
    "-c:v", "libx264", "-crf", "16", "-preset", "medium", "-c:a", "pcm_s16le", tmp], check=True)
r = subprocess.run(["ffmpeg", "-i", tmp, "-af", "loudnorm=I=-11:TP=-1:LRA=9:print_format=json", "-f", "null", "-"],
                   capture_output=True, text=True).stderr
m = json.loads(re.search(r"\{[^{}]*\"input_i\"[^{}]*\}", r).group(0))
ln = (f"loudnorm=I=-11:TP=-1:LRA=9:linear=true:measured_I={m['input_i']}:measured_TP={m['input_tp']}:"
      f"measured_LRA={m['input_lra']}:measured_thresh={m['input_thresh']}:offset={m['target_offset']}")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", tmp, "-af", ln + ",aresample=48000", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", f"{WORK}/aroll.mp4"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{WORK}/aroll.mp4", "-ac", "1", "-ar", "16000", f"{WORK}/audio/final.wav"], check=True)
print("pieces", n, "dur", round(t, 2))
