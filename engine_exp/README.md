# cdet-c-port; a fast C engine for the Rossi connected-determinant algorithm

A C implementation of the connected-determinant (CDet) algorithm for fermionic
perturbation theory on small Hubbard lattices, with a fast O(n L^2)
quasiseparable determinant kernel and an experimental anchor-duality module.

**Algorithm credit.** The connected-determinant recursion is from R. Rossi,
*Determinant Diagrammatic Monte Carlo Algorithm in the Thermodynamic Limit*,
Phys. Rev. Lett. **119**, 045701 (2017), arXiv:1612.05184. This package
implements that algorithm; it does not introduce a new one. It is the C
companion to the verified Python reference `cdet-python-reference`, against
whose golden values every result here is checked.

**What is original to this package (by Paul Watford).** The contributions added
on top of the Rossi algorithm are: the O(n L^2) quasiseparable determinant
kernel and its dynamic (treap-based) and parallel variants; the four
implementation techniques listed below (closed-form Green's functions,
symmetry-reduced vertex sums, kink-split integration); the `anchor_duality`
module (the c=1 compact-boson / free-fermion partition function at the two
modular anchors, the orbifold branch, the R to 2/R T-duality check, the
spin-structure sum, and the central-charge extraction with a fit-quality
estimate); the `cyclo_ratios` module (exact cyclotomic ratios at the modular
stabiliser orders, arithmetic only with no physical claim); and the scaling
benchmark in `benchmark/`. These are the parts to attribute to
this work; the underlying CDet algorithm is Rossi's.

## Quick start (run a calculation in one minute)

```
sh run_tests_unix.sh      # build + verify (194 checks).  Windows: run_tests_windows.bat
make cdet                 # build the command-line tool
./cdet                    # interactive menu: pick what to compute, answer the prompts
./cdet --help             # every option, with a one-line note on each
./cdet --version          # print the version and exit
```

One-shot examples (no menu):

```
./cdet --task order --lattice hexring --order 2 --beta 5 --mu 0.3
./cdet --task det   --n 256 --beta 20
./cdet --task green --lattice dimer --beta 5
./cdet --task anchors                 # the anchor-duality module (original)
./cdet --task stress                  # scaling benchmark (original)
```

`cdet` is the front door; the rest of the files are the library it drives. The
parameters you will usually change are `--beta` (inverse temperature), `--mu`
(chemical potential), and `--t` (hopping). `--task` chooses what to compute,
`--lattice` chooses the board. Everything has a sensible default, so `./cdet`
with no flags just works.

The numbers are verified against golden values that were originally produced by
an independent Python reference (cdet_reference/, via gen_golden.py and
gen_golden2.py), so the test suite does not grade itself. In this frozen,
self-contained drop only the resulting `golden.json` ships (and is sufficient:
`make test` reads it); the regeneration scripts and `cdet_reference/` are not
bundled — the engine is frozen, so no regeneration is needed.

The anchor-duality module and the scaling benchmark are described in
`benchmark/` and in the module's own output; they are the original physics and
performance content layered on top of the Rossi engine.

## Using the interactive menu

Run `./cdet` with no arguments and it walks you through one calculation. Every
prompt shows its default in square brackets; press Enter to accept it, or type a
value and press Enter to change it. The flow is:

1. **What to compute.** Five choices: `order` (a perturbative-order
   contribution), `det` (one fast determinant), `green` (the free propagator
   table), `dyndemo` (watch a determinant update as vertices are added and
   removed), and `anchors` (the modular anchor module, below). Default is 1.
2. **Which lattice.** `atom` (1 site), `dimer` (2), `piflux` (4-site pi-flux
   square), or `hexring` (6-site hexagon). Default is 4 (hexring). Ignored for
   the `anchors` task, which is lattice-independent.
3. **Model parameters.** `beta` (inverse temperature), `mu` (chemical
   potential), `t` (hopping amplitude), and for the `order` task, the
   perturbative order (1 or 2). Each has a default; press Enter to keep it.

