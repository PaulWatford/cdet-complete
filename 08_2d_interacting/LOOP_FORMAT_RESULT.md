# Do the uploaded tools help? (v106) — the gravity-loop resummation, assessed and adapted

Paul's `tests_and_scripts.zip` is the Watford FW-framework toolkit (gravity_loop_verification.py (uploaded, not bundled),
geometric_SUSY.py (uploaded, not bundled), the `fwverify` C suite). Assessed against the CDet deep-β program, with the
gravity-loop math and the "loop-format resolution for the tail" as the focus.

## What transfers — the gravity-loop closed-form resummation

The gravity-loop result: a sequence on a linear recurrence has a **rational generating function**,
so its formally-divergent tail resums in closed form, the asymptotics set by the dominant
characteristic root (there, P⁴). **This transfers to the deep-β series**, for a precise reason:
the deep-β quantities are finite sums of exponentials over the lattice spectrum,
A(β), ⟨C⟩(β) = Σ_k a_k e^(−βξ_k), ξ_k = level_k − μ. On a uniform β-grid that is *exactly* a
linear-recurrent sequence (Prony), roots e^(−ξ_k Δ); the dominant (slowest) root is the asymptotic
rate. **That is precisely the v105 bottleneck**: the deep static is ill-conditioned at high β
(vanishing slope + heavy tail), so z(∞) can't be reached by brute high-β measurement — but it can
be read off a recurrence fit at moderate, well-conditioned β.

## The enabling adaptation (why the naive form fails, and the fix)

Free-rate Prony is noise-sensitive — the framework's b_n were *exact integers*, so its recurrence
was clean; our measured points carry heavy-tail noise, and free-rate Prony returns unanchored or
spurious roots (a 4-point fit on the noisier naive A gave a negative root). The fix is unique to
this lattice: **the L=6 levels are exact integers {0,1,2,3}, so the decay rates ξ_k = level_k − μ
are known a priori.** Fitting only the *amplitudes* at known rates is a well-posed linear
least-squares problem — verified on clean stable A(β) (χ²=0.75/2) against the unanchored free-rate
fit. This is the usable "loop-format resolution for the tail."

## The honest target and the boundary

The static z(β) = 2 + ln s\*(β)/β with s\* ~ A/|c1|, so **z(∞) = 2 − (ρ_A − ρ_c1)** — the
*difference* of the dominant decay rates of A(β) and c1(β). A(β) at fixed μ decays at the trivial
level-2 rate (0.155); the non-trivial static needs the c1 channel too. So the resummation tool
resolves the asymptote **once A(β) and c1(β) are both measured clean on the stable engine + MoM** —
the closure is now well-motivated and the tool is in hand (`deep_beta_resummation.py`).

**What it does not do.** It does not touch the Monte-Carlo heavy tail (α≈1.06) — that is a
statistical sampling tail, not a recurrent series, and stays median-of-means (`deep_pool.py`).
The `fwverify` two-route + MPFR-to-30-digits pattern matches the v103 mpmath certifier — a
welcome confirmation of the certification methodology, not a new capability. geometric_SUSY.py (uploaded, not bundled)
is FW-physics closed-form derivation, unrelated to the sign program.

**Verdict: yes, partially and precisely.** The gravity-loop resummation is the right framework for
the deep-β *series* asymptote (the v105 tail), made usable here by the exact-integer spectrum
(known rates → well-posed amplitude fit). It does not help the MC tail or move the wall.

Reproduce: `python3 deep_beta_resummation.py` (channels; known-rate well-posed; free-rate contrast;
extrapolation; PASS ~5 s). Frozen engine untouched (194/194).
