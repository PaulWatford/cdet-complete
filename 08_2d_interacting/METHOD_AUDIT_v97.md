# METHOD_AUDIT_v97 — the parity-table round audited (outputs only)

The v97 round (the parity table, ledger #107) was audited against the KT-RG method v3.1
(Watford, April 2026). The method itself is not reproduced here; this document records the
audit's outputs: the scorecard, the steps run retroactively (which produced new content), and
the corrective plan adopted for v98.

## Scorecard

**Got right.** (1) The 4/4 parity pattern was converted to a registered prediction before
claiming a rule, and died by its own test — the round ends with an honest falsification instead
of a false rule in the ledger. (2) The v84 reread was a required-value-shaped move: asking what
the background must equal for the zero to sit at 1.8284, then measuring it (0.95 of the
deviation term). (3) The site-projection negative is a clean exclusion (translation invariance).
(4) Both instrument catches became permanent gates.

**Got wrong.** (1) Model diagnosis was skipped on a new instrument: the mask-tolerance bug
(1e-9 vs 1e-6 rounding) is an input-not-what-the-model-expects failure caught only after a
surprising second measurement — the false zero was briefly believed and stated. The
occupied-levels gate costs one line and belongs before the first measurement. (2) The
conditioning rule (s ≲ 10·e^(−βξ)) is a two-line derivation obtained instead by watching a 1e12
blowup. (3) The registered prediction was directional ("rises past 1.8284"), not quantitative —
weaker than the v94 standard of frozen numbers. (4) Only one branch was stated in advance
("A consistent with 0") with no magnitude expectation for the suppression branch, so the 3.8σ
result read as falsify-then-retreat instead of a measured discrimination between two stated
hypotheses. (5) Classification inflation: #107 asserts the v84 static "IS a root-flow crossing"
from one-point evidence — correct grade: CANDIDATE mechanism with a registered prediction.

**Missed (steps run retroactively below).** The differences table across windows; the deviation
written as ratios against framework integers; the portfolio re-prioritization; the stall check
on the four-round 13/7-vs-24/13 oscillation.

## Output 1 — the confound (the biggest miss)

Tabulating window differences beyond degeneracy parity exposes a confound the round never saw:
at L=8 the only odd-degeneracy level in range (2.0, deg 39) is also the only **rational** level
in an irrational spectrum, and at L=6 every level is rational. So "alive ⟺ odd first-empty
degeneracy" and "alive ⟺ rational first-empty level (ℚ-membership, the v93 field-theorem
object)" are confounded across the entire v97 table — and the falsification window
W8(0.828,1.414) (even AND irrational) is the one window where both hypotheses predict the same
outcome: it was the weakest available test. **The surviving "suppression pattern" is still two
patterns.** Corrective: the next parity window must be chosen for discrimination (an
even-degeneracy rational first-empty, or odd irrational), not convenience.

## Output 2 — the deviation as integer ratios (run now)

A_odd/A_even at β=28: 36.5 ± 24 (W6(1,2)/W6(0,1)); 33.6 ± 12 (W6(1,2)/W6(2,3)); 23.9 ± 7.3
(W8 pair). Framework-integer candidates: 36.5 vs deg 36; 23.9 vs 24 (suggestive); 60 excluded
at 4.9σ for the W8 pair. Verdict: the ratio test is **underpowered** — even-window A errors are
25–66%, so ratios exclude but cannot identify. Spec recorded: A_even to ±10% before the ratio
test means anything.

## Output 3 — the portfolio re-prioritization (reverses the v97 queue)

Scoring the open queue by difficulty and unlock leverage instead of recency:
COEFFICIENT PROGRAM PHASE 2 (difficulty 4, unlocks ~4: closes 13/7-vs-24/13, validates
root-flow quantitatively — making the L=8 crossover test partially redundant by predicting it —
and converts the residue formula from difficulty ~4 to ~2) outranks THE L=8 CROSSOVER TEST
(difficulty 3, unlocks ~2). The perceived phase-2 blocker (A to ±5% against heavy tails)
dissolves on diagnosis: v96 already measured that pointwise std decays at the same rate as A —
SNR is β-independent — so it is a bounded sampling-budget problem plus standard variance
reduction, not a wall. **v98 queue head: coefficient phase 2.**

The four-round 13/7-vs-24/13 oscillation (v93→v96) is a stall by any step count. The two clean
identifications in this sector (the β∈[10,32] anchored law; the exact L=8 balance check) were
both settled by exact structure, not by fitting noisy decay rates — the prescription converges
with the re-prioritization: attack the identification semi-symbolically through the census
coefficients' sign/cancellation structure, not through another rate fit.

## Output 4 — the prediction quantified (fixing the directional-only miss)

New measurement (mask gate run BEFORE measuring, per the corrective): A₈(40) = +0.1135(266) e-9
→ two-point decay rate 0.1231(233). Frozen curve (assumptions stated: c₁ frozen at the β=28
value −64 e-9, subexponential c₁ drift, single-exponential A₈ decay, single-term root
condition): z₈(β) = 2 − ln(|c₁|/A₈(β) − 1)/β gives

    z8(28) = 1.8268   [consistency: reproduces the v84 static 1.8284 at the measured β]
    z8(36) = 1.8378    z8(40) = 1.8417    z8(44) = 1.8449
    z8(48) = 1.8475 ± ~0.010 (rate error)    z8(56) = 1.8517

Sharpened registered prediction: the v84 "static" is already violated by +0.013 at β = 40 —
measurable at honest ±0.005 errors. The directional v97 prediction is subsumed.

## v98 corrective plan (adopted)

1. Queue reordered: coefficient phase 2 first (variance-reduction keystone), the L=8 deep scan
   second (it now tests the quantified curve above), the discriminating parity window third.
2. Standing protocol amended: model diagnosis (mask/conditioning gates) runs BEFORE the first
   measurement on any new instrument; every registered prediction states the expected magnitude
   under EACH live hypothesis; every suppression/enhancement factor is written as a ratio and
   tested against framework integers at registration time, with the power of the test recorded.
3. #107 classification corrected: "root-flow crossing" downgraded to CANDIDATE (one-point
   evidence) pending the curve test; noted in parity_table.py.