The result prints at the end. Everything the menu asks can also be set on the
command line with the matching flag (`--task`, `--lattice`, `--beta`, `--mu`,
`--t`, `--order`, `--n`), so the menu and the flags are two routes to the same
calculation. `./cdet --help` lists every flag.

## Layout (modular)

```
cdet_engine.h / .c shared, lattice-agnostic engine:
 - Hubbard-atom band Green's function G0_atom
 - real-symmetric Jacobi eigensolver (2x2..6x6)
 - dense determinant (LU, partial pivot)
 - Wick determinants D_corr / D_vac
 - Rossi recursion C_V (optimal 3^n submask iteration)
lattices.h / .c per-lattice free Green's functions (the only geometry):
 atom_init / atom_G0
 dimer_init / piflux_init / hexring_init + lattice_G0
momfreq.h / .c momentum-frequency (k, i omega_n) representation of the
 free propagator: spatial FFT (periodic) + fermionic
 Matsubara comb (antiperiodic, carries the sign-flip).
 Free propagator is DIAGONAL here: 1/(i w_n - (eps_k-mu)).
qss_det.h / .c O(n L^2) quasiseparable determinant of the (time-sorted)
 vertex matrix, via the SSS boundary-state recursion.
 Verified vs dense; benchmarked (make bench).
quad.h / .c technique #4: kink-split Gauss-Legendre quadrature for
 vertex-time integrals (splits [0,beta] at coincident-
 time kinks, preserving spectral accuracy).
symmetry.h / .c technique #3: lattice translation-symmetry reduction of
 vertex site configurations (orbit reps x multiplicity).
dense_eigen.h/.cpp OPTIONAL Eigen dense LA (det/eigh/solve) behind extern "C".
 Opt-in via `make eigen`; default build needs none of it.
rankone.h / .c rank-1 incremental factorization: maintains inverse +
 running determinant under row/col INSERT/REMOVE in O(m^2).
 The "subset nesting" lever + Monte Carlo move-ratios.
qss_parallel.h / .c multi-core (OpenMP) BATCH of independent quasiseparable
 determinants + hierarchical TREE-merge of one determinant
 (qss_det_tree). `make omp`.
driver.h / .c TOP-LEVEL driver (cdet_order): composes all four techniques
 into one order-n call for a translation-invariant observable.
schur.h / .c shared Schur-merge monoid primitives (leaf/chunk/merge of the
 (logdet,W,X) interface summaries).
dyndet.h / .c DYNAMIC determinant under insert/remove/reorder in
 O(L^3 log n), exact: a treap keyed by time, each node
 augmented with its subtree's Schur summary.
bench_qss.c qss-vs-dense determinant benchmark (correctness + timing).
test_eigen.c Eigen verification + benchmark (built by `make eigen`).
test_cdet.c verification harness: recompute every golden case in C
 and check against the frozen Python value to 1e-9
golden.json frozen golden values (extracted from the Python ref) -- SHIPS HERE
             (gen_golden.py / gen_golden2.py, which originally produced it, are
             not bundled in this frozen drop; golden.json is authoritative)
Makefile build + test
run_tests_*.{sh,bat} one-click build-and-test
```

## One-click verify

- **macOS / Linux:** `sh run_tests_unix.sh` (or `make test`)
- **Windows:** double-click `run_tests_windows.bat`

Either builds the engine + lattices + harness and runs the full suite.
Expected last lines:

```
 RESULT: 59 passed, 0 failed, 0 skipped (of 59)
 ALL CASES MATCH THE PYTHON REFERENCE TO 1e-09
```

## What's verified

All against the verified Python reference, at beta=5, mu=0.3, t=1, U=1:

- **atom**: closed-form G0 (incl. antiperiodic folding & 0^- convention),
 n_F, exact interacting G, density; **CDet recursion C_V at n=0..4**.
- **dimer / π-flux / hexring**: spectral-sum G0 over the diagonalised
 single-particle kinetic matrix (incl. the π-flux gauge-protected zero
 G0(0,2)≈0); **CDet recursion C_V at n=0..2** with (site,τ) vertices.
- **closed-form path** (the same multi-site G0 and CDet cases, prefixed
 `closed.`): computed via exact Lagrange/resolvent projectors instead of
 the iterative eigensolver; see below.

