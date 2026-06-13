import numpy as np, subprocess
def CV(L,n,configs):
    inp="".join("".join(f"{s} {t:.6f} " for s,t in cfg)+"\n" for cfg in configs)
    out=subprocess.run(["./oracle_ring",str(L),str(n)],input=inp,capture_output=True,text=True).stdout
    return np.array([float(x) for x in out.split()])
rng=np.random.default_rng(3); L=48; ncfg=25
print("Order-axis test: does locality suppress HIGH ORDER, or only spatial spreading?")
print("compact = all n vertices on 3 sites {0,1,2} (within one correlation volume).")
print("spread  = half on sites {0,1,2}, half on far sites {24,25,26}.\n")
print("%4s %16s %16s %12s"%("order n","med|C_compact|","med|C_spread|","spread/compact"))
for n in [4,6,8,10,12]:
    half=n//2
    comp=[]; spr=[]
    for _ in range(ncfg):
        taus=rng.uniform(0.1,4.9,n)
        comp.append([(i%3,taus[i]) for i in range(n)])
        spr.append([(i%3,taus[i]) for i in range(half)]+[(24+i%3,taus[half+i]) for i in range(n-half)])
    Cc=np.abs(CV(L,n,comp)); Cs=np.abs(CV(L,n,spr))
    mc=np.median(Cc); ms=np.median(Cs)
    print("%4d %16.4e %16.4e %12.2e"%(n,mc,ms,ms/mc if mc>0 else float('nan')))
print("\nIf med|C_compact| stays healthy as n grows -> compact high-order diagrams")
print("genuinely contribute -> you still pay full 2^n. Locality = SIZE axis, not ORDER axis.")
