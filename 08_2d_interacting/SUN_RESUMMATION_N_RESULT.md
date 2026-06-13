# Queue #2 (SU(N)), step 4 + the gravity-loop hint, realized in N (v145)

Two findings, one mechanism.

## Step 4 — the record persists to second order

The second-order EoS coefficient n2(N) of the 2-site SU(N) lattice (from ED) is a low-degree polynomial in N: a
degree-3 fit on N=2..5 predicts N=6 to ~3e-4 (self-test: predict N=5 to 8e-4). The record is not a first-order
accident — it carries to the interacting EoS.

## The gravity-loop hint, found — it lives in N, not U

The uploaded gravity-loop math gets exact resummation because its loop coefficients obey a finite linear
**recurrence** → the generating function is **rational** → the series resums in closed form. v140 showed that
does **not** happen in our coupling U (only the atom is rational there). It **does** happen in the flavor number
N: the record makes every coefficient a polynomial in N, so

- the coefficients obey a finite linear recurrence in N (a degree-d polynomial has vanishing (d+1)-th finite
  difference — that *is* an order-(d+1) recurrence: c1's 3rd difference is **7e-15**),
- their N-generating-function Σ_N c(N) xᴺ is **rational**, denominator (1−x)^{d+1} (residual 7e-15),
- so the all-N dependence resums exactly: from c1 at N=1,2,3 we reconstruct **c1(6) exactly** (dev 0) and the
  large-N rate (the N² coefficient = −β·d²).

This is the **same mechanism** as the gravity loops (finite recurrence → rational GF → exact resummation),
realized in N rather than U. The shared structure is the recurrence; the spectra differ — our characteristic
root is 1 (polynomial growth, the record is combinatorial), the gravity cascade's was a cubic (exponential
growth). It is also exactly *why* CoS is N-independent: the N-resummation is built in. Compute a few small N,
get every flavor number — including N=6 (¹⁷³Yb) and N→∞ — in closed form.

## Net

So the gravity-loop resummation idea, which didn't transfer to the coupling (v140), transfers cleanly to the
flavor number — and it is the structural reason the SU(N) EoS is reachable at SU(2) cost. The remaining
engineering is unchanged: the full connected-determinant + closed-loop record + τ-integrals (v132 fast minors)
for the strong-coupling-in-U EoS curve.

Reproduce: `python3 sun_resummation_N.py`. ED is the anchor only; frozen engine untouched (194/194).
