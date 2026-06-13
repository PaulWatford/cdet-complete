# Involution search and exact symmetry reduction of the site sum (v50)

**What was asked.** Search our actual model for a structural pairing rule (a meron-style involution)
by computation, not citation: is there a site map σ with C_V(σx) = −C_V(x) (a sign-cancelling
involution, the meron prize), or at least C_V(σx) = +C_V(x) (an exact symmetry that removes
redundant work)? Then turn whatever real structure exists into a reduction, and prove it.

**What the computation found** (`symmetry_reduction.py`, `symmetry_audit_sympy.py`):

1. **No sign-cancelling involution among the natural symmetries.** Tested time reversal
   (τ→β−τ), the sublattice translate, the diagonal reflection, and their products on the genuine
   engine weight. None gives the ratio C_V(σx)/C_V(x) = −1. Time reversal and the translate do not
   pair cleanly at all (they map a config to an unrelated one). So the meron escape does **not** open
   for the doped 2×2 via lattice symmetry — measured in our own engine, ratio came back +1 and never
   −1.

2. **An exact symmetry does exist, and it removes redundancy.** The 2×2 torus has automorphism
   group |G| = 8 (the square point group); the stabilizer of the external site is |G_0| = 2 — the
   diagonal reflection swapping the two B-sublattice sites and fixing the rest. On this element
   C_V(σx)/C_V(x) = +1.000 to machine precision (1e-8) at every order tested. Crucially this is a
   *symmetry*, not an anti-symmetry: orbit members have the **identical value and identical sign**, so
   nothing physical cancels — you simply stop recomputing copies.

3. **The reduction, verified.** Folding the discrete site-configuration sum (the L^n assignments of
   sites to vertices, at fixed vertex times) by G_0 reproduces the brute-force sum exactly and with
   fewer C_V evaluations:

   | order n | folded vs brute | C_V evals (folded / full) | speedup |
   |---|---|---|---|
   | 2 | match 6.6e-17 | 10 / 16 | 1.60x |
   | 3 | match 1.2e-16 | 36 / 64 | 1.78x |
   | 4 | match 8.5e-17 | 136 / 256 | 1.88x |

   The fold approaches the group order |G_0| = 2 as n grows (the swap-fixed fraction shrinks). Larger
   clusters carry larger stabilizers (point group up to order 8, more once the external is placed to
   maximise it), so the fold grows with the lattice's symmetry.

4. **Symbolic proof (sympy).** The reduction is exact because the stabilizer permutations satisfy
   P^T·H(t)·P − H(t) = 0 and [P, H(t)] = 0 as **polynomial identities in the hopping t** — not a
   numerical accident at t=1. Since the engine's propagator G₀ is a function of H alone, a permutation
   that fixes H and fixes the external site fixes G₀ on every index, hence fixes every determinant
   entry, hence fixes C_V — for every t, μ, β. `symmetry_audit_sympy.py` returns PASS.

## Honest scope — what this folds and what it does not

- It folds the **site-configuration space** (one of the exponential factors, L^n) by an exact lattice
  symmetry. Real, verified, sympy-proven.
- It does **not** touch the **physical fermion sign** (orbit members share the same sign; this is
  redundancy removal, not cancellation), and it does **not** fold the Rossi per-evaluation 2ⁿ
  subset-recursion (a different exponential structure). The sign wall and the order-axis 2ⁿ stand;
  this is a constant-factor (|G_0|×) saving on the site sum, growing with lattice symmetry.

The frozen engine is untouched (194/194); `symmetry_reduction.py` wraps it. Reproduce:
`python3 symmetry_reduction.py` (numeric, PASS) and `python3 symmetry_audit_sympy.py` (symbolic, PASS).

## v51 update — column/row slices, and the fold scales with the point group

**Question.** Does a full *column slice* (a left-right reflection of the whole lattice) or *row slice*
(top-bottom reflection) **cancel** the sign (ratio C_V(σx)/C_V(x) = −1, the meron prize) or merely
**fold** (ratio +1, redundancy)? On the 2×2 these collapse into the single diagonal swap; to separate
them we measured on the 4×4 torus, where rows and columns are distinct.

**Result (measured + proven).**
- The stabilizer of the external site on the 4×4 is the **full square point group D4, |G_0| = 8** —
  every rotation and reflection, including the column-slice (left-right) and row-slice (up-down)
  reflections. (On the 2×2 it had collapsed to order 2.)
- **All eight fold; none cancels.** Ratio C_V(σx)/C_V(x) = +1.000 to ~1e-10 for every element,
  including the column and row slices. No σ gives −1. So a column slice removes redundancy, it does
  not cancel the physical sign.
- **Symbolically proven for all t (sympy):** the column- and row-slice reflections satisfy
  P^T·H(t)·P − H(t) = 0 on the 16-site lattice — an exact polynomial identity, every t.
