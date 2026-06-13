"""cdet_stable_engine_dump.py (v109) -- regenerates spectrum_l6.bin (the exact cube_hopping L=6
spectrum the stable C engine reads) and cdet_stable_engine_refs.txt (Python reference C_V values for
the engine's `val` self-check). Run: python3 cdet_stable_engine_dump.py. The .bin ships with the
engine (like golden.json); this regenerates it from the Python source."""
import numpy as np, sys, struct; sys.path.insert(0,'.')
from symmetry_reduction import cube_hopping
from stable_cdet import StableFrozen
H=cube_hopping(6); ev,U=np.linalg.eigh(H); N=len(ev)
# dump spectrum (binary: N int32, then N float64 ev, then N*N float64 U row-major)
with open('spectrum_l6.bin','wb') as f:  # regenerates the C engine's spectrum data
    f.write(struct.pack('i',N))
    f.write(ev.astype('<f8').tobytes())
    f.write(np.ascontiguousarray(U,dtype='<f8').tobytes())
print(f"dumped spectrum_l6.bin: N={N}, {4+8*N+8*N*N} bytes")
# reference frozen C_V values for C-engine validation (v99 freeze: occ=1, probe=2)
mu=1.845; beta=36.0
refs=[]
for s in (0.0, 0.002):
    cd=StableFrozen(H,beta=beta,occ=1.0,probe=2.0,s=s,mode='v99')
    for cfg,taus in [((1,2,4),(34.8,35.0,35.7)),((7,30,101),(5.0,18.0,33.0)),((3,88,150),(34.1,35.7,35.9))]:
        V=[(cfg[i],taus[i]) for i in range(3)]
        val=cd.C_V(V,mu).real
        refs.append((s,cfg,taus,val))
        print(f"  s={s} cfg={cfg} taus={taus}: C_V={val:.10e}")
# write refs to a C header for the validation test
with open('cdet_stable_engine_refs.txt','w') as f:
    for s,cfg,taus,val in refs:
        f.write(f"{s} {cfg[0]} {cfg[1]} {cfg[2]} {taus[0]} {taus[1]} {taus[2]} {val:.15e}\n")
print("refs written")
