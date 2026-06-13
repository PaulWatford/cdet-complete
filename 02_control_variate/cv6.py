import teneva, numpy as np, subprocess, math, sys
np.random.seed(0)
HARNESS="./oracle_hex"; beta=5.0; n=int(sys.argv[1]); R=4
G=2**R; xg=(np.arange(G)+0.5)/G
def c2s(xs):
    t=[];pv=0.;j=1.
    for i in range(n):
        sp=beta-pv;x=pv+sp*xs[i];j*=sp;t.append(x);pv=x
    return t,j
def dec(row):
    xs=[]
    for v in range(n):
        x=0
        for p in range(R): x=(x<<1)|int(row[p*n+v])
        xs.append(xg[x])
    return xs
def ev(rows):
    ts=[];js=[]
    for r in rows:
        t,j=c2s(dec(r));ts.append(t);js.append(j)
    inp="\n".join(" ".join(f"{x:.12f}" for x in t) for t in ts)+"\n"
    out=subprocess.run([HARNESS,str(n)],input=inp,capture_output=True,text=True).stdout
    return np.array([float(x) for x in out.split()])*np.array(js)
Y=teneva.cross(lambda I:ev(np.asarray(I)),teneva.rand([2]*(n*R),r=2,seed=0),m=250000,e=1e-12,nswp=100,dr_max=8,cache={})
Y=teneva.truncate(Y,e=1e-10)
mean_g=teneva.sum(Y)/ (G**n)            # EXACT mean of the control over the grid
# Monte Carlo sample of grid points to estimate correlation & achievable reduction
rng=np.random.default_rng(1); M=25000
idx=rng.integers(0,G,size=(M,n))
rows=[]
for r in idx:
    b=[0]*(n*R)
    for v in range(n):
        x=int(r[v])
        for p in range(R): b[p*n+v]=(x>>(R-1-p))&1
    rows.append(b)
f=ev(rows)
g=teneva.get_many(Y,np.array(rows))
rho=np.corrcoef(f,g)[0,1]; bstar=np.cov(f,g)[0,1]/np.var(g)
red=np.var(f)/np.var(f-bstar*g)
print("hexring n=%d : TCI acc=%.1f%%  corr=%.5f  variance_reduction=%.1fx  (theory %.1fx)"%(
    n, np.linalg.norm(g-f)/np.linalg.norm(f)*100, rho, red, 1/(1-rho**2)))
