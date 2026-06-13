# Cross-check (v30) — the atomic-reference lever, quantified and validated on the Hubbard atom

The real lever queued since v23: a reference closer to the correlated regime needs fewer orders AND
has smaller terms (curing the v29 cancellation). Demonstrated EXACTLY on the Hubbard atom, where the
oracle is the closed-form G_exact_atom (independently confirmed against the C engine).
Reproduce: python3 07_predict_vs_compute/atomic_reference_order_reduction.py.

## Setup
Atom: beta=4, mu=0.7, tau=1. The U-series for G has a fixed complex branch point at the partition-
function zero Z(U)=0: U_sing = 0.5192 -/+ 0.7854 i, |U_sing| = 0.9415. So the BARE expansion (around
U=0) has radius 0.9415 and cannot reach U=2. A "shifted reference" expands around U0>0 (a proxy for
the atomic/dressed reference); its radius is the distance from U0 to the branch point.

## Oracle value (independently cross-checked)
G_exact(tau=1, beta=4, mu=0.7, U=2) = -0.1911547846, identical from the Python closed form and the C
engine's G_exact_atom -- so the order-reduction numbers below sit on a verified anchor.

## The lever, quantified (target: 1e-6 accuracy at U=2)
| reference            | radius | reaches U=2? | orders to 1e-6 | largest single term |
|----------------------|--------|--------------|----------------|---------------------|
| BARE (around U=0)    | 0.9415 | NO           | NEVER          | 3.8e+12             |
| shifted (around 1.5) | 1.2565 | yes          | 11             | 0.27                |
| shifted (around 1.9) | 1.5885 | yes          | 3              | 0.20                |
The bare order-40 partial sum at U=2 is -4.79e12 (diverged garbage); the shifted ones hit the exact
value (err 5e-18 at U0=1.5, 5e-51 at U0=1.9). Order to fixed accuracy drops from NEVER to single
digits.

## The cancellation cure (the v29 link, made quantitative)
v29: the high-order wall is catastrophic cancellation -- a small result built from huge cancelling
terms. Here it is exact: the BARE expansion's largest single term is 3.8e12 while the answer is ~0.19
-- ~13 digits annihilate in the sum (which is why double precision and the Mobius +/- both fail
there). The shifted expansion's largest term is ~0.2, the SAME scale as the answer -- there is
essentially no cancellation. So a better reference does not just converge faster; it removes the
precision problem at its source. This is the control-variate PRINCIPLE (v29) realized: shrink the
residual, don't correct it afterwards.

## What this is, and what is next (honest scope)
This is the exactly-solvable PROXY that quantifies the lever: atom-Taylor-around-U0 stands in for
dressing the reference. In the many-body engine the realization is swapping the bare reference
propagator (lattice_G0) in cdet_order_mc (v27) for a shifted/atomic reference (G_exact_atom / a
shifted-mu propagator) and expanding in the residual coupling. The lattice version's reciprocal radii
were already validated on the 2-site dimer (v24, bare radius 4t vs atomic U/4). The remaining build
is the COUNTERTERM-correct wiring in cdet_order_mc's C path (a dressed/skeleton reference double-
counts self-energy insertions unless the counterterm is carried) -- that is the genuine multi-step
piece, NOT claimed here. What IS established now: the lever's payoff is exact and large (order to
1e-6 at U=2: infinity -> 3-11), and it is simultaneously the cancellation cure.

## Status
VALIDATED (v30): on the Hubbard atom (oracle confirmed vs the C engine), a reference shifted toward
the correlated regime cuts the order to 1e-6 at U=2 from NEVER (bare diverges) to 11 (U0=1.5) or 3
(U0=1.9), and shrinks the largest term from 3.8e12 to ~0.2 -- removing the catastrophic cancellation.
This quantifies the target for the cdet_order_mc reference swap. GATED (honest): the counterterm-
correct lattice wiring in C is the next build; the scheme is validated (atom here, dimer v24).
