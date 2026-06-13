# The side-by-side (v94): both surfaces updated and parity-locked, the law tested out-of-sample — and the identification reopened

**The setup.** Both prediction surfaces carry the v93 law and the 13/7 competitor: the C
surrogate (`surr_static_l6_deep_law/alt`, ~ns) and the Python brute-force surface
(`atlas.static_l6_deep_law/alt`), parity-verified at 1e-15 across six β inside the csurrogate
gate. Out-of-sample predictions were **frozen to disk before any scan ran**: law → z(44)=1.8434,
z(52)=1.8419; competitor → 1.8467, 1.8483. The brute-force side used the certified honest
protocol (7-point grids, 4 draws × NT=2048, inter-draw errors, in-window quadratic + bootstrap;
a harness root-selection bug was caught and fixed at β=30).

**The measurements.** z(30) = 1.8138 ± 0.0037 — the **scope demonstration**: β=30 sits inside
the v92 crossover window, and both lines miss by ≥8σ exactly as the scope floor (β≈36) says they
must. z(44) = 1.8510 ± 0.0076 (law 1.0σ, competitor 0.6σ). z(52) = 1.8527 ± 0.0052 (law 2.1σ,
competitor 0.8σ).

**The verdict.** Out-of-sample: χ² 5.3 vs 1.0 — **~9:1 for 13/7**, against the v93 frozen test's
~80:1 for 11/6. Net: **the identification is reopened.** Over the six honest points (β=36–56)
all three readings fit — 11/6 refit (ln r = +3.11(50), χ²/dof 0.96), 13/7 refit (−2.98(58),
0.32), and a **constant 1.8467 ± 0.0021** (0.47). The constant reading revives the octagon chord
(0.5σ) and pushes both menu rationals out (5–6.5σ) — the **menu-vs-flatness tension**: a truly
flat z contradicts the exponent-balance menu as derived. The law's derivation, field theorem,
and L=8 verification stand; what's in question is the menu's degree bound — at order n=3, three
g₀ factors per spin plausibly cap weights at **6**, which would remove 13/7 and 15/8
structurally. That re-derivation is now the queue head: if weight ≤ 6 holds and z stays flat at
higher precision, the law needs a new term — or the chord needs a mechanism the field theorem
currently forbids. Freeze-then-predict did its job twice in a row: selecting 11/6 (v93), then
unselecting it (v94).

Reproduce: `python3 law_sidebyside.py` (frozen scoring; six-point fits; tension; scope; PASS,
<1 s) after `python3 csurrogate.py` (parity + DEEPLAW) and `python3 resonance_atlas.py` (A–I).
Frozen engine untouched (194/194).
