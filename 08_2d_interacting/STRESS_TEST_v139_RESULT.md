# Stress test of the hybrid plane-wave engine (v139)

A note first: the session's new features (fast minors, self-energy, the mapping) are verified **supplements**,
not yet wired into the hybrid — that is open item #5. This stresses what the hybrid actually carries: the
any-L plane-wave propagator, the `-fast` projector path, the continuous-freeze (mode 2), and the NaN guard.

## Where the hybrid is solid

| axis | result |
|---|---|
| validation | hybrid == stable @L6, **0.00e+00** |
| fast vs direct | **bit-identical** (L=6, L=12) — the projector path is exact |
| scale (mode 2, fast) | L=60 → 13 s · L=100 (1e6 sites) → 72 s · L=140 (2.7M sites) → 193 s |
| correctness at scale | freeze probe_val at L=100 = **1.000192** = surrogate exactly (direct ED infeasible) |
| robustness | NaN guard fires cleanly on every overflow — no crashes, exit 0 |

The fast path collapses ~50× at large L but still leaves ~60k distinct eigenvalues at L=140 — that count is
the per-propagator cost driver. As L grows, c1 shrinks (1.7e-4 at L=100, marginal vs its error): the v126
signal-budget law live — the probe merges into the sea.

## Precision (confirms the v138 learning)

Deep-β sweep at L=6, f64 vs long-double:

- **f64 walls at β ≈ 100** (A,c1 → NaN, the guard prints "precision wall" and stops). Last-digit noise from β≈60.
- **long-double reaches β ≥ 200** cleanly (A shrinking smoothly to 1.4e-3).

So: use `-DUSE_LD` for deep-β / deep-cancellation probes. f64 is fine to β≈80.

## Three silent / misleading failure modes — found and now guarded

The engine was *robust* (never crashed) but had three modes that produced wrong or mislabeled output silently.
All three are now guarded (input-only — valid runs are byte-for-byte unchanged, validation stays 0.00e+00):

1. **mode 0/1 at a non-crystallographic L** (L ∉ {1,2,3,4,6}, irrational spectrum) → the fixed probe level
   blows up to nonsense (z ~ 1e23) with no warning. *Guard:* warn and point to mode 2 (continuous freeze).
2. **large delta** → c1, a linear-response (s→0) derivative, is contaminated by the nonlinear regime (sign
   flip at delta=0.5). *Guard:* warn when delta > 0.1.
3. **delta = 0** → c1 = NaN; the NaN guard caught it but mislabeled it a "precision wall". *Guard:* refuse
   delta ≤ 0 up front with a clear message.

## Bottom line

The hybrid is robust and scales to multi-million sites; its real limits are (i) f64 precision past β≈100 (use
LD) and (ii) signal starvation at large L (intrinsic, the v126 law). The three input failure modes are now
guarded. Reproduce: `python3 stress_test_v139.py` (fast checks); the slow scans are the tables above. Frozen
engine untouched (194/194); the hybrid's val gate stays 0.00e+00.
