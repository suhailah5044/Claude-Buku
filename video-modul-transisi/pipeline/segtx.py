import os
WORK = os.environ.get("WORK", "/home/user/work")  # folder kerja: audio/, tx/, edl/
import json, numpy as np, wave
from faster_whisper import WhisperModel
m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=4)
wf=wave.open(f"{WORK}/audio/final.wav"); a=np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(np.float32)/32768.0
mp=json.load(open(f"{WORK}/edl/map.json"))
for sg in mp:
    s,d=sg['start'],sg['dur']
    seg=a[int(s*16000):int((s+d)*16000)]
    r,_=m.transcribe(seg,language="ms",beam_size=5,word_timestamps=True,condition_on_previous_text=False,temperature=0)
    ws=[(w.word.strip(),round(w.start+s,2),round(w.end+s,2)) for x in r for w in x.words]
    print(f"[{sg['name']} {s:.2f}+{d:.2f}] "+" ".join(f"{w}[{a_:.2f}-{b:.2f}]" for w,a_,b in ws),flush=True)
