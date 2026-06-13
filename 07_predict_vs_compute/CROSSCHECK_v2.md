# Cross-check proof data (v2) — predict vs compute

Half-filled 1D Hubbard ring, L=10. Path A = exact diagonalization. Path B = analytic
Lieb-Wu (Bethe-ansatz) prediction, no determinant sum. Reproduce: `python predict_vs_compute.py`.

## EXACT observable 1 — double occupancy d(U)
Path B is the Lieb-Wu integral d(U) = 2 int_0^inf J0 J1 sigma(wU/2)(1-sigma(wU/2)) dw.
| U | ED (Path A) | Lieb-Wu (Path B) | |diff| |
|---|---|---|---|
| 0.0 | 0.250000 | 0.250000 | 1.1e-16 |
| 0.5 | 0.233045 | 0.232960 | 8.6e-05 |
| 1.0 | 0.215738 | 0.215369 | 3.7e-04 |
| 2.0 | 0.178874 | 0.175453 | 3.4e-03 |
| 3.0 | 0.139552 | 0.133975 | 5.6e-03 |
| 4.0 | 0.104085 | 0.100241 | 3.8e-03 |
| 6.0 | 0.059256 | 0.058177 | 1.1e-03 |
| 8.0 | 0.037121 | 0.036640 | 4.8e-04 |
Status: EXACT and cheap. The residual is the finite-size gap between L=10 and the
thermodynamic limit (Lieb-Wu is the exact L=infinity value); it is not model error.

## EXACT observable 2 — ground-state energy per site e0(U)
Path B is the Lieb-Wu energy e0(U) = -4 int_0^inf J0 J1 / w * sigma(-wU/2) dw.
| U | ED/L | Lieb-Wu | |diff| |
|---|---|---|---|
| 0.0 | -1.294427 | -1.273242 | 2.1e-02 |
| 1.0 | -1.061441 | -1.040369 | 2.1e-02 |
| 2.0 | -0.863842 | -0.844374 | 1.9e-02 |
| 4.0 | -0.583432 | -0.573729 | 9.7e-03 |
| 8.0 | -0.331500 | -0.327531 | 4.0e-03 |
Status: EXACT and cheap. Residual is the known O(1/L^2) finite-size correction
(ED/L at L=10 vs the exact thermodynamic value).

## EFFECTIVE observable — spin correlator <S^z_0 S^z_r>(U)
Path B = interpolate(free shape [analytic], strong-coupling shape [one reference])
by the analytic moment <(S^z)^2> = (1 - 2 d(U))/4. Fully predictive (no ED scalar).
mean RMS 2.08e-3 vs correlator scale 0.082 (~2.5%); exact at the two anchors.
Status: EFFECTIVE model, honest few-percent residual. Not exact, by nature. This is
the boundary the program documents rather than hides.

## What v2 established
- Two observables (double occupancy, energy) are EXACT and cheap in 1D via Lieb-Wu;
  Path B reproduces Path A up to finite-size, with no diagonalization.
- The effective spin model is now fully analytic (analytic moment), trading ~0.4%
  accuracy (1.7e-3 -> 2.1e-3) for needing zero exact input.
