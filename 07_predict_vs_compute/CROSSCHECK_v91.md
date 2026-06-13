# CROSSCHECK_v91 — the correction propagated into both prediction surfaces

**Claims.** (1) The v90 law (the L=6 deep object is an anchored, geometry-independent static,
z = 1.824 − 0.72/β; logit rejected) now lives in both executable surfaces. (2) C surrogate:
`ATLAS_L6_DEEP_A/B` + `surr_static_l6_deep(beta)` with the open anchor identity (2√2−1 vs 11/6)
documented in the params header; the Class-I scope corrected (logit flow = mid-range roots only;
deep small-f roots live at the cancellation floor where the polynomial tail is β-dependent — route
to the static family); closed-form API checks added; fresh-seed gate re-passed (worst dev
3.55e-15); pedantic-C11 build clean. (3) Python atlas: gate-D's object recorded RESOLVED;
`static_l6_deep(beta)` added; new audit gate G checks the corrected law against the v90 stored
value-level zeros (`creep_crosscheck.Z_124`) at max dev 0.022 vs gate 0.025 — the audit is now
A–G and would fail if the superseded reading crept back. (4) The historical module
`deep_partner.py` leads with a REVISED docstring header (the Δ-decay framing was a baseline
artifact; the stored data is retained as the record its gates test); self-test PASS. (5) No new
physics claimed this round — this is consolidation/correction discipline.

**Reproduce.** `cd 08_2d_interacting && python3 resonance_atlas.py` → "resonance-atlas
integration audit (A-G): PASS"; `python3 csurrogate.py` → gate PASS; `gcc -O2 -Wall -Werror
-std=c11 -pedantic -o t csurrogate_test.c csurrogate.c -lm && ./t` → all cases match;
`python3 deep_partner.py` → PASS.

**Scope (honest).** The anchor identity remains open (needs ±0.005); the slope's residue formula
underived; gate G tests against the v90 measurement set, not fresh data.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
