import teneva, numpy as np, subprocess, itertools, math
np.random.seed(0)
HARNESS="./oracle_hex"; beta=5.0; n=4; R=4
G=2**R; xg=(np.arange(G)+0.5)/G; perm=[p*n+v for v in range(n) for p in range(R)]
def dec(row):
    xs=[]
    for v in range(n):
        x=0
        for p in range(R): x=(x<<1)|int(row[p*n+v])
        xs.append(xg[x])
    return xs
def c2s(xs):
    t=[];pv=0.;j=1.
    for i in range(n):
        sp=beta-pv;x=pv+sp*xs[i];j*=sp;t.append(x);pv=x
    return t,j
def ev(rows):
    ts=[];js=[]
    for r in rows:
        t,j=c2s(dec(r));ts.append(t);js.append(j)
    inp="\n".join(" ".join(f"{x:.12f}" for x in t) for t in ts)+"\n"
    out=subprocess.run([HARNESS,str(n)],input=inp,capture_output=True,text=True).stdout
    return np.array([float(x) for x in out.split()])*np.array(js)
# build TCI control g
Y=teneva.cross(lambda I:ev(np.asarray(I)),teneva.rand([2]*(n*R),r=2,seed=0),m=200000,e=1e-12,nswp=120,dr_max=10,cache={})
Y=teneva.truncate(Y,e=1e-10)
# exact grid arrays: f (brute force) and g (TCI reconstruction), aligned
allr=[]
for idx in itertools.product(range(G),repeat=n):
    b=[0]*(n*R)
    for v in range(n):
        x=idx[v]
        for p in range(R): b[p*n+v]=(x>>(R-1-p))&1
    allr.append(b)
f=ev(allr)
g=np.transpose(teneva.full(Y).reshape([2]*(n*R)),perm).reshape(-1)
N=len(f)
mean_f=f.mean(); mean_g=g.mean()          # mean_g is EXACT (known from TCI)
rho=np.corrcoef(f,g)[0,1]
bstar=np.cov(f,g)[0,1]/np.var(g)
res1=f-g; resb=f-bstar*g
print("hexring n=4  (TCI control variate, surrogate that plateaued at 24%)")
print("  exact grid mean (target) = %.6e"%mean_f)
print("  TCI surrogate accuracy   = %.1f%% (pointwise) -> NOT accurate"%(np.linalg.norm(g-f)/np.linalg.norm(f)*100))
print("  correlation f,g          = %.5f"%rho)
print("  EXACT variance reduction (the achievable MC speedup):")
print("    plain MC          var=%.3e"%np.var(f))
print("    CV beta=1         var=%.3e   -> %.1fx fewer samples"%(np.var(res1),np.var(f)/np.var(res1)))
print("    CV beta*=%.3f     var=%.3e   -> %.1fx fewer samples"%(bstar,np.var(resb),np.var(f)/np.var(resb)))
print("    theory 1/(1-rho^2)= %.1fx"%(1/(1-rho**2)))
# sampling demo: real error bars at fixed sample budgets (200 repeats)
rng=np.random.default_rng(0)
print("\n  sampling demo (RMS error of the integral-mean over 200 runs):")
print("  %8s %14s %14s %10s"%("samples","plain MC err","CV-MC err","speedup"))
for M in [200,2000,20000]:
    pe=[];ce=[]
    for _ in range(200):
        s=rng.integers(0,N,M)
        pe.append(f[s].mean()-mean_f)                       # plain
        ce.append((mean_g + (f[s]-bstar*g[s]).mean()) - mean_f)  # control variate
    pe=np.std(pe);ce=np.std(ce)
    print("  %8d %14.3e %14.3e %9.1fx"%(M,pe,ce,(pe/ce)**2))
