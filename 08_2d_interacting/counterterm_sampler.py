"""v47 -- Fully stochastic shifted CDet: sample the mu-derivatives DIRECTLY in one run.
v46 got the shifted coefficients by re-running the engine on a mu-grid and finite-differencing. v47 removes
both: the one-body counterterm = d/dmu insertions are evaluated analytically per Monte-Carlo sample by a
contour in COMPLEX mu on the SAME sampled vertex configurations. So one set of vertex samples yields a_m and
ALL its mu-derivatives a_m^{(j)} at once -- no finite-difference bias, no mu-grid re-sampling -- and the v46
resummation b_n = sum_j (alpha^j/j!) U^(n-j) a_{n-j}^{(j)}(mu-alpha) gives the shifted coeffs in a single run.

The connected determinant C_V is a faithful Python port of the frozen engine (engine/cdet_engine.c:
D_corr/D_vac/Rossi recursion) -- validated: G0 reproduces lattice_G0 to 1e-16 and the quadrature-integrated
a_1 reproduces ED to 1e-16. Here C_V is vectorised over the complex-mu circle for cheap derivative extraction."""
import numpy as np
from math import factorial
from hubbard_ed import hop_1d_ring, exact_coeffs
from shifted_expansion import shifted_coeffs

class RingCDet:
    def __init__(self, L=2, beta=4.0, t=1.0, to=0.7, ti=0.2):
        self.L,self.beta,self.to,self.ti=L,beta,to,ti
        self.ev,self.U=np.linalg.eigh(hop_1d_ring(L,t))
    def g0(self,i,j,tu,muA):
        L,beta=self.L,self.beta; out=np.zeros(len(muA),complex); tt=tu
        while tt> beta: tt-=2*beta
        while tt<=-beta: tt+=2*beta
        for k in range(L):
            xi=self.ev[k]-muA; nf=1.0/(np.exp(beta*xi)+1.0)
            gk=np.where(tt>0,-(1.0-nf)*np.exp(-xi*tt),np.where(tt<0,nf*np.exp(-xi*tt),nf))
            out+=self.U[i,k]*self.U[j,k]*gk
        return out
    def _bdet(self,rs,rt,cs,ct,muA):
        m=len(rs)
        if m==0: return np.ones(len(muA),complex)
        M=np.empty((len(muA),m,m),complex)
        for a in range(m):
            for b in range(m): M[:,a,b]=self.g0(rs[a],cs[b],rt[a]-ct[b],muA)
        return np.linalg.det(M)
    def _Dcorr(self,V,muA):
        n=len(V); rs=[0]+[v[0] for v in V]; rt=[self.to]+[v[1] for v in V]
        cs=[0]+[v[0] for v in V]; ct=[self.ti]+[v[1] for v in V]
        du=self._bdet(rs,rt,cs,ct,muA); dd=np.ones(len(muA),complex)
        if n>0:
            s=[v[0] for v in V]; tt=[v[1] for v in V]; dd=self._bdet(s,tt,s,tt,muA)
        return ((-1)**n)*du*dd
    def _Dvac(self,V,muA):
        n=len(V)
        if n==0: return np.ones(len(muA),complex)
        s=[v[0] for v in V]; tt=[v[1] for v in V]; dA=self._bdet(s,tt,s,tt,muA); return ((-1)**n)*dA*dA
    def C_V(self,V,muA):
        n=len(V)
        if n==0: return self._Dcorr([],muA)
        N=1<<n; Dv=[None]*N; C=[None]*N
        for mask in range(N): Dv[mask]=self._Dvac([V[i] for i in range(n) if mask&(1<<i)],muA)
        for k in range(n+1):
            for mask in range(N):
                if bin(mask).count("1")!=k: continue
                val=self._Dcorr([V[i] for i in range(n) if mask&(1<<i)],muA).copy()
                sm=(mask-1)&mask
                while True:
                    if sm!=mask: val=val-C[sm]*Dv[mask^sm]
                    if sm==0: break
                    sm=(sm-1)&mask
                C[mask]=val
        return C[N-1]

