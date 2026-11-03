# Claude-Buku

Projek video TikTok (9:16) review buku **Kuasai Algebra** (teknik FastMaths), dibina dengan [HyperFrames](https://github.com/heygen-com/hyperframes).

Audience: ibu ayah & pelajar sekolah menengah.

## `video-kuasai-algebra/`

Projek HyperFrames (HTML → video, 1080×1920, 30 fps, ~85 s).

| Fail | Isi |
| --- | --- |
| `index.html` | Root: A-roll (muka), 6 b-roll full screen dengan fade, latar header beranimasi, zoom punch |
| `compositions/s1–s5.html` | Grafik ikut bahagian: Hook/Intro, Jalan Kira, Teknik, Kelebihan, CTA |
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
- `assets/aroll.mp4` dalam repo dienkod CRF 21 supaya muat had 100 MB GitHub (timing sama dengan versi kerja).
- Footage mentah asal ada dalam folder Google Drive; tidak disimpan di sini.
