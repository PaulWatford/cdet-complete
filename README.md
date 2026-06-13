# CDet / connected-determinant suite

> New here? `INDEX.md` is the map of the whole package; `QUICKSTART.md` builds and verifies in minutes.

A numerically-exact connected-determinant (CDet) toolkit for the fermionic Hubbard / SU(N) problem, built around a
frozen 194/194 reference engine with a fast hybrid production path and an arithmetic surrogate.

### Try this first

```
cd engine && make CC=gcc test     # 194/194 -> the engine is correct
cd .. && ./cdet validate          # 5/5 gates, the full dashboard
./cdet converge                   # the thermodynamic-limit table, to 100x100, instantly
./cdet gui                        # browser front-end: sliders fill in the flags, runs the real commands
```

Everything is driven from the top-level `./cdet` command (`./cdet --help` for the full list). The numbered folders
(`01_…`–`08_…`) hold the staged source and raw C oracles behind that CLI — you don't need to open them to use the tool;
start from `./cdet` and reach for them only if you want the internals.

## Quickstart

Install as a package (editable) to get the `cdet` command on your PATH:

```
pip install -e ".[all]"     # all = rich (pretty output) + matplotlib (figures)
cdet validate               # 194/194 frozen + surrogate + hybrid parity + 2D path
```

On a modern Debian/Ubuntu you may see an "externally-managed-environment" (PEP 668) error. Either use a virtual
environment (`python3 -m venv .venv && . .venv/bin/activate && pip install -e ".[all]"`) or, to install into the user
environment, add `--break-system-packages`. If you would rather not install at all, every command also works as
`python3 cdet.py <subcommand>` (or `./cdet <subcommand>`) straight from this folder.

Or run without installing (pure standard library; `rich`/`matplotlib` optional):

```
python3 cdet.py validate      # run all validation gates (frozen 194/194, surrogate, hybrid parity, 2D path)
python3 cdet.py converge      # 2D thermodynamic-limit demo: 4x4 -> 100x100 (the 12x12 case is already representative)
python3 cdet.py resum         # conformal-Borel resummation vs Pade on the SU(N) EoS (the order axis)
python3 cdet.py run --L 6 --beta 30 40    # hybrid grid run (the production CDet path)
python3 cdet.py info          # architecture and capabilities
```

Or use the launcher: `./cdet validate`.  Optional pretty output: `pip install rich`.

CI runs the frozen 194/194 gate and `cdet validate` on every push (.github/workflows/ci.yml). **Dual-licensed:** free for
academic/noncommercial use (PolyForm Noncommercial 1.0.0); commercial use requires a license (see COMMERCIAL-LICENSE.md).

**Docker (one-command deployment):**

```
docker build -t cdet-suite .
docker run --rm cdet-suite                 # runs `cdet validate` (all gates) by default
docker run --rm cdet-suite converge        # any subcommand
```

The image bakes in the 194/194 frozen-engine gate at build time (it won't build if validation fails).

**Optional native bindings** (eliminate subprocess overhead for programmatic use):

```
pip install -e ".[bindings]" && python bindings/build.py
python -c "import sys; sys.path.insert(0,'bindings'); import cdet_core; print(cdet_core.G0_atom(0.3,5,0))"
```

These call the frozen reference engine's C primitives directly (bit-identical to the 194/194 engine, ~10^6x faster
than the compile+subprocess path).

Subcommands: `validate`, `converge`, `resum`, `eos`, `docc`, `chi`, `run`, `sweep`, `plot`, `export`, `gui`, `bench`, `diagmc`, `lab`, `shell`, `info`, and the wall-physics suite `wall`, `tide`, `primes`, `twist`, `trueradius`, `crosscheck`.

### Wall physics: where lattice size meets the order axis (v172–176)

The bare-U series has a finite radius of convergence — the "wall." Its leading weak-coupling cause is the RPA/Stoner
instability `U_c(L) = 1/max_q chi0(q,L)`, with `chi0` the free static (Lindhard) susceptibility built from the
plane-wave dispersion. Because `chi0` needs only the O(L) dispersion, the wall is computable at any lattice size to
100×100. The suite explores how the wall behaves with lattice size; all modules share one canonical core
(`wall_vs_size.chi0_max_rect`).

