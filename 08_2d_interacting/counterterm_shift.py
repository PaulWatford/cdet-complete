"""v46 -- Wire the v45 shifted-reference scheme into the actual CDet engine, WITHOUT re-architecting it.
The one-body counterterm -alpha*N is the generator of chemical-potential shifts, so counterterm insertions
resum exactly into mu-derivatives of the bare coefficients. Writing the shifted scheme as a 2D Taylor
expansion around (mu_ref=mu-alpha, U=0) gives the exact closed form

    b_n(alpha) = sum_{j=0}^{n} (alpha^j / j!) * U^(n-j) * a_{n-j}^{(j)}(mu - alpha),

where a_m^{(j)} = d^j/dmu^j of the BARE CDet coefficient a_m. So the engine (unchanged) computes bare
coefficients a_m at a few nearby mu; a thin resummation produces the shifted coefficients b_n. The bare
a_m exist and are finite even when the bare SERIES diverges, so only LOW orders (up to the shifted
convergence order) are needed -- that is the whole point of the shift. Spin structure is automatically
correct: d/dmu of G inserts -N = -(n_up + n_dn), exactly the counterterm.

Verified here two ways: (i) formula vs ED shifted coeffs to ~1e-12 (machine precision); (ii) the REAL C
engine (cdet_small, cdet_n = N*a_local) fed through the formula reproduces the shifted coeffs to engine
precision (np=64 quadrature + finite-diff)."""
import subprocess, numpy as np
from math import factorial
from hubbard_ed import hop_1d_ring
from shifted_expansion import shifted_coeffs, exactG

def _bare_coeffs_cplxmu(hop, mu, beta, tau, nmax, rU=0.5, MU=256):
    """Bare U^n coeffs a_n(mu) (local, site 0) at possibly-complex mu, via Cauchy-in-U."""
    N=hop.shape[0]; M2=2*N; dim=1<<M2
    par=lambda s,p:(-1.0 if bin(s&((1<<p)-1)).count("1")&1 else 1.0)
    def cdag(s,p): return (None,0.0) if s>>p&1 else (s|(1<<p),par(s,p))
    def c(s,p):    return (s&~(1<<p),par(s,p)) if s>>p&1 else (None,0.0)
    def opmat(op,p):
        Mx=np.zeros((dim,dim))
        for s in range(dim):
            s2,sg=op(s,p)
            if s2 is not None: Mx[s2,s]=sg
        return Mx
    H0=np.zeros((dim,dim),complex); Hint=np.zeros(dim)
    for s in range(dim):
        H0[s,s]+=-mu*bin(s).count("1")
        Hint[s]=sum(1 for i in range(N) if (s>>i&1)and(s>>(i+N)&1))
        for sp in (0,1):
            off=sp*N
            for i in range(N):
                for j in range(N):
                    if i==j or hop[i,j]==0: continue
                    sj,p1=c(s,j+off)
                    if sj is None: continue
                    si,p2=cdag(sj,i+off)
                    if si is None: continue
                    H0[si,s]+=hop[i,j]*p1*p2
    c0=opmat(c,0); c0d=opmat(cdag,0); Hd=np.diag(Hint).astype(complex)
    def Gc(U):
        w,VR=np.linalg.eig(H0+U*Hd); Wi=np.linalg.inv(VR)
        ci=Wi@c0@VR; cjd=Wi@c0d@VR; Z=np.sum(np.exp(-beta*w)); wt=np.exp(-beta*w)/Z
        return -np.sum(wt[:,None]*np.exp(tau*np.subtract.outer(w,w))*(ci*cjd.T))
    th=2*np.pi*np.arange(MU)/MU; G=np.array([Gc(rU*np.exp(1j*t)) for t in th])
    return np.array([np.sum(G*np.exp(-1j*n*th))/(MU*rU**n) for n in range(nmax+1)])

