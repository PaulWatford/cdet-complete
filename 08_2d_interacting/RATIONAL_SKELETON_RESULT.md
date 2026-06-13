# The rational self-energy hint: it lives in the skeleton expansion (v141)

v140 concluded the Hubbard self-energy series is not rational, so the gravity-loop 15-digit resummation route
doesn't transfer. That was the **grand-canonical** (fixed-μ) series — and the only non-rational ingredient
there is the density nd(U) drifting with U. Hold the density fixed and the structure is rational.

## The finding (atom, verified)

At fixed density n the self-energy is
**Σ(U) = U·n + U²·n(1−n)/(iω + μ − U(1−n))**, a [2/1] rational function of U. Its Taylor coefficients obey an
**exact one-term (geometric) recurrence**

  σ_{k+1} = [(1−n)/(iω+μ)] · σ_k    (k ≥ 2),

so the generating function is rational, and the [2/1] closed form reproduces Σ to **1.3e-15 at all U up to 3** —
past any bare-series radius. This is exactly the gravity-loop precondition (exact recurrence → rational GF →
exact resummation) that the grand-canonical series lacked.

| check | result |
|---|---|
| σ₁ = n | exact |
| 1-term recurrence (k≥2) | worst dev 2.0e-10 |
| [2/1] closed form vs exact, U≤3 | worst dev 1.3e-15 |

## Why this is the hint

The non-rationality is not intrinsic to the self-energy — it's the grand-canonical nd(U). The **skeleton /
bold expansion** (Σ as a functional of a *fixed* propagator/density — the Prokof'ev–Svistunov bold-line /
Luttinger–Ward object) removes exactly that dependence. So the rational / 15-digit route plausibly lives in the
skeleton expansion, not the bare one. That is the lead to pursue, and it matches the intuition that a rational
structure exists.

## Honest scope

Verified: the **atom**, at fixed density, is exactly rational (1-term recurrence, [2/1] exact). **Not** yet
shown: the **lattice** skeleton self-energy is rational — whether it inherits a finite (higher-order) rational
structure is the open question. This module is the bookmark plus the verified atom anchor; it does not claim
the lattice result.

Reproduce: `python3 rational_skeleton.py`. ED/closed-form is the anchor only; frozen engine untouched (194/194).
