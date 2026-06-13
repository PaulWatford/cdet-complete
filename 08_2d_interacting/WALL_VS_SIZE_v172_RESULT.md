# The convergence wall vs lattice size (v172)

**Question.** The bare-U series has a finite radius of convergence -- the "wall." The standing assumption in this
program was that the lattice is the *easy* axis and the wall lives on the *order* axis. This result tests the opposite
hypothesis: that the wall is partly a **finite-size** property, so that growing the lattice can move it -- i.e. a place
where lattice size *helps* the order axis.

**Method (uses the v162 plane-wave dispersion).** The leading weak-coupling cause of the wall is the RPA/Stoner
instability. The free static (Lindhard) susceptibility

>   chi0(q, L) = (1/N) sum_k [f(eps_k) - f(eps_{k+q})] / (eps_{k+q} - eps_k),   eps_k = -2t(cos kx + cos ky),

builds the particle-hole bubble chi(q) = chi0/(1 - U chi0), a geometric series in U that diverges at

>   **U_c(L) = 1 / max_q chi0(q, L).**

chi0 needs only the O(L) dispersion (no eigenvectors), so -- unlike the eigenvector path -- **U_c(L) is computable at
any lattice size up to 100x100** (L=100 runs in ~2 s). This is exactly what the v162 large-L propagator unlocked.

**Result.** The wall is a thermodynamic-limit quantity; the small-lattice wall is a finite-size artifact.

Half-filling (mu=0, beta=5), nesting channel q=(pi,pi) -- the channel that dominates the Hubbard model:

| L (LxL) | chi0_max | U_c (wall) |
|--------:|---------:|-----------:|
|   4     | 0.6094   | 1.641      |
|   8     | 0.5331   | 1.876      |
|  16     | 0.5077   | 1.970      |
|  32     | 0.5063   | 1.975      |
| 100     | 0.5063   | 1.975      |

The 4x4 lattice places the wall at U_c = 1.64; the true thermodynamic-limit wall is **1.975, ~20% further out**. The
small lattice is spuriously *pessimistic* -- it hides convergence that is really there. **Growing the lattice pushes
the wall back: lattice size helps.**

**Honest nuances.**
- *Filling dependence.* At incommensurate doping (mu=-0.6) the artifact reverses sign: the coarse q-grid misses the
  peak, so the small lattice is spuriously *optimistic* (U_c = 4.37 at 4x4 -> 3.30 in the TD limit). Either way the
  small lattice gives the wrong wall and you need the large lattice to get the true one.
- *Scope of U_c.* This is the leading REAL-axis instability (RPA/Stoner), validated as the exact bubble-sum radius. The
  FULL series radius can be set by complex-U structure closer than this (the v146 atom finding). U_c is the leading
  physical wall -- now computed at scale instead of guessed from the atom or a small cluster.

**Validation (pre-registered gates, all pass).** (1) chi0(q=0) equals the DOS-at-E_F sum rule (1/N)sum beta f(1-f) to
0.0e+00; (2) the vectorized chi0 equals a brute-force O(L^4) pair sum to 3.3e-16; (3) the bubble series sum_n
(U chi0max)^n has radius exactly 1/chi0max = U_c; (4) U_c(64) vs U_c(96) converged to 1e-9 (TD limit reached); (5) the
half-filling wall recedes with L. Frozen reference engine untouched (194/194). `wall_vs_size.py`, `cdet wall`.