- **The fold scales with the point group.** Folding the L^n site sum by the order-8 stabilizer is
  exact (match 3.3e-16 at n=2, 4.6e-15 at n=3) and gives **4.65×** fewer C_V evals at n=2 and
  **6.15×** at n=3, climbing toward |G_0| = 8 as n grows — versus 2× on the 2×2. So a larger, more
  symmetric lattice buys a larger exact fold.

**Honest scope (unchanged):** still a fold of the L^n site-configuration space (redundancy), now up
to the point-group order; still does NOT fold the Rossi 2ⁿ recursion and does NOT touch the physical
sign. The column/row slices are symmetries, not anti-symmetries. `square_point_stabilizer(Lx,Ly,hop)`
is the generator-based finder (no L! enumeration); reproduce via the extended `symmetry_reduction.py`
and `symmetry_audit_sympy.py` self-tests (both PASS).

## v52 update — 45-degree slices of the cube; the fold scales with dimension too

**Question.** Take the lattice into 3D — a cube of layers — and look at its *45-degree slices* (the
diagonal mirror planes of a cube, i.e. the axis-swap operations). Do they cancel (−1) or fold (+1),
and how large is the cube's fold?

**Result (measured + proven), 4×4×4 cube.**
- The stabilizer of the external site is the **full cube point group O_h, |G_0| = 48** (signed
  permutations of the three axes). Of these, **40 are 45-degree diagonal slices** (a non-trivial axis
  permutation = a diagonal mirror plane).
- **Every 45-degree slice folds; none cancels.** Ratio C_V(σx)/C_V(x) = +1.000 to ~1e-10 for the
  diagonal slices; no σ gives −1.
- **Symbolically proven for all t (sympy):** the axis-swap (45-degree) operations satisfy
  P^T·H(t)·P − H(t) = 0 — an identity in the hopping. (Proven on the small cube; the identity is
  structural and size-independent, since isotropic hopping is invariant under relabeling the axes.)
- **The cube buys a much larger fold.** Folding the N^n site sum (N=64) by the order-48 group is
  exact (match 5.2e-15) and gives **18.62×** fewer C_V evaluations at n=2, climbing toward |G_0| = 48
  as n grows.

**The pattern across dimensions and sizes:** the redundancy fold equals the order of the little group
of the external site, which grows with both lattice size and dimension — **2× (2×2 square) → 8× (4×4
square, D4) → 48× (4×4×4 cube, O_h)** — exact at every step, proven for all t. The 45-degree slices
are symmetries (fold), never anti-symmetries (cancel). Still the site-configuration factor only — not
the Rossi 2ⁿ recursion, not the physical sign. `cube_hopping(L)` and `cube_point_stabilizer(L,hop)`
are the 3D finders; reproduce via the extended self-tests (both PASS).

## v53 update — attacking the interior of the Rossi 2ⁿ: mask-fold (honest negative) + subset cache (real win)

**Question.** Can the proven symmetry machinery cut the per-evaluation 2ⁿ subset recursion itself?

**Part 1 — the mask-level fold (honest negative for the generic case).** A symmetry can fold the
masks *inside* one C_V only if it maps the vertex set to itself: it needs a vertex permutation π with
(p[s_π(i)], t_π(i)) = (s_i, t_i). Verified: on a deliberately **symmetric** config (two vertices on
diagonal-partner sites with **equal** times) the mask pairs are exactly identical (D_vac and D_corr
match to 1e-12; e.g. masks 001↔010, 101↔110), so the interior fold fires and is exact. But a
**generic** config (distinct continuous times) has trivial stabilizer — only the identity survives.
So the interior mask-fold is real but fires only on a measure-zero symmetric subset: **not a generic
2ⁿ cut.** Burnside again says why: the fold is set by fixed points, and generic configs have none.

**Part 2 — the real interior redundancy: subset memoization across the sum (measured win).**
D_vac and D_corr depend only on the vertex **subset**, not on which configuration is asking. Across
the enumerated site sum at fixed times the same subsets recur massively: at n=3 on the 4×4, the brute
enumeration performs 32768 subset evaluations (×2 kinds) but only **4913 subsets are distinct** (6.7×
raw redundancy). Caching them (`cv_cached`) and composing with the orbit fold
(`fold_site_sum_cached`):

| quantity | value |
|---|---|
| brute total (n=3, 4×4) | +0.00561802, 15.0 s |
| fold+cache total | +0.00561802, 1.1 s |
| match | 5.0e-15 |
| unique determinants | 2194 vs 65536 brute subset evals (**29.9× fewer**) |
| composition | orbit fold 6.15× × cache 4.86× |
| wall-clock | **13.9×** measured |

The two reductions are independent and multiply: the orbit fold cuts *which configs* are evaluated,
the cache cuts *the determinants per config*. Both exact; the totals agree with brute force to 5e-15.

**Honest scope.** The cache removes recomputation across an enumerated/quadrature site sum (it thrives
on shared times); it does not reduce the asymptotic 2ⁿ of a single isolated C_V on generic continuous
times (Part 1 is the proof of why). The physical sign is untouched throughout.
