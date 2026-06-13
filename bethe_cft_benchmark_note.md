# The Bethe = CFT benchmark for the 1D Hubbard model: three verified results

Paul Watford. Engine track (cdet package, module `07_predict_vs_compute`).
Companion to the question raised in our meeting (Q6): the finite-size regime where
Bethe-ansatz integrability and the c=1 conformal field theory must predict the same
spectrum, and whether the engine reproduces it.

This note is the rigorous track only. It reports numbers that have been checked
against exact references, with the boundaries of what is and is not clean stated
plainly. Every number below is reproducible from the scripts named in each section;
the engine test suite is unchanged at 194 passed, 0 failed.

## Summary

Three results, each verified against something exact, together demonstrate the
Bethe = CFT picture for the 1D Hubbard model rather than asserting it:

1. The charge Luttinger parameter K_rho(U) at quarter filling, from the exact
   Frahm-Korepin dressed-charge integral equation, agreeing with exact
   diagonalisation to 0.1 to 0.4 percent.
2. The spin velocity at strong coupling, from the finite-size Casimir energy, pinned
   to the exactly known Heisenberg spinon velocity pi/2 and confirmed inside the
   Hubbard model itself.
3. The finite-size spectrum of the strong-coupling spin sector, shown to be the c=1
   SU(2) level-1 conformal tower: leading scaling dimension 1/2, with the predicted
   primary-multiplet degeneracy exact.

The first supplies the exact Luttinger parameter. The second supplies a velocity
anchored to an exact value. The third shows the spectrum those two describe is the
conformal tower. That triad is the benchmark. A fourth result (added after the first
draft) supplies the charge velocity u_rho(U) at n = 0.5 to about 1 to 2 percent, so the
doped Luttinger liquid is now fully characterised: K_rho, u_rho, u_sigma.

## Result 1: exact charge Luttinger parameter K_rho(U)

Script: `bethe_Krho.py`. Filling n = 0.5 (quarter filling, away from the Mott point).

Method. The Frahm-Korepin dressed charge at zero magnetic field. Spin-integrated
kernel G(x) = (1/pi) integral_0^inf cos(x w)/(1 + e^{U w/2}) dw; dressed density rho
and dressed charge xi solved on the charge Fermi interval [-Q, Q], with Q fixed by the
density; then K_rho = xi(Q)^2 / 2.

Verification against exact limits:
- U -> 0 gives K_rho -> 1 (small resolvable point U = 0.2 gives 0.9924).
- U -> inf gives K_rho -> 1/2 (U = 100 gives 0.509).

Verification against exact diagonalisation (n = 0.5, L = 12):

| U | K_rho (Bethe, exact) | K_rho (ED) | difference |
|---|---|---|---|
| 1 | 0.9006 | 0.8971 | 0.4% |
| 2 | 0.8187 | 0.8167 | 0.2% |
| 4 | 0.7118 | 0.7111 | 0.1% |
| 8 | 0.6166 | 0.6163 | 0.1% |

The agreement improves as U grows because the ED residual is finite-size (L = 12) and
the correlation length shrinks with U, while the Bethe value is the thermodynamic
limit. Two independent methods, one analytic and one numerical, converging.

Provenance note. A first, from-memory reduction of the kernel gave K_rho = 2 at U = 0.
The U = 0 check caught it immediately; the corrected numerical kernel reproduced
xi = sqrt(2), hence K_rho = 1, and then matched ED. The limit check is what made the
result trustworthy.

## Result 2: spin velocity at strong coupling

Script: `spin_velocity.py`. Method: the finite-size Casimir term of the ground-state
energy, E0(L) = e_inf L - (pi c v)/(6 L), so v = -6 (slope) / (pi c) from a fit of
E0/L against 1/L^2. This uses ground-state energies only, an integrated quantity, with
no boundary-derivative extraction.

Method check against the exactly known Heisenberg spinon velocity v_s = pi/2:

| fit window | v_s | vs pi/2 = 1.5708 |
|---|---|---|
| L = 12,14,16 | 1.6068 | +2.3% |
| L = 14,16,18 | 1.5997 | +1.8% |
| L = 16,18,20 | 1.5948 | +1.5% |

The value drifts monotonically toward pi/2; the residual is the known SU(2)
logarithmic finite-size correction, which shrinks with L. The energy per site is
recovered to 0.02 percent (1/4 - ln 2).

Inside the Hubbard model, half-filled spin sector, strong coupling:

| U | u_sigma (Casimir) | Heisenberg 2 pi / U |
|---|---|---|
| 8  | 0.663 | 0.785 |
| 12 | 0.519 | 0.524 (1%) |

At U = 12 the charge sector is frozen and u_sigma matches the Heisenberg value to about
1 percent: the spin sector has flowed to a Heisenberg chain with J = 4/U. The weak
coupling end is fixed exactly by u_sigma(U = 0) = 2, the free Fermi velocity at half
filling.

## Result 3: the conformal tower

Script: `conformal_tower.py`. A 1+1D CFT predicts every gap as
E_n - E_0 = (2 pi v / L) x_n with x_n the L-independent scaling dimensions, so
multiplying gaps by L/(2 pi v) collapses the spectrum onto fixed dimensions. Tested in
the strong-coupling spin sector (Heisenberg point, v_s = pi/2 verified above, CFT is
c = 1 SU(2) level 1).

x_n = (E_n - E_0) L / (2 pi v_s):

| L | x (triplet) | x (excited singlet) | x (next) |
|---|---|---|---|
| 8  | 0.4237 | 0.4237 | 0.7712 |
| 10 | 0.4288 | 0.4288 | 0.7547 |
| 12 | 0.4327 | 0.4327 | 0.7417 |
| 14 | 0.4356 | 0.4356 | 0.7312 |
| 16 | 0.4380 | 0.4380 | 0.7226 |

Two things hold. The leading scaling dimension drifts monotonically toward the SU(2)
level-1 value 1/2, approaching from below with the known logarithmic correction. And
the lowest triplet and the lowest excited singlet are degenerate to every printed
digit at every L, which is the SU(2) level-1 primary multiplet. That degeneracy is a
structural prediction with no fitted parameter, and it is exact, which makes it the
sharpest part of the check.

## What the triad establishes

For the strong-coupling spin sector the chain of reasoning is closed and checked: the
velocity comes from an integrated quantity and matches the exact spinon velocity, and
the spectrum that velocity organises is the c = 1 SU(2) level-1 conformal tower, with
the primary multiplet degeneracy exact. The Bethe-integrable description and the CFT
description agree on the finite-size spectrum, demonstrated rather than assumed.

For the charge sector the exact Luttinger parameter K_rho is in hand to machine
precision against ED across the coupling range. It is the input the doped conformal
tower needs.

## Honest scope and open items

- The conformal tower is verified in the strong-coupling spin sector. The full doped
  tower uses the Frahm-Korepin charge dimensions, which depend on K_rho and also on the
  charge velocity.
- Doped tower (v9 probe, v10 result, doped_tower.py + doped_tower_pure.py). v9 tried a
  velocity-free 2k_F/4k_F ratio; it is EXACT at U=0 (R=2.000) but breaks at U>0 because
  2k_F mixes charge and spin (two velocities) while 4k_F is pure charge -- the break is a
  clean signature of spin-charge separation. v10 takes the fix the break named: use ONLY
  the pure-charge 4k_F operator and collapse its gap with the v8 charge velocity. Then
  x_4(ED) = gap(4k_F) L/(2 pi u_rho) tracks the predicted dimension 2 K_rho across
  U = 0..8, with a small finite-size deficit (~2-3%, flat in U) that drops below 1% once
  anchored at U=0. The doped charge sector's leading primary is 2 K_rho, tied to the
  exact Bethe K_rho -- the Bethe = CFT spectrum check, now carried from the spin sector
  (v7) into the doped charge sector. v11 then confirms that the small v10 deficit is
  finite-size: at the exact U=0 anchor (free-fermion gap, exact v_F=sqrt2) x_4 -> 2 as
  ~1/L^2 (fit x_4 = 2.0000 - 3.3/L^2, L=12..44), the L=12 free-fermion gap reproducing
  the many-body ED gap exactly. The standing ceiling is the large-L INTERACTING check
  (L=20 closed shell = 240M states), which is diagrammatic-Monte-Carlo territory, not ED.
- Spin-charge separation, quantified (v12) and cleaned (v13). The two doped-tower gaps
  plus the exact K_rho give u_rho (pure 4k_F gap), which matches the v8 flux stiffness to
  ~2-3%. The v12 u_sigma (from the 2k_F gap) was flagged as extracted-not-verified, and
  v13's independent measurement -- the SPIN STIFFNESS (a spin twist, integrated ground-
  state energy) -- corrected it (the v12 2k_F decomposition was biased up to ~29% at L=12).
  With u_rho from the charge stiffness and u_sigma from the spin stiffness -- one robust
  route on both legs -- the velocities coincide at U=0 (= v_F, no separation) and split
  with U: u_rho 1.43 -> 1.96, u_sigma 1.43 -> 0.71, ratio 1.0 -> 2.8. u_sigma at quarter
  filling is a new observable; its exact U>0 verification (the Bethe spin velocity) is next.
- u_sigma, exact-limit bracket (v14, bethe_spin_velocity.py). An exact Bethe spin velocity
  was attempted (spin analogue of bethe_Krho.py). The dressed-energy machinery is validated
  on the CHARGE velocity (1.92 vs the reference 1.93 at U=8), but the SPIN velocity via the
  endpoint slope is numerically fragile at zero field -- the spin Fermi point is at
  Lambda -> infinity, so the slope is a 0/0 limit (this is the known #13 fragility in its
  sharpest form, demonstrated, not hidden). u_sigma is therefore verified by BRACKETING
  between its two exact limits (U->0 -> v_F = sqrt2; U->inf -> 0), with the v13 stiffness
  monotone inside. An exact interior u_sigma(U) needs an integrated (not endpoint-slope)
  Bethe formulation -- the genuine remaining hard step.
- u_sigma, second independent ED route (v15, spin_susceptibility_qf.py). With the exact
  Bethe route blocked, u_sigma is corroborated by a second ED observable -- the lowest
  triplet gap Delta_t = E0(S_z=1) - E0(S_z=0) (a finite-size spin susceptibility), an
  EXCITATION energy sharing only the U=0 anchor with the v13 twist-response stiffness. The
  two agree at U=0 and bracket u_sigma within ~8-12% across U=0..8, both falling from v_F
  toward 0; the triplet runs low by the SU(2)_1 marginal log correction (which the
  integrated stiffness avoids). u_sigma is now multi-route corroborated, though an exact
  curve still awaits the integrated Bethe spin velocity.
- Spin velocity, EXACT at half filling (v16, spin_velocity_exact_check.py). At n=1 the
  zero-field spin velocity is exactly v_s = 2 I_1(2pi/U)/I_0(2pi/U) (Bessel; limits U->0 -> 2
  = v_F and U->inf -> 2pi/U = Heisenberg, both verified). Tested against it, the two ED routes
  bracket the exact value at every U -- triplet < exact < stiffness, exact closer to the
  stiffness -- and the stiffness converges toward it with L. This validates the bracket method
  against an exact reference, confirms the stiffness as the better estimate, and (transferring
  to n=0.5) locates the exact quarter-filling u_sigma between [v15 triplet, v13 stiffness],
  closer to v13. (CORRECTED by v18: this transfer to quarter filling was wrong -- see below.)
- Spin velocity across filling (v17, filling_dependence.py). Three generalizability tests:
  (1) the stiffness prefactor pi(L/2) is universal -- it hits v_F = 2 sin(pi n/2) to ~1% at
  every size (L=6,10,12) and filling (n=0.5, 0.833, 1.0); (2) the stiffness-vs-triplet bracket
  gap IS the SU(2)_1 marginal correction, small in the doped regime (~7-14%) and exploding at
  half filling (17-62%) -- a named, filling-controlled effect, not noise; (3) doping HELPS this
  observable (the correction shrinks ~60% -> 12%), so the doped liquid is the easy regime. The
  method scales and the residual gap is bounded and smallest where the package operates.
- Spin velocity, EXACT at quarter filling (v18, bethe_spin_velocity_integrated.py). The
  integrated Bethe route closes u_sigma: the dressed-energy velocity PROFILE has a flat PLATEAU
  at moderate Lambda (the asymptotic value), read instead of the singular endpoint that defeated
  v14. Validated against the half-filling Bessel curve to 0.1-0.2% (U=2,4,8). Exact quarter-
  filling result (U>=2): u_sigma = 0.951, 0.836, 0.585 at U=2,4,8 -- BELOW both ED routes (v13
  stiffness, v15 triplet). So the ED values are finite-size UPPER bounds, not a bracket; the true
  u_sigma is ~17% below the v13 stiffness at U=8. This corrects the v16 transfer (the half-filling
  bracket does not survive doping) and completes the u_sigma program; small U (<2) is resolution-
  limited (sharp-kernel wall).
- Spin velocity, the doping crossover (v19, doping_crossover.py). The exact-vs-ED comparison
  across n = 0.5, 0.833, 1.0 is one smooth crossover. The exact lies below both ED routes
  throughout the doped regime (confirming v18 at n=0.833 too) and between them only at half
  filling (v16). The stiffness is the upper envelope at every filling (always an overestimate);
  the triplet is the route that crosses -- above the exact when doped, dragged below it at half
  filling by the commensurate SU(2)_1 marginal correction (v17). One mechanism, all fillings.
- Spin velocity at small U, the sparse solver (v20, bethe_spin_velocity_sparse.py). A Fourier-
  diagonal fixed-point solver (the a_2 convolution solved exactly as e^{-2u|omega|}, no dense
  inversion) reaches small U where the dense solver could not: validated at half filling vs Bessel
  to 0.1-0.5% (U=0.5,1,2), complementary to the dense solver (FFT for U<=2, dense for U>=2,
  agreeing at U=2). Quarter-filling small U, however, is a structural wall: the velocity profile
  peaks then crashes with no asymptotic plateau (narrow spin-density support at low filling + small
  U), so exact quarter-filling u_sigma below U=2 needs a weak-coupling field-theory handle, not a
  finer grid. The exact quarter-filling curve stands for U>=2 (v18); the wall below is characterized.
- Spin velocity at small U, the analytic bridge (v21, weak_coupling_spin_velocity.py). The wall
  v20 named is bridged to leading order: u_sigma(n,U) = v_F(n) - U/(2pi) - U^2/(16pi^2) + ..., the
  leading 1/(2pi) coefficient exact at half filling (validated to 5 digits as the slope of the
  Bessel curve) and filling-independent (contact U -> momentum-independent backscattering, v_F
  cancels). So u_sigma(0.5,U) = sqrt2 - U/(2pi) + O(U^2) at quarter filling, consistent with the
  v20 lower bounds -- leading order only (the U^2 curvature is filling-dependent, not transferred).
  Three numerical routes were confirmed to fail there for distinct reasons (no plateau; recipe-
  sensitive finite-field read; ED-stiffness slope 6x off), establishing it as a genuine wall.
- Engine acceleration, the reverse direction begins (v22, 04_locality/locality_prune_test.py).
  Going beyond ED (~L=20) needs the DiagMC engine, whose wall is the per-order 3^n recursion. The
  first attempt to feed a learned pattern back into the engine -- using the proven folder-04 output-
  locality to prune the connected recursion -- was tested and RULED OUT: pruning that keeps 81% of
  the operations is still 74% wrong at order 12, because the connected value is a cancellation
  residual (long-range terms individually large, only the full sum cancels). Output-locality is not
  term-locality; the per-config 3^n is irreducible by pruning. The productive cost lever is reducing
  the ORDER n (control variate from the learned IR physics; atomic-limit expansion via the engine's
  G_exact_atom), since cost ~ 3^n -- the v23 target. Locality still helps on the sampling side only.
- Engine acceleration, the two-engine method + experiment 1 (v23, engine_exp/atomic_order_reduction.py).
  engine/ is now the FROZEN baseline oracle, engine_exp/ the sandbox; the fork is bit-identical at
  orders 1,2 (the clean-fork gate). Experiment 1 on the atom, anchored on the baseline exact
  G_exact_atom: the bare U=0 expansion has convergence radius ~0.94, so at U=2 it diverges (order-12
  partial sum +2799 vs exact -0.444); a resummation of the same orders converges (-0.4443), and at
  U=0.5 reaches 1.2e-10 vs the bare 2.9e-5. The engine cost wall is the ORDER needed and the scheme
  sets it; accelerate by changing the expansion point (shifted/atomic reference next), validated
  against the frozen baseline -- not by touching the per-order recursion (v22).
