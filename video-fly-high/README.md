# Fly High — Mengenal, Membaca & Membunyikan Suku Kata (Buku 1–5)

Video TikTok 9:16, 1080×1920, 30 fps, ~49 s. Footage dah diedit pengguna (CapCut: VO + cut), diedit semula dengan **HyperFrames**.

## Bahan (Google Drive)
- Footage: `copy_84152051-….mov` (HLG/Dolby Vision 8.4, 54 s)
- Font rujukan: screenshot CapCut "Vlogger." → **Lilita One** (paling hampir)
- Gaya kelebihan: `Style 1 - .PNG` (label kecil + tajuk KELEBIHAN DIA + pil putih + baris ikon + background blur)
- SFX: folder pengguna (`v24044….mp4`, dipecah kepada 22 bunyi `assets/sfx/sNN.wav`; bunyi boom/bass kuat tak diguna)
- Rujukan gaya: TikTok (teks pop + zoom punch), guideline "UGC Product Showcase + Cute Educational + Clean"

## Pipeline
```bash
python3 pipeline/prep.py footage.mov   # assets/aroll.mp4 + assets/vo.wav (hook dipindah ke depan, tone-map, 1.1x, EQ suara)
python3 pipeline/build.py              # index.html + sfx.json
npx --yes hyperframes@0.9.6 check && npx --yes hyperframes@0.9.6 render --quality delivery -o r.mp4
python3 pipeline/mux.py r.mp4 final/FlyHigh_v01.mp4   # suara ~-9.6 LUFS + SFX
```

## Keputusan
- Hook: segmen "Kita tengah belajar membaca, memang kena mula daripada asas…" dipindah ke depan (asal 20.0–24.6 s).
- Warna: tone-map HLG→SDR (mobius) tanpa eq/filter — kekal warna buku asal.
- Subtitle Montserrat 900 italic kecil di bawah (y≈1490); USP di atas (y≈170–420) — zon berasingan.
- Kelebihan (gaya Style 1) masa "bukan sekadar kenal huruf… langkah demi langkah".
- Tiada teks "beg kuning". Tiada muzik (tiada fail muzik diberi).

## Varian v03–v12 (`pipeline/variants.py`)
Hook terkuat di depan, susunan/panjang/ayat USP/animasi berbeza. USP + subtitle dalam kotak kaca blur gelap;
USP y≈250, subtitle y≈1390 (tak terlalu atas/bawah). Segmen dipotong pada titik senyap sebenar.

| # | Hook (suara) | Teks hook | Panjang |
| --- | --- | --- | --- |
| v03 | Kalau ibu ayah tengah cari bahan latihan membaca… | CARI BAHAN LATIHAN MEMBACA? | 23 s |
| v04 | Ini ada lima tahap tau… | 5 TAHAP BELAJAR MEMBACA | 27 s |
| v05 | Bukan sekadar kenal huruf… | BUKAN SEKADAR KENAL HURUF | 27 s |
| v06 | Kalau ibu ayah tengah cari bahan… | BAHAN LATIHAN MEMBACA DI RUMAH | 24 s |
| v07 | Ini buku keluaran Fly High… | MENGENAL, MEMBACA & MEMBUNYIKAN SUKU KATA | 25 s |
| v08 | Kena mula daripada asas… | BELAJAR MEMBACA MULA DARI ASAS | 27 s |
| v09 | Bukan sekadar kenal huruf… | LANGKAH DEMI LANGKAH | 23 s |
| v10 | Ini ada lima tahap tau… | SAMPAI BACA AYAT & CERITA | 26 s |
| v11 | Kalau ibu ayah tengah cari bahan… | BUKU LATIHAN MEMBACA ANAK? | 27 s |
| v12 | Kena mula daripada asas… | MULA DARI ASAS | 31 s |