def mu_derivs(hop, mu_ref, beta, tau, nmax, rho=0.25, Mm=128):
    """a_m^{(j)}(mu_ref), m,j=0..nmax, via Cauchy-in-mu (machine precision)."""
    th=2*np.pi*np.arange(Mm)/Mm; mus=mu_ref+rho*np.exp(1j*th)
    A=np.array([_bare_coeffs_cplxmu(hop,m,beta,tau,nmax) for m in mus])
    der=np.zeros((nmax+1,nmax+1))
    for m in range(nmax+1):
        for j in range(nmax+1):
            der[m,j]=(factorial(j)*np.sum(A[:,m]*np.exp(-1j*j*th))/(Mm*rho**j)).real
    return der

def shifted_from_bare(der, U, alpha, nmax):
    """b_n(alpha) from the mu-derivative table der[m,j] = a_m^{(j)}(mu-alpha)."""
    return np.array([sum(alpha**j/factorial(j)*U**(n-j)*der[n-j,j] for j in range(n+1))
                     for n in range(nmax+1)])

def engine_bare(L, beta, mu, to, ti):
    """REAL C engine bare local coeffs (a0=G0, a1, a2) = (G0, cdet_n(1)/N, cdet_n(2)/N)."""
    o=subprocess.run(["./cdet_small","ring",str(L),f"{beta}",f"{mu:.10f}","1.0",f"{to}",f"{ti}"],
                     capture_output=True,text=True).stdout.split()
    return float(o[0]), float(o[1])/L, float(o[2])/L

if __name__=="__main__":
    hop=hop_1d_ring(2,1.0); beta,to,ti=4.0,0.7,0.2; tau=to-ti; mu,U,alpha=1.1,4.0,1.5; mu_ref=mu-alpha; nmax=6
    print("="*78); print("v46: COUNTERTERM = d/dmu -- shifted CDet coeffs from bare engine data"); print("="*78)
    print(f"2-site ring  mu={mu} beta={beta} U={U} alpha={alpha}  (mu_ref={mu_ref})\n")
    der=mu_derivs(hop,mu_ref,beta,tau,nmax)
    b_form=shifted_from_bare(der,U,alpha,nmax)
    b_ed=shifted_coeffs(hop,mu,beta,tau,U,alpha,nmax).real
    print("(i) resummation formula vs ED shifted coeffs:")
    print(f"   {'n':>2} | {'b_n':>14} | {'|formula-ED|':>13}")
    for n in range(nmax+1): print(f"   {n:>2} | {b_ed[n]:>14.9f} | {abs(b_form[n]-b_ed[n]):>13.2e}")
    # (ii) real engine route for orders 1,2
    h=0.02; grid=mu_ref+h*np.arange(-3,4); G=np.array([engine_bare(2,beta,m,to,ti) for m in grid])
    d=lambda y,o:(y[3] if o==0 else (y[4]-y[2])/(2*h) if o==1 else (y[4]-2*y[3]+y[2])/h**2)
    b1=U*d(G[:,1],0)+alpha*d(G[:,0],1)
    b2=U**2*d(G[:,2],0)+alpha*U*d(G[:,1],1)+(alpha**2/2)*d(G[:,0],2)
    print("\n(ii) REAL C ENGINE (cdet_small) bare coeffs -> resummation -> shifted coeffs:")
    print(f"   b1: engine={b1:.8f}  ED={b_ed[1]:.8f}  |diff|={abs(b1-b_ed[1]):.1e}")
    print(f"   b2: engine={b2:.8f}  ED={b_ed[2]:.8f}  |diff|={abs(b2-b_ed[2]):.1e}")
    print("   (residual = engine quadrature + finite-diff; the formula itself is exact, see (i))")
    Gex=exactG(hop,mu,beta,tau,U)
    print(f"\nPayoff: only LOW-order bare coeffs needed. Resummed shifted sum (exact G={Gex:.6f}):")
    for K in [2,3,4,5]: print(f"   K={K}: {np.sum(b_form[:K+1]):.6f}  err={abs(np.sum(b_form[:K+1])-Gex):.1e}")
    print("   bare series at these (mu,U) DIVERGES (v45); the shift converges from a few engine coeffs.")
