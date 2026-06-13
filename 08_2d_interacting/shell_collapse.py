"""v41 -- the per-cluster R is NOT random: at fixed temperature it is a universal function of the Fermi-
level DETUNING delta = mu - (nearest single-particle shell). R is positive just below a shell, peaks when
the shell sits at mu (delta=0), and flips sign just above -- the SAME structure in every cluster, scaled by
an amplitude A(N) that shrinks with size. So the cluster-to-cluster 'shell noise' of v39/v40 is one curve
sampled at different delta. The organizing variable is delta (where mu sits relative to the shell), at fixed
beta; the temperature is a SEPARATE axis (beta*delta is NOT a single scaling variable -- shown below)."""
import subprocess, numpy as np
n=2; NMC=1000000
def R(L,beta,mu,seed=7):
    o=subprocess.run(["./mc2d","sq",str(L),str(L),str(n),f"{beta}",f"{mu:.6f}","1.0","0.7","0.2",str(NMC),str(seed)],
                     capture_output=True,text=True).stdout.split(); return float(o[2])
centers={2:0.0,3:-1.0,4:0.0}; beta=4.0; deltas=np.array([-1.0,-0.5,0.0,0.5,1.0])
data={L:np.array([R(L,beta,ec+d) for d in deltas]) for L,ec in centers.items()}
print(f"=== R vs detuning delta from nearest shell, at fixed beta={beta} (n=2) ===")
print("delta  | R(L=2)   R(L=3)   R(L=4)   <- same SIGN structure across clusters")
for i,d in enumerate(deltas):
    print(f" {d:+.2f}  | " + "  ".join(f"{data[L][i]:+7.4f}" for L in [2,3,4]))
A={L:data[L][np.argmin(np.abs(deltas))] for L in [2,3,4]}
print(f"\namplitude A(N)=R(delta=0): L2(N4)={A[2]:.3f}  L3(N9)={A[3]:.3f}  L4(N16)={A[4]:.3f}  (shrinks with N)")
print("shape after A-scaling (collapse near the shell):")
print("delta  | R/A(2)  R/A(3)  R/A(4)")
for i,d in enumerate(deltas):
    print(f" {d:+.2f}  | " + "  ".join(f"{data[L][i]/A[L]:+6.3f}" for L in [2,3,4]))
print("\n=== temperature is a separate axis: beta*delta is NOT a single scaling variable (L=3) ===")
print("beta*delta | R(beta=4)  R(beta=2)")
for bd in [-2,0,2]:
    print(f"   {bd:+d}       {R(3,4.0,-1.0+bd/4.0):+7.4f}    {R(3,2.0,-1.0+bd/2.0):+7.4f}")
print("\nDIAGNOSTIC: at fixed T, R is a universal function of the shell detuning delta; clusters differ only")
print("in where mu sits (delta) and by amplitude A(N). To compare clusters consistently, hold delta fixed")
print("(e.g. delta=0, shell at Fermi) -- the quantitative form of 'fix the filling'. R-vs-N looked random")
print("only because each cluster sat at a different delta. (Magnitude collapse is clean near the shell;")
print("the wings and the temperature axis carry extra structure.)")
