# Dual-mechanism hunt (v60): τ-interference confirmed; anisotropy real but insufficient; a ~10× closed-line enhancement remains

**The hypothesis (user's call after the v59 falsification):** the single-variable law failed because
multiple mechanisms operate together. Three rounds, same freeze-then-predict discipline.

**Round 1 — more geometric variables: REJECTED.** Adding d_min, axis-alignment count, rank, τ-gap to
MST raises R² only 0.178 → 0.198 (all five combined). No second *geometric* variable carries it.

**Round 2 — τ-interference as mechanism 2: CONFIRMED.** Variance decomposition at fixed sites:
**within-geometry (τ-only) fluctuation = 39–40% of var(ln|C|)** — the v49 zero-crossing interference.
Integrating τ out **doubles** the geometric law (R² 0.18 → 0.48 at L=8; self-test reproduces 0.23 →
0.44 at L=6). The scatter that buried v59's law was largely τ noise. But the frozen prediction of the
τ-averaged class ratio still fails (8.7× vs measured 75.5×), and stratifying the 1d mixture exposed
the anomaly: **body-diagonal lines (longest MST, 5.20) are as heavy as axis lines (MST 3.00)** and
3.4× heavier than face-diagonals — weight does not follow Euclidean distance within the class.

**Round 3 — propagator anisotropy as mechanism 2b: REAL BUT INSUFFICIENT.** Measured decay per
Euclidean unit at L=8: ξ = 0.90 (axis), 1.21–1.24 (face), 1.20 (body) — diagonals ~35% slower; one
body-diagonal step nearly matches one axis step despite √3 the distance. (At L=6's short wrap-safe
range the anisotropy is only ~9% — range-dependent, flagged.) Folding it into an anisotropic
decay-metric MST does **not** close the gap: R² 0.32, frozen prediction 6.8× vs 75.5×.

**Verdict.** The dual structure is real — (geometry) × (τ-interference) — and accounting for it
doubles explanatory power. But a persistent **~10× enhancement of closed-line configurations** over
the bulk survives every distance-based law tried.

**Banked hypothesis for v61 (untested — do not cite as result):** on the torus the 1d lines are
closed **rings** — periodic 1d sub-chains with discrete spectra. Ring-closure/winding coherence,
which no tree/decay metric can express, is the candidate third component. (Rhymes with the v41 shell
physics: discrete-spectrum effects beating continuum-decay intuition.)

Reproduce: `python3 dual_mechanism.py` (gates: τ share 15–65%, averaging gain, L=8 anisotropy >10%;
PASS, ~2 min). Frozen engine untouched (194/194).
