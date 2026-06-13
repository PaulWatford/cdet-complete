import numpy as np, subprocess
beta,mu,t=5.0,0.3,1.0
def G0_ring(i,j,tau,L):
    k=np.arange(L); eps=-2*t*np.cos(2*np.pi*k/L)-mu; nF=1.0/(np.exp(beta*eps)+1)
    if i==j and tau==0.0:
        return np.mean(nF)*1.0   # tau->0^- density convention (matches engine)
    s=1.0; tt=tau
    while tt>=beta: tt-=beta; s=-s
    while tt<0: tt+=beta; s=-s
    g=-(1-nF)*np.exp(-eps*tt)
    return s*(1.0/L)*np.sum(np.cos(2*np.pi*k*(i-j)/L)*g)
# revalidate L=6 incl diagonal
def gmat_engine(v):
    inp="".join(f"{si} {ta:.6f}\n" for si,ta in v)
    out=subprocess.run(["./gdump_ring","6",str(len(v))],input=inp,capture_output=True,text=True).stdout
    return np.array([[float(x) for x in r.split()] for r in out.strip().split("\n")])
v=[(0,0.5),(3,2.5),(1,1.1),(4,3.9),(2,0.8),(5,0.0)]
Ge=gmat_engine(v); Gp=np.array([[G0_ring(si,sj,ti-tj,6) for (sj,tj) in v] for (si,ti) in v])
print("L=6 full validation vs engine (incl diagonal): max diff %.2e  %s\n"%(np.max(np.abs(Ge-Gp)),"MATCH" if np.max(np.abs(Ge-Gp))<1e-9 else "FAIL"))

# THE TEST: two clusters of m vertices, A near site 0, B near site L/2 (max ring separation).
# Measure cross-block coupling magnitude AND numerical rank vs lattice size L.
print("Fast-multipole criterion: is the far-field coupling block LOW RANK?")
print("(low rank << m  =>  bulk compresses, your decomposition works at scale)\n")
print("%4s %4s %8s %14s %12s %14s"%("L","m","sep","||G_AB||","rank(G_AB)","singular values"))
m=8
rng=np.random.default_rng(0)
for L in [6,16,32,64,128]:
    sep=L//2
    # cluster A: sites 0..3 near origin, random times; B: same local pattern near site L/2
    sitesA=[i%4 for i in range(m)]
    sitesB=[(sep+i%4) for i in range(m)]
    tA=rng.uniform(0.2,4.8,m); tB=rng.uniform(0.2,4.8,m)
    GAB=np.array([[G0_ring(sa,sb,ta-tb,L) for (sb,tb) in zip(sitesB,tB)] for (sa,ta) in zip(sitesA,tA)])
    s=np.linalg.svd(GAB,compute_uv=False)
    rank=int((s>s[0]*1e-10).sum())
    svstr=" ".join("%.1e"%x for x in s[:5])
    print("%4d %4d %8d %14.3e %12d   %s"%(L,m,sep,np.linalg.norm(GAB),rank,svstr))
