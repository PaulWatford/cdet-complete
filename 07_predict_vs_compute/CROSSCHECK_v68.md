# CROSSCHECK_v68 — governance of the signed weight: coherence scale ξ_s, μ-controlled phase, parity falsified

**Claims.** (1) Parity (product of sublattice signs) predicts the τ-averaged orientation at 50%
(μ=0.5) and 59% (μ=0) — falsified at both, including the PH point. (2) Sign coherence decays with
its own scale: ln r_g vs MST gives ξ_s ≈ 3.0 (binned r_g 0.73/0.40/0.21), ~3× the magnitude's
effective decay — sign outlives weight, explaining why the signed answer concentrates harder than
the unsigned one. (3) The orientation is a filling-controlled phase: extent-3 axis lines at L=6 are
94% negative at μ=0.5 and 75–100% positive at μ=1.5 (extent-4: 100%, r_g 0.81) — Friedel-class;
the L=4 vs L=6 orientation difference is k-grid phase, not contradiction. (4) Coherence, not
positivity, is the invariant (matched-MST: lines 85%, bulk 72%); v67's mechanism restated
accordingly, with this turn's own interim "compact ⇒ positive" framing corrected on the record.

**Reproduce.** `cd 08_2d_interacting && python3 sign_governance.py` → extent-3 orientation at both
fillings, the flip gate, ξ_s; "sign-governance self-test ... PASS" (~2 min). The full extent table
and parity tests are in SIGN_GOVERNANCE_RESULT.md.

**Scope (honest).** Qualitative phase law (flip + coherence + scale), not quantitative (no fitted
period vs k_F — the open theory item); 16 geometries/cell; one β; the μ=0 parity failure has a
suspected, unproven mechanism (v54 dressing).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
