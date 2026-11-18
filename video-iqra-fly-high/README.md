# IQRA' Fly High (Kenal • Dengar • Faham) — video TikTok USP

Footage dah diedit pengguna (CapCut, 50.8 s, HLG, **tanpa VO**; audio = audio bonus dari telefon 10.2–16.1 s).
TikTok 9:16, 1080×1920, 30 fps. Dibina dengan **HyperFrames** (`index.html`).

## Gaya (Gaya IQRA')
- Ikut contoh TikTok pengguna: teks masuk **blur-in perkataan demi perkataan**, terapung perlahan, keluar blur-out.
- Font **Chewy** (padan screenshot "Vlogger." CapCut), putih + outline coklat gelap + bayang; perkataan penting **kuning #FFC21A**;
  bintang kecil berkelip (soft highlight). Saiz sederhana (~60 px, tajuk 92 px) — "50%".
- Satu USP pada satu masa, di ruang kosong (meja atas buku / bawah kiri masa shot telefon). Tiada kotak.
- Shot cover dipegang (36.6–43.7 s): tiada overlay — cover dah ada tajuk, produk jadi fokus.
- Kamera: zoom perlahan 1.0↔1.035 setiap shot + blur lembut 0.26 s pada setiap potongan. Warna footage **tidak diubah** (HLG→SDR terus, peraturan #20).
- SFX dari folder Drive pengguna (`assets/sfx/`: whoosh, swoosh, pop ×5, sparkle, shimmer) + selak kertas sintetik lembut pada setiap page flip. Tiada muzik.

## USP (masa)
| Masa | Shot | Overlay |
| --- | --- | --- |
| 0–3.3 | Halaman huruf | **IQRA' Fly High** + Kenal • Dengar • Faham (hook, nampak dari frame 0) |
| 3.6–6.4 | Cover atas meja | Warna Menarik, Anak Lebih Fokus |
| 7.0–10.1 | Halaman Alif (singa, telinga) | Kenal Huruf Melalui Gambar |
| 10.4–13.1 | Telefon main audio | Bonus Audio Disediakan |
| 13.3–16.0 | Telefon main audio | Baca Sambil Dengar Audio |
| 16.4–18.9 | Halaman Kha | Ilustrasi Comel & Berwarna |
| 19.2–22.2 | Halaman Za/Dho (zarafatun, zuhuurun…) | Contoh Perkataan Bahasa Arab |
| 23.6–25.8 | Halaman Makhraj Huruf | Panduan Makhraj Huruf |
| 26.0–28.3 | Halaman huruf besar | Huruf Hijaiyah Besar & Jelas |
| 44.3–50.8 | Selak halaman berwarna | Konsep Kenal, Dengar & Faham |

## Pipeline
```bash
python3 pipeline/build.py                       # index.html + sfx.json
npx hyperframes check && npx hyperframes render --quality delivery --sdr --video-frame-format png -o r.mp4
python3 pipeline/mux.py r.mp4 final/IQRA_Fly_High.mp4   # audio telefon (-12 LUFS segmen) + SFX, H.264 crf 18
```
`assets/footage.mp4` = `zscale` HLG→SDR footage asal (tidak di-commit).
