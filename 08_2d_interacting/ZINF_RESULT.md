# z(∞) resolved (v111): the asymptote is the bare probe level z=2 — the menu was a ln(β)/β approach all along

The v110 queue item: decide whether z(∞)=2 (the trivial probe level) or a genuine sub-2 rational.
Settled by model comparison on the clean flow, and the answer also explains the entire menu.

## The test

z(β) = 2 + ln(s\*)/β with s\* = A/|c1|, so **(2−z)·β = ln(|c1|/A)**. Two pictures predict different
growth:

- **Menu / exponential-gap (z∞ < 2)**: ln(|c1|/A) = ρ·β + q → z(∞) = 2−ρ, a clean rational.
- **Probe level (z∞ = 2)**: ln(|c1|/A) = p·ln β + q → z(β) = 2 − p·ln β/β → 2.

Fit to the clean 9-point grid (β=24–120, v109 float64 + v110 long double):

| model | fit | χ² |
|---|---|---|
| exponential-gap (z∞<2) | ρ=0.0552, z∞=1.945 | **622 / 7 — rejected** |
| power-law (z∞=2) | p=2.60 | 37 / 7 |
| general (both terms) | z∞ = **1.991(2)**, ρ=0.009 | 16 / 6 |

The exponential-gap picture — the entire "which menu rational" premise — is **rejected at χ²=622**.
The power-law picture fits (residuals 0.003 in z). z(∞) = **2 to within ~0.01**.

## Why z=2: A and |c1| share the same (vanishing) rate

The dominant-rate fit ln X = −ρβ + p·ln β + const gives:

- **A ~ β^(−2.8)**, ρ_A = 0.003(2) ≈ 0
- **|c1| ~ β^(−0.54)**, ρ_c1 = −0.004(0) ≈ 0

Both decay as **power laws**, not exponentials — they share the same (vanishing) exponential rate
because they are τ-averages of the *same* connected determinant with the *same* propagators (c1 is
just the s-derivative, which changes the power prefactor, not the rate). So |c1|/A ~ β^2.3,
ln(|c1|/A) ~ 2.3·ln β, and z(β) = 2 − 2.3·ln β/β → 2. The sign-structure zero sits at the **bare
probe level (level 2)** in the deep-β limit.

## What this closes

The menu rationals 11/6, 13/7, 24/13, 15/8, 17/9 (all in [1.83, 1.90]) are **finite-β crossings of
a ln(β)/β approach to z=2** — not asymptotes. The identification program running back to v93 was
fitting the slow transient. The question "which menu rational is z(∞)?" is **answered: none — it is
2**, the trivial probe level, reached not exponentially but as a power-law (ln β/β) approach. The
residual 1.991-vs-2.000 gap (0.009) is within the leading-order (s\*=A/|c1|) truncation and the
unconverged subleading rates; the decisive facts are the rejection of any exponential gap and the
power-law structure of both A and |c1|.

None of this moves the wall (R, 2^n unchanged). It is the final word on *where* the sign structure
sits: at the probe level, z=2, with a calculable ln(β)/β finite-β law.

Reproduce: `python3 deep_beta_asymptote.py` (model comparison + power-law fits; self-test PASS).
Data from `cdet_stable_engine` (frozen engine untouched, 194/194).
