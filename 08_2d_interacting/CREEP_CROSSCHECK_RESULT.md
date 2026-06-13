# The creep cross-checked both ways (v90, ledger #100): the deep object's law rewritten

**The directive:** run the C surrogate side and the brute-force side independently on Δ(β)'s decay
constant, pattern-hunt each, and compare.

**Brute force** (value-level deep-zero locations, L=6 (1,2,4), β=10–28, NT=1536): the trajectory is

> z(β) = 1.824(±0.022) − 0.72(±0.34)/β  (χ/dof 0.53) — pure logit **rejected** (χ/dof 2.90,
> and its fitted L=−3.29 contradicts the extracted −4.44).

Phase-0 catch en route: the v89 Δ(β) "decay" was an artifact of defining Δ against a baseline
extracted *at* β=20 — Δ(20)≈0 by construction; the right object is z(β) itself, and it is
anchored, not logit.

**Surrogate side** (arrangement + selectivity): the anchor sits 0.2σ from **2√2−1 = 1.8284 — the
L=8 static's exact anchor**, at a lattice whose integer spectrum contains no √2 (a possible
L-independent anchor), with **11/6 = 1.8333** (an L=6 Δk-rational) alive at 0.4σ. Unresolved at
±0.022; discrimination needs ±0.005 (queued). The selectivity table — sensitivity ~
1/(|p′(f\*)| f\*(1−f\*)) — explains why only the extreme roots feel the floor.

**The frozen discriminator decided the structure:** a spectrum-anchored static must be
geometry-independent; a per-geometry logit root must not. (1,3,5) value scans at β=12/20/28:
predicted 1.764/1.788/1.798, measured 1.7631/1.7889/1.7874 — **devs 0.001/0.001/0.011.
Universality wins.**

**The revision (banked openly; note added atop DEEP_PARTNER_RESULT):** the ~1.8 deep object is not
a Class-I logit trajectory — it is an **anchored, geometry-independent object of the static
class**, the third instance, now at L=6 where naive midpoints were excluded. The f\*=0.0116 root
remains a true property of the β=20 polynomial; the polynomial's deep tail is itself β-dependent
(the creep contaminates small-f extraction) — which is exactly why the logit flow failed and why
the two-window cross-check was the right instrument.

**What both sides of the coin showed:** brute force alone would have given an anchored fit with no
identity; the surrogate alone would have kept predicting logit. Together: a law-form correction,
a two-candidate anchor with a possible cross-L identity, and a decided universality.

**Open:** the anchor identity (2√2−1 vs 11/6, needs ±0.005); the slope's residue formula; whether
the L=8 and L=6 anchors are literally one L-independent object.

Reproduce: `python3 creep_crosscheck.py` (gates: model selection both ways; both anchor candidates
bracketed; the universality devs; a high-signal live bracket; PASS, ~25 s). Frozen engine
untouched (194/194).
