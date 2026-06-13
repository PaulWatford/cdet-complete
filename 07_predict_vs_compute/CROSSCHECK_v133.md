# CROSSCHECK_v133 — physical mapping: z(∞) = the single-particle addition pole

**Claim.** z(∞) is a real spectral observable: the leading single-particle addition pole (lowest-empty
level). (1) z(∞)=ε_probe (ZINF v111). (2) z(∞) tracks the level as it sweeps with L (2.0→√2→1.268→1.082→
1.0002, v125), worst dev 4e-7 — a pole detector, not a constant. (3) v78 cancellation lemma: ⟨C⟩(μ) is
rational in fugacity e^{βμ}, poles only at μ=ε_k (verified in fugacity_structure.py). Bound: poles at the
BARE ε_k → z(∞) is the FREE addition energy; interacting ε_k+ReΣ needs the self-energy resummation =
integration #3.

**Reproduce.** `cd 08_2d_interacting && python3 physical_mapping.py` (and `fugacity_structure.py` for
the pole↔level detection).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
