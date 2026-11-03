# Claude-Buku

Projek video TikTok (9:16) review buku **Kuasai Algebra** (teknik FastMaths), dibina dengan [HyperFrames](https://github.com/heygen-com/hyperframes).

Audience: ibu ayah & pelajar sekolah menengah.

## `video-kuasai-algebra/`

Projek HyperFrames (HTML → video, 1080×1920, 30 fps, ~69 s).

| Fail | Isi |
| --- | --- |
| `index.html` | Root: A-roll (muka), 5 b-roll full screen dengan fade, latar header beranimasi, zoom punch |
| `compositions/s1,s3,s4,s5.html` | Grafik ikut bahagian: Hook/Intro (+ jalan kerja ikut buku), Teknik, Kelebihan, CTA |
| `assets/aroll.mp4` | Talking-head yang dah disunting: jeda & ulangan dibuang, filler dibuang, speed 1.1x, suara -14 LUFS, tiada muzik |
| `assets/broll/` | Klip halaman buku (Kembangan, Kandungan, Latihan + QR) |
| `pipeline/build.py` | Penjana `index.html` + `compositions/` — semua teks, timing overlay & b-roll ditetapkan di sini |
| `pipeline/edl/` | Senarai potongan (v1 → v2 → v3) dan peta masa |
| `pipeline/transcripts/` | Transcript Whisper (Bahasa Melayu) setiap klip asal |

### Guna

```bash
cd video-kuasai-algebra
```

```bash
python3 pipeline/build.py
```

```bash
npx hyperframes check
```

```bash
npx hyperframes preview
```

```bash
npx hyperframes render --quality delivery -o kuasai-algebra.mp4
```

Perlukan Node.js 22+ dan FFmpeg.

### Nota

- Klip asal `5ef3a963.mov` dirakam terbalik (cermin) dan telah di-flip.
- B-roll iPhone asal adalah HDR (HLG, BT.2020 10-bit). Ditukar ke SDR BT.709 dengan `zscale` + `tonemap=mobius` + `eq=contrast=1.08:saturation=1.12` supaya kekal punchy, tidak flat:
  `zscale=tin=arib-std-b67:pin=bt2020:min=bt2020nc:t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,eq=contrast=1.08:saturation=1.12`
- `assets/aroll.mp4` dalam repo dienkod CRF 21 supaya muat had 100 MB GitHub (timing sama dengan versi kerja).
- Footage mentah asal ada dalam folder Google Drive; tidak disimpan di sini.

## `video-kuasai-algebra-2/`

Edit semula video voiceover Kuasai Algebra (25.6 s): muzik latar dibuang (Demucs), bar hitam dibuang, jeda dipendekkan, 1.1x, -11 LUFS,
caption kecil di ruang kosong, CTA "MEMANG RECOMMEND!". Final: `video-kuasai-algebra-2/final/Kuasai_Algebra_v2_FINAL_HD.mp4`.
Lihat `video-kuasai-algebra-2/README.md`.
