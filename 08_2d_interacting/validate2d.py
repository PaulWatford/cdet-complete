"""v36 gate: the 2D interacting connected-determinant engine vs exact diagonalization.
(1) cdet_order(n) = N * a_n for the 2x2 square AND the 1D ring L=4 (same convention, orders 1 and 2),
    where a_n is the U^n Taylor coefficient of the exactly-diagonalized local Green's function.
(2) capstone: reconstruct G(U) = G0 + U*(cdet1/N) + U^2*(cdet2/N) from the ENGINE coefficients and
    compare to exact ED G(U) at finite U -- the O(U^2) truncation error must fall like U^3."""
import numpy as np, subprocess, sys
from hubbard_ed import hop_1d_ring, hop_2d_square
from pin_convention import pieces, Gloc

beta,mu,t,to,ti=4.0,0.5,1.0,0.7,0.2; tau=to-ti
def eng(args): return [float(x) for x in subprocess.run(["./cdet_small"]+args,capture_output=True,text=True).stdout.split()]
def a_coeffs(hop,Us): 
    H0,Hint,c0,c0d=pieces(hop,mu,beta)
    return np.polyfit(Us,[Gloc(H0,Hint,c0,c0d,U,beta,tau) for U in Us],6)[::-1], (H0,Hint,c0,c0d)
Us=np.linspace(-0.06,0.06,13)
fails=0

print("=== (1) cdet_order(n) == N * a_n  (engine vs exact ED) ===")
cases=[("1D ring L=4",hop_1d_ring(4),["ring","4"],4),
       ("2D square 2x2",hop_2d_square(2,2),["sq","2","2"],4)]
pieces_cache={}
for name,hop,pre,N in cases:
    a,pc=a_coeffs(hop,Us); pieces_cache[name]=pc
    G0,c1,c2=eng(pre+[str(beta),str(mu),str(t),str(to),str(ti)])
    for n,(cn,an) in enumerate([(c1,a[1]),(c2,a[2])],1):
        pred=N*an; rel=abs(cn-pred)/(abs(pred)+1e-30); ok=rel<1e-4
        print(f"  {name:14s} n={n}: cdet={cn:+.10f}  N*a_n={pred:+.10f}  rel={rel:.1e}  {'OK' if ok else '*** FAIL'}")
        fails+= (not ok)

print("\n=== (2) capstone: 2D G(U) reconstructed from engine coeffs vs exact ED (2x2) ===")
H0,Hint,c0,c0d=pieces_cache["2D square 2x2"]; N=4
G0,c1,c2=eng(["sq","2","2",str(beta),str(mu),str(t),str(to),str(ti)])
a1e,a2e=c1/N,c2/N
prev=None
for U in [0.25,0.5,1.0,2.0]:
    rec=G0+U*a1e+U*U*a2e
    ex=Gloc(H0,Hint,c0,c0d,U,beta,tau)
    err=abs(rec-ex)
    ratio="" if prev is None else f"  err ratio={err/prev[1]:.2f} (U ratio^3={ (U/prev[0])**3:.2f})"
    print(f"  U={U:.2f}: engine O(U^2)={rec:+.8f}  exact ED={ex:+.8f}  |err|={err:.2e}{ratio}")
    prev=(U,err)

print("\n%s"%("ALL 2D GATES PASS" if fails==0 else "*** FAILURES ***"))
sys.exit(1 if fails else 0)