100 cases total, agreement to ~1e-16-1e-17 (round-off) on every case.

## Dynamic determinant (`dyndet`, exact O(L³ log n) updates)

For Monte Carlo, where each move changes one vertex, recomputing the whole
determinant is wasteful. `dyndet` maintains it under insert / remove / reorder in
O(L³ log n) per update, exactly. The structure: the Schur-merge of chunk
summaries `(logdet, sign, W, X)` is a *monoid* (associative, with the empty-chunk
identity), so a balanced BST (treap) keyed by vertex time; each node augmented
with its subtree's merge summary; gives the determinant at the root. A BST's
in-order traversal is time order, so subtree summaries are the correctly-ordered
chunk summaries; rotations preserve in-order and re-pull only O(1) nodes. Reorder
(a vertex crossing another in time) and insert/remove are all just BST ops with
summary pull-up; one mechanism, all exact, verified vs full recompute
(`dyndet.*`). This is the exact, structure-aware version of "cache determinant
data on a grid of shapes"; a *similarity*-keyed cache (e.g. product spheres)
provably cannot work here; closeness has ~zero correlation with the determinant.

## Multi-core parallelism (`qss_parallel`, `make omp`)

The dominant CDet cost is the NUMBER of determinants (2ⁿ subset determinants, or
the many Monte Carlo configurations); not the size of any single one. These are
independent, so `qss_det_batch` runs them across cores with OpenMP. Each item
uses the verified serial `qss_det`, so results are identical to round-off
regardless of thread count (verified: 155/155 in both the serial and `make omp`
builds). Build multi-core with `make omp`; the default build stays serial.

**Single-determinant parallelism (CLOSED, `qss_det_tree`):** the hierarchical
tree-merge now works at arbitrary depth. Each chunk exposes a complete summary
`(logdet, sign, W, X)` with `W = Bl^T M^{-1} A`, `X = Bu^T M^{-1} A`; adjacent
summaries merge through an L×L correction `K = (I_L − X_R W_L)^{-1}`. The merge
is associative (verified: balanced tree == left fold == serial), so one
determinant computes as a depth-log tree of independent leaves (parallel) plus
O(L³) merges. Verified to round-off at leaf counts 1,3,4,5,12. (A single qss
sweep is already ~92 µs at n=1024, so the tree pays off mainly for very large n
or when latency on one determinant matters; for many determinants, the batch
path is still the bigger win.)

**Verified (real threads):** two independent pthread workers each computing half
of a 2000-determinant batch produce BIT-IDENTICAL results to the serial run
(max diff 0.0). The partitioning is correct; independent work, no shared state.

**Measuring speedup:** `make bench_parallel` times the batch at 1,2,4,8 threads
and prints the speedup table. Run it on multi-core hardware for the real curve.
On 1 core it correctly reports ~1.0× (nothing to overlap). NOTE: a parallel
speedup cannot be derived from a serial run by subtracting overhead and halving
; on one core the threads timeshare rather than overlap, so there is no
overlapped time to halve. The work is embarrassingly parallel (verified), so the
ceiling is near-linear in cores; the actual number is whatever the hardware's
memory bandwidth and scheduling allow, and must be measured there.

**Caveat:** multi-core *speedup* was not measured (the build/verify environment
had 1 core); only *correctness* across thread counts was verified. Expected
batch scaling is near-linear in cores (independent work, dynamic schedule).

## The four techniques (Paul Watford's original optimisations); status

1. **Closed-form Green's functions** (vs matrix-exp); [done] `lattice_G0_closed`
 (Lagrange-projector path in lattices.c).
2. **Connected-determinant recursion** (dodges cancellation); [done] the Rossi
 `C_V` recursion *is* the engine (cdet_engine.c).
3. **Lattice-symmetry reduction of vertex configs**; [done] `symmetry.c`
 (translation-orbit reps × multiplicity; verified == full sum).
4. **Kink-split integration** at slope discontinuities; [done] `quad.c`
 (piecewise Gauss-Legendre; verified vs Python).

