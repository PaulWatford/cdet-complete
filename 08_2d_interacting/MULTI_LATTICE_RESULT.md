# Scaling the brute force across lattice sizes (v122): which laws are universal, how big we can go, and a hybrid path

Testing the program's laws (found at L=6) across L separates the **universal** from the
**crystallographic**, and the plane-wave propagator shows how to scale the brute force and build a
third, hybrid engine.

## The laws across L

**μ-rigidity is CRYSTALLOGRAPHIC, not universal.** The v120 theorem — the freeze is exactly μ-rigid
in a unit interval because cube_hopping(6) has an integer spectrum — holds exactly **iff cos(2π/L) is
rational iff L ∈ {1,2,3,4,6}**, the crystallographic restriction. For other L the 1D eigenvalues
−2cos(2πk/L) are irrational, the spectrum is dense, and the freeze is only approximately rigid:

| L | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 12 |
|---|---|---|---|---|---|---|---|---|
| integer spectrum | yes | yes | yes | **no** | yes | **no** | **no** | **no** |
| min eigenvalue gap | 4.0 | 3.0 | 2.0 | 0.53 | 1.0 | 0.15 | 0.24 | 0.20 |

**The scale law is UNIVERSAL.** z(∞) = the lowest-empty-level eigenvalue (the Fermi-surface probe). At
L=6, μ∈(1,2) that level is 2 → z=2; at μ∈(2,3) it is 3 → z=3; at L=4, μ∈(0,2) → 2. The mechanism
(corner-confined A, smallest-gap de-confined c1) needs only a clean lowest-empty level, which exists for
any L (sharp for crystallographic L, ε-sharp otherwise). **The Friedel law is universal too**: the
elementary ρ(0,r) oscillates for any L, with ρ(0,0) = occupied fraction and the wavevector tracking the
occupied-region boundary.

## The scaling enabler — the plane-wave propagator

The connected determinant is over a **fixed** set of vertices; the lattice enters **only** through
propagators g0(i,j,τ) = (1/N) Σ_k cos(k·Δr) G0_atom(ε_k, β, occ_k, τ) — each an O(N) plane-wave sum,
**no eigenvectors, no stored spectrum**. So the brute force is **O(N × MC), linear in N=L³, and
L-agnostic**. `cfriedel_L.c` generalizes the elementary object to any L on exactly this form (validated
4.8e-11 vs Python eigh at L=6), and runs the full structural layer at L=20 (N=8000) in well under a
second with zero stored data.

## How big can we go?

- **Structural laws** (spectrum, μ-rigidity, Friedel) are O(N), analytic, file-free → **L=20+ (N=8000)
  trivially**, in negligible context. The 375 KB `spectrum_l6.bin` is eliminated by the plane-wave form.
- **The determinant** (A, c1) with plane-wave propagators is O(N × MC) → **L≈12–16 comfortably** in a
  session; the cost grows linearly, not catastrophically, because the vertices stay fixed.
- **Exact μ-rigidity tests** are limited to the crystallographic L ∈ {2,3,4,6}; the scale and Friedel
  laws can be tested at any L (a larger L makes the Fermi surface — and the wall — sharper).
- The practical ceiling is set by **output/analysis context, not the lattice**: with no stored spectra,
  the lattice size is nearly free, so the binding constraint is how much we print and reason about.

## The third engine — a hybrid (surrogate → optimized brute)

Preserving the dual (surrogate vs brute) and adding a third that carries the surrogate as far as it goes
then hands off:

- **Phase 1 — carry the laws (surrogate-fast, O(N), any L, instant):** from (L, μ), get the integer-
  spectrum/μ-rigidity verdict, the Fermi surface / probe level (→ the z(∞) prediction), and the Friedel
  wavevector. No determinant, no MC. (`multi_lattice_laws.py`, `cfriedel_L.c scan`.)
- **Phase 2 — optimized brute (plane-wave determinant, O(N×MC)):** compute the actual A, c1 at the
  target L on the plane-wave propagator, validated against the phase-1 structure (does z flow to the
  predicted lowest-empty level? does the sign match the Friedel prediction?).

The handoff is exactly where the surrogate stops being exact: it carries the *discrete* structure for
free (and exactly, on crystallographic L); the brute fills in the *coefficient* the surrogate cannot
derive. This is the same chain as the scale and sign sides — distilled law → plane-wave structure →
determinant — now organized as a single engine that spends MC only where the laws run out.

None of this moves the wall, but it makes the wall's lattice-size dependence explicit and cheap to
probe. Reproduce: `python3 multi_lattice_laws.py`; `gcc -O2 -Wall -Werror -std=c11 -pedantic -o
cfriedel_L cfriedel_L.c -lm && ./cfriedel_L scan`. Frozen engine untouched (194/194).