```
cdet wall      # the wall vs lattice size: near half-filling the large lattice reveals a further-out wall (lattice helps)
cdet tide      # the wall oscillates with L; period = 2*pi/q* measures the Fermi nesting vector
cdet primes    # prime lattice sizes are the worst samplers (a Diophantine commensuration sieve)
cdet twist     # "half-integer" lattices: twisted BC don't heal the sieve; rectangular supercells do
cdet trueradius  # the TRUE complex-U radius: a thermal Fisher pair (Im~pi/beta), closer than the RPA wall, sieve-free
cdet crosscheck  # all models side by side + the cross-links between them
```

Finding: the tide and sieve are finite-size q-sampling artifacts of the grid relative to the nesting vector q*, not
properties of the true thermodynamic-limit wall.

### Diagrammatic Monte Carlo: the sign wall, measured (`diagmc`)

`cdet diagmc` is a Rossi-style connected-determinant Monte Carlo sampler. It samples the diagrammatic series with the
connected determinant as the weight (the same validated kernel as `connected`), reproduces the exact answer on solvable
systems within error bars, and **measures** the fermionic sign problem in the form it takes here: the across-order average
sign `<s> = |sum a_n U^n| / sum |a_n| U^n` collapses toward zero as `U` approaches the convergence radius, with cost to a
fixed error scaling as `1/<s>^2`.

```
cdet diagmc --system atom --U 1.5     # MC coefficients + ln(Z/Z0) vs exact, and the sign-wall scan
```

Honest scope: it does **not** defeat the sign problem -- that wall is Troyer-Wiese / NP-hard -- it exhibits it. The
reachable order is bounded by the `2^n` connected-determinant cost, and validation is on the small exactly-solvable
systems (atom, 2-site); a large-lattice, high-order production sampler remains future work.


(`cdet <subcommand> --help` for options).

---

# cdet — complete archive

The connected-determinant engine, its 2^n wall, and the complete set of attacks on
that wall — every one measured, the negatives kept as honestly as the wins. This
is a self-contained record: the extended engine source builds and passes its 194
verification checks, and each result folder carries its code plus a writeup with
explicit epistemic labels.

## What cdet is
A Hubbard-lattice connected-determinant solver (Rossi-style). At perturbative
order n it evaluates the connected determinant as a sum over all 2^n subsets of
the n interaction vertices. The recursion is exact; the cost and memory are the
2^n.

## The live record (where the current frontier is)
The running ledger is `real_patterns_v192.md` (top level): every banked result #1..#156 with its
epistemic label, the frozen predictions, and the open queue. Earlier frontiers (the deep-beta coefficient
program, the million-site projector scaling, the thermodynamic-limit z-flow) are banked; the **current
frontier** is the integration program prompted by Gunnar Möller's three papers (Kozik 2024 CoS;
Šimkovic-Kozik 2019 self-energy; Frankenbach 2025 QTT), in `08_2d_interacting/`:
- **#1 fast minors** (`fast_minors.py`) -- the connected determinant in O(2^n n^2) via one Schur-complement
  recursion + subset convolution (`cos_prototype.py`), verified term-by-term against the engine. A supplement;
  wiring it into the hot loop is a separate val-gated stage.
- **The physical mapping** (`physical_mapping.py`) -- z(inf) is a real spectral observable: the free
  single-particle ADDITION POLE (lowest-empty level), via the v78 fugacity lemma. It tracks the moving pole.
- **#3 self-energy** (`self_energy*.py`) -- the interacting upgrade of z: the interacting addition energy is
  eps + ReSigma, ED-verified; the diagrammatic Sigma converges within its radius; exact 1PI coefficients via
  the Dyson recursion. (v136's "1PI series has a larger radius" claim was RETRACTED in v137: R_Sigma ~ R_G;
  the Simkovic-Kozik advantage is efficiency + MC variance, and strong coupling needs resummation.)
Each round has a `07_predict_vs_compute/CROSSCHECK_v*.md`. The C surrogate (`08_2d_interacting/csurrogate.*`)
carries the banked scopes (incl. z(inf)=lowest-empty); the frozen engine (`engine/`, 194/194) is the exact
ground truth underneath all of it. `consolidation_v138.py` runs the three paths side by side as one health gate.

