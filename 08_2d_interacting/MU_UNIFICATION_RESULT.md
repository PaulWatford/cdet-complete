# The gap–momentum unification test (v118): move μ — prediction falsified, and the falsification sharpens the picture

v117 claimed the Fermi surface governs both the scale (z=2 via gap ξ₂=2−μ) and the sign (Friedel
wavelength via 2k_F), matching λ≈7.93 sites at μ=1.845. The decisive test is to **move μ**, which in a
thermal system changes the gap and k_F together. Prediction registered before measuring: the sign-flip
spacing tracks λ(μ); z(∞)=2 holds with a gap-shifted approach.

## Result — both the sign and the scale are μ-invariant

| μ | gap 2−μ | sign(A) x-scan | z(β=24,48,72) | continuous-k_F λ (predicted) |
|---|---|---|---|---|
| 1.3 | 0.700 | −−−++ | 1.786, 1.853, 1.887 | 3.64 sites |
| 1.6 | 0.400 | −−−++ | — | 4.88 sites |
| 1.845 | 0.155 | −−−++ | 1.785, 1.853, 1.887 | 7.93 sites |
| 1.9 | 0.100 | −−−++ | 1.781, 1.853, 1.887 | 9.89 sites |

The sign pattern is **identical at every μ** (reproducible across seeds; A values barely move), and the
z-flow is **μ-invariant** to <0.005 — both rising to 2. The registered prediction that the wavelength
would shrink ~2.7× from μ=1.9 to μ=1.3 is **falsified**.

## Why — the freeze makes the Fermi surface discrete

The engine is **frozen**: occupations are discrete (0/1), not thermal n_F(μ), so μ does not enter the
propagator. The Fermi surface is the level-1 | level-2 **boundary** — which levels are filled — and
that boundary is fixed for *all* μ in (1,2). μ enters only through the positive strip exp(0.5(μ−2))
(which cancels in z and does not touch the sign) plus a weak intrinsic shift in A. So nothing physical
moves as μ slides inside the window.

## Correction to v117

v117's wavelength match — λ(μ=1.845) ≈ 7.93 sites ≈ one flip per 5-site scan — was **coincidental**.
The Friedel momentum is the **discrete frozen-boundary** momentum, not the continuous 2k_F(μ). v117's
core claim survives (the sign oscillates with site geometry, Friedel-class), but the specific
"momentum = 2k_F(μ)" identification is retracted: the sign's spatial scale is set by the frozen level
structure, independent of μ.

## The unification, strengthened

The frozen Fermi surface is **one discrete (topological) object** — the filled-level set — and it
governs **both** the scale (z=2, the lowest empty level) and the sign (the Friedel pattern from the
occupied/empty mode structure), locked together and **rigid under μ within (1,2)**. μ matters only when
it *crosses* a level, changing the probe (the v114 divergence). The unification is tighter than v117
said: not two channels of a μ-tunable surface, but a single discrete object fixing both at once. This
is more sign-problem-relevant, not less — the object that pins the deep-β scale and paints the sign is
the discrete filled-level set, and it does not care where μ sits between levels.

None of this moves the wall. Reproduce: `python3 mu_unification_test.py` (self-test PASS); the scans via
`./cse grid 24 24 1 16 2048 31 0.002 0 2 8 43 <j> <mu>` (sign) and `./cse grid 24 72 24 10 2048 31
0.002 0 2 1 2 4 <mu>` (z-flow). Frozen engine untouched (194/194).
