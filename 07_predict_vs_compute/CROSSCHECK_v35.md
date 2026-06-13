# Cross-check (v35) — refreshing the frozen baseline to the validated best version

v34 fixed the quad.c np>64 overflow in the sandbox and left a note: carry it into engine/ at the next
deliberate baseline refresh. v35 is that refresh. The frozen baseline engine/ is updated to the best
tested version by promoting the validated core improvements; the discipline is to prove the promotion
moved no number.

## What was promoted (engine_exp/ -> engine/)
Only two core files differed between the sandbox and the baseline, and both were already validated
bit-identical in output:
- cdet_engine.c -- v26 buffer removal: fixed MAXDIM[18] / sub[16] arrays replaced by dynamic arrays
  sized to n, plus an OOM-safe NaN guard on the 2^n allocation. Removes the n<=16 order cap.
- quad.c        -- v34 fix: Gauss-Legendre node/weight arrays sized to np (were fixed double[64],
  overflowed the stack for np>64).
Everything else in engine/ (driver.c, lattices, schur, rankone, symmetry, all headers, main.c, the test
harness) is unchanged.

## Proof the refresh changed nothing numerical (invariant, all hold)
- cdet_order(1,2) @ L=6,beta=4,mu=0.7,t=1,tau=0.123/0.877,np=40 = -0.5082750022348369 /
  0.44040518398732875 -- bit-identical to pre-refresh.
- C_V n=8,12,16 (hexring beta=4,mu=0.7,t=1; tau_out=1.5,tau_in=0.5) = 4.107893936632339e-08 /
  5.2004546552889602e-10 / 3.6922703728839982e-11 -- bit-identical.
- engine 194/194 vs the independent Python reference (1e-9).

## What the refresh bought (new capability in the baseline)
- C_V now runs for n>16: n=17 = -6.03985223334e-11, n=18 = 3.16138279764e-11 (previously MAXDIM-capped).
- cdet_order now runs for np>64: np=96 reproduces the np<=64 value (-0.508275002235 / 0.440405183987;
  previously a stack overflow).

## Methodological consequence (stated openly)
The old audit notion "baseline pristine = still carries the MAXDIM[18]/sub[16]/node[64] caps" is RETIRED.
The baseline's defining property is now: reproduces the invariant constants above + Python 194/194, AND
is buffer-free / OOM-safe. After this refresh engine/ core and engine_exp/ core are intentionally
identical (md5-equal cdet_engine.c and quad.c); engine_exp/ additionally carries the experimental tools
(diagmc, cdet_config, blocked_cv, ...). The two-engine *core* bit-identical gate is now trivially true;
the real standing check is the invariant constants. Future unvalidated work forks from this refreshed
baseline into engine_exp/, as before. See engine/BASELINE_FROZEN.txt.

## Status
DONE (v35): the frozen baseline is refreshed to the validated best version -- dynamic buffers + OOM-safe
+ np-sized quadrature -- with every frozen constant preserved bit-identically and the n<=16 / np<=64 caps
removed. The v34 config interface (PLAIN/BLOCKED/CVAR) and all its gates are unchanged and still pass.
