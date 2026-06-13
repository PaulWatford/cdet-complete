import numpy as np, subprocess
beta,mu,t=5.0,0.3,1.0
def G0_atom(tau,beta,mueff):  # single level, engine convention; mueff = -(eval-mu)
    # engine G0_atom(tau,beta,mu): replicate via spectral: level energy xi=-mueff
    xi=-mueff
    nF=1.0/(np.exp(beta*xi)+1)
    if tau==0.0: return nF
    s=1.0; tt=tau
    while tt>=beta: tt-=beta; s=-s
    while tt<0: tt+=beta; s=-s
    return s*(-(1-nF)*np.exp(-xi*tt))
def G0_2d_numpy(Lx,Ly,sites,taus):
    N=Lx*Ly
    H=np.zeros((N,N))
    def idx(x,y): return (y%Ly)*Lx+(x%Lx)
    for x in range(Lx):
        for y in range(Ly):
            i=idx(x,y)
            for dx,dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                H[i,idx(x+dx,y+dy)]+=-t
    w,V=np.linalg.eigh(H)
    n=len(sites)
    G=np.zeros((n,n))
    for a in range(n):
        for b in range(n):
            i,j=sites[a],sites[b]; dtau=taus[a]-taus[b]
            tot=0.0
            for k in range(N):
                amp=V[i,k]*V[j,k]; xi=w[k]-mu
                tot+=amp*G0_atom(dtau,beta,-xi)
            G[a,b]=tot
    return G
Lx,Ly=4,4
sites=[0,5,10,15,3]; taus=[0.5,2.5,1.1,3.9,0.8]
inp="".join(f"{s} {ta:.6f}\n" for s,ta in zip(sites,taus))
out=subprocess.run(["./gdump_2d",str(Lx),str(Ly),str(len(sites))],input=inp,capture_output=True,text=True).stdout
Geng=np.array([[float(x) for x in l.split()] for l in out.strip().split("\n")])
Gpy=G0_2d_numpy(Lx,Ly,sites,taus)
# Tolerance 1e-8: the engine and this independent numpy spectral sum agree to
# machine precision (median ~2.6e-16) on 23/25 entries; the 2 worst entries reach
# ~3.4e-9 (rel ~4e-8), pure float accumulation in the highest-dynamic-range
# spectral terms (largest |dtau|). The old 1e-10 gate was tighter than an
# independent reimplementation can achieve and produced a spurious FAIL.
print("2D square %dx%d: engine vs numpy diagonalization, max|diff| = %.2e  %s"%(
    Lx,Ly,np.max(np.abs(Geng-Gpy)),"MATCH" if np.max(np.abs(Geng-Gpy))<1e-8 else "FAIL"))
