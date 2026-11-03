# Matematik SPM Final Boost (Cikgu Yasir) — 21 video TikTok pendek

Review buku, USP & persiapan akhir SPM. Audience: ibu ayah + pelajar Tingkatan 4 & 5.
TikTok/Reels 9:16, 1080×1920, 30 fps, 17–21 s setiap video. Dibina dengan **HyperFrames** (`videos/vNN/index.html`).

## Footage (Google Drive)

| Fail | Isi | Guna |
| --- | --- | --- |
| `INTRO/copy_*.mov` (10) | Voiceover hook (visual = skrin gambar produk) | VO intro (`i_*`) |
| `TENGAH/copy_*.mov` (3) | VO isi: bengkel kalkulator / soalan berpotensi tinggi / extra material | VO tengah (`t_*`) |
| `CTA/copy_*.mov` (5) | VO penutup | VO CTA (`c_*`) |
| `Footage.mov` | Review penuh 13 s (pegang buku) | VO + b-roll v21 |
| `IMG_1390–1409.MOV` (20) | Tangan + buku (cover, badge, isi kandungan, flip, spine), **senyap**, HDR HLG 4K 60 fps | B-roll (tone-map, **slow-mo 0.5×**) |
| `IMG_1367/1378.PNG`, `IMG_1382/1388.HEIC` | Screenshot kedai (harga, no. telefon) / foto | Tidak digunakan |

Semua klip dibaca betul (tiada cermin). Tiada muzik, suara sahaja.

## Pipeline

```bash
WORK=/home/user/wspm python3 pipeline/vo.py        # assets/vo/*.wav + pipeline/vo.json (jeda, 1.1x, compressor, transcribe semula)
WORK=/home/user/wspm python3 pipeline/broll.py     # assets/broll/*.mp4 (tone-map HLG, slow-mo 0.5x)
python3 pipeline/build.py [vNN ...]                # videos/vNN/ (index.html + compositions/gfx.html + sfx.json)
cd videos/vNN && npx hyperframes check && npx hyperframes render --quality delivery -o r.mp4
python3 pipeline/mux.py r.mp4 vNN final/SPM_Final_Boost_vNN.mp4 22   # audio -9.6 LUFS + toing, HEVC + sharpen
```

- `pipeline/build.py` — senarai 21 video (intro + tengah + CTA), shot b-roll, caption, zoom punch.
- `pipeline/shots.py` — perpustakaan shot + cue (setiap sebutan topik → shot buku sepadan, fade lembut 0.3 s) + `cy` ruang kosong.
- `pipeline/captions.py` — hook & caption (gaya #13: kotak gelap + border kuning, kecil, satu pada satu masa). Tiada teks "bakul/beg kuning".
- `pipeline/variety.py` — peraturan #14: hook lain, 3 versi ayat caption, b-roll lain, animasi masuk lain (pop/slide/drop/zoom/flip).
- Caption yang merentas shot dengan ruang kosong berbeza dipecah (bahagian 2 pindah, tanpa bunyi).

## Video

| # | Intro (hook) | Tengah | CTA |
| --- | --- | --- | --- |
| v01 | SPM dah makin dekat | Soalan berpotensi tinggi | Final preparation |
| v02 | SPM dah makin dekat | Bengkel kalkulator | Klik & tengok details |
| v03 | Jangan tunggu last minute | Extra material | Final preparation |
| v04 | Jangan tunggu last minute | Bengkel kalkulator | Masih ada masa |
| v05 | Skema jawapan | Soalan berpotensi tinggi | Checkout |
| v06 | Skema jawapan | Bengkel kalkulator | Parents consider |
| v07 | Bukan baca teori | Extra material | Checkout |
| v08 | Bukan baca teori | Soalan berpotensi tinggi | Final preparation |
| v09 | Susun ulangkaji | Soalan berpotensi tinggi | Checkout |
| v10 | Susun ulangkaji | Bengkel kalkulator | Klik & tengok details |
| v11 | Masih ada masa | Soalan berpotensi tinggi | Final preparation |
| v12 | Masih ada masa | Bengkel kalkulator | Masih ada masa |
| v13 | Latihan tak cukup | Bengkel kalkulator | Parents consider |
| v14 | Latihan tak cukup | Extra material | Final preparation |
| v15 | Kenapa saya tertarik | Bengkel kalkulator | Final preparation |
| v16 | Kenapa saya tertarik | Extra material | Checkout |
| v17 | Parents, anak ambil SPM | Soalan berpotensi tinggi | Final preparation |
| v18 | Parents, anak ambil SPM | Bengkel kalkulator | Checkout |
| v19 | Persiapan matematik SPM | Bengkel kalkulator | Final preparation |
| v20 | Persiapan matematik SPM | Extra material | Final preparation |
| v21 | Review penuh (Footage.mov) | — | Klik & tengok details |

Final: `final/SPM_Final_Boost_vNN.mp4` — link: `https://github.com/suhailah5044/Claude-Buku/raw/main/video-matematik-spm-final-boost/final/SPM_Final_Boost_vNN.mp4`
