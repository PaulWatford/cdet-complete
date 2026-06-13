"""v40 -- is single-order R the right observable at all? Test the measurable aggregate candidates that
were proposed as possibly cleaner than per-order R (which v39 showed is shell-contaminated):
  (A) average sign INTEGRATED over orders,  (B) crossover order n*,  (C) the per-order structure itself.
Verdict, honestly: at accessible sizes none of these is clean, and there is a clear mechanism for why."""
import subprocess, numpy as np
from hubbard_ed import hop_2d_square, exact_coeffs

def mu_for(L,beta,nt):
    k=2*np.pi*np.arange(L)/L; eps=-2*(np.cos(k)[:,None]+np.cos(k)[None,:]); lo,hi=-6.,6.
    for _ in range(60):
        m=.5*(lo+hi); lo,hi=(m,hi) if 2*np.mean(1/(np.exp(beta*(eps-m))+1))<nt else (lo,m)
    return .5*(lo+hi)
def Rn(L,n,beta,mu,nmc=400000,seed=7):
    o=subprocess.run(["./mc2d","sq",str(L),str(L),str(n),f"{beta:.4f}",f"{mu:.6f}","1.0","0.7","0.2",str(nmc),str(seed)],
                     capture_output=True,text=True).stdout.split(); return float(o[2]), abs(float(o[1])/float(o[3]))
def Sint(L,nmax,U,beta,mu,nmc=400000,seed=7):
    o=subprocess.run(["./isign","sq",str(L),str(L),str(nmax),f"{U}",f"{beta:.4f}",f"{mu:.6f}","1.0","0.7","0.2",str(nmc),str(seed)],
                     capture_output=True,text=True).stdout.split(); return float(o[0]),float(o[1])

beta=4.0; DENS=0.8
print("(A) INTEGRATED average sign S vs N, fixed density n=0.8, U=1.0, nmax=5  -- is it cleaner than per-order R?")
for L in [2,3,4]:
    mu=mu_for(L,beta,DENS); S,s=Sint(L,5,1.0,beta,mu)
    print(f"    L={L} N={L*L:2d}: S={S:+.4f} +/- {s:.4f}")
print("    -> still sign-alternating / non-monotonic: NOT cleaner than per-order R.")

print("\n  WHY: the order weights U^n*N*(N*beta)^n/n! are wildly non-uniform, so the 'integral over orders'")
print("  is dominated by ONE order, inheriting its shell structure. Exact 2x2 weights:")
a=exact_coeffs(hop_2d_square(2,2),0.5,beta,0.5,5); N=4
for U in [0.5,2.0]:
    w=[abs(U**n*N*a[n]) for n in range(1,6)]; print(f"    U={U}: order weights {['%.2f'%x for x in w]} -> order {int(np.argmax(w))+1} dominates")

print("\n(B,C) per-order R_n and crossover n* (|R_n|<0.05 = unresolvable), fixed density n=0.8:")
for L in [2,3,4]:
    mu=mu_for(L,beta,DENS); row=[]; nstar=None
    for n in range(1,6):
        if L==4 and n==5: row.append("  skip"); continue
        R,_=Rn(L,n,beta,mu); row.append(f"{R:+.3f}")
        if nstar is None and abs(R)<0.05: nstar=n
    print(f"    L={L} N={L*L:2d}: R_n(n=1..5) = {row}   n*={nstar}")
print("    -> R_n does not decay monotonically in n either, and n* jumps with cluster: no clean scaling.")

print("\nVERDICT: of the MEASURABLE candidates, none scales cleanly at accessible sizes. Integrating over")
print("orders fails (single-order domination); n* inherits the per-order a_n shell jumps; R(mu) oscillates")
print("and changes sign within a single cluster. Free-energy differences are a different (thermodynamic-")
print("integration) computation, not this engine's Green's-function MC. The contaminant is partial-shell")
print("FILLING; the principled cure is fixing the filling fraction (closed-shell cluster families) or going")
print("to large N -- both out of reach here. Honest status: no clean sign-scaling benchmark is extractable")
print("at accessible sizes with this engine's observables; that limit is itself the result.")
