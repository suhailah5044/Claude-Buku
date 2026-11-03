import json, numpy as np, wave
from faster_whisper import WhisperModel
m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=4)
wf=wave.open("/home/user/work/audio/final.wav"); a=np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(np.float32)/32768.0
e=json.load(open("/home/user/Claude-Buku/video-modul-transisi/pipeline/edl.json"))
W=[]
for sg in e["segments"]:
    s,t=sg['start'],sg['end']; seg=a[int(s*16000):int(t*16000)]
    r,_=m.transcribe(seg,language="ms",beam_size=5,word_timestamps=True,condition_on_previous_text=False,temperature=0)
    r=list(r); W+= [{"w":w.word.strip(),"s":round(w.start+s,3),"e":round(w.end+s,3),"seg":sg["seg"]} for x in r for w in x.words]
    print(f"[{sg['seg']:2d} {s:6.2f}-{t:6.2f}] "+" ".join(f"{w.word.strip()}[{w.start+s:.2f}]" for x in r for w in x.words),flush=True)

json.dump(W,open("/home/user/Claude-Buku/video-modul-transisi/pipeline/words.json","w"),ensure_ascii=False,indent=0)