**THREE-MODEL ARCHITECTURE (v147 consolidation).** (1) The FROZEN REFERENCE `engine/` (194/194, never altered)
is the validation anchor; efficiency via `make fast`/`make omp`. (2) The PRODUCTION ENGINE
`08_2d_interacting/cdet_planewave_engine.c` (the hybrid) carries every capability -- any-L, `-fast` projector
path, `-DUSE_LD` deep precision, mode-2 continuous freeze, 3 input guards, multi-million sites -- and validates
== the frozen reference bit-for-bit at L=6. (3) The SURROGATE `csurrogate.c` carries the fast arithmetic
observables (addition pole, Friedel edge, interacting pole, and the SU(N) EoS coefficients sun_c1/sun_n1). The
analysis supplements (fast_minors, self_energy*, physical_mapping, sun_*, resummation, rational_*) stay as
separate CLI modules -- research instruments with their own options. `consolidation_v147.py` is the health gate.

**UNIFIED ENTRY POINT (v148).** `08_2d_interacting/cdet_lab.py` is the single front door: a control plane that
exposes every capability as swappable components from the terminal, without touching the frozen reference. Pick an
observable and a solver: `python3 cdet_lab.py --target eos --method record --N 6 --U 1.0 --mu 1.0`. Run
`python3 cdet_lab.py list` for the full (target x method) map and `python3 cdet_lab.py validate` for the health
gate. Targets: eos, self-energy, addition-pole, double-occ, connected-det. Methods: ed, record, hubbard-i,
diagrammatic, surrogate, hybrid, fast-minors, engine.

