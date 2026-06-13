# The full 2D Friedel sign-map (v119): resolved at the elementary level — the discrete Fermi surface sets the wavevector exactly and μ-rigidly

v117 saw A's sign oscillate along a line; v118 showed it is set by the discrete frozen Fermi boundary,
rigid under μ. v119 maps the sign over a full 2D plane and resolves it at the elementary level.

## Two objects: the determinant A vs the elementary propagator ρ

Mapping sign(A) over the (x,y,0) plane (vertex site scanned, S0,S1 fixed off-plane) gives a structured
but messy pattern — many cells near nodal lines (|A|→0), and the fixed sites break the lattice symmetry.
That is expected: A is a connected determinant of propagators between {0,S0,S1,S2}, so its sign-vs-S2 is
a multi-propagator **superposition**.

The elementary object is the frozen one-particle density matrix
ρ(0,r) = Σ_{occupied k} U[0,k]U[r,k] = (1/N) Σ_{occ k} e^{ik·r} — the **Fourier transform of the
occupied region in k-space**. Its Friedel oscillation is set by the Fermi surface (the boundary of the
occupied region) directly.

## Result — the elementary map is clean, short, symmetric, and exactly μ-rigid

- **Cube-symmetric.** The ρ(0,r) sign-map is symmetric under x→6−x and y→6−y (the cube point group).
- **Short wavelength.** Dominant wavevector (120°, 180°) — wavelength ~2–3 sites — matching the
  level-1|level-2 boundary 1D modes (ε=+1 at k=2,4 → 120°/240°; ε=+2 at k=3 → 180°). The **discrete
  frozen Fermi surface sets the wavevector.**
- **μ-invariance is now analytic and exact.** There are **zero** modes with eigenvalue strictly in
  (1,2), so the occupied set {λ≤1} is *identical* for every μ in the window — ρ is the same map for all
  μ∈(1,2). This proves v118's numerical μ-rigidity from first principles.

## Reconciling v117

The elementary Friedel wavelength is **short** (~2–3 sites), not the ~8 sites inferred from A. A's sign
is a determinant superposition of these short elementary oscillations over the site pairs, producing a
longer, messier apparent envelope. v117's "~8-site wavelength / 2k_F(μ)" was that **superposition
envelope** (and, per v118, a coincidence) — not the elementary scale. The core v117 claim survives
unchanged (the sign is geometric and Friedel-class); v119 supplies the elementary wavevector and shows
how the determinant builds the observable sign from it.

## The sign side, closed consistently with the scale side

The discrete frozen Fermi surface — the filled-level set — sets the elementary Friedel wavevector
*exactly* and *μ-rigidly* (analytic), just as it sets the deep-β scale z=2 (the lowest empty level).
The same discrete object governs both, and the determinant assembles the observable sign by superposing
the elementary oscillations. None of this moves the wall.

Reproduce: `python3 frozen_friedel_map.py` (self-test PASS). The full A-map (multi-propagator) via
`./cse grid 24 24 1 16 2048 31 0.002 0 2 43 80 <idx>` for idx = x+6y over the plane. Frozen engine
untouched (194/194).
