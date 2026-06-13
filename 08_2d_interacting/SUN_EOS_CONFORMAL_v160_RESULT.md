# Conformal-Borel resummation — pushing the order axis (the real CDet frontier)

Taking the field comparison seriously: in CDet the **lattice is the easy axis** — the method works directly in the
thermodynamic limit, so a 12×12 = 144-site run in ~30 s is comfortably in the validation range people use, and our
locality-aware design is fast there. The real frontier is **how many perturbative orders you can reach and resum**.
The literature bears this out:

- Practical CDet reaches **~10–13 coefficients** (vs ~6–7 for older DiagMC).
- The bare-U series has a **finite radius from a non-trivial analytic structure** in the complex-U plane (a branch
  point) — even the Hubbard atom shows multiple complex-U poles. This is exactly the v146 wall (the lattice
  self-energy is algebraic in U).
- The state-of-the-art fix is **conformal-Borel resummation** keyed to that singularity (Rossi–Van Houcke–Werner;
  Prokof'ev–Svistunov), plus shifting the expansion's starting point (homotopic/shifted action).

## What we added

A conformal-Borel resummation of the SU(N) EoS series: Borel-transform (b_k = n_k/k!), locate the Borel singularity
|t_c| via Borel-Padé poles (here **complex, |t_c| ≈ 1.05** → the series is Borel-summable), re-expand the Borel
function in the conformal variable w(t) = (√(1+t/U_c)−1)/(√(1+t/U_c)+1) by exact series composition, and Borel-sum.

## Result (2-site SU(N) reference, validated vs ED)

| U | ED | conformal-Borel err | Padé[4/4] err | improvement |
|---|---|---|---|---|
| 0.4 | 0.56741 | 3.8e-3 | 6.0e-3 | 2× |
| 0.6 | 0.51484 | 5.7e-3 | 2.0e-2 | **4×** |
| 1.0 | 0.43790 | 4.3e-2 | 7.2e-2 | 2× |

Conformal-Borel extracts **more physics per order from the same coefficients** — the order-axis win.

## Honest ceiling

Pushing the resummation *reliably* into strong coupling (U≈2.3, Kozik) is sensitive to the precise singularity
location — which is the field's genuinely hard part (it requires the large-order/instanton analytic structure). An
early run that placed |t_c| favorably reached U≈2.5 at ~4%, but that was not robust to the singularity estimate, so
it isn't claimed. The robust route to strong coupling remains the **v153 two-point bridge** (weak side + strong
atomic anchor); conformal-Borel is simply the better *weak-side engine* to feed it.

## The two levers, together

- **Reach per order** — conformal-Borel (this module): more physics from the orders you have.
- **Orders per unit cost** — the chained two-round continuation (v158–159): ~√2 variance reduction per round, for
  both the amplitude and the interaction response, lowering each coefficient's error so more orders are reachable.

Lattice size was never the bottleneck; these two are the axes the field actually pushes, and we now push both.

Reproduce: `python3 sun_eos_conformal.py` (~3s). The frozen reference engine/ (194/194) is untouched.
