# Porting the elementary Friedel object ρ(0,r) to C (v121)

v120 closed with one open fix: the elementary frozen Friedel object ρ(0,r) lived only in Python
(`frozen_friedel_map.py`, via numpy eigh). It is now in C — `cfriedel.c` — fully self-contained and
validated.

## The key: no eigenvectors are needed

The cube factorizes into three rings, so the eigenmodes are plane waves k=(kx,ky,kz) with
ε(k) = −2(cos(2πkx/6)+cos(2πky/6)+cos(2πkz/6)), and the projector matrix element is basis-independent:

    ρ(0,r) = Σ_{occupied k} U[0,k]U[r,k] = (1/N) Σ_{ε(k)≤1} cos(k·r).

So the C port computes ρ directly from the analytic plane-wave structure — **no eigenvectors, no
spectrum file, no eigendecomposition**. It is exact.

## Validation

`cfriedel test` self-validates against embedded Python eigh references (9 points, worst dev 4.8e-11).
A full 216-point cross-check against the Python eigh density matrix gives worst dev **4.81e-11** over
the entire lattice. The C sign-map (`cfriedel map 0`) is identical to the v119 Python map:

```
     x0 x1 x2 x3 x4 x5
y0:   o  +  -  +  -  +
y1:   +  -  -  0  -  -
y2:   -  -  +  0  +  -
y3:   +  0  0  0  0  0
y4:   -  -  +  0  +  -
y5:   +  -  -  0  -  -
```

The occupied count is 156 — matching `surr_l6_occupied(μ∈(1,2))` — and, because the spectrum is integer
(v120), the map is exactly μ-rigid in the window.

## What the port closes

The sign side now has the same three-layer C coverage the scale side has: the **elementary ρ**
(cfriedel.c, exact, self-contained), the **determinant A** (the stable/brute engines, whose sign is a
superposition of ρ), and the **distilled rigidity carriers** (surrogate `gap_modes`/`occupied`). The
v120 lesson "the elementary ρ is Python-only" is resolved — it is now C, cross-validated against
Python, and the full elementary sign object is available without any linear-algebra dependency.

None of this moves the wall. Build: `gcc -O2 -Wall -Werror -std=c11 -pedantic -o cfriedel cfriedel.c
-lm`. Reproduce: `./cfriedel test`; cross-check vs `frozen_friedel_map.py`. Frozen engine untouched
(194/194).