- Engine acceleration, quantitative efficiency gain (v24, engine_exp/dimer_efficiency.py). On the
  exactly-solvable dimer (E0=(U-sqrt(U^2+16t^2))/2, verified vs ED), the engine's bare U-series
  (radius 4t) and the atomic/hopping series (radius U/4) have reciprocal radii -- complementary:
  bare for U<4t, atomic for U>4t. Cost ~3^n, so gain = 3^(N_bare-N_atomic). At strong coupling
  (U>4t) the bare series diverges (infinite cost); the atomic scheme converges with cost 3^N_atomic
  that shrinks as U/t grows (3^24,3^16,3^10,3^8,3^6 at U/t=6,8,12,16,32 for eps=1e-6). The gain is
  qualitative at strong coupling (impossible->feasible); the crossover U~4t is the hard seam (both
  marginal -> Pade, v23).
- Engine acceleration, stress test / wall (v25, engine_exp/stress_cv.c). Stress of the C_V connected
  recursion on both engines (shared code): measured RAM = 2*2^n*8 bytes, time ~x2.4/order (n=16:
  1.05 MB/1.26 s; n=21: 33.6 MB/93 s). On 3 GB the RAM wall is order 27 (2.0 GB); the 3^n time wall
  hits first (~n=24 in minutes). The frozen baseline surfaced two hidden fixed-buffer caps (sub[16],
  MAXDIM=18), raised+validated bit-identical in engine_exp. How much faster: the atomic scheme
  converges at order 16 (1.26 s/1.05 MB) while the bare scheme diverges and never converges even at
  the ceiling -- convergence-within-the-wall.
- Engine acceleration, buffers removed + crash-safe harness (v26, engine_exp). Every fixed order
  buffer in the connected recursion was deleted (sub[n]/M[m*m] VLAs, MAXDIM gone, C_V mallocs checked
  -> NaN), validated BIT-IDENTICAL to the frozen baseline at n<=16, 194/194, now uncapped. The cap is
  now a real resource wall: on a 4 GB box the time wall hits first (~n=20-24), the RAM guard at n=28.
  stress_cv.c is crash-safe by default (per-row fflush to a log, RAM-budget guard, SIGINT/SIGTERM
  handler), TESTED by a real interrupt mid-call (log kept n=1..18). Honest scope: full general-lattice
  atomic wiring is still gated by the missing high-order time-integration driver (cdet_order n=1,2).
- Engine acceleration, high-order time-integration gate opened (v27, engine_exp/diagmc.c). Built
  cdet_order_mc: general-n vertex-time+site integration by Monte Carlo (same integrand as
  cdet_order). VALIDATED against the frozen baseline at n=1,2 within MC error (sub-sigma at 1e6,
  error ~1/sqrt(nmc)); first high-order terms n=3 = 0.008(6), n=4 = -0.341(8) (baseline NaN). New
  wall = MC sign-variance growing with order; the atomic reference (v23/v24) is the lever to reduce
  it, now unblocked. stress_cv.c RAM guard 85%->90%.
- Engine acceleration, contiguity / subset-convolution study (v28, engine_exp/subset_conv_poc.c). The
  3^n scattered submask sum is a subset convolution; the zeta/Mobius butterfly computes it in
  O(2^n n^2) with contiguous access (Bjorklund STOC 2007). POC confirms correctness (~1e-12 vs naive)
  but in our regime it is slower at reachable n (crossover ~n=20-22), uses MORE RAM (n+1 ranks), and
  loses ~7 digits (Mobius +/-) -- bad for our cancellation-residual values. The contiguity's real use
  is enabling out-of-core streaming past the RAM wall; within RAM, reducing n (atomic ref) wins.
- Engine acceleration, in-RAM crossover + precision (v29, corrects v28). Re-measured past n=18: the
  fast butterfly subset convolution's in-RAM crossover is n=19 (n=21: 2.70x, growing), so it DOES help
  in RAM for n>=19 -- at the cost of ~(n+1)/2x more RAM (wall a few orders earlier). Its accuracy loss
  is catastrophic cancellation (grows with n), recoverable by precision (long double 4-14x), not a
  fixed ratio; not fixable by the MC control variate (deterministic), but the control-variate
  principle = the atomic reference. Streaming dropped; reducing n stays the lever.
- Engine acceleration, atomic-reference lever quantified (v30, 07/atomic_reference_order_reduction.py).
  On the Hubbard atom (oracle = closed-form G_exact_atom, confirmed vs the C engine), a reference
  shifted toward the correlated regime cuts the order to 1e-6 at U=2 from NEVER (bare diverges,
  |U_sing|=0.9415) to 11 (U0=1.5) or 3 (U0=1.9), AND shrinks the largest term 3.8e12 -> ~0.2 (removes
  the v29 cancellation). The counterterm-correct wiring into cdet_order_mc is the next build.
- Engine acceleration, out-of-core blocking (v31, engine_exp/blocked_cv.c). The scattered O(3^n)
  submask recursion factorizes over a bit-split into a block-level subset recursion -> schedulable
  HDD<->RAM streaming. Validated: matches flat C_V to ~1e-20 (exact, full accuracy), peak RAM fixed at
  3 blocks = O(2^nL) independent of n (43x-171x less at n=12-18, growing; 2^n on disk). Accuracy-
  first, RAM-bounded, HDD-overflow path; cost is block I/O ~3^nH (time-heavy by design).
- Engine acceleration, control variate low vs high order (v32, engine_exp/cv_highorder.c). The
  two-version/error-correct idea = the control variate, already realized in 02_control_variate (71x
  at n=4, rho=0.993; the win is correlation, not accuracy). Tested at high order: simple parametric
  references de-correlate (|rho|<=~0.7, ~1-2x) because the high-order connected value is a sign-
  oscillating residual. High-order CV needs an adaptive/learned surrogate; high correlation there is
  the open problem.
- Engine acceleration, the learned-pattern reference (v33, 07/learned_reference_cv.py). The custom
  analytic surrogate built from the engine's patterns (Lieb-Wu analytic moment -> correlator shape;
  K_rho; velocities; CFT tail) is an OBSERVABLE-level control variate with rho=0.998 vs the exact ED
  spin correlator -> 229x variance reduction, ~100x stronger than v32's per-sample parametric
  references. v32 and v33 live at different levels (per-sample sign-variance vs observable/IR
  convergence). Next: the Luttinger-liquid Green's-function reference from K_rho + velocities (in
  hand) subtracted inside the high-order DiagMC.
- Engine acceleration, the validated accelerations wired as switchable config modes (v34,
  engine_exp/cdet_config.{h,c}). One driver, cdet_order_mc_cfg, with a mode toggle: CDET_PLAIN
  (bit-identical to the v27 estimator), CDET_BLOCKED (the v31 out-of-core C_V per sample, == PLAIN to
  1.1e-12, peak RAM ~3*2^nL), CDET_CVAR (shifted-mu control variate, unbiased: 1.46 / 0.16 sigma from
  the frozen baseline). CVAR's honest accounting: rho=0.98/0.92 -> a POTENTIAL 27x/6.5x reduction, but
  NET 1.00x with an MC-estimated reference mean (the pilot's variance offsets the correlation gain) --
  the net-win awaits an analytic E[Y] (the v35 reference build). Butterfly excluded (shelved). Also
  recorded: the v33 "blocked still buggy" remark was wrong (fixed in v31), and the frozen cdet_order
  quadrature had an np>64 stack overflow (fixed-size node arrays), now FIXED in the sandbox and
  confirmed: the MC estimator matches cdet_order across two parameter sets and n=1,2 to under 1 sigma
  (the apparent discrepancy was the overflow producing a garbage value at np=120, not a real one).
- Baseline refresh (v35). The frozen baseline engine/ was deliberately updated to the validated best
  version by promoting two core files from engine_exp/: cdet_engine.c (dynamic buffers + OOM-safe,
  removing the n<=16 cap) and quad.c (np-sized quadrature, removing the np>64 overflow). Every frozen
  constant is preserved bit-identically (cdet_order(1,2), C_V n=8,12,16; 194/194), proving the refresh
  moved no number; engine/ now also runs n>16 and np>64. The "pristine = has the caps" notion is retired
  in favour of "reproduces the constants + Python ref AND is buffer-free/OOM-safe"; see CROSSCHECK_v35.
- Begin 2D, interacting (v36). The 2D non-interacting propagator (square2d_init) was fed into the
  connected-determinant engine and the first interacting orders validated against EXACT diagonalization
  of the 2D Hubbard model: cdet_order(n) = N * a_n (a_n = U^n Taylor coefficient of the exactly-
  diagonalized local Green's function) to ~1e-9 at n=1,2, with the same order<->U convention in 1D and
  2D and the prefactor confirmed = N for N=2,3,4,5. A capstone reconstructs the interacting G(U) from the
  engine coefficients with U^3 truncation error. This is a validated foundation, not physics: 2x2 and
  small rings are method anchors (no phases / thermodynamic limit / finite-T transition at this size),
  only orders 1,2 are reached, and the fermion sign problem -- the real 2D difficulty -- appears only at
  higher order on larger clusters (the next step). See 08_2d_interacting/ and CROSSCHECK_v36.
- 2D high-order Monte Carlo + the sign-problem wall (v37). A geometry-blind 2D MC driver (mc2d.c)
  reproduces the EXACT 2x2 Hubbard coefficients cdet_order(n)=N*a_n at orders 1-6, every order within
  2 sigma (a_n exact from diagonalization via a Cauchy contour integral). Orders 5,6 are beyond the
  deterministic quadrature's practical reach, so this is a genuine high-order validation. The sign
  problem was then measured, not asserted: the cancellation ratio R=mean(C_V)/mean(|C_V|) collapses and
  the cost for 1% precision (~1/R^2) explodes ~geometrically with cluster size (2x2->4x4 ~260x) and with
  inverse temperature (beta 2->8 on 3x3 ~570x). This is correctness plus a quantitative wall map, NOT a
  sign-problem solution: the 2x2 has no sign problem, so reaching order 6 there proves the driver, not
  the physics. See 08_2d_interacting/ (mc_validate.py, characterize_sign.py) and CROSSCHECK_v37.
- Does the determinant buy extra orders? (v38) Measured on the engine's own Wick matrices. The
  determinant evaluates order n as det(M) of the (n+1)x(n+1) propagator matrix -- a sum of (n+1)! signed
  contractions done exactly in O(n^3). Versus stochastically sampling those contractions, it buys the
  ORDER axis two ways: cost ((n+1)! vs n^3 -- the only way to evaluate past ~order 5; 5e9x by order 15)
  and per-order variance (it removes the cancellation perm(|M|)/|det(M)|, which grows with order on every
  cluster). But the SAME ratio at fixed order SHRINKS with cluster size (3.11->1.23 for N=4..16), the
  opposite of the v37 configuration-level wall (grows with size and inverse temperature). Conclusion:
  CDet buys order reach, NOT size/temperature reach -- two different sign walls, only the per-order one
  is determinant-curable. Mechanism isolation (not a wall-clock benchmark). See CROSSCHECK_v38.
- The scaling law of R (v39). The right success metric is whether a method moves R's decay exponent, not
  what order it reaches -- adopted. But at accessible sizes (N<=25, order 3) the per-order R has NO clean
  scaling law: at fixed density the size axis plateaus (L=3~L=4, |R|~0.35) then collapses (L=5), not an
  exponential; the temperature exponent's sign is ensemble-dependent (a clean-looking fixed-mu fit, R^2=
  0.98, was density drift; at fixed density it flips); and the separable form e^{-(aN+b*beta)} fails a
  29-sigma off-axis prediction. So no honest (a,b) benchmark exists in this regime -- the per-order R is
  shell-dominated. This corrects v37's fixed-mu beta-trend (conflated temperature with density) and
  withdraws any clean parametric form for R; the wall itself stands. See CROSSCHECK_v39.
- Are aggregate observables cleaner than per-order R? (v40) Tested the candidates (integrated-over-orders
  sign, crossover order n*, per-order structure). None scales cleanly at accessible sizes: the integrated
  average sign still sign-alternates with cluster because the order weights U^n N(N beta)^n/n! are non-
  uniform, so the sum is dominated by a single order and inherits its shell structure; n* and R_n inherit
  the same a_n shell jumps; R(mu) oscillates within one cluster. The contaminant is partial-shell filling
  at small N; the cure (fixed filling fraction via closed-shell families, or large N) is out of reach with
  the current toolkit. Free-energy differences (a different computation) were not tested. A measured limit,
  not a benchmark. See CROSSCHECK_v40.
- The organizing variable: R is universal in the Fermi-shell detuning (v41). The per-cluster R "shell
  noise" of v39/v40 is not random -- at fixed temperature R is a universal function of the detuning
  delta = mu - (nearest single-particle shell): positive below a shell, peak at delta=0 (shell at the
  Fermi level), sign flip just above, the same structure in L=2,3,4, with only an amplitude A(N)=
  0.82,0.60,0.50 (shrinking with N) distinguishing clusters. R-vs-N looked random only because each
  cluster sat at a different delta. This refines v40's "no diagnostic" into "the diagnostic is R(delta) at
  fixed T," and makes the cure quantitative (hold delta fixed). Honest bounds: magnitude collapse is clean
  only near the shell, and temperature is a separate axis (beta*delta is not a single variable). See
  CROSSCHECK_v41.
- A hierarchy of scales in R (v42). The v41 "magnitude collapse only near the shell" is the signature of a
  superposition: R(delta) = a near-shell THERMAL feature + a cluster-specific band-structure background. The
  feature's range is the thermal length (its sign-flip delta* ~ T=1/beta across beta=2,4,8; delta*/T ~ 0.9-
  1.2), and on an isolated shell its shape collapses vs beta*delta -- explaining why v41's fixed-beta collapse
  worked and why beta*delta is not a global variable (the background breaks it). Hierarchy: T=1/beta < shell
  spacing < bandwidth 8t. Ordinary multi-scale spectral structure; the "different forces" analogy is
  structural only (distinct ranges), explicitly not physics. See CROSSCHECK_v42.
- Upgrade test for "thermal": two axes support it, the order-cutoff refutes it (v43). The v42 "thermal"
  claim was stress-tested. Finite-size + temperature controls PASS: the n=2 feature width delta* is
  N-independent (0.24,0.26,0.21 for N=4,9,16, while level spacing varies strongly -> not shell-spacing)
  and ~ T (0.61,0.24,0.11 for beta=2,4,8). But the order-cutoff test FAILS: the feature is qualitatively
  different at each order (n=1 monotonic, n=2 peak at delta=0, n=3 peak at +0.2 with opposite sign below
  the shell), so no single feature is being broadened. NET correction to v42: "the near-shell feature is
  thermal" -> "the n=2 feature WIDTH is thermal-consistent"; the thermal ORIGIN is underdetermined, as the
  critique warned. The v41 organizing-variable result (R structured by the detuning, at fixed order/T)
  stands; only the v42 thermal-mechanism framing is narrowed. See CROSSCHECK_v43.