All four are now present and verified. What is *not* yet wired is a single
top-level "perturbative coefficient" driver that composes #3 + #4 + the engine
into one call per order; the verified pieces are all here to assemble it.

## Large-matrix strategy (linear algebra)

The plan targets very large matrices, so the linear-algebra choices matter:

- **The determinant that grows with the problem is the vertex matrix**, and the
 win there is the **qss O(n·L²)** path (`qss_det`), not a faster dense solver.
 At n=1024 it is ~2700× faster than dense O(n³) and matches to round-off.
 This is the primary large-matrix lever and it is built.
- **The dense `det_lu`** is now heap-based (handles arbitrary n; the old 8×8
 cap is fixed). It is a plain O(n³) LU; fine as the fallback / cross-check.
- **If a tuned dense solver is needed** (large dense blocks that are *not*
 quasiseparable), the optional **Eigen** path is now included
 (`dense_eigen.cpp/.h`, MPL2, header-only). It exposes `eigen_det`,
 `eigen_eigh`, `eigen_solve` behind a plain-C `extern "C"` interface, verified
 against the engine's `det_lu`/`jacobi_eigh` to round-off and ~2-3× faster than
 plain LU on large dense matrices (2.96× at n=1024). It is **opt-in**: the
 default `make`/`make test` stays pure C and dependency-free; build the Eigen
 path with `make eigen` (needs Eigen headers; `apt install libeigen3-dev`,
 `brew install eigen`, `vcpkg install eigen3`, or vendor them and set
 `EIGEN_INC`). Compiled with `EIGEN_MPL2_ONLY` so only MPL2/BSD code is
 included; MPL2 is compile-time-only with no redistribution obligation for
 your own sources. For the tiny Wick matrices the inlined `det_lu` is still
 preferable; Eigen is for the large dense path only.

**Wired into the recursion (v2.2-v2.3):** `cv_samesite_qss` computes the
same-site connected correlator with qss for the square vertex determinants,
verified end-to-end against the reference C_V to round-off (`samesite.CV.*`).

**Performance (corrected, measured; `make bench_scaling`):** the determinant
that grows with perturbation order is size n, and qss vs dense on it crosses
over at **n ≈ 18** (L=6): qss is 1.4× at n=20, 3.1× at n=32, 5.3× at n=40, and
the margin keeps growing.

**Caching (v2.4):** the same-site path precomputes the propagator table and qss
generators ONCE (O(n²L)) instead of recomputing `ss_g0` per matrix entry per
subset. End-to-end the same-site C_V now beats the dense engine even at low
order; 1.6× at n=3, 11× at n=6, 22× at n=10; purely from removing redundant
exp/cos work; the qss crossover (n>18) stacks on top.

### Closing the gap to Eigen; the honest levers

A matrix is only "generic" if you don't expose its structure. **Measured:** the
different-site CDet vertex matrix has off-diagonal blocks of rank exactly L (=6),
not full rank; it is quasiseparable just like the same-site case. So it gets
the O(n·L²) path too, via **complex generators** (`qss_build_ring_c`,
`qss_det_c`): different sites add phase factors e^{i2πk(i−j)/L}, the recursion is
identical over ℂ, and the determinant is real. Verified to round-off vs dense
(`qssc.detM.*`); benchmark crossover ~n=32, then 3.8× at n=64, 52× at n=256,
215× at n=512. We beat Eigen ~900× (same-site) / ~200× (different-site) on these
because qss exploits the rank-L structure Eigen can't see. Truly random matrices
*are* full-rank; those still go to Eigen (the optional `make eigen` path).

**Head-to-head (`make bench_eigen`, vs Eigen 3.4.0, every result agreeing to
round-off):** same-site qss ≈7× faster at n=64, ≈79× at n=256, ≈270× at n=512,
≈907× at n=1024; different-site (complex) qss crosses over ~n=32, then ≈2.3× at
n=64, ≈21× at n=256, ≈78× at n=512. On a *truly generic* random dense matrix qss
does not apply; at the default `-O2` Eigen beats our det_lu ≈1.8-2.8×, but that's
a build-flag artifact; `make fast` (`-O3 -march=native`) auto-vectorises det_lu's
SAXPY inner loop onto AVX2/FMA and reaches parity (≈0.6-1.0× up to n=256, Eigen
ahead only at n≥512 via cache-blocking). We don't hand-write SIMD/blocked LU to
chase Eigen there; that's reimplementing Eigen worse for a regime CDet never
visits; so genuinely-dense blocks delegate to Eigen (`make eigen`).

