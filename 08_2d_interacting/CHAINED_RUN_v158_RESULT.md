# Chained two-round run — efficiency and expansion from continuing the electron's position

A pure micro-efficiency study: run each model twice, and let round 1's terminal electron position seed round 2.
The persistent "electron position" of the stochastic engine is its RNG stream state `st_`; round 1 ends there and
round 2 continues from it. Both the efficiency and the expansion gains turn out to come from this single act of
*continuing the stream* rather than restarting it.

## Applied improvement (hybrid, evolving model)

The hybrid now exposes its terminal sampler state at the end of a grid run (`# terminal_state <st_>`) — print-only,
no computed number changes (val still 0.00e+00). Feeding it as round 2's seed continues the same RNG stream, so the
two rounds are guaranteed independent and non-overlapping. The **frozen reference source is untouched.**

## Efficiency gain (measured, β=30, NT=2000, vs an NT=16000 reference)

| scheme | mean error vs reference |
|---|---|
| single NT=2000 run | 0.0443 |
| **chained 2×2000 (round-1 terminal seeds round-2)** | **0.0319** |
| naive same-seed rerun | identical — **zero new information** |

The chained continuation gives a **1.39× error reduction (≈√2)** — the correct scaling for doubling *independent*
samples, achieved because the continued stream never overlaps. A naive same-seed rerun produces identical samples
and adds nothing — so the terminal-state chaining is precisely what makes round 2 count. Practical micro-efficiency:
**refine by continuing (reuse round 1's work) instead of restarting at 2×NT.**

## Expansion gain (config-space coverage, 30 rounds, C(5,3)=10 configs)

| walk | distinct configs reached |
|---|---|
| deterministic, result-seeded (surrogate-evaluated) | 1–2 (**cycles**) |
| **chained RNG continuation (terminal-state seeded)** | **9 / 10 (no cycle)** |

A purely deterministic result-seed *cannot* expand — a map on a finite state space must cycle. The same chaining
that buys the √2 efficiency also breaks the cycle: the continued stream never repeats, so it sweeps the
configuration space. This is why the stochastic hybrid is the one that expands.

## The three models under chaining

- **Hybrid** (stochastic IS): chaining the stream → √2 efficiency **and** non-cycling expansion.
- **Surrogate / brute force** (deterministic): no stream to continue; pure result-seeding cycles. Their role is
  *evaluation* — the surrogate scores a config ~1000× faster than the exact CDet — while the stochastic
  continuation supplies the exploration.

Net: round 1's electron position is worth continuing, not just reading. Reproduce: `python3 chained_run.py` (~10s).
The frozen reference engine/ (194/194) is untouched.
