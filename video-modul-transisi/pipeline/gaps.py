import json, numpy as np, wave, sys
from faster_whisper import WhisperModel
m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=4)
def load(n):
    wf=wave.open(f"/home/user/work/audio/{n}.wav"); return np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(np.float32)/32768.0
for spec in sys.argv[1:]:
    n,s,e=spec.split(':'); s=float(s); e=float(e); a=load(n)[int(s*16000):int(e*16000)]
    r,_=m.transcribe(a,language="ms",beam_size=5,word_timestamps=True,condition_on_previous_text=False,temperature=0,vad_filter=False)
    print(spec, " ".join(f"{w.word.strip()}[{w.start+s:.2f}-{w.end+s:.2f}]" for x in r for w in x.words), flush=True)
