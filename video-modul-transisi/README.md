# Modul Transisi Tahun 1 Edisi 2027 — video TikTok affiliate

Audience: ibu ayah yang anak bakal masuk Tahun 1 sesi 2027. TikTok 9:16, 1080×1920, 30 fps, ~87 s.
Suara asal Sue (tiada muzik / SFX), speed 1.1x, -14 LUFS.

## Footage (Google Drive)

| Klip | Isi | Guna |
| --- | --- | --- |
| `9c573.mov` | Talking head: hook → soalan kemahiran → 10–15 minit → 5 subjek → 4M | A-roll bahagian 1 |
| `4ed94.mov` | Talking head: menaakul → video tutorial & jawapan | A-roll bahagian 2 |
| `dfe55.mov` | Talking head: teman anak → okay/lemah → persediaan awal → CTA | A-roll bahagian 3 |
| `IMG_1272–1280.MOV` | iPhone 4K HDR (HLG): cover, kandungan, suku kata, flip halaman | B-roll (tone-map ke SDR) |
| `ScreenRecording…mp4` | Scroll PDF buku (Prabaca A–Z, vokal, matematik, Bahasa Arab…) | B-roll halaman |
| `IMG_1271.MOV` | Gelap / kabur | Tidak digunakan |

Semua klip SDR tidak terbalik (tulisan buku dibaca betul). Klip IMG_* ialah HLG BT.2020 → tone-map dengan filter yang dipersetujui.

## Pipeline

```bash
WORK=/home/user/work python3 pipeline/aroll.py    # assets/aroll.mp4 + pipeline/edl.json
WORK=/home/user/work python3 pipeline/broll.py    # assets/broll/*.mp4
python3 pipeline/segcheck.py                       # transcribe semula setiap segmen -> pipeline/words.json
python3 pipeline/build.py                          # index.html + compositions/gfx.html
npx hyperframes check && npx hyperframes render --quality delivery -o out.mp4
```

- `pipeline/aroll.py` — senarai take terbaik (ulangan, false start, "Okay" di awal dibuang), jeda > 0.1 s → 0.08 s, potongan pada grid frame (tiada drift A/V).
- `pipeline/build.py` — semua teks, 5 pop-up info, b-roll (fade 0.3 s + ken burns perlahan), zoom punch. Masa = saat mutlak pada `assets/aroll.mp4`.
- Teks hanya di band atas (bumbung kereta), tidak menutup muka atau buku. Tiada teks atas cover buku semasa b-roll cover.
- `assets/aroll.mp4` dalam repo dienkod semula (CRF 21) supaya bawah had 100 MB GitHub.
