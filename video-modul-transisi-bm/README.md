# Modul Transisi — Bahasa Melayu (KV / KVK), talking head

Sumber: `export_1794355878860.mov` (Drive, 207 s, SDR bt709, 1080×1920 30 fps) — talking head + buku di tangan, banyak take ulang.
Final ~65 s, 1080×1920, 30 fps. Gaya **Reel** (ikut Kuasai Algebra Dua): caption kecil + tajuk Anton + senarai kaca gelap, SFX bertukar-tukar.

## Suntingan
- Take terbaik setiap ayat (`pipeline/aroll.py` → `SEG`); buang "Okay" di awal, ulangan "dalam modul ni ada…", "sebelum masuk,", "saya tak tahu nak sebut macam mana", sembang tepi ("bungkus…", "terima kasih…") dan take CTA yang tersangkut.
- Jeda > 0.1 s → 0.08 s, potong dalam senyap, fade 10 ms, speed 1.1x. Setiap segmen ditranscribe semula (`condition_on_previous_text=False`) untuk semak hujung perkataan.
- Warna/cahaya asal (tiada eq / sharpen) — full range → tv sahaja.
- Semua teks di ruang gelap atas kepala (y ≈ 170–330): tak tutup muka atau buku.
- Contoh BAS: B = konsonan, A = vokal, S = konsonan (KVK) — ikut sebutan pengguna.
- Tiada teks "bakul kuning"; CTA guna ayat pengguna "boleh ambil set yang ini".

## Pipeline
```bash
RAW=/home/user/raw-mtbm python3 pipeline/aroll.py   # RAW/src.mov + RAW/a16.wav -> assets/aroll.mp4 + assets/vo.wav + pipeline/edl.json
python3 pipeline/build.py                            # index.html + sfx.json
npx hyperframes check && npx hyperframes render --quality delivery -o r.mp4
python3 pipeline/mux.py r.mp4 final/Modul_Transisi_BM.mp4   # VO ~-9.6 LUFS + SFX
```
