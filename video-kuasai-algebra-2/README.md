# Kuasai Algebra — versi voiceover (edit semula)

Sumber: video 29 s (voiceover + muzik latar atas klip halaman buku, ada bar hitam & teks lama dibakar).

Apa yang dibuat:
- Crop tengah 810×1440 → 1080×1920 penuh skrin (bar hitam dibuang), sharpen ringan.
- Muzik latar dibuang: suara diasingkan dengan Demucs (`htdemucs_ft`, stem vokal).
- Jeda > 0.1 s dipendekkan ke 0.08 s, speed 1.1x, -14 LUFS. Tiada muzik / SFX.
- Teks lama (0–4.4 s) ditutup oleh kotak hook (kelihatan dari frame pertama).
- Teks putih Montserrat 900 + aksen #FFC21A, kinetic type & zoom punch.

| Fail | Isi |
| --- | --- |
| `pipeline/plate.py` | Jana `assets/plate.mp4` (perlu `WORK` = folder dengan `raw/f1.mov` + `work/audio/sep_vocals.wav`) |
| `pipeline/build.py` | Jana `index.html` + `compositions/s1.html` (semua teks & timing) |
| `pipeline/gfx.py` | Gaya grafik dikongsi dari `video-kuasai-algebra` |
| `final/` | Video final |

```bash
python3 pipeline/build.py && npx hyperframes check && npx hyperframes render --quality delivery -o out.mp4
```
