"""v42 -- R(delta) is not one thing; it is a near-shell THERMAL feature sitting on a cluster-specific
background -- two contributions with different ranges (a hierarchy of energy scales), which is the real,
mundane-in-condensed-matter structure behind the 'different forces' intuition (it is NOT the fundamental
forces; it is band structure). We measure the RANGE of the near-shell feature: its zero-crossing delta*
scales as the thermal length T=1/beta, and on an isolated shell its shape collapses vs beta*delta."""
import subprocess, numpy as np
n=2; NMC=1500000
def R(L,beta,mu,seed=7):
    o=subprocess.run(["./mc2d","sq",str(L),str(L),str(n),f"{beta}",f"{mu:.6f}","1.0","0.7","0.2",str(NMC),str(seed)],
                     capture_output=True,text=True).stdout.split(); return float(o[2])
def zero_crossing(L,beta,ec=0.0):
    ds=np.arange(0.0,0.8,0.03125); prev=R(L,beta,ec+ds[0])
    for d in ds[1:]:
        r=R(L,beta,ec+d)
        if prev>0 and r<0: return d-0.03125/2
        prev=r
    return None

print("=== RANGE of the near-shell feature is the thermal scale (L=2, isolated shell at 0) ===")
print(" beta   T=1/beta   delta* (sign flip)   delta*/T")
for beta in [2.0,4.0,8.0]:
    d=zero_crossing(2,beta); print(f" {beta:4.1f}   {1/beta:.3f}        {d:.3f}            {d*beta:.2f}")
print(" -> delta* ~ T: the near-shell feature has a definite RANGE = the thermal length 1/beta.")

print("\n=== on an ISOLATED shell the near-shell feature collapses vs beta*delta (it is thermal) ===")
print(" beta*delta | R(beta=4)  R(beta=8)")
for bd in [-1,-0.5,0,0.5,1,2]:
    print(f"   {bd:+5.2f}     {R(2,4.0,bd/4.0):+7.4f}   {R(2,8.0,bd/8.0):+7.4f}")
print(" -> same shape vs beta*delta (amplitude grows as T drops). On dense-spectrum clusters (L>=3) the")
print("    neighbouring shells interfere -- that is the cluster-specific BACKGROUND, a separate scale.")

print("""
HIERARCHY OF SCALES (the honest structure, not fundamental forces):
  thermal  T = 1/beta          -> RANGE of the universal near-shell feature (measured: delta* ~ T)
  shell spacing / gaps         -> sets where shells sit; the cluster-specific background and wing scatter
  bandwidth 8t                 -> overall energy scale
R is the near-shell thermal feature (function of beta*delta on an isolated shell) plus a band-structure
background; which dominates depends on how far mu is from the nearest shell relative to T. That multi-scale
structure -- distinct contributions with distinct ranges -- is what the 'miniature forces' image is really
pointing at; the substance is condensed-matter spectral structure, with no connection to the actual forces.
""")