**FRIENDLY ENTRY POINT (v149).** New users should start with `08_2d_interacting/cdet_shell.py` -- a conversational
shell over the control plane: describe what you want in plain language ("self-energy in the Mott regime, U=4 mu=2
beta=5"); it states back what it understood, shows the exact command, and runs it only after you confirm yes/no.
Saying 'no' reverts without losing your named/saved configurations. `python3 cdet_shell.py` (then `help`).

**SWEEPS / STRESS TESTS (v151).** `08_2d_interacting/cdet_study.py` scans a parameter for any (target, method),
detects convergence or accuracy breakdown, and stops on user cutoffs -- `--max-time` (wall-clock budget) or
`--accuracy-cutoff` (error vs reference). It writes a log, `data.csv`, `summary.json`, and a `plot.png` (plus a
headless ASCII plot) with the convergence/breakdown points marked. Drivable in plain language from the shell:
"sweep U from 0.2 to 1.2 for self-energy diagrammatic, stop if accuracy drops below 5e-3".

## The wall
Each evaluation needs arrays of size 2^n indexed by vertex subsets. In RAM this
caps the reachable order (~n=28 at a few GB). The whole archive is about whether
that 2^n can be reduced, moved, or evaded.

## The complete map of the wall (the honest bottom line)
The wall has TWO independent axes, and they have DIFFERENT answers.

  ORDER axis (the 2^n in perturbative order)  —  IRREDUCIBLE per evaluation.
    Measured dead, every way tried:
      - low-rank / SVD of the subset array        -> full rank (127/128 on hexring)
      - tensor-train / MPS code over subset bits  -> full rank at every cut (100%)
      - lossless compression of the stored array  -> ~1.5x (xz), shuffle worse
      - generating polynomial / NN from geometry  -> 96% error (no fit)
      - sufficient statistic / "modular form"      -> full rank = no shorter description
    The 2^n is a count of independent degrees of freedom the exact answer depends
    on; no lossless reformulation reduces a count. What DOES bend is the NUMBER of
    expensive evaluations (not the per-call 2^n): see 01 and 02.

  SIZE axis (total lattice sites L)  —  DEMOLISHED by locality.
    Connected diagrams are spatially local: far vertices decouple exponentially
    (proven on the engine, 1D and 2D). Cost becomes independent of system size
    beyond a correlation length — the thermodynamic limit at correlation-volume
    cost. See 04 and 05.

  SIGN axis (per-configuration cancellation, the ~1/R^2 cost)  —  the real wall.
    The verified accelerations move the axes AROUND it, not it: shifted reference
    (convergence), complex-mu contour (derivatives), control variate (prefactor).
    None changes R. Contour deformation / thimbles do not bite either — our sign
    is a real sign-flip, not a complex phase (v49). The wall is Troyer-Wiese / NP-
    hard. The honest, composable recipe and its scope: 08_2d_interacting/
    BEST_METHODS.md (run best_methods.py — all PASS).

  SITE-SUM redundancy (the L^n site-assignment factor)  —  EXACT symmetry fold.
    Lattice automorphisms that fix the external site fold the site sum by the
    stabilizer order |G_0| — the little group of the external. It GROWS with
    lattice symmetry, size, AND dimension: 2x (2x2 square) -> 8x (4x4 square,
    D4, incl. column/row-slice reflections) -> 48x (4x4x4 cube, O_h, incl. the
    45-degree diagonal slices). Exact to machine precision, proven for all
    hopping t via sympy. Column/row/diagonal slices FOLD (+1), never CANCEL (−1);
    it does NOT touch the sign (orbit members share it) or the Rossi 2^n. See
    08_2d_interacting/SYMMETRY_REDUCTION_RESULT.md (symmetry_reduction.py +
    symmetry_audit_sympy.py). The interior of the per-evaluation 2^n: a mask-
    level fold exists but only on symmetric configs (measure-zero generically);
    the generic win is the SUBSET CACHE (D_vac/D_corr keyed on the vertex set,
    memoized across the sum), composing with the orbit fold to 29.9x fewer
    determinant evaluations at n=3 on the 4x4, exact to 5e-15 (cv_cached /
    fold_site_sum_cached). The -1 hunt is closed: it lives in the particle-hole
    VALUE channel but is dressed by the exact equal-time sum rule into an inter-
    observable identity with density counterterms -- no per-config -1 at fixed
    mu. Weight and sign concentrate on low-dimensional slices (x18.5 lines /
    x2.1 planes / x0.65 bulk; R 0.22/0.09/0.004) -- see 08_2d_interacting/
    VALUE_CHANNEL_SLICES_RESULT.md (value_channel_slices.py). The hierarchy is
    now an estimator: slice-STRATIFIED evaluation (enumerate heavy low-dim
    strata, Neyman-sample the bulk) -- unbiased, 22-44x variance cut at n=2 vs
    exact truth, 2.1x at n=3 where the heavy stratum exceeds the budget. See
    08_2d_interacting/SLICE_STRATIFIED_RESULT.md (slice_stratified.py). The
    v48 arc is CLOSED: the sign-vs-convergence trade-off is generic in the
    doped regime; the one exact alignment is half filling at low T, forced by
    particle-hole symmetry (GENERICITY_RESULT.md, genericity_search.py). Under
    larger-cluster + second-U testing (v64) the law SPLIT: the PH convergence-
    lock alpha*=U/2 is universal and quasi-exact (6-ring err 8.6e-6 via blocked
    sector ED, validated 4.8e-07), but sign alignment is cluster-dependent --
    it fails on the 6-ring, whose sign peak is not at the PH point
    (GENERICITY_CLUSTER_RESULT.md, genericity_cluster.py). CONSOLIDATED
    BASELINE (v65): 08_2d_interacting/cdet_best.py is the front door -- BestCDet
    + fold x cache (exact) + stratification + the split shift law + the
    concentration-law constants; BEST_METHODS.md (v65 edition) is the map of
    everything verified, the two laws, and the standing methodology. The NO-
    BRUTE-FORCE SIMULATOR (v66, surrogate.py): a geometry surrogate (OOS R2
    0.75) reproduces brute-force weight structure with zero evaluations and
    accelerates signed totals 33x where the sign is mild; its measured ceiling
    -- no gain on cancellation-dominated totals -- is the sign wall in
    estimator form (SURROGATE_RESULT.md). THE SIGN MODEL (v67, sign_model.py)
    then moved that ceiling: sign survival is bootstrap-real (1d 0.70 vs bulk
    0.34, CIs separate), the line sector's sign is 92% predictable and carries
    77% of the exact signed answer at 0.3% of configs, and the hybrid
    estimator reaches 87-110x over uniform, unbiased (SIGN_MODEL_RESULT.md).
    The bulk remainder stays a coin flip -- the wall's remaining territory.
    GOVERNANCE (v68, sign_governance.py): signed weight = magnitude envelope x
    coherence decay (xi_s ~ 3, sign outlives weight) x a mu-controlled
    orientation PHASE (Friedel-class; parity falsified; 94% negative at mu=0.5
    flips to 75-100% positive at mu=1.5). Coherence, not positivity, is the
    invariant (SIGN_GOVERNANCE_RESULT.md). Open: the quantitative phase law -- ATTEMPTED in v69 (phase_law.py): static
    Friedel and dominant-chain reductions both falsified under frozen protocol
    (34% / 64-66% vs a pre-set 75% gate); the phase is determinant-level
    interference as far as tested. Magnitude lawful, phase irreducible: the
    hardness, localized (PHASE_LAW_RESULT.md). SECTOR ESTIMATOR (v70,
    sector_estimator.py): the coherent sector is polynomially small by
    construction (3,774 of 10M at L=6) and exactly enumerable at any L; exact-
    moment design analysis became a standing rule and CORRECTED v67's gain to
    ~6x (the 87-110x was a lucky-baseline artifact, structural facts
    untouched); the L=6 exact sector sum is negative -- the v68 phase flip in
    exact arithmetic (SECTOR_ESTIMATOR_RESULT.md). PAIRING DEPTH (v71,
    pairing_depth.py): the phase has NO finite depth -- the complete single
    free determinant fails (44% OOC); by elimination the phase lives in the
    coupled two-spin integrand itself. The reduction ladder is complete; any
    surrogate orientation channel must be learned, not derived
    (PAIRING_DEPTH_RESULT.md). BULK REMAINDER (v72, bulk_remainder.py): not
    incoherent -- mu-controlled FRIEDEL RINGS in MST (alternating-sign shells,
    mid-range dominance, mu-shifting pattern confirmed by frozen test); the
    monotone-decay surrogate model was falsified by its own gates -- the
    falsification is the discovery (BULK_REMAINDER_RESULT.md). The rotation
    closed with all three passes converged on the orientation phase. The
    LEARNED channel (v73, learned_orientation.py) then failed the same frozen
    gate (33-35% held-out): a phase WRAPS and smooth models cannot interpolate
    a wrap -- the orientation channel is closed from both directions; what
    remains for the surrogate is magnitude-side
    (LEARNED_ORIENTATION_RESULT.md). SURROGATE v2 (v74, surrogate2.py):
    ceilings measured first (the old r_pred 0.32 was ~80% of its label-noise
    ceiling); v66's R2=0.75 scope-corrected as mixture-flattered (median error
    1.7x stands); the gain is TRANSFER -- L=4->L=6 R2 0.57, med-err 1.81x with
    10 linear features and an 8-shot intercept; r_pred regime map
    +0.32/+0.27/-0.57 by rank: predictability coextensive with coherence
    (SURROGATE2_RESULT.md). THE L=6 SHELL FOLD (v75, shell_fold.py): wrap-
    collinearity corrected (true sectors 1,618/82% at L=4, 16,950 at L=6 --
    wrap-safe definitions now standing); FIRST EXACT 10M-config totals
    (mu=0.5 -2.498e-3 validating the v70 pilot; mu=1.5 -2.225e-3); the
    sector's share falls 82% -> 42% with size and opposes the total at
    mu=1.5; rings persist, mu-dependent nodes, period unresolved
    (SHELL_FOLD_RESULT.md). RING PERIOD (v76, ring_period.py): not resolved
    at L=6 and unresolvable there in principle (xi_s/period ~ 2.5); the
    binned R_max near-miss (within 10% of 2kF, correct mu-shift) was killed
    by permutation null (p = 0.20/0.16); contact-shell coherence is real and
    mu-flipped (+0.66/-0.53); route = larger L + coherence-boosted
    observables (RING_PERIOD_RESULT.md). THE MU-PERIOD LAW (v77,
    mu_period.py): Delta-mu* = pi/(q beta), q -> 1 -- charge-1 fugacity
    winding, R- and L-independent; Friedel falsified for the mu-dependence;
    the orientation channel half-reopens (73-76% at the 75% bar; offset
    calibration is the residual); new theory target: derive q=1
    (MU_PERIOD_RESULT.md). THE COMB (v78, fugacity_structure.py): the
    mu-period's analytic origin established -- <C>_tau is exactly rational in
    the fugacity (cancellation lemma), poles on Matsubara combs at height
    pi/beta, detected directly by complex-mu continuation (3.9e6-fold
    at-level divergence); the charge-staircase reading falsified; comb-
    limited variation derives 1/beta scaling and R/L-independence
    (FUGACITY_STRUCTURE_RESULT.md). CONSOLIDATED SURROGATE (v79,
    cdet_surrogate.py): one integration layer -- wrap-safe sector,
    transferable magnitude (pooled 1.88x across draws; per-class intercepts
    tested and rejected), regime map, period-based orientation channel --
    with BEST_METHODS v79 edition closing the phase program's arc.
    THE RESONANCE REGIME (v80, resonance_regime.py, KT-review round): the
    beta>=12 boundary retracted -- two-regime law proved (level-attracted,
    geometry-independent flips at large beta, p = 0.013-0.041); naive
    midpoint law killed; core set external-time-independent; transfer
    bimodal via multiplicities (RESONANCE_REGIME_RESULT.md). THE PAIR LAW
    (v81, pair_law.py): the limit set IS the spectrum -- flips converge to
    the levels two-sidedly as eps +/- c/beta (best rms 0.004); candidate
    c = ln(deg)/2 (ln 6 = 1.792, 0.4% on the cleanest fit); no-free-parameter
    prediction banked for any (L, level) (PAIR_LAW_RESULT.md). THE TWO-CLASS
    STRUCTURE (v82, level2_structure.py): the fired prediction FAILED at L=8
    level 2 (deg corrected 63 -> 39; ln(deg)/2 demoted to a one-level fit) --
    exposing beta-STATIC Class-II crossings at specific level-pair midpoints
    (1.828 flat over beta 12-24; 2.121; 2.293); the midpoint law resurrects
    selectively; selection rules open (LEVEL2_STRUCTURE_RESULT.md). THE
    RESIDUE RATIO (v83, residue_ratio.py): c = logit of residue-polynomial
    roots, derived and beta-transfer-tested (beta=20 polynomial predicts
    beta=12-28 flips, max offset 0.022); multiplicity = root count across
    three geometries; the creep located at the cancellation floor
    (RESIDUE_RATIO_RESULT.md). THE SELECTION RULE (v84, selection_rule.py):
    Class-II statics need a vanishing background AND opposite-sign residues;
    mu* = mid + ln(-B/C)/(2 beta); positive (1.828) and negative (1.586)
    cases both measured; pair identity confirmed by beta-flow
    (SELECTION_RULE_RESULT.md). THE RESONANCE ATLAS (v85, resonance_atlas.py,
    CONSOLIDATION): one spine -- mu* = anchor + ln(ratio)/(q beta) for both
    classes; integration audit A-F PASS (devs 0.006-0.031, live 0.003);
    honest catch: the L=6 ~1.8 object unclassified; BEST_METHODS v85
    edition, rules 10-18 (RESONANCE_ATLAS_RESULT.md). THE CORE C SURROGATE
    (v86, csurrogate.c/h + csurrogate.py): every banked advance frozen into
    dependency-free C beside the engine -- features, magnitude model, sector,
    period, regime, Class-I roots, Class-II static, orientation stepping;
    engine-style gate with fresh-seed live references, match to 3.6e-15
    (CSURROGATE_RESULT.md). THE C SURROGATE UNDER TEST (v87,
    csurrogate_bench.c): clean-room caught 3 portability bugs (fixed; builds
    c99 + c11-pedantic); 1.5 us features (x212), 3-19 ns laws, ~875,000x per
    answer vs exact; two n-ceilings (computational ~unbounded vs validity
    n=3, extraction cap n<=6-7); transfer scope revised to 2.3x pooled
    after the contamination hypothesis was tested and excluded
    (CSURROGATE_BENCH_RESULT.md). THE ORDER AXIS (v88, order_axis.py): the
    spine survives n=4 (roots 0.156/0.643, transfer 0.024, no refit) and
    partially n=5 (lower root live-verified 0.011; upper marginal at the
    predicted wall); C surrogate extended with higher-order sets;
    exact-integer-determinant numerics catch (ORDER_AXIS_RESULT.md). THE
    DEEP PARTNER (v89, deep_partner.py): the ~1.8 object identified
    (level-2 deep partner, c=-4.44) and the "2.2 family" closed (upper
    partner, c=+2.95); the v85 c-drift quantified as sign-scan noise; the
    deep root's logit law large-beta scoped with the adjacent-comb creep
    measured in position (DEEP_PARTNER_RESULT.md). THE TWO-WINDOW CREEP
    CROSS-CHECK (v90, #100, creep_crosscheck.py): the deep trajectory is
    ANCHORED (1.824 - 0.72/beta; logit rejected) and geometry-independent
    (devs 0.001-0.011) -- the third static-class instance; anchor candidates
    2*sqrt(2)-1 (= the L=8 anchor) vs 11/6, open at +/-0.022
    (CREEP_CROSSCHECK_RESULT.md). THE CORRECTION PROPAGATED (v91): both
    prediction surfaces updated -- surr_static_l6_deep in the C surrogate
    with corrected Class-I scope; static_l6_deep + audit gate G in the
    atlas (CORRECTION_PROPAGATION_RESULT.md). THE ANCHOR TEST (v92,
    anchor_test.py + anchor_bridge.py): the v90/v91 law scoped to
    beta<=32; the deep-beta heavy-tail audit (kurtosis ~4500, multi-draw
    protocol mandatory); honest a_inf = 1.8437 +/- 0.0068 with the bridge
    verdict NOT RIGID -- octagon chord leading at 0.60 sigma, id OPEN,
    structural derivation primary (ANCHOR_TEST_RESULT.md). THE
    EXPONENT-BALANCE LAW (v93, exponent_balance.py): statics derived as
    integer-weighted means of the lattice's own levels -- the field
    theorem excludes the chord structurally and answers tau0/tau1 (no
    cross-anchor mixing); the frozen beta=36/40 discriminator selected
    11/6 at ~80:1 (EXPONENT_BALANCE_RESULT.md). THE SIDE-BY-SIDE (v94,
    law_sidebyside.py): surfaces parity-locked, out-of-sample frozen
    predictions measured at beta=44/52 -- the 11/6 identification
    REOPENED (~9:1 for 13/7 on the new points; a constant 1.8467(21)
    also fits, reviving the chord); the menu's degree bound is the
    raised decisive item (SIDE_BY_SIDE_RESULT.md). THE DEGREE BOUND
    (v95, degree_bound.py): census-settled at 7 = 2n+1 with full
    330-monomial support; the differences-menu adds 24/13 (q=13,
    near-flat) at 0.26 sigma from the constant reading -- the tension
    dissolved; identification open among {13/7, 24/13}; the coefficient
    program is the named closing route (DEGREE_BOUND_RESULT.md). THE
    COEFFICIENT PROGRAM PHASE 1 (v96, coefficient_flow.py): the
    FrozenCDet instrument validated and faithful; the background ALIVE
    (no midpoint static in (1,2)); the creep carrier identified
    (far-level antiperiodic images); prediction test inconclusive with
    the phase-2 spec computed (COEFFICIENT_FLOW_RESULT.md). THE PARITY
    TABLE (v97, parity_table.py): five window backgrounds across both
    lattices; the binary A=0 rule falsified by its own frozen test; a
    20-40x suppression pattern banked; the v84 L=8 static reread as a
    root-flow crossing with the deep-beta crossover replay registered
    as a frozen prediction (PARITY_TABLE_RESULT.md). THE METHOD AUDIT
    (v98, METHOD_AUDIT_v97.md): the suppression pattern found
    confounded (parity vs rationality); the root-flow claim downgraded
    to CANDIDATE; the L=8 prediction quantified (FROZEN_CURVE_Z8); the
    queue reordered by leverage -- coefficient phase 2 first. PHASE 2
    (v99, coefficient_phase2.py): the heavy-tail problem solved (IS
    sampler, 31x); the frozen polynomial measured (root z_pol(36) =
    1.8249(12)); root-flow excluded at ~10 sigma; THE TWO-SECTOR
    DISCOVERY -- the delta1 antiperiodic-image sector Delta is the
    second player at the zero; v96 faithfulness falsified at 3.4 sigma
    (COEFFICIENT_PHASE2_RESULT.md). THE DELTA SECTOR (v100,
    delta_sector.py): that second player resolved as a delta1 x f2
    CROSS-TERM (Delta(0)~0), measured and beta-growing, moving the
    frozen root toward the physical zero; the 13/7-vs-24/13 closure
    reduced to the assembled root flow z(beta) (DELTA_SECTOR_RESULT.md).
    And
    the slice hierarchy's WEIGHT half is UNIVERSAL and robust: 1d/bulk
    concentration grows 32x -> 165x with L, and holds 11x-184x (median, seed-
    stable) across order/temperature/filling/observable -- with U exact by
    theorem (SLICE_SCALING_RESULT.md + SLICE_UNIVERSALITY_RESULT.md;
    slice_scaling.py, slice_universality.py, FastCDet validated 4.2e-17). The
    per-class SIGN hierarchy was exposed as heavy-tail estimator-fragile and is
    downgraded to OPEN pending tail-aware statistics (v58 amendment). A freeze-
    then-predict derivation of the concentration from propagator/MST geometry
    was attempted and FALSIFIED (minor ingredient, ~17% of variance; prediction
    under-shoots 5-10x) -- the mechanism is open (DECAY_LAW_RESULT.md,
    decay_law.py). The dual-mechanism hunt (v60) confirmed tau-interference as
    a second component (40% of variance; averaging it out doubles the law) and
    measured real-but-insufficient propagator anisotropy; a ~10x closed-line
    enhancement remains (DUAL_MECHANISM_RESULT.md, dual_mechanism.py). The
    winding-phase ring-closure hypothesis was then FALSIFIED by a paired
    antiperiodic-twist experiment -- the enhancement is closure-independent;
    the unpaired run's fake 4x is banked as the artifact it was, and "pair
    every comparison" is standing methodology (RING_CLOSURE_RESULT.md,
    ring_closure.py). 1d channeling was then CONFIRMED (v62): ~2x at
    matched distance, graded monotone in collinearity, anisotropy-controlled
    and paired (CHANNELING_RESULT.md, channeling.py). Mechanism ledger: three
    confirmed (distance, tau-interference, channeling) + anisotropy minor + one
    falsified (winding). The arc CLOSED in v63: channeling compounds with
    length; the cleanly-identified two-coefficient law (b=0.537 bulk-only,
    c=+0.583 paired) composes to 59x vs the measured 75.5x -- locked at 1.27x
    agreement (MECHANISM_CLOSURE_RESULT.md, mechanism_closure.py). Open theory
    item: derive c.