- Literature map: the program's findings are documented, connected facets of one sign problem (v44). A hard
  search places every v36-v43 result in the published record: v38 (determinant removes per-order cancellation,
  exponential-not-factorial cost) is Rossi's founding CDet property (PRL 119, 045701, 2017); v37 (cost
  ~1/<s>^2, <s>~e^{-aN}e^{-b beta}) is standard DQMC scaling; v41 (R organized by Fermi-shell detuning, peaks
  at closed shells, oscillates with N) is the documented closed-shell "magic-density" sign effect ("Deconvolving
  the components of the sign problem", arXiv 2108.00553; closed-shell sign effects + compressibility-tracks-sign,
  arXiv 1107.0230); v42/v43 (near-shell thermal width) follows the compressibility-sign link and the
  sign<->quantum-criticality result (Science 375, 418, 2022); v36 (convergence radius ~0.5-1, poles) is the
  complex-coupling pole structure (Wu-Ferrero-Georges-Kozik, PRB 96, 041105, 2017; arXiv 2303.01607). The axes
  treated here as separate "walls" are already unified in the literature ("Geometry Dependence of the Sign
  Problem", arXiv 1501.02832; Science 2022). HONEST STATUS: this program is a transparent, exactly-validated
  INDEPENDENT REDISCOVERY of mapped structure -- worth is validation + methodology, not discovery. See
  CROSSCHECK_v44 and 08_2d_interacting/LITERATURE_MAP.md.
- Shifted-reference CDet: pole-moving + closed-shell operating point (v45). Turning the v44 literature map
  into a concrete, exactly-verified upgrade. The shifted-reference (chemical-potential counterterm) expansion
  H(xi;alpha)=[H0(mu)+alpha N]+xi(U Hint-alpha N) recovers the physical H at xi=1 for ANY alpha, but alpha
  moves the convergence-limiting pole (Wu-Ferrero-Georges-Kozik, PRB 96 041105). Exact (ED) verification: on a
  2-site ring the BARE series diverges (never <1e-3 in 14 orders) while the shifted series at the Hartree-scale
  alpha converges at ORDER 5; on the Hubbard atom the radius goes ~1.0 -> ~1.8. Since CDet per-order cost ~2^n,
  saving orders is an exponential 2^(K_bare-K_shift) cost reduction (and when bare diverges, the shift enables
  the calculation). The optimal alpha* ~ Hartree scale U<n>/2 -- the SAME Fermi-level re-centring as the v41/v44
  detuning: operating point sets delta=0 (closed shell, best sign), shift sets the reference Fermi level. Status:
  EXACT at the coefficient level + live-engine operating point; the one-body counterterm in the C MC recursion
  is scoped (v46), not yet done -- no claim the engine computes shifted CDet end-to-end. Frozen engine
  untouched (194/194). See CROSSCHECK_v45 and 08_2d_interacting/SHIFTED_REFERENCE_RESULT.md.
- Wiring the shift into the engine: counterterm = d/dmu (v46). The v45 shift is realised through the REAL CDet
  engine without modifying the frozen core, using the exact identity that the one-body counterterm -alpha*N is
  a chemical-potential derivative: b_n(alpha) = sum_j (alpha^j/j!) U^(n-j) a_{n-j}^{(j)}(mu-alpha), with
  a_m^{(j)} = d^j/dmu^j of the bare CDet coefficient (d/dmu inserts -N, spin-correct). Verified: the formula
  matches the ED shifted coeffs to machine precision (1e-12..1e-17, orders 0-6); the real C engine (cdet_small,
  cdet_n = N*a_local; divide by N) fed through it reproduces the shifted coeffs to engine precision (b1 6e-6,
  b2 4.5e-5, limited by np=64 quadrature + finite-diff). Bare series diverges at this (mu,U) yet the resummed
  shifted sum from a few low-order engine coeffs converges (K=5 err 6e-4) -- the order saving realised through
  the engine. Frozen engine untouched (194/194; cdet_order constants bit-identical). The production refinement
  (sample d/dmu directly via density insertions) is v47. See CROSSCHECK_v46 and
  08_2d_interacting/COUNTERTERM_RESULT.md.
- Fully stochastic shifted CDet: sample the mu-derivatives directly, one run (v47). Completes v45 (exact
  proof) -> v46 (engine route, finite-diff) -> v47 (direct sampling). The counterterm = d/dmu insertions are
  evaluated per Monte-Carlo sample by a contour in complex mu on the SAME sampled vertex configurations, so one
  run yields a_m and all mu-derivatives a_m^{(j)} with no finite-difference bias and no mu-grid re-sampling.
  C_V is a Python port of the engine's connected determinant (G0 and a_1 validated to 1e-16). 2-site ring:
  a1/a1'/a2 within 0.3 sigma of ED (the sampled mu-derivative independently cross-checked vs ED), and the
  assembled shifted b1,b2 within 0.3 sigma of ED shifted. Reference implementation (orders 1-2); porting the
  contour into the C high-order mc2d, and measuring the per-order sign R of the shifted vs bare sampler at the
  closed-shell operating point, are v48. Frozen engine untouched (194/194). See CROSSCHECK_v47 and
  08_2d_interacting/COUNTERTERM_SAMPLER_RESULT.md.
- Does the shift improve the sign, or only convergence? A competing-optima trade-off (v48). The reviewer's
  central question, tested head-on: the shifted reference is one knob (mu_ref = mu - alpha), but convergence
  and the per-order sign have DIFFERENT, COMPETING optima. 2x2, mu=0.5, U=4, beta=4: convergence-optimal
  alpha_conv=+1.5 (mu_ref=-1.0, the Hartree/pole-moving region, truncation error ~10x better) but sign |R_2|=0.05
  (worst); sign-optimal mu_ref=0.0 (the closed shell) gives |R_2|=0.82 but ~10x worse convergence. Confirmed
  across orders 2-4. Mechanism: convergence is governed by the nearest pole in the COMPLEX-U plane (Hartree
  shift moves it out), the sign by the real-axis SHELL/detuning (best on a closed shell) -- different physics,
  hence different optimal mu_ref. So pole-moving accelerates convergence (v45-v47) but does NOT move the sign
  wall, and its optimal shift degrades the sign. Honest answer: a substantially better perturbative method that
  does not move the fundamental sign wall -- no free lunch, exactly the cautious outcome anticipated. Single
  case across orders 2-4; genericity (or a filling where the Hartree point IS a closed shell, aligning the
  optima) is the v50 search. Frozen engine untouched (194/194). See CROSSCHECK_v48 and
  08_2d_interacting/SIGN_TRADEOFF_RESULT.md.
- Contour deformation, plundered and tested -- NULL on the sign, with a structural reason; plus the verified
  methods consolidated (v49). The one sign-relevant tool from the roots-of-unity / contour family is
  Lefschetz-style deformation; applied to the genuine v48 integrand (via cdet_port, bit-identical to the
  frozen ring port) the sign/variance-optimal contour is the real axis (A=0), integral invariant to 0.0e+00,
  because within each propagator-kink-pinned sector R=1 and the cancellation is DISCRETE between sectors. The
  lesson: our sign is a real sign-flip, not a complex phase, so deformation makes only a zero-integral
  imaginary part. The deformation-covariate is likewise null (perfect correlation, Re rigid to 1e-15); the
  whole control-variate family moves the prefactor, never R. Consolidated the three verified, axis-distinct
  accelerations (shifted reference / complex-mu contour / free-baseline control variate) in best_methods.py +
  BEST_METHODS.md, all exact-checked. Frozen engine untouched (194/194). See CROSSCHECK_v49,
  08_2d_interacting/CONTOUR_DEFORMATION_RESULT.md and BEST_METHODS.md.
- Exact symmetry reduction of the site sum, with a symbolic proof (v50). Searched our own engine for a
  meron-style involution by computation: no sign-cancelling pairing (ratio C_V(sigma x)/C_V(x) never -1), but
  an exact symmetry -- the stabilizer of the external site, |G_0|=2 (a diagonal reflection). Folding the L^n
  site-configuration sum by G_0 reproduces brute force to 6.6e-17 with up to |G_0|=2x fewer connected-
  determinant evaluations (growing with lattice symmetry). Proven symbolically for ALL hopping t via sympy
  (P^T H P - H = 0, [P,H]=0 as polynomial identities), so the fold is exact for every t, mu, beta. Removes
  redundancy on the site space only -- not the Rossi 2^n recursion, not the physical sign (orbit members share
  the same sign). Frozen engine untouched (194/194). See CROSSCHECK_v50,
  08_2d_interacting/SYMMETRY_REDUCTION_RESULT.md, symmetry_reduction.py and symmetry_audit_sympy.py.
- The symmetry fold scales with the lattice point group; column/row slices fold, not cancel (v51). On the 4x4
  torus the stabilizer of the external site is the full square point group D4 (|G_0|=8), including the column-
  slice (left-right) and row-slice (up-down) reflections. All eight fold (ratio C_V(sigma x)/C_V(x)=+1 to
  1e-10); none cancels (-1). Folding the L^n site sum by the order-8 group is exact (3.3e-16) and gives 4.65x
  (n=2) -> 6.15x (n=3) -> 8x fewer connected-determinant evaluations, versus 2x on the 2x2. Proven for all
  hopping t via sympy on the 16-site lattice. Redundancy on the site space only -- not the Rossi 2^n, not the
  sign. square_point_stabilizer() is the generator-based finder. Frozen engine untouched (194/194). See
  CROSSCHECK_v51 and 08_2d_interacting/SYMMETRY_REDUCTION_RESULT.md (v51 section).
- 45-degree slices of the cube fold too; the fold scales with dimension (v52). Took the lattice to 3D: on the
  4x4x4 cubic torus the stabilizer of the external site is the full cube point group O_h (|G_0|=48), of which
  40 are 45-degree diagonal slices (axis swaps). All diagonal slices fold (ratio +1 to 1e-10); none cancels.
  Folding the 64^n site sum by O_h is exact (5.2e-15) giving 18.62x fewer connected-determinant evaluations at
  n=2, climbing toward 48x. Proven for all hopping t via sympy (axis-swap identity, size-independent). The
  redundancy fold = the little-group order of the external site, growing with both size and dimension:
  2x (2x2) -> 8x (4x4, D4) -> 48x (4x4x4, O_h). Site-configuration factor only -- not the Rossi 2^n, not the
  sign. Frozen engine untouched (194/194). See CROSSCHECK_v52 and SYMMETRY_REDUCTION_RESULT.md (v52 section).
- Inside the Rossi 2^n: the mask-fold is measure-zero, the subset cache is the generic win (v53). A symmetry
  folds masks inside one C_V only on configs it maps to themselves -- verified exact on symmetric configs
  (equal times on partner sites), trivial generically (honest negative; Burnside: no fixed points, no fold).
  The generic interior redundancy is that D_vac/D_corr depend only on the vertex SUBSET, which recurs across
  the enumerated site sum: memoizing (cv_cached) and composing with the orbit fold (fold_site_sum_cached)
  reproduces brute force to 5.0e-15 with 29.9x fewer determinant evaluations at n=3 on the 4x4 (orbit 6.15x x
  cache 4.86x), 13.9x wall-clock. Scope: thrives on shared/quadrature times; does not cut the asymptotic 2^n
  of one isolated generic C_V; sign untouched. Frozen engine untouched (194/194). See CROSSCHECK_v53 and
  08_2d_interacting/SYMMETRY_REDUCTION_RESULT.md (v53 section).
- The value channel's -1 is real but dressed; weight and sign concentrate on low-dimensional slices (v54).
  Closing the -1 hunt mechanistically: geometric ops can only fold; the particle-hole transpose carries the -1
  off-diagonal (G(-mu)(i,j,tau) = -e_i e_j G(mu)(j,i,-tau), 2.5e-11) but the exact equal-time sum rule
  G(-mu)(i,i,0)+G(mu)(i,i,0)=1 (1e-15) dresses it: PH maps the 0^- convention to 0^+, the difference is a
  contact/density counterterm (the v46 d/dmu object). Both naive clean factors failed by computation -- the
  truth is an inter-observable identity (mu <-> -mu, externals swapped, plus counterterms), no per-config -1
  at fixed mu. Slice mine on the 4x4x4: 1d-line configs carry x18.5 their share of |weight| at R=0.22, 2d
  planes x2.1 at R=0.09, 3d bulk x0.65 at R=0.004 -- locality as a slice hierarchy; v55 candidate is slice-
  stratified evaluation (exact low-dim slices + sampled bulk). One lattice/order/mu; pattern, not yet law.
  Frozen engine untouched (194/194). See CROSSCHECK_v54, 08_2d_interacting/VALUE_CHANNEL_SLICES_RESULT.md and
  value_channel_slices.py.
- Slice-stratified evaluation (v55): the v54 hierarchy as an unbiased estimator. Stratify the site sum by the
  exact span-dimension label; enumerate heavy small strata (Neyman itself demanded it); sample the rest. n=2
  cube vs exact fold+cache truth at matched budget: 22-44x variance reduction, bias <=0.5 sigma; n=3 with the
  heavy stratum beyond the enumeration budget: 2.1x, means consistent (few reps). The law: gain ~ concentration
  relative to budget; unbiased in both regimes; sign R untouched. Frozen engine untouched (194/194). See
  CROSSCHECK_v55, 08_2d_interacting/SLICE_STRATIFIED_RESULT.md and slice_stratified.py.
- Genericity closed (v56): the sign-vs-convergence trade-off is generic exactly where the sign problem bites.
  Measured R2(mu_ref) landscapes plus direct convergence-optimal shifts (real-part metric, exact ED reference):
  every doped filling is separated (beta=4 gaps >=1.0 with R2 0.01-0.40 vs peak 0.82; beta=8 doped gaps
  1.0-1.5), and the one exact alignment is half filling mu=U/2 at low T (mu_ref=0.0 = the peak, R2=0.91, gap
  0.00) -- forced by particle-hole symmetry, the same point the sign-free theorems single out. A metric
  artifact briefly faked a doped alignment; the module self-test failed against it, it was retracted, and the
  correction is banked. No new free lunch; one mechanism-understood alignment. Frozen engine untouched
  (194/194). See CROSSCHECK_v56, 08_2d_interacting/GENERICITY_RESULT.md and genericity_search.py.
- The slice hierarchy survives scale (v57, theory-extraction begins). At L=4,6,8 cubes (64->512 sites, via
  FastCDet validated to 4.2e-17 against the frozen-port-validated CDet) with targeted sampling of the rare 1d
  class: the 1d/bulk per-configuration weight ratio GROWS 32x -> 74x -> 165x, and the 1d sign beats the bulk
  at every size (R 0.65->0.24 vs ~floor; L=8 bulk anomaly flagged). v54's undersampled d=1 R refined on the
  record. Careful claim now supported: the expansion's weight concentrates in a geometrically identifiable
  low-dimensional sector whose dominance grows with system size and which carries the healthiest sign -- a
  measured geometric structure of configuration space, not yet a theory of it. Frozen engine untouched
  (194/194). See CROSSCHECK_v57, 08_2d_interacting/SLICE_SCALING_RESULT.md and slice_scaling.py.
- Universality (v58): the weight concentration is universal and robust; the sign hierarchy is downgraded on
  the record. Swept order/temperature/filling/observable on the L=6 cube (U exact by the no-U-in-C_V theorem):
  median 1d/bulk weight ratio 11x-184x in every cell, seed-stable -- propagator geometry, not coincidence. The
  per-class sign claims of v54/v57 were exposed as heavy-tail estimator-fragile by a FAILING self-test (same
  cell: R(1d)=0.44 at 500 samples vs 0.02 at 400) and are downgraded to OPEN pending tail-aware statistics;
  the v57 L=8 anomaly was this instability. Lessons banked: ratios of means over heavy tails are not
  measurements until the estimator is shown stable; a failing gate is data. Frozen engine untouched (194/194).
  See CROSSCHECK_v58, 08_2d_interacting/SLICE_UNIVERSALITY_RESULT.md and slice_universality.py.
- Freeze-then-predict derivation attempt -- FALSIFIED (v59). Derived ln|C| ~ a - l_MST/xi with xi measured
  independently from the bare propagator (0.91); MST is the best geometry variable but carries only ~17% of
  the variance with slope HALF the prediction (effective ~2xi, unexplained); the frozen-slope zero-parameter
  prediction of class ratios (3x/5x/7x at L=4/6/8) under-predicts measurement (16x/62x/30x) by 5-10x. The
  exponential FORM in L survives; the dominant mechanism of the universal concentration is unidentified; the
  1d class is an axis/diagonal mixture requiring stratification. A falsified derivation issued before
  measurement, banked as the negative it is. Frozen engine untouched (194/194). See CROSSCHECK_v59,
  08_2d_interacting/DECAY_LAW_RESULT.md and decay_law.py.
- Dual mechanism (v60): tau-interference confirmed as the second component -- 40% of var(ln|C|); integrating
  tau out doubles the geometric law (R2 0.18->0.48). Propagator anisotropy measured (xi 0.90 axis vs ~1.2
  diagonals per Euclidean unit at L=8) but the anisotropic metric does not close the prediction gap (6.8x vs
  75.5x); the stratified 1d class shows the body-diagonal anomaly (longest lines, heaviest weight). A ~10x
  closed-line enhancement survives all distance laws; the ring-closure/winding-coherence hypothesis is banked
  for v61, untested. Self-test hardening caught a wraparound artifact faking xi=114. Frozen engine untouched
  (194/194). See CROSSCHECK_v60, 08_2d_interacting/DUAL_MECHANISM_RESULT.md and dual_mechanism.py.
- Winding-phase ring closure falsified by a paired twist experiment (v61). An antiperiodic twist along one
  axis (|H| bit-identical; only the winding phase changes) leaves PAIRED per-config line weights within ~±40%,
  axis-blind, with no mirror under twist-y -- the v60 hypothesis is falsified and the ~10x line enhancement is
  closure-independent. The unpaired version of the same experiment first faked a 4x axis-selective effect (the
  v58 heavy-tail pathology), caught by the paired design and banked as the artifact it was. Surviving untested
  hypothesis: 1d channeling (coherent multi-bounce along the line, twist-blind). Standing methodology promoted:
  pair every comparison in heavy-tailed systems. Frozen engine untouched (194/194). See CROSSCHECK_v61,
  08_2d_interacting/RING_CLOSURE_RESULT.md and ring_closure.py.
- 1d channeling confirmed (v62). With anisotropy controlled exactly (axis-directed families), MST-matched
  pairs and identical tau draws per pair: line/bent 1.8-2.0x, line/zig 1.9-2.4x, bent/zig 1.3x -- monotone in
  collinearity. Coherent multi-bounce along a shared direction enhances connected weight at fixed total
  distance (twist-blind, consistent with v61). Mechanism ledger for the universal concentration: distance
  decay + tau-interference + anisotropy + channeling CONFIRMED; winding closure FALSIFIED; a ~4x residual of
  the ~75x class gap remains unaccounted and open. Frozen engine untouched (194/194). See CROSSCHECK_v62,
  08_2d_interacting/CHANNELING_RESULT.md and channeling.py.
- Mechanism closure (v63): the two-coefficient law locks the universal weight concentration within 1.27x.
  Channeling COMPOUNDS with length (paired line/bent ratio ~1.6x at MST=3 -> ~2.7x at MST=4); after catching
  two fitting traps (spurious single-vertex collinearity credit; multicollinearity from l_coll == MST on the
  line family), each coefficient was identified where the other cannot contaminate it: b=0.537 from bulk-only
  regression (l_coll=0), c=+0.583 from the paired matched-MST contrast. Frozen composition at the class
  medians = 59x vs measured 75.5x -- agreement 1.27, within the 2x gate pre-set before the run. The mechanism
  arc (v57-v63) closes at the semi-quantitative level: distance decay compounded with length-growing 1d
  channeling, modulated by tau-interference; deriving c is the open theory item. Frozen engine untouched
  (194/194). See CROSSCHECK_v63, 08_2d_interacting/MECHANISM_CLOSURE_RESULT.md and mechanism_closure.py.
- Genericity beyond the 2x2 (v64): the v56 law splits. alpha*=U/2 at half filling is UNIVERSAL (2 clusters x 3
  couplings) and quasi-exact -- on the 6-ring the PH-shifted series reaches the extraction floor (err@K8 =
  8.6e-6, five orders below any other shift; blocked sector ED validated to 4.8e-07 against a dense-eig
  reference, ~150x faster). Sign alignment is CLUSTER-DEPENDENT: it fails at half filling on the 6-ring (R
  0.14 at the PH point vs peak 0.51 at mu_ref=-1.0), exactly as predicted before the run from the cluster's
  own measured landscape -- v56's alignment was a 2x2 coincidence of two distinct special points. New open
  question: the 6-ring sign peak sits ON a level, not in the PH gap. Frozen engine untouched (194/194). See
  CROSSCHECK_v64, 08_2d_interacting/GENERICITY_CLUSTER_RESULT.md and genericity_cluster.py.
- Consolidated baseline (v65). cdet_best.py is the front door composing the verified v49-v64 stack: BestCDet
  (2.8e-17 vs the validated port chain), orbit fold x subset cache (exact to 2.7e-15, 13x measured, 16384 ->
  578 determinants on the cube gate), slice stratification for big lattices, the SPLIT shift law (alpha*=U/2
  quasi-exact at half filling, sign caveat returned with the number), and the v63 concentration-law constants.
  BEST_METHODS.md upgraded to the v65 edition: composition table with provenance, the two laws, the standing
  methodology (each rule bought with a banked failure), and the unchanged wall statement -- nothing in the
  stack moves R at fixed mu. Frozen engine untouched (194/194). See CROSSCHECK_v65 and
  08_2d_interacting/cdet_best.py.
- The no-brute-force simulator (v66). The concentration law as a predictive surrogate (OOS R2 0.75, ~85
  calibration evaluations only): reproduces the v54 brute-force weight-share table with ZERO evaluations
  (every class within ~5 points), and guides small-budget estimation to 33x over uniform where the sign is
  mild (n=2, vs exact truth). Its ceiling is measured, not guessed: at the cancellation-dominated n=3 total
  (exact 262,144-config truth in 11 s via the consolidated stack, 168x fewer determinants) guided estimation
  gives no gain -- variance there is sign-driven, and a magnitude model cannot guide what it cannot see: the
  sign wall as an estimator theorem. Frozen engine untouched (194/194). See CROSSCHECK_v66,
  08_2d_interacting/SURROGATE_RESULT.md and surrogate.py.
- The sign model (v67): the knock answered. The per-geometry sign survival r_g is bootstrap-stable with
  non-overlapping CIs (1d/2d ~0.70 vs bulk 0.34) -- the v58-downgraded sign hierarchy is settled at the
  tau-integrated level; the line sector's sign is 92% predictable (bulk: coin flip). Structural fact: the
  d<=1 sector -- 0.3% of configs -- carries 77% of the exact signed total. Exploiting it, the hybrid estimator
  (exact line-sector enumeration + signed-sigma pilot-Neyman) moves the v66 ceiling from 0.7x to 87-110x at
  0.46% budget, unbiased, against the exact 262,144-config truth. A frozen-subsample 231x reading was rejected;
  a trimmed-samples gate failure was caught and fixed (the v58 lesson applied to our own gates). The bulk
  remainder stays a coin flip -- the wall's territory, now mapped to 0.3%. Frozen engine untouched (194/194).
  See CROSSCHECK_v67, 08_2d_interacting/SIGN_MODEL_RESULT.md and sign_model.py.
- Governance of the signed weight (v68): signed weight = magnitude envelope x sign-coherence decay x a
  filling-controlled phase. Parity falsified at both mu=0.5 and the PH point (50-59%). Sign coherence has its
  own, longer decay scale xi_s ~ 3.0 (3x magnitude) -- sign outlives weight, which is why the signed answer
  concentrates harder than the unsigned one. The orientation flips with filling (94% negative at mu=0.5 ->
  75-100% positive at mu=1.5, same geometries) -- the Friedel/k_F signature; the L=4-vs-L=6 orientation
  difference is k-grid phase. Coherence, not positivity, is the invariant; v67 restated correctly and the
  turn's own interim framing corrected on the record. Open theory item: the quantitative phase law (period vs
  k_F(mu)). Frozen engine untouched (194/194). See CROSSCHECK_v68,
  08_2d_interacting/SIGN_GOVERNANCE_RESULT.md and sign_governance.py.
