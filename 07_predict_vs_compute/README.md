# 07 — predict vs compute

The two-path experiment, exactly as posed: build the answer two ways and cross-check.

- Path A (compute): exact diagonalization -> the true spin correlator <S^z_0 S^z_r>(U).
- Path B (predict): a model that generates the correlator WITHOUT the determinant
  sum, from one scalar (the local moment), by interpolating two reference shapes:
  the free-fermion form (analytic) and the strong-coupling form (computed once).

Run:
```
python predict_vs_compute.py --L 10 --filling 1.0     # half-filling
python predict_vs_compute.py --L 10 --filling 0.6     # doped
```

## What it found (honest)
The one-scalar crossover model reproduces the FULL spatial correlator to a few
percent across the whole interaction range:
- half-filling: mean RMS 1.7e-3 vs correlator scale ~0.082 (~2%); worst ~5% near U=2.
- doped n=0.6: mean RMS 6e-4 vs scale ~0.055 (~1%).
Exact (to machine precision) at the two anchor points, by construction.

The cross-check also did its job during development: it caught a sign error in the
on-site term of the free model (the residual blew up at U=0 where it must vanish),
which was found and fixed. That is the loop working as intended.

## What this means, precisely
- YES: for THIS observable, in THESE regimes, a cheap effective model predicts the
  expensive result to a few percent. You compute one local scalar instead of the
  whole correlator, and the pattern follows. That is a real, legitimate reduction in
  WHAT must be computed for the quantity of interest.
- NO: this does not reduce the 2^n perturbative-order sum. The order sum is
  unchanged and remains full rank. This is an effective model that replaces the
  computation where it is valid, not a compression of the underlying algorithm.
- The model is anchored: the free shape is analytic, the strong-coupling shape was
  computed once. The driving scalar (the local moment, equivalently the double
  occupancy) is known analytically in 1D from the Bethe ansatz, so the model can be
  made fully predictive with no diagonalization at all -- a direct tie to the
  Bethe-ansatz benchmark.
- It is a few-percent model: good for prediction and intuition, not for precision.
  Where it fails (the residual) is the map of where the physics is richer than a
  two-shape crossover -- near criticality and strong doping it will break, and the
  cross-check is exactly how you find that boundary.

## The honest headline
The instinct was right: the pattern often CAN be predicted cheaply instead of
computed. The precise statement is that an effective model captures the observable
to a few percent in the crossover regime, validated against exact, with the
cross-check defining its domain of validity. That is real, and it is how effective
theories earn their place -- it is not the collapse of the exponential wall.