Other levers (all done):
- **(a) Avoid redundant work around the linear algebra**; caching (done).
- **(b) Exploit subset nesting**; DONE (`rankone.c`). Adding/removing a vertex
 is a rank-1 border update/downdate of the inverse + determinant in O(m²)
 instead of refactoring in O(m³). Verified vs from-scratch and the Python
 reference; benchmarked 1.9× (n=8) -> 12× (n=128) for incremental builds. This
 is also the standard Monte Carlo CDet insert/remove move-ratio
 (`r1_insert_ratio` / `r1_remove_ratio`). Eigen cannot do this; it does not
 know the matrices are nested.
- **(c) Vectorise our own kernels**; DONE (`make fast`: opt-in -O3
 -march=native -funroll-loops, ~1.2× on the qss kernel; non-portable, compile
 on the target machine). Default build stays portable -O2.
- **What we do NOT do:** try to out-engineer Eigen's dense LU on generic
 matrices. That kernel is many person-years of tuning; we delegate to Eigen
 there (already wired via `make eigen`). The gap that matters is end-to-end,
 and it closes by routing each matrix to the right tool, not by competing on
 the leg where Eigen is simply better.

## Quasiseparable determinant; O(n·L²) (`qss_det`)

The free-propagator vertex matrix, with vertices **sorted by imaginary time**,
is **quasiseparable of rank L** (L = number of bands): each entry is
`e^{−ξ_k(τ_a−τ_b)} = z_a/z_b`, a ratio, so each triangle is generated by rank-L
generators. Its determinant; which a CDet run computes enormous numbers of; 
can be taken in **O(n·L²)** instead of the dense **O(n³)**, via a sequentially-
semiseparable forward recursion that carries an L×L "boundary state" `W` across
the vertices:

```
pivot_i = A_i · (Bu_i − W·Bu_i)
W += outer(Bl_i − W·Bu_i , A_i − Wᵀ·A_i ) / pivot_i
det = ∏ pivot_i
```

with generators (same-site ring block, real):
`A[a,k]=L^{−1/2} e^{−ξ_k τ_a}`, `Bu[b,k]=L^{−1/2} e^{ξ_k τ_b} n_F^k`,
`Bl[b,k]=L^{−1/2} e^{ξ_k τ_b}(−(1−n_F^k))`.

The recursion was **derived from the block-inverse bordering identity** (not
fitted) and verified pivot-by-pivot against dense LU. The `qss.detM.*` golden
cases check the C implementation against the Python determinant to round-off.

**Benchmark** (`make bench`, C, same build, ring L=6); qss vs dense det, with
correctness re-checked at every n:

```
 n qss(us) dense(us) speedup |qss−dense|
 8 0.7 0.2 0.30x ~1e-17
 32 3.0 9.3 3.16x 0
 64 6.0 72.2 12.13x ~2e-17
 128 11.6 562.7 48.36x ~3e-17
 256 23.0 3869.8 168.62x ~3e-17
 512 45.9 30758.5 670.12x ~2e-16
 1024 90.7 244366.2 2694.22x ~2e-16
```

Crossover at n≈32; beyond it the O(n³)/O(n·L²) gap grows without bound (2694×
at n=1024), while agreement stays at round-off. qss time grows linearly in n;
dense grows cubically.

**Scope (honest).** Implemented for the **same-site ring block** (real
generators). Different-site blocks extend with complex generators (rank still
L); not implemented here. The recursion needs vertices sorted in time and the
free propagator's ratio structure; it computes the determinant of one vertex
matrix, which is the inner-loop primitive of the CDet recursion. Wiring it into
the full `C_V` recursion (replacing the dense `det_lu` calls for same-site
blocks) is the natural next step; the verified primitive is here.

