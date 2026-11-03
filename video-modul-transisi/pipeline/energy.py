import numpy as np, wave, sys
def load(n):
    wf=wave.open(f"/home/user/work/audio/{n}.wav"); return np.frombuffer(wf.readframes(wf.getnframes()),dtype=np.int16).astype(np.float32)/32768.0
cache={}
for spec in sys.argv[1:]:
    n,s,e=spec.split(':'); s=float(s); e=float(e)
    a=cache.setdefault(n,load(n))
    out=[]
    t=s
    while t<e:
        seg=a[int(t*16000):int((t+0.02)*16000)]
        db=20*np.log10(np.sqrt(np.mean(seg**2))+1e-9)
        out.append(f"{db:.0f}")
        t+=0.02
    print(spec, ' '.join(out))
