# The degree bound (v95): settled by a symbolic census — bound 7, menu corrected, tension dissolved

**The method.** The pure-Python CDet port runs on symbolic occupancies: one sympy symbol per
(spin, window level) for {0,1,2,3}, numeric saturation elsewhere, determinants through sympy,
the n=3 connected combination expanded exactly. Result: the exact polynomial of the stripped ⟨C⟩
in (f₂, f₃, δ₁, δ₀), with generic support taken as the intersection over independent τ draws.

**The theorem, verified.** Max total deviation weight at order n is **2n+1 = 7** at n=3 — the
up-spin determinant is (n+1)×(n+1) because it carries the external to/ti vertex (4 propagators
up + 3 down, each linear in occupancies). v93's "8" (matrix dimension, not propagator count) and
the v94-conjectured "6" (missed the external vertex) were both wrong. The support is **full**:
all 330 monomials up to weight 7 appear generically.

**The corrected menu.** Balance positions come from exponent *differences*, not positive-weight
pairs — v93's 3-member menu was doubly wrong. The realized candidate set near the object:
{25/14, 9/5, 20/11, 11/6, **24/13**, 13/7, 15/8, 17/9}, with μ\* = (2Δa+3Δb−Δc)/(Δa+Δb−Δc−Δd)
and q = |Δa+Δb−Δc−Δd|. All rational — the field theorem stands, the chord stays excluded. (The
v94 note "15/8 structurally excluded" is corrected: it is in the menu, dead only empirically.)

**The tension dissolved.** 24/13 = 1.84615 (q=13) sits 0.26σ from the v94 six-point constant
1.8467(21), and a q=13 balance approaches as ln(r)/(13β) — nearly flat over β=36–56. Fits:
11/6 χ²/dof 0.96; 13/7 0.32; **24/13 with ln r = +0.13(1.07): 0.48 — the "constant" reading is
the q=13 menu member.** The v94 menu-vs-flatness tension was an artifact of the wrong menu.

**Status.** Identification open among **{13/7 (q=7), 24/13 (q=13)}**, 11/6 disfavored; closing
routes: (a) **the coefficient program** — τ-average the 330 census coefficients (symbolic draws
or a numeric occupancy-design regression) and predict the realized zero outright, no fitting;
(b) deep-β precision (the two separate by ~0.005 at β=72, ~0.007 at β=100).

Reproduce: `python3 degree_bound.py` (census: 330/weight-7; menu; field; fits; PASS ~45 s).
Frozen engine untouched (194/194).
