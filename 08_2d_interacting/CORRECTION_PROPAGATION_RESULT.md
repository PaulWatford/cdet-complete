# The correction propagated (v91): both prediction surfaces updated to the v90 law

**The directive:** "update both to correct" — propagate the v90 two-window correction (the L=6
deep ~1.8 object is an anchored, geometry-independent static, not a logit-flow root) into both
prediction surfaces, so neither the Python atlas nor the C surrogate can ever again predict the
superseded law.

**The C surrogate** (`csurrogate.{c,h}`, params, test): gains `ATLAS_L6_DEEP_A = 1.824`,
`ATLAS_L6_DEEP_B = −0.72` and the API `surr_static_l6_deep(beta) = A + B/beta`, with the v91
comment block recording the correction and the open anchor identity (2√2−1 vs 11/6). The Class-I
scope in the header is **corrected**: the logit flow applies to mid-range roots; deep (small-f)
roots live at the cancellation floor where the polynomial's tail is β-dependent — route them to
the static family. Closed-form checks of the new API added to the test; the fresh-seed gate
re-passed (match 3.55e-15) and the pedantic-C11 build is clean.

**The Python atlas** (`resonance_atlas.py`): gate-D's audit-catch object is recorded as RESOLVED
in the docstring; the atlas gains `self.l6_deep = (1.824, −0.72)` and `static_l6_deep(beta)`, plus
a **new audit gate G**: the corrected deep-static law against the v90 stored value-level zeros
(`creep_crosscheck.Z_124`), max dev 0.022 against a 0.025 gate. The integration audit is now A–G
and passes.

**The historical module** (`deep_partner.py`): a REVISED header now leads the docstring — the
Δ(β) "decay" framing was a baseline artifact; the three roots remain true properties of the β=20
polynomial; the deep tail is itself β-dependent. The stored data and gates are retained as the
historical record they test; the self-test still passes.

**Why this round matters:** a correction that lives only in a result doc is a correction waiting
to be forgotten. Both executable surfaces now carry the corrected law, the corrected scope, and a
gate (G) that would fail if the old reading ever crept back in.

Reproduce: `python3 resonance_atlas.py` (audit A–G, PASS), `python3 csurrogate.py` (fresh-seed
gate, PASS), `gcc -O2 -Wall -Werror -std=c11 -pedantic csurrogate_test.c csurrogate.c -lm`
(clean), `python3 deep_partner.py` (PASS). Frozen engine untouched (194/194).
