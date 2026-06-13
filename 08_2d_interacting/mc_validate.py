"""v37 gate: the 2D high-order Monte-Carlo driver (mc2d) reproduces the EXACT 2x2 Hubbard Green's-
function coefficients a_n (from exact diagonalization, contour-extracted) at orders 3-6, where the
deterministic nested quadrature's np^n cost is impractical. cdet_order(n)=N*a_n; assert each MC
estimate agrees within 4 sigma. Orders 1,2 included as a bridge to the deterministic path."""
import subprocess, sys
from hubbard_ed import hop_2d_square, exact_coeffs

beta,mu,t,to,ti=4.0,0.5,1.0,0.7,0.2; N=4
a=exact_coeffs(hop_2d_square(2,2),mu,beta,to-ti,6)   # exact a_0..a_6
nmc={1:1000000,2:1000000,3:1000000,4:500000,5:200000,6:100000}
seed=20377
print(f"2x2 square, beta={beta} mu={mu} tau={to-ti}: MC vs exact ED  (cdet_order(n) = N*a_n, N={N})")
print(f"{'n':>2s} {'MC estimate':>14s} {'stderr':>11s} {'exact N*a_n':>13s} {'sigma':>7s}")
fails=0
for n in range(1,7):
    out=subprocess.run(["./mc2d","sq","2","2",str(n),str(beta),str(mu),str(t),str(to),str(ti),str(nmc[n]),str(seed)],
                       capture_output=True,text=True).stdout.split()
    est,err=float(out[0]),float(out[1]); exact=N*a[n]; sig=abs(est-exact)/err if err>0 else 0
    ok=sig<4.0; fails+=(not ok)
    print(f"{n:2d} {est:14.7f} {err:11.6f} {exact:13.7f} {sig:6.2f}{'' if ok else ' FAIL'}")
print("\n%s"%("MC DRIVER VALIDATED vs exact ED, orders 1-6" if fails==0 else "*** FAILURES ***"))
sys.exit(1 if fails else 0)
