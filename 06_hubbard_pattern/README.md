# 06 — Hubbard correlation pattern (standard test + animation)

The interference pattern of many electrons on a lattice, computed exactly.

## One command
```
python3 hubbard_pattern.py            # static figures + printed validation
python3 hubbard_pattern.py --anim     # also write the animated GIF
```
Options: `--L 10` (ring size), `--filling 1.0` (electrons per site; 1.0 = half),
`--Umax 8`. Needs python3 + numpy + scipy + matplotlib + pillow.

## What it computes
Exact diagonalization of a finite Hubbard ring, then:
- the spin correlation <S^z_0 S^z_r> in real space, for U/t = 0, 2, 4, 8;
- the charge structure factor N(q), showing the 2k_F and 4k_F features;
- an animated GIF of both as U ramps from 0 to Umax.

## What it shows
- U = 0: the weak free-fermion Friedel ripple.
- U large, half-filling: a clean alternating (-1)^r spin standing wave — the
  antiferromagnetic Mott pattern. The charge structure factor peaks at 2k_F.
- doped (e.g. --filling 0.6): the dominant wavevector moves off pi and the
  2k_F vs 4k_F weight shifts with U — the Luttinger-liquid competition.

## Built-in validation
At U = 0 the spin correlation must equal the analytic free-fermion result
-|rho(r)|^2/2. The script prints max|diff|; it is ~1e-17 (machine precision).
That is the honest self-check: the exact reference reproduces the known limit.

## Where this sits
This is the EXACT reference pattern, from exact diagonalization, which is capped
at small L by the exponential Hilbert space. It is the validation target the cdet
connected-determinant engine must reproduce at sizes ED cannot reach. The natural
next step is the cdet-vs-ED cross-check: the engine's finite-U correlators on the
same ring must land on these curves, then carry past the ED size wall.
