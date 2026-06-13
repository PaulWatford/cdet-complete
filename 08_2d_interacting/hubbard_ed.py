"""Exact diagonalization of the small-cluster Hubbard model, grand-canonical, finite-T.
Computes G_sigma(i,j;tau) = -<T c_i(tau) c_j^dag(0)> via the Lehmann representation, in the SAME
sign/convention as the engine's lattice_G0 (verified in the U=0 limit). Used as the independent anchor
for the 2D connected-determinant order coefficients. Works for any cluster given its hopping matrix."""
import numpy as np
from itertools import product

def hop_1d_ring(L, t=1.0):
    H=np.zeros((L,L))
    for i in range(L):
        H[i,(i+1)%L]-=t; H[(i+1)%L,i]-=t
    return H

def hop_2d_square(Lx,Ly,t=1.0):
    N=Lx*Ly; H=np.zeros((N,N))
    idx=lambda x,y:(y%Ly)*Lx+(x%Lx)
    for x in range(Lx):
        for y in range(Ly):
            i=idx(x,y)
            for dx,dy in [(1,0),(0,1)]:
                j=idx(x+dx,y+dy); H[i,j]-=t; H[j,i]-=t
    return H

class HubbardED:
    """Modes 0..N-1 = up on each site, N..2N-1 = down. Fock basis = all 2^(2N) bitstrings."""
    def __init__(self, hop, U, mu, beta):
        self.N=hop.shape[0]; self.U=U; self.mu=mu; self.beta=beta; self.hop=hop
        M=2*self.N; self.M=M; self.dim=1<<M
        self._build()
    def _parity(self, state, p):           # JW sign: (-1)^(occupied modes < p)
        return -1.0 if bin(state & ((1<<p)-1)).count("1")&1 else 1.0
    def _cdag(self, state, p):
        if state>>p & 1: return None,0.0
        return state|(1<<p), self._parity(state,p)
    def _c(self, state, p):
        if not (state>>p & 1): return None,0.0
        return state&~(1<<p), self._parity(state,p)
    def _build(self):
        N,M,dim,t,U,mu=self.N,self.M,self.dim,self.hop,self.U,self.mu
        H=np.zeros((dim,dim))
        for s in range(dim):
            # diagonal: -mu * Ntot + U * sum_i n_i up n_i down
            ntot=bin(s).count("1")
            dbl=sum(1 for i in range(N) if (s>>i&1) and (s>>(i+N)&1))
            H[s,s]+= -mu*ntot + U*dbl
            # hopping: -t_{ij} c_i^dag c_j for both spins (t is hopping matrix incl. -t already)
            for spin in (0,1):
                off=spin*N
                for i in range(N):
                    for j in range(N):
                        if i==j or t[i,j]==0: continue
                        sj,p1=self._c(s,j+off)
                        if sj is None: continue
                        si,p2=self._cdag(sj,i+off)
                        if si is None: continue
                        H[si,s]+= t[i,j]*p1*p2     # t[i,j] = -t for neighbors
        self.E,self.V=np.linalg.eigh(H)
        self.Z=np.sum(np.exp(-self.beta*self.E))
    def _op_matrix(self, op, p):
        dim=self.dim; rows=[];cols=[];vals=[]
        for s in range(dim):
            s2,sign=op(s,p)
            if s2 is not None: rows.append(s2);cols.append(s);vals.append(sign)
        Mx=np.zeros((dim,dim))
        for r,c,v in zip(rows,cols,vals): Mx[r,c]=v
        return Mx
    def G(self, i, j, tau, spin=0):
        """G_ij(tau) = -<T c_i(tau) c_j^dag(0)>, 0<tau<beta, in engine convention."""
        off=spin*self.N
        ci=self.V.T@self._op_matrix(self._c, i+off)@self.V          # in eigenbasis
        cjd=self.V.T@self._op_matrix(self._cdag, j+off)@self.V
        E=self.E; bz=self.beta; Z=self.Z
        w=np.exp(-bz*E)/Z
        # -sum_mn w_m e^{tau(E_m-E_n)} <m|c_i|n><n|c_j^dag|m>
        Emn=np.subtract.outer(E,E)                                  # E_m - E_n
        expf=np.exp(tau*Emn)
        M=(ci*cjd.T)                                                # <m|ci|n><n|cjd|m> elementwise
        return -np.sum((w[:,None])*expf*M)

if __name__=="__main__":
    # FREE-LIMIT CHECK: U=0 ED must reproduce the engine convention G0 (independent numpy spectral sum)
    Lx,Ly=2,2; beta,mu=4.0,0.5
    hop=hop_2d_square(Lx,Ly)
    ed=HubbardED(hop,U=0.0,mu=mu,beta=beta)
    # independent free G0 (same as val2d's numpy path)
    w,Vk=np.linalg.eigh(hop)
    def G0(i,j,tau):
        nF=1/(np.exp(beta*(w-mu))+1)
        return -np.sum(Vk[i]*Vk[j]*(1-nF)*np.exp(-(w-mu)*tau))
    print("FREE LIMIT (U=0) ED vs analytic G0, 2x2:")
    mx=0
    for (i,j,tau) in [(0,0,0.5),(0,1,1.3),(0,3,2.2),(1,2,0.8)]:
        a=ed.G(i,j,tau); b=G0(i,j,tau); mx=max(mx,abs(a-b))
        print(f"  G({i},{j};{tau}) ED={a:+.12f}  G0={b:+.12f}  diff={a-b:+.2e}")
    print(f"  max|diff| = {mx:.2e}  {'MATCH' if mx<1e-10 else 'FAIL'}")


def exact_coeffs(hop, mu, beta, tau, nmax, r=0.5, M=256):
    """Exact U^n Taylor coefficients a_n of the local Green's function G(0,0;tau;U), via the Cauchy
    contour integral a_n = (1/2pi i) oint G(U)/U^{n+1} dU on |U|=r (r inside the convergence disk).
    Uses a general complex eigendecomposition so complex U is handled exactly. r-independent inside
    the disk (verified). Returns real array a[0..nmax]."""
    import numpy as np
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
    c0=opmat(c,0); c0d=opmat(cdag,0); Hd=np.diag(Hint)
    def Gc(U):
        w,VR=np.linalg.eig(H0+U*Hd); Winv=np.linalg.inv(VR)
        ci=Winv@c0@VR; cjd=Winv@c0d@VR; Z=np.sum(np.exp(-beta*w)); wt=np.exp(-beta*w)/Z
        return -np.sum(wt[:,None]*np.exp(tau*np.subtract.outer(w,w))*(ci*cjd.T))
    th=2*np.pi*np.arange(M)/M; G=np.array([Gc(r*np.exp(1j*t)) for t in th])
    return np.array([ (np.sum(G*np.exp(-1j*n*th))/(M*r**n)).real for n in range(nmax+1) ])