## Contents
- engine/                full extended source. Builds clean; `golden.json` included;
                         194/194 verification checks pass. Adds to the original
                         engine: `ring_init` (arbitrary-L ring) and `square2d_init`
                         (2D square torus), both analytic eigenbases, validated to
                         machine precision against the original hexring.

- 01_tci_integrator/     Tensor-cross-interpolation on the time-INTEGRAL (acts on
                         the evaluation count, not the 2^n). Validated win on the
                         atom (simplex/time-ordering, ~1e-5). HEXRING_RESULT.md
                         records the measured FAILURE on the real multi-site lattice
                         (stuck at ~24% — the win rode the atom's single-site
                         symmetry) and the real path (frequency/IR basis).

- 02_control_variate/    The big win. The "failed" hexring TCI surrogate, used as a
                         CONTROL VARIATE, gives ~40-80x fewer Monte-Carlo samples
                         for the same error bar (correlation ~0.99, unbiased,
                         brute-force validated at n=4, holds at n=6). Reduces the
                         count of expensive evaluations, not the per-call 2^n.

- 03_streaming/          Exact streaming reformulation (out-of-core). Path A
                         (ranked convolution + long double; fast/sequential but
                         (n+1)*2^n storage) vs Path B (frugal 2*2^n but O(3^n)
                         recompute). Plus the measured fact: the path is
                         compute-bound, I/O is <0.2% of wall time, so async-I/O
                         overlap buys ~nothing; and lossless compression ~1.5x
                         only buys ~half an order of n.

