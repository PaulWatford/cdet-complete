# CROSSCHECK_v125 — the large-L study: z(∞) marches to the continuum Fermi level

**Claims.** (1) Frozen prediction (analytic): at μ=1.0, z(∞)=lowest-empty eigenvalue closes onto μ as L
grows, gap~L⁻³·³ (L=6→2.0, L=8→1.414, L=16→1.082, L=48→1.0009, L=100→1.00019). (2) Fast-path z-flows
track each L's lowest-empty value; the asymptote marches 1.414→1.268→1.082→1.0002 toward μ=1.0. (3) L=100
(1e6 sites) ran at 52s/point via the fast path (45× collapse, 22027 distinct eigenvalues); reported
probe_val=1.000192 == prediction. (4) Finding: z(∞)→μ thermodynamically but the signal (A, c1) vanishes as
the gap closes — signal-starved, the wall sharpens onto μ.

**Reproduce.** `cd 08_2d_interacting && gcc -O2 -Wall -Werror -std=c11 -pedantic -o cpw
cdet_planewave_engine.c -lm`; `./cpw grid 24 24 1 4 256 31 0.002 2 2 1 2 4 1.0 -L 100 -fast` (million-site
point); `python3 run_to_log.py /tmp/run.log -- ./cpw grid 24 96 24 12 2048 31 0.002 2 2 1 2 4 1.0 -L 16
-fast` (streamed L=16 flow); `python3 thermo_limit_study.py`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
