#!/usr/bin/env python3
"""Blur semua QR code / barcode dalam footage (permintaan pengguna).

Setiap segmen: kotak QR ditanda pada frame rujukan (manual + pengesan WeChat QR), kemudian dijejak ke setiap frame
dengan homography SIFT (halaman buku = satah) -> blur Gaussian kuat dengan tepi lembut. Warna lain tidak diusik.
Segmen selak laju 43.67-45.5 s (kandungan/Hijaiyyah lalu sekejap) TIDAK dijejak -> jangan guna dalam video (USE_OK).

Guna: python3 -I pipeline/qrblur.py <footage.mov> <out.mp4> [--debug dir]
"""
import sys, os, json, subprocess
import numpy as np, cv2
W, H, N = 1080, 1920, 1523
HL = "zscale=tin=arib-std-b67:pin=bt2020:min=bt2020nc:rin=tv:t=arib-std-b67:p=bt709:m=bt709:r=tv,format=bgr24"
BOX = lambda x0, y0, x1, y1: [[x0, y0], [x1, y0], [x1, y1], [x0, y1]]
# (frame_mula, frame_tamat_eksklusif, frame_rujukan, [quad...]) - quad dalam koordinat frame rujukan
SEGS = [
    (0, 104, 30, [BOX(0, 318, 80, 432)]),                                   # halaman awal: QR 'video pembelajaran' bucu kiri
    (104, 195, 135, ["det"]),                                               # cover atas meja: QR BONUS
    (195, 306, 204, [BOX(145, 1145, 305, 1305)]),                           # Huruf Hijaiyyah: QR video pembelajaran
    (702, 777, 735, ["det"]),                                               # Makhraj Huruf
    (851, 1023, 900, ["det", BOX(445, 990, 535, 1077), BOX(807, 937, 897, 1025), BOX(825, 1040, 913, 1127),
                      BOX(460, 1093, 547, 1181), BOX(655, 1170, 745, 1255)]),  # Kandungan: 9 QR
    (1097, 1310, 1140, ["det"]),                                            # cover dipegang
]
USE_OK_NOTE = "Elak 43.67-45.5 s (QR lalu laju masa selak)."

def det_quads(frame):
    wd = cv2.wechat_qrcode_WeChatQRCode(*[f"{os.environ.get('WC', 'wc')}/{f}" for f in
                                          ("detect.prototxt", "detect.caffemodel", "sr.prototxt", "sr.caffemodel")])
    _, pts = wd.detectAndDecode(frame)
    return [p.tolist() for p in pts]

def read_frames(src):
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-i", src, "-vf", HL, "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], stdout=subprocess.PIPE)
    while True:
        b = p.stdout.read(W * H * 3)
        if len(b) < W * H * 3: break
        yield np.frombuffer(b, np.uint8).reshape(H, W, 3)

def track(frames, refs, segs):
    sift = cv2.SIFT_create(2500)
    bf = cv2.BFMatcher()
    S = 0.5
    def feat(g):   # g = kelabu separuh resolusi
        return sift.detectAndCompute(g, None)
    def homog(fa, fb):
        (ka, da), (kb, db) = fa, fb
        if da is None or db is None or len(ka) < 8 or len(kb) < 8: return None, 0
        m = [a for a, b in bf.knnMatch(da, db, k=2) if a.distance < 0.75 * b.distance]
        if len(m) < 12: return None, 0
        pa = np.float32([ka[x.queryIdx].pt for x in m]) / S; pb = np.float32([kb[x.trainIdx].pt for x in m]) / S
        Hm, inl = cv2.findHomography(pa, pb, cv2.RANSAC, 6.0)
        return Hm, int(inl.sum()) if inl is not None else 0
    quads = {}
    for a, b, r, qs in segs:
        fr = feat(frames[r])
        base = []
        for q in qs:
            if q == "det": base += det_quads(refs[r])
            else: base.append(q)
        base = [np.float32(q) for q in base]
        Hprev, fprev = np.eye(3), fr
        order = list(range(r, b)) + list(range(r - 1, a - 1, -1))
        for i in order:
            if i == r - 1: Hprev, fprev = np.eye(3), fr
            fi = feat(frames[i])
            Hd, nd = homog(fr, fi)
            if nd >= 40: Hc = Hd
            else:
                Hs, ns = homog(fprev, fi)
                Hc = Hs @ Hprev if ns >= 15 else Hprev
            Hprev, fprev = Hc, fi
            quads[i] = [cv2.perspectiveTransform(q[None], Hc)[0].tolist() for q in base]
    return quads

def blur_frame(img, qs):
    if not qs: return img
    mask = np.zeros((H, W), np.float32)
    for q in qs:
        q = np.float32(q); c = q.mean(0); q = c + (q - c) * 1.28        # besarkan 28% (margin)
        cv2.fillConvexPoly(mask, q.astype(np.int32), 1.0)
    mask = cv2.GaussianBlur(mask, (0, 0), 7)[..., None]
    x0, y0, w, h = cv2.boundingRect((mask[..., 0] > 0.01).astype(np.uint8))
    pad = 40; x0, y0 = max(0, x0 - pad), max(0, y0 - pad); x1, y1 = min(W, x0 + w + 2 * pad), min(H, y0 + h + 2 * pad)
    roi = img[y0:y1, x0:x1]
    small = cv2.resize(roi, None, fx=0.12, fy=0.12, interpolation=cv2.INTER_AREA)
    bl = cv2.GaussianBlur(cv2.resize(small, (roi.shape[1], roi.shape[0]), interpolation=cv2.INTER_LINEAR), (0, 0), 9)
    out = img.copy(); m = mask[y0:y1, x0:x1]
    out[y0:y1, x0:x1] = (roi * (1 - m) + bl * m).astype(np.uint8)
    return out

if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    dbg = sys.argv[4] if len(sys.argv) > 4 and sys.argv[3] == "--debug" else None
    need = {i for a, b, r, _ in SEGS for i in range(a, b)}; refs_i = {r for *_, r, _ in SEGS}
    frames, refs = {}, {}
    for i, f in enumerate(read_frames(src)):
        if i in need: frames[i] = cv2.cvtColor(cv2.resize(f, None, fx=.5, fy=.5, interpolation=cv2.INTER_AREA), cv2.COLOR_BGR2GRAY)
        if i in refs_i: refs[i] = f.copy()
    print("frames", len(frames))
    quads = track(frames, refs, SEGS)
    del frames
    json.dump(quads, open(os.path.splitext(dst)[0] + "_quads.json", "w"))
    enc = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", "30", "-i", "-",
                            "-c:v", "libx264", "-crf", "13", "-preset", "medium", "-pix_fmt", "yuv420p", "-g", "30",
                            "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709", dst], stdin=subprocess.PIPE)
    for i, f in enumerate(read_frames(src)):
        o = blur_frame(f, quads.get(i, []))
        if dbg and i % 6 == 0 and i in quads:
            d = o.copy()
            for q in quads[i]: cv2.polylines(d, [np.int32(q)], True, (0, 255, 0), 3)
            cv2.imwrite(f"{dbg}/{i:04d}.jpg", cv2.resize(d, (270, 480)))
        enc.stdin.write(o.tobytes())
    enc.stdin.close(); enc.wait(); print("ok", dst, len(quads), "frame ada QR")
