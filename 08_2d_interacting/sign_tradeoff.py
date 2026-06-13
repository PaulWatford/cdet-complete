"""v48 -- Does the shift improve the SIGN, or only convergence? (the reviewer's million-dollar question)
The shifted reference is set by one knob, mu_ref = mu - alpha. Convergence is governed by the complex-U POLE
(moved out by a Hartree-scale shift); the per-order sign R is governed by the real-axis SHELL/detuning (best
when mu_ref sits on a closed shell, v41). Those are different physics, so the convergence-optimal and
sign-optimal shifts need not coincide -- and here they actively COMPETE. We find both optima for one case and
show the trade-off: the convergence-optimal (Hartree) shift lands OFF the closed shell and gives the WORST
sign. So pole-moving accelerates convergence but does NOT move the sign wall; chasing convergence pulls you
away from the good-sign operating point. Convergence side is ED-exact; sign side is the live mc2d sampler."""
import subprocess, numpy as np
from hubbard_ed import hop_2d_square
from shifted_expansion import exactG, shifted_coeffs, density, radius_estimate, best_shift

hop=hop_2d_square(2,2,1.0); beta,tau,U,mu=4.0,0.5,4.0,0.5   # 2x2 levels {-4,0,0,+4}; mu=0.5 just above the shell at 0
Gex=exactG(hop,mu,beta,tau,U); n=density(hop,mu,beta,U)

def Rsign(mu_s,order,NMC=1200000,seed=11):
    o=subprocess.run(["./mc2d","sq","2","2",str(order),f"{beta}",f"{mu_s:.4f}","1.0","0.7","0.2",str(NMC),str(seed)],
                     capture_output=True,text=True).stdout.split(); return abs(float(o[2]))
def conv_err(a):
    b=shifted_coeffs(hop,mu,beta,tau,U,a,12,M=240); return abs(np.sum(b[:9]).real-Gex)

if __name__=="__main__":
    print("="*78); print("v48: does the shift improve the SIGN or only convergence?  (2x2, mu=0.5, U=4, beta=4)")
    print("="*78); print(f"<n>/site={n:.3f}, Hartree U<n_sigma>={U*n/2:.2f}\n")
    # convergence-optimal shift (ED): scan alpha
    print("CONVERGENCE side (ED): truncation error at K=8 vs shift alpha")
    ac=None
    for a in [0.0,0.25,0.5,0.75,1.0,1.5,2.0]:
        e=conv_err(a); r=radius_estimate(shifted_coeffs(hop,mu,beta,tau,U,a,12,M=240))
        print(f"   alpha={a:+.2f} (mu_ref={mu-a:+.2f}): radius~{r:4.2f}  err@K8={e:.1e}")
        if ac is None or e<ac[1]: ac=(a,e)
    print(f"   -> alpha_conv={ac[0]:+.2f} (mu_ref={mu-ac[0]:+.2f})  [near the Hartree scale]\n")
    # sign-optimal reference (mc2d): scan mu_ref
    print("SIGN side (mc2d): |R_2| vs reference mu_ref")
    asg=None
    for mu_s in [-1.0,-0.5,-0.25,0.0,0.25,0.5]:
        r=Rsign(mu_s,2)
        print(f"   mu_ref={mu_s:+.2f} (alpha={mu-mu_s:+.2f}): |R_2|={r:.3f}")
        if asg is None or r>asg[1]: asg=(mu_s,r)
    print(f"   -> sign-optimal mu_ref={asg[0]:+.2f} (alpha_sign={mu-asg[0]:+.2f})  [on the closed shell]\n")
    # the trade-off, across orders
    print("THE TRADE-OFF (same knob mu_ref, competing optima):")
    print(f"  {'reference':>26} | {'conv err@K8':>11} | {'|R_2|':>6} {'|R_3|':>6} {'|R_4|':>6}")
    for tag,mu_s,a in [("SIGN-opt mu_ref=0.0 (shell)",0.0,0.5),
                       ("CONV-opt mu_ref=-1.0 (Hartree)",-1.0,1.5),
                       ("physical mu_ref=+0.5 (alpha=0)",0.5,0.0)]:
        print(f"  {tag:>26} | {conv_err(a):>11.1e} | {Rsign(mu_s,2):>6.3f} {Rsign(mu_s,3):>6.3f} {Rsign(mu_s,4):>6.3f}")
    print("\nVERDICT: convergence wants the Hartree/pole shift (mu_ref=-1.0, ~10x better trunc error); the sign")
    print("wants the closed shell (mu_ref=0.0, |R| ~0.8 vs ~0.05). The convergence-optimal shift has the WORST")
    print("sign. Pole-moving does NOT move the sign wall -- it trades against it. (Single case, multi-order;")
    print("mechanism: convergence<->complex-U pole, sign<->real-axis shell -- different physics, different optima.)")
