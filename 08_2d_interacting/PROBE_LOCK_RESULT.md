# Why z(∞)=2 is locked to level 2 (v114): the probe must be the Fermi surface — any other is Fermi-forbidden

v112–v113 found z(∞)=2 because level 2 is *both* the probe (the s-direction) and the smallest gap.
To test whether the mechanism generalizes — whether z(∞) simply tracks the probe level — the freeze
was generalized to an arbitrary probe (`cdet_stable_engine.c`, `set_freeze` with a `PROBE` level,
grid arg 10), and the probe moved from level 2 to level 3.

## The test

The background A is **identical** for probe=2 and probe=3 — at s=0 both freezes leave levels 2,3
empty, so only the s-*direction* differs. The response c1 = dC_V/ds is the discriminator:

| | probe=2 (Fermi surface) | probe=3 (test) |
|---|---|---|
| \|c1\| at β=24…72 | 237 → 156 (finite, decaying) | 3.8×10¹⁹ → 1.1×10⁷⁶ |
| \|c1\| rate | −0.009 (flat) | **+2.72 (diverges)** |
| z = 2+ln(A/\|c1\|)/β | rises to 1.89 → 2 | ill-defined |

probe=3's response **diverges exponentially**, exp(+2.72·β).

## Why — Fermi statistics, not coincidence

probe=3 forces **level 2** (the lowest empty level, gap 0.155) to 0 while scanning **level 3** (gap
1.155). Making level 3 occupied with level 2 empty is a **population inversion** — forbidden by Fermi
statistics. The connected determinant is expanded around the physical vacuum, which is unstable to
this perturbation, so the s-response diverges, with a free-energy cost that grows with β (colder =
more forbidden). Only probing the **lowest empty level** — the Fermi-surface level, level 2 — is a
physical excitation with a finite, well-defined response.

## Conclusion

z(∞)=2 is **locked** to level 2, not by coincidence but by structure: level 2 is the unique
physically-scannable probe. The three descriptions — *smallest gap*, *Fermi surface*, *the only valid
probe* — are the same statement. This sharpens v113: level 2's smallest-gap property is not merely
why its channel de-confines most; it is why it is the only consistent probe at all. The sign
structure compresses to one channel because there is only one channel it *can* compress to.

The mechanism does **not** generalize to arbitrary probes — and that non-generalization is itself the
content: the deep-β sign structure is pinned to the Fermi surface. None of this moves the wall.

Reproduce: `python3 probe_generalization_test.py` (self-test PASS); the divergence directly via
`./cse grid 24 72 16 12 3072 31 0.002 0 3` (probe=3) vs `… 0 2` (probe=2). Frozen engine untouched
(194/194).