## Momentum-frequency representation (`momfreq`)

The free propagator on a translation-invariant lattice diagonalises completely
in **momentum-frequency space** `(k, iω_n)`:

```
G0(k, iω_n) = 1 / (iω_n − (ε_k − μ)), ε_k = −2t cos(2πk/L),
 ω_n = (2n+1)π/β (fermionic Matsubara)
```

This realises the geometric picture exactly:

- **space is periodic** -> the lattice Fourier transform (FFT) sends it to
 momenta `k`; arrows that differ only by location collapse into one `k`-layer.
- **time is *anti*periodic** (`G(τ+β) = −G(τ)`) -> the **fermionic Matsubara
 comb** `ω_n = (2n+1)π/β` diagonalises it. Those odd-half-period waves carry
 the sign-flip *automatically*; there is no manual "if τ>β multiply by −1";
 the flip falls out of the basis. (Verified: `momfreq.flip.*` golden cases.)

In this basis the free propagator and the translation-invariant
(disconnected/vacuum) pieces are **diagonal**; one closed-form number per
`(k, iω_n)` layer, no matrix and no eigensolver. The `L`-site spatial problem
becomes `L` decoupled single-mode frequency problems. Run `demo_momfreq`.

`momfreq_G0_site(c, i, j, τ)` reconstructs the imaginary-time site propagator
from the diagonal data (inverse Matsubara sum with analytic `1/(iω_n)` tail
subtraction for full-precision convergence on the equal-time diagonal, then
inverse spatial FFT). Verified against the golden Python reference to ~1e-13.

**Scope (honest, and load-bearing).** This diagonalises the **free** propagator
and the translation-invariant pieces. It does **not** collapse the full CDet
determinant to a product, because the interaction vertices pin specific
`(site, τ)` points and break the clean translation symmetry; the
vertex-vertex matrix is *not* circulant (tested). So momentum-frequency is the
right representation for the free building blocks and the disconnected/vacuum
subtractions; the connected, vertex-pinned determinant still needs the
position-space recursion. The genuine speedup is the **spatial decoupling**
(`L`-site problem -> `L` independent `k`-sectors), not a whole-determinant FFT
shortcut. Treating the whole determinant as FFT-diagonalisable would give
clean-looking *wrong* numbers; this module deliberately does not do that.

## The two Green's-function paths (CDNet technique #1)

The multi-site lattices offer two ways to build G0, both verified:

- **`lattice_G0`**; numerical path: a Jacobi eigensolver diagonalises the
 kinetic matrix, then the spectral sum runs over eigenvectors. Matches numpy
 (which also diagonalises numerically) to round-off.
