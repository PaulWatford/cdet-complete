# CROSSCHECK_v129 — A's continuum Friedel wavevector

**Claims.** (1) The Fermi surface {ε≤1} = cos(kx)+cos(ky)+cos(kz)≤−1/2 is L-independent; at L=6 the x-angles
are {0,60,120,180} (v119's 120,180 present). (2) The Friedel edge (half-max of W(kx)) along x converges:
kx/L = 0.425(L6)/0.360(L24)/0.348(L96)/0.3472(L384) → ~0.347 (~125°, ~2.9 sites), the 120° (3-site, 1/3)
end of v119's (120,180) bracket. (3) v119's dominant wavevector confirmed as a convergent continuum feature;
(120,180) were the L=6 sampling. (4) Counterpart to v128: A integrates the whole sea (convergent wavevector,
sign converges); c1 picks one multiplet (jitter).

**Reproduce.** `cd 08_2d_interacting && python3 continuum_wavevector.py` (edge_kxL(L) for L=6…384).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
