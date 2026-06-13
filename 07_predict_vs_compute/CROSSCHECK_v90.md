# CROSSCHECK_v90 (ledger #100) — the two-window creep cross-check

**Claims.** (1) Brute force (value-level deep-zero locations, L=6 (1,2,4), β=10–28, NT=1536): the
trajectory fits z = 1.824(±0.022) − 0.72(±0.34)/β at χ/dof 0.53; pure logit rejected (χ/dof 2.90;
fitted L=−3.29 vs the extracted −4.44). Phase-0 catch: v89's Δ(β) was defined against a baseline
extracted at β=20, so Δ(20)≈0 by construction — the trajectory, not the deviation, is the object.
(2) Surrogate side: anchor candidates 2√2−1 = 1.8284 (0.2σ — the L=8 static's exact anchor, at a
lattice with no √2 in its spectrum: a possible L-independent anchor) and 11/6 = 1.8333 (0.4σ, an
L=6 Δk-rational); both open at ±0.022, discrimination needs ±0.005; the selectivity table
(sensitivity ~ 1/(|p′| f(1−f))) explains why only extreme roots feel the floor. (3) The frozen
discriminator: geometry-independence (required by the anchored reading, forbidden by per-geometry
logit) measured at (1,3,5): predicted 1.764/1.788/1.798, measured 1.7631/1.7889/1.7874 — devs
0.001/0.001/0.011 — universality wins. (4) Revision banked openly (note atop DEEP_PARTNER_RESULT):
the ~1.8 object is the third static-class instance; the f\*=0.0116 root is real at β=20 but the
polynomial's deep tail is β-dependent (the creep contaminates small-f extraction). (5) The
two-window lesson: each side alone was wrong or anonymous; together they produced a law-form
correction, a two-candidate anchor with a possible cross-L identity, and a decided universality.

**Reproduce.** `cd 08_2d_interacting && python3 creep_crosscheck.py` → model selection both ways,
both anchor candidates bracketed, the universality devs, a high-signal live bracket;
"creep-crosscheck self-test ... PASS" (~25 s).

**Scope (honest).** Anchor unresolved between two candidates; the slope's residue formula and the
cross-L anchor identity are open; the live gate uses the high-signal case (the low-signal
(1,3,5)@β=20 point is heavy-tail under-sampled at modest NT and lives in the stored scans).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
