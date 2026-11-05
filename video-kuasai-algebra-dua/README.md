# Kuasai Algebra — "Dua" (gaya Reel AI Edit)

Sumber: `Dua.MOV` (Drive, 26.6 s) — video CapCut pengguna: b-roll buku Kuasai Algebra + VO, tiada muzik.
HDR HLG → tone-map standard. Speed 1.1x. End card CapCut (24.5 s) dibuang; frame akhir ditahan untuk hujung "kuning".
Final 22.7 s, 1080×1920, 30 fps.

## Gaya "Reel AI Edit" (rujukan pengguna: iklan VGC "Footage Raw vs Hasil AI Edit")
- Caption kecil HURUF BESAR Montserrat 800 putih + perkataan kuning `#FFC21A`, tanpa kotak, atas (y≈250), gradient gelap atas.
- Tajuk besar font condensed **Anton** di bawahnya — masuk zoom-blur + zoom punch kamera.
- Senarai bernombor (01, 02…): baris kaca gelap, ikon garis, baris aktif = bar kiri kuning + perkataan kuning. Nombor topik ikut Kandungan buku.
- SFX bertukar: whoosh/selak kertas setiap shot baru, pop/click setiap overlay. Tiada teks "beg kuning".

## Pipeline
```bash
python3 pipeline/build.py                       # index.html + sfx.json (masa = masa asal Dua.MOV / 1.1)
npx hyperframes check && npx hyperframes render --quality delivery -o r.mp4
python3 pipeline/mux.py r.mp4 final/Kuasai_Algebra_Dua.mp4   # VO ~-9.6 LUFS + SFX
```
Aset (`assets/aroll.mp4`, `assets/vo.wav`) dijana dari Dua.MOV — lihat arahan ffmpeg dalam README ini:
`tm.mp4` (tone-map) → `trim=0:24.5,tpad=clone 0.5,setpts=PTS/1.1`; audio `atrim=0:24.95,highpass=75,atempo=1.1`.
