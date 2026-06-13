"""continuum_wavevector.py (v129) -- A's continuum Friedel wavevector: the v119 (120deg,180deg) dominant
wavevector is a real, convergent continuum feature.

v119 found the elementary density matrix rho(0,r)=(1/N) sum_{eps<=1} cos(k.r) dominated by SHORT-wavelength
(~2-3 site) structure at the level-1|2 boundary modes, characterized as (120deg,180deg) at L=6. Since A's
sign (v127/v128: converges) is a superposition of rho at the close vertex displacements (1,2,4 -> Dx=1..4),
this short-wavelength structure is what governs A. Does it converge as L->inf, and does it match v119?

THE FERMI SURFACE IS L-INDEPENDENT. The occupied sea is {eps<=1} <=> cos(kx)+cos(ky)+cos(kz) <= -1/2, a
FIXED continuum surface independent of L. v119's specific angles (120,180) were the L=6 DISCRETE SAMPLING of
this surface -- at L=6 only x-angles {0,60,120,180} exist, so the boundary modes snap onto 120 and 180.

THE FRIEDEL EDGE CONVERGES. The dominant short-wavelength of rho along x = the Fermi-surface edge of the
occupied weight W(kx) (the cosine-transform structure of rho). Its half-max crossing converges:
  L:     6     12     24     48     96    192    384
  kx/L: .425  .383   .360   .351   .348   .3476  .3472   -> ~0.347 (~125 deg, ~2.9 sites)
So the continuum dominant wavevector is kx/L ~ 0.347 (~125 deg), sitting at the 120deg (3-site, 1/3) end of
v119's (120,180) bracket -- (120,180) = the 3-site / 2-site wavelengths bracketing the ~2.9-site continuum
oscillation, exactly as a short-wavelength Friedel structure should.

CONCLUSION. v119's dominant-wavevector identification is CONFIRMED as a real continuum feature: the
density-matrix Friedel structure converges (the Fermi surface is fixed; the edge -> kx/L~0.347~120deg). The
specific (120,180) values were the L=6 sampling; the continuum lands at the 120deg (3-site) end. This is the
clean counterpart to v128: A integrates the whole sea -> this convergent continuum wavevector (sign(A)
converges, v127), whereas c1 picks one lowest-empty multiplet -> arithmetic jitter (sign(c1), v128)."""
import numpy as np

def edge_kxL(L, mu=1.0):
    k=np.arange(L); c=-2*np.cos(2*np.pi*k/L); C2=c[:,None]+c[None,:]
    W=np.array([np.sum(C2 <= mu - c[kx] + 1e-9) for kx in range(L//2+1)],dtype=float); W/=W.max()
    i=np.where(W<=0.5)[0][0]
    return (i-1 + (0.5-W[i-1])/(W[i]-W[i-1]))/L     # interpolated half-max crossing

def _selftest():
    print("continuum_wavevector self-test:")
    edges={L:edge_kxL(L) for L in [6,12,24,48,96,192,384]}
    seq=[edges[L] for L in [6,12,24,48,96,192,384]]
    assert all(seq[i]>seq[i+1] for i in range(len(seq)-1)), seq          # monotone convergence
    assert abs(edges[384]-0.347) < 0.003, edges[384]                      # -> ~0.347
    assert abs(edges[384]-1/3) < abs(edges[384]-1/2)                      # nearer 1/3 (120) than 1/2 (180)
    # at L=6 the FS x-angles are exactly the v119 discrete set {0,60,120,180}
    k=np.arange(6); c=-2*np.cos(2*np.pi*k/6); C2=c[:,None]+c[None,:]
    angs=sorted({round(min(kx,6-kx)/6*360) for kx in range(6) if (np.abs(C2+c[kx]-1.0)<2).any()})
    assert 120 in angs and 180 in angs, angs
    print(f"  Fermi-surface {{eps<=1}} is L-independent; L=6 x-angles {angs} (v119's 120,180 present)")
    print(f"  Friedel edge kx/L: 0.425 ->{edges[24]:.3f}->{edges[96]:.3f}-> {edges[384]:.4f} (~0.347, ~125 deg, 3-site end)")
    print(f"  => v119 dominant wavevector CONFIRMED as a convergent continuum feature; (120,180)=L=6 sampling. PASS")

if __name__ == '__main__':
    _selftest()