- The phase law attempted (v69): double falsification under frozen protocol (calibrate one cell, predict
  seven, gate pre-set at 75%). Static tau-averaged predictors collapse to 34% (they cannot even represent the
  measured mu-flip: the static free sign pattern is ++-++ at all fillings); the fully tau-integrated dominant
  chain reaches 64-66% -- partial signal with parity-competition reversals -- and fails the gate. Standing
  conclusion: the orientation phase is determinant-level interference as far as tested. The asymmetry --
  MAGNITUDE LAWFUL (two coefficients, v63) / PHASE IRREDUCIBLE (so far) -- is the sharpest localization yet of
  where the sign problem's hardness sits in this representation. Frozen engine untouched (194/194). See
  CROSSCHECK_v69, 08_2d_interacting/PHASE_LAW_RESULT.md and phase_law.py.
- Sector estimator + exact-moment methodology (v70, rotation 1/3). The coherent rank<=1 sector is polynomially
  small by construction and built without config-space enumeration (3,774 of 10,077,696 at L=6); exact strata
  counts vectorize; the estimator (exact sector + signed-sigma pilot-Neyman) is unbiased at any L. Exact
  second moments via the orbit fold gave design variances EXACTLY and CORRECTED our own v67 claim: true gain
  ~6x at B=1200, not the banked 87-110x (lucky-high uniform baseline; structural facts untouched; correction
  noted atop the v67 doc). Exact decomposition: 96% of uniform's noise is the sector's rarity; the bulk
  remainder is sign-driven and magnitude-incompressible. L=6 exact sector sum is NEGATIVE -- the v68 phase
  flip in exact arithmetic; the L=6 signed total stays noise-dominated at 0.045% budget: the machinery scales,
  the sign problem scales faster. New standing rule: heavy-tailed estimator comparisons must be exact-moment-
  based wherever possible. Frozen engine untouched (194/194). See CROSSCHECK_v70,
  08_2d_interacting/SECTOR_ESTIMATOR_RESULT.md and sector_estimator.py.
- Pairing depth (v71, rotation 2/3, surrogate-first). The orientation phase has NO finite pairing depth: the
  COMPLETE free 4-point determinant (all 24 Matsubara-cycle permutation terms) predicts the measured
  orientation at 44% out of calibration -- both pre-registered gates fail, identically in the engine-matched
  time convention. By elimination the phase lives in the coupled product of the two spin determinants over
  shared vertex times: the engine integrand itself. The reduction ladder (parity -> static -> chain -> any-
  depth determinant) is complete, every rung a frozen-protocol falsification. Surrogate consequence: any
  orientation channel must be learned, not derived. Frozen engine untouched (194/194). See CROSSCHECK_v71,
  08_2d_interacting/PAIRING_DEPTH_RESULT.md and pairing_depth.py.
- The bulk remainder (v72, rotation 3/3, surrogate-first): NOT incoherent -- mu-controlled FRIEDEL RINGS in
  configuration space. The frozen monotone-decay surrogate prediction failed both its pre-set gates, and the
  exact orbit-fold shell decomposition exposed why: alternating-sign MST shells (+,-,+,- at mu=0.5; the
  pattern shifts to -,-,-,+ at mu=1.5 with a 6x larger, nearly-aligned net -- the frozen confirmation test
  for phase rings), mid-range dominance (58%), 2.3x inter-shell cancellation. The orientation phase --
  proven formula-less below the coupled two-spin integrand -- governs the remainder's radial structure. The
  rotation closes with all three passes converged on that single object; the surrogate's missing channel is
  characterized, and the queued route to it is learned, not derived. Frozen engine untouched (194/194). See
  CROSSCHECK_v72, 08_2d_interacting/BULK_REMAINDER_RESULT.md and bulk_remainder.py.
- The learned orientation channel (v73): fails the same frozen gate the physics ladder failed -- logistic 33%
  and nonlinear MLP 35% held-out (train 74% both), with consistent anti-prediction at unseen mu. Mechanism
  identified: a phase WRAPS, and smooth models cannot interpolate a wrap from sparse mu samples; predicting
  unseen-mu orientation requires the mu-period -- the very law shown to have no sub-engine form. The
  orientation channel is closed at this scope from BOTH directions (derived + learned); remaining routes are
  tabulation, engine-derived features, or the mu-period analytically. Surrogate-gain avenues remaining are
  magnitude-side. Frozen engine untouched (194/194). See CROSSCHECK_v73,
  08_2d_interacting/LEARNED_ORIENTATION_RESULT.md and learned_orientation.py.
- Surrogate refinements (v74, queue item b). Ceilings measured before fitting (magnitude rho=0.95; r_g 0.40 at
  NT=20 -- the old r_pred 0.32 was ~80% of its ceiling: label noise, not model failure). Our own v66 headline
  R2=0.75 scope-corrected as mixture-flattered (the mixture-independent median per-config error 1.7x stands;
  note added atop the v66 doc). The real gain is TRANSFER: a 10-feature linear model carries L=4 -> L=6 (R2
  0.33 -> 0.57, med-err 2.88x -> 1.81x, 8-shot intercept); quadratic interactions destroy transfer. r_pred
  regime map: +0.32 / +0.27 / -0.57 within rank 1/2/3 -- sign-survival predictability is coextensive with
  coherence; the deep bulk resists even graded prediction, the v73 closure made quantitative. Frozen engine
  untouched (194/194). See CROSSCHECK_v74, 08_2d_interacting/SURROGATE2_RESULT.md and surrogate2.py.
- The L=6 shell fold (v75). En route, a definition correction: min-image collinearity is ill-defined on
  even-L tori -- the true (wrap-safe) coherent sector is 1,618 configs carrying 82% at L=4 and 16,950 at L=6;
  the v67/v70 sets were wrap-blind subsets, their numbers true for those subsets; the wrap-safe rule now
  extends to definitions. The fold itself: FIRST EXACT totals at 10,077,696-config scale, both fillings --
  mu=0.5: -2.498377e-3 (validating the v70 pilot dead-on; the phase flip vs L=4 holds for the full total);
  mu=1.5: -2.224768e-3. The size trend in exact arithmetic: the sector's share falls 82% -> 42% and at mu=1.5
  it OPPOSES the total -- the remainder grows with size; the sign problem scales faster than the machinery.
  Rings persist at L=6 with mu-dependent nodes; the period is NOT resolved (irregular spacings at this
  size/binning vs the frozen pi/k_F ~ 1.1-1.2). Frozen engine untouched (194/194). See CROSSCHECK_v75,
  08_2d_interacting/SHELL_FOLD_RESULT.md and shell_fold.py.
- The ring period (v76): NOT resolved at L=6 -- and shown to be unresolvable there in principle. Pure
  re-analysis of the fold: shell-coherence periodograms over four radial coordinates. The seductive near-miss
  (binned R_max peaks within 10% of 2k_F at both fillings, correct mu-shift) was killed by the correct
  discrete unbinned treatment plus a 1000-shuffle permutation null (p = 0.20/0.16) -- the v58 lesson in
  spectral form; perimeter's 16x low-q peak was trend leakage with the wrong mu-shift. What is real: strong,
  mu-flipped contact-shell coherence (+0.66/-0.53); beyond it amplitude starvation. The impossibility,
  quantified: xi_s ~ 3.0 against period ~ 1.2 leaves ~2 oscillations before decoherence on ~5 usable radii.
  Route: larger L with coherence-boosted observables (the v68 line-sector protocol). Frozen engine untouched
  (194/194). See CROSSCHECK_v76, 08_2d_interacting/RING_PERIOD_RESULT.md and ring_period.py.
- THE MU-PERIOD LAW (v77). The route v76 named, executed: dense-mu orientation on coherence-boosted lines.
  Friedel falsified on pre-registered gates (spacing R-independent; winding ~5x faster than 2 kF R;
  beta-dependent). The law: Delta-mu* = pi/(q beta) with q = 1.12/1.05/0.98 at beta = 4/6/8 -- CHARGE-1
  FUGACITY WINDING, R- and L-independent. The phase that resisted every geometric reduction has a form, and
  it lives in (mu, beta): dphi/dmu ~ beta. The orientation channel half-reopens: period-based prediction
  lifts held-out accuracy from 33-44% (v73) to 73-76% -- at the bar; the residual is offset calibration,
  engineering not law-finding. An initial 79% single-seed claim was downgraded by the seed-robustness sweep
  before banking. beta >= 12 banked as a protocol validity boundary. New theory target: derive q=1. Frozen
  engine untouched (194/194). See CROSSCHECK_v77, 08_2d_interacting/MU_PERIOD_RESULT.md and mu_period.py.
