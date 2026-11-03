# Claude-Buku — panduan untuk Claude

Repo ini untuk video TikTok review buku (biasanya buku latihan sekolah) oleh pemilik repo.
Contoh siap: `video-kuasai-algebra/` (projek HyperFrames + pipeline + 10 video final).
Untuk footage baru, ikut gaya dan proses di bawah melainkan pengguna minta lain.
Balas pengguna dalam Bahasa Melayu santai.

## Brief standard (guna kalau pengguna tak nyatakan)

- TikTok 9:16, 1080×1920, 30 fps. Audience: ibu ayah & pelajar sekolah menengah.
- **Tiada muzik, tiada SFX.** Suara sahaja, jelas, -14 LUFS.
- Buang jeda (semua senyap > ~0.1 s dipendekkan ke ~0.08 s), ayat ulang, false start, filler ("So,", "Okey,") di awal ayat. Kemudian **speed 1.1x** (`atempo=1.1`, pitch kekal).
- Hook paling kuat di depan. Teks hook mesti kelihatan dari frame pertama (thumbnail).
- B-roll halaman buku **full screen 2–3 s dengan fade lembut** setiap kali pengguna sebut topik/halaman buku, kemudian balik ke muka.
- Teks: **putih, bold (Montserrat 800/900)**, aksen kuning mustard `#FFC21A`. Letak **di atas kepala atau tepi sahaja — jangan tutup muka atau buku di tangan**. Kinetic type, zoom punch pada point penting, pop-up info. Energy tinggi tapi kemas.
- Tunjuk preview dulu; render final HD hanya bila pengguna setuju.
- Lepas video utama siap, pengguna biasanya minta **9 varian hook** (lihat `pipeline/variants.py`).

## Peraturan yang pengguna dah tetapkan (penting)

1. **Jangan sebut / tunjuk jalan kira dari mulut pengguna.** Pengguna tak yakin dengan matematik. Buang segmen suara yang mengira langkah demi langkah. Kalau nak tunjuk jalan kerja, paparkan sebagai grafik **sama persis macam notasi dalam buku** (contoh: `5(x − 4) = (5 × x) − (5 × 4) = 5x − 20`), bukan versi sendiri.
2. **Semak matematik** sebelum letak dalam grafik. Kalau ragu, jangan letak.
3. Jangan letak teks peraturan/konsep yang mengelirukan (cth "NOMBOR LUAR × SETIAP SEBUTAN" ditolak). Pilih teks ringkas yang orang biasa faham.
4. **Semak ayat berulang dengan teliti** — Whisper kadang-kadang gabungkan ulangan (cth "Nampak tak? Okey, nampak tak..."). Transcribe semula hasil potongan setiap segmen dengan `condition_on_previous_text=False` dan dengar semula bahagian yang mencurigakan.
5. Jangan potong terlalu rapat — hujung perkataan mesti penuh (suara "putus-putus" ditolak). Potong hanya dalam senyap; fade 8–12 ms sahaja.
6. CTA guna ayat pengguna sendiri; tiada overlay "beg kuning". Ayat yang disukai: "IBU AYAH, JUST CONSIDER!".

## Semakan footage (buat setiap kali)

- **Klip cermin/terbalik:** selfie kadang-kadang direkod mirror. Crop kawasan buku pada resolusi penuh dan baca tulisan; kalau terbalik, `hflip`.
- **HDR iPhone:** `ffprobe` — kalau `arib-std-b67` / `bt2020` (HLG 10-bit), **wajib tone-map**, jangan tukar terus (jadi flat & pudar). Filter yang pengguna setuju:
  ```
  zscale=tin=arib-std-b67:pin=bt2020:min=bt2020nc:rin=tv:t=linear:npl=203,format=gbrpf32le,zscale=p=bt709,tonemap=mobius:param=0.3:desat=0,zscale=t=bt709:m=bt709:r=tv,format=yuv420p,eq=contrast=1.08:saturation=1.12
  ```
  Klip SDR `yuvj420p` (full range) boleh terus ke `yuv420p`.
- Klip senyap (Whisper keluar "Terima kasih kerana menonton") = tiada suara; abaikan atau guna sebagai b-roll.

## Alat & tip teknikal

- **Muat turun dari Google Drive** (folder dikongsi): senarai fail dengan Drive MCP `search_files` (`parentId = '<folderId>'`), kemudian
  `curl -L -o f.mov "https://drive.usercontent.google.com/download?id=<fileId>&export=download&confirm=t"`. Jangan guna `download_file_content` untuk video besar.
- **Transcribe:** `pip install faster-whisper`, model `medium`, `language="ms"`, `word_timestamps=True`. Versi `av` dalam container rosak dengan path fail — **bagi audio sebagai numpy array** (baca WAV 16 kHz mono). Whisper salah dengar "darab"→"darat", "Kuasai Algebra"→"Kuasa Ijibran"; abaikan, ia isu transkripsi sahaja.
- **HyperFrames:** `npx skills add heygen-com/hyperframes` (skill lokal). MCP `compose` tak boleh edit footage sendiri. Pipeline: `pipeline/build.py` jana `index.html` + `compositions/`, kemudian `npx hyperframes check --json`, `snapshot`, `render --quality draft|delivery`.
- Layout: A-roll diturunkan 140 px (`gsap y:140`) supaya ada band header gelap beranimasi ~170–450 px di atas kepala untuk teks. Snapshot dulu untuk pastikan teks tak kena muka/buku.
- Render di container ni ~5–40 min untuk ~70 s; jalankan di latar belakang.
- **Loudness:** 2-pass `loudnorm=I=-14:TP=-1.5:LRA=11:linear=true` + `highpass=f=75,afftdn=nr=8:nf=-40`.

## Simpan & hantar

- Simpan projek + video final dalam repo ini (folder baru setiap buku, cth `video-<nama-buku>/`). Jangan commit footage mentah `.MOV`, `.hyperframes/`, `.media/`.
- **Had GitHub 100 MB setiap fail** — encode semula video final `-crf 19 -preset slow -movflags +faststart` (~75 MB untuk 69 s) sebelum commit. Tulis fail separuh siap di luar repo dulu.
- Repo ini **public**. Bagi pengguna link download terus:
  `https://github.com/suhailah5044/Claude-Buku/raw/main/<path>.mp4`
  dan uji link (`curl -sI -L`) selepas push.
- Pengguna guna telefon; fail dalam chat kadang-kadang tak boleh download — sentiasa bagi link repo.