- 04_locality/           The size-axis proof. Engine extended to large rings;
                         far-separated vertices suppress the connected determinant
                         exponentially (ratio 7e-3 -> 1e-11 as separation grows).
                         order_axis.py shows locality does NOT help the order axis
                         (compact high orders stay healthy -> full 2^n).

- 05_2d_lattice/         2D square torus extension (the real condensed-matter
                         geometry). Eigendecomposition exact to 2e-16. Demonstrates
                         the thermodynamic limit: a fixed local observable converges
                         to a system-size-independent value by ~12x12, at constant
                         cost. Locality confirmed in 2D.

- framework_bridge/      SEAM_RESOLUTION.md — adjacent work: the transcendental
                         boundary between the Watford and Nielsen frameworks, and
                         its resolution (even spectral data = modular forms; odd
                         zeta(3) cancels under supersymmetry; residue = ln(k_H)).
                         Uses the same DiagMC/determinant tooling.

## Build & verify the engine
```
cd engine
for f in *.c; do cc -O2 -std=c99 -I. -c "$f" -o "${f%.c}.o"; done
# link the verification main with the core (non-main) objects:
CORE=$(for o in *.o; do nm "$o" | grep -q " T main" || echo "$o"; done)
cc -O2 test_cdet.o $CORE -lm -o verify
./verify          # expects: RESULT: 194 passed, 0 failed
```
The result oracles in 01/04/05 link the same core objects (exclude all *main*
objects, add the one oracle .c). Each result folder's writeup states its own
build line.

## Honest one-paragraph summary
The per-order 2^n is irreducible — it is a count, and we measured (full rank, every
basis) that it has no shorter exact description. What is real and reduces: the
number of expensive evaluations (control variates, ~40-80x), and the entire
system-size dependence (locality — proven, 1D and 2D, the thermodynamic limit at
constant cost). The streaming/compression routes move the cost between RAM, disk,
and compute but do not shrink the count. Every claim here is backed by a run in
this archive.
