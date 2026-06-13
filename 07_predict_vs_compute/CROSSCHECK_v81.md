# CROSSCHECK_v81 — the pair law: the limit set is the spectrum

**Claims.** (1) Windowed trajectory flows (grid 0.0125, NT=120, β=12–28, two L=6 geometries) give
four fits around level ε=1 with limits r = 1.047/1.004/1.019/0.959 (all within 0.05 of the level;
best rms 0.004) and pair-symmetric slopes c = −1.97/+1.79/−1.83/+2.50 — the law
μ\*± = ε ± c_ε/β. (2) The limit set of the resonance regime is the single-particle spectrum;
every "midpoint" sighting (L=6 candidates and the L=8 0.707/1.000/1.828 coincidences) was a pair
partner in flight. (3) Candidate arrangement: c = ln(deg(ε))/2 — deg(1)=36 exactly at L=6,
ln(36)/2 = ln 6 = 1.792, a 0.4% hit on the cleanest fit, within the pooled spread (2.02±0.3);
stated as CANDIDATE with the forward-proof step named (derive the residue ratio of
adjacent-particle-number Boltzmann families). (4) Honest residuals: level-2 partners grid-pinned;
a partner-conflation analysis trap caught and recorded; one outlier fit from multiplicity jitter.
(5) Falsifiable prediction, no free parameters: any (L, level) pair tightens as ln(deg)/2β — L=8
level-2's exact degeneracy fixes its flight path.

**Reproduce.** `cd 08_2d_interacting && python3 pair_law.py` → four stored-trajectory fits with
gates (r within 0.06, signs, c-range), the candidate check, and a live-engine partner measurement
at β=24; "pair-law self-test ... PASS" (~30 s). Survey scripts documented in PAIR_LAW_RESULT.md.

**Scope (honest).** One level fit-grade (ε=1 at L=6); level 2 characterized but grid-pinned;
candidate c-formula unproved; axis lines, n=3.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
