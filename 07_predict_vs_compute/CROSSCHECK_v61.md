# CROSSCHECK_v61 — winding-phase ring closure falsified by a paired twist (unpaired artifact banked)

**Claims.** (1) The antiperiodic twist preserves |H| elementwise (gated True) — distances and
|hopping| identical, only the winding phase changes. (2) PAIRED per-config ratios (same sites, same
τ draws) show no axis-selective suppression and no mirror: x-lines 0.93×/0.99× and y-lines
1.14×/1.45× under twist-x/twist-y (bulk 0.70×/0.73×) — the winding-phase ring-closure hypothesis is
falsified; the ~10× line enhancement is closure-independent. (3) The UNPAIRED version of the same
experiment first produced an apparent 4× axis-selective suppression (0.24× vs 0.74×) — an unpaired
heavy-tail artifact, banked as such.

**Reproduce.** `cd 08_2d_interacting && python3 ring_closure.py` → |H| sanity gate, paired median
ratios (≈1.05×/0.84× at the self-test seeds), gates that both lie in [0.4, 2.5] (the falsification
itself); "ring-closure self-test ... PASS" (~90 s). Full two-layer narrative: RING_CLOSURE_RESULT.md.

**Standing methodology promoted.** In heavy-tailed systems, pair every comparison — same sites, same
τ draws, per-config ratios.

**Scope (honest).** L=6, n=3, one β/μ; the surviving 1d-channeling hypothesis is untested (v62).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
