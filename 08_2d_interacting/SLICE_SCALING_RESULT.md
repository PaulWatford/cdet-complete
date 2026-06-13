# The slice hierarchy survives scale — weight strengthens, sign persists and narrows (v57)

**The question (theory-extraction mode):** is the v54 slice hierarchy a 4×4×4 curiosity, or a
statement about the geometry of configuration space? Tested at L = 4, 6, 8 cubes (64 → 512 sites),
same protocol (n=3, μ=0.5, β=4), with **targeted** sampling of the rare 1d class (matched 900-sample
classes, noise floor 0.027). Enabled by `FastCDet` — the propagator's eigenmode loop vectorized,
validated against the frozen-port-validated CDet to **4.2e-17**, ~40× faster.

| L | 1d: mean\|C\| / R | bulk: mean\|C\| / R | 1d/bulk density ratio |
|---|---|---|---|
| 4 | 3.5e-06 / 0.652 | 1.1e-07 / 0.062 | **32×** |
| 6 | 5.4e-07 / 0.366 | 7.3e-09 / 0.064 | **74×** |
| 8 | 1.3e-07 / 0.244 | 8.1e-10 / 0.157 | **165×** |

(uniform-sample d=2 concentration likewise grows: 2.06× → 3.35× → 4.34×)

**Findings.**
1. **The weight hierarchy survives and strengthens:** per-configuration weight on 1d lines through the
   external exceeds the bulk by a growing factor (32× → 165×). Locality expressed as geometry.
2. **The sign hierarchy persists but narrows:** R(1d) decays 0.65 → 0.24 with L while the bulk sits
   at/near the floor. Flagged, unresolved: the L=8 bulk reads 0.157, above the floor — possibly
   heavy-tail inflation of the ratio estimator.
3. **v54 refined on the record:** its d=1 R=0.224 came from 12 uniform-sample configs (noise);
   targeted sampling gives 0.652 at L=4.

**Careful conceptual statement (what the data now supports):** the weight of the expansion is
concentrated in a geometrically identifiable low-dimensional sector whose per-configuration dominance
GROWS with system size, and that sector carries the healthiest sign; the diffuse bulk — exponentially
numerous, individually negligible, sign-incoherent — is where the variance lives. A measured geometric
structure of configuration space; not yet a theory of it.

Reproduce: `python3 slice_scaling.py` (validation gate 1e-12; hierarchy gates; PASS, ~60 s). Frozen
engine untouched (194/194).

## v58 amendment — the sign half of this result is downgraded

The universality sweep (v58) demonstrated that the per-class R estimator is heavy-tail fragile (same
cell: R(1d)=0.44 at 500 samples vs 0.02 at 400, same seed), and robust count-coherence is near the
binomial floor in most cells. The WEIGHT findings above stand (and are strengthened by median-based,
seed-stable re-measurement). The SIGN findings (R(1d) 0.65→0.24, "persists and narrows") are
downgraded to OPEN pending tail-aware statistics. See SLICE_UNIVERSALITY_RESULT.md.
