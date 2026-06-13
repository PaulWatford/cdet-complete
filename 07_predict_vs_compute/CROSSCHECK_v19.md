# Cross-check proof data (v19) — the exact spin velocity vs the ED routes, across filling

v18 found the exact u_sigma below both ED routes at quarter filling. v19 tests that at a SECOND
doped filling (n=0.833, L=12, N=5,5, a closed shell) and assembles the full exact-vs-ED picture
across n = 0.5, 0.833, 1.0. Exact via the v18 plateau method (validated vs the half-filling Bessel
curve to 0.1-0.2%). Reproduce: `python doping_crossover.py` (~4-5 min; ED tabulated, Bethe live).

## The crossover table
| n | U | EXACT | stiffness | triplet | exact/trip | position |
|---|---|-------|-----------|---------|------------|----------|
| 0.500 | 2 | 0.9512 | 1.2623 | 1.1327 | 0.840 | below both |
| 0.500 | 4 | 0.8358 | 1.0309 | 0.9074 | 0.921 | below both |
| 0.500 | 8 | 0.5847 | 0.7083 | 0.6251 | 0.935 | below both |
| 0.833 | 2 | 1.4505 | 1.7668 | 1.5954 | 0.909 | below both |
| 0.833 | 4 | 1.2334 | 1.4421 | 1.2410 | 0.994 | below both |
| 0.833 | 8 | 0.8033 | 0.9376 | 0.8149 | 0.986 | below both |
| 1.000 | 2 | 1.6399 | 1.8328 | 1.2434 | 1.319 | between |
| 1.000 | 4 | 1.2263 | 1.4137 | 0.6464 | 1.898 | between |
| 1.000 | 8 | 0.7305 | 0.8431 | 0.3229 | 2.262 | between |
(n=1.0 EXACT is the Bessel value; ED at L=10. n=0.5, 0.833 ED at L=12.)

## Reading it — one crossover unifies v16, v17, v18
- The STIFFNESS is ALWAYS above the exact (an overestimate at every filling): exact/stiffness
  ~ 0.75-0.90, worst at quarter filling. It carries a positive finite-size correction, no
  marginal correction.
- The TRIPLET is above the exact when DOPED (an overestimate) but BELOW it at half filling. The
  SU(2)_1 marginal correction (strongest at the commensurate point, v17) drags the triplet down;
  exact/triplet climbs 0.84 -> 0.99 as n goes 0.5 -> 0.833 (the exact approaching the triplet
  from below), then at n=1 the triplet collapses (exact/triplet jumps to ~1.3-2.3) and the exact
  sits above it.
- So the EXACT lies BELOW BOTH ED routes throughout the DOPED regime (confirming and generalizing
  v18) and BETWEEN them only at half filling (the v16 result). The ED routes are upper bounds when
  doped; the "bracket" is a half-filling-only feature, exactly because the marginal correction
  that creates it is a commensurate-point effect.

## Status
GENERALIZED (v19): the v18 result -- exact u_sigma below both ED routes -- holds at a second
doped filling (n=0.833), and the exact-vs-ED relationship across n=0.5, 0.833, 1.0 is a single
smooth crossover that unifies the half-filling bracket (v16), the marginal-correction filling-
dependence (v17), and the doped-regime ordering (v18). The stiffness is the upper envelope at all
fillings; the triplet is the route that crosses. OPEN (v20): small-U exact u_sigma (U<2) needs an
iterative/adaptive Bethe solver (the dense uniform grid is both noise-limited at small U and too
costly to refine); and the exact u_sigma at a third doped filling would map the crossover finely.
