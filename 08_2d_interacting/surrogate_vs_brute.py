import numpy as np, subprocess, sys, time; sys.path.insert(0,'.')
from slice_scaling import FastCDet
from surrogate2 import feats2
from symmetry_reduction import cube_hopping
t0=time.time()
# ---- fresh OUT-OF-SAMPLE L=6 configs (seed unused by the trained refs) ----
rng=np.random.default_rng(90210); N=216
cfgs=[]
while len(cfgs)<40:
    c=sorted(int(x) for x in rng.choice(np.arange(1,N),3,replace=False))
    if len(set(c))==3: cfgs.append(c)
# feed configs to the C surrogate dumper
inp="".join(f"6 {c[0]} {c[1]} {c[2]}\n" for c in cfgs)+"END\n"
out=subprocess.run(['./surr_dump'],input=inp,capture_output=True,text=True).stdout
surr={}; stat={}; zpol=None
for ln in out.splitlines():
    p=ln.split()
    if p[0]=="MAG": surr[(int(p[2]),int(p[3]),int(p[4]))]=(float(p[5]),int(p[6]))
    elif p[0]=="STAT": stat[float(p[1])]={kv.split('=')[0]:float(kv.split('=')[1]) for kv in p[2:]}
    elif p[0]=="ZPOL": zpol=float(p[1])
# ---- BRUTE exact ln-magnitude truth (same convention: beta=4, mu=0.5, to=0.7, ti=0.2, NT high) ----
cd=FastCDet(cube_hopping(6),beta=4.0,to=0.7,ti=0.2)
print(f"[building brute ln-magnitude truth, NT=200, {len(cfgs)} configs...]",flush=True)
rng2=np.random.default_rng(7)
errs=[]; rows=[]
for c in cfgs:
    vals=[abs(cd.C_V([(s,float(rng2.uniform(0,4.0))) for s in c],0.5).real) for _ in range(200)]
    truth=float(np.log(np.mean(vals)))
    pred,sec=surr[tuple(c)]
    xerr=float(np.exp(abs(pred-truth)))
    errs.append(xerr); rows.append((c,truth,pred,xerr,sec))
errs=np.array(errs)
print(f"\n=== PART 1: ln-magnitude  SURROGATE(C) vs BRUTE(exact CDet), out-of-sample, {len(cfgs)} configs ===")
print(f"per-config x-error: median {np.median(errs):.2f}x  mean {errs.mean():.2f}x  90th pct {np.percentile(errs,90):.2f}x  max {errs.max():.2f}x")
print(f"claimed scope (csurrogate.h): median transfer ~1.7-2.3x.  -> {'WITHIN' if np.median(errs)<2.5 else 'EXCEEDS'} scope")
# correlation (is the ordering right?)
T=np.array([r[1] for r in rows]); P=np.array([r[2] for r in rows])
print(f"rank corr (spearman) surrogate vs truth: {np.corrcoef(np.argsort(np.argsort(T)),np.argsort(np.argsort(P)))[0,1]:.3f}")
# worst discrepancies (both directions)
order=np.argsort(errs)
print("worst 4 OVER-estimates (surrogate too HIGH) and worst 4 UNDER (too LOW):")
signed=[(r[2]-r[1],r) for r in rows]
for d,r in sorted(signed)[:4]:
    print(f"  UNDER {r[0]} truth {r[1]:+.2f} surr {r[2]:+.2f}  ({np.exp(abs(d)):.1f}x){'  [sector '+str(r[4])+']' if r[4] else ''}")
for d,r in sorted(signed)[-4:][::-1]:
    print(f"  OVER  {r[0]} truth {r[1]:+.2f} surr {r[2]:+.2f}  ({np.exp(abs(d)):.1f}x){'  [sector '+str(r[4])+']' if r[4] else ''}")
print(f"[{time.time()-t0:.0f}s]")
import json; json.dump({"errs":errs.tolist(),"zpol":zpol,"stat":{str(k):v for k,v in stat.items()}},open('sxs1.json','w'))

# PART 2/3 (statics, carriers, sector, L=8) and the C dumper build are documented in
# SURROGATE_VS_BRUTE_RESULT.md; this script carries PART 1 (the magnitude accuracy test) as the
# reusable out-of-sample gate. Build the dumper: gcc -O2 -I. -o surr_dump <dumper> csurrogate.c -lm
