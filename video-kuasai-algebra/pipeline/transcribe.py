import os
WORK = os.environ.get("WORK", "/home/user/work")  # folder kerja: audio/, tx/, edl/
import sys, json
from faster_whisper import WhisperModel
m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=4)
for name in sys.argv[1:]:
    import numpy as np, wave; wf=wave.open(f"{WORK}/audio/{name}.wav"); a=np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(np.float32)/32768.0
    segs, info = m.transcribe(a, language="ms", word_timestamps=True, vad_filter=False, beam_size=5)
    out=[]
    for s in segs:
        out.append({"start":s.start,"end":s.end,"text":s.text,"words":[{"w":w.word,"s":w.start,"e":w.end} for w in s.words]})
    json.dump(out, open(f"{WORK}/tx/{name}.json","w"), ensure_ascii=False, indent=1)
    print(name, "done", flush=True)
