# CROSSCHECK_v117 — the sign side: A's sign is a Friedel oscillation; one Fermi surface, two channels

**Claims.** (1) Scanning a vertex site along x (others fixed, β=24), sign(A)=(−,−,−,+,+) for x=1…5 —
a reproducible zero-crossing (seeds 31 & 777 agree; |A| minimal at the flip). (2) The wavelength is
long (~7.93 sites = 2k_F from μ=1.845 aliased), not period-2; μ near the band top → small Fermi
surface. (3) The Fermi surface governs both the scale (z=2 via its gap ξ₂=0.155) and the sign (via
its momentum 2k_F → Friedel ~8 sites). (4) v116 found sign/scale separate; v117 finds one shared
origin via two channels.

**Reproduce.** `cd 08_2d_interacting && python3 site_sign_friedel.py` (self-test PASS); the scan via
`./cse grid 24 24 1 16 2048 31 0.002 0 2 8 43 <j>` for j=1…5 (and seed 777).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
