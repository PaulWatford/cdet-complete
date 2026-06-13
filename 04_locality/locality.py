import numpy as np, subprocess
def CV(L,n,configs):
    inp="".join("".join(f"{s} {t:.6f} " for s,t in cfg)+"\n" for cfg in configs)
    out=subprocess.run(["./oracle_ring",str(L),str(n)],input=inp,capture_output=True,text=True).stdout
    return np.array([float(x) for x in out.split()])
rng=np.random.default_rng(0)
n=8; half=n//2; ncfg=30
print("Locality test on the real engine (exact C_V), order n=%d."%n)
print("compact = all %d vertices near site 0 ; spread = %d near site 0, %d at far side (L/2)."%(n,half,half))
print("ratio = |C_spread| / |C_compact|  (paired same times). ratio->0 means connected diagrams are LOCAL.\n")
print("%4s %6s %16s %16s %12s"%("L","sep","median|C_compact|","median|C_spread|","ratio"))
for L in [6,12,24,48,96,192]:
    sep=L//2
    compact=[]; spread=[]
    for _ in range(ncfg):
        taus=rng.uniform(0.1,4.9,n)
        cc=[(i%4, taus[i]) for i in range(n)]                                  # all near 0
        sp=[(i%4, taus[i]) for i in range(half)]+[(sep+(i%4), taus[half+i]) for i in range(half)]
        compact.append(cc); spread.append(sp)
    Cc=np.abs(CV(L,n,compact)); Cs=np.abs(CV(L,n,spread))
    mc=np.median(Cc); ms=np.median(Cs)
    print("%4d %6d %16.4e %16.4e %12.2e"%(L,sep,mc,ms,ms/mc if mc>0 else float('nan')))