- **`lattice_G0_closed`**; closed-form path: uses the *exact* distinct
 eigenvalues (dimer ±t, π-flux ±√2 t, hexring −2t·cos(2πk/6)) and forms the
 **Lagrange/resolvent projectors** P_e = ∏_{e'≠e}(H−e'I)/(e−e') directly.
 No iteration, no eigenvectors, degeneracy handled automatically.

This is the C analogue of the CDNet design choice; closed forms over
numerical diagonalisation. It can't beat double-precision round-off on generic
values (nothing can), but where the physics has **exact structure** it
recovers it exactly: the π-flux gauge-protected zero G0(0,2) comes out as
`0.000000000000e+00` on the closed-form path, vs `-5.6e-17` on the Jacobi
path. Use `lattice_G0_closed` as the production G0; `lattice_G0` is kept as a
cross-check and a fallback for lattices whose exact spectrum you haven't
supplied.

**On the 1e-16 residuals:** these are IEEE-754 double-precision round-off
(machine epsilon ≈ 2.2e-16), identical in the numpy reference. They are the
floor of the `double` type, not a missing optimisation; no algorithm removes
them in double precision. If you ever need below that, the move is `long
double` or a bignum library, not a smarter method; for CDet at these orders it
is unnecessary (the references themselves are double).

## The anchor-duality task (`./cdet --task anchors`)

`./cdet --task anchors` runs the modular module and prints, in order:

- **The two anchors.** tau_1 = i (order 2, fixed by S: tau -> -1/tau) and
  tau_0 = e^(2 pi i / 3) (order 3, fixed by ST: tau -> -1/(tau+1)), with the
  fixed-point checks shown.
- **The compact-boson partition function** on the c = 1 line at the radius set
  by `--radius` (default sqrt(2), the self-dual point), and its modular
  S-invariance check across several tau (zero to round-off).
- **The free-fermion partition function** as the spin-structure sum, with the
  single sectors shown to be non-invariant while the sum is invariant.
- **The lattice reach** table: which finite rings are gapless (reach the
  critical line) and which are gapped, by their S-ratio and gap.
- **The central charge** from Cardy finite-size scaling, c near 1 for the
  gapless ring and near 0 for a gapped chain.

The newer outputs in this version add:

- **The tau_0 orbit.** Z at tau_0, ST(tau_0), ST(ST(tau_0)); since ST fixes
  tau_0 the three coincide to round-off (the order-3 companion to S fixing
  tau_1).
- **T-duality.** A table checking Z(tau, R) = Z(tau, 2/R) at several radii;
  zero to round-off, the symmetry the c = 1 line is built on.
- **Central charge with fit quality.** The same c, now reported with its RMS
  fit residual and the standard error from the fit covariance, so the value
  carries a stated precision. The small offset of the gapless c from exactly 1
  is the finite-size correction, not fit noise.
- **The orbifold branch.** The Ginsparg Z2-orbifold partition function, shown
  to be modular-S-invariant and R -> 2/R dual to round-off; the orbifold branch
  of the c = 1 line alongside the circle branch.
- **Cyclotomic ratios.** A short block of exact rational numbers built from the
  cyclotomic polynomials at the modular stabiliser orders, printed as reduced
  fractions. This is arithmetic only; no physical claim is made in the code.

Use `--radius R` to evaluate the partition functions at a different point on the
c = 1 line; the anchors and their symmetries do not depend on it. The task
ignores `--lattice` and the model parameters.

## Using the engine in your own code

The engine is geometry-agnostic. To compute a connected correlator:

```c
#include "cdet_engine.h"
#include "lattices.h"

LatticeCtx c;
hexring_init(&c, /*beta*/5.0, /*mu*/0.3, /*t*/1.0);

Vertex V[2] = { {0, 0.5}, {1, 1.4} }; /* (site, tau) vertices */
double Cn2 = C_V(V, 2, /*site_out*/0, /*tau_out*/1.5,
 /*site_in*/0, /*tau_in*/0.5,
 lattice_G0_closed, &c); /* closed-form G0 (preferred) */
```

`lattice_G0_closed` is the preferred G0 for dimer/π-flux/hexring (exact
projectors); `lattice_G0` is the numerical cross-check; use `atom_G0` for the
atom. To add a new lattice, write an `xxx_init` that fills `LatticeCtx` (build
the kinetic matrix, call `jacobi_eigh`, and; for the closed-form path; 
`build_closed_form` with the exact distinct eigenvalues) and reuse the shared
G0 callbacks. Nothing in the engine changes.

## Scope (honest)

This ports the **production CDet path**: closed-form/spectral Green's
functions, Wick determinants, and the recursion; the part your CDNet work
optimised and the part a production run actually executes. It does **not**
port the Python package's *reference scaffolding*: the 4096-dim sparse exact
diagonalisation, the sympy symbolic Taylor reference, the mpmath dps=50
checks, or the quadrature/spectral-function plotting. Those exist to *verify*
the engine in Python; here, that verification role is played by `golden.json`
(values they produced) checked by `test_cdet.c`. If you extend the engine,
regenerate/extend the goldens from the Python reference (`cdet_port.py` in
08_2d_interacting reproduces the same values to 1e-9; the original `gen_golden*.py`
are not bundled in this frozen drop) and the C suite will hold new code to the
same standard.

The Jacobi eigensolver reproduces `numpy.linalg.eigh` for these small
matrices to round-off; eigenvector sign/degeneracy freedom is irrelevant
because the Green's function is a spectral *sum* invariant to it (verified:
all G0 cases match to ~1e-16, including the degenerate ±t hexring levels).