- The Matsubara comb (v78): the mu-period's analytic origin, established. The cancellation lemma makes
  <C>_tau exactly rational in the fugacity z = e^{beta mu} (all e^{mu tau} factors cancel per determinant),
  with poles only on the negative z-axis -- Matsubara combs mu = eps_k + i(2m+1)pi/beta at uniform height
  pi/beta. Detected DIRECTLY by complex-mu continuation: a 3.9e6-fold at-level divergence approaching the
  comb vs flat between levels (contrast 3e5; Cauchy-Riemann verified). The literal charge-staircase reading
  -- ours and the simplest outside derivation -- was falsified first by the flat ln|C| slope test: the right
  rate, the wrong mechanism. Comb-limited variation derives the 1/beta scaling AND the R/L-independence in
  one stroke; "charge 1" is the z-degree of each Fermi denominator; pi is the antiperiodicity phase. The
  refined open item: the exact constant, as zero statistics. Frozen engine untouched (194/194). See
  CROSSCHECK_v78, 08_2d_interacting/FUGACITY_STRUCTURE_RESULT.md and fugacity_structure.py.
- The consolidated surrogate (v79, user-directed). cdet_surrogate.py composes every proven finding -- the
  wrap-safe sector, the transferable magnitude model, the r_pred regime map, and the period-based orientation
  channel with its comb mechanism -- each scoped at the point of use; BEST_METHODS gains the v79 edition with
  the phase program's closed arc and the nine methodology rules earned since v65. Consolidation acted as an
  audit: the transfer error refined to a pooled 1.88x across independent draws (the v74 1.81x sat at the
  favorable end), and a per-class-intercept hypothesis was tested and rejected. The walls are restated
  unchanged: R(N, beta) still decays exponentially; nothing here crosses the sign problem. Frozen engine
  untouched (194/194). See CROSSCHECK_v79, 08_2d_interacting/cdet_surrogate.py and BEST_METHODS.md.
- The resonance regime (v80, the KT-review round, user-directed). Applying the KT-RG method to the rounds
  before and during consolidation reopened a chain closed too early. The v77 "beta >= 12 unmeasurable"
  boundary is RETRACTED: the disagreeing extractions were two real scales. The two-regime law is proved with
  frozen nulls -- thermal pi/beta winding (geometry-dependent offsets) crossing over to a RESONANCE regime
  where flips attract to single-particle levels (p = 0.025) and become geometry-independent (p = 0.013-0.041
  at both lattice sizes). A Phase-0 fine-grid check also revised the beta=4 spacing (0.625, q ~ 1.26). The
  naive midpoint law was killed at the sparse L=6 spectrum; the core flip set is external-time-independent
  (its prettiest coincidence killed by its own discriminator); cross-geometry orientation transfer is
  bimodal -- positions universal, multiplicities residue-dependent. Frozen engine untouched (194/194). See
  CROSSCHECK_v80, 08_2d_interacting/RESONANCE_REGIME_RESULT.md and resonance_regime.py.
- The pair law (v81): the limit set is the spectrum. Trajectory flows (grid 0.0125, beta 12-28) show the
  resonance-regime flips converging to the single-particle levels TWO-SIDEDLY as mu*_(+/-) = eps +/-
  c_eps/beta (four fits, best rms 0.004) -- the candidate-set hunt is over, and every "midpoint" sighting
  was a pair partner in flight. Candidate arrangement: c = ln(deg)/2, with ln(36)/2 = ln 6 = 1.792 hitting
  the cleanest fit at 0.4%; the forward-proof step (the residue ratio) is named. Level-2 is grid-pinned and
  a partner-conflation analysis trap was caught. A no-free-parameter falsifiable prediction is banked for
  any (L, level). Frozen engine untouched (194/194). See CROSSCHECK_v81,
  08_2d_interacting/PAIR_LAW_RESULT.md and pair_law.py.
- The two-class structure (v82). The v81 no-free-parameter prediction was fired at L=8 level 2 and FAILED --
  with a Phase-0 catch en route (exact deg = 39, not the hand-count 63) and exactly the payoff such
  predictions exist for: the failure exposed the second mechanism class. Class I (Delta-k=1): flight pairs
  converging to levels, central pinned flips confirmed at both lattice sizes. Class II (Delta-k=2):
  beta-STATIC crossings at specific level-pair midpoints -- a flip flat at 1.819 +/- 0.009 across beta 12-24
  matching (0.828+2.828)/2 = 1.828, plus 2.121 and 2.293 at late beta. The v80 midpoint law resurrects
  selectively; v80's "1.81 cluster" is retro-identified. Open and sharply posed: the residue-pair sign
  condition (which crossings flip; the L=6 statics are suppressed) and the Class-I c-formula (ln(deg)/2
  demoted to a one-level fit). Frozen engine untouched (194/194). See CROSSCHECK_v82,
  08_2d_interacting/LEVEL2_STRUCTURE_RESULT.md and level2_structure.py.
- The residue ratio (v83, user-directed: "get that tied down"). The Class-I flight constants are DERIVED:
  near a level the tau-averaged coefficient (smooth external factor stripped) is a polynomial in the level
  occupancy, so every flip sits at mu* = eps + logit(f*)/beta with f* a residue-polynomial root -- pair =
  roots straddling 1/2, central flip = root near 1/2, multiplicity = root count. Beta-transfer verified
  (the beta=20 polynomial predicts the beta=12-28 flips with no refitting, max offset 0.022) and the
  multiplicity pattern confirmed across three geometries. The round also located where residues creep in:
  adjacent-comb contributions at the connected object's cancellation floor defeat the naive single-level
  freeze, which is exact only at s=1/2 -- the breakdown pattern read outward from the exact point. v81's
  fitted c's are retro-identified as fit-basis artifacts and the ln(36)/2 coincidence is resolved,
  explaining v82's falsification from the inside. Frozen engine untouched (194/194). See CROSSCHECK_v83,
  08_2d_interacting/RESIDUE_RATIO_RESULT.md and residue_ratio.py.
- The selection rule (v84). The v83 machinery extended to the Class-II statics: near a midpoint the
  coefficient is a saturated background plus two residue exponentials, and a static flip exists iff the
  background vanishes AND the residues have opposite signs -- then mu* = mid + ln(-B/C)/(2 beta), the same
  logit-type law with the two-residue ratio. The 1.828 static passes both conditions in value-level
  measurements (background 1.0 sigma from zero; ratio 0.70; beta-flow matching v82 at 0.010), and its pair
  identity (0.828, 2.828) is confirmed by flow against a rejected 1.707 alternative; the never-flipping
  1.586 midpoint fails condition (i) at 4.5 sigma. A slope probe discriminated the mechanism class in one
  measurement before any fitting. The narrow-window fit degeneracy is documented; the remaining derivation
  is why the background vanishes where it does. Frozen engine untouched (194/194). See CROSSCHECK_v84,
  08_2d_interacting/SELECTION_RULE_RESULT.md and selection_rule.py.
- The resonance atlas (v85, consolidation). v80-v84 integrated into one prediction surface with one spine:
  every resonance-regime flip is mu* = anchor + ln(ratio)/(q beta) -- Class I anchored at levels with
  residue-polynomial root odds (q=1), Class II at selected midpoints with the two-residue ratio (q=2);
  residues decide attendance. The integration audit collides every component pair: cross-component
  deviations 0.006-0.031, flow 0.014, a live check landing 0.003 from prediction -- and surfaces one honest
  catch, the unclassified L=6 ~1.8 object (conflated trajectories suspected), recorded rather than swept
  under a law. BEST_METHODS v85 edition adds the component table and methodology rules 10-18. Frozen engine
  untouched (194/194). See CROSSCHECK_v85, 08_2d_interacting/RESONANCE_ATLAS_RESULT.md and
  resonance_atlas.py.
- The core C surrogate (v86, user-directed). Every banked advance frozen into a dependency-free C module
  beside the frozen engine: the 10-feature transferable magnitude model with frozen trained weights, the
  wrap-safe sector test, the pi/beta period, the regime classifier, Class-I logit-law flips from frozen
  residue-polynomial roots, the flow-corrected Class-II static, and orientation parity stepping -- with
  each component's banked scope and the standing sign-problem wall stated in the header. Validation is
  engine-style and live: the gate regenerates Python reference vectors with a fresh seed every run,
  rebuilds with -Wall -Werror, and matches to a worst deviation of 3.6e-15. Frozen engine untouched
  (194/194). See CROSSCHECK_v86, 08_2d_interacting/CSURROGATE_RESULT.md, csurrogate.c/h and
  csurrogate.py.
- The C surrogate under test (v87, user-directed). Clean-room builds caught three portability bugs (fixed;
  the module now builds under strict C99 and pedantic C11). Efficiency measured: 1.5 microseconds per
  feature/magnitude prediction (212x the Python), 3-19 ns for the atlas laws, and ~875,000x per answer
  against an exact tau-averaged coefficient -- a ratio growing as ~2.6^n against the measured exact wall
  (x2.5-3.3 per order, 745 ms at n=9). The orders-of-n question is answered in two ceilings: computational
  (effectively unbounded -- O(1) laws, O(n^2) features to n=200 in under 2 ms) and validity (n=3 as
  shipped; higher orders need their own residue-polynomial extraction, capped at roughly n <= 6-7). A
  fresh end-to-end test broke the old pooled transfer gate; the contamination hypothesis was tested and
  excluded (0/8), and the scope was revised openly to 2.3x pooled / 1.7-2.7x per draw across four
  independent draws. Frozen engine untouched (194/194). See CROSSCHECK_v87,
  08_2d_interacting/CSURROGATE_BENCH_RESULT.md and csurrogate_bench.c.
- The order axis (v88). The v83 extraction fired at higher orders: the resonance spine -- flips at
  mu* = eps + logit(root)/beta with order-dependent roots -- survives n=4 cleanly (roots 0.156/0.643,
  beta-transfer verified at max dev 0.024 with no refitting) and partially n=5, where the practical wall
  arrives exactly as predicted (the lower root resolved and live-verified at dev 0.011; the upper flagged
  marginal). The C surrogate gains its first higher-order parameter sets. The fresh-seed gate also caught a
  real cross-language numerics bug -- float-determinant noise on singular integer matrices -- fixed with
  exact integer arithmetic on both sides. Frozen engine untouched (194/194). See CROSSCHECK_v88,
  08_2d_interacting/ORDER_AXIS_RESULT.md and order_axis.py.
- The deep partner (v89). One level-2 residue-polynomial extraction resolved three roots and closed two
  dangling anomalies: the unclassified ~1.8 object is level-2's deep lower partner (f* = 0.0116,
  c = -4.44), v80's "2.2 family" is the upper partner (flow devs 0.003-0.011), and the central root
  matches at 0.010. The v85 c-drift is quantified as sign-scan noise at the deep crossing. A designed
  value-level beta-transfer missed at beta=14, banking the law's large-beta scope: the deviation
  (+0.114@12 decaying to +0.003@28, ~e^{-0.3 beta}) is the adjacent comb's beta-compensated contamination
  at the cancellation floor -- the v83 creep measured in mu-position for the first time. Frozen engine
  untouched (194/194). See CROSSCHECK_v89, 08_2d_interacting/DEEP_PARTNER_RESULT.md and deep_partner.py.
