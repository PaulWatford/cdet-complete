# CROSSCHECK_v105 — the robust deep-β flow rises and fits no menu line

**Claims.** (1) The certified robust pool is z(36)=1.8428(40), z(44)=1.8536(121),
z(52)=1.8642(61) — each the zero of stripped ⟨C⟩(μ) located from median-of-means μ-scans on the
stable engine. (2) The flow rises monotonically (slope ~0.0013/unit) vs the naive pool's
near-flat ~0.0005/unit, and passes 13/7=1.8571 by β=52. (3) No single menu law fits:
11/6 χ²=13.4/2, 24/13 9.4/2, 13/7 6.5/2, CONST 8.7/2 (all χ²/dof > 3). (4) Conclusion: the naive
pool's flatness — which drove v93–95 to {13/7, 24/13} — was a corrupted+heavy-tailed artifact;
the certified rise+curvature require the v100 assembled root flow, not a menu line; the
identification is reopened as a flow. (5) Honest limit: 3 points, growing errors, ill-conditioned
high-β static — the rise is ~2–3σ; the solid claim is that the naive flatness does not survive.

**Reproduce.** `cd 08_2d_interacting && python3 deep_pool.py` (retraction; re-anchor;
faithfulness; live MoM; flow; PASS ~30 s).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
