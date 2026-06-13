# Toward million-site lattices (v124): the projector fast path, the continuous freeze, and the run-to-log crash harness

Three improvements for large-L, day-long, unattended runs. Streaming was already in place (the engine
fflush-es every β line); the rest is new.

## 1. Projector fast path — the million-lattice optimization (exact)

The plane-wave propagator g0(Δr,τ) = (1/N) Σ_k cos(k·Δr) val(ε_k,τ) is regrouped by **distinct
eigenvalue**: g0 = (1/N) Σ_{distinct ε} [Σ_{k:ε_k=ε} cos(k·Δr)] val(ε,τ). The bracket P[Δr][ε] is
precomputed once for the ~7 fixed vertex displacements (O(N)); then each propagator is O(#distinct ε),
not O(N). It is **exact** — at L=6 it reproduces the direct path to the last digit (A=1.341555,
c1=−234.4268).

| L | N | direct | fast | collapse |
|---|---|---|---|---|
| 12 | 1,728 | 59.5 s | **0.81 s** (73×) | 40× |
| 48 | 110,592 | — | 32.5 s | 52× |

The collapse #distinct/N is ~40–50× (cubic + cos degeneracy), and the fast path also drops the per-mode
trig. **L=100 — a million sites — is a day-long z-flow** (~tens of MB memory, no stored spectrum).

## 2. Continuous-threshold freeze — the scale law on irrational spectra

For non-crystallographic L the spectrum is irrational, so the integer-level freeze (lround) mis-assigns
levels. The continuous freeze (mode 2) uses occupied = ε≤μ, probe = the **lowest-empty eigenvalue** (a
degenerate eigenspace) → s, rest physical. Test at **L=8**, μ=1.0: the lowest-empty eigenvalue is
**√2 = 1.41421** (irrational). z = √2 + ln(|A|/|c1|)/β rises 1.243 → 1.267 → 1.290 → 1.317
(β=24/48/72/96) toward √2. **The scale law z(∞)=lowest-empty-eigenvalue holds even when that eigenvalue
is irrational** — it is fully universal, not tied to integer levels.

## 3. Run-to-log harness + NaN guard — safe day-long runs

The engine now guards against non-finite output: at the precision wall it prints `# NONFINITE …` and
stops cleanly instead of emitting silent NaN. `run_to_log.py` launches the engine, streams every line to
a log (line-buffered + fsync, so partial results survive a hard crash), detects the NONFINITE marker, a
non-zero exit, or a killing signal, and writes a final STATUS + last_good_beta. No run timeout is
imposed — safe to leave running for a day. Both the harness and the guard are self-tested.

## How big can we go

- **Direct O(N) path**: comfortable to L≈16 (L=12 is 0.8 s/point with the fast path, 59 s direct).
- **Projector fast path**: L=100 (N=10⁶, a million sites) is a day-long z-flow run; the optimization is
  exact, so the science is unchanged.
- The binding constraint is no longer the lattice (no stored spectra, tens-of-MB memory) but the number
  of β points and statistics one wants — which a day-long unattended run, logged and crash-safe, covers.

None of this moves the wall, but it makes the wall probeable at the thermodynamic scale. Reproduce:
`./cpw grid 24 24 1 12 2048 31 0.002 0 2 1 2 4 1.845 -L 12 -fast` (fast path); `./cpw grid 24 72 24 12
2048 31 0.002 2 2 1 2 4 1.0 -L 8` (L=8 continuous freeze → √2); `python3 run_to_log.py selftest`.
Frozen engine untouched (194/194).