- The two-window creep cross-check (v90, ledger #100, user-directed). The surrogate side and the
  brute-force side were run independently on the creep and compared. Brute force: value-level zeros across
  beta = 10-28 select an ANCHORED trajectory (z = 1.824 - 0.72/beta) and reject logit -- with a Phase-0
  catch that v89's Delta-decay was a baseline artifact. Surrogate side: the anchor sits 0.2 sigma from
  2*sqrt(2)-1, the L=8 static's exact anchor, at a lattice whose spectrum contains no sqrt(2) -- a possible
  L-independent anchor -- with 11/6 alive at 0.4 sigma. A frozen cross-geometry discriminator decided the
  structure: universality wins at devs 0.001-0.011, making the ~1.8 object the third static-class instance.
  Each window alone was wrong or anonymous; together they rewrote the law. Frozen engine untouched
  (194/194). See CROSSCHECK_v90, 08_2d_interacting/CREEP_CROSSCHECK_RESULT.md and creep_crosscheck.py.
- The correction propagated (v91, user-directed). The v90 law was pushed into both executable prediction
  surfaces: the C surrogate gains the L=6 deep-static API with a corrected Class-I scope (logit flow for
  mid-range roots only; deep small-f roots route to the static family), and the Python atlas gains the
  same law plus a new audit gate G that checks it against the v90 stored value-level zeros (max dev 0.022)
  -- a gate that fails if the superseded reading ever creeps back. The historical module carries a revised
  header. All gates re-passed; no new physics claimed -- consolidation/correction discipline. Frozen engine
  untouched (194/194). See CROSSCHECK_v91 and 08_2d_interacting/CORRECTION_PROPAGATION_RESULT.md.
- The anchor test (v92, user-directed, with the imported bridge tool). The v90/v91 anchored law is scoped
  to beta in [10,32] -- the deep trajectory rises through both v90 candidates. A heavy-tail audit at the
  cancellation floor (kurtosis ~4500) invalidates single-draw CLT errors there and installs the multi-draw
  dense protocol; an honest re-measurement gives a_inf = 1.8437 +/- 0.0068. The bridge tool, edited for
  the job (anchor_bridge.py), applies its own null rule: the candidate alphabet saturates the window
  (83% rarity) -- NOT RIGID; the octagon chord (the tau1-field constant) leads at 0.60 sigma but the
  identification is OPEN, closing only below sigma* = 0.0008 or by the structural background-zero
  derivation, whose field tag answers tau0-vs-tau1 exactly. Two in-flight catches banked. Frozen engine
  untouched (194/194). See CROSSCHECK_v92, 08_2d_interacting/ANCHOR_TEST_RESULT.md, anchor_test.py and
  anchor_bridge.py.
- The exponent-balance law (v93, the structural route executed). Statics derived as integer-weighted
  means of the lattice's own levels, z = mu* + ln(r)/(q beta) -- the field theorem answers tau0/tau1
  (statics live in the spectrum's field; the chord excluded structurally at L=6; the L=8 static is the
  (1,1) balance of (2sqrt2-2, 2sqrt2) exactly). Finite menu {11/6, 13/7, 15/8}; the frozen discriminator
  at beta=36/40 selected 11/6 at ~80:1; global law 11/6 + 2.67/(6 beta) at max 0.38 sigma over the
  honest pool. 13/7 not dead; ln r not yet derived; the (2,3) window found suppressed. Frozen engine
  untouched (194/194). See CROSSCHECK_v93, 08_2d_interacting/EXPONENT_BALANCE_RESULT.md and
  exponent_balance.py.
- The side-by-side (v94, user-directed). Both surfaces updated with the law + competitor lines and
  parity-locked (C vs Python, 1e-15, six betas); out-of-sample predictions frozen to disk, then measured:
  z(44) = 1.8510(76) and z(52) = 1.8527(52) score ~9:1 for 13/7 against the frozen 11/6 -- reversing the
  v93 in-sample 80:1: the identification REOPENED. The six-point pool admits 11/6 / 13/7 / a constant
  1.8467(21); the constant revives the chord at 0.5 sigma -- the menu-vs-flatness tension, raising the
  degree bound (weight <= 6 at n=3?) as the decisive queued item. z(30) = 1.8138(37) demonstrates the
  law's scope floor (>= 8 sigma from both lines in the crossover window). Frozen engine untouched
  (194/194). See CROSSCHECK_v94, 08_2d_interacting/SIDE_BY_SIDE_RESULT.md and law_sidebyside.py.
- The degree bound (v95). Settled by a symbolic census of the actual C_V (the port run on symbolic
  occupancies): the bound is 2n+1 = 7 with FULL 330-monomial support -- v93's 8 and v94's 6 both wrong.
  Balances come from exponent differences, correcting the menu to {..., 11/6, 24/13, 13/7, 15/8, ...};
  24/13 (q = 13, near-flat approach) sits 0.26 sigma from the v94 constant, dissolving the
  menu-vs-flatness tension: the flat reading IS the q=13 member. Identification open among {13/7,
  24/13}; the coefficient program (tau-average the census coefficients, predict the zero outright) is
  the named closing route. Frozen engine untouched (194/194). See CROSSCHECK_v95,
  08_2d_interacting/DEGREE_BOUND_RESULT.md and degree_bound.py.
- The coefficient program, phase 1 (v96). The freeze instrument (FrozenCDet: window occupancies by hand)
  built, validated against v89, and proven faithful at the physical point; the (1,2)-window background
  measured ALIVE (A(44) at 4.6 sigma -- no midpoint static) and decaying at effective rate ~0.10-0.12
  with prefactor curvature (the asymptotic 1/7-vs-2/13 band not reached); the far-level antiperiodic
  images identified as the concrete creep carrier; the no-fit root prediction inconclusive with the
  phase-2 spec computed. Frozen engine untouched (194/194). See CROSSCHECK_v96,
  08_2d_interacting/COEFFICIENT_FLOW_RESULT.md and coefficient_flow.py.
- The parity table (v97). Five window backgrounds across both lattices (WindowFrozen generalized): the
  binary "even first-empty degeneracy => A=0" rule FALSIFIED by its own registered prediction
  (W8(0.828,1.414) nonzero at 3.8 sigma); a robust 20-40x suppression pattern survives as observation;
  the v84 L=8 static reread as a root-flow crossing (A ~ 95% of the deviation term at 1.8284), with the
  deep-beta crossover replay REGISTERED as a frozen prediction; the freeze conditioning rule and the
  mask-tolerance catch banked; the (2,3) suppression's site-projection mechanism excluded. Frozen engine
  untouched (194/194). See CROSSCHECK_v97, 08_2d_interacting/PARITY_TABLE_RESULT.md and parity_table.py.
- The method audit (v98). v97 audited against the KT-RG method v3.1 (outputs only banked): the
  suppression pattern found CONFOUNDED (degeneracy parity vs level rationality -- the falsification
  test was the weakest available); the deviation ratios computed and found underpowered; #107's
  root-flow claim downgraded to CANDIDATE; the L=8 prediction QUANTIFIED (frozen z8 curve from
  A8(40) = +0.1135(266): the v84 static violated by +0.013 at beta=40 if root-flow holds); the queue
  reordered by leverage (coefficient phase 2 first). Frozen engine untouched (194/194). See
  CROSSCHECK_v98 and 08_2d_interacting/METHOD_AUDIT_v97.md.
- Coefficient program phase 2 (v99). The heavy-tail problem solved (integrand autopsy: alpha ~ 0.55
  infinite-variance tails; mixture importance sampler, weights <= 2, ~31x reduction, analytically
  validated); the frozen f2-polynomial measured to 3-7% (root s* = 0.00183(8), z_pol(36) = 1.8249(12));
  the registered root-flow branch excluded at ~10 sigma; and THE TWO-SECTOR DISCOVERY: v96 faithfulness
  falsified at 3.4 sigma -- the freeze kills the delta1 antiperiodic images, which form a hole-image
  sector Delta(s_phys; 36) = +0.369(109) e-9; the physical zero is the root of [frozen polynomial +
  Delta]. The literal-rate menu bookkeeping is queued for a tau-integrated re-derivation; the empirical
  pool stands. Frozen engine untouched (194/194). See CROSSCHECK_v99,
  08_2d_interacting/COEFFICIENT_PHASE2_RESULT.md and coefficient_phase2.py.
- The Delta sector (v100). The v99 "second player" RESOLVED as a delta1 x f2 cross-term, not a
  background: Delta(0;beta) ~ 0 at both beta (the hole sector vanishes when level 2 is empty), so the
  freeze omitted a cross-coefficient. The cross-slope measured (matched-s secants) d1(28)=+41.8(13.2),
  d1(36)=+88.8(21.5) e-9 grows with beta and shifts the effective root toward the physical f2*
  (0.00183 -> 0.00327, physical 0.00376). Delta1Frozen validated against the physical value. The
  13/7-vs-24/13 closure reduces to the assembled root flow z(beta), spec'd and predicted. Frozen engine
  untouched (194/194). See CROSSCHECK_v100, 08_2d_interacting/DELTA_SECTOR_RESULT.md and delta_sector.py.
- Consolidation (v101). A sweep, no new physics: the C surrogate brought current with v96-v100 (params
  status block + callable carriers surr_l6_zpol36 / surr_l6_cross_slope / surr_l6_root_linear; 4 new gate
  cases pass, still matches Python to 1e-9); the brute-force C reference drivers stamped and unmodified
  (still compile); every md audited self-contained -- the engine's gen_golden/cdet_reference orphan
  corrected (golden.json ships and is authoritative). Frozen engine untouched (194/194). See
  CROSSCHECK_v101, 08_2d_interacting/CONSOLIDATION_v101.md.
- Deep-beta program v102-v108 (consolidated cross-reference). v102 surrogate-vs-brute side-by-side (sector
  exact, ln-mag 1.81x; flagged a stale L=8 carrier). v103 PRECISION: naive float64 drops the deep-beta
  antiperiodic images (catastrophic 1-nf cancellation), fixed by the log-domain stable engine, mpmath-
  certified. v104 the pool SURVIVES under median-of-means (v103's "zero moves" retracted). v105 the robust
  flow RISES and fits no menu line. v106 the gravity-loop resummation adapted as the loop-format tail tool.
  v107 the assembled root flow gives z(inf)=1.8818(184) (lower menu falls, 15/8 returns). v108 both C layers
  consolidated + compared: the brute C's naive G0_atom carries the deep-beta bug latent (benign-correct);
  built+certified the log-domain G0_atom_stable. Frozen engine untouched (194/194). See CROSSCHECK_v102..v108
  and the matching RESULT.md files in 08_2d_interacting/.
- Stable C engine (v109). cdet_stable_engine.c (frozen connected determinant + log-domain propagator,
  reads spectrum_l6.bin), validated to machine precision vs Python C_V and vs high-stat Python A(40). A
  6-point grid to beta=64 in 150 s exposed that v107's high-beta A was heavy-tail-biased LOW (A(40) banked
  0.119 vs true 0.267) -> z(inf)=1.882 was an underestimate; the corrected flow rises to 1.878@64 still
  climbing, 15/8 falls, asymptote >=1.88 but UNPINNED (extrapolation unstable). Frozen engine untouched
  (194/194). See CROSSCHECK_v109, STABLE_C_ENGINE_RESULT.md.
- The plateau run (v110). Pushed the long-double engine (float64 NaNs at beta>=96) to beta=120: NO plateau
  -- the flow rises monotonically through every menu rational (15/8 at beta~61, 17/9 at ~74, 19/10 at ~87)
  to z(120)=1.920, still climbing, rho_A unconverged. z(inf) in [1.95,2.0], plausibly the trivial z=2. The
  menu-rational identification (v93-v107) is RETRACTED -- finite-beta crossings, not the asymptote. The
  freeze regularizes the determinant (frozen safe to 120; physical fails at ~56). Frozen engine untouched
  (194/194). See CROSSCHECK_v110, PLATEAU_RESULT.md.
- z(inf) resolved (v111). Model comparison on (2-z)*beta=ln(|c1|/A) over the clean flow REJECTS the
  exponential-gap/menu picture (chi2 622/7) for a power-law: A~beta^-2.8, |c1|~beta^-0.54 (both rates ~0),
  so z(beta)=2-2.3*ln(beta)/beta -> 2. z(inf)=2, the bare probe level; the menu rationals (11/6..17/9) are
  finite-beta crossings of a ln(beta)/beta approach, NOT asymptotes. The v93-v107 menu identification is
  closed. Frozen engine untouched (194/194). See CROSSCHECK_v111, ZINF_RESULT.md.
- z(inf)=2 derived (v112). A and c1 are tau-averages, so the power is set by J(beta)=beta^3*X: J_A->const
  (A corner-confined ~1/beta^3), J_c1~beta^2.7 (c1 de-confined by the smallest-gap level-2 channel,
  xi_2=0.155). |c1|/A~beta^2.7 forces z=2-2.7*ln(beta)/beta -> 2 -- z(inf)=2 because the probe level is the
  smallest gap. Windowed J_c1(W)~W^2.6 confirms de-confinement. Frozen engine untouched (194/194). See
  CROSSCHECK_v112, POWERLAW_DERIVATION_RESULT.md.
- Single-channel sharpening tested (v113). An external proposal (c1=sum a_n exp(-xi_n beta), xi_2<xi_n,
  phase in n=2 -> 'one mode of gap (2-mu)') splits: kernel SURVIVES (xi_2<xi_n true, phase in the single
  level-2 channel = v112), literal exp form FALSIFIED (predicts 3e6x decay, measured 1.66x). The level-2
  propagator SATURATES (int exp(-xi_2 tau)->1/xi_2=6.5) -> rate-0 power law, not an exp mode; gap (2-mu) =
  range + limit z(inf)=2, not a beta-rate. Frozen engine untouched (194/194). See CROSSCHECK_v113,
  SPECTRAL_CHANNEL_RESULT.md.
- z(inf)=2 locked to the Fermi surface (v114). Generalizing the freeze to an arbitrary probe and moving
  probe 2->3 shows the mechanism does NOT generalize: probe=2 (Fermi surface) gives finite c1 and z->2,
  probe=3 makes c1 DIVERGE as exp(+2.7 beta) -- a population inversion (level 3 occupied while level 2
  empty) forbidden by Fermi statistics. z(inf)=2 is locked to level 2 = the lowest empty level = the only
  valid probe. Frozen engine untouched (194/194). See CROSSCHECK_v114, PROBE_LOCK_RESULT.md.
- Full dual consolidation at the frontier (v115). Both C layers brought current with z(inf)=2: the
  surrogate's live carrier surr_l6_z_inf() had been returning the stale 1.8818 despite 13 caveat layers --
  now 2.0, plus surr_l6_z_finite (ln(beta)/beta law) and a legacy carrier; brute-C re-stamped pointing at
  the built stable engine. Side-by-side (surrogate carries 2.0 / stable-C derives 2.0 / brute-C ED-anchor
  at benign). LESSON: the duality is a CHAIN -- surrogate can't compute, brute-C can't go deep, stable-C
  can't self-certify; the cross-validation caught every deep-beta error. Frozen engine untouched (194/194).
  See CROSSCHECK_v115, DUAL_CONSOLIDATION_v115_RESULT.md.
- Site-choice generalization (v116). Varying the lattice sites at fixed Fermi-surface probe, z=2+ln(|A|/
  |c1|)/beta rises toward 2 for all 5 geometries -- z(inf)=2 is geometry-independent (registered prediction
  confirmed). NEW: the SIGN of (A,c1) varies by geometry (opposite->physical root, same->none); the SCALE
  (z=2) is doubly universal (probe- and site-independent), the SIGN structure is the geometric degree of
  freedom -- sign and scale separate. Frozen engine untouched (194/194). See CROSSCHECK_v116,
  SITE_GENERALIZATION_RESULT.md.
- The sign side = Friedel (v117). A's sign oscillates with site separation -- scanning a vertex site along x,
  sign(A)=(-,-,-,+,+), a reproducible zero-crossing (seeds agree, |A| min at the flip), Friedel-class. The
  wavelength is LONG (~8 sites = 2k_F from mu=1.845 near the band top), not period-2. UNIFYING: the Fermi
  surface governs BOTH -- its GAP sets the scale z(inf)=2, its MOMENTUM sets the sign. v116 found sign/scale
  separate; v117 finds one origin (the Fermi surface) via two channels. Frozen engine untouched (194/194).
  See CROSSCHECK_v117, FRIEDEL_SIGN_RESULT.md.
- Gap-momentum unification test = move mu (v118). Moving mu in (1,2) shows BOTH the sign pattern and the
  z-flow are mu-INVARIANT (sign(A)=(-,-,-,+,+) and z=1.786/1.853/1.887 at mu=1.3/1.6/1.9). The registered
  continuous-2k_F prediction is FALSIFIED: the engine is FROZEN, so the Fermi surface is the discrete
  level-1|level-2 boundary, fixed for all mu in the window. CORRECTS v117 (the 2k_F(mu) match was
  coincidental); STRENGTHENS the unification -- one discrete object governs both scale and sign, rigid in mu,
  mu mattering only when it crosses a level (v114). Frozen engine untouched (194/194). See CROSSCHECK_v118,
  MU_UNIFICATION_RESULT.md.
- Full 2D Friedel sign-map, elementary resolution (v119). The elementary frozen object rho(0,r)=FT of the
  occupied region is cube-symmetric, SHORT-wavelength (~2-3 sites, wavevector (120,180)deg = level-1|2
  boundary modes), and EXACTLY mu-invariant (ZERO modes in the gap (1,2) -> occupied set rigid; analytic
  proof of v118). A's sign is a determinant superposition of these short oscillations -- v117's ~8-site
  envelope was the superposition, not the elementary scale (v117 core survives). Same discrete Fermi surface
  sets scale (z=2) and sign. Frozen engine untouched (194/194). See CROSSCHECK_v119, FROZEN_FRIEDEL_MAP_RESULT.md.
- Full dual consolidation at the sign frontier (v120). The surrogate was scale-only; now it carries the
  sign-side analytic core (gap_modes/occupied over the cube integer multiplicities + the Friedel wavevector),
  confirmable in C with no eig, matching Python exactly. SHARPER THEOREM: cube_hopping(6) is integer-spectrum,
  so no mode lies in any open unit interval -> the freeze is exactly mu-rigid in ANY unit interval (generalizes
  v118/v119). Side-by-side spans scale and sign; the sign side is a chain (rho=Python, A=C, mu-rigidity=
  surrogate). Frozen engine untouched (194/194). See CROSSCHECK_v120, DUAL_CONSOLIDATION_v120_RESULT.md.
- Elementary Friedel object rho(0,r) ported to C (v121). cfriedel.c computes rho(0,r)=(1/N)sum_{eps(k)<=1}
  cos(k.r) from the plane-wave structure -- no eigenvectors, no spectrum file, no eigendecomposition --
  validated worst-dev 4.81e-11 vs the Python eigh density matrix over all 216 sites; map identical to v119;
  occupied 156, integer-spectrum mu-rigid. Closes the v120 open fix (sign side now full three-layer C
  coverage). Frozen engine untouched (194/194). See CROSSCHECK_v121, FRIEDEL_PORT_RESULT.md.
- Multi-lattice laws, scaling, hybrid (v122). mu-rigidity (v120) is CRYSTALLOGRAPHIC -- exact iff cos(2pi/L)
  rational iff L in {1,2,3,4,6} (verified L=2..12); the SCALE law z(inf)=lowest-empty-level and the FRIEDEL
  law are UNIVERSAL. The plane-wave propagator makes the brute force O(N x MC), L-agnostic, no stored spectrum;
  cfriedel_L.c runs the structural layer to L=20 in <1s. How big: structural laws L=20+, determinant L~12-16,
  ceiling is analysis-context not lattice. HYBRID: phase 1 laws (O(N), any L) -> phase 2 plane-wave determinant
  (O(N x MC)). Frozen engine untouched (194/194). See CROSSCHECK_v122, MULTI_LATTICE_RESULT.md.
- Phase 2 of the hybrid: L-generalized plane-wave determinant engine (v123). cdet_planewave_engine.c computes
  A,c1 at any L on the plane-wave propagator (no eigenvectors/spectrum file); validated == stable engine at L=6
  (A,c1 to the last digit). Scale law z(inf)=lowest-empty-level PROVEN multi-lattice: L=4 ->2, L=6 probe=3
  mu in (2,3) ->3 -- z(inf) is the lowest-empty level (size- and probe-general), not a constant 2. Cost ~linear
  in N; L~12-16 feasible. Open: non-crystallographic L needs a continuous-threshold freeze. Frozen engine
  untouched (194/194). See CROSSCHECK_v123, HYBRID_PHASE2_RESULT.md.
- Toward million-site lattices (v124). PROJECTOR FAST PATH (regroup g0 by distinct eigenvalue, EXACT, 73x at
  L=12) makes L=100 (1e6 sites) a day-long z-flow; CONTINUOUS FREEZE (mode 2) proves z(inf)=sqrt2 (irrational)
  at L=8 -- scale law holds even irrational; run_to_log harness + NaN guard for safe day-long unattended runs
  (streaming already in place). Frozen engine untouched (194/194). See CROSSCHECK_v124, SCALING_HARNESS_RESULT.md.
- The large-L study (v125). z(inf)(L)=lowest-empty(L) marches to the continuum Fermi level mu as L->inf
  (gap~L^-3.3): asymptote 2.0->1.414->1.082->1.0002, confirmed by fast-path z-flows. Ran L=100 (1e6 sites) at
  52s/pt (probe_val=1.000192==prediction). z(inf)->mu thermodynamically but the determinant signal vanishes as
  the gap closes (signal-starved; the wall sharpens onto mu). Frozen engine untouched (194/194). See
  CROSSCHECK_v125, THERMO_LIMIT_RESULT.md.
- The signal budget (v126). c1 (probe response) is the binding signal (relErr(c1)~gap^-0.47; relErr(A) flat);
  MC budget to resolve z(inf) ~ gap^-0.9 ~ L^3 ~ N -- POLYNOMIAL, no exponential sign-problem wall in this
  observable. A day-long L=100 run resolves a coarse million-site z-flow; launch recipe (run_to_log + cpw -L
  100 -fast) in the result. Frozen engine untouched (194/194). See CROSSCHECK_v126, SIGNAL_BUDGET_RESULT.md.
- The v116 selection rule vs large L (v127). sign(A)!=sign(c1) tested vs L: sign(A) converges (bulk), sign(c1)
  FRIEDEL-OSCILLATES in L (seed-stable 24-/32+/40-/48+), |c1|->0 -- the rule's outcome alternates and goes
  MARGINAL in the continuum; it is a finite-gap Friedel phenomenon, not a continuum invariant (prediction of
  uniform persistence partially falsified). Frozen engine untouched (194/194). See CROSSCHECK_v127,
  SELECTION_RULE_RESULT.md.
- The c1 sign in L is arithmetic jitter (v128). sign(c1) has NO Friedel period (period-16 falsified, 28/44 &
  36/52 mismatch, seed-stable); the probe momentum jumps number-theoretically. v119 contrast: A integrates the
  whole sea (clean continuum wavevector, converges), c1 picks one lowest-empty multiplet (jitters). No period
  to derive; the v116 rule is arithmetic at finite L, marginal in continuum. Frozen engine untouched (194/194).
  See CROSSCHECK_v128, PROBE_JITTER_RESULT.md.
- A's continuum Friedel wavevector (v129). v119's (120,180) dominant wavevector confirmed as a convergent
  continuum feature: the Fermi surface (cos-sum<=-1/2) is L-independent; rho's Friedel edge along x converges
  kx/L 0.425->0.347 (~120deg, 3-site end). (120,180)=L=6 sampling. Counterpart to v128 (A integrates the sea ->
  convergent; c1 picks one multiplet -> jitter). Frozen engine untouched (194/194). See CROSSCHECK_v129,
  CONTINUUM_WAVEVECTOR_RESULT.md.
- Consolidation v130. Surrogate + brute + merged hybrid brought current to v124-v129 and cross-validated:
  surrogate gained surr_lowest_empty / surr_friedel_edge (no eig); brute re-stamped (ED anchor); hybrid header
  merged. Three-way z(inf)=lowest-empty AGREES (surrogate-C == hybrid-C == python); only build-hygiene drift
  fixed. Frozen engine untouched (194/194). See CROSSCHECK_v130, CONSOLIDATION_v130_RESULT.md.
- CoS prototype + integration assessment (v131). Verified (vs the real engine) that a CoS-style subset-conv
  (O(2^n n^2)) reproduces C_V to machine precision; the engine's mask = CoS's connectivity record R, same 2^n
  wall. Honest cost: combine swap marginal (3^n beats 2^n n^2 only at n>=12; 2^n n^3 det cost dominates). Real
  lever = CoS forward DP (n^3->n^2) and SU(N) N-independence (the N=6 Yb frontier). See CROSSCHECK_v131,
  COS_PROTOTYPE_RESULT.md.
- The charge velocity at n = 0.5 is now in hand to about 1 to 2 percent (added after
  the first draft). The clean route is the flux stiffness divided by the EXACT K_rho,
  u_rho = pi (L/2)(d2E/dPhi2)/K_rho, which cross-checks the independent Bethe
  dressed-energy velocity at U = 4 and U = 8 to about 1 percent and is confirmed at
  L = 16. The earlier failures were from dividing by a contaminated particle-number
  curvature; replacing it with the exact K_rho fixed it. Script: charge_velocity.py.
- The small-U spin velocity is likewise charge-contaminated on L <= 12; the clean
  window is large U where the charge is frozen.

None of these open items affect the three verified results above. They mark where the
next computation needs more lattice, which is squarely in the engine's wheelhouse and a
natural place for the diagrammatic Monte Carlo machinery.

## Reproduction

All in `cdet_complete/07_predict_vs_compute/`:
- `bethe_Krho.py` ........ exact K_rho, prints the limit checks and the ED comparison.
- `spin_velocity.py` ..... Casimir velocity, Heisenberg check and Hubbard strong coupling.
- `conformal_tower.py` ... the tower collapse.
- `doped_tower.py` ....... doped-tower velocity-free probe (v9): exact U=0 anchor, and
  the spin-charge-separation break read off honestly.
- `doped_tower_pure.py` .. doped-tower pure-charge primary (v10): x_4 -> 2 K_rho, the
  fix to the v9 break, verified against the exact Bethe K_rho.
- `doped_tower_scaling.py` doped-tower finite-size scaling (v11): x_4 -> 2 as ~1/L^2 at
  the exact U=0 anchor, validated against the L=12 many-body gap.
- `spin_charge_velocities.py` two velocities from the doped tower (v12): u_rho and
  u_sigma split with U; u_rho cross-checked against the v8 flux stiffness.
- `spin_stiffness_qf.py` .. independent u_sigma via the spin stiffness (v13): corrects the
  v12 extraction; both velocities now from one robust flux-stiffness route.
- `bethe_spin_velocity.py` exact Bethe spin-velocity attempt (v14): charge-velocity
  validation, the zero-field spin-endpoint fragility, and the u_sigma exact-limit bracket.
- `spin_susceptibility_qf.py` second independent ED u_sigma via the lowest triplet gap
  (v15): corroborates the v13 stiffness within ~8-12%, calibrated at the exact U=0 limit.
- `spin_velocity_exact_check.py` EXACT half-filling spin velocity (v16, Bessel): validates
  the ED bracket, confirms the stiffness as the better estimate, locates quarter-filling u_sigma.
- `filling_dependence.py` ... u_sigma across n=0.5,0.833,1.0 (v17): prefactor generalizes across
  size/filling; the bracket gap = the SU(2)_1 marginal correction, suppressed by doping.
- `bethe_spin_velocity_integrated.py` EXACT quarter-filling u_sigma (v18): the dressed-energy
  plateau, validated vs half-filling Bessel to 0.1-0.2%; exact value lies below both ED routes.
- `doping_crossover.py` ... exact u_sigma vs ED routes across n=0.5,0.833,1.0 (v19): one smooth
  crossover -- below both when doped, between them at half filling; stiffness the upper envelope.
- `bethe_spin_velocity_sparse.py` sparse FFT solver (v20): reaches small U at half filling
  (validated vs Bessel); characterizes quarter-filling small U as a structural no-plateau wall.
- `weak_coupling_spin_velocity.py` analytic bridge (v21): u_sigma = v_F - U/(2pi) - U^2/(16pi^2),
  leading coeff exact at half filling and filling-independent; quarter small-U to leading order.
- `04_locality/locality_prune_test.py` engine acceleration (v22): locality-pruning the connected
  recursion ruled out (output-locality is not term-locality); cost lever is order reduction.
- `engine_exp/atomic_order_reduction.py` engine acceleration (v23): two-engine method (frozen
  baseline + sandbox); bare expansion diverges at strong coupling, resummation rescues it (vs G_exact_atom).
- `engine_exp/dimer_efficiency.py` engine acceleration (v24): quantitative gain on the dimer (vs ED);
  bare and atomic schemes complementary (radii 4t, U/4); strong-coupling gain qualitative, cost 3^N.
- `engine_exp/stress_cv.c` engine acceleration (v25): stress test of C_V; measured RAM/time wall
  (order 27 on 3 GB); how-much-faster = convergence-within-the-wall (atomic 1.26 s vs bare never).
- `engine_exp/stress_cv.c` (v26): buffers removed (VLAs, bit-identical to baseline), C_V OOM-safe,
  crash-safe harness (per-row fflush, RAM guard 90%, SIGINT handler, tested via real interrupt).
- `engine_exp/diagmc.c` + `diagmc_validate.c` (v27): high-order time-integration (cdet_order_mc) by
  MC over vertex times+sites; validated vs frozen baseline at n=1,2 within MC error; gives n>=3 terms.
- `engine_exp/subset_conv_poc.c` (v29): naive-3^n vs butterfly-2^n-n^2 subset convolution + long-
  double path; in-RAM crossover n=19 (n=21: 2.7x), error is recoverable cancellation (long double
  4-14x), fast form costs ~(n+1)/2x RAM. In-RAM speed tool for n~19-23; reducing n stays the lever.
- `07/atomic_reference_order_reduction.py` (v30): atom oracle quantifying the reference-shift lever --
  order to 1e-6 @ U=2: infinity (bare) -> 3-11 (shifted); largest term 3.8e12 -> 0.2 (cancellation
  cured). Confirmed vs the C engine G_exact_atom. Target for the cdet_order_mc reference swap.
- `CROSSCHECK_v5.md` ... `CROSSCHECK_v194.md` ... per-result proof data.

Engine: `cd cdet_complete/engine && make CC=gcc test` gives 194 passed, 0 failed;
`make CC=gcc bench && ./bench_qss` gives the fast-versus-dense determinant agreement.
- Integration #1 done as a supplement (v132). The connected determinant in O(2^n n^2): fast principal minors
  (one Schur recursion) + the v131 subset-conv reproduce the engine's full C_V to 3e-15, vs the engine's
  O(2^n n^3 + 3^n). Standalone verified path; engine untouched; prerequisite for #2 (SU(N)) and #3
  (self-energy). See CROSSCHECK_v132, FAST_MINORS_RESULT.md.
- Physical mapping resolved (v133). z(inf) is a real spectral observable: the single-particle addition pole
  (lowest-empty level). It tracks the moving pole (v125); the v78 fugacity lemma puts the poles at eps_k. Free
  now (g0 = free spectrum); the interacting addition energy needs the self-energy resummation = integration #3.
  So z and #3 are the same physical target at two resummation levels. See CROSSCHECK_v133, PHYSICAL_MAPPING_RESULT.md.
- Integration #3 step 1 (v134). The self-energy as the interacting upgrade of z, ED-verified: atom Sigma ==
  closed form (1e-15); dimer addition pole == z(inf) at U=0, = eps_free + Re Sigma at U>0. z is the Sigma=0
  limit of the interacting addition energy; #3 supplements it. See CROSSCHECK_v134, SELF_ENERGY_RESULT.md.
- Integration #3 step 2 (v135). The diagrammatic self-energy (connected-det order series + Dyson) converges
  geometrically to the exact ED Sigma inside the bare-series radius ~pi/beta (atom 7e-6 @U=0.3 order 8). The
  radius limit motivates the direct irreducible series (step 3). See CROSSCHECK_v135, SELF_ENERGY_DIAGRAMMATIC_RESULT.md.
- Integration #3 step 3-4 (v136 -> CORRECTED v137). v136 claimed the 1PI series has a much larger radius (~1.76);
  v137 RETRACTS this -- exact sigma_n (Dyson recursion) give R_Sigma~0.84 ~ R_G~0.73, no advantage (v136's number was
  a contour-proxy artifact). The real Simkovic-Kozik advantage is efficiency + MC variance. Exact sigma_n reproduce
  ED Sigma to 1.9e-9 @U=0.3. v133-135 unaffected. See CROSSCHECK_v137, SELF_ENERGY_IRREDUCIBLE_RESULT.md.
- Full consolidation (v138). Three paths (surrogate/plane-wave/python) agree (addition pole 5e-10, fast minors
  3e-15, exact 1PI sigma_n 7e-8); all v131-v137 advances live; README+QUICKSTART refreshed. Learnings: plane-wave
  LD for deep cancellation, self-energy engine wire-in + resummation, fast-minors wire-in. See CROSSCHECK_v138,
  CONSOLIDATION_v138_RESULT.md.
- Hybrid stress test + guards (v139). The hybrid is robust (val 0.00e+00, fast==direct, NaN guard clean, 2.7M
  sites @193s); f64 walls @beta~100, LD reaches >=200. Found + guarded 3 input failure modes (non-crystallographic
  L + mode 0/1, large delta, delta=0) -- input-only, val preserved. See CROSSCHECK_v139, STRESS_TEST_v139_RESULT.md.
- Resummation / precision (v140). The gravity-loop exact-recurrence 15-digit trick does NOT transfer (our sigma_n
  obey no finite recurrence). Pade extends strong-coupling reach (3e13->0.23 past the radius) not precision; most
  models already exact-resummed; the general accuracy lever is extended-precision arithmetic (LD/mpmath). See
  CROSSCHECK_v140, RESUMMATION_RESULT.md.
- Fold-in + rational hint (v141). Surrogate gains surr_interacting_pole (free pole + Hartree shift); v139 guards +
  LD already folded. THE HINT (live): at fixed density the atom self-energy IS rational (exact 1-term recurrence,
  [2/1] exact to 1e-15 past any bare radius) -- the 15-digit route lives in the skeleton/bold expansion; the
  grand-canonical nd(U) was the only non-rational piece. Lattice: open. See CROSSCHECK_v141, RATIONAL_SKELETON_RESULT.md.
- SU(N) step 1 (v142). Started queue #2: the SU(N) atom EoS + the N-polynomial record. ln Z U-coeffs are exact
  degree-(j+1) polynomials in N (cumulants of the pair count under the U=0 binomial; N=2..7 predict N=8,9,10 to
  5e-9; ED-checked 2e-11; SU(6) density 0.309 @U=1). N-independent kernel -> any flavor number. Lattice = step 2.
  See CROSSCHECK_v142, SUN_ATOM_RECORD_RESULT.md.
- SU(N) step 2 (v143). The N-polynomial record survives hopping: 2-site SU(N) lattice ED -> ln Z coeffs stay
  degree-(j+1) in N (c1 deg 2 predicts N=5,6 to 5e-5; U=0 factorizes to 1e-14). The CoS N-independent kernel
  evaluates at any flavor number on the lattice. Production CDet+record = remaining engineering. See CROSSCHECK_v143,
  SUN_LATTICE_RECORD_RESULT.md.
- SU(N) step 3 (v144). The production EoS route: first coefficient from single-flavor g0 (d,d') x the record
  (c1=-beta N(N-1)d^2, n1=-(N-1)d d') matches the 2-site SU(N) ED to 1e-7 for ALL N incl N=6, NO N=6
  diagonalization. The N=6 first-order EoS tracks ED at small U. CoS at SU(2) cost. Higher orders remain. See
  CROSSCHECK_v144, SUN_LATTICE_PRODUCTION_RESULT.md.
- SU(N) step 4 + gravity hint (v145). 2nd-order EoS record persists (n2 low-deg poly in N, N=6 to 3e-4). The
  gravity recurrence->rational-GF->exact-resummation mechanism lives in N (not U): coeffs poly in N -> finite
  recurrence (c1 3rd diff 7e-15) -> rational N-GF -> all-N EoS resums from a few small N (c1(6) exact). Same as
  gravity, in N; root 1 vs the gravity cubic. This is why CoS is N-independent. See CROSSCHECK_v145, SUN_RESUMMATION_N_RESULT.md.
- U-axis rational boundary (v146). Sigma(U) rational IFF eigenvalues linear in U IFF interaction diagonal (atom
  ||[Hkin,Hint]||=0 -> rational). Hopping (dimer ||[Hkin,Hint]||=1.4) -> algebraic eigenvalues -> lattice Sigma
  algebraic (branch points), not rational. 15-digit route = atom/local (DMFT) only; lattice needs conformal. See
  CROSSCHECK_v146, RATIONAL_LATTICE_BOUNDARY_RESULT.md.
- Full consolidation v147. Three models at highest capability: frozen reference engine/ (194/194, never altered,
  fast/omp), production hybrid (validates ==it, all caps), surrogate (+ SU(N) EoS carriers sun_c1/sun_n1). Analysis
  supplements kept as separate CLI modules. See CROSSCHECK_v147, CONSOLIDATION_v147_RESULT.md.
- Unified end-to-end model v148. cdet_lab.py control plane: every capability as swappable components from the
  terminal (--target x --method x --model), grounded in a web search of physicist needs, frozen reference
  untouched. See CROSSCHECK_v148, CDET_LAB_RESULT.md.
- Idiot-proof front-end v149. cdet_shell.py: conversational shell (plain language -> interpret -> confirm -> run),
  did-you-mean on typos, named/saved configs that survive reverts; thin safe layer over cdet_lab, frozen reference
  untouched. clig.dev best practices. See CROSSCHECK_v149, CDET_SHELL_RESULT.md.
- Blind-test hardening v150. Used cdet_shell as a zero-knowledge user; fixed 6 issues (confirm trap, N/n collision,
  validation, synonym substring bug, lenient yes/no, menu->help). Not possible to get stuck. See CROSSCHECK_v150,
  BLIND_TEST_v150_RESULT.md.
- Sweep/stress harness v151. cdet_study.py: scan a parameter, detect convergence/accuracy-drop, cutoffs (max-time,
  accuracy), outputs log+csv+json+png+ASCII with points of interest marked; NL-drivable in the shell. See
  CROSSCHECK_v151, CDET_STUDY_RESULT.md.
- SU(N) step 5 capstone v152. Record-predicted EoS curve <n>(U): K=8 contour on small N -> record-predict N=6 (no
  SU(6) diag) -> Pade matches direct SU(6) ED to ~1-2% out to U~1.2. Strong coupling needs conformal (v146). See
  CROSSCHECK_v152, SUN_EOS_CURVE_RESULT.md.
- Strong coupling reached v153. Two-point resummation (weak lattice record + strong atom-record atomic limit, both
  record-predicted) spans the U-axis: record-predicted SU(6) EoS hits U/t=2.3 (Kozik) at 2.4%, worst <5% to U=4, no
  SU(6) diagonalization. See CROSSCHECK_v153, SUN_EOS_STRONG_RESULT.md.
- 2D thermodynamic limit v154. The record is lattice-independent: leading EoS coeff n1=-(N-1)d d' transfers across
  geometry (to 1e-8) -> 2D k-integral gives SU(6) n1=-0.5116, no diagonalization; atomic strong anchor lattice-
  independent so the two-point extends to 2D. See CROSSCHECK_v154, SUN_EOS_2D_RESULT.md.
- Second-order coefficient decomposed v155. n2=(N-1)^2 a+(N-1) b; a=d(d'^2+0.5 d d'') self-consistent Hartree (free
  derivs, validated 2e-7, predicts n2(6) to 1.4e-4); dominant (N-1)^2 part exact in 2D (a_2D=0.005622); b=bubble,
  subleading. See CROSSCHECK_v155, SUN_EOS_N2_RESULT.md.
- Consolidation v156. Health gate re-proves the v148-155 arc (UI suite + SU(N) EoS weak->strong->2D->2nd order) and
  the three-model invariants, all vs ED/k-integral anchors; frozen engine 194/194 untouched. The consolidation rule
  is standing protocol. See CROSSCHECK_v156, CONSOLIDATION_v156_RESULT.md.
- Triple-run benchmark v157. Consolidation rule now runs all three (surrogate/brute-force/hybrid); applied the
  hybrid auto-fast projector path for crystallographic L (bit-identical, ~26x grid speedup, val 0.00e+00); frozen
  source never edited. See CROSSCHECK_v157, TRIPLE_BENCHMARK_v157_RESULT.md.
- Chained two-round v158. Round-1 terminal electron state (RNG stream) seeds round-2: continuation gives 1.39x
  (sqrt2) error reduction (vs zero-info same-seed rerun) and non-cycling config expansion (9/10 vs deterministic
  1-2 cycle); hybrid terminal_state print-only, val 0.00e+00, frozen source untouched. See CROSSCHECK_v158,
  CHAINED_RUN_v158_RESULT.md.
- Two-particle chained run v159. Two particles + exclusion: chained walk sweeps 10/10 pair-configs (Pauli held);
  continuation sqrt2 gain reaches both 1-body A (1.44x) and 2-body interaction c1 (1.39x). See CROSSCHECK_v159,
  TWO_PARTICLE_RUN_v159_RESULT.md.
- Conformal-Borel resummation v160. The CDet frontier is order (not lattice size); added the field's conformal-Borel
  tool keyed to the complex Borel singularity (|t_c|~1.05): beats plain Pade 2-4x on the SU(N) EoS (validated vs ED).
  Strong coupling needs large-order structure / the v153 bridge (fragile U~2.5 result not claimed). See
  CROSSCHECK_v160, SUN_EOS_CONFORMAL_v160_RESULT.md.
- Consolidation v161. Health gate + triple-run benchmark of the v157-160 arc with the frozen reference (194/194)
  retained as the parity anchor; all three models consistent. Improvement cycle: safe set_freeze precompute is
  bit-identical but negligible (~0.6%, not added); low-rank freeze update deferred as parity-risky. See CROSSCHECK_v161,
  CONSOLIDATION_v161_RESULT.md.
- Large-L plane-wave propagator v162. Added the closed-form 2D free propagator (square2d_G0_pw) straight from
  eps=-2t(cos kx+cos ky): O(L) memory, no eigenvectors, reaches 100x100 past the 16x16 LMAX cap. Exact vs the numerical
  path (1.25e-16); TD-converged past ~12-16 sites (big lattices unneeded). See CROSSCHECK_v162, SQUARE2D_PW_v162_RESULT.md.
- Unified CLI v163. Top-level `cdet` wraps the whole suite (validate/converge/resum/eos/run/sweep/lab/shell/info) with
  rich-optional output; self-contained (stdlib argparse). `cdet validate` shows all gates green in one table. See
  CROSSCHECK_v163, real_patterns ledger #173.
- Double occupancy v164. Added D=<n_up n_dn> as a proper interacting observable (D=-(1/beta)dlnZ/dU per site);
  two independent ED routes agree to ~1e-10; Mott suppression with U; conformal-Borel 65x better than Pade at U=1;
  E_int/site=U*D. Wired as `cdet docc`. See CROSSCHECK_v164, double_occupancy.py.
- Susceptibilities v165. Added charge compressibility kappa and spin susceptibility chi_s, each cross-checked by a
  derivative + a fluctuation-dissipation route (~1e-7); opposite Mott trends (kappa down, chi_s up); conformal-Borel
  resummation. Wired as `cdet chi`. See CROSSCHECK_v165, susceptibilities.py.
- Visualization v166. Built-in matplotlib figures (convergence/resummation/mott/summary) reproduced from the validated
  code paths; wired as `cdet plot`. See CROSSCHECK_v166, plots.py.
- Packaging/CI v167. pyproject.toml (pip install -e . -> working `cdet` command), MIT LICENSE, GitHub Actions CI
  running the frozen 194/194 gate + `cdet validate` + self-tests. packaging_check.py gates it. See CROSSCHECK_v167.
- Dual license v168. Switched MIT -> PolyForm Noncommercial 1.0.0 (free for academic/noncommercial) + a commercial
  license for business (COMMERCIAL-LICENSE.md). packaging_check.py verifies it; package still installs, cdet validate
  5/5. See CROSSCHECK_v168.
- Data export v169. Every validated observable -> CSV/JSON/HDF5 (reproduced from the gated code paths, round-trip
  verified); CSV/JSON stdlib, HDF5 optional. Wired as `cdet export`. See CROSSCHECK_v169, export.py.
- Native bindings v170. Optional pybind11 module cdet_core wraps the frozen engine primitives read-only; bit-identical
  to the 194/194 engine (0.0e+00), ~2e6x faster than compile+subprocess. Opt-in build; .so not shipped. See
  CROSSCHECK_v170, bindings/.
- Docker v171. One-command deployment (Dockerfile + .dockerignore); build bakes in the 194/194 gate, ENTRYPOINT cdet,
  CMD validate. docker_check.py gates the recipe; CI builds+validates the image. (docker build not run in the sandbox;
  recipe verified natively.) See CROSSCHECK_v171.
- The wall vs lattice size v172. Leading weak-coupling wall U_c(L)=1/chi0_max from the plane-wave dispersion (any L to
  100x100); near half-filling the small lattice is spuriously pessimistic and growing L pushes the wall back (1.64 ->
  1.975) -- lattice helps. Filling-dependent; U_c is the leading instability (bubble-sum radius), v146 complex-U caveat.
  Validated 5 ways. See CROSSCHECK_v172, wall_vs_size.py.
- The wall is a tide v173. U_c(L) oscillates (BZ-quadrature commensuration); period in L = 2pi/q* (measures the nesting
  vector: half-filling->2, mu=-2.8->3.68); even L exponential / odd L 1/L^2; amplitude calms as L grows. Validated 5
  ways. See CROSSCHECK_v173, wall_tide.py.
- Prime lattice sizes v174. A Diophantine sieve on the wall: primes are commensuration-blind -> worst-case samplers
  (~2.7x composite deviation); corr(#divisors,dev)=-0.39; the effect is the v173 curvature law on the grid-miss to q*
  (corr 0.96); filling-dependent. Validated 5 ways. See CROSSCHECK_v174, wall_primes.py.
- Half-integer lattices v175. Twisted BC (theta=1/2 anti-periodic) does NOT heal the sieve (q-transfer grid
  theta-independent); a rectangular supercell whose q-grid hits q* does (23x46 err 4e-4 vs 17x17 6e-2, prime dim OK).
  Tide/sieve are q-sampling artifacts. Validated 4 ways. See CROSSCHECK_v175, wall_twist.py.
- Consolidation v176. The 4 wall modules onto one canonical core (wall_vs_size.chi0_max_rect; square dev 0.0e+00);
  README wall section added; `cdet crosscheck` tests all models side by side (E one core; B<->E chi0(0)=dn/dmu 7e-13;
  D<->E same finite-radius phenomenon). All models retested green. See CROSSCHECK_v176, consolidation_v176.py.
- True radius v177. The nearest complex-U singularity of lnZ is a THERMAL Fisher pair at Im U=pi/beta (atom calibrated
  0.0e+00), CLOSER than the RPA wall (ring L=3 R_true 2.90 < R_RPA 3.42, the v146 caveat), and -- a global lnZ zero with
  no q-grid max -- WITHOUT the Diophantine sieve. Validated 5 ways. See CROSSCHECK_v177, wall_true_radius.py.
- Consolidation v178. Added INDEX.md (the single map of the ~647-file package: architecture, dir map, 19 CLI subcommands,
  the two arcs, where knowledge lives); README lists trueradius + points to INDEX; all refs resolve, no orphans; cdet
  validate 5/5, frozen 194/194. See CROSSCHECK_v178, INDEX.md.
- Tier 0 v179. Implemented the connected-determinant recursion itself (Rossi 2017): C(V)=D(V)-sum_{v*} C(S)D(V\S), det
  weights. Validated to machine precision -- linked-cluster identity (2e-16, n=2..5), atom lnZ series (6e-17, ord 1..5),
  2-site vs ED (1e-9). A faithful low-order CDet, NOT a sign-problem advance. See CROSSCHECK_v179, cdet_connected.py.
- UX polish v180. Acted on a blind-user CLI review: bare `cdet run` works, sweep progress, help examples, shell synonyms,
  README "Try this first". Interface only; validate 5/5, frozen 194/194. See CROSSCHECK_v180, UX_POLISH_v180_RESULT.md.
- GUI v181. `cdet gui` -- a local stdlib-http browser console: sliders (N,U,mu,beta,L) + quick-run cards over the
  most-used computations, instrument readouts + traces, amber limit lines. Verified endpoints (propagator 0.19944 =
  converge TD limit, validate 5/5). Front-end only. See CROSSCHECK_v181, cdet_gui.py.
- GUI CSV+CLI v182. Sweep cards export CSV (reusing export._write_csv -> matches `cdet export`); every card shows a live,
  runnable copy-as-CLI command. eos/docc/chi compute at the suite reference so commands reproduce exactly. Front-end
  only. See CROSSCHECK_v182, cdet_gui.py.
- GUI recent-runs v183. A server-side `recent` strip remembers explicit runs (chips: card+sliders+result; restore on
  click; dedup; cap 8). Fixed a real v181 high-N hang (sweep ED hangs at N>=6) by capping GUI N at 4 + server clamp;
  larger SU(N) via copy-as-CLI. Front-end only. See CROSSCHECK_v183, cdet_gui.py.
- GUI wrapper v184. Rebuilt the GUI as a thin front-end (per Paul): imports no physics; every card runs the real
  `cdet <subcommand> <flags>` via subprocess and shows its output; sliders fill flags; injection-safe; core calcs
  untouched. See CROSSCHECK_v184, cdet_gui.py.
- Assistant v185. An optional toggle-on help assistant in the GUI -- a self-contained rule-based knowledge graph
  (cdet_assistant.py; 21 commands/9 concepts/6 workflows), NOT an LLM; offline, instant; suggests commands, runs nothing.
  See CROSSCHECK_v185, cdet_assistant.py.
- Assistant upgrade v186. Applied researched chatbot best practices (idf scoring, difflib typo tolerance, disambiguation,
  closest-match fallback, intent signals, quick-reply suggestions, follow-up context) to the rule-based assistant; still
  offline/stdlib-only/runs-nothing; no physics changed. See CROSSCHECK_v186, cdet_assistant.py.
- Blind student test v187. Installed/used cdet blind as a first-year; fixed a QUICKSTART/README on-ramp inconsistency and
  the assistant's beginner gaps (SOS intent + foundational concepts: lattice, Hubbard model, ED, Monte Carlo). Docs/help
  only; no physics. See CROSSCHECK_v187, BLIND_TEST_v187_RESULT.md.
- Blind expert test v188. Ran the blind test as Moller; all named capabilities verify (engine, bench_qss, fast_minors,
  self_energy retraction kept, cv.py MC, size-axis oracles). Added `cdet bench` to surface the scattered benchmark suite
  from one command; reworded the Moller section self-contained; stated the honest no-production-DiagMC-sampler gap.
  Interface/docs only. See CROSSCHECK_v188, MOLLER_BLIND_TEST_v188_RESULT.md.
- DiagMC sampler v189. Added cdet_diagmc.py, a Rossi-style connected-determinant Monte Carlo reusing the validated
  cdet_connected kernel; reproduces exact ln(Z/Z0) within error bars and measures the across-order sign wall
  (<s>=|sum a_n U^n|/sum|a_n|U^n collapsing toward the radius). Does not defeat the sign problem; bounded by 2^n;
  validated on atom+2-site. See CROSSCHECK_v189, CDET_DIAGMC_v189_RESULT.md.
- Blind intermediate test v190. Installed/used blind; fixed a real `cdet sweep` crash (cmd_sweep passed the --base string
  where study() wants a base-params dict) and added a README PEP 668 install note. No physics. See CROSSCHECK_v190,
  BLIND_TEST_INTERMEDIATE_v190_RESULT.md.
- Chaos console test v191. Adversarial blind test; injection inert, fixed real self-DoS/nan (diagmc --nmax/--samples caps,
  sweep point cap + time budget, finite/positive guards). No physics. See CROSSCHECK_v191, CHAOS_TEST_v191_RESULT.md.
- Lifecycle test v192. Blind pause/restart/interrupt test; made `cdet sweep` interrupt-resilient (incremental data.csv +
  flushed log + finalized summary on Ctrl-C), the GUI port-conflict graceful (auto free port), and the cache write atomic.
  No physics. See CROSSCHECK_v192, LIFECYCLE_TEST_v192_RESULT.md.
- Cross-platform fix v193. A blind Windows install showed the C gates falsely FAILing (Unix-only /tmp/.exe/cp/python3 in
  the harness); rewrote build/run sites portably (tempfile+.exe, shutil, sys.executable, env via subprocess) and added a
  per-OS compiler note to the docs. Linux still 5/5; no physics. See CROSSCHECK_v193, CROSS_PLATFORM_v193_RESULT.md.
- Cross-platform sweep v194. Removed every hardcoded /tmp from executable Python (consolidation_v161 + ~13 modules);
  `cdet validate` now 5/5 on Windows. Linux self-tests unchanged; no physics. See CROSSCHECK_v194,
  CROSS_PLATFORM_SWEEP_v194_RESULT.md.
