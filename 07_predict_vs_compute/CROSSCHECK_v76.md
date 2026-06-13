# CROSSCHECK_v76 — the ring period: a null-calibrated negative with the impossibility quantified

**Claims.** (1) Pure re-analysis of the v75 fold (480k exact values; zero new engine sweeps):
shell-coherence f(r) = S(r)/Σ|v| over four radial coordinates (MST, sum-of-legs, R_max, perimeter),
detrended periodograms, pre-registered gates. (2) The near-miss: binned R_max periodograms peaked
within 9–10% of the continuum 2k_F at both fillings with the correct μ-shift — then KILLED by the
correct treatment: R_max is discrete (18 exact lattice radii); unbinned analysis + 1000-shuffle
permutation null gives p = 0.20 (μ=0.5) / 0.16 (μ=1.5): not significant. (3) Second trap caught:
perimeter's 16× low-q "peak" was trend leakage with the wrong μ-shift. (4) What is real: the
contact-shell coherence is strong and μ-flipped (+0.66 / −0.53, consistent with v68/v72); beyond
it the profile is amplitude-starved (|f| ≲ 0.1–0.3). (5) The structural impossibility: ξ_s ≈ 3.0 vs
period ≈ 1.2 → ~2 oscillations before decoherence on ~5 usable radii — L=6 cannot resolve the
period in principle; the route is larger L plus a coherence-boosted observable (the v68 line-sector
protocol). (6) Three standing lessons: permutation-null-calibrate spectral peaks; analyze discrete
coordinates unbinned; check ξ_s/period before designing a period measurement.

**Reproduce.** `cd 08_2d_interacting && python3 ring_period.py` → permutation p>0.05 at both
fillings from the stored exact profiles, contact-shell flip, amplitude starvation; "ring-period
self-test ... PASS" (~30 s). Profile provenance: the v75 fold pipeline (SHELL_FOLD_RESULT.md).

**Scope (honest).** One β, fixed times, two fillings; the stored profiles are exact fold outputs
transcribed to module constants (radii verified against the fold data); the negative is about
period *extraction at L=6*, not about the rings' existence — the exact shell alternation (v72/v75)
stands.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
