# Cross-check proof data (v18) — the EXACT spin velocity at quarter filling (and it corrects v16)

The item open since v13 is closed: an exact u_sigma(U) at quarter filling, via an integrated
(not endpoint-slope) Bethe route. Reproduce: `python bethe_spin_velocity_integrated.py`.

## Method — the PLATEAU, not the endpoint
v14 failed by reading the dressed-energy velocity eps_s'(Lambda)/(2 pi sigma(Lambda)) at the
spin Fermi point Lambda->infinity (a 0/0 limit at a truncated grid edge -> noise). The fix:
compute the velocity PROFILE v(Lambda) = |eps_s'(Lambda)|/(2 pi sigma(Lambda)) across Lambda and
read it where it is FLAT (a moderate-Lambda window, before grid noise). The asymptotic value
lives on that plateau. The |.| absorbs an overall sign convention in eps_s; the magnitude is what
the half-filling Bessel check validates. Plateau read = median of v over Lambda in [4,9].

## Validation at half filling (exact Bessel, v16)
| U | plateau | Bessel | err |
|---|---------|--------|-----|
| 2 | 1.6424 | 1.6399 | 0.2% |
| 4 | 1.2279 | 1.2263 | 0.1% |
| 8 | 0.7321 | 0.7305 | 0.2% |
0.1-0.2% -> the plateau method IS the exact spin velocity. The plateau is flat and grid-
independent (n=0.5 U=4: |v| = 0.8358 across Lambda=4..16, identical for NL=2400/3000/4000 and
Lmax=35/45/60). U<2 is resolution-limited (sharp kernels of width U/4; the plateau narrows and
grid noise overruns it -- the same wall v14 hit for the charge velocity), so only U>=2 is trusted.

## Result — exact u_sigma at QUARTER filling (U>=2)
| U | EXACT (Bethe) | v13 stiffness | v15 triplet | exact vs both |
|---|---------------|---------------|-------------|---------------|
| 2 | 0.9512 | 1.2623 | 1.1327 | below both |
| 4 | 0.8358 | 1.0309 | 0.9074 | below both |
| 8 | 0.5847 | 0.7083 | 0.6251 | below both |

## The correction to v16
v16 found, at half filling, triplet < exact < stiffness (exact closer to the stiffness) and
TRANSFERRED that bracket to quarter filling, concluding the exact u_sigma sat between [v15, v13],
near v13. The transfer was WRONG: the exact quarter-filling u_sigma lies BELOW BOTH ED routes.
The reason is exactly v17's mechanism -- the SU(2)_1 marginal correction that pushed the triplet
below the exact at half filling is SUPPRESSED by doping, so at quarter filling the triplet does
not drop below the exact; instead both finite-size (L=12) ED routes overestimate the
thermodynamic velocity, and the exact value sits beneath them. So v13 and v15 were UPPER BOUNDS,
not a bracket; the true u_sigma(n=0.5) is genuinely lower (e.g. ~17% below the v13 stiffness at U=8).

This is the exact computation overturning an inference -- the program working as intended. The
finite-size ED routes were correctly computed; the error was the v16 reading that the exact value
lay between them, which assumed a bracket structure that does not survive doping.

## Status
CLOSED (v18): exact u_sigma(U) at quarter filling for U>=2, via the validated dressed-energy
plateau (half-filling Bessel check 0.1-0.2%). The u_sigma arc is complete: measure (v13) ->
endpoint route fragile, exact-limit bracket (v14) -> second ED route (v15) -> exact half-filling
reference (v16) -> filling-dependence/generalization (v17) -> EXACT quarter-filling curve (v18,
correcting the v16 transfer). OPEN: small-U (<2) exact u_sigma needs an adaptive/finer spin grid
(the sharp-kernel wall); and the exact value's own finite-size-free confirmation of "ED routes are
upper bounds" could be sharpened with one more filling.
