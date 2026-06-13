"""Pin the engine's order<->U convention against ED on small clusters (1D ring L=4 and 2D square 2x2),
then the SAME convention must hold for both -- that consistency is the validation. Builds H=H0+U*Hint
once per cluster, re-diagonalizes per U, fits the Taylor series of the local G(0,0;tau;U)."""
import numpy as np, subprocess
from hubbard_ed import hop_1d_ring, hop_2d_square

def pieces(hop, mu, beta):
    N=hop.shape[0]; M=2*N; dim=1<<M
    par=lambda s,p:(-1.0 if bin(s&((1<<p)-1)).count("1")&1 else 1.0)
    def cdag(s,p): return (None,0.0) if s>>p&1 else (s|(1<<p),par(s,p))
    def c(s,p):    return (s&~(1<<p),par(s,p)) if s>>p&1 else (None,0.0)
    def opmat(op,p):
        Mx=np.zeros((dim,dim))
        for s in range(dim):
            s2,sg=op(s,p)
            if s2 is not None: Mx[s2,s]=sg
        return Mx
    H0=np.zeros((dim,dim)); Hint=np.zeros(dim)
    for s in range(dim):
        H0[s,s]+=-mu*bin(s).count("1")
        Hint[s]=sum(1 for i in range(N) if (s>>i&1)and(s>>(i+N)&1))
        for spin in (0,1):
            off=spin*N
            for i in range(N):
                for j in range(N):
                    if i==j or hop[i,j]==0: continue
                    sj,p1=c(s,j+off)
                    if sj is None: continue
                    si,p2=cdag(sj,i+off)
                    if si is None: continue
                    H0[si,s]+=hop[i,j]*p1*p2
    return H0,Hint,opmat(c,0),opmat(cdag,0)

def Gloc(H0,Hint,c0,c0d,U,beta,tau):
    E,V=np.linalg.eigh(H0+U*np.diag(Hint)); Z=np.exp(-beta*E).sum()
    ci=V.T@c0@V; cjd=V.T@c0d@V; w=np.exp(-beta*E)/Z
    return -np.sum(w[:,None]*np.exp(tau*np.subtract.outer(E,E))*(ci*cjd.T))

def taylor(hop,mu,beta,tau,Us):
    H0,Hint,c0,c0d=pieces(hop,mu,beta)
    G=np.array([Gloc(H0,Hint,c0,c0d,U,beta,tau) for U in Us])
    return np.polyfit(Us,G,deg=6)[::-1]   # a0,a1,a2,...

if __name__=="__main__":
    beta,mu,t,to,ti=4.0,0.5,1.0,0.7,0.2; tau=to-ti
    Us=np.linspace(-0.06,0.06,13)
    def eng(args):
        out=subprocess.run(["./cdet_small"]+args,capture_output=True,text=True).stdout.split()
        return [float(x) for x in out]
    for name,hop,args in [("1D ring L=4",hop_1d_ring(4),["ring","4",str(beta),str(mu),str(t),str(to),str(ti)]),
                          ("2D square 2x2",hop_2d_square(2,2),["sq","2","2",str(beta),str(mu),str(t),str(to),str(ti)])]:
        a=taylor(hop,mu,beta,tau,Us); G0,c1,c2=eng(args)
        print(f"\n{name}:")
        print(f"  ED   : a0={a[0]:+.12f}  a1={a[1]:+.12f}  a2={a[2]:+.12f}")
        print(f"  engine: G0={G0:+.12f}  cdet1={c1:+.12f}  cdet2={c2:+.12f}")
        print(f"  ratios: a0/G0={a[0]/G0:+.8f}   cdet1/a1={c1/a[1]:+.8f}   cdet2/a2={c2/a[2]:+.8f}")