def run(L=2,beta=4.0,to=0.7,ti=0.2,mu=1.1,U=4.0,alpha=1.5,rho=0.3,Mm=24,S1=120000,S2=60000,seed=1):
    cd=RingCDet(L,beta,1.0,to,ti); mu_ref=mu-alpha; tau=to-ti
    th=2*np.pi*np.arange(Mm)/Mm; circle=mu_ref+rho*np.exp(1j*th)
    def derivs(vals,jmax): return np.array([factorial(j)*np.sum(vals*np.exp(-1j*j*th))/(Mm*rho**j) for j in range(jmax+1)]).real
    def sample(m,S,jmax,sd):
        rng=np.random.default_rng(sd); acc=np.zeros(jmax+1); acc2=np.zeros(jmax+1); pref=(L*beta)**m/factorial(m)
        for _ in range(S):
            V=[(int(rng.integers(L)),float(rng.uniform(0,beta))) for _ in range(m)]
            d=derivs(cd.C_V(V,circle),jmax); acc+=d; acc2+=d*d
        mean=acc/S; return pref*mean, pref*np.sqrt(np.abs((acc2/S-mean**2)/S))
    a0=derivs(cd.C_V([],circle),2)                 # analytic (free G0), no sampling
    a1,a1e=sample(1,S1,1,seed); a2,a2e=sample(2,S2,0,seed+1)
    b1=U*a1[0]+alpha*a0[1]; b1e=U*a1e[0]
    b2=U**2*a2[0]+alpha*U*a1[1]+(alpha**2/2)*a0[2]; b2e=np.hypot(U**2*a2e[0],alpha*U*a1e[1])
    return dict(a1=a1,a1e=a1e,a2=a2,a2e=a2e,a0=a0,b1=b1,b1e=b1e,b2=b2,b2e=b2e,mu_ref=mu_ref,tau=tau,mu=mu,U=U,alpha=alpha,L=L,beta=beta)

if __name__=="__main__":
    R=run()
    hop=hop_1d_ring(R['L'],1.0)
    aED=exact_coeffs(hop,R['mu_ref'],R['beta'],R['tau'],2)
    # independent ED cross-check of the SAMPLED mu-derivative a1'
    from counterterm_shift import mu_derivs
    derED=mu_derivs(hop,R['mu_ref'],R['beta'],R['tau'],2)
    bED=shifted_coeffs(hop,R['mu'],R['beta'],R['tau'],R['U'],R['alpha'],2).real
    print("="*74); print("v47: FULLY STOCHASTIC shifted CDet -- mu-derivatives sampled DIRECTLY, one run"); print("="*74)
    print(f"2-site ring  mu={R['mu']} beta={R['beta']} U={R['U']} alpha={R['alpha']}  (sample at mu_ref={R['mu_ref']})\n")
    print("bare coeffs and their mu-derivative, sampled in ONE run (vs ED):")
    print(f"  a1   direct={R['a1'][0]:+.6f} +- {R['a1e'][0]:.6f}   ED={aED[1]:+.6f}   ({abs(R['a1'][0]-aED[1])/R['a1e'][0]:.1f} sigma)")
    print(f"  a1'  direct={R['a1'][1]:+.6f} +- {R['a1e'][1]:.6f}   ED={derED[1,1]:+.6f}   ({abs(R['a1'][1]-derED[1,1])/R['a1e'][1]:.1f} sigma)  <- mu-derivative, no FD")
    print(f"  a2   direct={R['a2'][0]:+.6f} +- {R['a2e'][0]:.6f}   ED={aED[2]:+.6f}   ({abs(R['a2'][0]-aED[2])/R['a2e'][0]:.1f} sigma)")
    print("\nshifted coeffs assembled from the ONE-RUN sampled mu-derivatives (vs ED shifted):")
    print(f"  b1   direct={R['b1']:+.5f} +- {R['b1e']:.5f}   ED={bED[1]:+.5f}   ({abs(R['b1']-bED[1])/R['b1e']:.1f} sigma)")
    print(f"  b2   direct={R['b2']:+.5f} +- {R['b2e']:.5f}   ED={bED[2]:+.5f}   ({abs(R['b2']-bED[2])/R['b2e']:.1f} sigma)")
    print("\nOne set of vertex samples -> a_m AND all a_m^{(j)} via the complex-mu contour: no finite-difference")
    print("bias, no mu-grid re-sampling. This is the production-form shifted CDet (v45 proof -> v46 engine -> v47 MC).")
