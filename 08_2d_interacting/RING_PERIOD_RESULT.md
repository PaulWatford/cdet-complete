# The ring period (v76): not resolved — the spectral near-miss killed by permutation null, and the structural reason quantified

**The attempt** (pure re-analysis of the v75 fold's 480k exact values, zero new engine sweeps):
shell-coherence profiles f(r) = S(r)/Σ|v| — envelope divided out — over four radial coordinates,
detrended periodograms, pre-registered gates (prominence both fillings; μ-shift; within 25% of 2k_F).

**The seduction and the kill.** Binned R_max periodograms peaked within **9–10% of the continuum
2k_F at both fillings, with the correct μ-shift** — everything the Friedel story wants. But R_max
is a *discrete* coordinate (18 exact lattice radii); the correct unbinned treatment plus a
1000-shuffle permutation null gives **p = 0.20 / 0.16: not significant.** The binned peaks were a
coincidence that null calibration caught — the v58 lesson in spectral form. (A second trap also
caught: Perimeter's spectacular 16× low-q "peak" was trend leakage with the *wrong* μ-shift.)

**What the exact discrete profiles actually show:** strong coherence at the contact shell only —
**+0.66 at μ=0.5, −0.53 at μ=1.5 (μ-flipped: real structure, consistent with v68/v72)** — then
|f| ≲ 0.1–0.3 everywhere after: the oscillation is amplitude-starved beyond the first radius.

**The structural reason (why L=6 cannot resolve the period even in principle):**
ξ_s ≈ 3.0 (v68) against a predicted period π/k_F ≈ 1.2 → **only ~2 oscillations fit before
decoherence**, sampled at ~5 usable lattice radii with coherence already <10%. Period extraction
requires larger L *combined with* a coherence-boosted observable (the controlled line-sector
protocol of v68, where coherence is high by construction) — not more analysis of bulk shells.

**Standing lessons (three, each bought here):** spectral peaks are not measurements until
calibrated against a permutation null; discrete coordinates must be analyzed unbinned — arbitrary
bin widths manufacture structure; and check ξ_s/period *before* designing a period measurement —
a coherence length under ~3 periods makes extraction impossible regardless of statistics.

Reproduce: `python3 ring_period.py` (gates: permutation p>0.05 at both fillings reproduced from the
stored exact profiles; contact-shell flip; amplitude starvation; PASS, ~30 s). Profiles' provenance:
the v75 fold (SHELL_FOLD_RESULT.md). Frozen engine untouched (194/194).
