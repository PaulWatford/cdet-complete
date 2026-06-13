# Can the gravity-loop "high precision via resummation" idea improve our accuracy? (v140)

The uploaded `gravity_loop_verification` reaches exact 15-digit resummation because its loop coefficients b_n
obey an **exact** linear 3-term recurrence → the generating function is **rational** → the series sums to a
closed form with no truncation. Honest answer to "can we do this for all our models": **partially, and not
the way that gives 15 digits.** Four findings, all tested against the exact ED self-energy.

## 1. The exact-recurrence trick does NOT transfer

Our self-energy coefficients σ_n obey **no** finite linear recurrence (order-2…5 fits give 3.5e-2 … 5.4e-4
prediction error, never zero). The generating function is not rational — the Hubbard partition function
contributes a transcendental e^{−βU}. So there is no exact closed form and no 15-digit resummation by that
route. (Their b_n give exactly 0; ours never do.)

## 2. Padé resummation transfers for REACH, not precision

A [m/n] Padé of Σ(U) analytically continues past the bare-series radius (~0.8): at U=3 it turns a **3.2e13
divergence into a 0.23 estimate**. But the residual past the radius is ~0.2–1 (structure-limited: Padé is
rational, Σ is not), and *inside* the radius the bare series is far better. So Padé is a strong-coupling
**reach** tool (the v138 open item #3), not a precision tool.

| U | bare series (order 24) | Padé [8/8] |
|---|---|---|
| 0.6 (inside) | 4e-4 | 7e-3 (worse) |
| 1.0 | 1e2 diverged | ~1 |
| 2.0 | 2e9 diverged | ~0.7 |
| 3.0 | 3e13 diverged | 0.23 |

## 3. Where we already have exact resummation

Most of our models are not truncated series at all: the **engine** computes the connected determinant exactly
(the Rossi recursion is exact); the **surrogate** carriers are closed-form; the **Dyson** relation
G = G₀/(1−ΣG₀) is itself an exact rational resummation in Σ. There is no truncation there to improve — they are
already at the resummation endpoint.

## 4. The general accuracy lever is extended-precision ARITHMETIC

The gravity-loop reaches 15 digits via exact (sympy) arithmetic. Our analog is **long double / mpmath in the
cancellation-dominated regimes**: the hybrid's LD build reaches β ≥ 200 where f64 walls at β ≈ 100 (v139).
That — not resummation — is the lever that improves accuracy across models, applied where catastrophic
*cancellation* (not series truncation) is the bottleneck.

## Net

Resummation extends our strong-coupling **reach** (Padé, #3); high **precision** comes from extended-precision
arithmetic (LD/mpmath) in cancellation regimes. The exact-recurrence 15-digit route is specific to a rational
series and does not apply to the Hubbard self-energy. (Different physics project; only the *mathematical*
technique was assessed.) ED is the anchor only; frozen engine untouched (194/194). Reproduce: `python3
resummation.py`.
