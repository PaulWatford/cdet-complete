# The site-choice generalization (v116): z(∞)=2 is geometry-independent; the SIGN is the geometric degree of freedom

v114 locked the probe to the Fermi-surface level. The one generalization the lock permits: vary the
lattice **sites** at fixed Fermi-surface probe and ask whether z(∞)=2 holds across geometries. The
engine was generalized (`cdet_stable_engine.c` grid takes optional sites). Prediction registered
before measuring: z(∞)=2 for all triples (the asymptote is the freeze's Fermi-surface level, not a
geometry property); rate varies.

## Result — five geometries, β=24/48/72

| sites | z = 2+ln(\|A\|/\|c1\|)/β | sign(A,c1) | physical root? |
|---|---|---|---|
| (1,2,4) | 1.785 → 1.853 → 1.887 | (+,−) | yes |
| (1,2,3) | 1.748 → 1.836 → 1.874 | (+,−) | yes |
| (1,5,25) | 1.764 → 1.847 → 1.882 | (−,+) | yes |
| (10,80,150) | 1.774 → 1.843 → 1.878 | (+,+) | no |
| (1,7,49) | 1.881 → 1.891 → 1.911 | (−,−) | no |

**Prediction confirmed.** The scale flow rises monotonically toward 2 in **every** geometry — compact,
spread, structured, both sign patterns. z(∞)=2 does **not** depend on the sites; it is the Fermi-
surface probe level. The approach rate varies as predicted ((1,7,49) at 1.88 by β=24 since |c1|≈16;
(1,2,3) at 1.75 since |c1|≈807) — different ln(β)/β prefactors.

## The new structure — sign is geometric, scale is not

Beyond the prediction: the **sign** of A and c1 varies by geometry. Opposite signs give a physical
leading root s* = −A/c1 > 0; same signs give s* < 0 (no physical small root). So:

- **The SCALE (z=2) is universal** — independent of probe (v114 Fermi-lock) and now of sites.
- **The SIGN structure is geometric** — which triples carry a physical zero-crossing depends entirely
  on the lattice geometry.

This is the anatomy of the sign problem, made explicit: the deep-β *scale* is pinned to the Fermi
surface no matter what; the *phase* — whether the connected determinant's background actually crosses
zero — is the geometric degree of freedom. **z(∞)=2 is doubly universal** (probe-independent and
site-independent), while the sign is where all the geometry lives.

## Net

The mechanism generalizes completely on the scale axis: every site choice, like every (forbidden-
otherwise) probe, gives z(∞)=2. The remaining content — the sign — is not a scale phenomenon at all;
it is geometric, and it is exactly what makes the determinant's zero appear or not. Sign and scale
separate cleanly. None of this moves the wall.

Reproduce: `python3 site_generalization_test.py` (self-test PASS); the grids via
`./cse grid 24 72 24 10 2048 31 0.002 0 2 <s0> <s1> <s2>`. Frozen engine untouched (194/194).
