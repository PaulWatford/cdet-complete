# real_patterns.md  (v192)

A running guide to the methodology that has actually produced results in the
predict-vs-compute program. Each entry is a method that was tried and what it did.
This is the meta-record: how the physics got found, honestly, including ceilings.

## Methods that worked (with the evidence)

1. **Anchor on exact limits.** Build the model from the two endpoints known exactly:
   U=0 free-fermion (closed form) and the strong-coupling limit. The interior is then
   an interpolation, not a fresh model. Gave the spin correlator to ~2%.

2. **Make the anchors physical limits, not borrowed datapoints (v3).** The
   strong-coupling anchor was first a single U=8 Hubbard correlator (a borrowed
   point). Replacing it with the Heisenberg ring correlator -- the exact U->infinity
   limit, in a 2^L space ~60x smaller than the Hubbard ED -- made the model principled:
   both anchors are now limits. Verified the Hubbard correlator flows to it
   (RMS 1.1e-2 at U=8 -> 8e-4 at U=32). Accuracy held at ~2.7%.

3. **Drive the model with one analytic scalar (v2).** Predict the whole correlator
   from a single number with its own closed form: the local moment
   <(S^z)^2> = (1 - 2 d(U))/4, with d(U) the analytic Lieb-Wu double occupancy. Made
   the model fully predictive (no diagonalization for the scalar) at ~0.4% cost.

4. **Use the cross-check residual as a diagnostic.** The residual's SHAPE localizes
   the error. A large residual peaking exactly at U=0 (where the model must be exact)
   pointed straight at an on-site sign error (+1/8 vs -1/8); fixing it cut the residual
   ~60x. The cross-check earns its keep by saying WHERE you are wrong.

5. **Separate EXACT-cheap from EFFECTIVE-model observables (v2).** In 1D the double
   occupancy and the energy are EXACT and cheap via Lieb-Wu integrals (verified vs ED
   up to finite-size). The spatial correlator is only an effective model (~2.5%).
   Knowing which is which stops you chasing exactness where it does not exist.

6. **Verify against a known closed-form limit at machine precision.** At least one
   point must be exactly checkable (U=0 free fermion, hit to 1e-16). If the model
   misses it, stop and fix before trusting anything else. The integrity anchor.

7. **Normalize the residual to the observable's own scale.** "RMS 2e-3" alone is
   meaningless; "2e-3 vs a correlator of 0.08, ~2.5%" is honest.

8. **Use numerically stable forms.** The Fermi factor overflowed at large U (NaN at
   U=8); the logistic form sigma, sigma(1-sigma) fixed it. Stability is part of "as
   efficient as possible."

9. **Cross-check against a formula that BREAKS, and read the break (v4).** When an
   approximate analytic handle (weak-coupling K_rho) leaves the physical range -- it
   dropped below the exact floor 1/2 above U~8 -- the DISAGREEMENT located the
   formula's regime boundary, and told you which side is right: the one respecting the
   exact bound (ED). Disagreement is information about the approximation, not failure
   of the measurement.

10. **Bracket an observable between its two exact limits (v4).** K_rho is exact at
    U=0 (=1) and U->infinity (=1/2). Extract in between from ED; the limits validate
    the endpoints, the monotonic trend validates the interior. You do not need an
    exact interior to trust a bracketed monotonic extraction.

11. **Calibrate the convention on an exact limit (v4).** The structure-factor slope
    has a convention-dependent prefactor; fixing it at U=0 (K_rho=1, known exactly)
    makes every other point an honest relative extraction with no free fudge.

12. **Verify a from-memory equation against a known limit BEFORE trusting it (v5).**
    The exact Bethe dressed-charge: a first naive analytic reduction of the kernel gave
    K_rho = 2 at U=0 (must be 1). The U=0 check caught it instantly; the corrected
    numerical kernel reproduced xi = sqrt2 (K_rho = 1) and then matched ED to 0.1-0.4%.
    Without that check a confidently-wrong "exact" curve would have shipped. This is
    the highest-risk case of entry #6: a reconstructed analytic derivation is exactly
    where the limit-check is non-negotiable.

13. **At a vanishing point, use an integrated/globally-signed quantity, not a local
    endpoint derivative (v6).** The charge velocity u = eps'(Q)/2pi rho(Q) reads the
    SLOPE of the dressed energy exactly where it vanishes, at the Fermi edge; on a
    finite grid that diverged at small U. The robust replacement is the finite-size
    Casimir energy E0(L) = e_inf L - (pi c v)/(6L), an integrated quantity (just
    ground-state energies, no boundary slope), which recovered the exact Heisenberg
    spinon velocity pi/2 to 1.5%. The same idea makes the framework vacuum robust:
    V4 = (2 Im tau)^4 |E4|^2 is a manifest square, so its zero at omega is automatically
    a clean minimum. Globally-signed beats fragile-local at a zero.

14. **Verify a method against an exactly-known instance before applying it (v6).**
    Before extracting any Hubbard velocity, the Casimir machinery was checked on the
    Heisenberg ring, whose spinon velocity pi/2 is known exactly. Only after it
    recovered pi/2 (with the right convergence trend) was it trusted on the Hubbard
    spin sector. Verify the tool on a known answer, then use it.

15. **Use a structural (not numerical) prediction as the strongest check (v7).** The
    conformal tower predicts not just the leading dimension (1/2, approached with a log
    correction) but a DEGENERACY: the lowest triplet and lowest excited singlet must
    coincide (the SU(2)_1 primary multiplet). That degeneracy held to all printed
    digits at every L. A predicted exact degeneracy is a sharper test than a numerical
    value with finite-size drift, because it has no free knob.

16. **When one input to a combination is contaminated, swap in an exact value rather
    than fighting the contamination (v8).** The charge velocity from the curvature
    ratio failed because the particle-number curvature mixes charge and spin at L<=12.
    The fix was not a better extraction or a bigger lattice: it was replacing that
    curvature with the exact K_rho (v5) in u_rho = pi (L/2)(d2E/dPhi2)/K_rho. Suddenly
    it tracked sqrt2 -> 2 and cross-checked the independent Bethe velocity to ~1%. If
    you already KNOW one factor exactly, do not re-measure it badly.

17. **The hypothesized fix is not always the real fix; check before grinding (v8).**
    The open items all said "needs a bigger lattice". L=16 turned out reachable, but the
    charge velocity was actually unlocked by the exact K_rho at L=12; L=16 only
    confirmed it. Test the cheap hypothesis (does the exact input fix it at small L?)
    before paying for the expensive one (minutes per flux solve at L=16).

18. **A "velocity-free" ratio is only velocity-free if both pieces share ONE velocity;
    when it breaks, the break itself measures the physics (v9).** The doped charge
    tower was probed by R = gap(4k_F)/gap(2k_F), expected to equal 4K_rho/(1+K_rho) and
    so to read K_rho with no fitted velocity. It is EXACT at U=0 (R=2.000, the anchor),
    but at U>0 R(ED) RISES (2.18->2.80) while 4K/(1+K) FALLS (1.90->1.53). The
    disagreement is not finite-size noise: 4k_F is pure charge (one velocity u_rho) but
    2k_F carries charge AND spin, so its gap mixes u_rho and u_sigma. The cancellation
    only holds when u_rho=u_sigma, i.e. at U=0; the monotonic rise of R is a clean,
    anchored signature of SPIN-CHARGE SEPARATION. Same lesson as #9: read the break,
    don't paper over it. And it specifies the corrected probe (a ratio of two PURE-charge
    gaps, both set by u_rho) instead of a vague "needs bigger lattice".

19. **The fix the break named, executed: pick the PURE-sector operator, then calibrate
    the finite-size velocity on the exact limit (v10).** v9's break said "use only the
    pure-charge 4k_F operator." Done: x_4(ED) = gap(4k_F)*L/(2 pi u_rho) with u_rho the
    v8 charge velocity. It now TRACKS 2 K_rho across U=0..8 (no divergence), with a raw
    deficit that is small and FLAT in U (~2-3%) -- the signature of a finite-size velocity
    renormalisation, not a model error. Calibrating that one factor at the exact U=0 point
    (#11) brings the doped-charge leading dimension onto 2 K_rho to < 1%. Two prior
    verified results (u_rho v8, K_rho v5) combine into a new one; the break-then-fix is
    the whole loop in two versions.

20. **When a "bigger lattice" check is unreachable, prove the finite-size claim at the
    EXACT limit instead, then validate the cheap route against the one lattice you do
    have (v11).** v10's deficit was "finite-size"; the clean confirmation would be a
    second closed-shell lattice, but the next one (L=20, quarter filling) is 240M states,
    out of brute-force ED reach. So the deficit was instead shown to vanish at the U=0
    anchor, where the gap (free-fermion DP) and the velocity (v_F=sqrt2) are EXACT at any
    L: x_4(U=0,L) -> 2 as ~1/L^2 (fit x_4 = 2.0000 - 3.3/L^2). The free-fermion gap at
    L=12 reproduces the many-body ED gap EXACTLY (1.46410), which is what licenses the
    cheap route for L=20..44. Don't fake the lattice you can't run; move the check to the
    limit where it is exact, and anchor the cheap method on the lattice you can run (#5,#6).

21. **A detected effect becomes a measurement when you solve for its parameters and
    cross-check ONE of them independently (v12).** v9 saw the 2k_F/4k_F ratio rise and
    called it spin-charge separation. v12 turns that into numbers: two gaps + one exact
    K_rho determine the two velocities (u_rho from the pure-charge 4k_F gap, u_sigma from
    the charge+spin 2k_F gap). They coincide at the U=0 anchor (= v_F, the no-separation
    point) and split with U (u_rho 1.40->1.90, u_sigma 1.40->0.50; ratio 1.0->3.8). The
    extraction is JUST-determined (2 gaps, 2 unknowns), so it has no internal check -- which
    is exactly why one leg must be checked externally: u_rho(spectral) matches the v8 flux-
    stiffness u_rho to ~2-3%. Be explicit about what is verified (u_rho) vs merely extracted
    (u_sigma, anchored only at U=0); name the independent check that would upgrade it (the
    S^2-resolved triplet gap). A just-determined fit is a result only with an outside anchor.

22. **The independent check is not a formality -- run it; here it CORRECTED the earlier
    number (v13).** v12 flagged u_sigma as extracted-not-verified. v13 measured u_sigma a
    second way -- the SPIN STIFFNESS (a spin twist: up +Phi, down -Phi; integrated ground-
    state energy, the robust kind, #13) -- and it disagreed with the v12 2k_F-gap extraction
    by up to ~29% (agreeing only at the U=0 anchor). The spin stiffness wins: no operator-
    dimension assumption, exact U=0 calibration (spin twist == charge twist for free
    fermions, so u_sigma(0)=u_rho(0)=1.4304 with no free constant). Lesson: when a value is
    "extracted, not verified", the verification can come back negative -- and that is the
    check earning its keep (#4). Bonus: replacing the spectral-gap u_sigma with the spin-
    stiffness u_sigma puts BOTH velocities on one consistent integrated method (charge twist
    -> u_rho, spin twist -> u_sigma), which is cleaner than mixing a gap with a stiffness.

23. **Before trusting a hard exact computation, validate the SAME machinery on its
    solvable cousin; if the target route is fragile, bracket between exact limits (v14).**
    Goal: the exact Bethe spin velocity. Built the dressed-energy solver and first checked
    it on the CHARGE velocity (finite Fermi point, known refs) -- it reproduced v_c at strong
    coupling (1.92 vs 1.93 at U=8), so the machinery is sound. Then the SPIN velocity: at
    zero field the spin Fermi point is at Lambda->infinity, the endpoint slope is a 0/0 limit
    at a truncated grid edge, and it returned unphysical (negative) values. That is entry #13
    in its sharpest form -- and the cousin-validation is what proves the failure is the
    physics/route, not a coding bug. So u_sigma was verified the robust way instead: bracket
    between its two EXACT limits (U=0 -> v_F, U->inf -> 0), with the v13 stiffness monotone
    inside (#10). Lesson: a fragile exact route is not a dead end if you (a) prove the code is
    right on the solvable case, and (b) fall back to exact-limit bracketing -- and you name
    the integrated reformulation that would finish the job, rather than grinding the slope.

24. **When the EXACT check is blocked, a second INDEPENDENT approximate route still buys
    confidence -- if it shares only the anchor, and you read its disagreement as information
    (v15).** The exact Bethe u_sigma was unreachable (v14). So u_sigma was measured a second
    way in ED -- the lowest TRIPLET gap (a finite-size spin susceptibility, an EXCITATION
    energy) -- sharing nothing with the v13 spin stiffness (a ground-state TWIST response)
    except the exact U=0 calibration. They agree at U=0 and bracket u_sigma within ~8-12%
    across U, the triplet route systematically low. The disagreement is not noise: it is the
    SU(2)_1 marginal log correction, which the excitation gap carries and the integrated
    stiffness does not -- so the stiffness stays the trusted value and the triplet corroborates
    the trend. Two methods that share only the anchor turn "one robust number" into "two
    independent numbers that agree to ~10%", which is real confidence even without the exact
    curve. Honesty rule kept: the marginal-correction explanation is LABELLED as the likely
    cause (it can't be scaled away -- L=12 is the only closed shell at n=0.5), not asserted.

25. **When the exact answer is out of reach HERE, borrow it from the nearest case where it
    IS known -- to validate the method and locate the truth (v16).** The exact quarter-filling
    u_sigma was unreachable, but at HALF filling the spin velocity has a closed form (Bessel:
    2 I_1(2pi/U)/I_0(2pi/U), validated by its U->0 and U->inf limits). Testing the two ED
    routes against THAT exact value showed, at every U: triplet < exact < stiffness, with the
    exact value closer to the stiffness, and the stiffness converging toward it with L. So the
    bracket method is validated against an exact reference, the stiffness is confirmed the
    better estimate, and the earlier "marginal correction makes the triplet low" claim (v15) is
    confirmed -- now severe at half filling, where that correction is strongest. The payoff
    transfers: the quarter-filling exact u_sigma is bracketed by [v15, v13] and sits closer to
    v13. Lesson: a solvable neighbour (different filling, same physics) both validates your
    approximate machinery AND bounds the unsolved case -- worth more than grinding the
    intractable direct route. The exact half-filling result is also the validator any future
    general-n Bethe solver must reproduce before being trusted at n=0.5.

26. **To prove a residual gap is a MECHANISM and not noise, vary the parameter that controls
    it and watch it move predictably (v17).** The ~12% stiffness-vs-triplet gap in u_sigma was
    attributed to the SU(2)_1 marginal correction. To test that, vary FILLING: the marginal
    coupling peaks at the commensurate half-filling point and is suppressed by doping. The gap
    obeyed exactly that -- ~7-14% across the doped fillings (n=0.5, 0.833) but 17-62% at half
    filling. A named effect predicts its own parameter dependence; noise does not. Two bonuses
    fell out: (a) the velocity prefactor pi(L/2) is universal -- it hits v_F to ~1% at every
    filling and size tested, so the rule scales rather than being tuned to one lattice; (b) the
    counter-intuitive payoff -- for THIS observable doping HELPS (smaller correction), so the
    doped liquid the package targets is the easy regime, not the hard one. Lesson for recording
    a discovery: a result is only trustworthy once you have shown it generalizes (size, filling)
    and have turned its leftover error into a mechanism with a parameter knob -- see the frame-
    of-reference checklist below.

27. **An exact solution can OVERTURN your own earlier inference -- welcome it, and fix the route
    that failed rather than the quantity (v18).** The exact quarter-filling u_sigma was finally
    computed via the integrated Bethe spin velocity. v14's failure was reading the dressed-energy
    velocity at the spin Fermi point Lambda->infinity (a 0/0 limit at a grid edge -> noise). The
    fix was not a new quantity but a new READOUT of the same one: the velocity PROFILE v(Lambda)
    has a flat PLATEAU at moderate Lambda (the asymptotic value) before grid noise; read the
    plateau, not the endpoint. Validated against the half-filling Bessel curve to 0.1-0.2%. The
    payoff was a correction to MY OWN v16: I had transferred the half-filling bracket
    (triplet < exact < stiffness) to quarter filling; the exact value turned out to lie BELOW BOTH
    ED routes there. The transfer assumed a structure that does not survive doping (v17's
    mechanism: the marginal correction that bracketed the exact at half filling is suppressed by
    doping, so both finite-size routes simply overestimate). Two lessons: (a) when a route is
    fragile, change the readout (plateau vs endpoint), not the physics; (b) an inference is not a
    result -- v16 "located" u_sigma by transfer and was wrong; only the exact computation settled
    it. Keep inferences labelled as inferences until an exact handle confirms or kills them.

28. **When two pieces look like contradictions, sweep the parameter between them -- a smooth
    crossover usually unifies them under one mechanism (v19).** v16 said triplet < exact <
    stiffness (half filling); v18 said exact < both (quarter filling). Apparent tension. Sweeping
    FILLING resolved it: exact/triplet climbs smoothly 0.84 -> 0.99 as n: 0.5 -> 0.833 (the exact
    approaching the triplet from below), then the triplet collapses at n=1 (marginal correction)
    and the exact ends up above it. So the stiffness is the upper envelope at EVERY filling (always
    an overestimate), and the triplet is the single route that crosses -- the half-filling
    "bracket" is just the doped ordering after the triplet has been dragged below the exact by the
    commensurate-point marginal correction. One mechanism (the filling-dependent SU(2)_1 marginal
    correction, v17) generates both regimes. Lesson: two exact facts at two parameter values are
    not a contradiction to argue about -- they are two points on a curve; compute the curve.

29. **A sparse/Fourier reformulation can crack one wall yet expose a deeper, structural one --
    characterize the new wall, don't paper it (v20).** The dense dressed-energy solver hit a
    resolution wall below U=2 (sharp kernels, O(N^3) refinement too costly). Reformulating with the
    a_2 convolution solved EXACTLY in Fourier (diagonal: e^{-2u|omega|}) plus a cheap fixed-point
    loop made a fine grid affordable, and it CRACKED small U at half filling (validated vs Bessel
    to 0.1-0.5%, where the dense solver failed). But it then revealed that quarter-filling small U
    is a DIFFERENT obstruction: the velocity profile rises to a peak then crashes into the noise
    floor with NO plateau, because at low filling + small U the spin density support is too narrow
    to reach the Lambda->inf asymptotic regime. So the original wall was resolution; the remaining
    wall is structural (no asymptotic plateau exists to read). Lesson: solving the stated bottleneck
    (cost) can uncover that the real obstruction was elsewhere (structure); when it does, name the
    new wall precisely (what fails, and what kind of handle -- here a weak-coupling expansion, not a
    finer grid -- would be needed), rather than reporting a peak as if it were the plateau.

30. **When every numerical route is walled, an ANALYTIC limit can bridge the gap -- if it is
    anchored on an exact case and its transferable part is isolated honestly (v21).** Quarter-
    filling small-U u_sigma defeated three numerical routes (Lambda->inf plateau: no plateau;
    finite-field read: recipe-sensitive by 2x; ED stiffness slope: 6x off -- the lattice does not
    resolve the weak-coupling slope). Each failure was for a DIFFERENT, named reason, which is what
    promotes "we couldn't get it" to "it is genuinely walled." The way through was the weak-coupling
    expansion u_sigma = v_F - U/(2pi) - U^2/(16pi^2) + ..., whose LEADING coefficient is (a) exact
    at half filling (validated to 5 digits as the slope of the Bessel curve) and (b) filling-
    independent for a stated reason (contact U -> momentum-independent backscattering -> v_F cancels
    in the coefficient). Crucially, only the part that is anchored+argued was claimed: the linear
    term transfers to quarter filling (pinned), the U^2 curvature does NOT (it is filling-dependent
    and larger when doped, shown via the U=2 exact value), so the bridge is leading-order only and
    said so. Lesson: a wall in the numerics is not the end -- an analytic limit anchored on an exact
    case can carry the result across, provided you transfer only the coefficient you have proven and
    label the order to which it holds.

31. **A property of the OUTPUT is not a property of the COMPUTATION -- test before exploiting it
    (v22).** The connected determinant is exponentially local in its OUTPUT (folder 04 proved
    |C_spread|/|C_compact| ~ exp(-sep/xi)). The tempting inference: prune the 3^n recursion to
    spatially-local terms. Tested directly -- it FAILS: pruning that keeps 81% of the operations
    still gives 74% error at order 12, and the error GROWS with order. The small connected value is
    a delicate residual after CANCELLATION of large disconnected determinants; the "long-range"
    terms are individually large and only their full sum cancels, so dropping them by distance
    destroys the result. Lesson: an emergent property of the answer (locality, smoothness, a
    symmetry of the final number) does not license restructuring the computation that produces it --
    the intermediate quantities can be large and entangled even when the result is small and local.
    Test the exploitation on a case with a known answer before building anything on it; here the
    test redirected the whole effort (from pruning the recursion to reducing the order n via a
    control variate / atomic-limit expansion, which does not fight the cancellation).

32. **To accelerate a tool, freeze a baseline copy of it and make that the exact anchor -- the same
    discipline used for the physics (v23).** Speeding up the engine is exactly like the simulation
    arc: it needs an exact reference for every change. So fork the engine -- `engine/` FROZEN
    baseline oracle, `engine_exp/` sandbox -- and gate every experiment on reproducing the baseline
    (bit-identical where it must be: the fork was checked identical at orders 1,2; within controlled
    error where the change is an approximation, validated against an exact closed form the baseline
    ships, here G_exact_atom). This converts "did my optimization break the answer?" from a hope
    into a test, the way exact Bethe/ED did for the observables. Corollary from experiment 1: the
    engine's cost wall is the ORDER needed, and the order needed is set by the EXPANSION SCHEME, not
    only the physics -- the bare U=0 series diverges at the strong coupling we operate in (radius
    ~0.94 < U=2), while a resummation of the same orders converges. Accelerate by changing the
    expansion point/scheme (validated against the frozen baseline), not by touching the per-order
    recursion (v22 showed that breaks the cancellation).

33. **Two expansion schemes that are COMPLEMENTARY beat either alone; quantify the gain in the
    cost's own currency (here 3^(orders saved)) (v24).** On the exactly-solvable dimer the bare
    U-series (radius 4t) and the atomic/hopping series (radius U/4) have RECIPROCAL radii: bare
    converges only for U<4t, atomic only for U>4t. So neither is "better" -- they tile the (U,t)
    plane, and the right move is to pick the scheme by regime. Because cost ~ 3^n in the order n,
    the efficiency gain is exponential in the orders saved: gain = 3^(N_bare - N_atomic), and where
    the bare series DIVERGES (the strong coupling we operate in) the gain is qualitative -- an
    impossible calculation becomes a feasible one whose cost (3^N_atomic) actually SHRINKS as the
    coupling strengthens (3^24 -> 3^6 across U/t = 6 -> 32 at eps=1e-6). Two lessons: (a) report an
    acceleration in the cost model's real units (orders -> 3^orders), not as a vague "faster"; (b) a
    scheme's value is regime-specific -- the honest deliverable is the crossover map (who wins
    where) plus the hard seam (here U~4t, where both are marginal and only resummation helps), not a
    single headline factor.

34. **Benchmark to the real wall, and let the frozen baseline surface the hidden caps (v25).**
    Asked "how much faster," the honest move was a stress test of the actual cost object -- the C_V
    connected recursion (RAM 2*2^n, time ~3^n) -- not a vague estimate. Two things came out. (a) The
    measured wall is not what you assume: on a 3 GB box C_V caps at order 27 by RAM (2.0 GB), but the
    3^n TIME wall hits first (~n=24 in minutes, n=27 ~ 5 h/call), and BEFORE either, the baseline
    caps on FIXED BUFFERS (sub[16], MAXDIM=18) that have nothing to do with RAM -- the frozen
    baseline vs raised-buffer sandbox is exactly what surfaced them, validated bit-identical at
    n<=16. (b) When the two engines are still the same code, "how much faster" is not two binaries
    racing -- it is which SCHEME converges within the shared wall: the atomic scheme finishes a
    strong-coupling evaluation at order 16 (measured 1.26 s, 1.05 MB) while the bare scheme diverges
    and never finishes, even marched to the 3 GB / multi-hour ceiling. Lesson: measure the cost
    object directly, report the wall you actually hit (often a buffer, not RAM/time), and express the
    gain as convergence-within-the-wall when the speedup is a scheme change rather than a code change.


35. **Remove fixed buffers and make the tool crash-safe by default, so a long run never silently caps
    or loses data (v26).** Two lessons compounded. (a) The v25 stress test had been capping on hidden
    fixed buffers (sub[16], MAXDIM=18), not on RAM/time -- so the fix is to delete the buffers, not
    raise them: every order array in the recursion became a size-n VLA (sub[n], M[m*m], rs[n+1]...),
    MAXDIM was removed, and C_V's two mallocs are now checked (return NaN, never segfault). Validated
    by the frozen-baseline gate: bit-identical at n<=16, 194/194, and now runs uncapped -- the wall is
    finally a genuine resource wall (time first ~n=20-24, RAM guard at n=28 on 4 GB). (b) A run that
    takes minutes per order WILL get Ctrl-C'd or OOM'd, so the data must be safe by construction, not
    by luck: write each completed row to a log and fflush() it immediately (on disk before the next,
    slower order begins), guard RAM to stop gracefully before OOM, and install an async-signal-safe
    SIGINT/SIGTERM handler that just names the log. Tested with a real interrupt mid-call: the log
    kept every completed row. Lesson: when a measurement loop is expensive and open-ended, default to
    durable incremental logging + graceful resource guards + signal handling; "it'll probably finish"
    is not a data-retention plan. Corollary on honesty: "wire it in fully" was delivered as the
    buffer-free, crash-safe INFRASTRUCTURE plus an explicit statement that the full general-lattice
    atomic series is still gated by the missing high-order time-integration driver (cdet_order is
    n=1,2 only) -- the scheme is validated (v23/v24), the integration path is the real next build.
    Naming the gate beats claiming completion.


36. **Open the gate, then validate the new path against the old one where they overlap (v27).** The
    high-order series had been blocked for every scheme by one missing piece: cdet_order integrates
    the vertex times only for n=1,2. The fix was to build the general-n time integration as a Monte
    Carlo over vertex times and sites (cdet_order_mc), using the SAME integrand (C_V, lattice_G0, the
    L*/n! convention) so the new path overlaps the old one at n=1,2. That overlap is the validation:
    the MC reproduces the frozen baseline at n=1 and n=2 sub-sigma at 1e6 samples, with the error bar
    shrinking ~1/sqrt(nmc). Converging to the RIGHT value (not many-sigma off) is what certifies the
    estimator's measure/prefactor -- a wrong (L*beta)^n or 1/n! would converge tightly to a wrong
    number. With that anchored, n=3,4 (baseline NaN) are trustworthy first high-order terms. Lesson:
    when you add a new computational path, make it share the integrand/convention of a trusted path
    so a region of overlap exists, and certify the new path THERE before believing it where no check
    exists. Corollary: the wall simply moved -- the MC integrand is sign-oscillating, so variance per
    sample grows with order (the diagrammatic sign problem). That is now the real high-order wall (not
    RAM, not a buffer), and it is exactly the quantity a better reference reduces -- so the atomic
    reference (v23/v24) is the right next lever, now unblocked by this path.


37. **When a wall looks like an access-pattern problem, check the literature for the canonical
    rewrite -- then measure whether it actually helps YOUR regime (v28).** The 3^n submask sum has a
    scattered access pattern; the obvious wish is "make it contiguous." That wish maps to a real named
    result: the scattered sum IS a subset convolution, and the zeta/Mobius (Yates/butterfly) transform
    computes it in O(2^n n^2) with passes that touch only contiguous memory (Bjorklund et al., STOC
    2007). A POC confirmed the rewrite is CORRECT (reproduces the naive convolution to ~1e-12). But
    measuring it in our regime killed it as a speedup: (a) it is SLOWER at reachable orders (the ranked
    embedding's n+1 transforms + n^2 rank-products are a heavy constant; the wall-time crossover is
    ~n=20-22, past the RAM wall); (b) it uses MORE memory (n+1 popcount ranks -> O(2^n n)), moving the
    RAM wall the WRONG way; (c) it loses ~7 digits on benign data (Mobius alternating +/-), and our
    connected value is a cancellation residual (#31), so precision is our worst enemy amplified --
    practitioners avoid it for this reason. Lesson: the canonical rewrite is worth knowing and its
    contiguity is real (it is what makes out-of-core streaming feasible at all), but "asymptotically
    faster / theoretically contiguous" is not "better here" -- measure the constant, the memory
    direction, and the precision on YOUR data before adopting. Corollary: the one true payoff of the
    contiguous form is enabling blocked external-memory streaming past the RAM wall; the lever for
    going faster WITHIN RAM stays reducing n (atomic reference), the opposite (and penalty-free) trade.


38. **Re-measure past the crossover before declaring a method dead; separate fixed bias from
    recoverable rounding by adding precision (v29).** v28 called the fast (butterfly) subset
    convolution "slower in our regime" -- but had only measured to n=18, just below the crossover.
    Re-measured in RAM: the crossover is n=19, and the fast form then wins and keeps winning (n=20:
    1.74x, n=21: 2.70x, growing). The honest correction: it DOES help in RAM for n>=19; its real cost
    is memory (n+1 popcount ranks, ~(n+1)/2x more RAM -> RAM wall a few orders earlier), so it is a
    speed-vs-RAM trade in a window, not a dead end. Lesson: a constant-heavy method can sit below its
    asymptotic crossover exactly in the range you first test; measure on BOTH sides of the predicted
    crossover before concluding. Second strand: the butterfly's accuracy loss is NOT a fixed ratio you
    can scale away -- it grows with n (Mobius alternating +/- cancellation) and SHRINKS with precision
    (long double cut it 4-14x), which is the diagnostic that distinguishes recoverable rounding from
    systematic bias. The MC control variate cannot fix it (that reduces statistical variance; this is
    deterministic), but the control-variate PRINCIPLE -- subtract a known reference to shrink the
    residual -- is the cure and is identical to the atomic-reference lever, since the cancellation is
    bad precisely because the value is a tiny residual of huge terms (#31). Diagnostic rule: vary
    precision to classify an error (fixed bias is precision-immune; cancellation is not), and shrink
    the residual at its source (better reference) rather than correcting after the fact.


39. **Quantify the lever on the exactly-solvable proxy before paying for the hard implementation
    (v30).** The atomic/dressed reference had been argued (v23 Pade, v24 dimer radii, v29 cancellation)
    but never quantified as a single order-reduction number against an exact oracle. The atom does it
    cleanly: the U-series has a fixed complex branch point (|U_sing|=0.9415), so bare (around U=0)
    diverges at U=2; a reference shifted toward the target (Taylor around U0>0, a proxy for dressing
    the reference) has a larger radius and converges. Measured vs the closed form (confirmed against
    the C engine): order to 1e-6 at U=2 goes from NEVER (bare) to 11 (U0=1.5) to 3 (U0=1.9), and the
    largest single term collapses from 3.8e12 to ~0.2 -- i.e. the SAME shift that reduces the order
    also removes the catastrophic cancellation (the v29 cure), because both are symptoms of the result
    being a tiny residual of huge terms. Lesson: when the real implementation is expensive and risky
    (here the counterterm-correct lattice wiring), first nail the payoff on an exactly-solvable proxy
    so the target is a hard number, not a hope -- and watch for the bonus where one mechanism fixes two
    symptoms. Honest corollary: a quantified proxy is not the implementation; the C wiring in
    cdet_order_mc (dressed reference + counterterm to avoid double-counting) remains the build.


40. **"Random access" is about the schedule, not the data -- a known processing order can be blocked
    out-of-core (v31; corrects v28/v29).** I had said out-of-core on the scattered submask recursion
    was hopeless. That was right only for NAIVE paging (let the OS fault on random addresses). The
    user pushed: we process the 2^n in a specific order, so schedule the disk traffic instead of
    leaving it to chance. Correct -- because the submask lattice FACTORIZES over a bit-split
    mask=(h,l): sm subset mask <=> sm_H subset h AND sm_L subset l. The recursion becomes a block-
    level subset recursion; processing h in increasing order, building block h needs only blocks
    hs subset h and h-minus-hs, loaded one at a time. Validated: blocked matches flat C_V to ~1e-20
    (EXACT arithmetic, no Mobius -> no accuracy loss), peak RAM a FIXED 3 blocks = O(2^nL) independent
    of n (43x-171x less at n=12-18, growing without bound; the 2^n lives on disk). Lessons: (i) before
    calling an access pattern unblockable, check whether the SCHEDULE is known -- a deterministic
    order can almost always be tiled even if the address pattern looks random; (ii) match the tool to
    the real criteria -- accuracy + RAM + HDD-overflow (speed irrelevant) selects blocking (exact,
    RAM-bounded, I/O-heavy) and rejects the butterfly (less accurate, more RAM, faster) which
    optimizes the one axis that did not matter; (iii) say plainly when an earlier claim was too
    strong -- "I was wrong about hopeless" is a result, not an embarrassment.


41. **The control variate's power is correlation, not accuracy -- which is why it shines at low order
    and stalls at high order (v32).** The user proposed pairing a cheap 'generated' value with the
    exact 'calculated' one and correcting the former by the latter -- the control variate, already in
    02_control_variate. Its result makes the principle vivid: a surrogate only 11.7% accurate gives
    71x variance reduction because its correlation with the exact is 0.993 (reduction = 1/(1-rho^2),
    independent of accuracy). So the user's instinct is right: an inaccurate-but-correlated cheap
    version is exactly what you want. But measuring it at HIGH order (engine_exp/cv_highorder.c) shows
    the catch: simple parametric references (decoupled atoms, shifted-mu, weak-hop) DE-CORRELATE with
    the full C_V (|rho| <= ~0.7, erratic -> only 1-2x), because the high-order connected value is a
    sign-oscillating residual that a fixed reference cannot track -- getting high correlation there is
    as hard as the sign problem itself. Lessons: (i) for a control variate, chase CORRELATION not
    accuracy -- a crude surrogate can win big if it tracks the target; (ii) it is COMBINE, not
    flip/alternate -- the gain is the correlation-weighted correction at the same order, not swapping
    methods per order; (iii) the butterfly is not a CV partner (same quantity, less accurate -- a CV
    needs a cheaper correlated observable with a known mean); (iv) where a fixed reference fails, the
    surrogate must be ADAPTIVE/LEARNED (the TCI surrogate that hit rho=0.993 was data-driven) -- that
    is the high-order path, with high correlation the open problem.


42. **The surrogate we already built from the patterns IS the control variate -- at the OBSERVABLE
    level, where v32 was not looking (v33).** v32 closed with 'high order needs a learned/adaptive
    surrogate,' which overlooked the custom analytic reference we built from the engine's own
    patterns (Lieb-Wu analytic moment -> spin-correlator shape; K_rho; spin/charge velocities; CFT
    tail). The resolution is a LEVEL distinction: v32 tested PER-SAMPLE surrogates (approximations of
    C_V at each random vertex-time config, to cut MC sign-variance), and the learned patterns are not
    per-sample quantities -- they describe the CONVERGED observable, so they cannot plug in there.
    But at the observable level they are an excellent control variate: learned_reference_cv.py
    measures rho=0.998 between the analytic prediction and the exact ED correlator over a (U,r) grid
    -> 1/(1-rho^2)=229x variance reduction (199x measured directly), versus v32's per-sample
    parametric references at rho<=0.7 -> 1-2x: ~100x stronger, and already built. Lesson: there are
    TWO distinct hard problems -- per-sample sign-variance (v32's level, where simple references fail)
    and the observable / slow-IR convergence (the learned patterns' level, where they win). When a
    'we need a new surrogate' conclusion appears, check whether a custom reference already exists at a
    DIFFERENT level first. Honest gap: this reference is the spin correlator; the DiagMC computes the
    Green's function, whose learned reference (Luttinger-liquid G asymptotics) is DETERMINED by K_rho
    + velocities (both in hand) -- constructible, not yet assembled and subtracted.

### #43 -- Wiring the validated accelerations as switchable config modes (and what that exposed) (v34)

v33 admitted the accelerations were standalone POCs, not options on the solver. v34 wires the validated
ones into ONE driver, cdet_order_mc_cfg (engine_exp/cdet_config.{h,c}), with a mode toggle; the frozen
baseline is untouched and all of it lives in engine_exp/. Three modes, three gates
(engine_exp/cdet_config_validate.c, all pass): CDET_PLAIN is BIT-IDENTICAL to cdet_order_mc (the wrapper
does not perturb the reference path); CDET_BLOCKED routes each sample's C_V through the v31 out-of-core
bit-split blocking and reproduces PLAIN to 1.1e-12 (RAM bounded to ~3*2^nL doubles, the 2^n array on
disk); CDET_CVAR subtracts a correlated shifted-mu reference and is UNBIASED (1.46 / 0.16 sigma from the
frozen baseline). The butterfly is deliberately excluded (shelved v29). The integration matters less
than what CVAR's honest accounting exposed: rho=0.98/0.92 gives a POTENTIAL 27x/6.5x reduction, but ONLY
if E[Y] is known exactly; with E[Y] from an MC pilot, the pilot's own variance (beta^2 Var(Y)/P)
reintroduces what the correlation removed, so the measured NET reduction is 1.00x. (An earlier draft
omitted the pilot term from the error bar and reported a spurious "7.6 sigma bias" -- it was an
undercounted error, not a bias; fixed.) This quantifies end-to-end why the control variate needs an
ANALYTIC reference mean: CVAR is correct plumbing, and dropping a known E[Y] (atomic counterterm /
learned-G) in makes the 6-27x real. Two corrections in the same spirit: (a) v33 said blocked_cv "still
has the h=0 bug" -- WRONG, it was fixed in v31 and reproduces flat C_V to ~1e-20 (re-confirmed, wired
as-is); (b) a discrepancy chased to ground: the MC estimator and cdet_order appeared to disagree at
tau_out=1.5,tau_in=0.5 (n=1: 0.18 vs -0.83). ROOT CAUSE was integrate_piecewise_1d/2d (quad.c) sizing
its Gauss-Legendre node arrays as fixed double[64]; gl_grid_1d(np) writes np entries, so np>64 overflows
the stack -- I had read cdet_order at np=120 (corrupt), so -0.83 was garbage, never a real value. There
is NO real discrepancy: at safe np the quadrature is converged from np=8 (identical to 12 digits) and
the MC matches it at BOTH parameter sets and n=1,2 (<1 sigma at 20M; now standing gate 4). FIXED in the
sandbox: quad.c sizes nodes/wts to np (engine_exp only); bit-identical for np<=64 (C_V n=8,12,16 and
cdet_order(1,2) unchanged, engine_exp still 194/194), and np>64 now works. CORRECTION to my own earlier
v34 wording: NOT "only safe at np=40" -- safe & converged for every np, np=40 was never special. engine/
left frozen (carries the original buffers).

### #44 -- Refreshing the frozen baseline: promote validated improvements, prove nothing moved (v35)

The two-engine method is freeze a pristine baseline, validate every change in the sandbox bit-identical,
and -- the step taken here -- PROMOTE the validated changes back into the baseline when asked. v35
refreshed engine/ by copying in the only two core files that differed from engine_exp/ and had been
validated bit-identical in output: cdet_engine.c (v26 buffer removal MAXDIM[18]/sub[16] -> dynamic,
sized to n, plus an OOM-safe NaN guard) and quad.c (v34 node arrays sized to np). The discipline is the
point: because both had been proven to reproduce the frozen numbers exactly, the promotion was safe and
the proof is mechanical -- after the swap, engine/ still gives cdet_order(1,2) = -0.5082750022348369 /
0.44040518398732875 and C_V n=8,12,16 = 4.107893936632339e-08 / 5.2004546552889602e-10 /
3.6922703728839982e-11 to the last digit, and 194/194 vs the Python reference. What the refresh BOUGHT:
engine/ now runs C_V for n>16 (n=17,18 confirmed) and cdet_order for np>64 (np=96 reproduces the np<=64
value) -- neither possible before. Methodological consequence, stated plainly: the old 'pristine = still
has the MAXDIM[18]/sub[16]/node[64] caps' invariant is RETIRED. The baseline's defining property is now
'reproduces the invariant constants + Python 194/194 AND is buffer-free / OOM-safe.' engine/ core and
engine_exp/ core are intentionally identical after this; engine_exp/ additionally carries the
experimental tools (diagmc, cdet_config, blocked_cv). The two-engine *core* bit-identical gate becomes
trivially true; the real standing check is the invariant constants above. Next unvalidated work forks
from this refreshed baseline into engine_exp/ as before.

### #45 -- Begin 2D: the interacting engine validated against exact 2D diagonalization (v36)

The whole 1D program (Bethe/ED-anchored) was a solved model done carefully. v36 starts the unsolved
direction -- 2D -- the honest way: foundation first, validated against an independent exact reference,
with scope stated plainly. The non-interacting 2D propagator already existed (square2d_init, separable
circulant eps=-2t(cos kx+cos ky)); v36 feeds it into the connected-determinant engine (C_V is
geometry-blind, so cdet_order with hexring_init->square2d_init and L->N=Lx*Ly is the whole change) and
validates the first interacting orders. The anchor is new and is the point: exact diagonalization of the
small Hubbard cluster (hubbard_ed.py, grand-canonical Lehmann G in the engine's convention). Pinned and
verified: cdet_order(n) = N * a_n, a_n the U^n Taylor coefficient of the exactly-diagonalized local G,
sign +1, IDENTICAL in 1D and 2D at orders n=1,2 to ~1e-9; the prefactor confirmed = N across rings
N=2,3,4,5. Capstone: the engine's O(U^2) series reconstructs the exact 2D interacting G(U) with U^3
truncation error. Lesson reaffirmed: validate a NEW direction on the smallest exactly-solvable instance
before scaling -- a 2x2 ED costs nothing and turns 'the engine probably works in 2D' into 'cdet_order_2d
matches exact ED to 1e-9 at both orders.' Honest ceiling, stated as a result: 2x2 and small rings are
METHOD ANCHORS, not physics (no phases / thermodynamic limit / finite-T transition at this size); only
orders 1,2 (deterministic quadrature) are reached; higher orders need a 2D MC driver (cdet_order_mc is
1D-hardwired), and only THERE does the fermion sign problem -- the real 2D difficulty -- appear. Stripes,
pairing, the cuprate question remain far beyond this. v36 = the validated 2D foundation, nothing more.

### #46 -- 2D high order via Monte Carlo: validate first, then measure the wall (v37)

v36 proved the 2D engine at orders 1,2 (deterministic quadrature). v37 went high-order the honest way:
build the MC driver, prove it CORRECT against an exact anchor before claiming any reach, then measure the
difficulty rather than assert it. Two reusable pieces made this clean. (a) Exact high-order coefficients:
finite differences / polyfit are useless past a_2, but the Cauchy contour integral a_n = (1/2pi i) oint
G(U)/U^{n+1} dU on a small complex circle gives a_n to ~1e-13, r-independent inside the convergence disk
(needs a general complex eigendecomposition since complex U makes H complex-symmetric). That turned 'we
think the MC works at order 6' into 'MC = exact to <2 sigma at n=1..6'. (b) The driver generalization was
trivial precisely because C_V is geometry-blind -- diagmc.c's hexring became 'any prebuilt LatticeCtx + N',
nothing else changed; the recurring dividend of a geometry-blind core. The genuinely informative result is
NOT the order reached but the WALL measured: the sign-cancellation ratio R = mean(C_V)/mean(|C_V|) is
intrinsic (no exact answer needed), and Nsamp->1% ~ 1/R^2 is a tangible cost. On 2x2 the sign is benign
(7e5 samples for 1%); 4x4 costs ~260x more, beta=8 on 3x3 ~570x more -- |R| collapses geometrically in
size and inverse-T. LESSON, restated: separate 'the machine is correct' from 'the physics is hard'. A tiny
exactly-solvable cluster proves correctness to arbitrary order (contour + ED); the sign problem only shows
up with scale and cold, and must be MEASURED on systems too big to check exactly -- which is fine, because
R is self-measured. OVERCLAIM GUARD honored: reaching order 6 on 2x2 is correctness, not 'solving 2D'; and
because no naive-expansion baseline was built, NO 'CDet beats a conventional expansion' claim is made --
only 'this CDet MC is correct and the wall is here'. Overcoming the wall is the next frontier, not a result.

### #47 -- Does the determinant organization buy order reach? Measure both walls separately (v38)

The question "can CDet buy extra useful orders before the wall hits?" has a clean measured answer once you
realize there are TWO different walls and the determinant addresses only one. The engine's unit of work is
det(M) of the (n+1)x(n+1) Wick matrix -- a sum of (n+1)! signed contractions done exactly in O(n^3). So the
honest baseline is "what would sampling those contractions cost/suffer," measured on the engine's OWN
matrices (faithful, no strawman code): cost (n+1)! vs n^3 (crossover ~order 5, 5e9x by order 15 -- past
order 5 the determinant is the ONLY way to evaluate the order), and per-order cancellation perm(|M|)/|det|
that a contraction-sampler eats (grows with ORDER on every cluster, ~1.5^n on 2x2). Both say: CDet buys the
ORDER axis. The decisive honesty move was Pillar 3 -- checking the SAME ratio at FIXED order across cluster
sizes: perm/|det| SHRINKS with N (3.11->1.23), the OPPOSITE of the v37 configuration-level sign wall (R
collapses, cost ~1/R^2 grows with N and beta). That single contrast proves they are different walls: the
determinant tames within-configuration Wick cancellation (per-ORDER); the across-configuration MC sign
problem (per-SIZE/TEMPERATURE) is untouched. LESSON: when a method "helps the sign problem," ask WHICH sign
problem -- separate the per-order (combinatorial, determinant-curable) cancellation from the per-system
(physical, sampling-level) one, and measure each axis independently. OVERCLAIM GUARD: I did NOT reimplement
historical per-diagram DiagMC, so no wall-clock-vs-competitor claim; perm/|det| + (n+1)!/n^3 isolate the
MECHANISM, which is the honest, checkable statement. Net: CDet climbs the order axis cheaply; size and
temperature -- where 2D Hubbard physics is -- need different medicine, which keeps v38's "yes" from inflating.

### #48 -- Fit the wall's scaling law: the metric is right, the clean fit was an artifact (v39)

Good external suggestion: stop reporting "what order did I reach" and instead fit the decay law of R
(R~e^{-aL}, e^{-b*beta}, e^{-f}) -- that exponent is the real benchmark a variance-reduction scheme must move.
The framing is correct and adopted. The discipline lesson is in what happened when I actually fit it. First
pass at fixed mu gave a BEAUTIFUL temperature fit: b=+0.35, R^2=0.98. Tempting to bank. But fixing mu lets
the density drift as you change beta or L, so that clean line was partly a density effect, not the sign
wall. Controlling the right variable (fixed DENSITY, mu tuned per point) demolished the tidy story: the
temperature exponent FLIPPED SIGN (b=-0.05), the size axis showed a shell plateau (L=3~L=4) then collapse
(L=5) rather than an exponential, and the separable form e^{-(aN+b*beta)} failed a direct off-axis
prediction by 29 sigma. So there is NO honest single (a,b) benchmark at accessible sizes -- the per-order-3
R is dominated by finite-size momentum-shell/filling structure, and any reported exponent is fitting that
structure. LESSON (a sharp one): a high R^2 on a one-variable slice is NOT evidence of a real scaling law if
a confounder (here density) co-varies; control it before fitting, and TEST separability with an off-axis
prediction rather than assuming it. META-LESSON: a clean-looking number that would have been satisfying to
report was an artifact; catching it required deliberately trying to break it. CATCH-22 worth remembering:
the regime where the wall's law is clean (large N) is exactly where R is unmeasurably small -- the wall
blocks measuring the wall. This also corrected v37 (its beta-trend at fixed mu conflated T with density).

### #49 -- When the metric is contaminated, swapping observables may not help: test it, find the mechanism (v40)

v39 showed per-order R is shell-contaminated; the natural next move (good suggestion) is to try a more
aggregate observable that might scale cleaner -- integrated-over-orders average sign, crossover order n*,
free-energy differences, variance growth rates. The disciplined result is to actually TEST the measurable
ones rather than assume an aggregate is automatically cleaner. It is not. The integrated average sign still
sign-alternates with cluster (L=2 +0.06, L=3 -0.12, L=4 +0.02), and there is a clean MECHANISM: the physical
order weights U^n N(N beta)^n/n! are exponentially non-uniform, so the 'integral over orders' is dominated by
a single order (lowest order for U inside the convergence radius, highest computed order outside it) and
simply inherits that order's shell structure -- aggregation cannot average shell effects away when one term
carries all the weight. n* and per-order R_n inherit the same a_n shell jumps; R(mu) on a single cluster
oscillates and flips sign even between non-interacting shell levels. LESSON: a contaminated metric is not
fixed by picking a different summary statistic if they all derive from the same shell-structured a_n; locate
the CONTAMINANT (here: partial-shell filling at small N) and you find the real lever (fix the filling
fraction -- closed-shell families -- or enlarge N), which is a different and harder move than swapping
observables. OVERCLAIM GUARD: I tested integrated sign and n* and reported the negative honestly with its
mechanism; I did NOT test free-energy differences (a different thermodynamic computation) and made no claim
about them; and I did not claim the closed-shell cure works, only that the data points to it. The result is
a measured limit, not a tidy benchmark -- and the limit is the finding.

### #50 -- The contamination has an organizing variable: find it before declaring 'no diagnostic' (v41)

v40 concluded (correctly, but too broadly) that no aggregate observable from this estimator gives clean
scaling at small clusters; the fair narrowing is 'no diagnostic *as a function of N*'. The right move, prompted
by 'what single ratio affects ALL clusters, differently, encoding where each sits?', was to stop plotting
against N and ask what spectral quantity organizes the scatter. It is the Fermi-level DETUNING delta = mu -
nearest single-particle shell. At fixed T, R is a UNIVERSAL function of delta across clusters: positive below a
shell, peak at delta=0 (shell at the Fermi level), sign flip just above -- identical structure for L=2,3,4,
with only an amplitude A(N) (0.82,0.60,0.50, shrinking with N) and the cluster's own delta distinguishing them.
So the 'shell noise' was one curve sampled at scattered delta; R-vs-N looked random only because each cluster
sat at a different detuning. LESSON: before banking 'no clean scaling', search for the natural ABSCISSA -- the
contaminant itself often IS the scaling variable (here shell-filling -> detuning). A messy plot can be a clean
plot in the wrong coordinates. This converts 'no diagnostic' into 'the diagnostic is R(delta) at fixed T' and
makes the v40 cure precise (hold delta fixed). OVERCLAIM GUARD honored on the way back up: I did NOT claim a
full universal curve -- the magnitude collapses only near the shell, and the beta=2-vs-4 test showed beta*delta
is NOT a single variable, so temperature is a separate axis; the established claim is just that delta (not N)
organizes the size/filling axis. Banking the partial win honestly is the point, not inflating it to a law.

### #51 -- A messy curve can be a sum of clean pieces with different ranges; measure the ranges (v42)

The v41 collapse held only near the shell -- flagged (via a 'miniature forces' analogy) as possibly multiple
mechanisms with different ranges. The disciplined response: take the structural intuition seriously, deflate
the cosmic reading, and MEASURE. R(delta) separates into a near-shell THERMAL feature plus a cluster-specific
band-structure background. The feature's RANGE is the thermal length: its sign-flip delta* scales as T=1/beta
(delta*/T ~ 0.9-1.2 across beta=2,4,8), and on an ISOLATED shell its shape collapses vs beta*delta -- so that
piece is genuinely a function of beta*delta, which is WHY v41's fixed-beta delta-collapse worked and why the
global beta*delta collapse failed (the background, a separate scale, breaks it). LESSON: 'the collapse only
works in part of the range' is often the signature of a SUPERPOSITION -- decompose into contributions and
find each one's scale, rather than concluding 'no clean law'. A curve that won't collapse as a whole may be
two curves that each do, on different variables. OVERCLAIM GUARD, two ways: (i) the strong/weak/EM-forces
analogy is acknowledged as STRUCTURAL ONLY (distinct ranges) and explicitly disclaimed as physics -- this is
band structure, not the Standard Model; (ii) delta*/T is order-one but drifts (1.22->0.88), so 'range ~ T'
is reported as a measured trend, not an exact law, and the decomposition as demonstrated, not closed-form.
The honest hierarchy: T=1/beta (near-shell range) < shell spacing < bandwidth 8t.

### #52 -- Run the upgrade test even when you expect to pass; sometimes it corrects you (v43)

v42 said the near-shell feature is 'thermal (range ~ T)'. A sharp critique: that is 'consistent with
thermal', not 'thermal' -- upgrade it by mechanism-separation (order cutoff, alt formulations), spectral
consistency, or finite-size control. I ran the decisive ones expecting confirmation. Result was MIXED and
it corrected me. The finite-size + temperature controls (Test C) PASS cleanly: delta* is N-independent
(0.24,0.26,0.21 across N=4,9,16, while the level spacing varies a lot -> not shell-spacing) and delta* ~ T
(0.61,0.24,0.11 for beta=2,4,8). But the order-cutoff test (Test A) FAILS: the feature is qualitatively
DIFFERENT at each order -- n=1 monotonic (no peak), n=2 peak at delta=0, n=3 peak at +0.2 with opposite sign
below the shell. There is no single feature being broadened, so 'thermal broadening' is not a universal
mechanism; only the n=2 feature WIDTH is thermal-consistent. LESSON: a scaling that looks clean on one or
two axes can still fail mechanism-separation; run the order/discretisation/estimator-variation tests
BEFORE upgrading 'consistent with X' to 'is X' -- and be ready to narrow your own prior claim when they
fire. CORRECTION BANKED: v42's 'the feature is thermal' is narrowed to 'the n=2 feature width is thermal-
consistent; the feature is order-dependent and the thermal ORIGIN is underdetermined.' The reviewer was
right; the test, not the intuition, settled it. (v41's detuning-as-organizing-variable, at fixed order/T,
is unaffected -- only the v42 mechanism framing changed.)

### #53 -- Before claiming a pattern is yours, search the literature HARD; mine was already mapped (v44)

After eight iterations finding structure in the CDet sign cancellation (order, size, temperature, filling/
shell, coupling radius), a hard literature search settled originality honestly: almost all of it is known,
and the axes I had treated as separate 'walls' are recognized facets of ONE sign problem that the community
has already connected. Specifics: v38 (det removes per-order cancellation, exp-not-factorial cost) is the
DEFINING property of Rossi's connected-determinant method (PRL 2017); v37 (cost ~1/<s>^2, <s>~e^{-aN}e^{-b
beta}) is textbook DQMC scaling; v36 (convergence radius from poles in the complex-coupling plane) is the
Hubbard-atom result of Wu-Ferrero-Georges-Kozik (PRB 2017). The sharpest lesson concerns the result that
FELT most original -- v41's 'R is organized by the Fermi-shell detuning, peaking at closed shells, oscillating
with N': that is exactly the documented closed-shell 'magic-density' effect in the average sign ('Deconvolving
the components of the sign problem', arXiv 2108.00553; closed-shell sign effects, arXiv 1107.0230). The
feeling of discovery was real; the discovery was not. LESSON: excitement about a clean pattern in a toy model
is a cue to search the literature HARDER, not less -- and the honest framing of a faithful rediscovery is
'I independently re-derived mapped structure' (valuable as exact validation + methodology), never 'I found a
new connection'. Bank the literature anchor next to every banked observable. Residue, stated weakly: the
per-ORDER coefficient delta-structure differing by order (v43 Test A) I did not find stated per-order -- but
'did not find' is not 'is new', and the next step is to read the coefficient-level CDet literature before any
claim. Keep wanting the deflation: being mapped already is the normal, good outcome of working in a mature
field, and finding it yourself -- with exact cross-checks -- is the point.

### #54 -- Turn the literature map into a build: the pole is a knob, and it is the same knob (v45)

After v44 placed every finding in the literature, the constructive move was to USE the most actionable result
-- Wu-Ferrero-Georges-Kozik pole-moving -- as a real upgrade. Implemented the shifted-reference (chemical-
potential counterterm) expansion: H(xi;alpha)=[H0+alpha N]+xi(U Hint - alpha N) recovers physical H at xi=1
for ANY alpha, but alpha moves the convergence-limiting pole. EXACT (ED) verification: on a 2-site ring the
BARE series diverges (never <1e-3 in 14 orders) while the shifted series at the Hartree-scale alpha converges
at ORDER 5 -- the shift does not merely speed convergence, it makes a divergent calculation possible. Because
CDet per-order cost ~2^n, saving orders is an exponential (2^Delta K) cost cut: this is the honest reading of
'2^n reduction' -- not a cheaper subset sum, but FEWER subset sums needed. The satisfying unification: the
optimal shift alpha* came out at the Hartree scale U<n>/2, i.e. the SAME Fermi-level re-centring that defines
the detuning delta from v41/v44. One knob: the operating point sets delta=0 (closed shell, best sign); the
shift sets the reference Fermi level to the Hartree position (pole moved, fast convergence). LESSON: when a
literature search shows your toy results are known, the payoff is that the literature's CURES are now yours to
implement -- map first, build second. HONESTY GUARD: verified at the exact coefficient level and shipped as a
resummation/reference-selection tool; the one-body counterterm is NOT yet wired into the C connected-determinant
MC, so no claim the engine computes shifted CDet end-to-end (scoped v46). Frozen engine untouched (194/194).

### #55 -- The hard wiring job had an exact shortcut: a counterterm is a derivative (v46)

v45 scoped "wire the shift into the C connected-determinant" as hard (the one-body counterterm -alpha*N
breaks the engine's symmetric spin determinant). v46 found it needs NO engine surgery: -alpha*N is the
generator of mu-shifts, so counterterm insertions resum exactly into mu-derivatives of the bare coefficients.
Writing the shifted scheme as a 2D Taylor expansion about (mu-alpha, U=0) gives the closed form
b_n = sum_j (alpha^j/j!) U^(n-j) a_{n-j}^{(j)}(mu-alpha). VERIFIED two ways: the formula matches the ED
shifted coeffs to MACHINE PRECISION (1e-12..1e-17, orders 0-6); and the REAL C engine's bare coeffs
(cdet_small) fed through it reproduce the shifted coeffs to engine precision (b1 6e-6, b2 4.5e-5, limited by
np=64 quadrature + finite-diff, not the identity). A convention bite along the way: engine cdet_n(m) is the
EXTENSIVE N*a_m^local while a0=G0 is local -- the factor-of-2 (N=2) mismatch was the tell; divide by N. LESSON:
before re-architecting validated code for a new feature, check whether the feature is an EXACT transform of
what the code already outputs -- a one-body counterterm = d/dmu, a momentum shift = a phase, etc. The cheapest
correct implementation often leaves the frozen core untouched and adds a thin exact resummation. HONESTY: the
identity is exact; the engine route is engine-precision (quadrature+FD); production would sample d/dmu directly
(density insertions) -- an efficiency refinement, not a correctness gap. Frozen engine still 194/194,
cdet_order constants bit-identical.

### #56 -- A derivative you can sample: complex-mu on shared samples beats a mu-grid (v47)

v46 reached the shifted coeffs but used a mu-grid + finite differences for the mu-derivatives (a ~1e-5 FD bias
and re-runs at several mu). v47 removes both at once: evaluate each Monte-Carlo sample's connected determinant
at COMPLEX mu on a small circle and Cauchy-extract -- the exact analytic d/dmu (the density-operator insertion)
per sample, from ONE set of vertex samples. The contour points are deterministic re-evaluations of the SAME
sample, so all mu-derivatives come free of extra sampling noise and free of FD bias. Verified on the 2-site
ring: a1, a1', a2 each within 0.3 sigma of ED, the sampled mu-derivative a1' independently cross-checked
against ED's Cauchy value (not just self-consistent), and the assembled shifted b1,b2 within 0.3 sigma of ED
shifted. To do it I PORTED the engine's connected determinant to Python (D_corr/D_vac/Rossi) and validated the
port hard before trusting the sampler -- G0 to 1e-16 vs lattice_G0, and piecewise-quadrature a_1 to 1e-16 vs
ED (the kinks at the external times must be split, exactly as cdet_small does -- a single Gauss panel gave a
1e-3 error and was the tell). LESSON: when you need derivatives of a Monte-Carlo estimator, reach for analytic
continuation on the existing samples (complex-step / contour / jet) before a parameter grid -- same samples,
exact derivative, no bias, no extra runs. And validate a reimplementation to machine precision on a known case
before sampling with it. HONESTY: Python reference implementation of the production estimator (orders 1-2 to
MC stats); porting the contour into the C high-order mc2d is an unshipped optimisation; frozen engine untouched
(194/194). Chain complete: v45 exact proof -> v46 engine route -> v47 fully stochastic.

### #57 -- The same knob can have two competing optima; the win on one axis can be the loss on the other (v48)

Asked the million-dollar question head-on: does the shifted reference improve the SIGN, or only convergence?
Set it up as the cleanest possible test -- find the convergence-optimal shift (ED, min truncation error) and
the sign-optimal shift (mc2d, max |R|) for ONE case and compare. They are DIFFERENT and in TENSION:
convergence wants alpha_conv~+1.5 (mu_ref=-1.0, the Hartree/pole-moving region, ~10x better truncation error)
while the sign wants alpha_sign~+0.5 (mu_ref=0.0, the closed shell, |R_2|=0.82 vs 0.05). The convergence-
optimal shift has the WORST sign of the three points tested -- pole-moving does not move the sign wall, it
trades against it. MECHANISM that makes this honest rather than a fluke: convergence is set by the nearest
pole in the COMPLEX-U plane (Hartree shift moves it), the sign by the real-axis SHELL/detuning (best on a
closed shell) -- different physics, so generically different optimal mu_ref. LESSON: when one control
parameter governs two desiderata, do not assume optimizing one helps the other -- measure both objectives
against the SAME parameter and look for tension; the clean negative ('same knob, competing optima') is a real
result and exactly the cautious outcome the reviewer anticipated. It also REFRAMES the earlier excitement:
operating-point selection (sign) and pole-moving (convergence) are the same mu_ref but pull opposite ways.
HONESTY: single case (2x2, mu=0.5, U=4, beta=4) across orders 2-4; the mechanism argues genericity but it is
NOT proven -- a filling where the Hartree point IS a closed shell could align them (the only 'both at once'
route), which is the v50 search. Frozen engine untouched (194/194).

### #58 -- A real sign-flip is the wrong kind of cancellation for contour deformation (v49)

Plundered the one tool with a real shot at the sign wall -- Lefschetz-style CONTOUR DEFORMATION (deform the
imaginary-time integration contour so the integrand's phase flattens) -- and tested it on the genuine v48
integrand (cdet_port, validated bit-identical to the frozen ring port). It is NULL, and the reason is
structural and useful. (A) Decompose the order-1 time integral at the propagator kinks {0,ti,to,beta}:
WITHIN each analytic sector R=1.000 (the integrand is sign-coherent); the entire deficit is DISCRETE,
between sectors. A valid contour must PIN at every kink (off-axis the two propagator branches disagree ->
discontinuous integrand -> illegal deformation), so the cancellation sits exactly where no smooth contour
can reach. (B) Minimising int|.| over the pinned deformation family returns amplitude A=0 (the real axis) in
every sector, integral invariant to 0.0e+00. THE LESSON: our sign problem is a REAL SIGN-FLIP (the
determinant is real and changes sign between configs), not a complex PHASE (the e^{iS} thimbles are built to
flatten). A real, sector-coherent integrand gives a contour nothing to grip -- deforming it manufactures
only a zero-integral imaginary part and leaves the signed integral, and its discrete cancellation, untouched.
This is the concrete local face of the Troyer-Wiese NP-hardness. n=2 cross-check reproduces the v48 wall
(|R_2| 0.82 shell vs 0.04 Hartree). 08_2d_interacting/CONTOUR_DEFORMATION_RESULT.md, contour_deformation.py.
Frozen engine untouched (194/194).

### #59 -- The deformation family is a perfect-correlation covariate; covariates move the prefactor, never R (v49)

The sharp follow-up: the contour invariance makes every amplitude an UNBIASED estimator of the same integral
I, so {Re h_A} is a family of equal-mean estimators and their differences are zero-mean control variates
("covariates") with the undeformed axis A=0 as comparator -- a legitimate variance-reduction setup, and the
RIGHT question (decorrelation), distinct from the R question of #58. Tested: the optimal variance-minimising
combination gives x1.00 (zero gain), weights perfectly uniform. Diagnosis: the deformation moves only the
IMAGINARY part; the real signed integrand is identical to the axis to 1e-15 (validated against a toy whose
real part moves by 1.4, so the deformation is live, not dead). Perfectly correlated -> no covariate juice.
GENERAL CEILING worth stating once: no control variate can change R at all -- combining unbiased estimators
of one mean reduces VARIANCE, never the mean/mean-|.| ratio -- so the entire covariate family moves the
PREFACTOR, never the exponential wall. Where the same instinct DOES pay: the free-baseline control variate
(subtract the known U=0 wave, sample the small interaction remainder), a real prefactor win at weak coupling
(range reduction x8.4 at U=0.5 -> x1.5 at U=4; the strong validated version is the v33 learned IR reference,
rho=0.998, 229x). 08_2d_interacting/best_methods.py, BEST_METHODS.md. Frozen engine untouched (194/194).

### #60 -- Search for an involution; you find a symmetry (folds redundancy) but not a sign-canceller (v50)

Did the meron question by COMPUTATION, not citation: is there a site map sigma with C_V(sigma x) = -C_V(x)
(sign-cancelling involution = the prize) or +C_V(x) (exact symmetry = redundancy removal)? Tested time
reversal, sublattice translate, diagonal reflection, products, on the genuine engine weight. RESULT: (1) NO
sign-cancelling involution among the natural symmetries -- ratio C_V(sigma x)/C_V(x) came back +1 and never
-1; time reversal and translate don't even pair cleanly (map to unrelated configs). (2) An EXACT symmetry DOES
exist: 2x2 torus automorphism group |G|=8, stabilizer of the external site |G_0|=2 (the diagonal swap of the
two B-sublattice sites), with ratio +1.000 to 1e-8. It is a symmetry, not an anti-symmetry -- orbit members
have IDENTICAL sign, so nothing physical cancels. (3) Folding the discrete site-configuration sum (L^n site
assignments at fixed times) by G_0 reproduces brute force exactly (match 6.6e-17) with fewer C_V evals: 1.60x
at n=2, 1.78x at n=3, 1.88x at n=4 -> |G_0|=2x as n grows. (4) Symbolic proof: P^T H(t) P - H(t) = 0 and
[P,H(t)] = 0 are polynomial identities in the hopping t (sympy), so the fold is exact for every t, mu, beta --
G0 is a function of H, so a permutation fixing H and the external site fixes C_V. LESSON: when you ask 'is
there a pairing rule', measure the ratio C_V(sigma x)/C_V(x) -- +1 buys redundancy (an exact, sympy-provable
constant-factor saving on the site sum, growing with lattice symmetry), -1 would buy the sign, and our doped
lattice yields only the former. It folds ONE exponential factor (the L^n site space), NOT the Rossi 2^n
recursion and NOT the physical sign. 08_2d_interacting/symmetry_reduction.py, symmetry_audit_sympy.py,
SYMMETRY_REDUCTION_RESULT.md. Frozen engine untouched (194/194).

### #61 -- The fold scales with the lattice point group; column/row slices fold, they do not cancel (v51)

Tested the 'full column slice' question by computation on the 4x4 torus (where rows and columns are distinct,
unlike the 2x2 where they collapse). The stabilizer of the external site is the FULL square point group D4,
|G_0|=8 -- all four rotations and all four reflections, INCLUDING the column-slice (left-right) and row-slice
(up-down) reflections. Measured C_V(sigma x)/C_V(x) for every element: all are +1.000 to ~1e-10 (FOLD), none
is -1 (no CANCEL). Symbolically proven for all hopping t (sympy): the column/row reflections satisfy
P^T H(t) P - H(t) = 0 on the 16-site lattice. Folding the L^n site sum by the order-8 group is exact (match
3.3e-16 at n=2, 4.6e-15 at n=3) and gives 4.65x fewer C_V evals at n=2, 6.15x at n=3, climbing toward |G_0|=8
-- versus 2x on the 2x2. LESSON: the redundancy fold is set by the little group of the external site, which
GROWS with lattice symmetry (2x on 2x2 -> 8x on 4x4 -> larger on bigger clusters); a column/row slice is a
symmetry (folds), never an anti-symmetry (would cancel). Still the site-space factor only -- not the Rossi 2^n,
not the sign. square_point_stabilizer() is the generator-based finder (no L! enumeration).
08_2d_interacting/symmetry_reduction.py + symmetry_audit_sympy.py, SYMMETRY_REDUCTION_RESULT.md (v51 section).
Frozen engine untouched (194/194).

### #62 -- 45-degree slices of the cube fold too; the fold scales with dimension (v52)

Took the lattice to 3D (4x4x4 cube) and tested its 45-degree slices = the diagonal mirror planes = the axis-
swap operations. Stabilizer of the external site = full cube point group O_h, |G_0|=48 (signed axis perms), of
which 40 are 45-degree diagonal slices. Measured C_V(sigma x)/C_V(x): all diagonal slices +1.000 to ~1e-10
(FOLD), none -1 (no CANCEL). Symbolically proven for all t (sympy): the axis-swap operations satisfy
P^T H(t) P - H(t) = 0 (proven on the small cube; the identity is structural/size-independent -- isotropic
hopping is invariant under axis relabeling). Folding the N^n site sum (N=64) by the order-48 group is exact
(match 5.2e-15) giving 18.62x fewer C_V evals at n=2, climbing toward |G_0|=48. LESSON: the redundancy fold =
the little-group order of the external site, growing with BOTH size and dimension: 2x (2x2) -> 8x (4x4, D4) ->
48x (4x4x4, O_h). 45-degree slices are symmetries (fold), never anti-symmetries (cancel). Still the site-space
factor only -- not the Rossi 2^n, not the sign. cube_hopping()/cube_point_stabilizer() are the 3D finders.
08_2d_interacting/symmetry_reduction.py + symmetry_audit_sympy.py, SYMMETRY_REDUCTION_RESULT.md (v52 section).
Frozen engine untouched (194/194).

### #63 -- Inside the 2^n: the mask-fold is real but measure-zero; the subset CACHE is the generic win (v53)

Attacked the interior of the Rossi 2^n recursion with the proven symmetry machinery. (1) HONEST NEGATIVE: a
mask-level fold inside one C_V needs a vertex permutation pi with (p[s_pi(i)],t_pi(i))=(s_i,t_i). Verified it
fires EXACTLY on symmetric configs (diagonal-partner sites, equal times: masks 001<->010, 101<->110 identical
to 1e-12) but a generic config (distinct continuous times) has trivial stabilizer -- so it is NOT a generic
2^n cut (Burnside: no fixed points, no fold). (2) THE REAL INTERIOR REDUNDANCY: D_vac/D_corr depend only on
the vertex SUBSET; across an enumerated site sum at fixed times the same subsets recur massively (6.7x raw at
n=3 on 4x4). Memoizing them (cv_cached) and composing with the orbit fold (fold_site_sum_cached): n=3 4x4
total matches brute to 5.0e-15 with 2194 unique determinants vs 65536 brute subset evals = 29.9x fewer
(orbit 6.15x x cache 4.86x, independent and multiplicative), wall-clock 13.9x measured. LESSON: when a fold
fails generically, look for the same redundancy ACROSS the sum instead of WITHIN one evaluation -- the subset
is the natural cache key because the recursion's primitives depend on sets, not configs. Scope: thrives on
shared/quadrature times; does not cut the asymptotic 2^n of one isolated C_V on generic times; sign untouched.
08_2d_interacting/symmetry_reduction.py (cv_cached, fold_site_sum_cached), SYMMETRY_REDUCTION_RESULT.md (v53).
Frozen engine untouched (194/194).

### #64 -- The value channel's -1 is real but dressed; weight and sign live on low-dim slices (v54)

(1) THE -1 HUNT, CLOSED MECHANISTICALLY. Geometric ops can only fold (+1): a site permutation commuting with H
fixes the propagator. The value channel (particle-hole) was the one place a -1 could live. Measured: the
transpose identity G(-mu)(i,j,tau) = -e_i e_j G(mu)(j,i,-tau) holds off-diagonal (2.5e-11), but on the
equal-time diagonal the EXACT sum rule G(-mu)(i,i,0)+G(mu)(i,i,0)=1 (1e-15) breaks the naive -1: PH maps the
0^- convention to 0^+, difference = identity on the equal-time diagonal = a contact/DENSITY counterterm (the
v46 d/dmu object). Both naive predictions FAILED by computation (ratios non-constant, derived bare -1 off by
1e3) -- the truth is an operator identity: C_V(-mu) = -(externals-swapped C_V)(+mu) + counterterm tower. NO
per-config -1 at fixed mu in either channel; the sign wall stands; the usable product is the doping reflection
mu <-> -mu with exact corrections (composable with v45-v47). LESSON: when a derived clean factor fails
numerically, hunt the regularization -- the equal-time 0^- diagonal was the hidden assumption, and the failure
mechanism (the sum rule) is itself the exact result. (2) SLICE HIERARCHY (pattern mine, 4x4x4, n=3, mu=0.5):
classifying configs by affine-span dimension through the external, weight concentrates on low-dim slices --
1d lines x18.5 their config share at R=0.22, 2d planes x2.1 at R=0.09, 3d bulk x0.65 at R=0.004; mean|C| falls
~10x per added dimension. Locality appears as a slice hierarchy: lines/planes dominate per-config and carry
the best sign; the bulk is numerous, tiny, sign-dead. HINT BANKED for v55: slice-STRATIFIED evaluation (exact
low-dim slices + sampled bulk remainder; stratification by an exact label never biases). One lattice/order/mu
-- a measured pattern, not yet a law. 08_2d_interacting/value_channel_slices.py (self-tests PASS),
VALUE_CHANNEL_SLICES_RESULT.md. Frozen engine untouched (194/194).

### #65 -- Stratify by the slice label: 22-44x where concentration beats budget, 2x where it doesn't (v55)

Turned the v54 slice hierarchy into an estimator: stratify the site sum by the exact span-dimension label,
enumerate small heavy strata, Neyman-sample the rest (unbiased by construction; only the GAIN needed
measuring). n=2 cube vs exact fold+cache truth at matched budget: plain std 5e-3 -> stratified 0.8-1.1e-3 =
22-44x variance reduction, bias <=0.5 sigma; Neyman itself DEMANDED full enumeration of the d<=1 strata
(allocation exceeded stratum size) -- the hierarchy asserting itself. n=3 (with a 3d bulk; heavy d=2 stratum
53262 configs no longer enumerable at budget): 2.1x, means consistent, few-rep caveat. LESSON (the law of it):
stratified gain is large exactly when the concentration is steep RELATIVE TO BUDGET; it degrades gracefully to
modest-but-unbiased when the heavy strata must be sampled. Composes with the orbit fold and subset cache (the
ground truth uses them). Sign R untouched -- a variance tool living on the slice structure.
08_2d_interacting/slice_stratified.py (self-test PASS), SLICE_STRATIFIED_RESULT.md. Frozen engine untouched.

### #66 -- The trade-off is generic in the doped regime; the one alignment is half filling, by symmetry (v56)

Closed the v48 arc. Measured R2(mu_ref) landscapes (beta=4: peak 0.82 at 0; beta=8: peak 0.91 at 0) and the
convergence-optimal shift alpha* per filling (direct truncation-error minimization vs exact ED, REAL-part
metric). beta=4: SEPARATION at every filling (gap >=1.0; R2 at the convergence optimum 0.01-0.40). beta=8:
EXACT alignment at half filling mu=U/2 -- alpha*=U/2 puts mu_ref=0.0 = the sign peak (R2=0.91, gap 0.00) --
MECHANISM: the Hartree shift U<n>/2 = U/2 maps the reference to the particle-hole point, which IS the shell;
mu=1.5 on the shoulder (0.89); doped mu=0-0.5 sharply separated (gaps 1.0-1.5, R2 0.01-0.14). CORRECTION ON
THE RECORD: an earlier pass claimed alignment at mu=1.0 -- a METRIC ARTIFACT (|complex residual| instead of
the real part let the wrong winner surface in a near-degenerate alpha landscape); the module self-test FAILED
against the flawed sweep, which is how it was caught; corrected landscapes are unimodal and separated there.
VERDICT: generic trade-off where the sign problem bites (doped); the one robust both-at-once point is half
filling at low T, forced by particle-hole symmetry -- the same point every sign-free structure points to. No
new free lunch; one mechanism-understood alignment. Scope: one cluster/U/tau, alpha grid 0.5.
08_2d_interacting/genericity_search.py (self-test gates BOTH faces, PASS), GENERICITY_RESULT.md.
Frozen engine untouched (194/194).

### #67 -- The slice hierarchy survives scale: weight strengthens (32x->165x), sign persists and narrows (v57)

Theory-extraction test: is the v54 hierarchy a one-size curiosity? Scaled to L=4,6,8 cubes (64->512 sites,
reachable via FastCDet -- vectorized eigenmode loop, validated to 4.2e-17 against the frozen-port-validated
CDet) with TARGETED sampling of the rare 1d class (matched 900-sample classes, floor 0.027). RESULT: (1) the
weight-density hierarchy survives and STRENGTHENS -- 1d/bulk per-config ratio 32x -> 74x -> 165x; d=2
concentration 2.06x -> 4.34x. Locality expressed as geometry. (2) the sign hierarchy persists at every size
but NARROWS: R(1d) 0.65 -> 0.37 -> 0.24, bulk at/near floor (L=8 bulk 0.157 above floor -- flagged, possibly
heavy-tail ratio inflation, unresolved). (3) v54 refined on the record: its d=1 R=0.224 was 12 uniform
configs (noise); targeted sampling gives 0.652 at L=4. CAREFUL CONCEPTUAL CLAIM now supported: the expansion's
weight concentrates in a geometrically identifiable low-dimensional sector whose dominance GROWS with system
size and which carries the healthiest sign; the diffuse bulk (numerous, negligible, sign-incoherent) is where
variance lives. A measured geometric structure of configuration space -- not yet a theory of it. LESSON: rare
classes need targeted sampling before their statistics are quotable. 08_2d_interacting/slice_scaling.py
(self-test PASS), SLICE_SCALING_RESULT.md. Frozen engine untouched (194/194).

### #68 -- Universality: weight concentration is universal and robust; the sign hierarchy is DOWNGRADED (v58)

Swept the slice hierarchy across order (n=2,3,4), temperature (beta=2,4,8), filling (mu=0,0.5,1.5) and the
observable on the L=6 cube (U exactly universal by the banked no-U-in-C_V theorem). (1) WEIGHT UNIVERSALITY
STANDS, strengthened: 1d/bulk ratio >10x in EVERY cell -- mean-based 10x-223x, MEDIAN-based (robust) 11x-184x,
seed-stable (beta=8: 66x/55x/61x across seeds). A property of propagator geometry. (2) SIGN HIERARCHY
DOWNGRADED ON THE RECORD: the module's first self-test FAILED -- same cell gave R(1d)=0.44 at 500 samples vs
0.02 at 400, same seed -- exposing that R=|mean|/mean|.| over these heavy-tailed |C| distributions is
estimator-fragile at current sample sizes; robust count-coherence S=|2f_- -1| sits near the binomial floor in
most cells. The v54/v57 per-class sign statements ("hierarchy persists and narrows") are downgraded to OPEN
pending weighted-bootstrap/tail-aware statistics; v57's flagged L=8 bulk anomaly was this same instability.
LESSONS: a ratio of means over heavy tails is not a measurement until the estimator is shown stable; gate
self-tests on robust statistics; a failing gate is data. 08_2d_interacting/slice_universality.py (robust
gates PASS), SLICE_UNIVERSALITY_RESULT.md; SLICE_SCALING_RESULT.md amended. Frozen engine untouched (194/194).

### #69 -- Derivation attempt: predict the concentration from propagator geometry -- FALSIFIED (v59)

Applied the frontier bar: derive, FREEZE the constant, predict, then measure. Derivation: connected weight
decays exponentially with the minimal connecting network, ln|C| ~ a - l_MST/xi, xi measured independently
from the bare propagator (0.91); class ratio then follows by pure geometry, zero further parameters. RESULTS:
(1) the data's own form IS exponential in L (v57 ln-ratio linear in L) -- form survives. (2) MST is the best
geometry variable (R2=0.17 vs tour 0.12, max-leg 0.01) but the slope is HALF the prediction (-0.51 vs -1.10;
effective decay ~2xi, unexplained) and geometry carries only ~17% of ln|C| variance. (3) Frozen-slope
prediction of class-median ratios: 3x/5x/7x at L=4/6/8 vs MEASURED 16x/62x/30x -- under-prediction 5-10x: the
single-variable law is FALSIFIED as the explanation. (4) Auxiliary: per-class medians fluctuate strongly
across runs (30x vs 52-82x at L=8) -- the 1d class is a MIXTURE (axis vs diagonal lines, heavy tails); future
class statistics must stratify by line type. VERDICT: line not crossed; the dominant mechanism of the
(universal, robust) concentration is UNIDENTIFIED. LESSON: freeze-then-predict makes a failed theory cleanly
falsifiable instead of quietly fitted -- bank the negative. 08_2d_interacting/decay_law.py (self-test gates
include the falsification itself, PASS), DECAY_LAW_RESULT.md. Frozen engine untouched (194/194).

### #70 -- Dual mechanism: tau-interference confirmed (40%), anisotropy real but insufficient; ~10x closed-line residual (v60)

User hypothesis after the v59 falsification: multiple mechanisms. Three rounds. (1) More geometric variables
REJECTED: five combined raise R2 only 0.178->0.198. (2) TAU-INTERFERENCE CONFIRMED as mechanism 2: within-
geometry (tau-only) fluctuation = 39-40% of var(ln|C|) (the v49 zero-crossings); integrating tau out DOUBLES
the geometric law (R2 0.18->0.48 at L=8; 0.23->0.44 at L=6). The frozen tau-averaged prediction still fails
(8.7x vs 75.5x), and stratifying the 1d mixture exposed the anomaly: BODY-DIAGONAL lines (MST 5.20) as heavy
as AXIS lines (MST 3.00), 3.4x heavier than face-diagonals -- weight does not follow Euclidean distance inside
the class. (3) ANISOTROPY REAL BUT INSUFFICIENT: xi per Euclidean unit at L=8 = 0.90/1.21/1.20
(axis/face/body), ~35% slower on diagonals (only ~9% at L=6's short range -- range-dependent, flagged); the
anisotropic decay-metric MST does not close the gap (R2 0.32; prediction 6.8x vs 75.5x). VERDICT: dual
structure real -- (geometry) x (tau-interference) -- explanatory power doubled; a persistent ~10x enhancement
of CLOSED-LINE configurations survives all distance laws. HYPOTHESIS BANKED for v61 (untested): the 1d lines
are closed RINGS on the torus -- ring-closure/winding coherence (discrete 1d sub-chain spectra; rhymes with
v41 shells) is the candidate third component. LESSONS: variance-decompose before declaring a law's variables
exhausted; stratify mixtures before regressing across them; a wrap-unsafe fit can fake a 100x decay length
(caught in self-test hardening). 08_2d_interacting/dual_mechanism.py (PASS), DUAL_MECHANISM_RESULT.md.
Frozen engine untouched (194/194).

### #71 -- Winding-phase ring closure FALSIFIED by a paired twist; the unpaired run faked a 4x effect first (v61)

Tested the v60 hypothesis with a surgical intervention: an ANTIPERIODIC twist along one axis -- |hopping| and
all distances bit-identical (gated), only the winding phase of that axis's loops changes. Frozen predictions:
distance laws -> zero change; winding coherence -> selective suppression of the twisted axis's lines,
mirrored under twist-y. LAYER 1 (the artifact): the unpaired run (independent tau draws per lattice) showed
x-lines at 0.24x vs y-lines 0.74x -- an apparently clean 4x axis-selective effect. LAYER 2 (the truth): fully
PAIRED rerun (same sites AND same tau draws; median of per-config ratios) -- x-lines 0.93x/0.99x, y-lines
1.14x/1.45x, bulk 0.70x/0.73x under twist-x/twist-y. No suppression, no mirror: the 4x was an unpaired
heavy-tail artifact (the v58 pathology, caught by the paired design). VERDICT: maximally changing the closure
phase leaves line weights within ~±40% and axis-blind -- the winding-phase form of ring closure is FALSIFIED;
the ~10x line enhancement is CLOSURE-INDEPENDENT. Surviving refined hypothesis (untested): 1d CHANNELING --
coherent multi-bounce along the line's short segments, twist-blind by construction; v62 test = lines vs
equally-compact non-collinear configs at matched decay-metric MST. LESSON (thrice-earned, now standing
methodology): in heavy-tailed systems PAIR every comparison -- same sites, same taus, per-config ratios.
08_2d_interacting/ring_closure.py (gates include the falsification, PASS), RING_CLOSURE_RESULT.md.
Frozen engine untouched (194/194).

### #72 -- 1d channeling CONFIRMED: collinearity carries ~2x at matched distance; the mechanism ledger (v62)

Tested the surviving hypothesis with full controls: three families from the SAME axis-directed distances
(LINE all-on-one-axis / BENT two-axes / ZIG three-axes), anisotropy controlled exactly by cubic symmetry,
pairs matched on MST to 0.01, identical tau draws per pair. Frozen predictions: distance law -> all ~1;
channeling -> line > bent > zig. MEASURED: line/bent 1.82-2.04x, line/zig 1.93-2.43x, bent/zig 1.33x --
monotone in collinearity, separated from 1: CHANNELING IS REAL (coherent multi-bounce along a shared
direction at fixed total distance; twist-blind, consistent with v61). MECHANISM LEDGER for the universal
concentration: CONFIRMED = distance decay (tau-avg R2 0.48) + tau-interference (40% of variance) + anisotropy
(minor) + channeling (~2x, graded); FALSIFIED = winding closure; RESIDUAL = distance x channeling composes to
~16x of the ~75x class gap -> ~4x UNACCOUNTED (candidates: mechanism interactions, matching range, class tail
composition) -- stated, not absorbed. LESSON: control anisotropy by building comparisons from symmetry-
equivalent displacements; grade a mechanism by a monotone family, not a single contrast.
08_2d_interacting/channeling.py (PASS), CHANNELING_RESULT.md. Frozen engine untouched (194/194).

### #73 -- Mechanism closure: the two-coefficient law locks the concentration within 1.27x (v63)

Chased the ~4x residual with the gate PRE-SET at 2x. (1) CHANNELING COMPOUNDS WITH LENGTH: paired line/bent
ratio grows ~1.6x at matched MST=3 -> ~2.7x at MST=4 (c ~ +0.5/unit); v62's flat ~2x was the average of a
growing function. (2) TWO TRAPS CAUGHT: a first l_coll definition gave bulk configs spurious channeling credit
for a single vertex (any point is trivially collinear with the external -- direction groups need >=2
vertices); and the joint two-term fit suffered MULTICOLLINEARITY (line family has l_coll == MST identically,
so the regression zeroed c and inflated b). Cure: CLEAN IDENTIFICATION -- b=0.537 from BULK-ONLY regression
(l_coll=0 exactly, R2=0.16), c=+0.583 from the PAIRED matched-MST contrast (distance cancels per pair, n=10).
(3) LOCKDOWN: frozen composition at the class medians exp(0.537x3.00 + 0.583x4.24) = 59x vs measured 75.5x ->
agreement factor 1.27, WITHIN the pre-set gate. The universal weight concentration is now mechanistically
accounted: distance decay compounded with length-growing 1d channeling, modulated by tau-interference (40%).
Open: WHY c ~ 0.5-0.6 (propagator calculation not attempted). LESSONS: when regressors are identical on a
subpopulation, identify each coefficient where the other cannot contaminate it; audit feature definitions for
degenerate cases (single-point "lines") before fitting. 08_2d_interacting/mechanism_closure.py (gates include
the 2x lockdown, PASS), MECHANISM_CLOSURE_RESULT.md. Frozen engine untouched (194/194).

### #74 -- Beyond the 2x2: the genericity law SPLITS -- PH convergence-lock universal, sign alignment cluster-dependent (v64)

PIVOT target (b) executed. AXIS 1, couplings (2x2, beta=8): alpha* = U/2 at mu = U/2 at U=2 AND U=8 (with
v56's U=4: three couplings), every doped point separated (R 0.13-0.14 vs peak 0.91) -- the mechanism tracks U
exactly. AXIS 2, cluster (6-ring, U=2, beta=8), enabled by BLOCKED SECTOR ED ((N_up,N_dn) splits 4096-dim into
49 sectors <=400; validated vs a 120-s dense-eig reference to 4.8e-07; ~150x faster): frozen prediction stated
BEFORE the run from v56's measured 6-ring landscape (peak at mu_ref=-1.0, R(0)=0.14) -- PH mechanism should
hold, sign alignment should FAIL. Measured: alpha*=U/2 wins by FIVE ORDERS OF MAGNITUDE (err@K8 = 8.6e-6 at
the extraction floor vs ~1e0 elsewhere -- the PH-symmetric reference is QUASI-EXACT, stronger than v56 knew);
and sign there is R=0.14 vs peak 0.51 -- alignment FAILS at half filling. REFINED LAW: (i) universal --
convergence locks to the PH point alpha*=U/2 at half filling (2 clusters x 3 couplings), quasi-exactly;
(ii) cluster-dependent -- sign alignment requires the cluster's sign peak to coincide with the PH point (true
on the 2x2, false on the 6-ring): v56's "align at half filling" was a 2x2 coincidence of two distinct special
points. CURIOUS OPEN: the 6-ring sign peak sits ON a level (-1.0), not in the gap at 0 -- naive shell logic
fails there, reason unknown. LESSON: a law passing on one system may be two laws in coincidence; test the
components separately on a system where they can come apart. 08_2d_interacting/genericity_cluster.py (PASS),
GENERICITY_CLUSTER_RESULT.md. Frozen engine untouched (194/194).

### #75 -- Consolidation: the baseline upgraded to the composed best of v49-v64 (v65)

Built the front door cdet_best.py: BestCDet (=FastCDet, 2.8e-17 vs the validated CDet) + best_site_sum
(orbit fold x subset cache; gates exact at 3.5e-16 on the 4x4 and 2.7e-15 on the 4^3 cube, 13x measured
wall-clock, 16384 -> 578 determinants) + best_site_sum_sampled (slice stratification for big cubes) +
recommended_shift encoding the SPLIT shift law (alpha*=U/2 at half filling, quasi-exact, with the
cluster-dependent sign caveat IN the return value) + CONCENTRATION_LAW constants (b=0.537, c=0.583,
tau-share 0.40, lockdown 1.27). BEST_METHODS.md upgraded to the v65 edition: the composition table with
measured factors and banked provenance, the two laws, and the standing methodology (pair comparisons; robust
statistics; wrap-safe fits; freeze-then-predict; stratify mixtures; clean identification; failing gates are
data -- each rule bought with a banked failure). The wall statement stands verbatim: nothing in the stack
moves R at fixed mu; the fold channels are provably +1 and the value channel's -1 is dressed (v54). The
package now teaches its own best practice. 08_2d_interacting/cdet_best.py (4 gates PASS), BEST_METHODS.md
(v65 edition). Frozen engine untouched (194/194).

### #76 -- The no-brute-force simulator: surrogate predicts brute structure with zero evals; the wall appears as an estimator theorem (v66)

Built the concentration law into a predictive surrogate: ln<|C|>_tau ~ a - b*MST + c*l_coll + d*dim,
calibrated on ~85 tau-averaged geometries (the only true evaluations), OUT-OF-SAMPLE R2 = 0.75-0.76, median
per-config error 1.7x (mixed bulk+line ensemble breaks the v63 multicollinearity in practice). (1) ZERO-
EVALUATION structure: the v54 brute-force weight-share table reproduced with no C_V calls -- 4.9/48.4/46.7%
vs measured 5.6/43.0/51.5%; concentrations 14.5/2.40/0.59 vs 18.5/2.09/0.65. (2) GUIDED ESTIMATION where sign
is mild: n=2 vs exact truth at budget 400/4096 -- stratify by PREDICTED weight: 33x over uniform (survey;
5x at self-test seeds, heavy-tail spread), bias <=1 sigma, tying the hand-built v55 stratification while
generalizing; defensive importance sampling 12x (weaker -- sign flips hurt C/p; stratified recommended).
(3) THE BOUNDARY, MEASURED: n=3 vs the exact 262,144-config truth (computed in 11 s by the consolidated
stack: 24,958 determinants vs 4.2M brute, 168x fewer) -- guided estimation gives NO gain (0.7x) because the
total is cancellation-dominated: variance is SIGN-driven, and a magnitude predictor cannot guide what it
cannot see. The sign wall expressed as an estimator theorem, measured. LESSON: a surrogate's ceiling is set
by which component of variance it models; state the ceiling as part of the deliverable.
08_2d_interacting/surrogate.py (gates PASS), SURROGATE_RESULT.md. Frozen engine untouched (194/194).

### #77 -- The sign model: v58 settled, line-sector sign predictable, estimator ceiling moved 0.7x -> ~100x (v67)

Knocked on the converged door (v58 tail-aware sign question == the surrogate's missing sign channel).
(1) SETTLED: the per-geometry sign survival r_g = |<C>_tau|/<|C|>_tau (the stable object; v58's downgrade
targeted unstable per-sample R) is bootstrap-bounded with NON-OVERLAPPING CIs: 1d 0.70 [0.59,0.81] / 2d 0.70
[0.58,0.82] / bulk 0.34 [0.25,0.47] -- the sign hierarchy is real at the tau-integrated level. The SIGN itself
is predictable for lines: 92% positive (bulk 45%, coin flip); r_g correlates with dim (-0.45) and MST (-0.50).
(2) STRUCTURAL FACT: the d<=1 sector -- 808 of 262,144 configs, 0.3% of the space -- carries 77% of the exact
signed total (+0.002949 of +0.003846): sign coherence concentrates the SIGNED sum harder than magnitude
concentrates the unsigned one. (3) CEILING MOVED: hybrid (enumerate the sign-coherent d<=1 sector exactly +
pilot-Neyman the rest) at 0.46% budget vs the exact 262,144-config truth: 87-110x over uniform, bias <=1
sigma -- where v66 magnitude-only gave 0.7x. FLAGGED NOT BANKED: a 231x magnitude-bin reading ran on a frozen
subsample (selection variance missing from its std). METHODOLOGY CATCH: the first self-test failed because
trimmed sample sizes broke the bootstrap separation -- the v58 lesson applied to our own gates; survey sizes
restored. Scope: one lattice/order/mu/beta; line-sign predictability measured not derived; the bulk remainder
stays a coin flip -- the wall stands, territory mapped to 0.3%. 08_2d_interacting/sign_model.py (PASS),
SIGN_MODEL_RESULT.md. Frozen engine untouched (194/194).

### #78 -- Governance of the signed weight: coherence decays on its own scale; orientation is a mu-controlled phase (v68)

Asked what governs where the SIGNED weight lives. Answer, measured: signed weight = magnitude envelope (v63
law) x sign-coherence decay x a filling-controlled PHASE. (1) PARITY FALSIFIED: sublattice-sign product
predicts orientation at 50% (mu=0.5) and 59% (mu=0, the PH point) -- coin flip; suspected (unproven) reason
for the mu=0 failure: the v54 equal-time dressing. (2) SIGN COHERENCE OUTLIVES WEIGHT: ln r_g vs MST gives
xi_s ~ 3.0 -- 3x the magnitude's effective decay; binned r_g 0.73 -> 0.40 -> 0.21. This is why the signed
answer concentrates harder than the unsigned one (v67's 77% in 0.3%). (3) THE ORIENTATION IS A PHASE: extent-3
axis lines at L=6 are 94% NEGATIVE at mu=0.5 and 75-100% POSITIVE at mu=1.5 (extent-4: 100%, r_g 0.81) --
same geometries, opposite sign; the Friedel/k_F signature; also resolves the L=4 (92% positive) vs L=6
(negative) apparent contradiction as k-grid phase difference. (4) The invariant is COHERENCE, not positivity
(matched-MST: lines 85%, bulk 72% coherent) -- v67 restated correctly: the line sector carries the answer
because its phase is deterministic, not because it is positive; this turn's own interim "compact => positive"
framing corrected on the record. OPEN THEORY ITEM: the quantitative phase law (fit the orientation period vs
free-fermion k_F(mu)). LESSON: when an orientation statistic flips between systems, suspect a phase, not a
contradiction. 08_2d_interacting/sign_governance.py (PASS), SIGN_GOVERNANCE_RESULT.md.
Frozen engine untouched (194/194).

### #79 -- The quantitative phase law: two sub-determinant reductions FALSIFIED under frozen protocol (v69)

Went for the formula. Protocol: calibrate predictor + one global sign on ONE cell (L=6, mu=0.5, extent 3),
freeze, predict 7 other (L, mu, extent) cells per-geometry; gate PRE-SET at >=75% mean accuracy. (1) STATIC
FRIEDEL FALSIFIED: four tau-averaged single-particle predictors (per-leg sign products, det of the averaged
propagator matrix, dominant-permutation-with-parity) saturate calibration (93%) and collapse out of it --
mean 34% (anti-correlated cells to 7%). Diagnostic: <C>_tau averages the PRODUCT of propagators, not the
product of averages; and the static free sign pattern is ++-++ at ALL fillings -- it cannot even represent
the measured mu-flip. The phase needs joint-tau structure (v60's 40% channel, again). (2) DOMINANT CHAIN
FALSIFIED: the fully tau-integrated chain loop (Matsubara sum, no determinants) reaches 64-66% -- real
partial signal (two cells 100%/93%) but fails the gate with one cell anti-correlated (21%); the cell-wise
reversals are the fingerprint of competing pairings of opposite permutation parity. STANDING CONCLUSION: the
orientation phase is determinant-level interference as far as tested -- MAGNITUDE IS LAWFUL (two
coefficients, v63), THE PHASE RESISTED EVERY SUB-DETERMINANT REDUCTION: a sharp localization of where the
sign problem's hardness sits in this representation. Scope: axis lines, n=3, one beta; "irreducible" = both
tested reductions failed frozen gates, not a proof. LESSON: a predictor that saturates its calibration cell
has shown nothing until it survives frozen out-of-cell prediction. 08_2d_interacting/phase_law.py (self-test
reproduces the double falsification, PASS), PHASE_LAW_RESULT.md. Frozen engine untouched (194/194).

### #80 -- Sign model folded into the surrogate as scalable exact machinery; v67 gain CORRECTED by exact moments (v70)

ROTATION pass 1 of 3 (fold-in). (1) SCALABLE MACHINERY: the coherent rank<=1 sector is polynomially small BY
CONSTRUCTION and built from direction classes in O(N^2) -- 808/262,144 at L=4, 3,774/10,077,696 at L=6
(0.037%); per-config rank classification vectorizes (exact strata counts over all 10M L=6 configs in 6 s);
estimator = exact sector sum + signed-sigma pilot-Neyman, unbiased at any L. r_pred (OOS R2 0.32, xi_s 2.2 vs
measured 3.0) banked as the surrogate's sign channel -- role: identifies the enumeration target. (2) THE
CORRECTION: exact second moments via the same orbit fold (C group-invariant) give design variances EXACTLY --
uniform true std 1.08e-2 at B=1200 (seed-set measurements ranged 2.75e-3 to 3.0e-2, BOTH unreliable);
v67-design true std 4.30e-3 -> TRUE GAIN ~6x; the banked 87-110x was a lucky-high-baseline artifact and is
CORRECTED on the record (structural facts untouched). Exact decomposition: 96% of uniform's E[C^2] is the
sector's rarity (the single all-external config: 34%); bulk 4% -- removing the sector exactly is the whole
magnitude-side win; the rest is sign-driven (v66's theorem, now exact). (3) L=6 DEMO at 10M scale (~0.045%
budget): exact sector sum -5.87e-4 -- NEGATIVE, v68's mu=0.5 orientation flip in exact arithmetic; total
estimate -2.3e-3 +/- 4.5e-3 -- error bar exceeds value: the machinery scales, the sign problem scales faster.
TWO construction bugs caught by own gates (13-direction family != rank-1 sector, 5% vs 77%; dropped
all-external config, off-by-one vs exact count). NEW STANDING RULE: heavy-tailed estimator comparisons must
be exact-moment-based wherever exact moments are computable; rep-spread comparisons are not measurements.
08_2d_interacting/sector_estimator.py (PASS), SECTOR_ESTIMATOR_RESULT.md; correction note added atop
SIGN_MODEL_RESULT.md. Frozen engine untouched (194/194).

### #81 -- Pairing depth: the phase has NO finite depth; no single free determinant carries it (v71)

ROTATION pass 2 of 3 (item a), run SURROGATE-FIRST per the new standing mode (user directive: experiment on
the surrogate, engine as crosscheck, until major surrogate gains). The free 4-point tau-integrated
determinant decomposes exactly into 24 permutation terms via Matsubara cycle sums; depth-k predictor = sign
of the k largest terms; frozen v69 protocol; PRE-REGISTERED gates: depth-2 >= 75%? full depth >= 75%? BOTH
FAIL: OOC 46% / 46% / 63% / 44% at k = 1/2/4/24; the engine-matched external-time-fixed variant is
IDENTICAL. The complete single free determinant predicts the orientation no better than chance-ish. The v69
conclusion SHARPENS by elimination: the phase lives in the COUPLED PRODUCT OF THE TWO SPIN DETERMINANTS over
shared vertex times (+ connected/vacuum subtraction) -- the engine integrand itself; consistent with v54
(cross-spin dressing) and v60 (tau-interference). REDUCTION LADDER COMPLETE: parity 50-59% -> static 34% ->
chain 64% -> any-depth single determinant <= 63%, full 44% -- all frozen-protocol falsifications. SURROGATE
CONSEQUENCE: no physics-reduced orientation channel exists below the engine; the remaining route is a
LEARNED statistical channel (queued). Scope: axis lines, n=3, one beta; dressed-propagator determinants
untested. 08_2d_interacting/pairing_depth.py (PASS), PAIRING_DEPTH_RESULT.md. Frozen engine untouched
(194/194).

### #82 -- The bulk remainder: mu-controlled Friedel rings; the frozen surrogate model falsified by its own crosscheck (v72)

ROTATION pass 3 of 3 (item c), surrogate-first. FROZEN PREDICTION (zero evals): remainder signed content
decays monotonically with MST -- compact shell >= 86 +/- 20 % (G1); far bulk = noise without signal (G2).
EXACT CROSSCHECK (orbit-fold per MST bin over rank>=2, L=4): BOTH GATES FAIL. The data: binned signed sums
ALTERNATE (+0.000256 / -0.000463 / +0.001080 / -0.000053 at mu=0.5, total +0.000819 = v70 reference);
dominant content MID-RANGE (58% at MST 4.5-5.5); inter-shell cancellation 2.3x; noise concentrates at
intermediate MST (61%). FROZEN CONFIRMATION TEST: if phase rings, mu must move them -- at mu=1.5 the pattern
shifts to (-,-,-,+), net -0.005101 (6x larger, cancellation 1.13x, matching v68's higher coherence). The
remainder is organized as FRIEDEL RINGS IN CONFIGURATION SPACE, governed by the orientation phase that
v69/v71 proved has no sub-engine formula. ROTATION'S UNIFIED CONCLUSION: all three passes ended at the same
object -- the phase; the surrogate's missing channel is fully characterized and the only queued route is
LEARNED, not derived. LESSON: when a monotone-decay model meets an oscillating truth, the falsification IS
the discovery -- bank the rings, not the regret. 08_2d_interacting/bulk_remainder.py (PASS),
BULK_REMAINDER_RESULT.md. Frozen engine untouched (194/194).

### #83 -- The learned orientation channel fails the same frozen gate; the channel closed from both directions (v73)

Queued surrogate experiment executed: train on 9 cells (L=6, mu 0.5/1.0/2.0, extents 3-5; 108 labeled line
geometries), evaluate on ENTIRELY HELD-OUT cells (unseen mu=1.5 all extents AND unseen L=4); pre-set gate
>= 75% (the bar the physics ladder failed; best rung chain 64%). TWO HYPOTHESIS CLASSES, BOTH FAIL:
L2-logistic with physics-informed features -- train 74%, held-out 33% (consistent ANTI-prediction at unseen
mu, down to 0% on one cell); nonlinear MLP with harmonics and pairwise interference features -- train 74%,
held-out 35%. STRUCTURAL REASON, identified: A PHASE WRAPS -- smooth models cannot interpolate a wrap from
sparse mu samples; predicting orientation at unseen mu requires the mu-PERIOD, which is exactly the
quantitative phase law v69/v71 proved has no sub-engine form. The circle closes: to learn the channel you
need the law; the law does not reduce. THE ORIENTATION CHANNEL IS CLOSED AT THIS SCOPE from both directions
(derived: 50-59/34/64/44%; learned: 33/35%). Remaining routes named honestly: dense mu-tabulation
(measurement, not modeling); engine-derived features (defeats the purpose); the mu-period analytically (open
theory item). Surrogate-gain avenues remaining are magnitude-side. LESSON: before fitting a model across a
control parameter, ask whether the target is a phase in that parameter -- if it wraps, sparse-sample learning
is structurally impossible, and the honest alternatives are tabulation or theory.
08_2d_interacting/learned_orientation.py (PASS), LEARNED_ORIENTATION_RESULT.md. Frozen engine untouched
(194/194).

### #84 -- Surrogate refinements: ceilings first, the R2-mixture artifact corrected, transfer is the gain, and the r_pred regime map (v74)

Queue item (b), surrogate-first. (1) CEILINGS MEASURED FIRST (new standing practice): split-half reliability
gives magnitude rho=0.95 at NT=20 (real headroom above 0.75) and r_g rho=0.40 at NT=20 / 0.57 at NT=40 -- the
"weak" r_pred 0.32 was ~80% OF ITS CEILING: label noise, not model failure. (2) R2-MIXTURE ARTIFACT (scope
correction of our own reporting): v66's 0.75 was test-composition-flattered (line-heavy spread); the same
model scores 0.55 on a standardized bulk-heavy split; median per-config error (1.7x) is the mixture-
independent co-headline; clarification note added atop SURROGATE_RESULT.md. (3) TRANSFER IS THE GAIN:
10-feature linear ridge -- in-distribution a wash (0.55 -> 0.59) but L=4 -> L=6 transfer R2 0.33 -> 0.57,
med-err 2.88x -> 1.81x (8-shot intercept, stated); quadratic interactions DESTROY transfer; two pipeline bugs
caught (garbled CV formula silently breaking lambda selection; quadratic extrapolation blowup). (4) r_pred
REGIME MAP: within rank-1 +0.32 / rank-2 +0.27 / rank-3 -0.57 -- sign-survival predictability lives exactly
where coherence lives; the deep bulk resists even graded prediction: the v73 closure, quantitative in the
survival channel. LESSONS: measure the label-noise ceiling before chasing R2; R2 without a declared test
mixture is not a quality claim; report median per-config error alongside. 08_2d_interacting/surrogate2.py
(PASS), SURROGATE2_RESULT.md. Frozen engine untouched (194/194).

### #85 -- The L=6 shell fold: first exact 10M-config totals, rings at L=6, and the wrap-collinearity correction (v75)

The fold ran (240,464 orbit reps of 10,077,696 configs, both fillings, ~25 min). EN ROUTE, A DEFINITION
CORRECTION: min-image collinearity is ILL-DEFINED on even-L tori (lines wrap through the antipode --
{0,(5,1,0),(3,3,0)} is collinear but its min-image rows are not parallel); the per-config min-image rank is
not orbit-consistent, and the v67/v70 "rank<=1 sector" was the min-image-parallel SUBSET of the true
torus-line sector. WRAP-SAFE definition (common cyclic line through origin, group-invariant): L=4 sector =
1,618 configs carrying 82% (was 808/77%); L=6 = 16,950 (0.17%, was 3,774). Old numbers true for the smaller
subsets; notes added to both docs; the standing wrap-safe rule EXTENDS TO DEFINITIONS. THE FOLD: first exact
L=6 totals -- mu=0.5: -2.498377e-3 (v70 pilot -2.3e-3 +/- 4.5e-3 VALIDATED dead-on; the phase flip vs L=4
holds for the full total); mu=1.5: -2.224768e-3. SIZE TREND, exact: sector share 82% (L=4) -> 42% (L=6) and
at mu=1.5 the sector OPPOSES the total (-22%) -- the remainder grows with size: the sign problem scaling
faster than the machinery, in exact arithmetic. RINGS AT L=6: oscillation persists (2 sign changes per
filling; mu-dependent patterns); half-unit bins give mu-dependent node positions (3.0/4.5/5.5... vs
3.5/4.0/5.0...) but IRREGULAR spacings (0.5-1.5) -- right scale vs the frozen pi/k_F ~ 1.1-1.2, period NOT
resolved; refinement path named (per-leg extent instead of MST). LESSON: on a torus, check every geometric
DEFINITION for antipodal ambiguity before building sectors on it. 08_2d_interacting/shell_fold.py (PASS),
SHELL_FOLD_RESULT.md. Frozen engine untouched (194/194).

### #86 -- The ring period: not resolved; the spectral near-miss killed by permutation null; the impossibility quantified (v76)

Pure re-analysis of the v75 fold (zero new engine sweeps). Shell-coherence f(r) = S(r)/Sum|v| over four
radial coordinates, detrended periodograms, pre-registered gates. THE SEDUCTION: binned R_max periodograms
peaked within 9-10% of the continuum 2k_F at BOTH fillings with the correct mu-shift. THE KILL: R_max is
DISCRETE (18 exact lattice radii); unbinned treatment + 1000-shuffle permutation null gives p = 0.20 / 0.16
-- NOT significant; the binned peaks were a coincidence null calibration caught (the v58 lesson in spectral
form). Second trap: Perimeter's 16x low-q "peak" was trend leakage with the WRONG mu-shift. WHAT IS REAL: the
contact-shell coherence is strong and mu-FLIPPED (+0.66 at mu=0.5 / -0.53 at mu=1.5, consistent with
v68/v72); beyond it the profile is amplitude-starved (|f| <~ 0.1-0.3). THE STRUCTURAL IMPOSSIBILITY,
quantified: xi_s ~ 3.0 vs period ~ 1.2 -> ~2 oscillations fit before decoherence, on ~5 usable radii at <10%
coherence -- L=6 CANNOT resolve the period in principle; the route is larger L + a coherence-boosted
observable (the v68 line-sector protocol). THREE LESSONS BANKED: spectral peaks need permutation-null
calibration; discrete coordinates must be analyzed unbinned (bin widths manufacture structure); check
xi_s/period before designing a period measurement. 08_2d_interacting/ring_period.py (PASS),
RING_PERIOD_RESULT.md. Frozen engine untouched (194/194).

### #87 -- THE MU-PERIOD LAW: charge-1 fugacity winding; Friedel falsified; the wrap solved, the offset now the bottleneck (v77)

The route v76 named, executed: coherence-boosted line protocol (L=6/8 axis lines, dense mu-grid step 0.1,
sign(<C>_tau), persistence-filtered flips; r_g DIPS at flips -- they are physical zeros). FRIEDEL FALSIFIED
on pre-registered gates: spacing R-INDEPENDENT (G1 backwards), positions do not collapse on 2 kF R = m pi
(G2: winding ~5x faster), and spacing is strongly beta-dependent. THE LAW: median spacing 1.00/0.70/0.50/0.40
at beta=2/4/6/8 vs pi/beta = 1.57/0.79/0.52/0.39 -- implied charge q = 1.12/1.05/0.98 -> Delta-mu* =
pi/(q beta), q -> 1: CHARGE-1 FUGACITY WINDING, R- and L-independent. The phase that resisted every geometric
reduction (v68-v73) has a form, and it lives in (mu, beta): dphi/dmu ~ beta. NEW THEORY TARGET: derive q=1
from the tau-integrated integrand. THE CHANNEL HALF-REOPENS: period-based calibrate-then-predict lifts
held-out accuracy from v73's 33-44% (anti-prediction) to 73-76% -- AT the 75% bar, not robustly above (per-run
variance 0-100%); the residual is OFFSET calibration (half-grid flip error = 8-15% of the 0.65 period),
engineering not law-finding. LIMITS BANKED: beta >= 12 unmeasurable with this estimator (independent
extractions disagree 0.40 vs 1.50 -- a protocol validity boundary); level-floor hypothesis raised, its
cross-predictions failed-or-undecidable; beta=2 censored. An initial 79% single-seed reopening claim was
DOWNGRADED by the seed-robustness sweep before banking -- the sweep is now standard for protocol claims.
LESSON: a law is what survives seeds, gates, and horizons; a number that hovers at the bar is reported as at
the bar. 08_2d_interacting/mu_period.py (PASS), MU_PERIOD_RESULT.md. Frozen engine untouched (194/194).

### #88 -- The analytic origin of the mu-period: the Matsubara comb, detected by complex-mu continuation (v78)

Theory item (a) executed, with a falsification en route. THE CANCELLATION LEMMA (rigorous, any order): all
explicit e^{mu tau} factors cancel per determinant, so <C>_tau is EXACTLY rational in z = e^{beta mu} with
poles only at z = -e^{beta eps_k} < 0 -- mu-poles on Matsubara combs mu = eps_k + i(2m+1)pi/beta at uniform
height pi/beta. THE STAIRCASE FALSIFICATION: the literal charge-staircase (adjacent fugacity powers, our v77
reading AND the simplest outside derivation Paul relayed) predicts +beta slope steps in ln|C| at flips;
measured slopes are FLAT (0.03-0.33 beta) -- dead; Fermi factors are degree-matched and saturate. THE DIRECT
DETECTION: the engine analytically continues in mu (Cauchy-Riemann residual 6e-4); approaching the comb at a
level, |<C>| rises 3.9e6-fold by y = 0.77 (pi/beta = 0.785); between levels, x12 (flat); contrast 3e5 -- the
pole is exactly where the lemma puts it. THE MECHANISM: comb-limited sign structure derives the 1/beta
scaling AND R/L-independence in one stroke; q ~ 1 = nearest-comb dominance (matches the measured drift
1.12 -> 0.98); "charge 1" = the z-degree of each Fermi denominator; pi = the antiperiodicity phase. REFINED
OPEN ITEM: the exact constant (zero spacing ~ pi/beta vs O(pi/beta)) -- a zero-statistics question for
high-degree negative-pole rational functions. Reading note added atop MU_PERIOD_RESULT. LESSON: when a
heuristic and a measurement agree, the heuristic can still be mechanism-false -- test the mechanism's
distinctive prediction (here the slope staircase), not just the law's value. 08_2d_interacting/
fugacity_structure.py (PASS), FUGACITY_STRUCTURE_RESULT.md. Frozen engine untouched (194/194).

### #89 -- The surrogate consolidated: cdet_surrogate.py, the v79 BEST_METHODS edition, and two refinements found during integration (v79)

User-directed consolidation. ONE integration layer (cdet_surrogate.py) now carries every proven finding:
wrap-safe sector identification (v75), the transferable magnitude model (v74), the r_pred regime map (v74),
and the period-based orientation channel (v77 law + v78 comb mechanism), each with its verified scope stated
at the point of use; BEST_METHODS.md gains the v79 edition (component table, the phase program's closed arc,
the nine methodology rules earned since v65). TWO REFINEMENTS FOUND DURING INTEGRATION (consolidation as
audit): (1) the v74 transfer figure 1.81x sits at the favorable end of draw-to-draw spread -- two independent
draws give 1.74x / 2.69x, POOLED 1.88x, banked with mixtures declared; (2) a per-class-intercept hypothesis
was raised, TESTED, and REJECTED (line/bulk offsets differ by only 0.16 ln units; the bulk offset estimate
is noisier; the 8-shot LINE intercept is the consolidated choice). End-to-end self-test: wrap-collinear
sector recognition, two-draw pooled transfer gate (<= 2.6x), orientation channel above its honest gates,
integrated report. LESSON: consolidation is not bookkeeping -- re-deriving every number in one place is an
audit that finds the draw-spread and kills the untested hypothesis. 08_2d_interacting/cdet_surrogate.py
(PASS), BEST_METHODS.md v79 edition. Frozen engine untouched (194/194).

### #90 -- The resonance regime: the KT review reopens the chain; a boundary retracted, a second regime proved (v80)

User-directed round: apply the KT-RG method + how-to-think patterns to review v75-v79 for missed structure;
"don't count your hypotheses off yet." THE REVIEW DELIVERED. (1) Phase-0 reversal: fine-grid beta=4 spacing
is 0.625 (q ~ 1.26) -- the banked 0.70 was grid-inflated; two spacing populations already at beta=4.
(2) IS/IS-NOT on the discarded beta=12 "0.40 vs 1.50 disagreement": both numbers real -- intra- vs
inter-cluster spacing. THE TWO-REGIME LAW, two independent significant statistics: flips attract to levels
with growing beta (p = 0.025 at beta = 12 and 16, frozen uniform nulls) and become GEOMETRY-INDEPENDENT
(cross-geometry nearest-flip distance 0.020-0.025, p = 0.013-0.041 at beta=16, BOTH L; vs p = 0.19 at
beta=4). THE v77 "beta >= 12 UNMEASURABLE" BOUNDARY IS RETRACTED -- it was the resonance regime announcing
itself (note atop MU_PERIOD_RESULT). (3) The limit set: naive levels+midpoints KILLED at L=6 (p=0.33);
trajectories convergent (1.988 -> level 2; one family 1 + ln4/beta candidate); the core set is
EXTERNAL-TIME-INDEPENDENT (toti discriminator; the pretty 2(to+ti)=1.8 match killed by its own test -- FM-5
caught in the act); identification open with a concrete program (degeneracy-weighted Delta-E/Delta-k with
ln(g)/beta corrections). (4) THE UNLOCK with fine structure: positions geometry-free -> calibration
transfers; multiplicities geometry-dependent (residues) -> transfer BIMODAL (79-87% matched cluster, 32-47%
anti-phased vs the odd geometry); refined channel = position set + parity anchors. LESSONS: a discarded
disagreement between two measurements may be two real scales -- run IS/IS-NOT before declaring
unmeasurability; re-measure at finer resolution before banking a drift; and a chain of linked anomalies
that hits an unknown is evidence FOR structure ahead, not against the chain.
08_2d_interacting/resonance_regime.py (PASS), RESONANCE_REGIME_RESULT.md. Frozen engine untouched (194/194).

### #91 -- The pair law: the limit set is the spectrum; flips converge to levels as eps +/- c/beta (v81)

The Delta-E/Delta-k program executed via trajectory flows (windowed scans, grid 0.0125, NT=120, beta 12-28,
two geometries). THE LIMIT SET IDENTIFIED: four clean fits put r within 0.05 of level 1 (best rms 0.004),
approached TWO-SIDEDLY as a flip pair mu*_(+/-) = eps +/- c_eps/beta. Every "midpoint" ever sighted -- the
L=6 candidates AND the L=8 0.707/1.000/1.828 coincidences -- was a pair partner in flight; the candidate-set
hunt is over. THE c-ARRANGEMENT (candidate): c = ln(deg(eps))/2 -- deg(1) = 36 exactly at L=6, ln(36)/2 =
ln 6 = 1.792, a 0.4% hit on the cleanest fit (+1.79, rms 0.004), inside the pooled spread (2.02 +/- 0.3).
Forward mechanism sketch: a flip = crossing of Boltzmann families differing by one particle at the level,
mu* = eps + ln(g_ratio)/(beta Dk); the symmetric pair = particle-side and hole-side crossings. RESIDUALS,
honest: level-2 partners grid-pinned and partner-conflated at beta=12 (analysis trap caught: per-window
min-flip mixes a pair when both enter the window); the (1,3,5) upper fit is the multiplicity-jitter outlier.
FALSIFIABLE PREDICTION banked: any (L, level) pair tightens as ln(deg)/2beta with no free parameters --
L=8's deg are exactly computable. RETRO-EXPLAINS: v80's level attraction, the geometry-free universal set,
the intra-cluster scale 2c/beta. LESSON: when hunting a limit set, measure trajectories and extrapolate --
candidate-set guessing tests are underpowered against points in flight. 08_2d_interacting/pair_law.py
(PASS), PAIR_LAW_RESULT.md. Frozen engine untouched (194/194).

### #92 -- The fired prediction fails; the two-class structure: flight pairs AND static midpoint crossings (v82)

The v81 no-free-parameter prediction fired at L=8 level 2. PHASE-0 CATCH EN ROUTE: exact deg = 39 (the
hand-count said 63; the script corrected the on-record prediction to 2 +/- 1.832/beta before firing).
VERDICT: FALSIFIED AS UNIVERSAL -- no flips at 2 +/- 1.832/beta in windowed trajectories (grid 0.0125,
NT=120, beta 12-28, two geometries); c = ln(deg)/2 is demoted to a one-level fit (L=6 eps=1, 0.4%). WHAT THE
FAILURE EXPOSED -- TWO MECHANISM CLASSES: Class I (Delta-k=1) flight pairs eps +/- c/beta converging to
levels (v81; central pinned flips at levels confirmed at BOTH L); Class II (Delta-k=2) beta-STATIC crossings
at specific level-pair midpoints: L=8 flip FLAT at 1.819 +/- 0.009 across beta 12-24 vs (0.828+2.828)/2 =
1.828, plus late-beta statics at 2.121 = (1.414+2.828)/2 and 2.293 = (2+2.586)/2 (window-edge registrations
excluded as a documented artifact class). RETRO-CLEANUP: v80's L=8 "1.81 cluster" was this static all along;
the midpoint law resurrects SELECTIVELY. SELECTION-RULE PUZZLE, sharply posed: the L=6 statics
(half-integers) were killed by v80's own test (p=0.33) -- which crossings flip is a residue-pair sign
condition, lattice/geometry-dependent; open, alongside the Class-I c-formula. LESSON: a one-level fit hit at
0.4% is still only a fit -- fire the no-free-parameter shot at new territory BEFORE promoting; and when a
predicted flight is absent, look for a STATIC occupying the window. 08_2d_interacting/level2_structure.py
(PASS), LEVEL2_STRUCTURE_RESULT.md. Frozen engine untouched (194/194).

### #93 -- The residue ratio tied down: c = logit of the residue-polynomial roots (v83)

User-directed: "residues always creep in all over the place -- get that tied down." DERIVED AND TESTED:
near a level, <C>_tau(mu) x e^{-(to-ti)(mu-eps)} is a low-degree POLYNOMIAL p(f) in the level occupancy
(lemma-grounded: all mu-dependence through occupancies), so every Class-I flip sits at mu* = eps +
logit(f*)/beta with f* a root of p. Pair = roots straddling 1/2; central flip = root near 1/2;
MULTIPLICITY = root count. EVIDENCE: (1) structure -- chi/dof ~ 1 over the full crossing region (and a
2-time slice fit 60x below noise); (2) BETA-TRANSFER -- the beta=20 polynomial predicts (1,2,4) flips
across beta = 12-28 with NO refitting, median offset 0.014, max 0.022; (3) multiplicity -- (1,2,3)'s root
at 0.447 predicts its central flip (0.987 vs measured 1.01) while (1,2,4)/(1,3,5) have p(1/2) != 0 at
10/2.4 sigma, central flips correctly absent. THE CREEP LOCATED: the naive single-level freeze (SCDet)
matches EXACTLY at s = 1/2 and breaks down away from it -- adjacent-comb residues contribute at the
connected object's ~1e-8 cancellation floor at the SAME order; extraction must go through the direct curve
via the logit map. RETRO-CLEANUP: v81's fitted c's were fit-basis artifacts (r/c trade); root logits are
the fundamental constants; the ln(36)/2 coincidence resolved as accidental, explaining v82's falsification
from the inside. TWO PHASE-0 CATCHES EN ROUTE: (a) the first extraction pinned a vertex time (2-time slice
!= the 3-time flip object -- Q0.2); (b) SCDet's s = 1/2 machine-match isolated the bug-vs-truncation
question in one diff. LESSON: when a truncation fails, find the point where it is EXACT and read the
breakdown pattern outward -- it localizes what crept in. 08_2d_interacting/residue_ratio.py (PASS),
RESIDUE_RATIO_RESULT.md. Frozen engine untouched (194/194).

### #94 -- The Class-II selection rule: two conditions, measured both ways (v84)

Extending the v83 machinery to the statics. Near a midpoint, <C>(mu) ~ A + B e^{-beta(mu-mid)} +
C e^{+beta(mu-mid)}; a static flip exists iff (i) the saturated background A VANISHES in the window AND
(ii) the residues have OPPOSITE signs -- then mu* = mid + ln(-B/C)/(2 beta), the same logit-type law with
the two-residue ratio. POSITIVE CASE (the 1.828 static, values not signs): zero at 1.8196, K = -0.35
(residue ratio 0.70), A consistent with zero (1.0 sigma), B*C < 0; the beta-flow zero(beta) = 1.8284 -
0.18/beta matches v82's stored positions at max dev 0.010, while any 1.707-midpoint alternative predicts
1.895@12 -- REJECTED by 0.076: pair identity (0.828, 2.828) confirmed by FLOW, not numerology. NEGATIVE
CASE (midpoint 1.586, never observed): no sign change; A nonzero at 4.5 sigma -- condition (i) fails;
suppression = background dominance. The L=6 half-integer suppression now reads the same way (stated
prediction). HONEST: the three-term fit is partially degenerate over the narrow window (collinear basis;
the DIRECT zero + flow is the robust extraction and is what the gates test); one geometry, one case each
way; why A vanishes where it does = the remaining derivation. METHOD NOTE: the slope probe (ln|C| rates)
discriminated the mechanism class in ONE measurement before any model fitting -- measure the discriminator
first, fit second. 08_2d_interacting/selection_rule.py (PASS), SELECTION_RULE_RESULT.md. Frozen engine
untouched (194/194).

### #95 -- The resonance atlas: v80-v84 consolidated; one spine; the integration audit's honest catch (v85)

CONSOLIDATION ROUND (the v79 pattern). resonance_atlas.py integrates the arc into one prediction surface;
BEST_METHODS v85 edition adds the component table and methodology rules 10-18. THE ONE-SPINE STATEMENT:
every resonance-regime flip is a logit-type law mu* = anchor + ln(ratio)/(q beta) -- Class I: anchor = a
level, ratio = residue-polynomial root odds, q = 1; Class II: anchor = a level-pair midpoint, ratio = the
two-residue ratio, q = 2. Residues decide attendance; positions geometry-free, multiplicities not; the
thermal regime keeps v77's pi/beta winding. INTEGRATION AUDIT (the self-test): roots(135) hit the stored
v81 trajectories at <= 0.006 (lower, every beta); roots hit the v80 basin flips at <= 0.031; the
selection-rule flow hits the v82 statics at <= 0.014; regime classification matches the v80 p-values; a
live engine check lands 0.003 from the root prediction. THE HONEST CATCH (audit gate D): the L=6 ~1.8
flip is UNCLASSIFIED -- Class-I c drifts 3.1 -> 5.5, and 1.8 is neither a half-integer nor a third at
L=6; likely two conflated trajectories (the v81 trap); recorded on the open list rather than swept under
a law. LESSON: consolidation IS an audit -- colliding every component pair surfaced one object no single
round had noticed was lawless. 08_2d_interacting/resonance_atlas.py (PASS), RESONANCE_ATLAS_RESULT.md,
BEST_METHODS.md v85 edition. Frozen engine untouched (194/194).

### #96 -- The core C surrogate: every banked advance frozen into C beside the engine (v86)

User-directed: "update the surrogate as a core c module and add all the advances we have made."
csurrogate.c/h is a dependency-free C module composing with (never touching) the frozen engine, carrying:
the 10 geometric features and the transferable magnitude model with frozen trained weights and
L-intercepts (v74/v79); the wrap-safe sector test by cyclic-line enumeration (v75); the pi/beta thermal
period (v77/v78); the regime classifier (v80); Class-I flip prediction from frozen residue-polynomial
roots via the logit law (v81/v83); the Class-II static with its flow correction (v82/v84); and
orientation parity stepping (v77/v85) -- each with its banked scope stated in the header, including the
standing wall (nothing here moves the exponential sign problem). VALIDATION, ENGINE-STYLE: the gate
csurrogate.py regenerates reference vectors LIVE WITH A FRESH SEED EVERY RUN (features, sector,
frozen-model magnitude parsed back from the header, atlas numbers live from residue_ratio and
selection_rule), rebuilds with -Wall -Werror, and demands "ALL CASES MATCH THE PYTHON REFERENCE TO
1e-09" -- observed worst deviation 3.6e-15 across 28 configs + 15 class-1 + 4 static references plus API
checks. PORT NOTES BANKED: mst_length includes the origin (Prim, min-image); matrix rank done in exact
integer arithmetic (fraction-free elimination) since min-image displacements are integers; collinear-group
keys are sign-canonicalized rounded unit vectors -- each verified by the exact-match gate rather than by
assumption. 08_2d_interacting/csurrogate.c/h, csurrogate_test.c, csurrogate_params.h (generated, frozen
weights), csurrogate.py (PASS), CSURROGATE_RESULT.md. Frozen engine untouched (194/194).

### #97 -- The C surrogate under test: clean-room, efficiency, the two n-ceilings, and a scope revision (v87)

User-directed test round. CLEAN-ROOM (five files + gcc only) caught three portability bugs, fixed in
shipped source: M_PI is POSIX not strict C99; a -pedantic const-array error; the POSIX feature macro for
clock_gettime -- the module now builds under c99 AND c11-pedantic, -Wall -Werror, gate still 3.6e-15.
EFFICIENCY: features/magnitude 1.5 us (x212 vs Python feats2); atlas laws 3-19 ns (52-355 M/s); per-ANSWER
vs exact ~875,000x (1.5 us vs ~1.3 s per tau-averaged n=3 coefficient), growing ~2.6^n. THE ORDERS-OF-n
ANSWER, two ceilings stated separately: COMPUTATIONAL -- exact C_V measured growing x2.5-3.3 per order
(1.75 ms n=3 -> 745 ms n=9); the surrogate is O(1) in n for atlas laws and O(n^2) for an n-generalized
feature kernel (0.5 us n=3 -> 1.7 ms n=200, scaling probe) -- effectively unbounded; VALIDITY -- the
shipped laws/weights are n=3-derived; higher orders need their own v83-machinery extraction, capped by the
exact wall at roughly n <= 6-7 tau-averaged. THE AUDIT CATCH: fresh end-to-end draws (2.72x, 2.67x)
exceeded the banked pooled gate; the contamination hypothesis for v79's favorable 1.74x draw was TESTED
AND EXCLUDED (0/8 config overlap); the truth is simpler -- four independent draws pool to 2.31x with
per-draw spread 1.74-2.72x, and the earlier pooled figures sat on the favorable side because one lucky
draw dominated. Scope revised openly in csurrogate.h, CSURROGATE_RESULT, cdet_surrogate. LESSONS: ship no
C without a clean-room strict-standards build; and when a fresh draw breaks a gate, first test the
exciting explanation (contamination), then accept the boring one (spread) -- and widen the pool, not the
goalposts. 08_2d_interacting/csurrogate_bench.c, CSURROGATE_BENCH_RESULT.md, portability fixes in
csurrogate.c/csurrogate_test.c, scope revisions in csurrogate.h/cdet_surrogate.py. Frozen engine untouched
(194/194).

### #98 -- The order axis: the spine survives n=4 and (partially) n=5; exact-determinant numerics catch (v88)

The v83 logit-map extraction fired at higher orders. n=4 ((1,2,3,4), beta=20): curve fits at chi/dof 0.04;
roots 0.156/0.643 -- a pair straddling 1/2 with parameters DISTINCT from every n=3 set (min distance
0.185), same law; beta-transfer with NO refitting verified by direct n=4 sign scans at beta 14/24, max dev
0.024 (the beta=14 lower flip at 0.001). n=5 ((1,2,3,4,5)): the practical wall arrives exactly where v87
predicted (signal 20x smaller, s/n 4.3) yet the curve is coherent -- the LOWER root 0.402 resolved and
live-verified (dev 0.011); the upper root flagged MARGINAL and not gated. THE SPINE IS NOT AN n=3 ARTIFACT.
The C surrogate gains its first higher-order parameter sets (ATLAS_ROOTS_N4/N5 +
surr_class1_flips_order(), marginality documented); gates re-passed. THE NUMERICS CATCH (the fresh-seed
gate working as designed): vol^(1/3) used numpy's float determinant -- ~1e-13 noise on singular integer
matrices (vol^(1/3) ~ 1e-5 instead of exact 0) -- mismatching the C cofactor noise on a random config; the
displacement matrix is integer-valued by construction, so BOTH sides now use the exact integer determinant
(feats2 corrected, banked note; ~1e-4 ln effect on frozen weights, negligible). NEW OPEN OBSERVABLE: the
root flow with n (three orders on record, geometry confounded -- needs matched-geometry sequences).
LESSON: integer-valued quantities deserve integer arithmetic; float library noise differs across
implementations and a cross-language exact-match gate finds it. 08_2d_interacting/order_axis.py (PASS),
ORDER_AXIS_RESULT.md, C extension in csurrogate.{c,h}/csurrogate_params.h/csurrogate_test.c, feats2
correction in surrogate2.py. Frozen engine untouched (194/194).

### #99 -- The deep partner: the ~1.8 object identified; two anomalies closed; the creep measured in position (v89)

One level-2 residue-polynomial extraction (L=6, (1,2,4), beta=20, small-f-weighted grid) resolved THREE
roots and closed two dangling anomalies at once. f* = 0.0116 (c = -4.44) IS the unclassified ~1.8 object
-- level-2's deep lower partner, Class I after all; f* = 0.4437 is the central flip (beta >= 16 max dev
0.010); f* = 0.9504 (c = +2.95) IS v80's dangling "2.2 family" (flow devs 0.003-0.011). The v85 c-drift is
QUANTIFIED as sign-scan noise: through the deep crossing |p| ~ 0.4-5e-9 vs the v81 NT=120 sem ~ 3.2e-9 --
signs noise-dominated over +/-0.04, exactly the observed scatter. Level 2 has 3 roots vs level 1's 2:
root count varies by level (multiplicity law). THE DESIGNED MISS BANKED AS MEASUREMENT: a value-level
beta-transfer at beta=14 found the zero at ~1.768, not the predicted 1.683 -- the deep root's pure logit
law is LARGE-BETA SCOPED, with Delta(beta) = +0.114@12 / +0.086@14 / +0.034@16 / +0.003@28 decaying
~e^{-0.3 beta}: the adjacent level-1 comb's beta-compensated contamination at the ~1e-9 cancellation
floor -- THE v83 CREEP MEASURED IN MU-POSITION for the first time; the larger-|p| roots show no departure.
LESSONS: an anomaly flagged honestly (v85's gate D) plus better machinery equals a clean kill later;
small-f (deep) roots live at the cancellation floor where scans must be VALUE-level and laws carry
adjacent-comb corrections; and a transfer miss at a pre-set gate is a measurement of the correction, not
a failure of the law's scoped form. 08_2d_interacting/deep_partner.py (PASS), DEEP_PARTNER_RESULT.md.
Frozen engine untouched (194/194).

### #100 -- The creep cross-checked both ways: the deep object's law rewritten; a possible cross-L anchor (v90)

User-directed two-window round: surrogate side and brute-force side run independently on the creep, then
compared. BRUTE FORCE (value-level zeros, beta 10-28): the deep trajectory is ANCHORED, z = 1.824(+/-0.022)
- 0.72(+/-0.34)/beta at chi/dof 0.53; pure logit REJECTED (chi/dof 2.90, fitted L contradicts the
extraction). Phase-0 catch: v89's Delta(beta) "decay" was an artifact of a beta=20-anchored baseline --
Delta(20) ~ 0 by construction; fit z(beta) itself. SURROGATE SIDE: the anchor sits 0.2 sigma from
2*sqrt(2)-1 = 1.8284 -- THE L=8 STATIC'S EXACT ANCHOR -- at a lattice whose integer spectrum contains no
sqrt(2) (possible L-INDEPENDENT anchor), with 11/6 alive at 0.4 sigma; selectivity table explains why only
extreme roots feel the floor. THE FROZEN DISCRIMINATOR DECIDED: geometry-independence required by the
anchored reading, forbidden by the per-geometry-logit reading -- (1,3,5) scans land at devs
0.001/0.001/0.011: UNIVERSALITY WINS. REVISION banked openly (note atop DEEP_PARTNER_RESULT): the ~1.8
object is the THIRD instance of the static class (at L=6, where naive midpoints were excluded); the
f*=0.0116 root is real at beta=20 but the polynomial's deep tail is beta-dependent -- why logit failed.
WHAT THE TWO WINDOWS SHOWED: brute force alone = an anonymous anchored fit; surrogate alone = a wrong
logit prediction; together = law-form correction + two-candidate anchor + decided universality. LESSONS:
when a baseline is extracted at one parameter value, deviations defined against it vanish there by
construction -- fit the trajectory, not the deviation; and a designed cross-window disagreement is the
fastest law-form test. OPEN: anchor identity (needs +/-0.005); the slope's residue formula; the cross-L
anchor question. 08_2d_interacting/creep_crosscheck.py (PASS), CREEP_CROSSCHECK_RESULT.md, revision note
in DEEP_PARTNER_RESULT.md. Frozen engine untouched (194/194).

### #101 -- The correction propagated: both prediction surfaces updated to the v90 law (v91)

User-directed consolidation round ("update both to correct"). The v90 two-window correction -- the L=6
deep ~1.8 object is an ANCHORED, GEOMETRY-INDEPENDENT static, not a logit-flow root -- now lives in both
executable surfaces, not just the result docs. C SURROGATE: ATLAS_L6_DEEP_A/B (1.824, -0.72) +
surr_static_l6_deep(beta) with the open anchor identity documented; the Class-I scope CORRECTED in the
header (logit flow = mid-range roots only; deep small-f roots live at the cancellation floor where the
polynomial tail is beta-dependent -- route to the static family); closed-form test added; fresh-seed gate
re-passed at 3.55e-15; pedantic-C11 clean. PYTHON ATLAS: gate-D object recorded RESOLVED; static_l6_deep()
added; NEW AUDIT GATE G -- the corrected law vs the v90 stored value-level zeros (max dev 0.022, gate
0.025); audit now A-G, PASS. HISTORICAL MODULE: deep_partner.py carries a REVISED docstring header (the
Delta-decay framing was a baseline artifact; data retained as the historical record its gates test);
self-test PASS. LESSON: a correction that lives only in a result doc is a correction waiting to be
forgotten -- propagate it into every executable surface and add a gate that fails if the old reading
creeps back. 08_2d_interacting/CORRECTION_PROPAGATION_RESULT.md; edits in csurrogate.{c,h},
csurrogate_params.h, csurrogate_test.c, resonance_atlas.py, deep_partner.py. Frozen engine untouched
(194/194).

### #102 -- The anchor test: the law scoped, the floor's tails audited, the question reopened with the bridge tool (v92)

User-directed round on the tau0/tau1 anchor question, finishing with Paul's cdet-diagnose-bridge v0.57
edited for the job. RESULT 1 (SOLID): the deep trajectory rises THROUGH both v90 candidates above beta~32
-- the v90/v91 anchored law is an EFFECTIVE intermediate-window form (beta 10-32), not an asymptote;
scopes propagated. RESULT 2 (SOLID, METHODOLOGY): the deep-beta heavy-tail audit -- kurtosis ~4500, 98% of
variance in the top 0.1% of samples; single-draw CLT errors INVALID at the floor (a "+8 sigma" and a "-4.5
sigma" at the same point were both outlier artifacts of ~0.00 +/- 0.02); required protocol = multi-draw
inter-draw errors + dense grids (sparse linear fits curvature-biased); two in-flight catches banked (a
window-edge artifact behind a premature "universality broken" call; live gates redesigned multi-draw).
RESULT 3 (OPEN, QUANTIFIED): honest record z(48)=1.846(9), z(56)=1.8407(103) -> a_inf = 1.8437 +/- 0.0068
(beta=64 unresolved); the edited bridge tool (anchor_bridge.py) applies its own null-model rule -- the
framework alphabet near 1.84 saturates (rarity 83% at 1 sigma) -> NOT RIGID, one-of-many; the octagon
chord sqrt(2+sqrt2) [Q(sqrt2), the tau1 field] is the LEADING candidate at 0.60 sigma, recorded as
leading, NOT identified; sigma* = 0.0008 (72x budget) or the STRUCTURAL route (the background-zero
derivation -- the derived form's field answers tau0-vs-tau1 with no sigma). A withdrawn single-draw
preliminary ("plateau 1.8486, chord 0.17 sigma") is retained as the cautionary record. LESSONS: at the
cancellation floor, error bars are a measurement of their own; a hit without the null number next to it is
not a result; and when the alphabet saturates the band, the only honest closes are precision below sigma*
or derivation. 08_2d_interacting/anchor_test.py (PASS), anchor_bridge.py (imported, edited),
ANCHOR_TEST_RESULT.md; constant corrections in csurrogate_params.h/csurrogate_test.c/resonance_atlas.py.
Frozen engine untouched (194/194).

### #103 -- The exponent-balance law: the deep static derived as 11/6, the field question answered (v93)

The structural route the bridge tool named primary (v92), executed. THE LAW: by the v78 lemma the
stripped <C> in a saturated window is a FINITE polynomial in the deviations e^{-beta|mu-eps|} (weights
<= 8); a zero locks where two monomials balance -> mu* = (sum w_i eps_i)/(sum w_i), an integer-weighted
mean of the lattice's own LEVELS, approached as z = mu* + ln(r)/(q beta), q = sum w_i (the one-spine
form, now derived). FIELD THEOREM (the tau0/tau1 answer): statics live in the spectrum's field -- Q at
L=6, Q(sqrt2) at L=8; the octagon chord is EXCLUDED STRUCTURALLY at L=6; no cross-anchor mixing. L=8
verification exact: the (1,1) balance of (2sqrt2-2, 2sqrt2) = 2sqrt2-1 = the v84 static, with the
rejected 1.707 = the naive adjacent midpoint -- both v84 facts accommodated. FINITE MENU in (1.80,1.88):
{11/6, 13/7, 15/8}. FROZEN DISCRIMINATOR (registered before measuring): 11/6 -> z(36)=1.8475,
z(40)=1.8461; 13/7 -> 1.8369, 1.8389; MEASURED honest dense: z(36)=1.8450(30), z(40)=1.8457(46) ->
chi2 0.7 vs 9.5, ~80:1 FOR 11/6; global law z = 11/6 + 2.67(54)/(6 beta) fits all four honest points at
max 0.38 sigma. VERDICT: the deep static = the RATIONAL 11/6 (tau0-side), ~2.6 sigma by the frozen test;
the v92 "NOT RIGID one-of-many" upgraded to "derived 3-member menu + frozen-test selection". HONEST
SCOPE: 13/7 disfavored not dead; ln r measured (+2.7(5)) not derived (the residue formula, queued); the
(2,3)-window kill-shot INCONCLUSIVE -- that window is SUPPRESSED (~30-50x below the (1,2) window,
|<C>| <~ 0.04e-9 at beta 20-28), itself a datum (queued); the parity/degeneracy rule for which windows
carry A=0 (the deeper background-zero why) remains the head of the program.
08_2d_interacting/exponent_balance.py (PASS), EXPONENT_BALANCE_RESULT.md; propagation:
surr_static_l6_deep_law + ATLAS_L6_DEEP_ID/LNR in the C surrogate (DEEPLAW test), l6_deep_id + gate I in
the atlas. Frozen engine untouched (194/194).

### #104 -- The side-by-side: surfaces parity-locked, the law tested out-of-sample, the identification reopened (v94)

User-directed: update both the surrogate and the brute-force versions, test side by side on new values.
SETUP: both surfaces carry the law + the 13/7 competitor (surr_static_l6_deep_law/alt in C;
atlas.static_l6_deep_law/alt in Python; parity 1e-15 across six betas inside the csurrogate gate);
out-of-sample predictions FROZEN TO DISK before any scan. MEASUREMENTS (honest dense protocol): z(30) =
1.8138(37) -- the SCOPE DEMONSTRATION (beta=30 is in the v92 crossover window; both lines miss by >= 8
sigma, as the beta~36 law floor requires; also caught+fixed a harness root-selection bug); z(44) =
1.8510(76); z(52) = 1.8527(52). VERDICT: out-of-sample chi2 5.3 vs 1.0 -> ~9:1 FOR 13/7, against the v93
frozen test's ~80:1 for 11/6 -- NET: the identification is REOPENED. Six-point pool: 11/6 refit chi2/dof
0.96; 13/7 refit 0.32; CONSTANT 1.8467(21) 0.47 -- all acceptable; the constant reading revives the chord
(0.5 sigma) and pushes both menu rationals out (5-6.5 sigma): the MENU-VS-FLATNESS TENSION. The law's
derivation, field theorem, and L=8 verification stand; the menu's DEGREE BOUND is the raised decisive
item (n=3 has three g0 factors per spin -> plausibly weight <= 6, removing 13/7 and 15/8 structurally; if
so and z stays flat, the law needs a new term or the chord needs a mechanism the field theorem forbids).
Freeze-then-predict selected 11/6 (v93) and unselected it (v94) -- the discipline working as designed.
08_2d_interacting/law_sidebyside.py (PASS), SIDE_BY_SIDE_RESULT.md; status revisions in
csurrogate_params.h, resonance_atlas.py (l6_deep_const), exponent_balance.py (revised header). Frozen
engine untouched (194/194).

### #105 -- The degree bound: settled by a symbolic census; the menu corrected; the tension dissolved (v95)

METHOD: the pure-Python CDet port run on SYMBOLIC occupancies (one symbol per spin x window level,
numeric saturation elsewhere; sympy determinants; the n=3 connected combination expanded exactly) -- the
exact polynomial of the stripped <C> in (f2, f3, delta1, delta0), generic support = intersection over
tau draws. THEOREM (verified): max total weight = 2n+1 = 7 at n=3 (the up determinant is (n+1)x(n+1) --
it carries the external to/ti vertex: 4 up + 3 down propagators, each linear in occupancies); v93's "8"
(matrix dimension, not propagator count) and v94's conjectured "6" (missed the external vertex) BOTH
WRONG; support FULL (all 330 monomials). CORRECTED MENU: balances come from exponent DIFFERENCES --
near the object: {25/14, 9/5, 20/11, 11/6, 24/13, 13/7, 15/8, 17/9}, mu* = (2Da+3Db-Dc)/(Da+Db-Dc-Dd),
q = |Da+Db-Dc-Dd|; all rational (field theorem stands; chord stays excluded; the v94 "15/8 structurally
excluded" note corrected -- in the menu, dead only empirically). TENSION DISSOLVED: 24/13 = 1.84615
(q=13) is 0.26 sigma from the v94 constant 1.8467(21) and its 1/(13 beta) approach is near-flat over
beta 36-56 -- the "constant" reading IS the q=13 member (fit: ln r = +0.13(1.07), chi2/dof 0.48; vs
13/7 at 0.32, 11/6 at 0.96). STATUS: open among {13/7, 24/13}, 11/6 disfavored; closing routes (a) THE
COEFFICIENT PROGRAM -- tau-average the 330 census coefficients and predict the realized zero outright,
no fitting; (b) deep-beta precision (~0.005 separation at beta=72). LESSON: two consecutive wrong
hand-bounds were settled in one stroke by making the algebra itself compute -- when a structure question
stalls, ask the object, not the napkin. 08_2d_interacting/degree_bound.py (PASS),
DEGREE_BOUND_RESULT.md; revisions in exponent_balance.py, law_sidebyside.py, csurrogate_params.h
(ATLAS_L6_DEEP_CAND), resonance_atlas.py (l6_deep_cand). Frozen engine untouched (194/194).

### #106 -- The coefficient program, phase 1: the freeze instrument, the background alive, the prediction test honestly inconclusive (v96)

THE INSTRUMENT: FrozenCDet (window occupancies by hand: <=1 -> 1, level2 -> s, level3 -> 0, far levels
physical), validated against v89 (A(20) = +1.853(75) vs ~+2) and proven FAITHFUL at the physical point
(the frozen value at (s_phys, mu_phys), the frozen value at mu_exp = 1.84, and the raw physical value
agree within errors at beta=36 -- all consistent with the physical zero). The per-config strip identity
fails through far-level ANTIPERIODIC IMAGES -- the creep carrier identified concretely; typical-config
determinants scale exactly; the tau-averaged object is the honest one. THE BACKGROUND IS ALIVE:
A(beta) = 1.853(75)/0.839(102)/0.277(45)/0.167(36) e-9 at beta = 20/28/36/44 -- A(44) > 0 at 4.6 sigma:
NO background-zero in the (1,2) window, hence no midpoint static (consistent with no 3/2 flip). The
decay's effective rate ~0.10-0.12 with prefactor curvature (pair rates 0.099(16)/0.139(25)/0.063(34));
the asymptotic rate (= 2 - z_inf in the root-flow picture: 1/7 vs 2/13) NOT yet reached -- the
13/7-vs-24/13 status unchanged. THE PREDICTION TEST: the naive {A, c1} root lands ~2.5x below the
physical f2* -- INCONCLUSIVE, not failed (faithfulness passes; the gap sits in A's heavy-tailed
estimation -- two batches at 2 sigma tension -- and small-s curvature below the grid). PHASE-2 SPEC,
computed: A to +/-5% (~500 draws x 2048 per beta), a geometric s-grid below 0.002, mu_exp pinned per
beta; then the polynomial root is a PARAMETER-FREE prediction of the zero. LESSON: an instrument is only
as good as its noisiest coefficient -- validate faithfulness first (cheap), then budget the statistics
where the root actually lives. 08_2d_interacting/coefficient_flow.py (PASS, FrozenCDet reusable),
COEFFICIENT_FLOW_RESULT.md. Frozen engine untouched (194/194).

### #107 -- The parity table: the A=0 rule falsified by its own frozen test; the suppression pattern; the v84 static reread (v97)

The sharpened background-zero question, measured with the generalized WindowFrozen across both lattices
(beta=28, multi-draw). THE TABLE: W6(0,1) A = -0.023(15) [first-empty deg 36]; W6(1,2) +0.839(102)
[27 ODD]; W6(2,3) +0.025(8), residue dead [14]; W8(0.828,1.414) -0.0208(55) [60]; W8(1.414,2.0)
+0.497(76) [39 ODD]. THE FROZEN TEST, HONESTLY SCORED: at 4/4 consistency the binary rule "even
first-empty degeneracy => A = 0" was registered and tested on W8(0.828,1.414): A = -0.0208(55), 3.8
sigma from zero -- THE STRICT RULE IS DEAD BY ITS OWN PREDICTION. Survives: a robust SUPPRESSION
pattern (odd windows A ~ +0.5-0.85; even windows |A| 20-40x smaller, 4-30x in |A/c1|) -- five-window
observation, unpaired-mode mechanism a hypothesis only. THE v84 STATIC REREAD: at mu=1.8284, beta=28
the W8(1.414,2.0) background equals ~95% of its dominant deviation term -- the L=8 "static" is an
A-vs-f(2.0) ROOT-FLOW CROSSING, the same structure whose L=6 version produced an effective anchored law
that failed at deep beta. FROZEN PREDICTION REGISTERED (untested): the L=8 deep-beta zero rises past
2*sqrt(2)-1 above beta ~ 32-40, replaying the L=6 crossover. INSTRUMENT HARDENING, two catches: the
conditioning rule s <~ 10 e^{-beta xi_probe} (a 1e12 blowup at s=0.02 observed first); the mask-
tolerance bug (1e-9 vs 1e-6 rounding silently emptied level 1.414 -> the scout's FALSE ZERO; the
occupied-levels check now gated). Honest negative: the W6(2,3) suppression is NOT site-projection
(weights uniform by translation invariance); its mechanism stays open. LESSONS: a 4/4 arrangement is a
hypothesis, not a rule -- register the prediction and let it die in public; and at the e-11 scale a
tolerance mismatch is a physics error. 08_2d_interacting/parity_table.py (PASS, WindowFrozen reusable),
PARITY_TABLE_RESULT.md. Frozen engine untouched (194/194).

### #108 -- The method audit of v97: the confound found, the prediction quantified, the queue reordered (v98)

The v97 round audited against the KT-RG method v3.1 (Watford; outputs banked in
08_2d_interacting/METHOD_AUDIT_v97.md, method not reproduced). GOT RIGHT: prediction registered before
the rule, killed by its own test; the v84 reread as a required-value move; clean negatives; catches
gated. GOT WRONG: model diagnosis skipped on a new instrument (the false zero was briefly believed; the
mask gate belongs BEFORE the first measurement); the conditioning rule derived by explosion instead of
two lines in advance; the registered prediction directional rather than quantitative; only one
hypothesis branch stated in advance (so the 3.8-sigma result read as falsify-then-retreat instead of a
measured discrimination); #107 classification inflated ("IS a root-flow crossing" from one-point
evidence -> downgraded to CANDIDATE). MISSED, run retroactively with new content: (1) THE CONFOUND --
across the whole v97 table, odd first-empty degeneracy coincides with first-empty-level RATIONALITY
(at L=8 the only odd level in range, 2.0/deg 39, is the only rational one; L=6 is all-rational): the
falsification window was the one where both hypotheses agree -- the weakest available test; the
surviving suppression pattern is TWO patterns; the next parity window must discriminate. (2) The
deviation as integer ratios: A_odd/A_even = 36.5(24)/33.6(12)/23.9(7.3) vs candidates {36, 24};
60 excluded at 4.9 sigma; test UNDERPOWERED -- A_even to +/-10% required. (3) The portfolio
re-prioritization REVERSES the queue: coefficient phase 2 (unlocks the identification, the residue
formula, and predicts the L=8 curve) outranks the L=8 scan; its perceived blocker dissolves on v96's
own SNR-is-beta-independent discovery. (4) The stall check on the four-round 13/7-vs-24/13 oscillation
prescribes the exact-structure route (census coefficient signs) over another rate fit. FIXED IN-TURN:
A8(40) = +0.1135(266) measured (mask gate BEFORE measuring), two-point rate 0.1231(233), and the
prediction QUANTIFIED: frozen z8 = {36: 1.8378, 40: 1.8417, 44: 1.8449, 48: 1.8475 +/- ~0.010,
56: 1.8517} with z8(28) = 1.8268 reproducing the v84 static as consistency -- the static should be
violated by +0.013 already at beta=40. LESSON: the protocol's back half (freeze-then-predict, gates,
banked corrections) held; the front half (diagnose the instrument first, table the differences before
promoting a pattern, write deviations as integer ratios at registration, order the queue by leverage)
is now standing protocol. 08_2d_interacting/METHOD_AUDIT_v97.md; parity_table.py revised
(FROZEN_CURVE_Z8, A8_RECORD, the downgrade note). Frozen engine untouched (194/194).

### #109 -- Coefficient program phase 2: the heavy-tail problem solved; the frozen polynomial measured; THE TWO-SECTOR DISCOVERY (v99)

THE ESTIMATOR: the s=0 integrand autopsy (top 1% of tau-samples carry 95.5% of the mass at clustered
times; survival tail index alpha ~ 0.55 -- INFINITE VARIANCE, error bars fiction; demonstrated by a
24-draw brute mean swinging -0.178 -> +0.023 on late spikes) -> mixture importance sampler (1/2 uniform
+ 1/2 truncated-Laplace cluster mode; weights <= 2, mean 1; validated analytically at 0.5 sigma over
300k; ~31x variance reduction; the +/-5% spec drops from ~26 min to ~50 s per point). THE FROZEN
POLYNOMIAL (beta=36, mu_exp=1.845, all IS): A = +0.3700(108) [supersedes v96's tail-biased +0.277(45)];
grid P(0.0005)/P(0.001)/P(0.002)/P(0.004) = +0.2553(127)/+0.1678(118)/-0.0345(74)/-0.4063(126); root
s* = 0.00183(8) -> z_pol(36) = 1.8249(12); internally smooth (frozen(s_phys=0.0037584) = -0.3391(143)
sits on it). THE REGISTERED TWO-BRANCH TEST, SCORED: the root-flow branch (root at the physical f2* =
0.00376(41); small-s slope bending to ~ -98) EXCLUDED at ~10 sigma -- the slope stayed ~ -200 down to
s = 0.0005. And the failure branch's missing piece IDENTIFIED: THE TWO-SECTOR DISCOVERY -- v96
faithfulness FALSIFIED at 3.4 sigma at IS power (physical(1.845) = +0.030(108), the v93 zero is real,
vs frozen-at-the-physical-point = -0.3391(143)). The 1e-13 argument compared occupancy values but
ignored exponentially growing coefficients: the level-1 particle branch (1-nf1) e^{(mu-1)tau} =
e^{-(mu-1)(beta-tau)} is O(1) in the tau -> beta corner -- the freeze kills these ANTIPERIODIC IMAGES;
physically they form a hole-image sector Delta(s_phys; 36) = +0.369(109) e-9, the same size as
everything else at the zero. The physical zero is the root of [frozen polynomial + Delta(s; beta)] --
which is why the frozen root sits 2.05x below the physical f2*. The v96 "faithfulness PASS" was the
underpowered gate the v98 audit flagged: AUDIT VINDICATED. CONSEQUENCES REGISTERED: the literal-rate
menu bookkeeping (v93/v95) is suspect for hole-side monomials (the tau-corner saddle reduces effective
hole rates; tau-integrated re-derivation queued); the empirical pool unaffected; v96 #106 "proven
FAITHFUL" downgraded in-module; the decisive 13/7-vs-24/13 object is now Delta(s; beta). LESSONS: an
infinite-variance estimator cannot be fixed by more draws -- autopsy the integrand first; and an
identity "forced analytically" is only as good as every factor in the product -- occupancy differences
of 1e-13 times coefficients of e^{+30} are O(1). 08_2d_interacting/coefficient_phase2.py (PASS, IS
sampler reusable), COEFFICIENT_PHASE2_RESULT.md; downgrade notes in coefficient_flow.py and
exponent_balance.py (both still PASS). Frozen engine untouched (194/194).

### #110 -- The Delta sector: the v99 "second player" is a delta1 x f2 CROSS-TERM, not a background; measured, beta-growing, reconciling (v100)

THE INSTRUMENT: Delta1Frozen (level 1 kept PHYSICAL -- antiperiodic images alive; level2 -> s, level3
-> 0, far physical), gated against the raw physical value at (s_phys, mu) (-0.041(79) vs +0.030(108),
0.5 sigma); Delta(s;beta) = Delta1Frozen(s) - FrozenCDet(s) recovers Delta(s_phys;36) = +0.334(81) vs
the v99-inferred +0.369(109). THE STRUCTURAL DISCOVERY: Delta(0;beta) ~ 0 at BOTH beta (+0.036(29) at
28, -0.009(20) at 36) -- the hole sector VANISHES when level 2 is empty, so Delta is NOT an independent
background (the literal v99 framing) but a delta1 x f2 CROSS-TERM, the coefficient the single-level
freeze structurally omits; the true object is the full (f2, delta1) polynomial, of which the v99 freeze
is only the f2-diagonal. THE CROSS-SLOPE: matched-s secants over the identical [0, 0.00376] (legit since
Delta(0)~0) -- d1(28) = +41.8(13.2), d1(36) = +88.8(21.5) e-9: GROWS with beta (~2.1x over delta-beta=8,
1.9 sigma). DIRECTION: c1_eff = c1_frozen(-202) + d1(+89) = -113 moves the linear root 0.00183 -> 0.00327
toward the physical f2* = 0.00376 (residual = s^2 curvature, matches v99's smooth grid) -- the two-sector
picture confirmed AND corrected: one polynomial, one beta-growing cross-coefficient. THE OPEN (registered,
spec'd): the 13/7-vs-24/13 closure is now the assembled root flow z(beta) = 2 - ln s*(beta)/beta with
s*(beta) the root of A + c1_eff s + c2 s^2 -- needs A, c1_frozen, d1, c2 on a common grid (only beta=36
complete; d1 at 28, 36); SPEC: the full coefficient grid at beta in {36,44,52} to +/-5% (IS, ~50 s/pt),
assemble z(beta), test vs the empirical pool's deep points (48,52,56) as a FROZEN PREDICTION. PREDICTION
REGISTERED (directional): the cross-term keeps s* above the frozen root at all beta, so z_assembled >
z_pol, and the ASSEMBLED curve -- not the one-sector frozen root -- is what the pool measures (the
FROZEN_CURVE_Z8 L=8 prediction inherits the same one-sector caveat). LESSON: a "background that appears
only at the physical point" is the signature of a CROSS-TERM, not a new sector -- test it at the empty
point first (Delta(0)) and the structure names itself. 08_2d_interacting/delta_sector.py (PASS,
Delta1Frozen reusable), DELTA_SECTOR_RESULT.md. Frozen engine untouched (194/194).

### #111 -- Consolidation: the surrogate and brute-force C brought current; all mds self-contained (v101)

A sweep round, no new physics. THE C SURROGATE (csurrogate.*): the params header gained the full v96-v100
status block (background alive; the v96 "faithfulness" FALSIFIED at 3.4 sigma; the two-sector delta1 x f2
CROSS-TERM picture; menu open among {13/7, 24/13}; the assembled root flow as the registered closure),
with new constants (ATLAS_L6_ZPOL36, A_IS36, C1_FROZEN, F2STAR, XSLOPE_B/D); and the frontier is now
CALLABLE -- surr_l6_zpol36() (one-sector frozen root 1.8249), surr_l6_cross_slope(beta) (the beta-growing
cross-slope), surr_l6_root_linear(beta) (the cross-term-corrected root). Four new gate cases
(ZPOL/XSLOPE/XGROW/XROOT) pass; the surrogate still matches the Python reference to 1e-9 and builds
-Wall -Werror. THE BRUTE-FORCE C (cdet2d.c, cdet_small.c, cdet_vs_naive.c): stamped with a v101 note as
the exact ED-validated ground truth the surrogate approximates, intentionally unmodified; all three still
compile against the frozen engine. SELF-CONTAINMENT: every md audited for references to missing modules;
the one true orphan -- the engine golden-regeneration tooling (gen_golden.py, gen_golden2.py,
cdet_reference/), referenced by START_HERE.md and engine*/README.md but never bundled -- corrected in
place (golden.json SHIPS, 16 KB, authoritative; make test reads it, 194/194; the regeneration pointer now
aims at the bundled cdet_port.py, which reproduces the goldens to 1e-9). README gained a live-record
pointer (the ledger + the deep-beta frontier + the surrogate's role). LESSON: a self-contained archive is
a claim that must be tested -- the orphan scan found docs instructing the reader to run scripts that were
never shipped; ship the authoritative artifact (golden.json) and point regeneration at what IS bundled.
08_2d_interacting/CONSOLIDATION_v101.md; csurrogate.{c,h}, csurrogate_params.h, csurrogate_test.c
updated; CSURROGATE_RESULT.md noted; engine*/START_HERE.md + engine*/README.md de-orphaned. Frozen engine
untouched (194/194).

### #112 -- Surrogate vs brute-force, side by side: five claims vs exact CDet; discrepancies on BOTH sides (v102)

Ran the C surrogate head-to-head against the brute-force exact CDet (the validated ground truth), fresh
and out-of-sample, both lattices -- the check the existing gate omits (it tests C == Python MODEL, port
fidelity; this tests MODEL == TRUTH, accuracy). AGREES (within scope): sector EXACT (0/120 disagreements,
L=6 and L=4); ln-magnitude median 1.81x (within the stated 1.7-2.3x scope); the 13/7 deep-static line
closer to the brute pool (chi2 1.7) than 11/6 (chi2 5.6); background A(36) 0.370(11) vs fresh IS 0.349(19)
(1.0s); one-sector z_pol(36) 1.8249 vs fresh-brute 1.8251 (0.0002); cross-corrected root_linear 1.8410 vs
physical ~1.845 (0.004 s^2 residual, closes 80% of the gap, right direction). DISCREPANCY 1 (surrogate
side): surr_class2_static -- the v84 L=8 K-flow form (DECREASING toward 1.8284) -- diverges from the v100
brute root-flow reread (RISING with beta) by up to 0.021 over beta 28-44, OPPOSITE slope; the carrier was
never updated when v97/v100 reread the L=8 static as a root-flow crossing. Flagged with a supersession
note in csurrogate.h + params (the decisive deep L=8 zero scan -- the queued crossover test -- is the
arbiter; the v84 form retained as history, NOT silently overwritten with the still-unconfirmed v100
curve). DISCREPANCY 2 (brute/glue side): the first harness used z = 2 - ln s*/beta; the correct relation
(s* ~ e^{-beta(2-z)}) is z = 2 + ln s*/beta -- a spurious 0.35 "discrepancy" caught precisely BECAUSE the
surrogate's z_pol36 was trustworthy and the brute glue was not. ln-magnitude structure: the 1.81x median
hides a two-directional tail -- the surrogate over-predicts deep-bulk magnitude by up to 64x (floors near
-19.7 while truth reaches -24) and under-predicts the most compact config ~19x -- the documented
"deep-bulk strictly unpredictable" regime boundary, not a regression. LESSONS: port-fidelity is not
accuracy -- run the model against truth, not only against its own Python twin; in a side-by-side the
more-trusted side is the instrument that finds the other's bug; a carrier left un-updated through a
reread becomes silently wrong with the OPPOSITE slope -- the worst kind. 08_2d_interacting/
SURROGATE_VS_BRUTE_RESULT.md, surrogate_vs_brute.py (PART 1 reusable gate); csurrogate.h + params
supersession notes. Frozen engine untouched (194/194).

### #113 -- PRECISION: naive float64 silently drops the deep-beta antiperiodic images; the stable engine fixes it, mpmath certifies it (v103)

Asked whether higher precision was needed, mirrored the exact CDet recursion in 200-digit mpmath and
compared on the DEEP-BETA CORNER configs (clustered tau near beta -- 95% of the heavy-tail MC mass):
naive float64 is WRONG by 8%-370%, ZERO correct digits on the worst. MECHANISM: g0 = sum_k U U occ_k
exp(-xi tau); for tau near beta and a far OCCUPIED level (xi<<0) the particle branch needs
(1-nf)exp(-xi tau) = exp(-xi tau - softplus(-beta xi)) ~ O(1), but float64 computes (1-nf) as
1.0-1.0 = 0 (nf rounds to 1) and the term VANISHES -- exactly the antiperiodic images that carry the
deep structure. FIX (the brute's final form): assemble each exponent in the LOG DOMAIN before exp, so
every term is bounded -- stable_cdet.StableCDet / StableFrozen, pure float64, ~2.2 ms/call, CERTIFIED
against mpmath-200 to ~1e-9 on the corner configs (vs 370% naive). mpmath (mp_cdet.MPCDet) is the
CERTIFIER, not a production engine (needs dps 120-200 for deep beta, ~10^4-10^5x too slow for MC).
WHAT SURVIVES CERTIFICATION (re-measured stable, beta=36, IS): frozen A(36) +0.3754(128) vs naive
0.370(11) (0.3 sigma -- the freeze removes far images anyway); the delta1 x f2 cross-term
Delta(s_phys) +0.453(135) vs naive +0.334(81) (0.8 sigma -- two-sector mechanism real);
faithfulness still FALSIFIED 3.2 sigma (was 3.4). WHAT MOVES: physical(1.845) stable -0.1915(48) vs
naive +0.030(108) -- ~4 sigma, and the error bar HALVES (corner float64 garbage was inflating variance
too). CONSEQUENCE: the deep-beta ZERO is NOT where naive placed it; the EMPIRICAL POOL {z(36)=1.845,...}
that anchors the 13/7-vs-24/13 menu was measured in naive float64 on the corrupted corner-dominated
samples -- the pool, and the menu identification, MUST be re-measured on the stable engine. FINAL-FORM
READING: the brute's final form is the stable log-domain engine (the precision wall was an ALGORITHM
artifact -- huge intermediates that cancel -- not a need for bignum); the surrogate's frozen-side
carriers (A, zpol, cross-slope) survive, its pool-fit carriers (menu lines, static family) inherit a
PENDING RE-FIT (caveat added to params); both models measure ONE object (the coefficient polynomial and
its root flow) whose instrument was systematically wrong on the dominant configs. None of it touches the
wall (R, 2^n unchanged) -- it is a theory of WHERE the sign structure sits, now measured correctly.
LESSON: precision is not a knob to crank uniformly -- diagnose WHERE it bites (the corner integrand, not
the MC variance), certify with a slow exact tool, then fix the ALGORITHM so the fast engine is correct.
08_2d_interacting/stable_cdet.py (PASS, certified), mp_cdet.py (PASS, certifier), PRECISION_RESULT.md;
csurrogate_params.h precision caveat. Frozen engine untouched (194/194).

### #114 -- The deep-beta pool re-anchored on the stable engine: a precision fix needs a robust estimator too; the pool SURVIVES; v103's "zero moves" RETRACTED (v104)

The mandatory re-anchor -- and a self-correction. v103 fixed a real per-config precision bug (the stable
engine stands) but then drew a conclusion from a SINGLE importance-sampling draw (physical(1.845) =
-0.1915(48), "the deep zero moves ~4 sigma") whose error bar is fiction. AUTOPSY: the STABLE integrand is
still heavy-tailed (tail index alpha ~ 1.06 -- better than naive 0.55 but still infinite-variance), mass
on EDGE configs (one tau near the boundary -- the antiperiodic image), distinct from naive's clustered
mass. Under alpha ~ 1 single IS errors are INVALID -- the v92 lesson, momentarily un-applied. ROBUST
RE-MEASURE (median-of-means, valid for alpha>1, 72 batches = 3 seeds x 24): physical(1.845) = -0.077(60)
-- CONSISTENT WITH ZERO (1.3 sigma; batch-mean range [-0.62,+1.62], the heavy-tail tell). Re-anchored
zero z(36) = 1.8428(40), a -0.0022 shift from the naive pool 1.8450(30): 0.4 sigma -- THE POOL SURVIVES
the precision fix. v103's "the zero is not where naive placed it" is WITHDRAWN (a heavy-tail fluctuation).
WHAT STANDS: the stable ENGINE is correct & necessary (naive 8-370% wrong per-config, mpmath-certified);
frozen A(36) +0.3754(128) (frozen-side, robust); faithfulness STILL falsified -- robust physical
-0.077(60) vs frozen-side frozen(s_phys) -0.348(11) is 4.4 sigma, so the delta1 x f2 cross-term survives.
The 13/7-vs-24/13 question at beta=36 is unchanged (z=1.843: 0.7 sigma from 24/13, ~4 sigma from 13/7) --
one beta is not the identification, the flow is. STANDING PROTOCOL (amended): every deep-beta mean uses
the stable engine AND median-of-means with inter-batch errors, reporting the batch range as the tell.
LESSON (twice learned): a precision fix does not fix heavy tails -- you need BOTH, and a single IS draw is
never a result under alpha ~ 1. I over-claimed in v103 by trusting one draw; the re-measurement caught and
retracted it in public. 08_2d_interacting/deep_pool.py (PASS, robust estimator), DEEP_POOL_RESULT.md;
stable_cdet.py v104 supersession note. Frozen engine untouched (194/194).

### #115 -- The robust deep-beta flow: the certified pool RISES and fits NO menu line; the assembled root flow is required (v105)

The full robust pool re-scan on the certified stable engine (median-of-means, the v104 protocol):
z(36)=1.8428(40), z(44)=1.8536(121), z(52)=1.8642(61), each the mu* where stripped <C>(mu) crosses zero
from a 2-3 point mu-scan of robust MoM points. THE FLOW RISES monotonically (1.843->1.854->1.864), slope
~0.0013/unit vs the naive pool's nearly-flat ~0.0005/unit; by beta=52 it has PASSED 13/7=1.8571. Single
menu-law fits z=mu*+lnr/(q beta): 11/6 chi2 13.4/2, 24/13 9.4/2, 13/7 6.5/2, CONST 8.7/2 -- NONE FIT
(all chi2/dof>3); the best (13/7) fails by overshoot. CONCLUSION: the naive pool's apparent FLATNESS --
which drove four rounds (v93-95) to {13/7, 24/13} -- was an ARTIFACT of corrupted corner configs +
heavy-tail bias (falsely-flat, falsely-low high-beta points). The single-line menu fit is the wrong
model; the certified rise+curvature vindicate the v100 ASSEMBLED ROOT FLOW (z = 2 + ln s*(beta)/beta,
s* the root of A + c1_eff s + c2 s^2 with the delta1 x f2 cross-term in c1_eff). The identification is
REOPENED and is a FLOW, not a constant. REGISTERED PREDICTION: z(64) > 1.87; the asymptote (if any) lies
above 13/7; the decisive test is to assemble the flow from independently-measured certified coefficients
and reproduce these 3 points with NO fitting. HONEST LIMITS: 3 points, growing errors, an ill-conditioned
high-beta static (vanishing slope + heavy tail) -- the rise is ~2-3 sigma over the range; solid claim =
the naive flatness does not survive certification, so the menu-line ID it supported is withdrawn. LESSON:
a conclusion is only as trustworthy as the noisiest data underneath it -- four rounds of menu-narrowing
rested on high-beta points that were both float64-corrupted AND heavy-tail-biased; fixing both reopened
the question. 08_2d_interacting/deep_pool.py (PASS, POOL_STABLE + flow_verdict), ROBUST_FLOW_RESULT.md.
Frozen engine untouched (194/194).

### #116 -- Do the uploaded FW tools help? The gravity-loop resummation, adapted as the loop-format resolution for the deep-beta tail (v106)

Paul's tests_and_scripts.zip = the Watford FW toolkit (gravity_loop_verification.py, geometric_SUSY.py,
the fwverify C suite). Assessment vs the CDet deep-beta program. WHAT TRANSFERS: the gravity-loop result
-- a linear-recurrent sequence has a RATIONAL generating function, tail resums in closed form, asymptote
= dominant root (there P^4). It transfers to the deep-beta SERIES because A(beta), <C>(beta) are finite
SUMS OF EXPONENTIALS over the spectrum (sum_k a_k exp(-beta xi_k), xi_k = level_k - mu) -> on a uniform
grid exactly linear-recurrent (Prony), dominant root = asymptotic rate. This is precisely the v105
bottleneck (the deep static is ill-conditioned at high beta, so z(inf) can't be brute-measured -- but it
CAN be read off a recurrence fit at moderate beta). THE ENABLING ADAPTATION: free-rate Prony is
noise-sensitive (the framework's b_n were EXACT INTEGERS; our points carry heavy-tail noise -> spurious
roots), but the L=6 levels are EXACT INTEGERS {0,1,2,3} -> the decay RATES xi_k are KNOWN a priori, so
fitting only AMPLITUDES is a well-posed LINEAR problem (verified chi2 0.75/2 on clean stable A(beta) via
deep_beta_resummation.py, with A measured stable+MoM at beta=24/32/40/48 = 1.328(217)/0.357(125)/
0.119(28)/0.051(23)). THE TARGET: z(inf) = 2 - (rho_A - rho_c1), the DIFFERENCE of the dominant rates of
A and c1 (A at fixed mu decays at the trivial level-2 rate 0.155; the non-trivial static needs c1 too) --
so the tool resolves the asymptote ONCE A(beta) AND c1(beta) are measured clean; the closure is now
well-motivated and the tool is in hand. BOUNDARY (honest): it does NOT touch the MC heavy tail
(alpha ~ 1.06 -- statistical, not a recurrent series; stays median-of-means); fwverify's two-route +
MPFR-30-digit pattern just CONFIRMS the v103 mpmath certifier (methodology, no new capability);
geometric_SUSY is FW physics, unrelated. VERDICT: yes, partially and precisely -- the right framework for
the deep-beta series asymptote, made usable by the exact-integer spectrum; it does not help the MC tail or
move the wall. LESSON: a tool from a neighbouring framework transferred because of a STRUCTURAL match
(both are exponential/recurrent series), but needed adaptation to our noise (known-rate amplitude fit) --
borrow the structure, not the recipe. 08_2d_interacting/deep_beta_resummation.py (PASS, reusable),
LOOP_FORMAT_RESULT.md. Frozen engine untouched (194/194).

### #117 -- The assembled root flow: z(inf) from the rate difference; the lower menu falls, the high end returns (v107)

The closure v105 left open, via the v106 loop-format tool: reach the asymptote from the RATE DIFFERENCE of
two well-conditioned moderate-beta series, not by ill-conditioned high-beta measurement. Measured on the
stable engine + MoM on a uniform grid: A(beta) = 1.328(217)/0.357(125)/0.119(28)/0.051(23) (fast decay)
and c1(beta) = -319.8(69.9)/-193.8(49.5)/-195.4(20.7)/-172.2(16.0) (slow decay) at beta=24/32/40/48. The
leading static s* = A/|c1| gives z(beta)=2+ln(A/|c1|)/beta and z(inf)=2-(rho_A-rho_c1). With MC error
propagation: rho_A = 0.1406(158), rho_c1 = 0.0225(95) (A decays ~6x faster), so Z(INF)_LEADING =
1.8818(184). This sits ABOVE the lower menu the naive program converged to: 24/13=1.8462 (1.9s,
disfavoured), 13/7=1.8571 (1.3s, disfavoured); consistent with the HIGH end 15/8=1.8750 (0.4s) and
17/9=1.8889 (0.4s). 15/8 was declared empirically DEAD in v94/v95 (4.6s) on NAIVE data -- the
certified+robust+resummed analysis RESURRECTS it. INTERNAL CONSISTENCY: the leading-order finite-beta
flow (1.772->1.831) sits ~0.03 below the robust pool (1.843->1.864) -- exactly the v100 delta1 x f2
cross-term, which lifts the root toward physical; so the measured-full-static route and the assembled
leading+cross route AGREE on the shape, both rising to ~1.88. HONEST LIMITS: leading order (omits c2
curvature and the cross-term's effect on the asymptotic rate); 4 points/series, 10-40% rate errors;
c1(40) slightly high. ROBUST: rho_A >> rho_c1, so z(inf) is well above 2-rho_A, and the lower menu is
disfavoured at 1.3-1.9s from TWO independent methods (robust-pool extrapolation + rate difference).
WHAT IT CLOSES: v105's reopened rising flow now has a quantified asymptote ~1.88; the four-round naive
convergence to {13/7, 24/13} is overturned; the high end returns. None of it moves the wall (R, 2^n
unchanged). LESSON: a borrowed tool (the gravity-loop rate-difference asymptote) reached a number the
direct measurement could not -- the asymptote lives in the rates, which are well-conditioned at moderate
beta, not in the static, which is ill-conditioned at high beta. 08_2d_interacting/deep_beta_resummation.py
(PASS, assembled_z_inf + A_STABLE/C1_STABLE), ASSEMBLED_FLOW_RESULT.md. Frozen engine untouched (194/194).

### #118 -- Consolidate + side-by-side both C layers: dual insights, one root cause, one cure (v108)

Both C layers brought current with v104-v107 and compared across three axes. SURROGATE: its menu carriers
still said "open {13/7, 24/13}, PENDING RE-FIT" -- v104-107 resolved that (pool survives & RISES, no menu
line fits, assembled z(inf)=1.8818(184), lower menu falls, 15/8 returns); added live carriers
surr_l6_z_inf()=1.8818 and surr_l6_pool(beta) (robust pool 36/44/52), old menu lines labelled superseded.
BRUTE C: re-stamped v108 with the PRECISION CAVEAT -- its propagator is the frozen engine's naive G0_atom
(-(1-n_F)exp(-xi tau)), correct & ED-validated at benign beta but carrying the v103 deep-beta bug latent
(a far occupied level's (1-n_F) -> 1.0-1.0=0, image vanishes; demonstrated in C: naive G0_atom=-0.000000
vs stable -0.049787=analytic at beta=36,xi=-3,tau=35). SIDE-BY-SIDE: (value) surrogate z_inf/pool AGREE
with stable truth by construction; the SUPERSEDED 13/7 / 11/6 lines DISAGREE with the resolved asymptote
at 1.8 / 2.2 sigma (retired). (precision) naive C wrong, stable C correct at deep beta. (speed) stable C
G0_atom_stable is only 1.29x the naive call (22.4 vs 17.3 ns) while deep-beta-correct; the surrogate carrier
is 4.4 ns (lookup); the Python stable g0 is 21375 ns (216-level sum) -- so a stable C engine is ~1000x the
Python stable engine. DUAL INSIGHTS: SURROGATE can be improved by (1) guarding the misleading superseded
menu carriers, (2) linking cdet_stable to COMPUTE deep-beta values not just look them up, (3) a
regime-conditional ln-magnitude model for the still-uncaptured deep-bulk 64x tail. BRUTE C can be improved
by porting the log-domain G0_atom_stable (built+certified here, cdet_stable.c) -> a deep-beta-correct C
engine at 1.29x cost and ~1000x the Python stable workhorse, which is what would tighten v107's z(inf)=
1.88(2) (10-40% rate errors from only 4 points -> a 20-point grid becomes cheap). COMBINATION (one root
cause, one cure): the four engines fill a 2x2 of (fast/slow) x (deep-correct/deep-wrong); stable-C is the
missing fast+correct quadrant, now filled. BOTH layers inherit the SAME flaw (the naive propagator -- the
surrogate indirectly via carriers fit to naive-corrupted pool data, the brute directly) and take the SAME
cure (the log-domain propagator -- re-ground the surrogate on certified z(inf), port G0_atom_stable to C).
Ideal stack now visible: surrogate triage -> stable-C production -> mpmath certification. None of it moves
the wall. LESSON: consolidating two layers TOGETHER exposed a shared root cause neither showed alone.
08_2d_interacting/cdet_stable.{c,h} + cdet_stable_test.c (PASS, benign-match + deep-beta-correct),
csurrogate.* (z_inf/pool carriers + v104-107 params), brute drivers v108-stamped, DUAL_CONSOLIDATION_
RESULT.md. Frozen engine untouched (194/194).

### #119 -- The stable C deep-beta engine: unbiased A(beta) to beta=64 corrects a hidden v107 bias; 15/8 falls; the asymptote rises but is not pinned (v109)

The v108 queue item delivered: cdet_stable_engine.c -- the frozen connected determinant with the log-domain
propagator, reading the exact L=6 spectrum (spectrum_l6.bin) so it matches the Python stable engine.
VALIDATED to machine precision vs StableFrozen.C_V (worst significant rel dev 0.0 above the 1e-13 floor)
and vs high-statistics Python: A(40)=0.262(9) [C] vs 0.267(4) [Python] (0.5 sigma). SPEED: a 6-point grid
to beta=64 (Python could not reach) in 150 s vs ~15-20 min biased. THE EXPOSURE: v107's A(beta) was
HEAVY-TAIL-BIASED LOW at high beta -- banked A(40)=0.119(28) is 2.3x below the true 0.267 -- so v107's
rho_A was too large and z(inf)=1.882(18) was an UNDERESTIMATE. The corrected clean flow z=2+ln(A/|c1|)/beta:
1.780/1.815/1.835/1.854/1.868/1.878 at beta=24..64, RISES and is STILL CLIMBING at beta=64 (no plateau).
DECISION: 15/8=1.875 is now DISFAVORED (the flow passes THROUGH it at beta~62, not asymptoting to it);
the asymptote is >=1.88, pointing to 17/9=1.889 or higher. HONEST LIMIT: the asymptote is NOT pinned --
1/beta fit gives 1.933, 1/beta^2 gives 1.961, they disagree and both fit poorly (chi2 120/4, 20/3); the
flow still curves at beta=64, the single-rational model may be wrong (multi-exponential object). INTERNAL
CONSISTENCY holds: the leading flow sits below the robust pool by a SHRINKING cross-term lift
(+0.013/+0.005/+0.003 at beta=36/44/52) = the v100 delta1 x f2 correction vanishing as beta grows --
confirming the C flow is the same object measured cleanly. NET: the C engine is the deliverable (validated,
~1000x the Python stable engine) and it CORRECTS a hidden bias -- the asymptote is higher than v107 thought,
15/8 is out, but pinning it needs beta>64 (cheap in C now) or a multi-exponential channel model. None of it
moves the wall. LESSON: a fast correct engine doesn't just speed things up -- it exposes biases the slow
engine hid (v107's high-beta A was undersampled, and the slow Python couldn't run enough statistics to
notice). 08_2d_interacting/cdet_stable_engine.c (PASS, validated), spectrum_l6.bin, _dump.py, _refs.txt,
_grid_v109.txt, STABLE_C_ENGINE_RESULT.md; csurrogate_params.h v109 caveat. Frozen engine untouched (194/194).

### #120 -- The plateau run: NO plateau; the flow crosses every menu rational and keeps rising; the menu identification falls (v110)

The v109 queue item delivered: pushed the C grid to beta=120 for the plateau. FIRST a precision finding:
the float64 stable engine degrades on extreme-corner configs -- but that wall is on the PHYSICAL engine
(StableCDet vs mpmath: 2.6% at beta=56, 8.7% at 64, 15% at 80), a DETERMINANT-level cancellation beneath
the v103 propagator-level one. The FROZEN engine (which measures A) is well-conditioned: freezing the deep
occupied levels removes the ill-conditioned occupied-far physical amplitudes, so float64-vs-long-double
agree to ~1e-6 at beta=64, ~1e-4 at beta=80 -- THE v109 GRID IS CLEAN, NO RETRACTION. float64 NaNs at
beta>=96; long double (x87 80-bit, +3.3 digits) reaches beta=120 (validated: matches Python at 36, float64
to 80). The freeze is also a numerical regulator -- that is what makes the plateau reachable. THE RESULT:
the full flow z=2+ln(A/|c1|)/beta = 1.780/1.815/1.835/1.854/1.868/1.878/1.895/1.909/1.920 at
beta=24..120 RISES MONOTONICALLY, still climbing at beta=120 (+0.011 from 100), NO PLATEAU. It CROSSES the
menu rationals (15/8 at beta~61, 17/9 at ~74, 19/10 at ~87) rather than asymptoting to any. rho_A is still
DECREASING at beta=120 (0.097->0.027), not converged -- the slowest channel hasn't dominated, the asymptote
is at beta>>120. The rate difference (2-z)beta=ln(|c1|/A) has slope rho_A-rho_c1~0.045 and shrinking ->
z(inf) in [1.95,2.0], PLAUSIBLY the trivial z=2 (zero at the probe level 2) with slow 1/beta corrections
(not proven). RETRACTION: the menu-rational identification (v93-v107: 11/6, 13/7, 24/13, 15/8, 17/9) read
FINITE-BETA values as the asymptote; the clean deep flow shows NO low-q rational asymptote in [1.83,1.90]
-- those were finite-beta crossings of a monotone rise toward a high value (>=1.92, likely ->2). The
question "which menu rational is z(inf)?" was the wrong question. ATLAS_L6_Z_INF=1.8818 (v107) is a
finite-beta value, NOT z(inf). Pinning z(inf) is not possible by brute beta-extension (multi-exponential
convergence too slow even at 120); needs the known-rate resummation with A's channels resolved, or it is
simply 2. None of it moves the wall (R, 2^n unchanged) -- it relocates WHERE the sign structure sits: at
the probe level in the deep-beta limit, not at an exotic rational. cdet_stable_engine.c now carries the
long-double mode (-DUSE_LD) + valb check + the v110 precision note; cdet_stable_engine_plateau_v110.txt,
PLATEAU_RESULT.md; csurrogate_params.h v110 caveat. Frozen engine untouched (194/194).

### #121 -- z(inf) RESOLVED: the asymptote is the bare probe level z=2; the menu was a ln(beta)/beta approach (v111)

The v110 queue item settled: is z(inf)=2 or a sub-2 rational? Model comparison on (2-z)*beta = ln(|c1|/A)
over the clean 9-point flow (beta=24-120, v109 float64 + v110 long double). The EXPONENTIAL-GAP picture
(ln(|c1|/A)=rho*beta+q -> z_inf=2-rho, a menu rational) is REJECTED at chi2 622/7. The POWER-LAW picture
(ln(|c1|/A)=p*ln beta+q -> z_inf=2) fits (chi2 37/7, residuals 0.003 in z); the general fit gives
z_inf=1.991(2). STRUCTURAL REASON: the dominant-rate fit ln X = -rho*beta + p*ln beta + const gives
A ~ beta^-2.8 (rho_A=0.003(2)~0) and |c1| ~ beta^-0.54 (rho_c1=-0.004~0) -- BOTH decay as POWER LAWS, not
exponentials, sharing the same (vanishing) rate because they are tau-averages of the SAME connected
determinant with the SAME propagators (c1 is the s-derivative, which changes the power prefactor not the
rate). So |c1|/A ~ beta^2.3, ln(|c1|/A) ~ 2.3 ln beta, and z(beta) = 2 - 2.3*ln(beta)/beta -> 2. THE
ANSWER: z(inf) = 2, the bare probe level (level 2), to within ~0.01 (the 1.991-vs-2 gap is leading-order
s*=A/|c1| truncation + unconverged subleading rates). THE MENU IS CLOSED: the rationals 11/6, 13/7, 24/13,
15/8, 17/9 (all in [1.83,1.90]) are finite-beta CROSSINGS of a ln(beta)/beta approach to z=2, NOT
asymptotes -- the identification program (v93-v107) fit the slow transient. The decisive facts: the
exponential gap is rejected (chi2 622) and both A and |c1| are power-law. None of it moves the wall (R,
2^n unchanged) -- it is the FINAL WORD on WHERE the sign structure sits: at the probe level z=2, with a
calculable ln(beta)/beta finite-beta law. deep_beta_asymptote.py (model_comparison, power_laws, z_flow;
self-test PASS), ZINF_RESULT.md; csurrogate_params.h ATLAS_L6_Z_INF_RESOLVED=2.0. Frozen engine untouched
(194/194).

### #122 -- z(inf)=2 DERIVED: A corner-confined (~1/beta^3), c1 level-2 de-confined (~beta^-0.3); the ratio forces z->2 (v112)

The v111 queue item delivered: derive the power laws behind z(inf)=2 from structure. KEY: A and c1 are
tau-AVERAGES, A=<C_V>=(1/beta^3) integral dtau^3 C_V, so the beta-power lives in the un-normalized integral
J(beta)=beta^3*X. MEASURED on the clean grid: J_A=beta^3*A -> CONST (beta^-0.02; deep-half beta^-0.12) ->
A ~ 1/beta^3; J_c1=beta^3*|c1| ~ beta^+2.7 (GROWS) -> |c1| ~ beta^-0.3. MECHANISM: at s=0 level 2 is empty
and the connected determinant's antiperiodic images align only in the tau->beta corner -- a BETA-INDEPENDENT
O(10)-wide region -- so integral dtau^3 C_V CONVERGES (three 1/beta x an O(1) corner integral => A~1/beta^3,
CORNER-CONFINED). c1=dC_V/ds activates LEVEL 2, whose gap xi_2=2-mu=0.155 is the SMALLEST -> longest-range
propagator exp(-0.155|dtau|) (range ~6.5) connecting tau's across the WHOLE box -> the integral GROWS as
beta^2.7 (DE-CONFINED). Direct windowed check at beta=64: J_c1(W)=integral over [beta-W,beta]^3 grows as
W^2.6 (no saturation) -- box-filling support confirmed. CONCLUSION: |c1|/A=J_c1/J_A ~ beta^(q_c1-q_A)=
beta^2.7, a POSITIVE power, so z(beta)=2-2.7*ln(beta)/beta -> 2. The exponent difference 2.7 (matching
v111's p~2.3-2.6) IS the story; z(inf)=2 is FORCED by q_c1>q_A, not fitted -- a structural consequence of
the smallest-gap channel (level 2 = the probe level itself) decaying slower than the corner-confined
background. THE SIGN-STRUCTURE ZERO SITS AT THE PROBE LEVEL BECAUSE THE PROBE LEVEL IS THE SMALLEST GAP.
None of it moves the wall (R, 2^n unchanged). deep_beta_powerlaw_derivation.py (integrals, powers; self-test
PASS), POWERLAW_DERIVATION_RESULT.md; csurrogate_params.h v112 note. Frozen engine untouched (194/194).

### #123 -- The 'single de-confined mode' sharpening tested: the level-2 channel is real, but it SATURATES (not an exp mode) (v113)

An external suggestion (shared by Paul) sharpened v112: prove c1(beta)=sum_n a_n exp(-xi_n beta) with
xi_2<xi_n for all n>2, so the phase fluctuations are ENTIRELY carried by the n=2/level-2 sector -> 'sign
problem = one de-confined mode with gap (2-mu)'. Tested against the data, it splits. SURVIVES (=v112):
xi_2<xi_n is TRUE -- the gaps xi_n=level_n-mu put level 2 (the probe) closest to mu=1.845 (xi_2=2-mu=0.155),
smaller than every level above mu (level 3:1.155, 4:2.155,...); the phase response c1=dC_V/ds is carried by
this single smallest-gap channel; the compression of the sign structure to ONE spectral channel is real.
FALSIFIED (the literal form): c1 is NOT sum_n a_n exp(-xi_n beta). If it were, the n=2 term would make |c1|
decay at rate xi_2=0.155 -> factor exp(0.155*96)~2.9e6 over beta=24..120; MEASURED |c1| drops 1.66x (eff
rate 0.0046, 34x too small) -> overpredicts by ~1e6. CORRECTION: c1 is a tau-AVERAGE; the level-2
exponential lives in the tau-PROPAGATOR exp(-xi_2|dtau|) and SATURATES under integration (int_0^beta
exp(-xi_2 tau) dtau -> 1/xi_2=6.45, converged by beta~48), contributing a beta^0 (rate-0) factor NOT an
exp(-xi_2 beta) mode -- which is exactly why integrated c1 is a POWER LAW (v112) and z(beta)->2 as a
ln(beta)/beta approach, not pinned by an exponential gap. The gap (2-mu) enters correctly as the
de-confinement RANGE 1/(2-mu)=6.5 in tau and the LIMIT z(inf)=2 (probe level at energy 2), but is NOT a
beta-rate. NET: the kernel ('sign problem = one de-confined channel, the level closest to mu') is right and
is the real compression; 'with gap (2-mu)' is right for range+limit, wrong as a rate; the object is a
SATURATING de-confined channel, not an exponential mode -- and that distinction is why z is reached as a
slow power-law approach (the whole v93-v107 menu detour). None of it moves the wall (R, 2^n unchanged).
spectral_channel_test.py (gaps, test_exponential_form, saturation; self-test PASS), SPECTRAL_CHANNEL_
RESULT.md; csurrogate_params.h v113 note. Frozen engine untouched (194/194).

### #124 -- z(inf)=2 is LOCKED to level 2: the probe must be the Fermi surface; any other is Fermi-forbidden (v114)

Does the v112-v113 mechanism generalize? z(inf)=2 because level 2 is BOTH the probe (s-direction) AND the
smallest gap -- confounded. Separated by generalizing the freeze to an arbitrary PROBE level
(cdet_stable_engine.c set_freeze + grid arg 10) and moving the probe from 2 to 3. RESULT: the background A
is IDENTICAL for probe=2 and probe=3 (at s=0 both leave levels 2,3 empty -- only the s-DIRECTION differs),
but c1=dC_V/ds is the discriminator: probe=2 (Fermi surface) gives finite decaying c1 (237->156 over
beta=24-72), z=2+ln(A/|c1|)/beta -> 2, WELL-DEFINED; probe=3 makes c1 DIVERGE exponentially at rate +2.72
per beta (3.8e19 -> 1.1e76), ill-defined. WHY: probe=3 forces level 2 (lowest empty, gap 0.155) to 0 while
scanning level 3 (gap 1.155) -- a POPULATION INVERSION (level 3 occupied, level 2 empty) forbidden by Fermi
statistics; the connected determinant, expanded around the physical vacuum, is unstable to this
perturbation, so the s-response diverges with a free-energy cost growing with beta. CONCLUSION: z(inf)=2 is
LOCKED to level 2 not by coincidence but because level 2 is the unique physically-scannable probe -- the
lowest empty level, the Fermi surface. 'smallest gap' = 'Fermi surface' = 'the only valid probe' are the
SAME statement. This SHARPENS v113: level 2's smallest-gap property is not merely why its channel
de-confines most, it is why it is the only consistent probe at all -- the sign structure compresses to one
channel because there is only one channel it CAN compress to. The mechanism does NOT generalize to arbitrary
probes, and that non-generalization is the content: the deep-beta sign structure is pinned to the Fermi
surface. None of it moves the wall. probe_generalization_test.py (divergence_rate; self-test PASS),
PROBE_LOCK_RESULT.md; cdet_stable_engine.c (generalized probe), csurrogate_params.h v114 note. Frozen engine
untouched (194/194).

### #125 -- Full dual consolidation at the frontier: both C layers current with z(inf)=2; the duality is a chain (v115)

Both C layers consolidated with all proven advances through v114, rebuilt, tested, compared. STALE->CURRENT:
the surrogate's live carrier surr_l6_z_inf() STILL returned 1.8818 (the v107 underestimate) despite z(inf)=2
being resolved (v111)/derived (v112)/Fermi-locked (v114) -- 13 caveat layers narrated the story while the
callable returned the wrong value. Now surr_l6_z_inf()=2.0, with surr_l6_z_finite(beta) carrying the
ln(beta)/beta law (z=2-2.6*ln(beta)/beta) and surr_l6_z_inf_legacy() preserving 1.8818 for the record; menu
carriers explicitly superseded. Brute-force C (cdet2d/cdet_small/cdet_vs_naive) re-stamped v115; its precision
caveat now points at the BUILT deep-beta layer cdet_stable_engine.c and records the resolved physics. REBUILD
TEST all green (surrogate gate, stable C float64+long double validate, stable propagator benign+deep, brute
drivers build+benign, 4 analysis modules, frozen 194/194, constants bit-identical). SIDE-BY-SIDE (3 layers):
z(inf) surrogate 2.0 (carries) / stable-C 2.0 (derives, flow->2) / brute-C -- (too shallow); benign beta all
agree (brute ED-validated, stable matches to machine precision); deep beta only stable-C correct (brute naive
G0=-0.0 vs stable -0.0498); speed surrogate 7.4ns / brute-C naive 14.2ns / stable-C 17.4ns (1.22x). LESSONS
(the duality is a CHAIN, each layer covers a blind spot): (1) the surrogate cannot compute, only carry -- it
was carrying the WRONG physics (1.8818) and would forever; the engine re-grounds it. (2) The brute-C cannot go
deep but IS the anchor -- the stable engine is trusted because it matches the brute-C's ED-validated C_V at
benign beta. (3) The stable engine cannot self-certify -- it is the bridge inheriting the brute-C's exactness
(log-domain propagator matches at benign) and extending it where the naive propagator fails. (4) DEEPEST: the
cross-validation between the three caught EVERY error -- the heavy-tail bias (v109), the precision walls (v110),
the z(inf)=2 resolution (v111-v114) were each found at a SEAM between methods, never inside one. Ideal stack
now complete+current: brute-C (exact anchor) -> stable-C (fast deep production) -> surrogate (fast carrier),
mpmath spot certifier. None of it moves the wall. csurrogate.* (z_inf->2.0 + z_finite + legacy), brute drivers
v115, DUAL_CONSOLIDATION_v115_RESULT.md. Frozen engine untouched (194/194).

### #126 -- The site-choice generalization: z(inf)=2 is geometry-independent; the SIGN is the geometric degree of freedom (v116)

The one generalization the v114 Fermi-lock permits: vary the lattice SITES at fixed Fermi-surface probe.
Engine generalized (cdet_stable_engine.c grid takes optional sites, args 11-13). PREDICTION REGISTERED before
measuring: z(inf)=2 for all triples (asymptote = the freeze's Fermi-surface level, not geometry), rate varies;
falsifier = any clean z(inf)!=2. RESULT over 5 geometries (beta=24,48,72): z=2+ln(|A|/|c1|)/beta rises
monotonically toward 2 in EVERY triple -- (1,2,4) 1.785->1.887, (1,2,3) 1.748->1.874, (1,5,25) 1.764->1.882,
(10,80,150) 1.774->1.878, (1,7,49) 1.881->1.911. PREDICTION CONFIRMED: z(inf)=2 does NOT depend on the sites;
the approach rate varies (|c1| ranges 16-807 -> different ln(beta)/beta prefactors). NEW STRUCTURE beyond the
prediction: the SIGN of A and c1 varies by geometry -- opposite signs give a physical leading root s*=-A/c1>0
((1,2,4),(1,2,3),(1,5,25)), same signs give s*<0 no physical small root ((10,80,150),(1,7,49)). So the SCALE
(z=2) is universal -- independent of probe (v114) AND of sites (v116), DOUBLY universal -- while the SIGN
structure is the GEOMETRIC degree of freedom. This is the anatomy of the sign problem made explicit: the
deep-beta scale is pinned to the Fermi surface no matter what; the phase (whether the determinant background
crosses zero) is geometric, exactly what makes the zero appear or not. Sign and scale separate cleanly. None
of it moves the wall. site_generalization_test.py (z_flow, physical_root; self-test PASS),
SITE_GENERALIZATION_RESULT.md; cdet_stable_engine.c (optional sites), csurrogate_params.h v116 note. Frozen
engine untouched (194/194).

### #127 -- The sign side: A's sign is a Friedel oscillation; the Fermi surface governs scale AND sign (v117)

v116 left the sign as the geometric degree of freedom; v117 asks if it is PREDICTABLE. The propagator
g0(i,j,tau)=sum_k U[i,k]U[j,k] occ_k(tau) carries U[i,k]U[j,k]~cos(k.(r_i-r_j)) on the cube lattice, so the
sign should be a Friedel oscillation (cf. v68). PREDICTION REGISTERED before measuring: sign(A) oscillates
with separation at a Fermi wavelength (a period-2 sub-guess was also registered). RESULT: scanning one vertex
site along x (others fixed, beta=24), sign(A)=(-,-,-,+,+) for x=1..5 -- a REPRODUCIBLE zero-crossing (signs
agree across seeds 31 & 777; |A| minimal at the flip). A's sign is geometric and OSCILLATORY, Friedel-class
CONFIRMED. The wavelength is LONG not period-2: mu=1.845 sits near the 1D band top (max|eps|=2) so the Fermi
surface is SMALL; from -2cos(theta_F)=mu, 2k_F aliases to 0.793 rad -> wavelength ~7.93 sites (half ~4.0) ->
~1 flip per 4 sites, matching the 1 flip in the 5-site scan. The period-2 sub-guess was WRONG (wrong
momentum). A is a connected determinant of several propagators so the net sign is a SUPERPOSITION of cos(k.dr)
terms, not a single clean cosine -- but the oscillation SCALE matches 2k_F. UNIFYING: the Fermi surface
governs BOTH -- the deep-beta SCALE z(inf)=2 via its energy GAP xi_2=2-mu=0.155 (v112-v116), and the SIGN via
its MOMENTUM 2k_F -> Friedel wavelength ~8 sites (v117). v116 found sign and scale SEPARATE (independent
axes); v117 finds they share ONE origin (the Fermi surface) through two channels: the gap (scale) and the
momentum (sign). This also localizes v68's Friedel-class sign coherence: it is the background determinant A
whose sign oscillates at 2k_F. None of it moves the wall, but it is the first time the sign and the scale of
this object are traced to the SAME object by two distinct mechanisms. site_sign_friedel.py (friedel_wavelength;
self-test PASS), FRIEDEL_SIGN_RESULT.md; csurrogate_params.h v117 note. Frozen engine untouched (194/194).
[CORRECTED by #128 (v118): the continuous-2k_F wavelength match was COINCIDENTAL -- moving mu shows the sign
is mu-invariant, set by the DISCRETE frozen Fermi boundary, not 2k_F(mu). The 'Fermi surface governs both'
claim survives and is strengthened (one discrete object, rigid in mu); the specific 2k_F(mu) identification
is retracted.]

### #128 -- The gap-momentum unification test (move mu): prediction falsified; the frozen Fermi surface is discrete and rigid (v118)

v117 said the Fermi surface governs scale (z=2 via gap xi_2=2-mu) AND sign (Friedel via 2k_F). The decisive
test is to MOVE mu (in a thermal system that changes the gap and k_F together). PREDICTION REGISTERED before
measuring: sign-flip spacing tracks lambda(mu)=2pi/(2pi-2arccos(-mu/2)) (3.64 sites at mu=1.3 vs 9.89 at
mu=1.9, ~2.7x); z(inf)=2 with a gap-shifted approach. RESULT -- prediction FALSIFIED and the falsification is
the finding: the sign pattern is mu-INVARIANT (x-scan sign(A)=(-,-,-,+,+) at mu=1.3,1.6,1.9, reproducible
across seeds, A values barely move), and the z-flow is mu-INVARIANT too (z=1.786/1.853/1.887 at mu=1.3,
identical to <0.005 at mu=1.845 and 1.9; c1 essentially mu-independent). ROOT CAUSE: the engine is FROZEN --
occupations are discrete (0/1), NOT thermal n_F(mu), so mu does not enter the propagator. The Fermi surface is
the level-1|level-2 BOUNDARY (which levels are filled), fixed for all mu in (1,2); mu enters only via the
positive strip exp(0.5(mu-2)) (cancels in z and sign) plus a weak shift in A. CORRECTION TO v117: the
wavelength match lambda(1.845)~7.93 sites ~ 1 flip/5-scan was COINCIDENTAL; the Friedel momentum is the
DISCRETE frozen-boundary momentum, not continuous 2k_F(mu). v117's core (sign oscillates with geometry,
Friedel-class) survives; the '2k_F(mu)' identification is RETRACTED. STRENGTHENED UNIFICATION: the frozen Fermi
surface is ONE discrete (topological) object -- the filled-level set -- governing BOTH the scale (z=2, lowest
empty level) and the sign (Friedel pattern from the occupied/empty modes), locked together and RIGID under mu
in (1,2). mu matters only when it CROSSES a level (changing the probe -> v114 divergence). Tighter than v117:
not two channels of a mu-tunable surface, but one discrete object fixing both at once. mu_unification_test.py
(lambda_continuous; self-test PASS), MU_UNIFICATION_RESULT.md; cdet_stable_engine.c (optional mu, arg 14),
csurrogate_params.h v118 note. Frozen engine untouched (194/194).

### #129 -- The full 2D Friedel sign-map, resolved at the elementary level (v119)

v117 saw A's sign oscillate along a line; v118 showed it set by the discrete frozen Fermi boundary, rigid in
mu. v119 maps the sign over a full 2D plane and resolves it at the ELEMENTARY level. PREDICTION REGISTERED:
the 2D map shows Friedel domains with nodal lines, cube symmetry, and mu-rigidity. RESULT: mapping sign(A)
over the (x,y,0) plane gives a structured-but-messy pattern (many near-node cells, fixed sites S0,S1 break
symmetry) -- expected, since A is a multi-propagator determinant whose sign-vs-S2 is a SUPERPOSITION. The
ELEMENTARY object is the frozen density matrix rho(0,r)=sum_{occ k}U[0,k]U[r,k]=(1/N)sum_{occ k}e^{ik.r} = FT
of the OCCUPIED REGION in k-space; its Friedel oscillation is set by the Fermi surface directly. For rho:
(1) the sign-map is CUBE-SYMMETRIC (x->6-x, y->6-y); (2) SHORT wavelength ~2-3 sites, dominant wavevector
(120,180)deg = the level-1|2 boundary 1D modes (eps=+1 at k=2,4 -> 120/240; eps=+2 at k=3 -> 180) -- the
DISCRETE frozen Fermi surface sets the wavevector; (3) mu-invariance is now ANALYTIC and EXACT: ZERO modes
have eigenvalue strictly in (1,2), so the occupied set {lambda<=1} is identical for every mu in the window ->
rho is exactly the same map for all mu in (1,2) (first-principles proof of v118). RECONCILES v117: the
elementary Friedel wavelength is SHORT (~2-3 sites), not the ~8 sites inferred from A; A's sign is a
determinant superposition of these short oscillations, giving a longer messier envelope -- v117's '~8-site /
2k_F(mu)' was that envelope (and per v118 coincidental), not the elementary scale. v117's core (sign is
geometric, Friedel-class) is unchanged. The sign side closes consistently with the scale side: the discrete
frozen Fermi surface (filled-level set) sets the elementary Friedel wavevector exactly and mu-rigidly, just as
it sets z=2; the determinant assembles the observable sign by superposing the elementary oscillations. None of
it moves the wall. frozen_friedel_map.py (frozen_density_matrix, gap_is_empty; self-test PASS),
FROZEN_FRIEDEL_MAP_RESULT.md; csurrogate_params.h v119 note. Frozen engine untouched (194/194).

### #130 -- Full dual consolidation at the sign frontier: the surrogate gains a sign side; a sharper theorem (v120)

Both C layers consolidated with all advances through v119. Since v115 the entire SIGN side opened (v116-v119)
and the surrogate was SCALE-ONLY -- it carried z(inf)=2 but nothing about the sign (which lived only in Python
rho(0,r) and the C determinant engines). FIXED: the surrogate now carries the sign-side analytic core --
surr_l6_gap_modes(lo,hi) and surr_l6_occupied(mu) over the cube integer multiplicities ATLAS_L6_MULT
{1,6,12,14,27,36,24,36,27,14,12,6,1} (sum 216), plus the dominant Friedel wavevector (120,180)deg -- all
confirmable in C with NO eigendecomposition, matching Python EXACTLY (gap(1,2)=0, occ(1.3)=occ(1.9)=156).
Brute-C re-stamped v120 + sign pointer; stable-engine CLI doc fixed (was missing the sites/mu args). SHARPER
THEOREM the consolidation produced: distilling the sign side forced 'why is mu-rigidity exact' -> because the
cube_hopping(6) spectrum is INTEGER-valued, NO mode lies in any open unit interval (n,n+1), so the freeze is
exactly mu-rigid in ANY unit interval (jumping only when mu crosses an integer). v118/v119 found this for
(1,2); the consolidation generalized it to a one-line eig-free check. REBUILD all green (gate, stable f64+LD,
propagator, brute, 5 analysis modules scale+sign, frozen 194/194, constants). SIDE-BY-SIDE (3 layers x 2 axes):
SCALE z(inf) surrogate 2.0 / stable-C 2.0 / brute-C shallow; SIGN elementary rho = Python(eig), determinant A
= C engines, mu-rigidity = surrogate carrier (no eig, matches Python). Engine-level: occupied set, rho, sign(A)
exactly mu-rigid; z-flow rigid to ~0.005; |A| weak residual mu-dependence (~12% over (1,2)) changing neither
sign nor z=2. LESSONS: (1) the sign side is a CHAIN like the scale side -- elementary rho (Python eig) ->
determinant A sign (C, superposition) -> distilled carriers (surrogate, no eig); before v120 the cheapest level
was empty. (2) Consolidation OUT-PERFORMED experiment: the integer-spectrum theorem is sharper than the mu-scans
or rho-map produced -- forcing a fact into the fast layer clarified the physics. (3) Optimization for the C
engines: a mu-scan within a unit interval is redundant for sign+occupied set (one eval suffices). (4) Still
open: elementary rho is Python-only; a future fix could port it (FT of the occupied region) to C. None of it
moves the wall. csurrogate.* (gap_modes/occupied/MULT + Friedel wavevector, v117 note corrected inline), brute
drivers v120, stable CLI doc, DUAL_CONSOLIDATION_v120_RESULT.md. Frozen engine untouched (194/194).

### #131 -- Porting the elementary Friedel object rho(0,r) to C (v121)

v120 closed with one open fix: the elementary frozen Friedel object rho(0,r) lived only in Python
(frozen_friedel_map.py, numpy eigh). Now it is in C -- cfriedel.c -- self-contained and validated. KEY: no
eigenvectors are needed. The cube factorizes into three rings, so the eigenmodes are plane waves k=(kx,ky,kz)
with eps(k)=-2(cos(2pi kx/6)+cos(2pi ky/6)+cos(2pi kz/6)), and the projector matrix element is basis-
independent: rho(0,r)=sum_{occ k}U[0,k]U[r,k]=(1/N)sum_{eps(k)<=1}cos(k.r). So cfriedel.c computes rho directly
from the analytic plane-wave structure -- no eigenvectors, no spectrum file, no eigendecomposition -- and it is
exact. VALIDATION: 'cfriedel test' self-validates vs embedded Python eigh refs (9 points, worst 4.8e-11); a
full 216-point cross-check vs the Python eigh density matrix gives worst dev 4.81e-11 over the whole lattice;
the C sign-map (cfriedel map 0) is identical to the v119 Python map; occupied count 156 (matches
surr_l6_occupied), exactly mu-rigid (integer spectrum, v120). WHAT IT CLOSES: the sign side now has the same
three-layer C coverage the scale side has -- elementary rho (cfriedel.c, exact, self-contained), determinant A
(stable/brute engines, sign = superposition of rho), distilled rigidity carriers (surrogate gap_modes/
occupied). The v120 'elementary rho is Python-only' is resolved: now C, cross-validated, no linear-algebra
dependency. None of it moves the wall. cfriedel.c (test/r/map/occ modes, gcc -Wall -Werror -std=c11 -pedantic),
FRIEDEL_PORT_RESULT.md; frozen_friedel_map.py + csurrogate_params.h point at it. Frozen engine untouched (194/194).

### #132 -- Scaling the brute force across lattice sizes: universal vs crystallographic laws, the plane-wave path, a hybrid (v122)

Testing the laws (found at L=6) across L separates universal from crystallographic and shows how to scale.
KEY: mu-rigidity (v120) is CRYSTALLOGRAPHIC, not universal -- the freeze is exactly mu-rigid in a unit interval
iff the spectrum is integer iff cos(2pi/L) is rational iff L in {1,2,3,4,6} (the crystallographic restriction).
Verified L=2..12: integer at L=2,3,4,6 (min eigen-gap 4,3,2,1); irrational at L=5,7,8,12 (min gap 0.53,0.15,
0.24,0.20 -> only approximately rigid). UNIVERSAL laws (any L): the SCALE law z(inf)=lowest-empty-level
eigenvalue (the Fermi-surface probe) -- L6 mu in (1,2)->2, mu in (2,3)->3, L4 mu in (0,2)->2; and the elementary
FRIEDEL rho(0,r) oscillation (rho(0,0)=occupied fraction, wavevector = occupied-region boundary). SCALING
ENABLER: the connected determinant is over a FIXED vertex set; the lattice enters ONLY via propagators
g0=(1/N)sum_k cos(k.dr) G0_atom(eps_k,beta,occ_k,tau), each an O(N) plane-wave sum -- NO eigenvectors, NO stored
spectrum -> brute force is O(N x MC), LINEAR in N=L^3, L-agnostic. cfriedel_L.c generalizes the elementary
object to any L on this form (validated 4.8e-11 vs Python eigh at L=6), runs the structural layer at L=20
(N=8000) in <1s with zero stored data. HOW BIG: structural laws O(N), file-free -> L=20+ trivially (the 375KB
spectrum_l6.bin is eliminated by the plane-wave form); the determinant O(N x MC) -> L~12-16 comfortably (linear,
vertices fixed); exact mu-rigidity tests limited to crystallographic L in {2,3,4,6}; the practical ceiling is
output/analysis context, not the lattice. HYBRID (third engine, preserves the dual): phase 1 carries the laws
(surrogate-fast, O(N), any L, instant: integer-spectrum verdict, probe level -> z(inf) prediction, Friedel
wavevector); phase 2 runs the optimized plane-wave determinant (O(N x MC)) for A,c1, validated against phase 1.
The handoff is exactly where the surrogate stops being exact -- it carries the discrete structure for free
(exactly on crystallographic L), the brute fills in the coefficient. None of it moves the wall but makes the
wall's lattice-size dependence explicit and cheap. multi_lattice_laws.py (integer_spectrum, lowest_empty_level;
self-test PASS) + cfriedel_L.c (occL/scan/map[L][mu]/r[L][mu]), MULTI_LATTICE_RESULT.md; csurrogate_params.h
v122 note. Frozen engine untouched (194/194).

### #133 -- Phase 2 of the hybrid: the L-generalized plane-wave determinant engine; multi-lattice scale law proof (v123)

The hybrid's phase 2 is BUILT: cdet_planewave_engine.c is the stable engine with the eigenvector propagator
replaced by the plane-wave form g0(i,j,tau)=(1/N)sum_k cos(2pi k.dr/L) val(eps(k),occ(k),tau), eps(k)=
-2(cos+cos+cos) on the fly -- NO eigenvectors, NO spectrum file, arbitrary L. The freeze is generalized to
track mu into any gap (occupied<PROBE, probe=PROBE->s, PROBE+1 empty, >=PROBE+2 physical); Rossi recursion /
cluster IS / MoM / log-domain G0_atom reused unchanged. VALIDATION: at L=6 PROBE=2 it reproduces the stable
engine EXACTLY (A=1.341555, c1=-234.4268 to the last digit; val worst rel dev 0.00e+00) -- the plane-wave g0
is a drop-in. MULTI-LATTICE SCALE LAW z(inf)=lowest-empty-level eigenvalue: TEST1 L=4 (N=64, different
lattice) PROBE=2 mu=1.0 in (0,2) -> z 1.678/1.800/1.846 -> 2; TEST2 L=6 PROBE=3 mu=2.5 in (2,3, different
probe level) -> z 2.773/2.852/2.862 -> 3. So z(inf) is the lowest-empty level (NOT the constant 2), holding
across lattice SIZE and PROBE LEVEL. SCALING ~linear in N (one beta=24 K8 NT1024 point: L=4 2.1s, L=6 7.4s,
L=8 16.3s); L~12-16 feasible per point, no stored data. HYBRID COMPLETE: phase 1 (multi_lattice_laws.py /
cfriedel_L.c) carries the laws (spectrum, probe level -> z prediction, Friedel) for any L instantly; phase 2
(cdet_planewave_engine.c) computes A,c1 and confirms z flows to the phase-1-predicted lowest-empty level; the
dual (surrogate/brute) is preserved, this is the third engine spending MC only where the laws run out. OPEN:
non-crystallographic L (irrational spectrum) needs a continuous-threshold freeze (lround only approximates the
levels) to test the scale law there cleanly. None of it moves the wall but makes z(inf)=lowest-empty-level a
proven size-independent, probe-general law. cdet_planewave_engine.c + hybrid_phase2_test.py (zflow; self-test
PASS), HYBRID_PHASE2_RESULT.md; csurrogate_params.h v123 note. Frozen engine untouched (194/194).

### #134 -- Toward million-site lattices: projector fast path, continuous freeze, run-to-log crash harness (v124)

Three improvements for large-L, day-long, unattended runs (streaming was already in place -- the engine
fflush-es every beta line). (1) PROJECTOR FAST PATH (million-lattice optimization): the plane-wave propagator
g0(dr,tau)=(1/N)sum_k cos(k.dr) val(eps_k,tau) is regrouped by DISTINCT eigenvalue: g0=(1/N)sum_{distinct eps}
[sum_{k:eps_k=eps}cos(k.dr)] val(eps,tau); the bracket P[dr][eps] is precomputed once for the ~7 fixed vertex
displacements (O(N)), then each propagator is O(#distinct eps) not O(N). EXACT -- at L=6 fast==direct to the
last digit (A=1.341555, c1=-234.4268). Speedups: L=12 direct 59.5s -> fast 0.81s (73x); L=48 (N=110592)
32.5s/pt. Collapse #distinct/N ~40-50x (cubic+cos degeneracy) plus dropping per-mode trig. -> L=100 (1e6 sites)
is a day-long z-flow (tens of MB, no stored spectrum). The direct O(N) path was ~3.6 h/pt at L=100 (13ms/site);
ceiling ~L=16 without the fast path. (2) CONTINUOUS-THRESHOLD FREEZE (mode 2) for non-crystallographic L: lround
mis-assigns levels on irrational spectra; the continuous freeze uses occupied=eps<=mu, probe=lowest-empty
eigenvalue->s, rest physical. TEST L=8 mu=1.0: lowest-empty eigenvalue = sqrt(2)=1.41421 (IRRATIONAL); z=sqrt2+
ln(|A|/|c1|)/beta rises 1.243/1.267/1.290/1.317 (beta=24/48/72/96) toward sqrt2. The scale law z(inf)=
lowest-empty-eigenvalue holds even when irrational -- fully universal. (3) RUN-TO-LOG HARNESS + NaN GUARD: the
engine prints '# NONFINITE...' and stops cleanly at the precision wall (no silent NaN); run_to_log.py streams
every line to a log (line-buffered + fsync, survives a hard crash), detects NONFINITE / nonzero exit / killing
signal, writes STATUS + last_good_beta, no run timeout -- safe to leave for a day. HOW BIG: direct path to
L~16; fast path L=100 (1e6 sites) a day-long z-flow; binding constraint is now beta-points/stats, not lattice.
None of it moves the wall. cdet_planewave_engine.c (fast path + mode 2 + NaN guard, both builds validate
0.00e+00) + run_to_log.py (selftest PASS) + hybrid_scaling_test.py (l8_zflow; self-test PASS),
SCALING_HARNESS_RESULT.md; csurrogate_params.h v124 note. Frozen engine untouched (194/194).

### #135 -- The large-L study: z(inf)(L) marches to the continuum Fermi level (v125)

Using the v124 machinery (plane-wave engine, projector fast path, continuous freeze, run_to_log), ran the
scale law up the lattice sizes. FROZEN PREDICTION (analytic, before measuring): at fixed mu=1.0, z(inf)=the
lowest-empty eigenvalue above mu closes onto mu as L grows, gap ~ L^-3.3 (the local level spacing ~1/L^3):
L=6 2.000, L=8 1.414, L=16 1.082, L=48 1.0009, L=100 1.00019. So z(inf)->mu thermodynamically -- the lattice
probe level converges to the continuum Fermi level. MEASUREMENT (fast-path z-flows, continuous freeze, streamed
through run_to_log): each L's flow z=lowest_empty(L)+ln(|A|/|c1|)/beta rises toward THAT L's lowest-empty value
-- L=8 1.243/1.267/1.290/1.317 ->1.414 (clean), L=12 ->1.268, L=16 1.013/1.029/1.038 ->1.082; the asymptote
MARCHES down with L (1.414->1.268->1.082->1.0002) toward mu=1.0 exactly as predicted, getting noisier as the
gap (and signal) shrinks. L=100 (a MILLION sites) ran at 52s/point via the fast path (45x collapse, 22027
distinct eigenvalues), probe_val reported = 1.000192 == prediction; the full z-flow is a day-long run. FINDING:
z(inf)(L)=lowest_empty(L)->mu as L->inf (continuum Fermi surface), but the determinant SIGNAL vanishes as the
gap closes (the probe merges into the Fermi sea, A and c1 both shrink) -- the thermodynamic measurement is
signal-starved and needs growing statistics. The wall sharpens onto mu: the scale law's content survives to the
continuum but resolving it there costs MC. thermo_limit_study.py (lowest_empty + recorded flows; self-test PASS)
+ THERMO_LIMIT_RESULT.md; csurrogate_params.h v125 note. Frozen engine untouched (194/194).

### #136 -- The signal budget: resolving z(inf) at large L costs ~N (polynomial, no exp wall) (v126)

z(inf) is read from z=probe_val+ln(|A|/|c1|)/beta; as L grows the gap g=lowest_empty(L)-mu closes (~L^-3.3)
and the signal weakens. WHICH BINDS (fast path, fixed stats K12 NT2048, beta=24, mu=1.0): relErr(A)~gap^0.06
(FLAT -- A stays O(0.1) at ~5-8% error any L); relErr(c1)~gap^-0.47 (GROWS as the gap closes). So c1, the
probe-channel response, is the BINDING signal -- it shrinks toward the Fermi sea as the probe level merges in.
BUDGET LAW: MC error ~1/sqrt(samples), so budget to hold z-precision ~ relErr^2 ~ gap^-0.9; with gap~L^-3.3,
budget(samples) ~ L^3 ~ N -- POLYNOMIAL, NOT exponential. Resolving z(inf) costs only ~linearly in the number
of sites; there is NO exponential sign-problem wall in this observable (doubling L needs ~8x stats). L=100
CHECK: K5 NT384 (1920 samples) c1=5.5e-4 +/- 3.9e-4 (~70% err, barely resolved), 117s/pt -- consistent; ~5% on
c1 needs ~170x more samples (~3.3e5/pt, ~5.5h/pt), so a day-long unattended run resolves a coarse z-flow at a
MILLION sites. LAUNCH RECIPE (day-long, crash-safe): python3 run_to_log.py LOG -- ./cpw grid 24 144 24 24 8192
31 0.002 2 2 1 2 4 1.0 -L 100 -fast (K24 NT8192 ~2e5 samples/pt x 6 beta; streams + fsync-logs; tail -f live).
signal_budget_study.py (fit_exponents; self-test PASS) + SIGNAL_BUDGET_RESULT.md; csurrogate_params.h v126
note. Frozen engine untouched (194/194).

### #137 -- The v116 sign(A,c1) selection rule vs large L: a finite-gap Friedel phenomenon (v127)

v116: a physical root z exists iff sign(A)!=sign(c1) (root s*=-A/c1>0 needs opposite signs); the sign pattern
varied by GEOMETRY at L=6. Varying L at fixed sites (1,2,4): FROZEN PREDICTION (before measuring): sign(A) is
set by the continuum density-matrix Friedel structure at the vertex displacements, converges as L->inf, so the
rule PERSISTS uniformly (always physical). RESULT -- PARTIALLY FALSIFIED (banked): sign(A) converges (stable -,
one small-L flip at L=12; the bulk background determinant) AS PREDICTED, but sign(c1) FRIEDEL-OSCILLATES with L
-- 24:-, 32:+, 40:-, 48:+ -- and is SEED-STABLE (L=24-/L=32+ across seeds 31/17/99; L=40-/L=48+ across 31/17),
so real Friedel, not MC noise. The probe eigenspace (lowest-empty level) is a set of momenta that shifts around
the Fermi surface as L changes (number theory of which cosine-sum lands just above mu); c1, the response to
occupying that eigenspace, oscillates with the probe momentum's Friedel phase at the vertex displacements --
same root cause as v117/v119, now in the PROBE channel vs lattice size. So the selection-rule OUTCOME alternates
yes/no with L, and since |c1|->0 as the gap closes (probe merges into the sea), the selection goes MARGINAL in
the continuum. CORRECTION: the rule does NOT uniformly persist; sign(A) persists, sign(c1) is a Friedel
oscillation in L with vanishing amplitude -- the v116 selection rule is a finite-gap (finite-L) Friedel
phenomenon, not a continuum invariant. Sharpens v116/v119: background sign (A, geometry) and probe-response sign
(c1, probe momentum) are both Friedel oscillations of the same elementary density matrix; only the background
survives to the continuum. selection_rule_continuum.py (physical(L); self-test PASS) + SELECTION_RULE_RESULT.md;
csurrogate_params.h v127 note. Frozen engine untouched (194/194).

### #138 -- The c1 sign in L: arithmetic jitter, not a Friedel period (v128)

v127 asked: derive the period of the sign(c1) oscillation in L and connect it to the v119 density-matrix
wavevector. ANSWER: there is NO clean period, and that absence (plus why) is the result. Two hypotheses frozen
before measuring: H1 period-16 (sign(L)==sign(L+16)); H2 arithmetic jitter (sign set by which cosine-sum
multiplet is lowest-empty at each L). MEASUREMENT (sign(c1), sites 1,2,4, beta=24, seed-stable): L=24- 28+ 32+
36+ 40- 44- 48+ 52-. H1 predicts 24/40(-/-) ok, 32/48(+/+) ok, but 28/44(+/-) and 36/52(+/-) MISMATCH; the
breakers L=28,36,44 are SEED-STABLE (seeds 31/17). So H1 FALSIFIED, H2 holds. WHY: the lowest-empty eigenspace
is whichever cosine-sum multiplet lands just above mu, and its dominant |kx|/L jumps number-theoretically with L
(0.29,0.13,0.05,0.0,0.07,0.0,0.0,0.06 for L=24..52), so the Friedel phase cos(2pi kx Dx/L) at the x-aligned
vertices (0,1,2,4) jitters with no period. CONNECTION TO v119 (by contrast -- the insight): A (background) =
(1/N) sum over the WHOLE occupied Fermi sea of cos(k.dr) -> smooth sum -> clean continuum Friedel wavevector
(v119), sign(A) CONVERGES (v127); c1 (probe response) = derivative w.r.t. occupying the SINGLE lowest-empty
multiplet -> discrete arithmetically-sensitive selection -> sign(c1) JITTERS, no period. That is exactly why
v127 saw A converge but c1 oscillate. The v116 selection rule lives in c1 -> arithmetic at finite L, marginal
(|c1|->0) in the continuum. No period to derive: the background carries the clean continuum wavevector, the
probe response carries only arithmetic remnants. probe_jitter_analysis.py (period16_holds; self-test PASS) +
PROBE_JITTER_RESULT.md; csurrogate_params.h v128 note. Frozen engine untouched (194/194).

### #139 -- A's continuum Friedel wavevector: v119's (120,180) is a convergent continuum feature (v129)

v119: the elementary density matrix rho(0,r)=(1/N) sum_{eps<=1} cos(k.r) is dominated by short-wavelength
(~2-3 site) structure at the level-1|2 boundary, characterized (120deg,180deg) at L=6. A's sign (v127/v128:
converges) superposes rho at the close vertex displacements, so this governs A. THE FERMI SURFACE IS
L-INDEPENDENT: {eps<=1} <=> cos(kx)+cos(ky)+cos(kz)<=-1/2 is a fixed continuum surface; v119's specific angles
were the L=6 discrete sampling (at L=6 only x-angles {0,60,120,180} exist, so boundary modes snap to 120,180).
THE FRIEDEL EDGE CONVERGES: the half-max crossing of the occupied weight W(kx) (the cosine-transform structure
of rho) along x goes kx/L = 0.425(L=6)/0.383/0.360/0.351/0.348/0.3476/0.3472(L=384) -> ~0.347 (~125deg, ~2.9
sites), sitting at the 120deg (3-site, 1/3) end of v119's (120,180) bracket -- (120,180) = the 3-site/2-site
wavelengths bracketing the ~2.9-site continuum oscillation. CONCLUSION: v119's dominant-wavevector
identification CONFIRMED as a real convergent continuum feature (Fermi surface fixed; edge -> kx/L~0.347~120);
the specific (120,180) values were the L=6 sampling. Clean counterpart to v128: A integrates the WHOLE sea ->
this convergent continuum wavevector (sign(A) converges, v127); c1 picks the SINGLE lowest-empty multiplet ->
arithmetic jitter (sign(c1) no period, v128) -- same density matrix, convergent wavevector to the background,
jittering remnant to the probe response. continuum_wavevector.py (edge_kxL; self-test PASS) +
CONTINUUM_WAVEVECTOR_RESULT.md; csurrogate_params.h v129 note. Frozen engine untouched (194/194).

### #140 -- Consolidation pass: surrogate, brute force, merged hybrid brought current (v130)

A consolidation sweep bringing all three engines current to v124-v129 and cross-validating side by side.
SURROGATE (csurrogate.c/.h): added L-generalized carriers surr_lowest_empty(L,mu) (scale law z(inf) for ANY L,
no eigendecomposition -- pure cosine arithmetic) and surr_friedel_edge(L,mu) (v129 density-matrix Friedel edge,
half-max of W(kx) -> ~0.347); banner updated; strict gate (-Wall -Werror -pedantic) clean, 28/28 match (worst
3.55e-15). BRUTE FORCE (cdet_vs_naive.c, cdet_small.c, cdet2d.c): re-stamped v130, still the ED-validated
naive-but-benign small-beta anchor (builds from frozen engine sources -I../engine); frontier now lives in the
hybrid. MERGED HYBRID (cdet_planewave_engine.c): header consolidated -- one engine carries phase-1 laws +
phase-2 connected determinant + projector fast path (-fast) + continuous freeze (mode 2) + NaN guard, validates
== stable engine at L=6 (0.00e+00). THREE-WAY CROSS-CHECK of z(inf)=lowest-empty(L,mu): L=6(mu1.845)->2.0,
L=8->1.41421, L=12->1.26795, L=48->1.00092 -- surrogate(C) == hybrid(C eng) == python, ALL AGREE; Friedel edge
surrogate-C == python (0.4250/0.3604/0.3483/0.3472, L=6/24/96/384). LESSON (recurring): the dual is a CHAIN --
surrogate CARRIES the laws (C, no eig), hybrid DERIVES them (plane-wave determinant), python REFERENCES them,
brute ANCHORS at small beta; cross-validation keeps all consistent. This pass found/fixed only build-hygiene
drift (stdlib include, calloc init for the strict gate, brute include path) -- NO numerical drift; the
v124-v129 physics is carried identically across all three. dual_consolidation_v130.py (self-test PASS) +
CONSOLIDATION_v130_RESULT.md; csurrogate.c/.h + the three brute stamps + hybrid header; csurrogate_params.h
v130 note. Frozen engine untouched (194/194).

### #141 -- CoS prototype: a verified subset-convolution reorganization of C_V, and an integration assessment (v131)

Following Gunnar Moller's papers (Kozik 2024 combinatorial summation CoS; Simkovic-Kozik 2019 self-energy CDet;
Frankenbach 2025 QTT), prototyped CoS against the engine's actual connected determinant. cos_harness.c dumps the
engine's per-subset D_corr/D_vac and ground-truth C_V (D_corr/D_vac/C_V are exposed in cdet_engine.h). VERIFIED:
(1) a faithful port of the engine's Rossi recursion reproduces C_V EXACTLY (0.0e+00, n=3..7) -- confirms we
understand the algorithm; (2) a CoS-style 2^n organization (solve D_corr = C (*) D_vac by subset convolution,
D_vac[empty]=1, rank-by-rank zeta domain, O(2^n n^2)) reproduces C_V to machine precision (2e-15). So the engine's
'mask' IS a connectivity record = CoS's R read backward (subset recursion) vs forward (DP); the 2^n wall is the
same object. HONEST COST: the 3^n submask combine only overtakes 2^n n^2 at n>=12, and both are dominated until
~n=16 by the shared 2^n*n^3 cost of the 2^n sub-determinants (which subset-conv does NOT touch). So swapping the
combine alone is a real but small win, only at high order; the big lever is the n^3->n^2 determinant prefactor,
needing the CoS forward DP (incremental minors). INTEGRATION LIST (ranked): (1) CoS forward DP w/ incremental
minors (real prefactor win); (2) SU(N) generalization O(n^3 4^n) N-independent -> the N=6 Yb EoS frontier the
engine cannot reach ((N^2/2)^n blowup); (3) self-energy/irreducible series (new observable); (4) CoS symmetrization
for MC variance reduction; (5) the verified subset-conv combine (easy, marginal, n>=12 only); (6) record-R pruning
= our suppression made algorithmic (highest upside, least certain); (7) QTT compression (outlier, park it).
cos_prototype.py (rossi_naive + cos_subsetconv; self-test PASS, live vs engine) + cos_harness.c +
COS_PROTOTYPE_RESULT.md; csurrogate_params.h v131 note. Frozen engine untouched (194/194).

### #142 -- Integration #1 (the prefactor win): the connected determinant in O(2^n n^2), as a supplement (v132)

First of the seven CoS upgrades, built as a SUPPLEMENT (frozen engine + all existing engines untouched). The
engine pays O(2^n n^3) + O(3^n): it recomputes each of the 2^n sub-determinants from scratch (O(n^3) LU per mask)
then runs an O(3^n) submask combine. Both removable: (a) FAST PRINCIPAL MINORS -- every D_vac[mask]=(-1)^|S|
det(M[S,S])^2 is a principal minor of the vertex matrix M, every D_corr[mask] adds the bordered minor
det(M+[{0}US]); all 2^n principal minors come from ONE Schur-complement recursion in O(2^n n^2) (the fast
principal minor algorithm CoS/CDet-fast use, Kozik 2024 ref [45]); two PMDs (M and bordered M+) give every D_vac
and D_corr. (b) SUBSET-CONVOLUTION combine (v131): O(3^n) -> O(2^n n^2). Chained, the full connected determinant
is O(2^n n^2) vs O(2^n n^3 + 3^n). VERIFIED live vs the engine (cos_harness.c): fast principal minors vs numpy
4e-14; D_vac vs engine all masks 1e-17; C_V (fast-minors + subset-conv) vs engine ground truth 3e-15 (n=3..7).
Determinant kernel ~n/3 faster (4x at n=12), compounding with the combine win. STATUS: a standalone verified path,
NOT an engine modification; realizing the speedup means wiring it into the hot loop gated by the engine's val-mode
(staged separately so 194/194 + 0.00e+00 stay baseline). Prerequisite for #2 (SU(N)) and #3 (self-energy).
fast_minors.py (all_principal_minors + fast_connected_determinant; self-test PASS live vs engine) +
FAST_MINORS_RESULT.md; csurrogate_params.h v132 note. Frozen engine untouched (194/194).

### #143 -- Physical mapping: z(inf) is the single-particle addition pole (a real spectral observable) (v133)

The crux Paul flagged: does z(inf)=lowest-empty-level encode REAL physics? Answer: yes -- it is the leading
single-particle ADDITION POLE (the lowest unoccupied excitation above the Fermi sea). Chain, each link already
banked: (1) z(b)=eps_probe+ln(s*)/b -> z(inf)=eps_probe (ZINF v111); (2) the level MOVES as L grows (2.0 -> sqrt2
-> 1.268 -> 1.082 -> 1.0002, v125) and z(inf) TRACKS it (dev <=4e-7) -- a detector of a moving pole, not a
constant; (3) the v78 cancellation lemma (FUGACITY_STRUCTURE) proves <C>(mu) is exactly rational in fugacity
e^{b.mu} with poles ONLY at mu=eps_k (Matsubara comb at the single-particle levels; fugacity_structure.py saw the
3.9e6 rise at the comb), so the deep-beta z-flow is a real-axis extraction of the nearest pole above the sea =
the lowest-empty level. So z(inf) is the single-particle addition spectrum's leading pole -- the standard object
DiagMC reconstructs by analytic continuation. HONEST BOUND: poles sit at the BARE eps_k (g0 = free spectrum), so
z(inf) is the FREE addition energy; the interacting one eps_k+Re Sigma(eps_k) needs the self-energy resummation =
exactly integration #3. So z and #3 are the same physical target at two resummation levels; #3 turns the free
addition spectrum z measures today into the interacting one, without undoing the free z-flow (the Sigma=0 limit).
physical_mapping.py (self-test PASS: z(inf)==addition pole, worst dev 4e-7, pole sweeps 1.0002..2.0) +
PHYSICAL_MAPPING_RESULT.md; csurrogate_params.h v133 note. Frozen engine untouched (194/194).

### #144 -- Integration #3 (step 1): the self-energy as the interacting upgrade of z, ED-verified (v134)

Building on the v133 mapping (z(inf) = FREE addition pole eps_k; interacting = eps_k + Re Sigma): established the
self-energy observable and verified it exactly vs exact diagonalization (hubbard_ed.py), the ground truth the
diagrammatic self-energy series (Simkovic-Kozik) will reproduce. (A) ATOM: Sigma(iw)=G0^-1-G^-1 from the ED
Lehmann G matches the closed-form atomic Sigma = U<n> + U^2<n>(1-<n>)/(iw+mu-U(1-<n>)) to 1e-15 -- the Dyson
extraction is correct. (B) DIMER (free levels -+t): the spectral-weight-averaged addition energy of the
lowest-empty (antibonding) mode is EXACTLY eps_free = z(inf) at U=0, and eps_free + Re Sigma at U>0 (1.271 @U.5,
1.563 @U1, 2.236 @U2, 2.995 @U3; leading shift = Hartree U<n_-s>). So z and #3 are the same physical target at
two resummation levels: z reports the Sigma=0 (free) addition pole, the self-energy series reports the
interacting one. SUPPLEMENTS z (the free z-flow = the Sigma=0 limit, recovered to 1e-9); ED is only the
verification anchor; frozen engine untouched. NEXT sub-step: compute Sigma diagrammatically (engine-side
irreducible series) reusing the v132 fast minors, verify convergence to this ED Sigma. self_energy.py (self-test
PASS) + SELF_ENERGY_RESULT.md; csurrogate_params.h v134 note. Frozen engine untouched (194/194).

### #145 -- Integration #3 (step 2): the diagrammatic self-energy converges to the exact Sigma (v135)

Showed the ENGINE-SIDE route reaches the v134 interacting self-energy. Pipeline per Matsubara frequency:
a_n(iw) = U^n coefficients of G(iw;U) (the connected-determinant order series the engine samples / the v132 fast
minors evaluate at O(2^n n^2)); G_diag = sum_n a_n U^n (resum); Sigma_diag = G0^-1 - G_diag^-1 (Dyson). VERIFIED
(atom, vs closed-form/ED Sigma): geometric convergence inside the bare-series radius ~pi/beta -- U=0.3 order2->1.4e-2
order8->7e-6; U=0.5 order8->6.6e-4; U=0.8 (near radius) order8->4.9e-2 (slows). The radius limit is exactly why
Simkovic-Kozik compute the IRREDUCIBLE (1PI) series DIRECTLY (larger radius) rather than connected-G+Dyson -> so
this both verifies the diagrammatic Sigma and pinpoints step 3 (the direct irreducible recursion, the convergence
upgrade). Order coefficients here = exact U-contour integral on the ED G (the target the connected-det MC converges
to); the coefficients->G->Sigma pipeline + convergence are what is verified. ED anchor only; engine untouched.
self_energy_diagrammatic.py (self-test PASS) + SELF_ENERGY_DIAGRAMMATIC_RESULT.md; csurrogate_params.h v135 note.
Frozen engine untouched (194/194).

### #146 -- Integration #3 (step 3): the irreducible (1PI) series and its larger convergence radius (v136)

The reason Simkovic-Kozik compute Sigma DIRECTLY. v135's connected-G+Dyson inherits G's radius R_G (G's pole in U).
The self-energy's OWN series sum sigma_n U^n has a larger radius R_Sigma, because the G-pole is a REGULAR point
of Sigma (G->inf => G^-1->0 => Sigma=G0^-1 finite); Sigma's nearest singularity is further out -- for the atom the
PARTITION-FUNCTION zero Z(U)=0 (Im U ~ pi/beta), not the G-pole. DEMONSTRATED (atom beta=5 mu=0.5 vs exact ED
Sigma): R_G~0.80, R_Sigma~1.76 (2.2x larger). Inside R_G both work (bare cleaner); PAST R_G the bare series
DIVERGES (U=0.9->2.5, U=1.1->13.5, U=1.3->10) while the direct 1PI series stays converged (~0.1, 0.096, 0.059).
HONESTY: here sigma_n come from a Cauchy contour on the ED Sigma(U) inside R_Sigma -- a proxy whose accuracy floors
~1e-1 (the G-pole sits near the contour); the production route computes sigma_n EXACTLY via the 1PI determinant
recursion (connected-det recursion with one-particle-reducible diagrams removed, reusing v132 fast minors), giving
the full radius with no contour noise -- the remaining engine-side build. Supplements v135 (bare = inside-R_G).
ED anchor only; engine untouched. self_energy_irreducible.py (self-test PASS) + SELF_ENERGY_IRREDUCIBLE_RESULT.md;
csurrogate_params.h v136 note. Frozen engine untouched (194/194).

### #147 -- Integration #3 (step 4): exact 1PI coefficients, and a CORRECTION to v136 (v137)

Computed the EXACT self-energy coefficients and, in doing so, RETRACTED an overclaim in v136. v136 claimed the
1PI series has a much larger radius (R_Sigma~1.76 vs R_G~0.80, "2.2x", "reaches strong coupling the bare series
can't") -- WRONG. v136 extracted sigma_n by a contour on Sigma(U) at rS~1.0-1.5 that ENCLOSED Sigma's own
singularity near |U|~0.8, so those were not Taylor coefficients; they gave a bounded-but-wrong (~1e-1) result that
masqueraded as convergence. CORRECT (this step): exact sigma_n via the Dyson coefficient recursion (no contour):
a_n = connected-G coeffs (a0=G0), sigma_n = a_n/G0^2 - (1/G0) sum_{m<n} sigma_m a_{n-m}. These reproduce the ED
self-energy to 1.9e-9 @U=0.3, 6e-5 @U=0.5. Their decay gives the TRUE radii: R_G~0.73 (|a_n|^1/n), R_Sigma~0.84
(|sigma_n|^1/n) -- ESSENTIALLY EQUAL, no significant advantage. The genuine Simkovic-Kozik advantage is EFFICIENCY
(compute Sigma directly, no G inversion) + lower MC VARIANCE, NOT a larger bare-series radius; reaching strong
coupling needs resummation (Pade/conformal) or action-shift tricks, applied to G and Sigma alike. STILL STANDS
(unaffected): v133 (z=free addition pole), v134 (addition energy=eps+ReSigma, ED-verified), v135 (diag-Sigma
converges within its radius). Only v136's radius claim is retracted; the exact recursion replaces the flawed proxy.
self_energy_irreducible.py (rewritten, self-test PASS) + SELF_ENERGY_IRREDUCIBLE_RESULT.md (rewritten with the
retraction); csurrogate_params.h v137 note. Frozen engine untouched (194/194).

### #148 -- Full consolidation of the Moller-paper integration program (v138)

Consolidated v131-v137 and ran the three engines/paths side by side (consolidation_v138.py, the single health
gate). THREE-WAY AGREEMENT: surrogate-C == plane-wave-C(==stable @L6, 0.00e+00) == python on the addition pole =
lowest-empty level (worst 5e-10); fast minors == engine connected determinant (3e-15); exact 1PI sigma_n == ED at
U=0.3 (7e-8). All three engines build clean (surrogate 3.55e-15; frozen 194/194). LEARNINGS / further fixes from
the runs: (1) plane-wave shows ~2e-7 rel dev at tiny values (~5e-11, below the 1e-13 floor) -> use -DUSE_LD for
deep-cancellation probes; (2) the self-energy observable lives in Python/ED -> wire the diagrammatic sigma_n into
the engine, and per v137 strong coupling needs RESUMMATION (Pade/conformal), not the irreducible series; (3) fast
minors O(2^n n^2) is standalone -> wire into the hot loop (val-gated, #5); (4) the surrogate carries the free
addition pole but not the interacting shift -> could carry the leading Hartree U<n_-s> as a cheap interacting-pole
estimate. README + QUICKSTART refreshed (ledger #1..#147; current frontier = the integration program; the v137
retraction noted). All supplements; frozen engine untouched (194/194). consolidation_v138.py (self-test PASS) +
CONSOLIDATION_v138_RESULT.md; csurrogate_params.h v138 note.

### #149 -- Stress test of the hybrid plane-wave engine, + robustness guards (v139)

Stressed the hybrid's ACTUAL features (any-L plane-wave, -fast projector path, mode-2 continuous freeze, NaN
guard) -- the session's new features are supplements NOT yet wired in (#5). ROBUST: validation == stable @L6
0.00e+00; fast == direct bit-identical (L6, L12); scales to 2.7M sites (L=140) in 193s via fast path; freeze
probe_val at L=100 == surrogate exactly (1.000192); NaN guard fires cleanly on every overflow (no crashes).
PRECISION (confirms v138): f64 walls at beta~100 (NaN guard), long double reaches beta>=200 -> use -DUSE_LD for
deep-cancellation. THREE silent/misleading failure modes FOUND + now GUARDED (input-only, valid runs byte-identical,
val stays 0.00e+00): (a) mode 0/1 at non-crystallographic L (not in {1,2,3,4,6}) blows up to nonsense (z~1e23) with
no warning -> warn, use mode 2; (b) large delta contaminates the linear-response c1 (sign flip @delta=0.5) -> warn
if delta>0.1; (c) delta=0 -> c1=NaN mislabeled "precision wall" -> refuse delta<=0 with a clear message. Also: fast
path collapses ~50x but leaves ~60k distinct eigenvalues @L=140 (the cost driver); c1 shrinks at large L (v126
signal-budget law live). stress_test_v139.py (self-test PASS: validation, fast==direct, guards) +
STRESS_TEST_v139_RESULT.md; cdet_planewave_engine.c gained the 3 input guards (re-validated 0.00e+00);
csurrogate_params.h v139 note. Frozen engine untouched (194/194).

### #150 -- Resummation / precision: can we borrow the gravity-loop idea? (v140)

Paul uploaded gravity_loop_verification (a different project, the Watford gravity-loop cascade) which gets exact
15-digit resummation because its loop coefficients obey an EXACT linear 3-term recurrence -> rational generating
function -> closed form. Assessed whether that transfers to our models (tested vs exact ED self-energy): (1) NO
exact-recurrence transfer -- our sigma_n obey no finite linear recurrence (order 2..5 errors 3.5e-2..5.4e-4, never
0; the Hubbard partition function adds a transcendental e^{-beta U}), so the GF is not rational and there is no
15-digit closed form. (2) PADE transfers for REACH not precision -- a [8/8] Pade of Sigma(U) turns a 3.2e13
divergence at U=3 into a 0.23 estimate (extends past the bare radius ~0.8), but residual ~0.2-1 (structure-limited,
Sigma not rational) and worse than the bare series inside the radius. So Pade = the strong-coupling reach tool
(#3), not precision. (3) Most of our models already have EXACT resummation: the engine (exact Rossi recursion),
the surrogate (closed-form), Dyson (G=G0/(1-Sigma G0) exact rational in Sigma) -- no truncation to improve. (4)
The general accuracy lever = extended-precision ARITHMETIC (LD/mpmath) in cancellation regimes: the hybrid's LD
build reaches beta>=200 where f64 walls at beta~100 (v139). So: resummation extends reach, extended precision
improves accuracy; the 15-digit exact-recurrence route is specific to a rational series and not ours.
resummation.py (self-test PASS) + RESUMMATION_RESULT.md; csurrogate_params.h v140 note. Frozen engine untouched.

### #151 -- Fold-in of session enhancements + the rational self-energy hint (v141)

FOLD-IN (enhancements into the models, where appropriate): (1) the surrogate gains surr_interacting_pole(L,mu,U,nsig)
= surr_lowest_empty + U*nsig -- the leading interacting addition pole (free pole + Hartree shift U<n_-sigma>, the
v134 leading self-energy term); the Sigma=0 limit recovers the free pole exactly (gate check added, surrogate gate
still 3.55e-15). (2) Confirmed already-folded: the v139 input guards (delta<=0, large delta, non-crystallographic L)
live in the hybrid; the LD deep-cancellation path is in the engine. (Fast-minors hot-loop wire-in remains #5 -- it
would alter the hybrid's C_V path and is a separate val-gated build; not forced.) THE RATIONAL HINT (Paul's lead,
now LIVE): v140 said the self-energy isn't rational -- but that was GRAND-CANONICAL. At FIXED density the atom
self-energy Sigma(U)=U n + U^2 n(1-n)/(iw+mu-U(1-n)) IS rational: exact 1-term (geometric) recurrence
sigma_(k+1)=[(1-n)/(iw+mu)]sigma_k for k>=2 (dev 2e-10), and the [2/1] closed form reproduces Sigma to 1.3e-15 at
ALL U up to 3 (past any bare radius). The grand-canonical nd(U) was the ONLY non-rational piece. So the 15-digit
exact-recurrence route lives in the SKELETON / bold (fixed-density, Luttinger-Ward / Prokof'ev-Svistunov) expansion.
Verified: the atom. Open: whether the LATTICE skeleton self-energy inherits a finite rational structure -- the
standing lead. rational_skeleton.py (self-test PASS) + RATIONAL_SKELETON_RESULT.md; csurrogate.{c,h}+test gained the
carrier; csurrogate_params.h v141 note. Frozen engine untouched (194/194).

### #152 -- Queue #2 (SU(N)), step 1: the atom EoS + the N-polynomial record (v142)

Started the queue's clearest physics item, #2 (SU(N) -> the N=6 173-Yb EoS). Step 1 establishes the CoS
N-independence structure on the exactly-solvable SU(N) atom (single site, H=-mu sum n_a + U sum_{a<b} n_a n_b;
E_k=-mu k+U k(k-1)/2, degeneracy C(N,k); at U=0 the flavors are independent so k~Binomial(N,p)). FINDING: the
linked-cluster object ln Z(U) has U-coefficients c_j = kappa_j(Y) (-beta)^j/j! where Y_k=k(k-1)/2 (interacting-pair
count) and kappa_j is its cumulant under the U=0 binomial; since binomial factorial moments are polynomial in N,
each c_j(N) is an EXACT degree-(j+1) polynomial in N -- the combinatorial RECORD (each flavor loop = one factor N).
VERIFIED: c_j(N) degree j+1 (fit N=2..7 predicts N=8,9,10 to 4.8e-9); exact-cumulant coeffs match an ED contour to
2.2e-11; SU(6) atom density at U=1 = 0.308978 (the Yb flavor number). So compute the N-independent kernel once,
evaluate at any N. (Note: the per-flavor density is a ratio and is NOT polynomial in N; ln Z is -- the right
linked-cluster object.) OPEN (step 2): the LATTICE SU(N) connected determinant, record = closed-loop count of the
actual diagrams, reusing the v132 fast minors -> toward the N=6 Yb lattice EoS. sun_atom_record.py (self-test PASS)
+ SUN_ATOM_RECORD_RESULT.md; csurrogate_params.h v142 note. Frozen engine untouched (194/194).

### #153 -- Queue #2 (SU(N)), step 2: the record survives hopping (v143)

The question that matters for a real lattice EoS: does the v142 atom N-polynomial record survive HOPPING? Tested on
a 2-site SU(N) Hubbard cluster by ED (2N orbitals, 2^{2N} states; H = -t hop(same flavor) - mu n + U sum_site
sum_{a<b} n_a n_b). FINDING: YES, the record survives. (1) U=0 factorization ln Z(N)=N*single-flavor to 1.3e-14
(ED correctness). (2) c1(N) is a degree-2 polynomial -- fit N=2,3,4 predicts N=5,6 to 5e-5 (self-test predicts N=5
to 7e-6); 3rd finite-difference over N ~3e-5. (3) c2(N) degree 3 -- predicts N=6 to ~1e-3 (finite-difference
extraction noise floor). So the CoS N-independence (compute the N-independent kernel once, evaluate the polynomial
at any flavor number) holds for the LATTICE, not just the atom -> the N=6 173-Yb EoS is reachable from the kernel
WITHOUT diagonalizing N=6. SCOPE: verified c1 (deg 2) tightly, c2 (deg 3) at the noise floor; c3 (deg 4) consistent
but needs N>6 (dense ED OOMs at 2^14). OPEN: the production lattice connected-determinant with the closed-loop
record from g0 minors (v132 fast minors compute the per-flavor minors; the N^loops record sits on top) -- the
remaining engineering for the full EoS. sun_lattice_record.py (self-test PASS) + SUN_LATTICE_RECORD_RESULT.md;
csurrogate_params.h v143 note. Frozen engine untouched (194/194).

### #154 -- Queue #2 (SU(N)), step 3: the production EoS route (v144)

Built the PRODUCTION route the record enables: compute the SU(N) EoS from the N-independent single-flavor g0 TIMES
the record, WITHOUT diagonalizing the N-flavor system (the CoS value proposition). First coefficient, 2-site
lattice, with d=per-flavor density and d'=d(d)/dmu of the FREE SINGLE-FLAVOR system: c1=-beta N(N-1) d^2 (record
N(N-1)=flavor pairs); n1=-(N-1) d d' (EoS density coeff, record (N-1)). Both reproduce the SU(N) ED to ~1e-7 for
EVERY N=2..6, and the N=6 (173-Yb) value comes purely from single-flavor g0 + record -- NO N=6 diagonalization. The
first-order EoS n(U)~n0+U n1 at N=6 tracks the ED curve at small U (2.9e-3 @U=0.05) and departs at larger U (~0.1
@U=0.3) where higher orders enter. So the single-flavor g0 (computed once) x the combinatorial record gives the
EoS at any flavor number -- exactly how CoS reaches N=6 at SU(2) cost. SCOPE: first-order (Hartree) coeff via g0 x
record verified at all N incl N=6, no N-flavor ED. OPEN: higher orders -- the full connected-determinant sum with
the closed-loop record + imaginary-time integrals (v132 fast minors supply the per-flavor minors) -> the
strong-coupling EoS curve. sun_lattice_production.py (self-test PASS) + SUN_LATTICE_PRODUCTION_RESULT.md;
csurrogate_params.h v144 note. Frozen engine untouched (194/194).

### #155 -- Queue #2 (SU(N)), step 4 + the gravity-loop hint realized in N (v145)

TWO findings, one mechanism. STEP 4: the record persists to SECOND order -- n2(N), the 2-site SU(N) 2nd-order EoS
coefficient (ED), is a low-degree polynomial in N (deg-3 fit N=2..5 predicts N=6 to ~3e-4). THE GRAVITY-LOOP HINT,
FOUND: the gravity math resums exactly because its loop coeffs obey a finite linear recurrence -> rational GF ->
closed form. v140 showed this does NOT happen in our coupling U (only the atom is rational). It DOES happen in the
flavor number N: the record makes every coefficient a polynomial in N, so (a) the coeffs obey a finite linear
recurrence in N (a degree-d poly has vanishing (d+1)-th difference = an order-(d+1) recurrence; c1's 3rd diff is
7e-15), (b) their N-generating-function sum_N c(N)x^N is RATIONAL with denominator (1-x)^{d+1} (residual 7e-15),
(c) so the all-N dependence resums EXACTLY -- from c1 at N=1,2,3 reconstruct c1(6) exactly (dev 0) and the large-N
rate (N^2 coeff = -beta d^2). SAME mechanism as the gravity loops (finite recurrence -> rational GF -> exact
resummation), realized in N not U; shared structure = the recurrence, spectra differ (our characteristic root is 1,
polynomial/combinatorial growth; gravity's was a cubic, exponential). This is also WHY CoS is N-independent -- the
N-resummation is built in. So the gravity resummation idea, which didn't transfer to U (v140), transfers cleanly to
N. Remaining engineering unchanged: full CDet + closed-loop record + tau-integrals (v132 fast minors) for the
strong-coupling-in-U EoS curve. sun_resummation_N.py (self-test PASS) + SUN_RESUMMATION_N_RESULT.md;
csurrogate_params.h v145 note. Frozen engine untouched (194/194).

### #156 -- The U-axis rational lead, pursued to its boundary (v146)

Pursued the v141 standing lead (does the LATTICE skeleton self-energy inherit the atom's rational structure?) and
found its boundary with a clean theorem. THEOREM: Sigma(iw;U) is rational in U IFF the many-body eigenvalues E_k(U)
are LINEAR in U IFF the interaction is diagonal in the energy basis. The ATOM's U n_up n_dn is diagonal in the
occupation basis -> linear eigenvalues -> rational (15-digit, v141). BOUNDARY: with hopping the kinetic term does
NOT commute with the interaction (||[H_kin,H_int]||=1.4 for the dimer vs 0 for the atom), so eigenvalues are
ALGEBRAIC in U -> Sigma is ALGEBRAIC (branch points), NOT rational. Verified: dimer Sigma fails the constant-coeff
recurrence (residual 0.21 vs atom ~1e-4) with branch-point coefficient growth. CONSEQUENCE: the exact 15-digit
RATIONAL route is confined to the ATOM / LOCAL self-energy (Hubbard-I / DMFT-atomic, the Mott-physics driver). The
full lattice Sigma is algebraic -- a finite-degree closed form in principle, but branch points cap simple
resummation (Pade reaches past the radius, 1e6->O(1) @U=3, not to 15 digits; conformal/algebraic is the lattice
tool). NET (the two axes differ): rational is EXACT along N (the record, v145 -- constant-coeff recurrence) and
along U only LOCALLY (the atom, v141); along U the lattice is ALGEBRAIC because hopping makes the eigenvalues
nonlinear in U. rational_lattice_boundary.py (self-test PASS) + RATIONAL_LATTICE_BOUNDARY_RESULT.md;
csurrogate_params.h v146 note. Frozen engine untouched (194/194).

### #157 -- Full consolidation: three models at highest capability (v147)

Consolidated the integration arc (v131-v146) and brought all three models to their highest proven capability,
keeping the analysis supplements as separate CLI modules (Paul's design directive). ARCHITECTURE made explicit:
(1) FROZEN REFERENCE engine/ (194/194, NEVER altered) -- the validation anchor every result is checked against;
its validated numerics are not changed (that is what keeps the archive trustworthy); efficiency via make fast
(-O3 -march=native) / make omp. (2) PRODUCTION ENGINE cdet_planewave_engine.c (hybrid) -- carries every capability
(any-L, -fast projector, -DUSE_LD deep precision, mode-2 freeze, 3 input guards, multi-million sites) and validates
== the frozen reference bit-for-bit at L=6 (0.00e+00). (3) SURROGATE csurrogate.c -- fast arithmetic carriers, now
gaining surr_sun_c1(N,d)=-N(N-1)d^2 and surr_sun_n1(N,d,d')=-(N-1)d d' (the SU(N) EoS coefficients = record x
single-flavor amplitude, v144; match the python production route at N=6; gate still 3.55e-15). Kept as separate
CLI modules (better design + end-user options): fast_minors, cos_prototype, physical_mapping, self_energy*,
rational_skeleton, sun_atom/lattice_record, sun_lattice_production, sun_resummation_N, rational_lattice_boundary,
resummation. JUDGMENT CALL (stated to Paul): did NOT alter the frozen engine's validated numerics -- its frozen-ness
is the trust foundation; an LD rebuild would need invasive source changes, so the engine keeps its f64 numerics +
fast/omp targets, and the hybrid is the LD/capability mirror. README + QUICKSTART + engine/README refreshed to the
three-model architecture; ledger range #1..#156. consolidation_v147.py (self-test PASS: 3 models agree, all caps
live) + CONSOLIDATION_v147_RESULT.md; surrogate gained sun_c1/sun_n1 + gate check; csurrogate_params.h v147 note.
Frozen engine untouched (194/194).

### #158 -- The unified end-to-end model: cdet_lab.py control plane (v148)

Built the new additional model Paul asked for: a complete end-to-end version that contains EVERY feature as
SWAPPABLE COMPONENTS, driven purely from the terminal after unzipping -- WITHOUT touching the frozen reference.
It is a CONTROL PLANE, not a fourth engine: it unifies the two C engines + surrogate + ~dozen analysis modules at
the INTERFACE level via three orthogonal choices. --target = the observable {eos (<n>(mu)), self-energy, addition-
pole, double-occ, connected-det}; --method = the swappable solver {ed, record, hubbard-i, diagrammatic, surrogate,
hybrid, fast-minors, engine}; --model/params = the system {atom|dimer|lattice, N, U, mu, beta, L, t}. The
(target,method) map is ENFORCED (undefined combos rejected -> `list`). DESIGN GROUNDED IN A WEB SEARCH of what
physicists configure: the SU(N) cold-atom EoS <n>(mu) benchmark (Pasqualetti PRL 132.083401, Kozik CoS 2309.13774,
T/t=0.3 U/t=2.3 N=6); DMFT self-energy/spectral workflows (DCore/TRIQS) with the Hubbard-I rational Sigma as the
Mott/large-U solver (confirmed EXACTLY = our v141/v146 form, arXiv 1101.4870) and atomic-limit validity at integer
filling/large U (0911.1422); DiagMC observables energy/entropy/double-occupancy/spin-correlations (PRB 87.205102).
Commands: list, validate (runs the consolidation health gate), and --target/--method/--model. Self-test routes 5
representative components end-to-end (PASS); list/validate/swaps/guard all verified. cdet_lab.py (self-test PASS) +
CDET_LAB_RESULT.md; README+QUICKSTART point to it as the single entry point; csurrogate_params.h v148 note. Frozen
engine untouched (194/194).

### #159 -- The idiot-proof conversational front-end: cdet_shell.py (v149)

Built the friendly text interface Paul specified, grounded in a web search of CLI best practices (clig.dev: the CLI
is a CONVERSATION; make it DISCOVERABLE; design with EMPATHY). cdet_shell.py is a two-state machine (HOME/CONFIRM)
over cdet_lab: the user describes what they want in plain language; the shell interprets it, states back what it
thinks they meant WITH every assumed default shown (no hidden options), presents the exact command, and runs it only
after yes/no. 'no' reverts to HOME but never loses the named/saved configuration library. INTELLIGENCE on imperfect
input: synonyms map plain words to components (density->eos, sigma->self-energy, mott->hubbard-i); typo-robust (a
surviving keyword still resolves, e.g. 'addtion pole'); did-you-mean + example syntax when nothing resolves or when
an explicit method is unknown ('via teleport' -> lists valid solvers). NAMED CONFIGS: save <name> / save as <name> /
run <name> / forget <name> / configs; the library survives reverts. It is a THIN SAFE layer: imports the
(target,method) map from cdet_lab as the single source of truth (so nothing drifts/hides), never invents
capabilities, and routes every run through cdet_lab so the frozen reference stays the anchor. Self-test = a 14-step
scripted session through the state machine (clarify->confirm->execute, 'no' keeps the library, typos/bad-methods get
guidance, help/list/examples/configs reachable); live stdin REPL verified end-to-end (real Hubbard-I run). cdet_shell.py
(self-test PASS) + CDET_SHELL_RESULT.md; README+QUICKSTART point to it as the friendly entry point; csurrogate_params.h
v149 note. Frozen engine untouched (194/194).

### #160 -- Blind usability test + hardening of cdet_shell.py (v150)

Used the shell as a zero-knowledge user (vague/wrong/impatient/contradictory input; actively trying to get stuck or
lose the way back). Found SIX real problems and fixed all, regression-guarded in a now-21-step self-test. (1) The
CONFIRM step was a TRAP: cancel/back/help/quit all looped on 'please answer yes or no' -- the user couldn't even quit
-> now yes/no match by intent (first word + keyword: 'yes please','actually nevermind','cancel','back' all work),
quit/exit leave from any state, help explains the confirm options, and a new request mid-confirm is explained rather
than stonewalled. (2) N (flavors) vs n (vertices) COLLISION: 'N=0' set both (both lowercase to 'n') -> case-sensitive
N vs n. (3) NO VALIDATION: SU(0) ran, 'U=abc' silently dropped -> reject out-of-range with a fix ('N must be >=1')
and warn on non-numeric assignment. (4) SYNONYM SUBSTRING BUG: 'connected determinant' picked method 'ed' because
'ed' matched inside 'connectED' -> word-boundary synonym scan. (5) rigid confirm phrasing -> lenient intent. (6)
menu/options/'what can you do' -> help; stray yes/no at home -> gentle 'nothing pending'. VERDICT vs the criteria:
not possible to get stuck (every state has labeled exits, quit always works), easy to get back to start (no/cancel/
back/nevermind revert, saved library survives), logical (one describe->confirm->run loop), understandable (defaults
shown, errors suggest the fix), powerful (full control plane reachable). cdet_shell.py (self-test PASS, 21 steps) +
BLIND_TEST_v150_RESULT.md; csurrogate_params.h v150 note. Frozen engine untouched (194/194).

### #161 -- Sweep / stress harness with cutoffs, logs, data, and graphs: cdet_study.py (v151)

Built the sweep/stress capability Paul asked for: scan one parameter for a chosen (target,method), collect data,
detect convergence or accuracy breakdown, stop on USER-DEFINED CUTOFFS, and emit logs + data + graphs with the
points of interest marked. CUTOFFS: --max-time T (stop when cumulative wall time > T s), --accuracy-cutoff EPS (stop
when error vs the natural reference > EPS; references: diagrammatic Sigma vs ED, record EoS vs ED, fast-minors det
vs numpy), --conv-tol TOL (flag convergence when |delta y|<TOL for k consecutive steps). OUTPUTS to
./cdet_runs/<stamp>_<target>_<var>/: data.csv (x,y,error,step_s,elapsed_s), summary.json (config + stop reason +
points of interest), plot.png (y on left axis, error on log right axis, convergence/breakdown/cutoff/min/max
markers; matplotlib Agg, graceful fallback), run.log (timestamped + highlighted summary), and an ASCII plot printed
to the terminal (always, headless-safe) with a legend. PHYSICALLY MEANINGFUL demos: diagrammatic Sigma vs ED error
climbs 2e-14->2e-2 as U approaches the bare-series radius (~pi/beta) and the accuracy cutoff stops exactly there;
addition-pole vs L converges to z(inf) and conv is flagged. WIRED INTO cdet_shell: plain-language sweeps ('sweep U
from 0.2 to 1.2 for self-energy diagrammatic beta 5 mu 1, stop if accuracy drops below 5e-3'; 'scan L ... until it
converges'; 'vary n ... stop after 10 seconds') -> interpreted, the exact cdet_study command shown with cutoffs
spelled out, confirmed, run, and saveable like any config; missing range -> friendly prompt. Shell self-test now 25
steps (incl 2 sweep cases); cdet_study self-test = convergence + accuracy + time cutoffs + ascii plot. cdet_study.py
(self-test PASS) + CDET_STUDY_RESULT.md; csurrogate_params.h v151 note. Frozen engine untouched (194/194).

### #162 -- SU(N) step 5 (capstone): the record-predicted EoS curve in U (v152)

Assembled steps 1-4 into the full equation of state <n>(U) and pushed it as far in U as the algebraic structure
allows. PIPELINE: (1) extract the per-flavor density U-series n_k(N) to order K=8 for small N=2,3,4,5 via a clean
complex-U CONTOUR on the solvable 2-site reference (mu=1,beta=2,t=1) -- needed a local complex-U Hamiltonian since
the real build_H drops Im(U); (2) RECORD-PREDICT the N=6 series: fit each order n_k(N) as a polynomial in N and
evaluate at N=6 -- WITHOUT diagonalizing the SU(6) system (the production promise, now for the whole series);
(3) Pade[3/3]-RESUM into <n>(U); (4) VALIDATE vs DIRECT SU(6) ED at real U. RESULT: the record-predicted N=6 curve
(using only N<=5 data) matches direct SU(6) ED to ~1-2% out to U~1.2 -- an order of magnitude past the bare-series
radius (~0.16, the v146 algebraic branch point); leading coeffs n0,n1,n2 predicted to 1e-4..1e-3. HONEST REACH: the
bare series converges only to the branch-point radius; Pade extends to U~1.2 at the percent level; strong coupling
(U/t~2-3, the Kozik/Yb regime) needs the conformal/algebraic resummation of the v146 boundary, not more orders --
the natural next build. NET (SU(N) arc closed): the EoS is exactly N-predictable (the record), its U-reach is set by
the algebraic branch point; the two axes behave exactly as established (N rational/exact, U algebraic/finite-reach).
sun_eos_curve.py (self-test PASS, N<=5, ~40s) + SUN_EOS_CURVE_RESULT.md; csurrogate_params.h v152 note. Frozen
engine untouched (194/194).

### #163 -- Reaching strong coupling: SU(N) EoS by two-point resummation (v153)

The v152 capstone reached only U~1.2 (Pade capped by the v146 algebraic branch point). This reaches STRONG COUPLING
(U/t~2-3, the Kozik/Yb regime) by anchoring BOTH ends of the coupling axis instead of extrapolating one. WEAK (U->0):
the lattice record series n_k(N) (v152). STRONG (U->inf): the per-flavor density -> atomic limit with 1/U expansion
n=m0+m1/U+...; m0 = t=0 SU(N) atom density (the v142 atom record, single-site, NO 2-site diagonalization), m1 =
leading hopping correction; both m0(N),m1(N) smooth in N -> record-predictable from small N. A two-point Pade [2/2]
matching 3 weak + 2 strong coeffs bridges the crossover; the modest order is deliberate (higher orders develop
spurious poles in the physical window -- the weak series' small radius poisons them; [2/2] is stable, verified by a
(J,L) scan). RESULT: the record-predicted SU(6) EoS (only N<=5 data, NO SU(6) diagonalization) matches direct SU(6)
ED across the WHOLE coupling range, reaching U/t=2.3 (the Kozik benchmark coupling) at 2.4% and worst <5% out to U=4.
NET: the SU(N) EoS is now record-predicted weak->strong -- weak end from the lattice record (v152), strong end from
the atom record (v142), bridged by a stable two-point Pade; both N-extrapolations are exact-in-N records, and the
U-axis (algebraic, finite-radius each side, v146) is SPANNED by anchoring both limits. sun_eos_strong.py (self-test
PASS, N<=5, ~2s) + SUN_EOS_STRONG_RESULT.md; csurrogate_params.h v153 note. Frozen engine untouched (194/194).

### #164 -- The SU(N) production route in the 2D thermodynamic limit (v154)

Made the jump from the 2-site reference to the real target (2D square lattice, the Kozik/Pasqualetti 173-Yb SU(6))
on one fact: THE RECORD IS LATTICE-INDEPENDENT. The N-combinatorics ((N-1), N(N-1)) does not know about the lattice;
only the single-flavor input changes. The leading (Hartree) EoS coefficient is n1(N)=-(N-1) d d' (record x free
single-flavor density d and compressibility d'=dd/dmu). VALIDATED: n1 from the formula matches direct SU(N) cluster
ED to 1e-7..1e-9 on 2-site, 1D ring-4, AND a genuine 2D square cluster (2x3) -- so the leading SU(N) EoS coefficient
on ANY lattice is the record times the free d,d'. THERMODYNAMIC LIMIT: replace the cluster d,d' with converged free
2D k-integrals (eps(k)=-2t(coskx+cosky); nk=120 vs 240 identical) -> d(mu=1,beta=2)=0.671378, d'=0.152391 -> the 2D
SU(6) leading EoS coefficient n1=-0.511561 with NO finite-cluster diagonalization. STRONG COUPLING: the atomic limit
(t=0, single decoupled site) is lattice-independent, so the v142 atom-record anchor and the v153 two-point construction
extend to 2D unchanged (weak 2D Hartree + strong atom record) -- the production prediction to be benchmarked against
the Kozik DQMC/experiment (<n>(mu) at T/t=0.3, U/t=2.3, N=6). NET: the record carries the N-dependence unchanged from
the 2-site reference to the thermodynamic limit; only the single-flavor amplitude is recomputed as a 2D integral.
sun_eos_2d.py (self-test PASS, ~25s) + SUN_EOS_2D_RESULT.md; csurrogate_params.h v154 note. Frozen engine untouched
(194/194).

### #165 -- The second-order EoS coefficient: record x single-flavor amplitudes, Hartree part exact in 2D (v155)

To extend the 2D weak series past leading order we need n2. DECOMPOSITION (the point): n2(N) = (N-1)^2 a + (N-1) b.
a = d(d'^2 + 1/2 d d'') is the SELF-CONSISTENT HARTREE iteration, built entirely from the free single-flavor density
d and its mu-derivatives d',d'' -- NO interaction integral. (The naive guess 1/2 d^2 d'' is WRONG: it drops the d'^2
term from feeding n1 back through the Hartree shift, and even has the wrong sign -- this was the earlier sticking
point.) a grows as (N-1)^2 (5x the bubble at N=6) -> the dominant piece. b = the genuine second-order particle-hole
BUBBLE (correlation), subleading in N. VALIDATED (2-site): a from the free-derivative formula matches the fitted
(N-1)^2 coefficient to 1.8e-7, and the decomposition (a exact + b fitted) predicts n2(N=6)=1.046125 vs direct SU(6)
ED 1.046266 (err 1.4e-4). THERMODYNAMIC LIMIT: a is built from d,d',d'' -- converged free 2D k-integrals -> the
DOMINANT (N-1)^2 part of the 2D n2 is exact with no diagonalization: a_2D(mu=1,beta=2)=0.005622 -> 2D SU(6) n2
dominant part 25 a_2D=0.140544; the bubble b is the subleading correction (its 2D value is the local G(tau) bubble
integral, the one remaining single-flavor amplitude). NET: like n0,n1, the second-order coefficient is record x
single-flavor amplitudes; its fastest-growing-in-N piece is pure self-consistent Hartree and exact in the 2D
thermodynamic limit. sun_eos_n2.py (self-test PASS, N<=5, ~6s) + SUN_EOS_N2_RESULT.md; csurrogate_params.h v155
note. Frozen engine untouched (194/194).

### #166 -- Consolidation of the v148-155 arc (v156)

Periodic checkpoint per the consolidation rule (precedent: consolidation_v101/115/120/130/138/147). Deliverable is a
HEALTH GATE, not a new result: consolidation_v156.py (~1s) re-proves the whole current state coheres. Re-checks the
three-model invariants (surrogate SU(N) c1,n1 == production route; surrogate addition pole == python; fast-minors
connected determinant == numpy det) AND runs ONE fast live check, each tied to an exact anchor, of every capability
added since v147: (A) the UI control plane -- cdet_lab (10 components), cdet_shell (shares cdet_lab.COMPONENTS),
cdet_study (sweep harness); (B) the SU(N) EoS arc -- weak n0=free single-flavor density (v152), strong atomic anchor
smooth in N + stable two-point [2/2] (v153), 2D production transfer + converged k-integral n1=-0.5116 (v154), 2D n2
Hartree part a_2D=0.005622 (v155). All pass vs ED/k-integral anchors; frozen engine/ 194/194 untouched. The
consolidation rule itself is recorded as standing protocol (THE CONSOLIDATION RULE section). consolidation_v156.py +
CONSOLIDATION_v156_RESULT.md; csurrogate_params.h v156 note.

### #167 -- Triple-run benchmark added to the consolidation rule; hybrid auto-fast improvement (v157)

Per Paul's extension, the consolidation rule now includes a TRIPLE-RUN BENCHMARK + IMPROVEMENT CYCLE: build and run
all three models (surrogate csurrogate.c, brute-force frozen reference engine/, hybrid cdet_planewave_engine.c),
compare strengths/weaknesses vs the frozen anchor (correctness, wall-time, coverage/scaling), apply improvements to
the EVOLVING models, retest the gains, record benchmarks. HARD SAFEGUARD (flagged + baked in): the frozen reference
SOURCE is never edited -- that would destroy the validation anchor; its only improvements are the existing make
fast/omp build variants. APPLIED THIS RUN: the hybrid's projector fast path was shown BIT-IDENTICAL to the default
(val 0.00e+00 and grid output unchanged, verified) and collapses ~17x for crystallographic L (216 modes -> 13
distinct), so it is now AUTO-ENABLED for crystallographic L (default-on, -nofast escape hatch) -> measured ~26x grid
speedup (0.34s vs 8.83s at NT=1500); val still 0.00e+00; the frozen engine/ (194/194) is untouched. Benchmark table
recorded (surrogate ~1.5ms instant/exact-on-coverage, hybrid ~4ms exact+scalable, brute force ~2.5s canonical). The
rule update is recorded in THE CONSOLIDATION RULE section. triple_benchmark.py (self-test PASS, ~6s) +
TRIPLE_BENCHMARK_v157_RESULT.md; cdet_planewave_engine.c auto-fast change; csurrogate_params.h v157 note.

### #168 -- Chained two-round run: continuing the electron's position (v158)

Per Paul: a pure micro-efficiency study -- run all three twice, round-1's result moves the electron to its next
position, which seeds round-2. The persistent "electron position" of the stochastic engine is its RNG stream state
st_; round-1 ends there and round-2 CONTINUES from it (not a restart). APPLIED (hybrid, evolving model): expose the
terminal sampler state at grid end (print-only -- no computed number changes; val still 0.00e+00; frozen reference
untouched). EFFICIENCY (measured, beta=30, NT=2000, vs NT=16000 ref): chained 2x2000 continuation err 0.0319 vs
single 0.0443 -> 1.39x (~sqrt2) -- the correct scaling for doubling INDEPENDENT samples (the continued stream never
overlaps); a naive SAME-seed rerun is identical (zero new info), so the terminal-state chaining is exactly what
makes round-2 count. Practical: refine by CONTINUING (reuse round-1 work) instead of restarting at 2xNT. EXPANSION
(config-space, 30 rounds, C(5,3)=10): a deterministic result-seeded walk visits only 1-2 configs (CYCLES -- a
finite-state deterministic map must), but the chained-stream continuation sweeps 9/10 (no cycle). BOTH gains come
from the same act of continuing round-1's stream into round-2 (independent samples that never repeat -> efficiency,
never cycle -> expansion). The deterministic models (surrogate/brute force) cannot expand under pure result-seeding;
their role is fast evaluation (surrogate ~1000x the exact CDet per config) while the stochastic continuation
supplies exploration. chained_run.py (self-test PASS, ~10s) + CHAINED_RUN_v158_RESULT.md; cdet_planewave_engine.c
terminal_state print; csurrogate_params.h v158 note. Frozen engine untouched (194/194).

### #169 -- Two-particle chained two-round run (v159)

Per Paul ("add two particle run twice"): repeat the chained two-round protocol with TWO particles -- where the
physics begins, since two particles obey EXCLUSION (no double occupancy, Pauli) and carry a PAIR correlation (the
connected two-body content the CDet exists to capture). EXPANSION: the two-particle chained-continuation walk moves
one of the two particles each round to a free site (never onto the other -- exclusion), continuing the stream so it
never cycles; it sweeps the FULL pair-config space 10/10 (C(5,2)) with exclusion held throughout. EFFICIENCY
(hybrid, vs NT=20000 ref): chaining round-1's terminal stream into round-2 reduces the error of BOTH the one-body
amplitude A (1.44x) and the two-body interaction response c1 (1.39x) by ~sqrt2 -- the gain REACHES THE INTERACTION,
not only the amplitude (an earlier 6-seed read gave c1 1.07x but that was noise; 12-14 seeds give ~sqrt2 for both).
NET: the continuation gains carry from one particle to two and from the amplitude to the interaction; exclusion is
respected throughout. two_particle_run.py (self-test PASS, ~20s) + TWO_PARTICLE_RUN_v159_RESULT.md; csurrogate_params.h
v159 note. Frozen engine untouched (194/194).

### #170 -- Conformal-Borel resummation: pushing the order axis (v160)

Took Paul's field comparison (CDet: lattice is the easy axis -- thermodynamic limit; 12x12 ~30s is normal -- the
real frontier is ORDERS reached+resummed) and web-searched the state of the art: practical CDet reaches ~10-13
coefficients (vs ~6-7 older DiagMC); the bare-U series has a finite radius from a non-trivial complex-U analytic
structure (branch point -- exactly v146, the lattice self-energy is algebraic in U); the resummation SOTA is
conformal-Borel (Rossi/Van Houcke/Werner; Prokof'ev-Svistunov) keyed to the Borel-plane singularity, plus shifting
the starting point (homotopic/shifted action). ADDED conformal-Borel to the SU(N) EoS: Borel transform b_k=n_k/k!;
locate the Borel singularity via Borel-Pade poles (COMPLEX here, |t_c|~1.05 -> Borel-summable); exact re-expansion
in w(t)=(sqrt(1+t/Uc)-1)/(sqrt(1+t/Uc)+1) by series composition; Borel sum. VALIDATED vs ED (2-site SU(N)): beats
plain Pade ~4x at U=0.6, ~2x at U=1.0 -- more physics per order from the SAME coefficients. HONEST CEILING (retract
overreach): an early run with a favorable |t_c| reached U~2.5 at ~4%, but that was not robust to the singularity
estimate, so it is NOT claimed; reliable strong coupling needs the large-order/instanton structure (the field's
genuinely hard part) or the v153 two-point bridge (conformal-Borel is its better weak-side engine). SYNTHESIS with
the two-particle runs: reach-per-order (conformal-Borel) x orders-per-cost (chained continuation sqrt2, both A and
the interaction) = the two levers the field actually pushes; lattice size was never the bottleneck. sun_eos_conformal.py
(self-test PASS, ~3s) + SUN_EOS_CONFORMAL_v160_RESULT.md; csurrogate_params.h v160 note. Frozen engine untouched (194/194).

### #171 -- Consolidation of the v157-160 arc (v161)

Full consolidation per the rule (with the v157 triple-run + improvement-cycle extension), retaining the frozen
baseline for parity. consolidation_v161.py health gate (~4s, PASS): v147 cross-model invariants; FROZEN BASELINE
PARITY (hybrid 0.00e+00 vs the reference -- the retained anchor); v157 auto-fast bit-identical to -nofast (~28x);
v158 terminal-state chaining; v159 two-particle exclusion (10/10 pair-configs); v160 conformal-Borel beats Pade.
Triple-run benchmark recorded with the frozen reference as the parity anchor (surrogate ~2.9ms/3.55e-15; hybrid
~5.6ms/0.00e+00; brute force ~2.5s/194-194). IMPROVEMENT CYCLE: profiled the hybrid inner loop -- set_freeze_d
recomputes the s=0 and s=delta occupation arrays every sample though they are sample-INDEPENDENT; precomputing them
once and swapping pointers is BIT-IDENTICAL (val 0.00e+00; grid output identical) but the measured gain is NEGLIGIBLE
(0.621->0.617s, ~0.6%, within noise -- C_V dominates), so it was NOT added to the source (complexity for no benefit).
The genuine next lever -- a low-rank determinant update for the freeze-0->freeze-delta change (the freeze flips only
the probe-level occupation, entering g0 linearly) -- is identified but parity-risky and DEFERRED until it can be
validated bit-identical against the frozen baseline. Honest outcome: the big lever (-fast ~28x, v157) is already
applied; not every improvement cycle yields a new safe win. Precedent: consolidation_v101/115/120/130/138/147/156.
consolidation_v161.py + CONSOLIDATION_v161_RESULT.md; csurrogate_params.h v161 note. Frozen engine untouched (194/194).

### #172 -- Large-L plane-wave propagator: 100x100 + thermodynamic-limit confirmation (v162)

Took Paul's comparison (the method's strength is that big finite lattices are unnecessary -- past the correlation
length ~12-16 sites the finite result IS the thermodynamic limit; 100x100 needs the closed-form/FFT propagator route my
own notes describe). The 2D engine's numerical path was capped at 16x16 because it stores eigenvectors (O(LMAX^2),
LMAX=256). ADDED the closed-form plane-wave path (lattices.c/.h): square2d_pw_init + square2d_G0_pw evaluate the free
propagator straight from the analytic dispersion eps=-2t(cos kx+cos ky), G0(i,j;tau)=(1/N) sum_{kx,ky}
cos(k.(r_i-r_j)) g_band(eps_k;tau), using ONLY a 1D cosine table (which doubles as the phase table) -> O(L) memory, no
eigenvectors. Reaches 100x100 = 10^4 sites, far past LMAX. VALIDATION: exact vs the numerical square2d path where both
apply (worst |G0_num - G0_pw| = 1.25e-16 at L=6 and L=12). TD-CONVERGENCE (NN propagator G0(r=(1,0),tau=0), beta=5):
within ~5e-4 of the infinite system by 16x16, ~1e-5 by 32x32, and 100x100 confirms it (Delta=2.2e-11 vs 64x64) -- the
concrete demonstration that you don't need huge lattices, and the cap is removed when you want it. The LMAX cap is
BYPASSED not raised (raising is O(LMAX^2) memory and risks stack overflow; the plane-wave path is the right tool, as the
original notes said). Existing numerical val2d still matches (3.39e-09, no regression). Frozen reference engine/ used
read-only, untouched (194/194). square2d_pw_demo.c (gate: parity<1e-12) + lattices.c/.h + SQUARE2D_PW_v162_RESULT.md;
csurrogate_params.h v162 note.

### #173 -- Unified `cdet` CLI (v163)

Started Paul's elevation checklist at the highest-impact item: a top-level unified CLI. ADDED cdet.py -- one `cdet`
entry point over the whole codebase with subcommands validate/converge/resum/eos/run/sweep/lab/shell/info, per-command
--help, and friendly error handling (try/except with usage hints). Output is rich-optional: a small console layer uses
`rich` tables/panels when importable and falls back to clean ASCII otherwise, so the shipped package needs NO external
dependency (stdlib argparse only). `cdet validate` compiles+runs every gate (frozen reference 194/194, surrogate match
1e-9, hybrid 0.00e+00 parity vs the frozen anchor, 2D plane-wave exact+TD-converged, consolidation health gate) and
prints a single PASS/FAIL table -- the validation-depth showcase. `cdet converge` renders the v162 4x4->100x100 TD table;
`cdet resum` the v160 conformal-Borel-vs-Pade improvement; `cdet run` the hybrid production grid. Snappy defaults
(resum/eos N=4, fully ED-validated); SU(6) cold-atom is a several-minute contour run guarded by a disk cache + a status
note (not shipped -- runtime artifact). Launcher script `./cdet`; README quickstart prepended. Frozen engine untouched
(used read-only by `validate`). cdet.py (--selftest gate PASS) + README quickstart; csurrogate_params.h v163 note.
This addresses checklist #1 (unified CLI + rich output); the rest of the checklist is the roadmap (python bindings,
streaming/high-order, more observables, packaging/CI, docker).

### #174 -- Double occupancy observable (v164)

Continued the elevation checklist at item #3 (more physics output). ADDED double_occupancy.py: the double occupancy
D=<n_up n_dn> as a proper interacting observable for the 2-site SU(N) reference (the suite previously had only the
atomic single-site limit). Uses the thermodynamic identity <D_hat> = -(1/beta) dlnZ/dU, D per site = <D_hat>/N_sites
(N_sites=2), with D_hat = sum_site sum_{a<b} n_{site,a} n_{site,b} (= sum_site n_up n_dn for N=2). The U-series comes
from a complex-U contour on lnZ, mirroring density_series. VALIDATION: two INDEPENDENT ED routes agree to ~1e-10 -- the
lnZ U-derivative (docc_ed) and the direct thermal average of D_hat over the ED spectrum (docc_ed_direct). Physical
checks: monotone Mott suppression (D falls 0.549->0.293->0.141->0.069 across U=0,1,2,3 for N=2); conformal-Borel
resummation 65x better than plain Pade at U=1; interaction-energy link E_int/site = U*D. Wired into the CLI as
`cdet docc` (ED / conformal-Borel / E_int table). Frozen engine untouched (194/194). double_occupancy.py (self-test gate
PASS) + cdet.py docc subcommand; csurrogate_params.h v164 note. Remaining checklist roadmap: python bindings,
streaming/high-order, more observables (susceptibilities, self-energy maps), packaging/CI, docker.

### #175 -- Susceptibilities: charge compressibility + spin (v165)

Continued the checklist at item #3 with the linear-response susceptibilities. ADDED susceptibilities.py: charge
compressibility kappa = d<n>/dmu and spin susceptibility chi_s = d<Sz>/dh|_{h=0} for the 2-site SU(N) reference (Sz =
sum_site (n_up-n_dn)/2). VALIDATION: each computed by TWO INDEPENDENT ED routes -- a derivative route and a
fluctuation-dissipation route (kappa == (beta/2N) Var(N_hat); chi_s == beta Var(Sz)) -- agreeing to ~1e-7; the routes
share no code path, so it is a genuine cross-check (same discipline as the v164 double occupancy). PHYSICS: the
opposite-trend hallmark of Mott correlation -- kappa DECREASES with U (charge fluctuations suppressed, approach to the
incompressible Mott state: 0.268->0.183->0.111) while chi_s INCREASES (local-moment formation, enhanced magnetic
response: 0.268->0.285->0.318->0.487). Each also gets a complex-U weak series (contour, like density_series) resummed
with conformal-Borel (chi_s err 3.5e-3 vs ED at U=1). Wired into the CLI as `cdet chi` (kappa/chi_s table with the
cross-dev columns). Frozen engine untouched (194/194). susceptibilities.py (self-test gate PASS) + cdet.py chi
subcommand; csurrogate_params.h v165 note. Remaining roadmap: python bindings, streaming/high-order, self-energy maps,
packaging/CI, docker.

### #176 -- Visualization: built-in figures (v166)

Continued the checklist at item #3 (visualization). ADDED plots.py: built-in matplotlib figures (Agg backend, no
display) rendered from the SAME code paths the gates validate, so the plots cannot drift from the numbers. Four
figures: (1) 2D thermodynamic-limit convergence -- nearest-neighbour propagator vs lattice size 4->100 with the
correlation-length band (the python plane-wave G0_NN matches the validated C path to round-off); (2) resummation reach
-- conformal-Borel vs plain Pade abs-error vs U on the SU(N) EoS (log-y); (3) the Mott story -- double occupancy and
charge compressibility falling while the spin susceptibility rises (the opposite-trend hallmark, all three on one
axis); (4) a 2x2 summary dashboard adding a validation-status panel (frozen 194/194, hybrid 0.00e+00, observables
cross-checked vs ED). Wired into the CLI as `cdet plot [convergence|resummation|mott|summary] [--out dir]`. Frozen
engine not involved (post-processed observables). plots.py (self-test gate PASS) + cdet.py plot subcommand;
csurrogate_params.h v166 note. cdet_figures/ is a runtime artifact (not shipped).

- DATA EXPORT (v169): checklist item #3 (export formats: HDF5/JSON/CSV for integration). Added export.py -- every
  validated observable (convergence, resummation, eos, docc, chi) exports to CSV / JSON / HDF5, each dataset reproduced
  from the SAME gated code paths (cannot drift, like plots.py). CSV+JSON use only the stdlib; HDF5 is optional (h5py).
  Each file carries column names + metadata (N, beta, mu, etc.). self-test round-trips every dataset (write CSV/JSON,
  read back, assert numeric match). Wired as `cdet export [what] [--format csv|json|hdf5|all]`; pyproject gains a
  [hdf5] extra (h5py) added to [all]. export.py (self-test gate PASS) + the CLI subcommand. (cdet_data/ is a runtime
  artifact, not shipped.)

- NATIVE BINDINGS (v170): the heavier roadmap item -- pybind11 bindings to eliminate subprocess overhead for
  programmatic use. Added bindings/cdet_core.cpp -- a native module wrapping the FROZEN reference engine's C primitives
  (G0_atom, G_exact_atom, density_exact, n_F) plus the 2D plane-wave propagator (square2d_g0), all read-only (engine
  source untouched). Because these ARE the frozen functions compiled in, results are BIT-IDENTICAL to the 194/194
  engine (parity vs a freshly-compiled frozen-C reference = 0.0e+00). Benchmark: native call ~120 ns vs ~232 ms for one
  compile+subprocess -> ~2e6x overhead removed per engine access, so Python loops over the engine are now native.
  OPT-IN build (bindings/build.py compiles the .so) so the pure-python `pip install` stays compiler-free; pyproject
  gains a [bindings] extra (pybind11), README documents it, CI builds+gates it. bindings/bindings_check.py is the gate
  (build + bit-identical parity + speed). The platform-specific .so is NOT shipped (source ships, rebuilt on target).

- DOCKER (v171): the last roadmap item -- one-command deployment. Added Dockerfile (python:3.12-slim + gcc/g++,
  COPY, pip install -e ".[all]", ENTRYPOINT cdet, default CMD validate) and .dockerignore (excludes pycache/.so/egg-info/
  figures/data). The build BAKES IN validation: it runs `make CC=gcc test` so the image won't build unless the frozen
  engine passes 194/194; `docker run cdet-suite` then runs `cdet validate` by default. docker_check.py gates the recipe
  structure; CI gains a docker job that actually builds the image and runs `cdet validate` in the container (on GitHub,
  where Docker is available). HONEST: `docker build` is not run in this sandbox (no Docker daemon) -- but every command
  the Dockerfile runs (pip install, make test -> 194/194, cdet validate -> 5/5) was verified natively, and each is
  covered by its own gate. This completes the elevation checklist (CLI, observables, figures, export, packaging/CI,
  dual license, native bindings, docker). Dockerfile + .dockerignore + docker_check.py (gate PASS).

- THE WALL vs LATTICE SIZE (v172): attacked the convergence wall with the new large-L machinery to test where lattice
  size HELPS the order axis. The bare-U series' leading weak-coupling wall is the RPA/Stoner instability
  U_c(L)=1/chi0_max(L), where chi0 is the free static Lindhard susceptibility from the plane-wave dispersion
  eps_k=-2t(cos kx+cos ky) -- the v162 feature. chi0 needs only the O(L) dispersion, so U_c(L) is computable at ANY L
  up to 100x100 (L=100 ~2s). FINDING: the wall is a thermodynamic-limit quantity; the small-lattice wall is a
  finite-size artifact. Near half-filling (nesting q=(pi,pi), the dominant Hubbard channel) the small lattice is
  spuriously PESSIMISTIC -- U_c=1.64 at 4x4 vs the true TD wall 1.975 -- so growing L pushes the wall back: LATTICE
  HELPS. Honest nuances banked: at incommensurate doping the artifact reverses sign (small lattice optimistic, 4.37 ->
  3.30); and U_c is the leading REAL-axis instability (= the exact bubble-sum radius), while the FULL radius can be set
  by complex-U structure closer than this (the v146 caveat). Validated 5 ways (sum rule 0.0e+00; vectorized==brute
  3.3e-16; bubble-series radius==U_c; TD convergence 1e-9; wall recedes with L). wall_vs_size.py (self-test gate PASS)
  + `cdet wall` + WALL_VS_SIZE_v172_RESULT.md. Frozen engine untouched. Remaining roadmap: python bindings,
streaming/high-order, self-energy maps, docker.

- THE WALL IS A TIDE (v173): Paul asked to sweep lattice size up/down and work out the wall's "waves". U_c(L) does not
  drift smoothly to the TD limit -- it OSCILLATES, because chi0(q,L) is a Brillouin-zone quadrature and whether the peak
  momentum q* lands on a grid point depends on commensuration with L. Three wave laws, all validated: (1) PERIOD = 2pi/q*
  -- the oscillation wavelength in L measures the nesting vector (half-filling q*=(pi,pi) -> period 2 even/odd; doped
  mu=-2.8 q*x=0.542pi -> period 3.68 == 2/0.542). (2) BRANCH LAWS at half-filling: even L (peak on-grid) converges
  EXPONENTIALLY (BZ-quadrature spectral accuracy, ratio ~0.5 per dL=2); odd L (peak missed by ~pi/L) converges as 1/L^2
  (p=-1.89). Even from below (1.64->1.975), odd from above (3.13->1.99); meet at U_inf=1.9752. (3) AMPLITUDE decays with L
  (split 1.49@L4 -> 0.035@L32): violent in 'shallow water' (small L), calm in 'deep water'. wall_tide.py (gate PASS) +
  `cdet tide` + WALL_TIDE_v173_RESULT.md. Frozen engine untouched.

- PRIME LATTICE SIZES = A DIOPHANTINE SIEVE (v174): Paul asked to step the lattice through primes and find patterns. The
  v173 error law (deviation ~ curvature x (grid-miss to q*)^2) makes the lattice size enter through NUMBER THEORY: the
  grid-miss distance is how well the rational grid {k/L} approximates q*/2pi. PRIME L (no divisors) are
  commensuration-blind -- they cannot land a grid point near any low-denominator momentum, so they always miss q* and
  ride the UPPER envelope of the tide; COMPOSITE L (many divisors) capture the peak. Quantified (mu=-0.6, q*=(0.78,1)pi):
  primes deviate ~2.7x more than composites; corr(#divisors,dev)=-0.39; holds WITHIN odd L (primes 0.022 > odd-comp
  0.014, so deeper than the v173 parity); and the whole effect IS the v173 curvature law -- corr(grid-miss^2, dev)=+0.96.
  Filling-dependent (the Diophantine signature): sharp near a low-denominator peak, washes out at a generic-irrational
  peak (x2.7 -> x1.1 at mu=-2.8). Takeaway: never read a finite-lattice wall off a prime lattice; prefer sizes whose
  divisors match the nesting vector. Validated 5 ways. wall_primes.py (gate PASS) + `cdet primes` +
  WALL_PRIMES_v174_RESULT.md. Frozen engine untouched.

- HALF-INTEGER LATTICES = TWISTED BC + RECTANGULAR SUPERCELLS (v175): Paul asked if lattices can be half-integer. No
  fractional site count, but two standard senses: (A) twisted BC k=2pi(n+theta)/L with theta=1/2 = anti-periodic = the
  literal half-shifted grid; (B) rectangular Lx x Ly cells (non-square q-grid). Used them to test whether the v173 tide /
  v174 sieve are real or sampling artifacts. VERDICT: twist does NOT heal the sieve -- in the particle-hole
  susceptibility the twist cancels in k->k+q differences, so the momentum-TRANSFER grid q=2pi m/L is theta-independent
  (peak q-index identical for theta=0 and 1/2); anti-periodic does not flip the even/odd parity and twist-averaging trims
  the prime error only ~7%. So the sieve is a q-RESOLUTION effect. But a RECTANGULAR supercell whose q-grid lands on q*
  DOES heal it: 23x46 hits q*=(18/23,46/46) -> error 4e-4 even though 23 is PRIME, vs square 17x17 -> 6e-2. Unifying rule
  is DIOPHANTINE: capture <=> q*_comp*L/2 near an integer (per direction). Conclusion: the tide and sieve are finite-size
  q-sampling artifacts of the grid vs the nesting vector, not properties of the true wall; cure is a supercell hitting q*,
  not a finer twist. Validated 4 ways. wall_twist.py (gate PASS) + `cdet twist` + WALL_TWIST_v175_RESULT.md. Frozen engine
  untouched.

- CONSOLIDATION v176 (one wall core; all models side by side): Paul asked to consolidate + apply upgrades to all modules
  and docs, test all models side by side, find/fix issues, retest. (1) DRY'd the 4 wall modules onto ONE canonical core
  wall_vs_size.chi0_max_rect(Lx,Ly,beta,mu,thx,thy,t) -- the rect+twist upgrade now lives in the base; wall_twist
  delegates (removed its duplicate _fermi/chi0_max), tide/primes already imported it; square-periodic results unchanged
  (dev 0.0e+00). (2) Docs: added a Wall-physics section to the README (was undocumented) + `cdet crosscheck`. (3)
  Side-by-side cross-check (consolidation_v176.py): E shares one core; B<->E chi0(q=0)==dn/dmu (free compressibility,
  7e-13); D<->E the SAME finite-radius phenomenon in two systems (U_c^EoS=1.054 vs U_c^wall=1.975; resummation extends
  past both -- at U=0.7 bare EoS diverged |bare-ED|=3.6 but conformal-Borel tracks ED |cb-ED|=0.009). (4) Issues fixed:
  duplicate Lindhard core -> single chi0_max_rect; README doc gap -> filled. (5) Retested ALL models green (surrogate,
  frozen 194/194, cdet validate 5/5, observables D, wall E, CLI, packaging, docker). Frozen engine untouched.
  consolidation_v176.py (gate PASS) + `cdet crosscheck` + CONSOLIDATION_v176_RESULT.md.

- THE TRUE RADIUS IS THERMAL, NOT THE RPA WALL (v177): went after the deferred probe -- does the TRUE radius (nearest
  complex-U singularity of lnZ, the v146 branch point) inherit the tide/sieve? EXACT ANCHOR: the Hubbard atom's lnZ is
  singular at Fisher zeros U=-ln(A)/beta +- i pi/beta (A=(1+2e^{bmu})e^{-2bmu}); a direct complex-zero finder reproduces
  the analytic radius to 0.0e+00. FINDINGS: (1) the true radius is THERMAL -- its nearest singularity is a complex pair
  at Im U ~ pi/beta (Matsubara-like), categorically different from the real-axis RPA wall. (2) It is CLOSER than the RPA
  wall (ring L=3: R_true 2.90 < R_RPA 3.42) -- the complex-U structure, not the Stoner instability, sets the actual
  radius (the v146 caveat, now numerical). (3) It does NOT inherit the Diophantine sieve: the sieve is specifically a
  chi0_max grid-MAX artifact (grid misses q*), while R_true is a global lnZ property with no q-grid max, so the sieve
  mechanism is structurally absent. HONEST LIMITATION: a direct large-L test is precluded (sieve needs large L = 2D
  lattice; R_true needs small L = ED; the complex-zero search is delicate -- L=4 flips between resolutions, L=3 stable).
  The case rests on the exact atom anchor + thermal nature + the structural no-grid-max fact + small-ring evidence.
  Validated 5 ways. wall_true_radius.py (gate PASS) + `cdet trueradius` + WALL_TRUE_RADIUS_v177_RESULT.md. Frozen engine
  untouched.

- CONSOLIDATION v178 (one index for the whole package): Paul asked to consolidate all files and docs. The package had
  grown to ~647 files (127 RESULTs, 176 CROSSCHECKs, a ledger of #1..#188, the frozen engine, the wall suite) with NO
  top-level map. Added INDEX.md -- the single authoritative entry point: the three-model architecture, the directory map,
  all 19 CLI subcommands, the two arcs (elevation checklist v163-171 + wall-physics arc v172-177), and where each kind of
  knowledge lives (ledger / RESULTs / CROSSCHECKs / benchmark note). Fixed README (now lists trueradius, points to INDEX);
  QUICKSTART left as-is (build-and-verify, still current). Verified: every file reference in INDEX/README resolves to a
  real file; all 19 CLI subcommands documented; no broken refs or orphans; cdet validate 5/5; frozen 194/194; surrogate
  3.55e-15. Frozen engine untouched. INDEX.md + CONSOLIDATION_v178_RESULT.md + README/csurrogate notes.

- TIER 0: IMPLEMENTED THE CONNECTED DETERMINANT ITSELF (v179): after an honest web-search reality-check (the suite was a
  validation harness AROUND a frozen engine and had never implemented CDet -- the Rossi 2017 method the package is named
  for), Paul said build Tier 0. Implemented the connectedness recursion C(V)=D(V)-sum_{v* in S subsetneq V} C(S)D(V\S)
  with the full weight D(V)=det(M)^2 per spin (M_ab=G0(vertex_a,vertex_b), vertex=(site,tau)), and the free-energy series
  U^n coeff = (-1)^n * integral over the ordered-tau simplex of C. VALIDATED THREE WAYS to machine precision: (1) the
  linked-cluster identity D(V)=sum_partitions prod C(B) at random positions n=2..5 (worst 2e-16, no quadrature -- proves
  the recursion combinatorics); (2) atom lnZ U-series orders 1..5 vs the closed form (6e-17); (3) 2-site Hubbard lattice
  lnZ U-series orders 1..3 vs ED (order1 1e-12, order2 2e-12, order3 1e-9). HONEST FRAMING (module + result): a faithful
  low-order CDet on solvable systems -- makes the package genuinely IMPLEMENT the method rather than only validate an
  engine -- but NOT a sign-problem contribution (deterministic, low-order; the high-order MC sampler in the strong-U/
  low-T/doped regime past the complex-U poles is Tier 2+ and unbuilt). cdet_connected.py (3-gate PASS) + `cdet connected`
  + CDET_CONNECTED_v179_RESULT.md. Frozen engine untouched.

- UX POLISH FROM A BLIND-USER REVIEW (v180): a reviewer drove the CLI as a new user (praised the unified ./cdet, rich
  output, validate dashboard, converge to 100x100, the shell) and flagged concrete gaps. Addressed each: (1) bare
  `cdet run` now works -- the upper beta auto-resolves to one bstep above --beta, with a "customize:" line showing the
  full invocation (was: printed beta None and failed); (2) `cdet sweep` prints per-point progress [i/n] var=... via a new
  progress hook in cdet_study.study(); (3) worked-examples epilogs added to run/sweep/lab --help; (4) shell synonyms
  added (number density, occupancy, doublons, cdet, ...) and the "couldn't tell" message now points to `examples`/`help`;
  (5) README gained a "Try this first" block + an explicit note that the numbered folders are internals behind ./cdet.
  Verified unchanged: validate 5/5, frozen 194/194, surrogate 3.55e-15, converge still 100x100, shell paths work. HONEST
  SCOPE: interface polish only -- nicer to drive, but does not change what the tool computes or its standing as a
  validated pedagogical CDet that reproduces known physics. UX_POLISH_v180_RESULT.md + csurrogate v180 note.

- A LOCAL BROWSER GUI WITH SLIDERS + QUICK RUNS (v181): Paul asked for quick runs (fast defaults of the most-used items)
  with easy slider customization and a GUI. Built `cdet gui` -- a stdlib-http (no new deps) single-page console served
  at 127.0.0.1: a slider rail (N, U, mu, beta, L) + one-click quick-run cards (equation of state, double occupancy,
  susceptibilities, convergence wall, true radius, free propagator L->inf, validate), each with an instrument-style
  monospace readout and a small SVG trace; a Live toggle re-runs cards on slider movement. Design grounded in the subject
  (a numerical instrument): dark console, tabular mono readouts, teal oscilloscope traces, amber threshold lines for the
  two physical limits (the RPA wall and the true radius). Backend endpoints call the SAME functions as the CLI (eos/docc/
  chi/wall/trueradius + a plane-wave propagator + a validate subprocess). VERIFIED by starting the server, curling every
  endpoint (eos 0.3716, docc 0.2933, kappa 0.1826/chi_s 0.2853, wall 1.9752, radius 1.5723 Im=pi/beta, propagator 0.19944
  = converge TD limit, validate 5/5), 404 on unknown routes, balanced HTML, every card maps to a route; launches from
  both `cdet gui` and `python3 cdet_gui.py`. SCOPE: front-end over existing computation -- one-click most-used items with
  slider customization; no new physics, nothing the tool computes changes. cdet_gui.py + `cdet gui [--port][--no-browser]`
  + CDET_GUI_v181_RESULT.md. Frozen engine untouched (194/194).

- GUI CSV DOWNLOAD + COPY-AS-CLI (v182): the two follow-ups I'd suggested. (1) CSV: the sweep cards (eos, docc, chi,
  wall, propagator) get a CSV button -> /api/<card>?...&csv=1; the server builds the sweep and formats it with the
  suite's own export._write_csv, so the file matches `cdet export` byte-shape (# name + JSON meta, columns, rows) and is
  served as a real attachment download (cdet_<card>.csv). (2) Copy-as-CLI: every card shows the exact runnable `cdet ...`
  command, live-synced to the sliders, with a copy button (clipboard + textarea fallback). FAITHFULNESS FIX: so the
  eos/docc/chi commands reproduce exactly, those cards now compute at the suite reference (mu=1,beta=2) like the CLI
  (their "uses" tags shrank to N U), and the global mu/beta sliders drive only the lattice cards (wall/trueradius/
  propagator) where the CLI does take --beta --mu. VERIFIED: CSV returns export-formatted text + attachment headers for
  all 5 sweep cards; bare eos=0.437896 matches the CLI; the copied commands RUN (cdet eos --N 4 --U 1 -> 0.4379, cdet
  trueradius --beta 2 --mu 0.5 -> 1.5723, cdet wall --beta 5 --mu 0 reproduces the wall sweep). Front-end only; no new
  physics. cdet_gui.py + CDET_GUI_CSV_CLI_v182_RESULT.md. Frozen engine untouched.

- GUI RECENT-RUNS MEMORY + HIGH-N HANG FIX (v183): added the suggested "recent runs" strip -- a server-side ring buffer
  (cap 8) of explicit runs shown as chips above the cards (card id + slider values + result; amber value for the limit
  cards), click a chip to restore those sliders and re-run, a clear link. Only explicit Run clicks are remembered (Run
  sends &log=1; Live auto-reruns on slider drag do NOT), consecutive identical configs dedupe. New meta-endpoints
  /api/_recent and /api/_clear; survives page refresh within the session. FOUND+FIXED A REAL v181 BUG while testing: the
  sweep cards rebuilt their trace via repeated 2-site ED, which scales steeply with N -- instant to N=4 (0.09s), 3.3s at
  N=5, hangs at N>=6 -- so with the N slider going to 8 a single eos/docc/chi click could wedge the request for a minute
  (this is what made an earlier test appear to hang the shell). Fixed by capping the GUI N slider at 4 (every run
  sub-second) + trimming sweeps to 11 points + server-side clamp N<=4; larger SU(N) stays available via each card's
  copy-as-CLI command (cached-series path), with a rail hint. VERIFIED: 3 explicit runs recorded most-recent-first,
  repeat dedupes, unlogged live rerun not recorded, clear empties, page wired; routes sub-second even when N requested
  high (clamped). Front-end only; no new physics. cdet_gui.py + CDET_GUI_RECENT_v183_RESULT.md. Frozen engine untouched.

- GUI REBUILT AS A THIN WRAPPER OVER THE CLI (v184, Paul's correction): Paul pushed back that the GUI had drifted into a
  PARALLEL implementation -- a particular calc done by the GUI while everything else is commands -- and that it should
  "literally do what the console would do before manually," sliders just plugging into the existing command flags, never
  changing any calculations. He was right: v181-183 had the GUI calling physics functions directly (density_ed/wall/...),
  which forced the mu=1/beta=2 hardcoding, the N cap, and GUI-side sweeps/CSV. REBUILT cdet_gui.py to import NO physics
  (stdlib only): every card is a real `cdet` subcommand, its controls are that subcommand's actual flags (slider per
  number, dropdown per choice), and Run executes `python3 cdet.py <subcommand> <flags>` via subprocess and shows its real
  ANSI-stripped output. EVERY subcommand is a card (validate/converge/connected/crosscheck/eos/docc/chi/resum/wall/tide/
  primes/twist/trueradius/run with --L and the beta range/sweep/export) -- nothing GUI-only, nothing reimplemented. No
  caps, no hardcoded params: whatever you set goes straight to the command; slow is slow exactly as the CLI is. copy gives
  the exact command; recent lists real commands; clicking restores controls + re-runs. INJECTION-SAFE: list-argv
  subprocess (never a shell), allow-listed subcommands only, every value cast/validated (beta=5;rm -rf / is rejected, not
  run -- verified). VERIFIED: eos card runs `cdet eos --N 4 --U 1.0 --K 10` returning its real table; wall/trueradius
  likewise; injection rejected; unknown command refused; recent records real commands; core cmd_eos/docc/chi never changed
  and identical. cdet_gui.py + CDET_GUI_WRAPPER_v184_RESULT.md. Frozen engine untouched (194/194).

- OPTIONAL SELF-CONTAINED HELP ASSISTANT (v185): Paul asked for an optional toggle-on chatbot in the software to help
  users figure out what to do / the capabilities, alongside the existing docs, and asked whether a free self-contained
  model could be bundled. Gave the honest options (Ollama/GPT4All/llama.cpp would add 2-7GB and be slow on CPU) and
  proposed a rule-based assistant instead, which he approved. Built cdet_assistant.py: a self-contained RULE-BASED
  knowledge graph (NOT an LLM -- no model, no download, no API, offline, instant) of 21 commands (desc/params/example/
  related), 9 physics concepts (sign problem, CDet, the wall/U_c, the true/thermal radius, resummation, Mott, the TD
  limit, the three-model architecture, the parameters) and 6 workflows (getting started, observables, the wall study,
  lattice runs, the method, export), with a keyword matcher that weights specific multi-word phrases over generic ones,
  recognises command names/greetings/'what can you do', and falls back gracefully. Wired into the GUI as a TOGGLE-ON
  slide-in panel (hidden by default -- purely optional, as asked): top-right 'assistant' button, chat bubbles, bot
  replies render light markdown + clickable command chips that copy; /api/assist endpoint calls respond(). It complements
  the docs and runs NOTHING. VERIFIED: the module's 10-query self-test passes (start/wall/CDet/double-occupancy/true
  radius/parameters/bare command/export/capabilities/nonsense fallback), every command example is real, /api/assist
  returns sensible answers with relevant chips through the server, and the panel is hidden until toggled. GUI stays a pure
  CLI wrapper; the assistant adds no physics. cdet_assistant.py + panel in cdet_gui.py + CDET_ASSISTANT_v185_RESULT.md.
  Frozen engine untouched (194/194).

- ASSISTANT UPGRADED WITH CHATBOT BEST PRACTICES (v186): Paul asked me to research how chatbots are built and improve the
  assistant. Web-searched production help-bot practices (intent matching, graceful fallback, fuzzy/typo tolerance,
  disambiguation, UX) and applied the established ones, keeping it self-contained/offline/rule-based/runs-nothing (stdlib
  only -- difflib, math, re; no model, no inference). Rewrote the matcher: idf term-importance scoring over a unified pool
  of commands+concepts+workflows (distinctive words outweigh common ones; stopwords dropped; multi-word phrases bonused);
  difflib typo tolerance + light stemming (started->start); confidence gating with **disambiguation** ("Did you mean X or
  Y?") instead of guessing; **closest-match fallback** that surfaces nearest topics instead of a generic miss; action-verb
  vs definitional **intent signals** (compute->command, "what is"->concept); a **forward path** on every reply via tappable
  quick-reply suggestions; and lightweight **follow-up** via a threaded ctx topic ("tell me more"/"an example"/"parameters").
  respond() now returns {reply, commands, suggestions, topic}. GUI wired to render suggestion quick-replies and thread ctx;
  welcome offers starters. Self-test extended to 10 query + 6 behaviour checks, all pass. SCOPE: a better help layer grounded
  in cited best practices -- NOT a language model and NOT any change to physics; assistant still imports no physics and runs
  nothing, GUI still the pure wrapper, frozen engine untouched (194/194). cdet_assistant.py + cdet_gui.py +
  CDET_ASSISTANT_UPGRADE_v186_RESULT.md.

- BLIND STUDENT TEST + ONBOARDING FIXES (v187): Paul asked me to blind-test installing/using cdet as a first-year student
  learning lattice work. Did it from a clean unzip, README/QUICKSTART only, following the on-ramp literally. The CLI
  on-ramp is genuinely good (make CC=gcc test 194/194; ./cdet validate 5/5; ./cdet converge clear TD table; bare
  ./cdet eos/wall/docc all run flagless and end with a plain-language takeaway). Found real friction and fixed it:
  (1) QUICKSTART contradicted the README's ./cdet front door -- step 1 said `make test` (no CC=gcc), never mentioned
  ./cdet or the GUI/assistant, and steered the student into low-level cdet_lab.py/cdet_shell.py + a researcher-only
  "What to show Moller" section; added a "Start here (friendly on-ramp)" block at the top (the four ./cdet commands +
  assistant + bare-command tip + CC=gcc note) and relabeled Moller "(Researchers)". (2) The assistant whiffed on genuine
  beginner questions -- "what should I run first" -> the HEAVY cdet run (word "run" collision); "what is the hubbard model"
  -> the three-MODEL architecture; "what is a lattice/exact diagonalization/monte carlo" -> no concept; "I'm a first year /
  what do I do / I don't understand" -> disambiguation instead of the on-ramp. Added a beginner-SOS intent (new/lost ->
  getting-started directly, no flags) and four foundational concepts (lattice, Hubbard model, exact diagonalization, Monte
  Carlo) that orient a novice and point to the right command; these also fix the collisions. (3) Refreshed a stale cdet
  info gui row. VERIFIED live via /api/assist; specific-term answers unchanged (no regressions); assistant self-test grew
  to 14 query + 6 behaviour checks, all pass; 13 concepts. SCOPE: docs/help only -- no physics changed, assistant still
  offline and runs nothing, GUI still the pure wrapper, frozen engine untouched (194/194). cdet_assistant.py + QUICKSTART.md
  + cdet.py + BLIND_TEST_v187_RESULT.md.

- BLIND EXPERT TEST (MOLLER) + BENCHMARK SURFACING (v188): Paul asked me to re-run the blind test as Gunnar Moller starting
  from scratch, wanting to test capabilities and run benchmarks. Did it cold (fresh unzip, docs only) from a skeptical
  expert lens. Everything named for him VERIFIES and stays honest: make test 194/194; make bench/bench_qss = 12655x speedup
  at n=2048 with 1e-13 agreement, linear to 1M; fast_minors.py O(2^n n^2) connected determinant = 3e-15 vs the engine
  (the CoS/CDet-fast claim); self_energy_irreducible.py shows R_Sigma~R_G and KEEPS the v136 radius overclaim retracted
  (advantage = efficiency/variance); physical_mapping (z=addition pole), consolidation_v138 (three paths agree), cdet_lab
  validate+list (control plane), resum (conformal-Borel vs Pade), the size-axis oracles (build_oracles.sh self-contained;
  val2d 3.4e-9; locality decay to 2e-11), and cv.py MC control variate ~70-80x matching 1/(1-rho^2). FRICTION FOUND:
  (1) benchmarks were scattered (make bench, cv.py, fast_minors.py, oracles) with no front door -- `./cdet --help` didn't
  surface them. Added a `cdet bench` subcommand (runs the headline engine benchmark + prints a reproducible index of the
  rest), surfaced in cdet info, README, the QUICKSTART on-ramp, the GUI (a bench card), and the assistant (a bench command
  + a 'benchmarks' workflow + a benchmark intent so 'run benchmarks' routes there instead of colliding with `cdet run`).
  (2) the 'What to show Moller' section read like internal lab notes (v137, 'v136 RETRACTED') -- reworded self-contained.
  HONEST GAP stated plainly: capabilities are a verified engine + deterministic low-order CDet (fast-minors) + control-
  variate MC variance reduction + analysis modules; there is NO production Rossi-style DiagMC sampler at high order in the
  doped/strong-coupling regime (the head-to-head an expert would want vs a CoS run) -- Tier 2, unbuilt, and the README's
  honest bottom line already says the sign axis is the NP-hard wall. VERIFIED: cdet bench runs (engine table + index); GUI
  bench card runs the real command; assistant routes benchmark/performance/capability queries to the suite; self-test 14
  query + 6 behaviour checks pass (22 commands, 7 workflows). SCOPE: interface/docs only -- no physics changed, frozen
  engine untouched (194/194). cdet.py + cdet_gui.py + cdet_assistant.py + QUICKSTART.md + README.md +
  MOLLER_BLIND_TEST_v188_RESULT.md.

- CONNECTED-DETERMINANT MONTE CARLO SAMPLER (v189): the v188 expert test flagged that the package described diagrammatic
  Monte Carlo but did not contain it. Paul: "let's add that." Built cdet_diagmc.py -- a real Rossi-style connected-
  determinant Monte Carlo that reuses the validated cdet_connected kernel (same code path as the deterministic series).
  Two estimators: (A) an importance-sampled per-order MC integrator of a_n with error bars, (B) a grand-canonical
  Metropolis walker (insert/remove/shift over diagram order + times), anchored on n=1, reproducing ln(Z/Z0). Both VALIDATED
  vs exact within error bars (atom 0 sigma; 2-site within error; summed observable vs exact partial sum dev 1e-16; walk vs
  exact partial sum dev <0.03, chain mean sign 0.54). TWO HONEST FINDINGS shaped it: (1) det(M)^2 is positive so the small
  solvable clusters are essentially sign-free WITHIN an order (intra-order <sign>~1) -- did not fabricate one; (2) the real
  measurable sign problem here is the ACROSS-ORDER alternating series <s>=|sum a_n U^n|/sum|a_n|U^n, which collapses toward
  the convergence radius (atom beta=2: <s> 0.75->0.36->0.18->0.007 as U 0.3->1->1.5->2; cost ~1/<s>^2 to ~1e4) -- the same
  object as the bare-series radius the rest of the package studies. SCOPE STATED PLAINLY: it does NOT defeat the sign
  problem (NP-hard); it exhibits it. Order bounded by 2^n; validated on atom+2-site; a large-lattice high-order production
  sampler remains future work -- but the package now actually contains the MC method it is named for. Made the self-test
  fast enough to gate (49s; trimmed sample/step counts; the atom is near-zero-variance). Wired into cdet diagmc (with an
  ASCII sign-wall plot), cdet info, the GUI (a sign-wall card via the pure wrapper), and the assistant (a diagmc command +
  a sampler routing intent so 'run the monte carlo sampler' no longer collides with `run`). Updated README (a DiagMC
  subsection), QUICKSTART, INDEX. Frozen reference engine untouched (194/194). cdet_diagmc.py + cdet.py + cdet_gui.py +
  cdet_assistant.py + README.md + QUICKSTART.md + CDET_DIAGMC_v189_RESULT.md.

- BLIND INTERMEDIATE-STUDENT TEST + SWEEP FIX (v190): Paul asked for a blind test as an intermediate student: get the zip,
  unpack, install, use the program. Did it cold. The install/use surface is good (pip install -e + the cdet console script
  work; export writes CSV, plot writes PNG, diagmc runs, each reporting its output path). Found+fixed a REAL CRASH: `cdet
  sweep --target eos --var U --values 0.5 1 1.5` raised TypeError "'str' object is not a mapping" -- cmd_sweep passed the
  --base flag string ("L") into cdet_study.study() where `base` must be a dict of fixed params, so `{**base, var: x}` blew
  up; a natural intermediate task (sweep an observable over U) was broken in BOTH the CLI and the GUI sweep card. Fixed by
  passing an empty base dict (evaluate() already supplies beta/mu/U defaults); verified across targets (eos, double-occ)
  and via the GUI. Also: the README's lead install step `pip install -e ".[all]"` fails on Ubuntu 24 with PEP 668
  externally-managed-environment -- added a venv / --break-system-packages note and the reminder that python3 cdet.py works
  with no install. Minor: surfaced that `cdet export <dataset>` takes a positional (convergence/resummation/eos/docc/chi)
  in cdet info / README / assistant. A genuine bug fix + install-doc fix; no physics changed; frozen engine untouched
  (194/194). cdet.py + README.md + cdet_assistant.py + BLIND_TEST_INTERMEDIATE_v190_RESULT.md.

- ADVERSARIAL CHAOS CONSOLE TEST + HARDENING (v191): Paul asked for a blind test trying to break the console "like an ADHD
  cat on the keyboard or a kid trying every way to screw it up." Hammered the CLI and GUI with garbage subcommands,
  unicode/emoji, keyboard mash, missing/typo'd flag values, shell-injection payloads, and absurd numbers. MOST OF IT WAS
  ALREADY SAFE: argparse rejects unknown subcommands/choices/bad numeric values cleanly (exit 2, no traceback); injection is
  inert because the CLI never spawns a shell and both the CLI (type=float) and GUI (per-flag casters + allow-list) reject
  `1;rm -rf /`, `$(whoami)`, backticks as invalid numbers; the GUI returns clean JSON errors ({"error": "--U expects a
  number"}, {"error": "unknown command: hackme"}) with nothing executed (verified /tmp marker survived). REAL BUGS FOUND +
  FIXED (cdet.py only): (1) `diagmc --nmax 99999` HUNG -- each order runs the ~2^n connected-determinant recursion, a
  self-DoS; now --nmax capped at 8 (note) / floored at 1; (2) `sweep --values $(seq 1 500)` HUNG; now the point list is
  capped at 60 (note) and the sweep carries a 120s time budget so it stops gracefully with a recorded reason; (3)
  `diagmc --samples 0` / `--nmax 0` produced nan (empty-set average); now --samples floored at 100, --nmax at 1; (4)
  `diagmc --beta nan|inf`, `--U inf`, `--beta 0` silently produced garbage; now a clean "must be finite" / "beta must be
  positive" error. NOTED (not bugs): `plot --out` treats the path as an output directory; argparse rejects negative
  scientific notation as a bare value (--mu -1e5; use --mu=-1e5). Normal use unchanged; no physics; frozen engine untouched
  (194/194). cdet.py + CHAOS_TEST_v191_RESULT.md.

- BLIND LIFECYCLE TEST + INTERRUPTION RESILIENCE (v192): Paul asked for a blind test as a user exiting, switching off,
  restarting, walking away for ages, resuming, with impatient retries mid-process -- how does it handle every pause /
  restart / interrupted process. Used it that way. MUCH WAS ALREADY ROBUST: Ctrl-C (SIGINT) on any CLI command prints a
  clean "interrupted." (exit 130) via the top-level handler, no traceback; the browser console is stateless per request so
  walking away and coming back works and it stops cleanly on Ctrl-C; and the SU(N) series cache read already tolerates a
  corrupt/half-written file (falls back + recomputes). THREE REAL FRAGILITIES FIXED: (1) an interrupted `cdet sweep` lost
  ALL its work -- data.csv/summary.json were only written after the whole sweep finished and run.log was never flushed, so
  Ctrl-C/kill/sleep discarded every computed point. Now data.csv is written+flushed point-by-point, the log flushes per
  line, and KeyboardInterrupt is caught so the run still finalizes summary.json with a clear stop reason ("interrupted by
  user (Ctrl-C) after k of n points"); verified that interrupting a 6-point sweep after 1 point keeps that point in
  data.csv. (2) restarting the console while the old one was still bound dumped an OSError [Errno 98] Address already in use
  traceback (a common "did I already start it?" mistake) -- now serve() probes the requested port and the next nine, opens
  on the first free one with a note ("port N was busy ... using N+1 instead"), or prints a friendly all-busy message. (3)
  the cache write was not atomic -- now temp-file + os.replace so an interrupt can neither corrupt nor lose the cache. No
  physics changed; frozen engine untouched (194/194). cdet_study.py + cdet_gui.py + cdet.py + LIFECYCLE_TEST_v192_RESULT.md.

### #177 -- Packaging and CI (v167)

Continued the elevation checklist at items #4/#6 (distribution / commercial readiness). ADDED pyproject.toml: the
project installs with `pip install -e .` and exposes a real `cdet` console command via the entry point cdet:main
(verified the installed command runs `cdet validate` from outside the repo -> 5/5 gates). Runtime dependencies are
numpy+mpmath; optional extras [viz]=matplotlib and [rich]=rich (so the core stays light). MIT LICENSE added (declared
in pyproject). GitHub Actions CI (.github/workflows/ci.yml) on python 3.9/3.11/3.12: installs the package, builds the
FROZEN reference engine and runs its 194/194 gate (the parity anchor), then runs `cdet validate` (frozen + surrogate +
hybrid 0.00e+00 + 2D plane-wave + consolidation), the physics-module self-tests (double_occupancy, susceptibilities,
plots, sun_eos_conformal, two_particle_run, consolidation_v161), and the CLI self-test -- enforcing the whole
validation depth on every push. packaging_check.py is the gate for the scaffolding (parses pyproject, checks the entry
point resolves, the CI runs the frozen gate + cdet validate, and LICENSE exists). README quickstart now leads with the
pip-install path. Frozen engine untouched (194/194). pyproject.toml + .github/workflows/ci.yml + LICENSE +
packaging_check.py (self-test gate PASS); csurrogate_params.h v167 note. cdet_suite.egg-info is an install artifact (not
shipped). Remaining roadmap: python bindings, streaming/high-order, docker.

### #179 -- Data export to CSV/JSON/HDF5 (v169)

Continued the checklist at item #3 (export formats for easy integration). ADDED export.py: every validated observable
becomes a downloadable dataset -- convergence (TD limit), resummation (conformal-Borel vs Pade), eos (SU(N) density),
docc (double occupancy + interaction energy), chi (charge compressibility + spin susceptibility) -- each reproduced
from the SAME code paths the gates validate, so an exported file cannot drift from the numbers (same discipline as the
v166 figures). Three formats: CSV and JSON via the standard library (always available); HDF5 optional via h5py. Each
dataset carries its column names and metadata (N, beta, mu, observable). The self-test round-trips every dataset: write
CSV/JSON (+HDF5 when h5py is present), read back, assert the numeric rows match the source exactly. Wired into the CLI
as `cdet export [convergence|resummation|eos|docc|chi] [--format csv|json|hdf5|all] [--out dir]`. pyproject.toml gains
a [hdf5] optional extra (h5py), added to [all]. Frozen engine untouched (194/194). export.py (self-test gate PASS) +
cdet.py export subcommand; csurrogate_params.h v169 note. cdet_data/ is a runtime artifact (not shipped). Remaining
roadmap: streaming/high-order, docker.

### #180 -- Native pybind11 bindings (v170)

Took the heavier roadmap item: native bindings to eliminate subprocess overhead for programmatic use. ADDED bindings/
-- cdet_core.cpp, a pybind11 module wrapping the FROZEN reference engine's C primitives (G0_atom, G_exact_atom,
density_exact, n_F) and the 2D plane-wave free propagator (square2d_g0). The engine is used READ-ONLY (its source is
untouched); the binding #includes the frozen headers under extern "C" and links the unmodified cdet_engine.c +
lattices.c objects, so the wrapped functions ARE the frozen functions -> results are BIT-IDENTICAL to the 194/194
engine. The gate (bindings_check.py) proves it three ways: (1) it builds; (2) native G0_atom == a freshly-compiled
frozen-C G0_atom to 0.0e+00 over several args, and native square2d_g0 (L=16 NN) matches the validated plane-wave value;
(3) benchmark -- native call ~120 ns vs ~232 ms for one compile+subprocess, i.e. ~2e6x overhead removed per engine
access, so programmatic loops over the engine are now native instead of paying a process spawn each time. Kept it
OPT-IN: bindings/build.py compiles the extension on demand, so the default `pip install -e .` stays pure-python and
compiler-free; pyproject gains a [bindings] extra (pybind11), the README documents the build, and CI adds an optional
step that builds the bindings and runs the gate. The platform-specific compiled .so is NOT shipped -- the source
(cdet_core.cpp, build.py, bindings_check.py) ships and is rebuilt on the target. Frozen engine untouched (194/194).
bindings/cdet_core.cpp + build.py + bindings_check.py (gate PASS); pyproject [bindings] extra; CI step; README note;
csurrogate_params.h v170 note. Remaining roadmap: streaming/high-order.

### #181 -- Docker one-command deployment (v171)

Completed the elevation checklist's last packaging item: a Docker image. ADDED Dockerfile -- python:3.12-slim base,
apt-installs gcc/g++/make for the frozen C engine and the optional native bindings, COPY the repo, `pip install -e
".[all]"` (rich + matplotlib + h5py extras), then `cd engine && make CC=gcc test` so the IMAGE WILL NOT BUILD unless
the frozen engine passes 194/194 (validation baked into the build). ENTRYPOINT is the unified `cdet` CLI with default
CMD `validate`, so `docker run --rm cdet-suite` runs all gates and `docker run --rm cdet-suite <subcommand>` runs any
capability. Added .dockerignore (excludes __pycache__, *.so, *.egg-info, cdet_figures, cdet_data, caches). docker_check.py
gates the recipe (base image, gcc/g++, COPY+install, the baked `make test`, ENTRYPOINT/CMD, and the .dockerignore
exclusions) and cross-references that each build command is a real project gate. CI gains a `docker` job that builds
the image and runs `cdet validate` in the container (executes on GitHub, where a Docker daemon is available). HONEST
caveat (stated in the gate and the ledger): `docker build` is NOT run in this build/test sandbox -- there is no Docker
daemon -- so the gate validates the recipe structurally and confirms every command it runs (pip install, make test ->
194/194, cdet validate -> 5/5) works natively and is covered by its own gate. Frozen engine untouched (194/194).
Dockerfile + .dockerignore + docker_check.py (self-test gate PASS) + CI docker job + README section; csurrogate_params.h
v171 note. The elevation checklist (unified CLI, cross-checked observables, figures, data export, packaging/CI, dual
license, native bindings, docker) is now complete; remaining deeper-physics roadmap: streaming/high-order orders.

### #182 -- The convergence wall vs lattice size: where lattice size helps (v172)

Took Paul's pivot head-on: attack the convergence WALL with the new large-L machinery and find where lattice size HELPS
the order axis. The wall (finite radius of the bare-U series) has, as its leading weak-coupling cause, the RPA/Stoner
instability: the particle-hole bubble chi(q)=chi0/(1-U chi0) is geometric in U and diverges at U_c(L)=1/max_q chi0(q,L),
with chi0 the free static Lindhard susceptibility from the lattice dispersion eps_k=-2t(cos kx+cos ky) -- the v162
plane-wave physics. Because chi0 needs only the O(L) dispersion (no eigenvectors), U_c(L) is computable at ANY size to
100x100 (~2s), which is exactly what let us watch the wall move with L for the first time. FINDING: the wall is a
thermodynamic-limit quantity and the small-lattice wall is a finite-size artifact. At half-filling (nesting channel
q=(pi,pi), which dominates the Hubbard model) the small lattice is spuriously pessimistic: U_c=1.64 at 4x4 but 1.975 in
the TD limit (~20% further out). Growing the lattice pushes the wall back -- lattice size helps; the bare series
converges further than any small lattice reveals. Reported honestly: the effect is filling-dependent (at incommensurate
doping mu=-0.6 the coarse grid misses the peak so the small lattice is instead optimistic, 4.37 -> 3.30), and U_c is the
leading real-axis instability (validated as the exact bubble-sum radius) while the full radius can be set by complex-U
structure closer than this (v146). I deliberately did NOT force the headline: I first chased the exact many-body Fisher
zero (ED, ring) and found it noisy/estimator-dependent and ED-limited, so I pivoted to the physically-clean leading
instability that the new feature makes computable at scale. Five pre-registered gates all pass: chi0(0)=DOS sum rule
(0.0e+00); vectorized chi0 == brute-force O(L^4) (3.3e-16); bubble-series radius == 1/chi0max; U_c(64) vs U_c(96)
converged (1e-9); half-filling wall recedes with L. Frozen reference engine untouched (194/194). wall_vs_size.py
(self-test gate PASS) + `cdet wall` subcommand + WALL_VS_SIZE_v172_RESULT.md; csurrogate_params.h v172 note. Remaining
deeper-physics roadmap: streaming/high-order orders; and tightening the wall estimate beyond the leading instability
(the complex-U structure).

### #202 -- Blind lifecycle test: pausing, interrupting, restarting, walking away (v192)

Paul: a blind test as a user exiting, switching off, restarting, walking away for ages, coming back, resuming -- every
stop/start, impatient retries mid-process, interrupted process. Used the program exactly that way: Ctrl-C in the middle of
runs, killing processes, restarting the server while the previous one was still up, idling and returning, and impatiently
re-running. REASSURINGLY, MUCH WAS ALREADY SOUND: SIGINT on any CLI command is caught by the top-level handler and prints a
clean "interrupted." with exit 130 (no KeyboardInterrupt traceback on converge/diagmc/sweep); the browser console holds no
per-session state (each request shells a fresh subprocess), so walking away and coming back just works, and it shuts down
on Ctrl-C with "stopped."; and the on-disk SU(N) series cache already wraps its read in try/except, so a half-written or
corrupt cache file degrades to a recompute rather than crashing later runs. THE TEST FOUND THREE REAL FRAGILITIES, NOW
FIXED. (1) An interrupted `cdet sweep` lost everything it had computed: cdet_study.study() wrote data.csv and summary.json
only after the entire loop finished, and emit() wrote run.log without flushing, so a Ctrl-C (or a kill, or the machine
sleeping) discarded every point already done and even the log of them. Fixed by opening data.csv up front, writing the
header and then each row with an explicit flush as it is computed, flushing run.log on every emit, and wrapping the sweep
loop in try/except KeyboardInterrupt so an interrupt still falls through to the finalizer, which writes summary.json with a
stop_reason of "interrupted by user (Ctrl-C) after k of n points"; verified by interrupting a six-point eos sweep after the
first point completed and confirming that point survives in data.csv with the correct stop reason and a plot.png of the
partial curve. (2) Restarting the console while the old server was still bound to the port dumped a raw OSError [Errno 98]
Address already in use traceback from socketserver -- a very common "did I already close it?" situation; serve() now probes
the requested port and the next nine, binds the first free one and prints "port N was busy (the console may already be
running there); using port N+1 instead", and if all ten are busy prints a friendly message pointing at the likely-running
console and the --port flag instead of crashing. (3) The cache write json.dump(data, open(cache,"w")) truncated the file
before writing, so an interrupt mid-write could leave a corrupt cache (harmless on read, but it destroyed a previously-good
cache and forced a multi-minute recompute for large N); it now writes a temp file and os.replace()s it into place
atomically, so an interrupt can neither corrupt nor lose the cache. Verified normal use is unchanged: a full sweep still
completes and archives data.csv/summary.json/plot.png/run.log, validate is 5/5, crosscheck and --selftest pass, the
assistant self-test passes, the diagmc and surrogate gates pass, and the frozen reference engine is still 194/194 and
untouched. No physics changed. cdet_study.py + cdet_gui.py + cdet.py + csurrogate_params.h v192 +
LIFECYCLE_TEST_v192_RESULT.md.

### #201 -- Adversarial "chaos" console test: break it like a cat on the keyboard (v191)

Paul: another blind test -- "try and break the console as if an ADHD cat running on the keyboard or a kid trying every
possible way to screw it up." Hammered the CLI and GUI blind with garbage subcommands, unicode and emoji, keyboard mash,
missing and typo'd flag values, shell-injection payloads (`1;rm -rf /`, `$(whoami)`, backticks), and absurd numbers (huge,
zero, negative, inf, nan). MOST OF THE SURFACE WAS ALREADY ROBUST, which was reassuring: argparse rejects unknown
subcommands, invalid choices, and non-numeric flag values with clean single-line errors and exit code 2 (no tracebacks);
shell injection is structurally inert because the CLI never invokes a shell and the GUI builds an allow-listed list-argv
with per-flag casters, so `1;rm -rf /tmp` is rejected as an invalid float on both paths and a planted /tmp marker survived;
the GUI answers hostile input with clean JSON errors ({"error":"--U expects a number"}, {"error":"unknown command:
hackme"}) at HTTP 200 with nothing executed. BUT THE CHAOS FOUND FOUR REAL DEFECTS, all fixed in cdet.py: (1) `cdet diagmc
--nmax 99999` HUNG the console -- each diagram order evaluates the ~2^n connected-determinant recursion, so an unbounded
order count is a self-inflicted denial of service; --nmax is now capped at 8 (with a note) and floored at 1. (2) `cdet
sweep` with a huge value list (`--values $(seq 1 500)`) ran until timeout; the point count is now capped at 60 (with a
note) and the sweep carries a 120-second time budget, so it always terminates gracefully with a recorded stop reason
instead of hanging. (3) `cdet diagmc --samples 0` and `--nmax 0` produced nan by averaging an empty sample set; --samples
is floored at 100 and --nmax at 1. (4) `cdet diagmc --beta nan|inf`, `--U inf`, and `--beta 0` silently produced garbage
numbers; they now return a clean "beta, mu and U must be finite numbers" / "beta (inverse temperature) must be positive"
error (which required adding `import math` to cdet.py). NOTED AS NON-BUGS: `cdet plot --out PATH` treats PATH as an output
directory and writes cdet_summary.png inside it (intentional, if mildly surprising); and argparse rejects negative
scientific notation given as a bare value (`--mu -1e5`), which is standard argparse option-prefix behaviour and is avoided
with the equals form `--mu=-1e5`. Verified that normal use is unchanged (diagmc, sweep, validate 5/5, crosscheck, the
frozen 194/194, the surrogate gate all still pass) and that each previously-hanging input now returns in well under a
second with a friendly note. No physics changed; the frozen reference engine is untouched. cdet.py + csurrogate_params.h
v191 + CHAOS_TEST_v191_RESULT.md.

### #200 -- Blind intermediate-student test: install + real use, and a sweep-crash fix (v190)

Paul: run another blind test on getting the zip, unpacking, running the install, and using the program as an intermediate
student. Did it cold from a fresh unzip of v189 as a user who knows the physics basics and wants to install properly and do
real work. THE INSTALL/USE SURFACE IS GOOD: `pip install -e ".[all]" --break-system-packages` installs cleanly and lands
the `cdet` console script on PATH (cdet validate -> 5/5); `cdet export --format csv` writes cdet_data/cdet_docc.csv and
`cdet export eos`/`chi`/`convergence`/`resummation` work via the dataset positional; `cdet plot` writes
cdet_figures/cdet_summary.png; `cdet diagmc` runs and shows the sign wall -- each command reports the path it wrote and
explains the result. TWO REAL FRICTIONS, FIXED: (1) `cdet sweep` CRASHED -- `cdet sweep --target eos --var U --values 0.5
1 1.5` raised TypeError "'str' object is not a mapping". Root cause: cmd_sweep called study(a.target, a.method, a.base, ...)
passing the --base flag (a string defaulting to "L") into cdet_study.study()'s `base` parameter, which must be a DICT of
fixed base parameters -- so the per-point `p = {**base, var: x}` did {**"L", ...} and blew up. This broke a completely
natural intermediate task (sweeping an observable over U) in BOTH the CLI and the GUI sweep card. Fixed by passing an empty
base-params dict {} (evaluate() already supplies its own defaults via p.get("beta",5.0)/p.get("mu",1.0)/p.get("U",1.0)),
verified across targets eos and double-occ and through the GUI sweep card (ok, completed, no error). (2) the README's LEAD
install instruction `pip install -e ".[all]"` fails on a modern Debian/Ubuntu with the PEP 668 externally-managed-
environment error -- a first-contact wall; added a note offering the venv path and `--break-system-packages`, plus the
reminder that `python3 cdet.py <cmd>` / `./cdet <cmd>` need no install at all. MINOR: `cdet export` defaults to the docc
dataset and that you can pass eos/chi/convergence/resummation as a positional was undiscoverable from the surfaces around
it; surfaced it in `cdet info`, the README capabilities line, and the assistant's export entry. SCOPE: a genuine
user-facing bug fix plus an install-doc fix and a discoverability nudge -- no physics changed, the frozen reference engine
is untouched (194/194), and validate/crosscheck/surrogate/frozen all still pass. cdet.py + README.md + cdet_assistant.py +
csurrogate_params.h v190 + BLIND_TEST_INTERMEDIATE_v190_RESULT.md.

### #199 -- A connected-determinant Monte Carlo sampler: the sign wall, measured (v189)

The v188 blind expert test ended on an honest gap: the package described diagrammatic Monte Carlo but did not contain a
production Rossi-style DiagMC sampler. Paul: "well... let's add that then, update the docs and the chatbot." Built
cdet_diagmc.py, a real connected-determinant Monte Carlo, scoped honestly. It samples the connected-determinant series
ln(Z/Z0)=sum_n (-U)^n integral_{simplex} C_n dt using the SAME validated kernel as the deterministic path (imported from
cdet_connected -- one code path for sampler and exact). Two estimators: (A) an importance-sampled per-order Monte-Carlo
integrator returning each coefficient a_n with an error bar and the within-order average sign, and (B) a grand-canonical
Metropolis walker (insert / remove / shift moves over the diagram order and the imaginary times, weight |U|^n|C_n|,
anchored on the n=1 sector to fix the normalization) -- the actual DiagMC chain -- reproducing ln(Z/Z0). DEVELOPMENT WAS
DRIVEN BY VALIDATION and produced two honest findings I kept rather than papered over: (1) the det(M)^2-per-spin weight is
manifestly positive, so on the small exactly-solvable clusters (atom, 2-site, even a triangle ring I probed) there is
essentially NO within-order sign problem (intra-order <sign> ~ 1) -- I did not fabricate a sign decay that is not there;
(2) the genuine, measurable sign problem in this formulation is the ACROSS-ORDER alternating series, <s> = |sum a_n U^n| /
sum |a_n| U^n, which collapses toward zero as U approaches the convergence radius -- measured on the atom at beta=2 as <s>
falling 0.75 -> 0.56 -> 0.36 -> 0.18 -> 0.007 across U = 0.3, 0.6, 1.0, 1.5, 2.0, with the cost to a fixed error ~ 1/<s>^2
rising to ~10^4 -- which is the SAME object as the bare-series convergence radius the wall-physics suite already studies.
VALIDATION (all in the self-test, made fast enough to gate at ~49s by trimming sample/step counts since the atom is
near-zero-variance): per-order MC coefficients vs the exact deterministic coefficients (atom, 0 sigma; 2-site n=2 within
error bars); the summed observable vs the exact partial sum (dev 5.5e-17, with the gap to the closed form correctly
attributed to series truncation, not MC error); the Metropolis walk vs the exact partial sum (dev <0.03, chain mean sign
0.54 -- the walk DOES see a sign <1 because it samples across orders); and the across-order sign wall asserted to collapse
with U. SCOPE, STATED PLAINLY: this does NOT defeat the sign problem -- that wall is Troyer-Wiese / NP-hard -- it exhibits
and quantifies it; the reachable order is bounded by the 2^n connected-determinant cost; validation is on the small
solvable systems; a large-lattice, high-order production sampler is still future work. But the package now actually
contains, and validates, the Monte-Carlo method it is named for. WIRED IN: cdet diagmc (a CLI command with flags
--system/--beta/--mu/--U/--nmax/--samples and an ASCII sign-wall plot), a row in cdet info, a GUI sign-wall card through
the same pure CLI wrapper, and the assistant (a diagmc command entry, the sign-problem/monte-carlo concepts pointing to it,
and a sampler routing intent so "run the monte carlo sampler" routes to diagmc instead of colliding with the run command).
Updated README (a "Diagrammatic Monte Carlo: the sign wall, measured" subsection with honest scope), QUICKSTART (the
on-ramp), and INDEX. Assistant self-test now 16 query + 6 behaviour checks (23 commands). Frozen reference engine untouched
(194/194). cdet_diagmc.py + cdet.py + cdet_gui.py + cdet_assistant.py + README.md + QUICKSTART.md + INDEX.md +
CDET_DIAGMC_v189_RESULT.md + csurrogate_params.h v189.

### #198 -- Blind expert test (Gunnar Moller) + benchmark surfacing (v188)

Paul: re-run the blind test as Gunnar Moller starting from scratch, wanting to test capabilities and run benchmarks. I did
it cold from the opposite end of the first-year test -- a skeptical domain expert (the researcher whose three papers
motivated the integration program), fresh unzip, README/QUICKSTART only, trying to verify the claims and get benchmark
numbers. EVERYTHING NAMED FOR HIM VERIFIES AND STAYS HONEST: `cd engine && make test` -> 194/194 and `make fast`
re-verifies; `make bench`/`./bench_qss` -> the connected-determinant evaluation vs a dense-LU cross-check, 12655x speedup
at n=2048, agreement ~1e-13, linear scaling to 1,048,576; `fast_minors.py` -> the connected determinant in O(2^n n^2),
verified term-by-term against the engine to 3e-15 (the CoS / CDet-fast decomposition his group uses); `self_energy.py` +
`self_energy_irreducible.py` -> eps+ReSigma ED-verified and exact 1PI coefficients, with the honest finding that
R_Sigma ~ R_G (no radius advantage) and the earlier 1.76 overclaim KEPT RETRACTED, the Simkovic-Kozik edge attributed to
efficiency/MC variance; `physical_mapping.py` (z(inf) = addition pole to 4e-7), `consolidation_v138.py` (three paths
agree), `cdet_lab.py validate` + `list` (the full target x method control plane, swap solver/observable, benchmark vs ED),
`./cdet resum` (conformal-Borel vs Pade with the improvement column), the size-axis oracles (`./build_oracles.sh` builds
self-contained in place -> `val2d.py` 2D torus vs numpy = 3.4e-9 MATCH; `locality.py` exponential decay ratio to 2e-11),
and the Monte-Carlo control-variate benchmark (`02_control_variate/cv.py` -> ~70-80x variance reduction matching theory
1/(1-rho^2) = 71x). So the capabilities are real, cross-checked, and the negatives are kept -- an expert would trust it.
FRICTION FOUND AND FIXED: (1) the benchmarks were scattered across `make bench`, `cv.py`, `fast_minors.py`, and the oracle
scripts with NO front-door entry -- an expert asking "how do I run benchmarks" had to discover them folder by folder, and
`./cdet --help` did not surface them. Added a `cdet bench` subcommand that runs the headline engine speedup benchmark and
then prints a reproducible index of the rest (MC variance, the O(2^n n^2) fast-minors verification, the size-axis locality
and 2D benchmarks, with the one-time build_oracles.sh note); surfaced it in `cdet info`, the README subcommand list, the
QUICKSTART friendly on-ramp, the GUI (a no-flag bench card through the same pure wrapper), and the assistant (a `bench`
command entry + a "benchmarks" workflow + an explicit benchmark intent so "run benchmarks"/"performance"/"benchmark the
engine" route to the suite instead of colliding with the `run` command). (2) The QUICKSTART "What to show Moller" section
read like internal lab notes (internal version numbers, "v136 RETRACTED") -- reworded to be self-contained, with plain
statements (R_Sigma ~ R_G on the atom; the advantage is efficiency and MC variance; strong coupling needs resummation) an
external reader can follow, plus a `./cdet bench` pointer in the on-ramp. THE HONEST GAP, STATED PLAINLY (not a quick fix):
the capabilities are a verified reference engine + deterministic low-order CDet (fast-minors) + control-variate MC variance
reduction + analysis modules; there is NO production Rossi-style DiagMC sampler running at high order in the doped /
strong-coupling regime -- the head-to-head an expert would actually want to benchmark against a CoS production run. The
README's honest bottom line already says the sign axis is the real, Troyer-Wiese / NP-hard wall and Tier 2 (the full MC
sampler) is unbuilt; the right thing for an expert is to say so rather than imply a competitive sampler exists. VERIFIED:
`cdet bench` runs (engine table + index); the GUI bench card runs the real `cdet bench`; the assistant routes
benchmark/performance/capability queries to the suite; the assistant self-test (14 query + 6 behaviour checks) passes with
22 commands and 7 workflows. SCOPE: interface and docs only -- no physics changed, the assistant still runs nothing, the
GUI is still the pure CLI wrapper, and the frozen reference engine is untouched (194/194). cdet.py + cdet_gui.py +
cdet_assistant.py + QUICKSTART.md + README.md + MOLLER_BLIND_TEST_v188_RESULT.md + csurrogate_params.h v188.

### #197 -- Blind usability test as a first-year student (v187)

Paul: blind-test installing and using cdet as a student learning lattice work in their first year. I unzipped the package
fresh into a clean dir and used ONLY what a new user sees -- README, QUICKSTART -- following the on-ramp literally, with no
insider knowledge of module layout or flags, to surface real onboarding friction. WHAT WORKS (a student succeeds): the
README "Try this first" block is a clean four-command on-ramp; `cd engine && make CC=gcc test` -> 194/194; `./cdet validate`
-> a 5/5 rich dashboard; `./cdet converge` -> a clear 4x4..100x100 thermodynamic-limit table with a plain-language takeaway
("past ~12-16 sites the value is already the infinite-system result"); and bare `./cdet eos`, `./cdet wall`, `./cdet docc`
all run with NO flags, each ending in a one-line physics explanation -- good for learning. FRICTION FOUND AND FIXED:
(1) QUICKSTART contradicted the README's front door. README front-doors `./cdet` (validate/converge/gui + the assistant);
QUICKSTART step 1 said `make test` (no CC=gcc), never mentioned `./cdet` or the GUI/assistant anywhere in its early steps,
and instead steered the student into the low-level cdet_lab.py / cdet_shell.py scripts inside 08_2d_interacting plus a
researcher-only "What to show Moller" section -- so a first-year following QUICKSTART would miss the polished front door
entirely. Fixed by inserting a "Start here (the friendly on-ramp)" block at the very top of QUICKSTART (the four ./cdet
commands, the assistant toggle, the bare-command tip, and the `CC=gcc` fallback note) and relabeling the Moller section
"(Researchers)". (2) The assistant -- strong on specific cdet terms (beta -> parameters; wall -> cdet wall) -- failed the
naive questions a real first-year asks: "what should I run first" returned the HEAVY production `cdet run --L 16 --beta 10
--beta-hi 40` (the word "run" collided with the command); "what is the hubbard model" returned the three-MODEL ARCHITECTURE
concept (keyword "model" collision); "what is a lattice", "what is exact diagonalization", "what is monte carlo" had no
foundational concept and produced confusing matches; and "I'm a first year, what do I do", "I don't understand any of this"
bounced to a disambiguation instead of just handing over the on-ramp. Fixed by (a) a beginner-SOS intent placed before the
scorer -- new / lost / "what do I do" / "what should I run first" / "where do I start" / "I don't understand" / "first
year" / "beginner" -> the getting-started workflow directly, reworded as "New here? Start with these ... no flags needed",
with gentle follow-up suggestions -- and (b) four foundational CONCEPTS (lattice, Hubbard model, exact diagonalization,
Monte Carlo), each a short beginner-level explanation that points to the right command, which also resolve the "run first"
and "model" collisions. (3) Refreshed a stale `cdet info` gui row ("local browser console" -> "browser front-end over the
CLI (+ optional assistant)"). VERIFIED: every failing question now answers correctly, confirmed live through the running
server's /api/assist; the specific-term answers are unchanged (no regressions); the assistant self-test grew from 10+6 to
14 query + 6 behaviour checks and passes; concept count 9 -> 13. SCOPE: docs and help-layer only -- no physics changed, the
assistant still imports no physics and runs nothing, the GUI is still the pure CLI wrapper, and the frozen reference engine
is untouched (194/194). cdet_assistant.py + QUICKSTART.md + cdet.py + BLIND_TEST_v187_RESULT.md + csurrogate_params.h v187.

### #196 -- Assistant upgraded with chatbot best practices (v186)

Paul: research online for the best setups of chatbots, learn, then improve the chatbot. I web-searched current
help-chatbot practice -- intent structuring and fallback design (Towards Data Science, Rasa), graceful failure and
"surface the closest matches" disambiguation (UX Content / BMO case study, Fuselab), fuzzy/typo tolerance and "did you
mean" (Azure AI Search, System Overflow scoring-and-gating, difflib-style Levenshtein), and hybrid menu + free-form UX
(Infobip) -- and applied the well-established techniques to the existing rule-based assistant. It stays exactly what it
was: self-contained, offline, rule-based, RUNS NOTHING, stdlib only (difflib, math, re) -- no model, no inference, no new
dependencies. The matcher was rewritten from raw keyword-overlap to: (1) idf term-importance scoring over a UNIFIED pool of
commands + concepts + workflows, so distinctive words (occupancy, susceptibility, radius) outweigh common ones, stopwords
are dropped, and multi-word phrases get a bonus (including raw description n-grams for commands so "double occupancy" and
"equation of state" resolve to docc/eos); (2) difflib typo tolerance ("explain the wal" -> wall; a misspelled command ->
"Did you mean cdet wall?") plus a light suffix stemmer (started->start); (3) confidence gating that answers directly when
one topic clearly leads but otherwise DISAMBIGUATES ("Did you mean X or Y?") rather than guessing; (4) a closest-match
FALLBACK that surfaces the nearest topics as tappable suggestions instead of a generic "not sure"; (5) intent signals --
an action verb (compute/run/measure) biases toward the actionable command, a definitional phrasing ("what is", "what does
... mean") biases toward the concept; (6) a forward path on EVERY reply via quick-reply suggestion chips (related topics,
"what do its parameters mean?", "how do I start?"), with starter prompts in the welcome; and (7) lightweight follow-up
memory -- the panel threads the last answered topic as ctx so "tell me more", "an example", or "what are the parameters"
expand on the prior turn with no server-side session state. respond() now returns {reply, commands, suggestions, topic};
the /api/assist endpoint accepts an optional ctx; the GUI renders suggestion quick-replies (distinct pill style), threads
ctx via a _lastTopic var, and offers starter chips. Tuned the scoring/gating against a battery of real queries (idf, action
vs definitional bias, phrase n-grams) so the common intents land directly while genuinely ambiguous ones disambiguate.
Extended the self-test from 10 query checks to 10 query + 6 behaviour checks (typo tolerance, keyword intent, fallback
offers suggestions, every answer carries a forward path, follow-up uses context, action-verb intent bias) and asserted the
return-shape on several queries -- all pass. Verified live: /api/assist returns the new suggestions/topic fields, follow-up
via ctx works, typo and fallback behave, and the page carries the sugg-chip + &ctx= + _lastTopic wiring. SCOPE, stated
plainly: this is a better HELP LAYER grounded in cited best practices -- it is NOT a language model and changes NO physics;
the assistant still imports no physics and runs nothing, the GUI is still the pure CLI wrapper, and the frozen reference
engine is untouched (194/194). cdet_assistant.py + cdet_gui.py + CDET_ASSISTANT_UPGRADE_v186_RESULT.md + csurrogate_params.h
v186 note.

### #195 -- An optional, self-contained help assistant (v185)

Paul: add an optional toggle-on chatbot to the software to assist the user on what to do and what the capabilities are,
in tandem with the existing help docs; and asked whether a free, completely self-contained chatbot could be bundled to
give AI-style responses. Answered honestly: a real local LLM (Ollama / GPT4All / llama.cpp with Llama/Mistral weights)
would add ~2-7GB to the package and be slow on CPU (minutes per reply) -- the wrong trade for a help assistant -- and
proposed instead a self-contained RULE-BASED assistant (a knowledge graph + keyword matcher: instant, offline, no
downloads, maintainable, and it cannot hallucinate capabilities because every entry maps to something real). Paul
approved. Built cdet_assistant.py: COMMANDS (21 subcommands, each with desc/params/example/related), CONCEPTS (9: the
sign problem, CDet/connected determinant, the wall & U_c/RPA/Lindhard, the true/thermal Fisher-zero radius, conformal-
Borel resummation, Mott physics, the thermodynamic limit, the three-model architecture, the parameters beta/mu/U/N/L),
and WORKFLOWS (6: getting started, observables, the wall study, lattice run, the method, export). respond(query) is pure
rule matching: it handles greetings and 'what can you do', recognises explicit command names (returns that command's help
with a runnable example), and otherwise scores concepts and workflows by keyword overlap weighted by phrase specificity
(multi-word keys like 'true radius' outrank generic ones like 'radius', which fixed an initial mismatch), with a graceful
fallback. Wired into the GUI as a TOGGLE-ON slide-in panel, hidden by default so it is purely optional as asked: a
top-right 'assistant' button opens it; chat bubbles; bot replies render light markdown (**bold** -> teal) and a row of
suggested-command chips that copy to the clipboard; a welcome message states it is offline, rule-based, complements the
docs, and runs nothing. Server side, a new /api/assist?q=... endpoint calls cdet_assistant.respond and returns
{reply, commands}; the GUI otherwise remains the pure CLI wrapper from v184 (the assistant imports no physics and executes
nothing). VERIFIED: cdet_assistant._selftest passes 10 query checks (getting started -> validate; 'what is the wall' ->
U_c; connected determinant -> CDet; double occupancy -> docc; true radius -> Fisher; 'what does beta mean' -> inverse
temperature; bare 'eos' -> equation of state; export -> csv; 'what can you do' -> command list; nonsense -> fallback) and
asserts every command example is a real command; through the running server /api/assist returns sensible answers with
relevant command chips, the page carries the toggle + panel + wiring, and the panel ships hidden until toggled. SCOPE: a
help layer only -- optional, offline, rule-based; it teaches and suggests but changes and runs nothing. Frozen reference
engine untouched (194/194). cdet_assistant.py + assistant panel/endpoint in cdet_gui.py + CDET_ASSISTANT_v185_RESULT.md +
csurrogate_params.h v185 note.

### #194 -- GUI rebuilt as a thin wrapper over the CLI (v184)

Paul's correction (voice): he was worried the GUI had become a parallel path -- "if you're doing a particular lattice
calculation from the GUI on its own ... does that mean one thing is only done by the GUI and everything else is done by
commands?" -- and stated the GUI "should just literally be a case of doing what the console would do before manually,"
with sliders plugging into the existing command controls, "reusing existing math and existing commands," and NOT changing
any calculations or core code. He was right, and this is the fix. The v181-183 GUI had drifted: its cards imported the
physics modules and called density_ed/docc_ed/kappa_fluct/wall/atom_nearest_zero directly, which is what forced the ugly
compromises -- the eos/docc/chi cards hardwired mu=1, beta=2; an N<=4 cap was bolted on to dodge the slow large-N ED; the
GUI computed its own sweeps and built its own CSVs. All of that was the wrong shape. REBUILT cdet_gui.py from scratch as a
pure front-end: it now imports ONLY the Python standard library (no numpy, no suite modules). A single /api/run endpoint
builds a list argv [python, cdet.py, <subcommand>, <flags>] from an allow-list (subcommand -> {flag: caster}), runs it via
subprocess.run (cwd=ROOT, never shell=True), strips ANSI, and returns the command's real stdout. Every subcommand is a
card and its controls are that subcommand's actual flags: validate/converge/connected/crosscheck/info (no flags); eos/
docc/resum (--N --U --K), chi (--N --U); wall/tide/primes/twist/trueradius (--beta --mu); run (--L lattice size, --beta,
--beta-hi, --bstep, --K, --NT); sweep (--target, --var, --values); export (--format). Sliders for numbers, dropdowns for
choices (target/var/format), a text box for the values list. So nothing is GUI-only and nothing is reimplemented -- if you
can type it you can slide it, and vice versa. No caps and no hardcoded parameters: whatever the user sets is passed
straight through, and a slow setting is slow exactly as the CLI is (subprocess timeout 300s, with a friendly message).
copy yields the exact command; the recent strip lists real command strings and clicking one restores that card's controls
and re-runs. SAFE BY CONSTRUCTION: list argv (no shell), allow-listed subcommands, numeric values cast and string values
restricted to known sets, so a value like "5;rm -rf /" is rejected with "--beta expects a number" rather than executed
(verified), and an unknown command is refused. VERIFIED end-to-end (server up, curled, down): the eos card runs `cdet eos
--N 4 --U 1.0 --K 10` and returns its real SU(N) table; wall runs `cdet wall --beta 5.0 --mu 0.0` (output has U_c);
trueradius returns the real radius; the injection attempt is sanitized; the unknown command is rejected; recent records
the three real commands. The core cmd_eos/cmd_docc/cmd_chi in cdet.py were never modified across any of this and still
produce identical results (confirmed bare density_ed(a.N,a.U) intact). Updated the README and INDEX GUI lines to describe
the wrapper accurately. SCOPE: this is purely the interface layer; the calculations, commands, and the frozen engine are
untouched (194/194). cdet_gui.py (rewritten) + CDET_GUI_WRAPPER_v184_RESULT.md + README/INDEX/csurrogate v184 notes.

### #193 -- GUI: a recent-runs memory (+ a high-N hang fix) (v183)

Paul: go (build the recent-runs strip suggested at the end of v182). Added a small server-side memory of explicit runs: a
`recent` strip above the cards showing the last up-to-8 runs as chips (card id + the slider values used + the result;
amber value for the limit cards wall/trueradius), click a chip to restore those slider settings and re-run, plus a clear
link. Kept it honest and unobtrusive: ONLY explicit Run clicks are remembered (the Run handler sends &log=1; the Live
auto-reruns triggered by dragging a slider do not, so the memory reflects intent not slider twitches), consecutive
identical configs collapse in place (no duplicate chips), and the ring buffer caps at 8. Implemented as a module-level
_RECENT buffer with a _record() recorder called from the handler when log is in the query, plus two meta-endpoints
/api/_recent and /api/_clear handled before the ROUTES lookup; the strip survives a page refresh within the session. The
frontend threads a log flag through runCard (button -> runCard(c,true) logs; live onSlide -> runCard(c,false) does not;
fixed the latent forEach(runCard) index-as-log bug at the same time), refreshes the strip after a logged run, and renders
chips with restore-on-click. FOUND AND FIXED A REAL v181 RESPONSIVENESS BUG in the process: the sweep cards rebuild their
trace with repeated 2-site density_ed/docc_ed/kappa calls, and that ED scales steeply with N -- measured instant to N=4
(0.09s), 3.34s at N=5, and effectively hanging at N>=6 -- so with the N slider topping out at 8 a single eos/docc/chi
click could wedge the request for ~a minute (this is exactly what made an earlier server smoke test appear to hang the
shell -- a curl to eos?N=6 blocked the handler thread). Fixed by capping the GUI N slider at 4 (where every run is
sub-second), trimming the eos/docc/chi sweeps from 21/17 to 11 points, and clamping N<=4 server-side in those three
endpoints; larger SU(N) remains available from the terminal via each card's copy-as-CLI command (which uses the cached
contour-series path), with a rail hint stating the split. VERIFIED end-to-end: three explicit runs recorded most-recent-
first (trueradius, eos, wall), a repeated config dedupes (count stays 3), an unlogged live rerun is not recorded, clear
empties the buffer, and the page carries the recent strip + refreshRecent/renderRecent + &log=1 wiring; routes are now
sub-second even when N is requested high (clamped): eos 0.94s, chi 0.26s. SCOPE: front-end only -- a tiny convenience
memory plus a responsiveness fix; no new physics, nothing the tool computes changes. Frozen reference engine untouched
(194/194). cdet_gui.py + CDET_GUI_RECENT_v183_RESULT.md + csurrogate_params.h v183 note.

### #192 -- GUI: downloadable CSV + copy-as-CLI (v182)

Paul: add that -- the two follow-ups suggested at the end of v181 (wire sweep cards to a downloadable CSV reusing export;
add a copy-as-CLI button so the GUI teaches the command line). DOWNLOAD CSV: the sweep cards (eos, docc, chi, wall, free
propagator) get a CSV button that hits /api/<card>?...&csv=1; the server computes the sweep and formats it with the
suite's own export._write_csv (not a re-implementation), so the downloaded file is the same shape as `cdet export` output
(a "# <name>" + JSON-meta header line, a column row, the data rows), served with Content-Disposition: attachment;
filename=cdet_<card>.csv. COPY AS CLI: each card renders the exact `cdet ...` command that reproduces it, kept in sync as
the sliders move, with a copy button (navigator.clipboard with a textarea execCommand fallback); commands are real and
runnable (cdet eos --N 4 --U 1, cdet wall --beta 5 --mu 0, cdet trueradius --beta 2 --mu 0.5, cdet converge, cdet
validate, ...). FAITHFULNESS FIX (the honest part): the CLI's eos/docc/chi don't expose --mu/--beta, so to make the
copied command reproduce the displayed value rather than approximate it, those three cards now call the compute functions
bare at the suite reference point (mu=1, beta=2) -- exactly what the CLI does -- and their "uses" tags shrank to N U; the
global mu/beta sliders consequently drive only the lattice cards (wall, true radius, propagator), where the CLI genuinely
takes --beta --mu. Considered instead parametrizing eos/docc/chi with --mu/--beta but that would have meant recomputing
the cached series at arbitrary mu/beta and risking the commands' cross-check routes, out of proportion to the ask. VERIFIED
end-to-end (server up, curled, down): CSV returns export-formatted text with the right Content-Type/Content-Disposition
for all five sweep cards; the page carries the .cli line, copy and CSV controls; bare eos value 0.437896 matches `cdet
eos`; and the copied commands actually run -- cdet eos --N 4 --U 1 -> 0.4379, cdet trueradius --beta 2 --mu 0.5 -> radius
1.5723, cdet wall --beta 5 --mu 0 reproduces the wall sweep that contains the slider's L. HTML balanced; every csv card
builds a CSV; CLI lines live-sync. SCOPE: front-end only -- it moves work out of the GUI (a file you can keep, a command
you can run) and adds no new physics; nothing the tool computes changes. Frozen reference engine untouched (194/194).
cdet_gui.py + CDET_GUI_CSV_CLI_v182_RESULT.md + csurrogate_params.h v182 note.

### #191 -- A local browser console: quick runs with sliders (v181)

Paul: add quick runs -- fast defaults of the most-used items with easy slider customization -- and give it a GUI. Since
the package is real code on disk, the honest GUI is a LOCAL web console (a browser mockup/artifact could not drive the
engine), so built cdet_gui.py: a Python-stdlib http server (no new dependencies beyond numpy) serving a single-page
console at 127.0.0.1. UI: a left rail of sliders (N SU(N) flavors, U interaction, mu chemical potential, beta inverse
temperature, L lattice size) and a grid of one-click quick-run cards -- equation of state (density), double occupancy,
susceptibilities (charge kappa + spin chi_s), convergence wall (RPA U_c), true radius (the complex-U Fisher pair), free
propagator (L->inf), and validate (5 gates). Each card lists the sliders it reads, shows a large monospace tabular
readout, and (where a sweep applies) a small SVG trace; a Live toggle re-runs cards on slider movement (debounced).
Following the frontend-design skill, grounded the look in the subject as a numerical INSTRUMENT: dark console, mono
readouts, teal oscilloscope-style traces, and amber threshold lines reserved for the two physical limits (the wall and
the radius) -- one action/data accent (teal), one limit accent (amber), everything else quiet; responsive to mobile;
errors reported in-interface rather than crashing the server. Backend: each /api/<name> endpoint calls the SAME compute
functions as the CLI (sun_eos_curve.density_ed, double_occupancy.docc_ed, susceptibilities.kappa_fluct/chi_spin_fluct,
wall_vs_size.wall, wall_true_radius.atom_nearest_zero, a local plane-wave NN propagator, and a `cdet.py validate`
subprocess); all are sub-second so the console feels live. VERIFIED end-to-end by starting the server and curling: page
loads (title present), eos 0.3716 / docc 0.2933 / kappa 0.1826, chi_s 0.2853 / wall U_c 1.9752 / true radius 1.5723 with
Im=pi/beta thermal detail / free propagator 0.19944 (matches converge's TD limit 0.1994379636) / validate 5/5 gates;
unknown endpoint returns 404; the embedded HTML is tag-balanced and every card id maps to a registered route; launches
from both `cdet gui` and `python3 cdet_gui.py`. Wired `cdet gui [--port N] [--no-browser]`; added gui to the INDEX
interactive group and the README CLI list + a "Try this first" demo line. HONEST SCOPE (in the result): a front-end over
existing computation -- it makes the most-used items one click with slider customization and adds no new physics; nothing
the tool computes changes. Frozen reference engine untouched (194/194). cdet_gui.py + CDET_GUI_v181_RESULT.md +
csurrogate_params.h v181 note.

### #190 -- UX polish from a blind-user CLI review (v180)

A reviewer exercised the CLI as a new (blind) user: praised the unified ./cdet entry point, the rich tables/colors, the
validate dashboard, converge reaching 64x64/100x100 instantly, the interactive shell, and --help discoverability; rated
it commercial-viable for expert users and flagged concrete usability gaps. Acted on the actionable ones (interface only;
engine and physics untouched): (1) bare `cdet run` now works -- the upper beta resolves to one --bstep above --beta (was:
a.beta_hi stayed None and the run printed "30.0..None" and broke), plus a cyan "customize:" line showing the full
invocation; (2) `cdet sweep` prints per-point progress [i/n] var=value through a new optional progress= hook added to
cdet_study.study(), with --verbose still giving full per-point detail; (3) worked-examples epilogs (RawDescriptionHelp
Formatter) added to the run/sweep/lab subparsers so `cdet <cmd> --help` shows copy-pasteable lines; (4) the interactive
shell got more synonyms (number density/occupancy->eos, doublons->double-occ, cdet->connected-det) and its "I couldn't
tell which observable" message now points users to `examples` and `help`; (5) README gained a "Try this first" three-line
block (engine test -> validate -> converge) and an explicit orientation note that the numbered folders 01..08 are the
staged source/oracles behind ./cdet and need not be opened to use the tool. Verified unchanged after the polish: cdet
validate 5/5, frozen engine 194/194, surrogate worst dev 3.55e-15, converge still reaches 100x100, the shell menu/
examples/parse paths all work. HONEST SCOPE (stated in the result): this is usability polish -- it makes the tool nicer
to drive for an expert, matching the reviewer's "commercial-viable for experts" usability judgment, but it does not
change what the tool computes or its standing as a validated pedagogical CDet implementation reproducing known physics.
Frozen reference engine untouched. UX_POLISH_v180_RESULT.md + README/help/shell updates + csurrogate_params.h v180 note.

### #189 -- Tier 0: the connected-determinant recursion, implemented and validated (v179)

After the web-search reality-check (honest verdict: the suite reproduces/explores KNOWN physics -- CDet is Rossi 2017, the
complex-U wall is a documented limitation, conformal-Borel is established SOTA -- good engineering but NOT a sign-problem
advance; "massive progress" overstates it), discussion turned to what a real contribution would require (a Monte Carlo
CDet sampler at high order in the strong-U/low-T/doped "prohibited area"), tiered 0-3. Paul: build Tier 0 -- the piece the
package conspicuously never had: the connected determinant ITSELF. Implemented Rossi's recursion C(V)=D(V)-sum_{v* in S
subsetneq V} C(S) D(V\S), full weight D(V)=det(M)^2 per spin (M_ab=G0(vertex_a,vertex_b), vertex=(site,tau); atom uses one
level eps=-mu, 2-site uses bonding/antibonding eps=-mu-/+t), free-energy series ln(Z/Z0)=sum_n (-U)^n/n! integral C so the
U^n coefficient is (-1)^n times the ordered-tau simplex integral of C (C symmetric). VALIDATED to machine precision three
ways: (1) the linked-cluster identity D(V)=sum_partitions prod C(B) at random vertex positions n=2..5 -- worst 2e-16, NO
quadrature, proving the connectedness combinatorics exactly; (2) atom lnZ U-series orders 1..5 vs closed form -- worst
6e-17; (3) 2-site Hubbard lnZ U-series orders 1..3 vs ED -- order1 1e-12, order2 2e-12, order3 1e-9 (order3 ED-fit limited,
not CDet). HONEST FRAMING (in module + result): a faithful LOW-ORDER, DETERMINISTIC CDet on exactly-solvable systems --
makes the package genuinely implement the method it is named for rather than only wrapping a frozen engine -- but
explicitly NOT a contribution to the sign problem; the frontier (high-order MC sampler in the prohibited regime past the
complex-U poles, with reference-shifting moves) is Tier 2-3 and unbuilt. Three-gate self-test passes. Frozen reference
engine untouched (194/194). cdet_connected.py + `cdet connected` + CDET_CONNECTED_v179_RESULT.md + csurrogate v179 note.

### #188 -- Consolidation: a single index for the whole package (v178)

Paul: consolidate all files and docs. The package had reached ~647 files -- 127 *_RESULT.md findings, 176 CROSSCHECK
records, a 145-entry ledger (#1..#188), the frozen reference engine, the production plane-wave engine, the surrogate,
the SU(N) EoS + observables, and the wall suite -- with no single map. Added INDEX.md as the authoritative entry point:
the one invariant (engine 194/194), the three-model architecture table, the directory map, the full 19-subcommand CLI
grouped by purpose, the two arcs (elevation checklist v163-171: CLI/observables/figures/export/packaging-CI/dual-license/
bindings/docker; wall-physics arc v172-177: wall moves with L -> tide -> prime sieve -> twist/rectangular -> consolidation
-> the true thermal radius), and where each kind of knowledge lives. Doc consistency pass: README now lists the full wall
suite including trueradius (was missing) and points to INDEX.md; QUICKSTART (build-and-verify) left current; verified
every INDEX/README file reference resolves to a real file, all 19 CLI subcommands are documented, and there are no broken
references or orphans across any doc. Re-verified green post-consolidation: cdet validate 5/5; frozen engine 194/194;
surrogate worst dev 3.55e-15; orphan scan clean. Frozen reference engine untouched. INDEX.md + CONSOLIDATION_v178_RESULT.md
+ README update + csurrogate_params.h v178 note. The package is now navigable from a single top-level index.

### #187 -- The true radius is thermal, not the RPA wall (v177)

Paul: do it -- go after the deferred probe of whether the TRUE radius (the nearest complex-U singularity of the actual
lnZ, the v146 branch point, beyond the RPA instability) inherits the v173 tide / v174 sieve. The earlier ED Fisher-zero
attempts were noisy and estimator-dependent; this time I anchored on GROUND TRUTH: the Hubbard atom Z(U)=1+2e^{bmu}+
e^{-bU+2bmu} is entire, lnZ singular at the Fisher zeros U=-ln(A)/beta +- i pi/beta (A=(1+2e^{bmu})e^{-2bmu}), so the
true radius is sqrt((lnA/beta)^2+(pi/beta)^2). A direct complex-zero finder (coarse scan + Newton) reproduces this to
0.0e+00 -- which calibrates the method. FINDINGS: (1) the true radius is THERMAL, not an instability -- the nearest
singularity is a complex-conjugate Fisher pair at Im U ~ pi/beta (a Matsubara-like scale), categorically different from
the real-axis RPA wall; for small Hubbard rings the nearest zero stays on this thermal line (beta=2, mu=0.5, L=3:
Im U=1.84 pi/beta). (2) It is CLOSER than the RPA wall (ring L=3: R_true~2.90 < R_RPA~3.42) -- the complex-U structure,
not the Stoner instability, sets the actual convergence radius; this is the v146 caveat made numerical. (3) It does NOT
inherit the Diophantine sieve: the sieve is specifically a property of chi0_max being a MAX over the q-grid (the grid
misses the continuum peak q* by a number-theoretic amount), whereas R_true is a GLOBAL analytic property of lnZ (the
nearest complex-U zero) with no q-grid maximization, so the sieve mechanism is structurally absent. HONEST LIMITATION
(stated in the module and result): a direct large-L demonstration is precluded -- the sieve appears at large L (the 2D
lattice) while R_true is only computable at small L (ED, 2^{2L} states), and the complex-zero search is delicate (the
L=4 ring flips between scan resolutions; L=3 is stable and used for the gate). The case rests on the exact atom anchor
(0.0e+00), the thermal nature (Im U=pi/beta), the structural no-grid-max fact, and small-ring evidence that R_true is
thermal and < R_RPA. CONCLUSION: two different radii govern the bare-U series -- the RPA wall (real-axis Stoner
instability, carrying the q-grid tide and Diophantine sieve) and the true radius (a thermal complex-U Fisher pair near
pi/beta, closer, sieve-free); the number-theoretic structure lives in the q-sampling of the RPA wall, not in the
analytic continuation of lnZ. Five pre-registered gates pass (atom finder==analytic 0.0e+00; atom zero at Im=pi/beta;
ring L=3 R_true<R_RPA; ring L=3 zero on the thermal line; structural no-grid-max). Frozen reference engine untouched
(194/194). wall_true_radius.py (self-test gate PASS) + `cdet trueradius` subcommand + WALL_TRUE_RADIUS_v177_RESULT.md;
csurrogate_params.h v177 note. This closes the wall arc's last open probe.

### #186 -- Consolidation: one wall core, all models side by side (v176)

Paul: consolidate and apply the upgrades to all modules and docs; test all models side by side and see what each informs
about the others; find things to fix/improve in all; then retest. CONSOLIDATION: the v172-175 arc had four wall modules,
and wall_twist re-implemented the Lindhard susceptibility wall_vs_size already had (generalized to rectangular+twist).
Factored them onto ONE canonical core, wall_vs_size.chi0_max_rect(Lx,Ly,beta,mu,thx,thy,t), of which the square-periodic
chi0_max is the special case; wall_twist now delegates (its duplicate _fermi and chi0_max removed), wall_tide and
wall_primes already imported the core. The rect/twist upgrade now lives in the base, available to every wall module;
square-periodic results unchanged (dev 0.0e+00). Verified other modules' dispersion/fermi (plots, sun_eos_2d/n2,
sun_lattice_production) are DIFFERENT physics (weak-coupling 2D series, production lattice) and correctly left
independent. DOCS: README had zero wall-suite documentation -> added a Wall-physics section (wall/tide/primes/twist/
crosscheck + the shared core); new `cdet crosscheck` subcommand. SIDE-BY-SIDE CROSS-CHECK (consolidation_v176.py): A
frozen engine / B plane-wave engine / C surrogate / D SU(N) EoS+observables / E wall suite, with the links: E internal
(4 modules one core, dev 0.0e+00); B<->E (chi0(q=0)==dn/dmu free compressibility, 7e-13, the wall's susceptibility and
the lattice density share the dispersion); D<->E (the SAME finite-radius phenomenon -- U_c^EoS=1.054 conformal-Borel
singularity vs U_c^wall=1.975 Lindhard; resummation extends past the wall in both: at U=0.7 the bare EoS series diverged
|bare-ED|=3.6 while conformal-Borel tracks ED |cb-ED|=0.009; the wall suite generalizes the EoS radius finding to the
lattice). ISSUES FOUND+FIXED: duplicate Lindhard core -> single chi0_max_rect; README wall-doc gap -> filled. RETEST
(all models, post-consolidation, all pass): surrogate worst dev 3.55e-15; frozen 194/194; cdet validate 5/5; observable
models D (eos/conformal/docc/chi/resummation/export) OK; wall models E (vs_size/tide/primes/twist) PASS; consolidation
cross-check PASS; CLI self-test + packaging + docker gates PASS. Frozen reference engine untouched (194/194).
consolidation_v176.py (self-test gate PASS) + `cdet crosscheck` + CONSOLIDATION_v176_RESULT.md; README wall section;
csurrogate_params.h v176 note. Remaining open probe (deferred, honest): whether the TRUE radius (the complex-U branch
point of v146, beyond the RPA instability) inherits the same tide/sieve -- now attackable with the rectangular-supercell
trick to remove commensuration noise.

### #185 -- "Half-integer" lattices: twisted BC and rectangular supercells (v175)

Paul asked whether lattices can be half-integer (alongside "go for it" on the true radius). There is no fractional site
count -- a periodic lattice needs an integer number of sites -- but "half-integer" has two precise standard meanings, and
using them resolved what the v173 tide and v174 sieve actually ARE. (A) Twisted boundary conditions: single-particle
momenta k=2pi(n+theta)/L with theta a flux through the torus; theta=0 periodic, theta=1/2 ANTI-PERIODIC = the literal
half-shifted grid (twist-averaging is the standard finite-size technique). (B) Rectangular/tilted supercells Lx x Ly: a
non-square momentum-transfer grid (2pi mx/Lx, 2pi my/Ly), effectively non-integer linear resolution. VERDICT (beta=5,
mu=-0.6, q*=(0.783,1.000)pi): TWIST DOES NOT HEAL THE SIEVE. In the particle-hole susceptibility the twist cancels in
k->k+q differences, so the momentum-TRANSFER grid q=2pi m/L is theta-INDEPENDENT (verified: the peak q-index is identical
for theta=0 and theta=1/2). Hence anti-periodic BC does not flip the even/odd parity, and twist-averaging cuts the prime
error only ~7% -- the sieve is a q-RESOLUTION bottleneck, not a k-quadrature one. RECTANGULAR SUPERCELLS DO HEAL IT: a
non-square q-grid can land a point exactly on q* -- 23x46 hits q*=(18/23, 46/46) and the error collapses to 4e-4 even
though 23 is PRIME, where the square 17x17 misses by 6e-2. The unifying rule is DIOPHANTINE: a lattice captures q* in a
direction iff q*_comp*L/2 is near an integer; composite/even L meet this more often when q* is near a low-denominator
rational (the v174 sieve), and a rectangular cell meets it per-direction for any size (good-L error 0.008 vs bad-L 0.017).
CONCLUSION: the tide and prime sieve are finite-size SAMPLING artifacts of the q-grid relative to the nesting vector --
not properties of the true thermodynamic-limit wall; the cure is a supercell whose q-grid hits q*, not a finer twist.
Four pre-registered gates pass (anti-periodic doesn't flip parity + q-index theta-independent; twist-avg leaves prime
error >0.7x; rectangular 23x46 <0.01 while 17x17 >0.05; Diophantine q*_x L/2 near integer => smaller error). Frozen
reference engine untouched (194/194). wall_twist.py (self-test gate PASS) + `cdet twist` subcommand +
WALL_TWIST_v175_RESULT.md; csurrogate_params.h v175 note. Remaining open probe (deferred, stated honestly): whether the
TRUE radius -- the complex-U branch point of v146, beyond the RPA instability -- inherits the same tide/sieve; that needs
the complex-U singularity of the actual lattice lnZ (ED-limited), not the leading instability.

### #184 -- Prime lattice sizes: a Diophantine sieve on the wall (v174)

Paul: jump and reduce the lattice through primes, see what patterns emerge. The v173 error law (wall deviation ~
peak-curvature x (distance from the true peak q* to the nearest grid momentum)^2) makes lattice size enter through
number theory, because that grid-miss distance is a Diophantine quantity -- how well the rational grid {k/L} approximates
q*/2pi. Found a clean sieve (beta=5, mu=-0.6, q*=(0.78,1.00)pi): PRIME L are commensuration-blind (no divisors -> cannot
represent any low-denominator momentum) so they systematically miss q* and ride the UPPER envelope of the tide, while
COMPOSITE L (many divisors -> dense rational approximants) capture the peak. Quantified: prime L deviate ~2.7x more from
the TD wall than composite L; corr(#divisors(L), dev) = -0.39 (more divisors -> better capture); the effect survives
controlling for the v173 even/odd parity (within ODD L, primes 0.022 > odd-composites 0.014); and -- the key link -- the
entire pattern is the v173 curvature law applied to the grid-miss: corr(grid-miss(L)^2, dev) = +0.96. Filling dependence
is the Diophantine signature: the sieve is sharp only when q* sits near a low-denominator commensurate vector (good
rational targets), and washes out at a generic-irrational peak (ratio x2.7 at mu=-0.6 -> x1.1 at mu=-2.8). Practical
upshot: stepping through primes traces the worst-case wall and through highly composite sizes the best; never read a
finite-lattice wall off a prime lattice -- prefer sizes whose divisors match the nesting vector. Five pre-registered
gates all pass (corr(miss^2)>0.85; prime/comp ratio>2; corr(#div)<-0.3; primes>odd-composites within odd L; sieve sharp
at mu=-0.6, washed out at mu=-2.8). Frozen reference engine untouched (194/194). wall_primes.py (self-test gate PASS) +
`cdet primes` subcommand + WALL_PRIMES_v174_RESULT.md; csurrogate_params.h v174 note. Remaining deeper-physics roadmap:
streaming/high-order orders; tightening the wall beyond the leading instability (the complex-U structure).

### #183 -- The wall is a tide: its finite-size waves (v173)

Paul: sweep lattice size up and down, see how the wall/tide reacts, work out its waves. The v172 wall U_c(L)=1/chi0_max
is a Brillouin-zone quadrature on the discrete LxL grid, so it does not converge smoothly -- it OSCILLATES, because
whether the peak (nesting) momentum q* lands on a grid point depends on commensuration with L. Swept every integer L and
worked out three wave laws, each a pre-registered gate. (1) PERIOD = 2pi/q*: the L-wavelength of the oscillation equals
2pi over the peak momentum, so the tide's period MEASURES the Fermi nesting vector -- half-filling q*=(pi,pi) gives a
period-2 even/odd parity wave; doping to mu=-2.8 moves q* to (0.542,0)pi and the measured FFT period 3.68 matches the
predicted 2/0.542=3.69. (2) BRANCH LAWS (half-filling): the even-L branch (peak captured on-grid) converges
EXPONENTIALLY -- spectral accuracy of the trapezoidal BZ quadrature for the smooth finite-T integrand (deviation x0.5
per dL=2); the odd-L branch (peak missed by ~pi/L) converges as 1/L^2 (fitted p=-1.89), because the grid maximum sits
~pi/L from the true peak and a smooth peak's curvature makes the deficit O(1/L^2). Even approaches from below
(1.64->1.975), odd from above (3.13->1.99), meeting at U_inf=1.9752. (3) AMPLITUDE: the wave height (neighbour even/odd
split) decays with L (1.49 at L~4 -> 0.035 at L~32) -- violent in 'shallow water' (small lattices), calm in 'deep
water'; decreasing the lattice amplifies the waves, which is why a small cluster gives an unreliable wall. All five
gates pass (half-filling period 2; incommensurate period 2pi/q*; odd p~-2; even ratio<0.7; amplitude decay + branches
meeting). Frozen reference engine untouched (194/194). wall_tide.py (self-test gate PASS) + `cdet tide` subcommand
(ASCII tide chart + period readout) + WALL_TIDE_v173_RESULT.md; csurrogate_params.h v173 note. Remaining deeper-physics
roadmap: streaming/high-order orders; tightening the wall beyond the leading instability (the complex-U structure).

### #178 -- Dual license: free academic, paid commercial (v168)

Paul: make it free for academic use but chargeable for business. Replaced the MIT LICENSE with a DUAL license. Free
tier = PolyForm Noncommercial License 1.0.0 (web-fetched the official text from polyformproject.org/github to reproduce
it verbatim) -- a standard, lawyer-drafted noncommercial license under which any noncommercial purpose is permitted and
which EXPLICITLY names educational institutions and public research organizations as permitted regardless of funding
(so academic use is free). Paid tier = a commercial license required for any commercial purpose (for-profit use, a
commercial product/service, or anticipated commercial application); COMMERCIAL-LICENSE.md describes the grant and a
contact placeholder. LICENSE has a DUAL-LICENSE header, the Required Notice (Copyright 2026 CDet suite), and the full
PolyForm NC text. pyproject.toml: license -> { file = "LICENSE" } + classifier "License :: Other/Proprietary License".
README and the packaging gate updated (packaging_check.py now asserts the PolyForm NC text + explicit academic-free
clause + COMMERCIAL-LICENSE.md). Added an honest in-file caveat that this is a standard structure, not legal advice,
and a lawyer should review a real commercial offering. Verified: `pip install -e .` still works and `cdet validate` is
5/5. Frozen engine untouched (194/194). LICENSE + COMMERCIAL-LICENSE.md + pyproject.toml + packaging_check.py;
csurrogate_params.h v168 note. Remaining roadmap: python bindings, streaming/high-order, self-energy maps, docker.

## Frame-of-reference checks (apply to every claimed result, before banking it)
A number that holds in one corner is a coincidence until these are run. Standing checklist:
- GENERALIZABILITY (size): does it hold as L changes, or only at one lattice? Quote the
  L-dependence of any prefactor and show convergence (e.g. stiffness -> exact Bessel as L grows,
  v16; prefactor hits v_F at L=6,10,12, v17). A rule that scales with system size is the win.
- MECHANISM OF THE RESIDUAL (the "smoking gun"): name the leftover error and show its before/
  after under the knob that controls it. Don't report "~12% off"; report "12% = the marginal
  correction, which goes 60% -> 12% as you dope" (v17). If you can't move it predictably, you
  don't yet understand it.
- FILLING / REGIME ROBUSTNESS: does it survive away from the special (commensurate) point --
  n=1 -> doped? State whether doping helps or hurts and why (v17: it helps u_sigma). Holding up
  under doping is elite territory; failing under doping is also a result, if reported.
- EXACT ANCHOR: is every approximate number tied to at least one exactly-known limit or case
  (U=0 v_F; the n=1 Bessel curve; a Bethe value)? Calibrate convention on the exact case (#11),
  and treat disagreement with it as information (#4), never tune to make it vanish.

## THE CONSOLIDATION RULE (run every time Paul says "consolidate")
A consolidation is a periodic checkpoint that re-proves the whole current state coheres; the deliverable is a
health-gate, not a new physics result. Precedent: consolidation_v101/v115/v120/v130/v138/v147. Each time:
1. Create consolidation_vNN.py (vNN = the version number) in 08_2d_interacting/ -- ONE health-gate module whose docstring restates the
   three-model architecture (FROZEN REFERENCE engine/ 194/194; PRODUCTION ENGINE cdet_planewave_engine.c;
   SURROGATE csurrogate.c) plus the UI control plane and the analysis supplements, INCLUDING everything added
   since the previous consolidation. Its `_selftest()` (a) re-checks the cross-model invariants (surrogate ==
   production route; surrogate addition pole == python; fast-minors connected determinant == numpy), and (b) runs
   ONE FAST live check of each headline capability added since the last consolidation, each tied to an exact
   anchor (ED / the frozen engine). Keep the whole gate fast (seconds), since it runs every audit.
2. Write CONSOLIDATION_vNN_RESULT.md (template): the consolidated state + the arc since the last consolidation.
3. Run the FULL standard audit (engine 194/194; surrogate gate; plane-wave val 0.00e+00; the new + consolidation
   self-tests; compileall; strings clean; orphan check).
4. Bank like any version: real_patterns_vNN renamed forward, ledger entry, banked bullet, queue refresh, surrogate
   banner note, CROSSCHECK_vNN, bethe range bump.
5. TRIPLE-RUN BENCHMARK + IMPROVEMENT CYCLE (added v157): build and run all THREE models -- the surrogate
   (csurrogate.c, pure-arithmetic, no CDet sum), the brute-force frozen reference (engine/, the canonical CDet),
   and the hybrid/production engine (cdet_planewave_engine.c) -- and use the triple run to compare strengths and
   weaknesses on a common-anchor basis (correctness vs the frozen reference / ED, wall-time, coverage/scaling).
   Look for improvements on all three; APPLY them to the EVOLVING models (hybrid, surrogate). HARD SAFEGUARD: the
   FROZEN REFERENCE source is NEVER edited -- editing it destroys the validation anchor; its only "improvements"
   are the existing non-source build variants (make fast / make omp), benchmarked alongside. Any hybrid/surrogate
   change must be verified BIT-IDENTICAL (or strictly better vs the anchor) before adoption -- retest the gain
   (correctness preserved + speedup measured) and RECORD the benchmark table. triple_benchmark.py is the harness.
6. Package + clean-room verify + present.
The point: after a consolidation, a single command re-proves that the frozen anchor is intact and every claimed
capability since the last checkpoint is still live and still agrees with ED, AND all three models have been run
head-to-head with any improvement applied-and-retested against the anchor. Nothing new is asserted about the
physics; everything old is re-verified and the three implementations are re-benchmarked.

## Ceilings found (equally important)
- Locality-pruning the connected-determinant recursion does NOT reduce the per-order 3^n (v22).
  The connected determinant is exponentially local in OUTPUT (folder 04), but pruning the recursion
  by spatial distance fails: keeping 81% of the operations still gives 74% error at order 12, and
  the error grows with order. The small connected value is a cancellation residual of large
  disconnected terms; the long-range terms are individually large and essential to the cancellation.
  So the per-config 3^n is irreducible by locality. The cost lever is reducing the ORDER n (control
  variate / atomic-limit expansion), not pruning -- and locality helps only on the sampling side.
- The endpoint-derivative velocity (eps'(Q)/2pi rho(Q)) is numerically unusable at
  small U (vanishing-point slope on a finite grid). Two attempts confirmed it; the fix
  was to change the quantity (Casimir, integrated), not to grind the extraction. The
  Casimir route is itself accessible-lattice-limited (charge-freezing below U~10 on
  L<=12). Knowing which observable is robustly extractable is part of the method.
- The two-shape effective model for the spin correlator PLATEAUS at ~2.5-2.7%. That
  is the honest ceiling of "interpolate two limits by one scalar." Below it requires
  a second input, trading efficiency for accuracy. Recognizing a plateau is a result.
- The 2k_F/4k_F tower ratio is NOT a clean K_rho probe (v9): it conflates u_rho and
  u_sigma because 2k_F is charge+spin. Not a failure of the measurement -- a property
  of the observable. The pure-charge ratio is the route that stays velocity-free.
- The exact Bethe SPIN velocity via the dressed-energy ENDPOINT slope is numerically
  unreliable at zero field (v14): the spin Fermi point is at Lambda->infinity, so the
  slope is a 0/0 limit at a truncated grid edge (unphysical/negative output). The same
  solver gives the CHARGE velocity fine (finite Fermi point), which proves it is the
  route, not the code. RESOLVED in v18: read the velocity PROFILE's flat PLATEAU at
  moderate Lambda instead of the endpoint -- validated vs the half-filling Bessel curve to
  0.1-0.2%. The endpoint was the mistake, not the dressed-energy formula.
- The integrated (plateau) spin velocity is resolution-limited at small U on the DENSE solver
  (v18): kernels of width U/4 are sharp, the plateau narrows, grid noise overruns it. v20 split
  this into two distinct walls. (a) RESOLUTION (dense-solver-specific) -- cracked: a SPARSE FFT
  fixed-point solver (a_2 convolution diagonal in Fourier, e^{-2u|omega|}) affords a fine grid
  cheaply and reaches small U at HALF filling, validated vs Bessel to 0.1-0.5% (FFT for U<=2,
  dense for U>=2, agreeing at the U=2 overlap). (b) STRUCTURAL (quarter filling, small U) -- not
  cracked, but characterized: the velocity profile rises to a peak then crashes into the noise
  floor with NO plateau, because at low filling + small U the spin density support is too narrow
  to reach the Lambda->inf asymptotic regime. The peak is a rough lower bound only. So exact
  quarter-filling u_sigma below U=2 needs a weak-coupling field-theory handle (v_s = v_F - O(U)),
  not a finer grid -- a structural wall, distinct from resolution and named as such.

## The standing distinction this program keeps
Predicting an observable cheaply is real and useful; the cross-check defines where it
holds. It is a separate thing from reducing the 2^n order sum, which is full rank and
unchanged. Both are true at once: the machinery stays exponential while the observable
is predictable. None of the methods above touches the order-sum complexity, and the
guide does not claim otherwise.

## Banked observables
- EXACT-cheap (Lieb-Wu / Bethe, verified vs ED): double occupancy d(U), energy e0(U),
  and (v5) the charge Luttinger parameter K_rho(U) via the dressed-charge equation --
  both limits exact, ED cross-check 0.1-0.4%.
- EFFECTIVE model (~2.5%, plateaued): spatial spin correlator <S^z_0 S^z_r>(U).
- STRONG-COUPLING-VERIFIED (v6): spin velocity u_sigma via the Casimir energy --
  method verified vs the exact Heisenberg pi/2 (1.5%), Hubbard u_sigma matched to
  2pi/U at U=12 (1%); full curve and charge velocity await larger lattices.
- TOWER-VERIFIED (v7): the finite-size spectrum of the strong-coupling spin sector
  forms the c=1 SU(2)_1 conformal tower -- leading dimension -> 1/2, triplet/singlet
  primary-multiplet degeneracy exact. Bethe = CFT spectrum demonstrated (Moeller Q6).
- VERIFIED ~1-2% (v8): charge velocity u_rho(U) at n=0.5 via flux stiffness + exact
  K_rho; cross-checks the independent Bethe dressed-energy velocity at U=4,8 to ~1%,
  confirmed at L=16. The doped Luttinger liquid (K_rho, u_rho, u_sigma) is now
  characterised.
- SEPARATION-DETECTED (v9): the doped tower ratio R=gap(4k_F)/gap(2k_F) is exact at
  U=0 (R=2.000, K_rho=1) and rises monotonically with U (2.18->2.80 over U=1..8),
  while the single-velocity prediction 4K/(1+K) falls. The rise is a clean, anchored
  signature of spin-charge separation (4k_F pure-charge u_rho; 2k_F mixes u_rho,u_sigma).
  Not a K_rho probe -- a separation probe. Velocity-free K_rho needs the pure-charge ratio.
- DOPED-TOWER-VERIFIED (v10): the doped charge sector's leading PURE-charge primary has
  scaling dimension 2 K_rho. x_4(ED)=gap(4k_F)*L/(2 pi u_rho) tracks 2 K_rho across
  U=0..8; raw deficit ~2-3% (flat in U, finite-size), < 1% after U=0 calibration. Uses
  u_rho (v8) + K_rho (v5); the v9 spin-charge break is resolved by using the pure operator.
  Carries Bethe = CFT spectrum from the spin sector (v7) into the doped charge sector.
- FINITE-SIZE-CONTROLLED (v11): the v10 deficit is finite-size. At the exact U=0 anchor
  (free-fermion gap, exact v_F=sqrt2) x_4 -> 2 as ~1/L^2 (fit x_4 = 2.0000 - 3.3/L^2,
  L=12..44); the L=12 free-fermion gap reproduces the many-body ED gap exactly. The
  doped charge-tower dimension 2 K_rho is now anchored AND finite-size-controlled.
- SEPARATION-QUANTIFIED (v12): both Luttinger velocities from the doped tower. u_rho (pure
  4k_F gap) coincides with the v8 flux stiffness to ~2-3% and rises 1.40->1.90 with U. NOTE:
  the v12 u_sigma (from the 2k_F gap) is SUPERSEDED by v13 -- it was biased up to ~29%. The
  qualitative split (u_sigma falls while u_rho rises) stands; the reliable numbers are v13.
- SEPARATION-CLEANED (v13): u_sigma at quarter filling via the SPIN STIFFNESS (spin twist,
  integrated GS energy) -- independent of the 2k_F gap, exact U=0 anchor (u_sigma=u_rho=
  1.4304). It corrects the v12 extraction (disagrees up to ~29%). Now BOTH velocities come
  from flux stiffness (charge twist -> u_rho, spin twist -> u_sigma): coincide at U=0, split
  with U (u_rho 1.43->1.96, u_sigma 1.43->0.71, ratio 1.0->2.8). Clean spin-charge separation.
- BRACKETED (v14): u_sigma(n=0.5) is pinned between its two EXACT limits, U->0 -> v_F=sqrt2
  and U->inf -> 0, with the v13 stiffness monotone inside. The Bethe machinery is validated
  on the CHARGE velocity (1.92 vs ref 1.93 at U=8); the exact SPIN velocity via the endpoint
  slope is fragile at zero field (Fermi point at Lambda->inf). So u_sigma is robustly measured
  (v13) + exact-limit bracketed (v14); an exact interior curve awaits an integrated Bethe form.
- CORROBORATED (v15): u_sigma(n=0.5) now rests on TWO independent robust ED observables -- the
  spin stiffness (v13, a twist response) and the lowest triplet gap (v15, an excitation energy,
  = a finite-size spin susceptibility) -- sharing only the U=0 anchor. They agree at U=0 and
  bracket u_sigma within ~8-12% across U=0..8, both falling from v_F toward 0; the triplet runs
  low by the SU(2)_1 marginal log correction (which the integrated stiffness avoids, so the
  stiffness stays the trusted value). Confidence in u_sigma is now multi-route, not single.
- EXACT-VALIDATED (v16): at HALF filling the spin velocity is exactly known (Bessel,
  2 I_1(2pi/U)/I_0(2pi/U), limits verified). Testing the two ED routes against it: at every U
  triplet < exact < stiffness, exact CLOSER to the stiffness, stiffness converging with L. The
  bracket method is validated against an exact reference and the stiffness confirmed the better
  estimate AT HALF FILLING. NOTE (corrected by v18): the inference that this bracket TRANSFERS to
  quarter filling (exact between [v15, v13], near v13) was WRONG -- at quarter filling the exact
  u_sigma lies BELOW both ED routes (the bracket structure does not survive doping). The half-
  filling validation stands; the quarter-filling transfer does not. The Bessel result remains the
  validator any general-n solver must reproduce (and v18's plateau solver does, to 0.1-0.2%).
- GENERALIZED (v17): the u_sigma method scales -- the velocity prefactor pi(L/2) hits v_F to
  ~1% at every size (L=6,10,12) and filling (n=0.5, 0.833, 1.0) tested. The stiffness-vs-triplet
  bracket gap is a NAMED, filling-controlled effect (the SU(2)_1 marginal correction): ~7-14% in
  the doped regime, exploding to 17-62% at half filling. So doping HELPS u_sigma (suppresses the
  correction) -- the doped liquid is the easy regime, and the residual gap is bounded and smallest
  exactly where the package operates. Three frame-of-reference tests (size, mechanism, doping) passed.
- EXACT (v18): the quarter-filling spin velocity is computed exactly via the integrated Bethe
  route -- the dressed-energy velocity PROFILE's flat PLATEAU (not the endpoint, which v14 showed
  is singular). Validated against the half-filling Bessel curve to 0.1-0.2% (U=2,4,8). Result
  (U>=2): u_sigma(n=0.5) = 0.951, 0.836, 0.585 at U=2,4,8 -- BELOW both ED routes. So the v13/v15
  ED values are upper bounds (finite-size, L=12), not a bracket; the true u_sigma is ~17% under
  the v13 stiffness at U=8. This closes the u_sigma program and corrects the v16 transfer. Small
  U (<2) is resolution-limited (sharp-kernel wall).
- CROSSOVER (v19): the v18 result generalizes -- the exact u_sigma lies below both ED routes at a
  SECOND doped filling (n=0.833, L=12) too. Across n = 0.5, 0.833, 1.0 the exact-vs-ED ordering is
  one smooth crossover: the STIFFNESS is the upper envelope at every filling (always an
  overestimate, exact/stiffness ~0.75-0.90); the TRIPLET is above the exact when doped but below
  it at half filling (exact/triplet climbs 0.84 -> 0.99 as n: 0.5 -> 0.833, then jumps >1 at n=1
  as the marginal correction collapses the triplet). The half-filling "bracket" (v16) is just the
  doped ordering after the commensurate marginal correction (v17) drags the triplet under the
  exact -- one mechanism, all fillings.
- SMALL-U (v20): a SPARSE FFT fixed-point solver (a_2 convolution exact in Fourier) reaches small
  U where the dense solver could not -- validated at HALF filling vs Bessel to 0.1-0.5% (U=0.5,1,2),
  complementary to the dense solver (agree at U=2). But quarter-filling small U is a STRUCTURAL wall:
  the velocity profile peaks then crashes with no asymptotic plateau (narrow spin-density support at
  low filling + small U). So exact quarter-filling u_sigma stands for U>=2 (v18); U<2 there needs a
  weak-coupling field-theory handle, not a finer grid. One wall (resolution) cracked, a deeper one
  (structural) named.
- BRIDGED (v21): quarter-filling small-U u_sigma, walled to numerics (three routes fail: no plateau,
  recipe-sensitive finite-field read, ED-stiffness slope 6x off), is bridged ANALYTICALLY to leading
  order. u_sigma(n,U) = v_F(n) - U/(2pi) - U^2/(16pi^2) + ...; the leading 1/(2pi) is exact at half
  filling (validated to 5 digits as the Bessel-curve slope) and filling-independent (contact U ->
  momentum-independent backscattering, v_F cancels). So u_sigma(0.5,U) = sqrt2 - U/(2pi) + O(U^2),
  consistent with the v20 lower bounds. Leading-order only: the U^2 curvature is filling-dependent
  (larger when doped) and not transferred. The u_sigma program is complete: exact U>=2 all fillings,
  exact all-U at half filling, leading-order at quarter-filling small U.
- REVERSE DIRECTION (v22): with ED walled (~L=20), going further needs the engine, whose wall is the
  per-order 3^n. First attempt to feed a learned pattern BACK into the engine -- using folder-04
  output-locality to prune the connected recursion -- was TESTED and RULED OUT: pruning that keeps
  81% of the operations is still 74% wrong at order 12, because the connected value is a cancellation
  residual (long-range terms individually large, only the full sum cancels). Output-locality is not
  term-locality. The productive lever (v23) is reducing the ORDER n -- a control variate from the
  learned IR physics (exact K_rho power law, velocities, CFT tail) and/or expanding around the atomic
  limit (the engine ships G_exact_atom) -- since cost ~ 3^n makes each saved order worth 3^(delta-n),
  and neither fights the cancellation. Locality still helps, but on the sampling side (confine the
  vertex integration to compact configs), reducing variance not per-config cost.
- TWO-ENGINE + EXP 1 (v23): the engine-acceleration arc now runs under the same discipline as the
  physics. `engine/` is the FROZEN baseline oracle; `engine_exp/` the sandbox; fork checked bit-
  identical (orders 1,2). Experiment 1 (atom, anchored on the baseline's exact G_exact_atom): the
  bare U=0 engine expansion has convergence radius ~0.94, so at U=2 it DIVERGES (order-12 partial
  sum +2799 vs exact -0.444); a resummation of the same orders (Pade, pole-structure-informed)
  converges (-0.4443), and at U=0.5 reaches 1.2e-10 vs the bare 2.9e-5. So the order needed is set
  by the expansion SCHEME -- the order-reduction lever is real, validated against the exact anchor.
- QUANTIFIED (v24): on the exactly-solvable dimer (E0=(U-sqrt(U^2+16t^2))/2, verified vs ED), the
  bare U-series (radius 4t) and the atomic/hopping series (radius U/4) have RECIPROCAL radii ->
  complementary: bare for U<4t, atomic for U>4t. Cost ~3^n, so gain = 3^(N_bare-N_atomic). At strong
  coupling (U>4t) the bare series DIVERGES (infinite cost; 12-order sum = +126 vs exact -0.472 at
  U/t=8); the atomic scheme converges with cost 3^N_atomic that SHRINKS as U/t grows: 3^24, 3^16,
  3^10, 3^8, 3^6 at U/t = 6, 8, 12, 16, 32 (eps=1e-6). So the gain is qualitative at strong coupling
  (impossible -> feasible), cheapest deep in strong coupling; the crossover U~4t is the hard seam
  where both are marginal and a resummation (Pade, v23) is needed.
- STRESS / WALL (v25): stress test of C_V on both engines (shared recursion). Measured cost: RAM =
  2*2^n*8 bytes exactly, time ~x2.4/order (n=16: 1.05 MB, 1.26 s; n=21: 33.6 MB, 93 s). On a 3 GB
  box the RAM wall is order 27 (2.0 GB), but the 3^n time wall hits first (~n=24 in minutes). The
  frozen-baseline discipline surfaced two HIDDEN fixed-buffer caps (sub[16], MAXDIM=18), raised and
  validated bit-identical in engine_exp. How much faster: the atomic scheme converges at order 16
  (1.26 s, 1.05 MB) while the bare scheme diverges and never converges even at the 3 GB / multi-hour
  ceiling -- convergence-within-the-wall, not a percentage.
- BUFFERS GONE + CRASH-SAFE (v26): removed every fixed order buffer from engine_exp's recursion
  (sub[n], M[m*m], rs[n+1] VLAs; MAXDIM deleted; C_V mallocs checked -> NaN, no segfault). Validated
  bit-identical to the frozen baseline at n<=16, 194/194, now runs uncapped. Buffer-free wall (4 GB
  box): time wall first (~n=20-24), RAM guard at n=28 -- a genuine resource wall, not a code cap.
  stress_cv.c (v26) is crash-safe by default: per-row fflush to a log, RAM-budget guard (graceful
  stop before OOM), async-signal-safe SIGINT/SIGTERM handler; TESTED by a real mid-call interrupt
  (log kept n=1..18). Honest scope: this is the buffer-free + crash-safe INFRASTRUCTURE; the full
  general-lattice atomic series is still gated by the missing high-order time-integration driver.
- HIGH-ORDER GATE OPENED (v27): built cdet_order_mc (engine_exp/diagmc.c) -- general-n time
  integration by Monte Carlo over vertex times+sites, same integrand as cdet_order. VALIDATED against
  the frozen baseline at n=1,2 within MC error (n=1: -0.5077 +/-0.0022 vs -0.508275, +0.25 sigma;
  n=2: 0.44092 +/-0.0035 vs 0.440405, +0.15 sigma; error ~1/sqrt(nmc)). First high-order terms
  (baseline NaN): n=3 = 0.008 +/-0.006, n=4 = -0.341 +/-0.008. New wall = MC sign-variance growing
  with order (the sign problem), which is what the atomic reference reduces. stress_cv.c RAM guard
  raised 85%->90%.
- CONTIGUITY / SUBSET CONVOLUTION (v28): the 3^n scattered submask sum is a subset convolution;
  zeta/Mobius butterfly does it in O(2^n n^2) with contiguous (no scatter/gather) access (Bjorklund
  STOC 2007; det-DiagMC recursion is O(2^n n^3 + 3^n), Rossi PRL 2017). POC (engine_exp/
  subset_conv_poc.c) confirms correctness (~1e-12 vs naive) but for our regime it is SLOWER at
  reachable n (crossover ~n=20-22), uses MORE RAM (n+1 ranks -> O(2^n n)), and loses ~7 digits
  (Mobius +/-) on data we compute as cancellation residuals. Real payoff: contiguity is what makes
  out-of-core/blocked streaming feasible past the RAM wall; within RAM, reducing n (atomic ref) is
  the penalty-free lever.
- IN-RAM CROSSOVER + PRECISION (v29, corrects v28): re-measured past n=18 -- the fast butterfly
  subset convolution's in-RAM wall-time crossover is n=19 (n=20: 1.74x, n=21: 2.70x, growing). Cost:
  ~(n+1)/2x more RAM (popcount ranks), so its RAM wall is a few orders earlier (~n=24 vs ~n=27). The
  accuracy loss is catastrophic cancellation (grows with n, 9e-13 -> 6e-9 over n=12..21), NOT a fixed
  ratio: long double recovers it 4-14x, proving recoverable rounding. The MC control variate can't fix
  deterministic cancellation, but the control-variate PRINCIPLE = the atomic reference (shrink the
  residual at source). So the rewrite is a usable speed tool in the n~19-23 window (precision via long
  double, memory cost accepted); it does NOT reach higher orders. Reducing n stays the real lever.
- ATOMIC-REFERENCE LEVER QUANTIFIED (v30): on the Hubbard atom (oracle = closed-form G_exact_atom,
  confirmed vs the C engine), a reference shifted toward the correlated regime cuts the order to 1e-6
  at U=2 from NEVER (bare diverges, |U_sing|=0.9415) to 11 (U0=1.5) or 3 (U0=1.9), AND shrinks the
  largest single term from 3.8e12 to ~0.2 -- the same shift removes the catastrophic cancellation
  (v29 cure). The lever's payoff is exact and large; the counterterm-correct wiring into
  cdet_order_mc is the remaining C build (scheme validated: atom here, dimer v24).
- OUT-OF-CORE BLOCKING (v31, engine_exp/blocked_cv.c): the scattered O(3^n) submask recursion
  factorizes over a bit-split mask=(h,l) into a block-level subset recursion -> schedulable HDD<->RAM
  streaming. Validated: matches flat C_V to ~1e-20 (EXACT, no Mobius -> full accuracy), peak RAM fixed
  at 3 blocks = O(2^nL) independent of n (43x-171x less at n=12-18, grows without bound; 2^n on disk).
  Accuracy-first, RAM-bounded, HDD-overflow path (cost: total block I/O ~3^nH, time-heavy by design).
  Corrects the earlier 'out-of-core hopeless' claim. Butterfly shelved (wrong trade for accuracy+RAM).
- CONTROL VARIATE, low vs high order (v32): the user's two-version idea = the control variate, already
  in 02_control_variate (71x at n=4, rho=0.993; reduction 1/(1-rho^2) is set by CORRELATION not
  accuracy -- an 11.7%-accurate surrogate still gives 71x). Tested at high order
  (engine_exp/cv_highorder.c): simple parametric references (decoupled/shifted-mu/weak-hop)
  DE-CORRELATE (|rho|<=~0.7, ~1-2x) because the high-order connected value is a sign-oscillating
  residual. So CV is proven low-order; high-order needs an ADAPTIVE/LEARNED surrogate (TCI-like), and
  high correlation there is the open problem. It is COMBINE not flip; the butterfly is not a CV partner.
- LEARNED-PATTERN REFERENCE as observable-level control variate (v33): the custom analytic surrogate
  built from the engine's patterns (Lieb-Wu analytic moment -> correlator shape; K_rho; velocities;
  CFT tail) has rho=0.998 with the exact ED spin correlator over a (U,r) grid -> 229x variance
  reduction (learned_reference_cv.py), ~100x stronger than v32's per-sample parametric references.
  Resolves v32's 'need a new surrogate': it overlooked a custom reference at a DIFFERENT (observable)
  level. Gap: this is the spin correlator; the DiagMC Green's-function reference (Luttinger-liquid G
  from K_rho + velocities, both in hand) is constructible but not yet assembled/subtracted.

- CONFIG INTEGRATION of the validated accelerations (v34): one driver cdet_order_mc_cfg
  (engine_exp/cdet_config.{h,c}) with switchable modes -- CDET_PLAIN (bit-identical to cdet_order_mc),
  CDET_BLOCKED (v31 out-of-core C_V per sample, == PLAIN to 1.1e-12, peak RAM ~3*2^nL), CDET_CVAR
  (shifted-mu control variate, unbiased: 1.46 / 0.16 sigma from the frozen baseline). CVAR rho=0.98/0.92
  -> potential 27x/6.5x IF E[Y] exact, but NET=1.00x with an MC-estimated mean (pilot variance offsets
  the gain) -- net-win awaits an analytic reference mean. Butterfly excluded (shelved). Also: a quad.c
  np>64 stack overflow (fixed-size double[64] node arrays) was found and FIXED in engine_exp (sized to
  np, bit-identical for np<=64); it had produced a garbage cdet_order value (np=120) that looked like an
  MC/cdet_order discrepancy -- gate 4 now confirms MC == cdet_order across two param sets and n=1,2
  (<1 sigma). Validator engine_exp/cdet_config_validate.c, all 4 gates pass.

- BASELINE REFRESH (v35): the frozen baseline engine/ was deliberately updated to the validated best
  version by promoting cdet_engine.c (v26 dynamic buffers + OOM-safe) and quad.c (v34 np-sized nodes)
  from engine_exp/. Every frozen constant is UNCHANGED to the last digit (cdet_order(1,2), C_V n=8,12,16
  above; 194/194), proving the refresh moved no number; it removed the n<=16 and np>64 caps (n=17,18 and
  np=96 now run) and added OOM-safety. 'Pristine = has the caps' is retired; the baseline invariant is
  now 'reproduces the constants + Python ref AND is buffer-free/OOM-safe.' engine/ core == engine_exp/
  core; engine_exp/ adds the experimental tools.

- BEGIN 2D INTERACTING (v36): the connected-determinant engine, validated in 2D at orders 1,2 against
  exact diagonalization of the 2D Hubbard model. cdet_order(n)=N*a_n (a_n = U^n Taylor coeff of the
  exactly-diagonalized local G) to ~1e-9 at n=1,2, SAME convention in 1D and 2D, prefactor=N confirmed
  for N=2,3,4,5; free 2D G0 re-validated (3.4e-9 vs numpy ED); capstone G(U) reconstruction with U^3
  truncation error. 08_2d_interacting/ (cdet2d.c, cdet_small.c, hubbard_ed.py, validate2d.py). METHOD
  ANCHOR not physics: 2x2/small rings, orders 1,2 only; higher orders + the sign problem are v37+.

- 2D HIGH-ORDER MC (v37): mc2d.c (geometry-blind MC, any lattice) reproduces exact 2x2 Hubbard
  coefficients cdet_order(n)=N*a_n at n=1..6, every order <2 sigma (a_n exact via Cauchy contour,
  hubbard_ed.exact_coeffs). Orders 5,6 are past deterministic quadrature's reach. Sign-problem wall
  measured: R=mean/|mean| and Nsamp->1%~1/R^2; 2x2 benign (7e5) -> 4x4 ~260x, beta 2->8 on 3x3 ~570x.
  08_2d_interacting/ (mc2d.c, mc_validate.py, characterize_sign.py). Correctness + wall map; NOT a
  sign-problem solution, NOT a CDet-vs-naive-expansion comparison.

- DETERMINANT BUYS ORDER REACH, NOT SIZE/T (v38): measured on the engine's actual Wick matrices.
  Cost (n+1)! vs O(n^3) (determinant is the only way past ~order 5; 5e9x by order 15); per-order
  cancellation perm(|M|)/|det| a contraction-sampler suffers grows with ORDER on every cluster
  (~1.5^n on 2x2, ~1.13^n on 4x4) and is removed exactly by det. BUT at fixed order it SHRINKS with
  cluster size (3.11->1.23 for N=4..16) -- opposite to the v37 configuration-level wall (grows with
  N, beta). Two different walls; the determinant addresses the per-ORDER one only. 08_2d_interacting/
  (cdet_vs_naive.c, buy_orders.py). Mechanism isolation, NOT a wall-clock-vs-competitor benchmark.

- R SCALING LAW (v39): the metric (fit R's decay, not order reached) is right, but at accessible sizes
  (N<=25, order 3) the per-order R has NO clean law: fixed-density size axis plateaus (L=3~L=4 |R|~0.35)
  then collapses (L=5 ~0.05), not exponential (R^2~0.87); the temperature exponent's SIGN is ensemble-
  dependent (fixed-mu +0.35 R^2=0.98 = density-drift artifact; fixed-density -0.05); separable
  e^{-(aN+b*beta)} fails a 29-sigma off-axis prediction. No honest (a,b) reported. Corrects v37's fixed-mu
  beta-trend (conflated temperature with density). 08_2d_interacting/scaling_law.py.

- AGGREGATE OBSERVABLES DON'T DECONTAMINATE (v40): tested the candidates proposed as cleaner than per-
  order R. Integrated-over-orders average sign still sign-alternates with cluster (single-order domination:
  weights U^n N(N beta)^n/n! are non-uniform, one order dominates); n* and R_n inherit a_n shell jumps;
  R(mu) oscillates within one cluster. Contaminant = partial-shell FILLING at small N; cure = fixed filling
  fraction (closed shells) or large N, both out of reach. Free-energy differences not tested (different
  computation). 08_2d_interacting/ (isign.c, robust_observables.py). A measured limit, not a benchmark.

- ORGANIZING VARIABLE = SHELL DETUNING (v41): the per-cluster R 'shell noise' of v39/v40 is a UNIVERSAL
  function of the Fermi detuning delta=mu-(nearest shell) at fixed T: positive below the shell, peak at
  delta=0, sign-flip just above -- same in L=2,3,4, with amplitude A(N)=0.82,0.60,0.50 shrinking with N.
  R-vs-N looked random only because clusters sat at different delta. Diagnostic = R(delta), refining v40's
  'no diagnostic'; the controlled comparison is fixed delta (quantitative 'fix the filling'). Honest bounds:
  magnitude collapse clean only near the shell; temperature is a SEPARATE axis (beta*delta is not a single
  variable). 08_2d_interacting/shell_collapse.py.

- HIERARCHY OF SCALES IN R (v42): R(delta) = a near-shell THERMAL feature (range ~ T=1/beta; sign-flip
  delta* ~ T across beta=2,4,8; shape collapses vs beta*delta on an isolated shell) + a cluster-specific
  band-structure background (dense-spectrum clusters, the wings). Explains v41 (fixed-beta delta-collapse =
  the thermal piece dominating) and why beta*delta is not a global variable (background breaks it).
  Hierarchy T < shell spacing < bandwidth 8t. 08_2d_interacting/scales.py. Structural multi-scale result;
  the 'forces' analogy is structural only, NOT physics.

- THERMAL CLAIM PARTLY CORRECTED (v43): v42's 'near-shell feature is thermal' upgrade-tested. Test C
  (finite-size + temperature) PASSES: delta* N-independent (0.24,0.26,0.21 for N=4,9,16) and ~ T
  (0.61,0.24,0.11 for beta=2,4,8) -> thermal-consistent width, not shell-spacing. Test A (order cutoff)
  FAILS: feature shape/sign/crossing change with order (n=1 monotonic, n=2 peak at 0, n=3 peak at +0.2),
  so no single feature is broadened. NET: narrowed to 'the n=2 feature WIDTH is thermal-consistent';
  thermal ORIGIN underdetermined. v41 organizing-variable result stands. 08_2d_interacting/thermal_tests.py.

- LITERATURE MAP (v44): the v36-v43 'separate walls' are documented, connected facets of one sign problem.
  v38->Rossi PRL 119 045701 (2017); v37->DQMC <s>~e^{-aN}e^{-b beta} (arXiv 2509.18075, 2112.09209,
  Troyer-Wiese); v41 shell-detuning->closed-shell 'magic density' sign effect (arXiv 2108.00553, 1107.0230);
  v42/v43 thermal width->compressibility-tracks-sign (1107.0230) + sign<->criticality (Science 375 418 2022);
  v36 radius->complex-coupling poles (Wu-Ferrero-Georges-Kozik PRB 96 041105 2017; arXiv 2303.01607). Already
  unified in 'Geometry Dependence of the Sign Problem' (arXiv 1501.02832) and Science 2022. Program = faithful
  independent rediscovery, not discovery. 08_2d_interacting/LITERATURE_MAP.md.

- SHIFTED-REFERENCE CDet (v45): H(xi;alpha)=[H0+alpha N]+xi(U Hint-alpha N), physical at xi=1 for any alpha;
  alpha moves the pole. EXACT-verified: 2-site bare DIVERGES, shifted(alpha*~Hartree) converges at order 5
  (1e-3), 2e-5 by K=12; Hubbard atom bare radius~1 -> shifted~1.8. Cost ~2^(K_bare-K_shift) (divergent->order5).
  alpha* ~ U<n>/2 (Hartree) = the v41/v44 detuning knob; operating point sets delta=0 (best sign), shift sets
  reference Fermi level. 08_2d_interacting/shifted_expansion.py. Coefficient-level exact; MC counterterm = v46.

- COUNTERTERM = d/dmu (v46): shifted CDet coeffs from bare engine data, no engine surgery.
  b_n = sum_j (alpha^j/j!) U^(n-j) a_{n-j}^{(j)}(mu-alpha). Formula vs ED shifted: machine precision
  (1e-12..1e-17, orders 0-6). REAL engine (cdet_small, cdet_n=N*a_local; divide by N) -> shifted: b1 6e-6,
  b2 4.5e-5 (quadrature+FD limited). Bare diverges yet resummed shifted converges from low-order engine
  coeffs (K=5 err 6e-4). 08_2d_interacting/counterterm_shift.py. Frozen engine untouched (194/194).

- FULLY STOCHASTIC SHIFTED CDet (v47): mu-derivatives sampled DIRECTLY in one run via a complex-mu contour on
  shared samples (= analytic d/dmu insertion; no FD bias, no mu-grid). C_V is a Python port of the engine
  (G0, a_1 validated to 1e-16). 2-site ring: a1/a1'/a2 within 0.3 sigma of ED (a1' cross-checked vs ED),
  shifted b1,b2 within 0.3 sigma of ED shifted. 08_2d_interacting/counterterm_sampler.py. Reference impl
  (orders 1-2); C-mc2d port unshipped; frozen engine untouched.

- SIGN vs CONVERGENCE TRADE-OFF (v48): the shift's knob mu_ref has competing optima. 2x2, mu=0.5, U=4, beta=4:
  convergence-optimal alpha_conv=+1.5 (mu_ref=-1.0, Hartree; err@K8 5.6e-3) but |R_2|=0.05 (worst); sign-optimal
  mu_ref=0.0 (closed shell) |R_2|=0.82 but err@K8 6.3e-2. Confirmed orders 2-4. Convergence<->complex-U pole,
  sign<->real-axis shell: different physics, different optima -> pole-moving does NOT move the sign wall.
  08_2d_interacting/sign_tradeoff.py. Single case; genericity not proven (v50).

- CONTOUR DEFORMATION IS NULL ON THE SIGN (v49): deformed the genuine v48 integrand (2x2, mu=0.5, U=4,
  beta=4) via cdet_port (bit-identical to the frozen ring port). Sign/var-optimal contour amplitude = 0
  (the real axis); integral invariant to 0.0e+00. Within each kink-pinned sector R=1; the cancellation is
  DISCRETE between sectors, where no pinned smooth contour can reach. Reason: our sign is a real sign-flip,
  not a complex phase -> deformation makes only a zero-integral imaginary part. 08_2d_interacting/
  CONTOUR_DEFORMATION_RESULT.md, contour_deformation.py. Frozen engine untouched.

- COVARIATE FROM DEFORMATION IS NULL; CEILING ON THE FAMILY (v49): the contour invariance gives unbiased
  estimators of one mean -> zero-mean covariates with A=0 as comparator. Optimal combo x1.00 (deformed Re
  rigid to 1e-15, perfectly correlated). General ceiling: control variates reduce variance, never R, so the
  covariate family moves the PREFACTOR only. The free-baseline CV (subtract U=0, sample remainder) is the
  one that pays -- weak-U range reduction x8.4->x1.5. 08_2d_interacting/best_methods.py, BEST_METHODS.md.

- BEST-METHODS CONSOLIDATION (v49): the three verified, composable accelerations in one exact-checked place
  -- shifted reference (convergence; bare diverges->shifted converges, K=11 err 1e-5), complex-mu contour
  (derivatives; matches direct shift to 6e-14), free-baseline control variate (prefactor; weak-U win).
  Each moves a DIFFERENT axis; none moves R. 08_2d_interacting/best_methods.py + BEST_METHODS.md.

- EXACT SYMMETRY REDUCTION OF THE SITE SUM (v50): the involution search found no sign-canceller (ratio never
  -1) but a real symmetry: 2x2 stabilizer of the external site |G_0|=2 (diagonal swap), C_V(sigma x)=+C_V(x)
  to 1e-8. Folding the L^n site sum by G_0 is exact (match 6.6e-17) with |G_0|=2x fewer C_V evals as n grows
  (1.60x/1.78x/1.88x at n=2/3/4). Symbolically proven for all hopping t (sympy: P^T H P - H = 0, [P,H]=0).
  Redundancy removal only -- identical sign within an orbit; folds the site space, NOT the Rossi 2^n or the
  sign. Grows with lattice symmetry. 08_2d_interacting/symmetry_reduction.py + symmetry_audit_sympy.py.

- POINT-GROUP FOLD SCALES WITH THE LATTICE (v51): on 4x4 the stabilizer of the external site is the full D4
  (|G_0|=8, incl. column/row-slice reflections); folding the L^n site sum is exact (3.3e-16) giving 4.65x
  (n=2) -> 6.15x (n=3) -> 8x fewer C_V evals, vs 2x on the 2x2. All eight ops FOLD (ratio +1 to 1e-10); none
  CANCELS (-1). Proven for all t (sympy). square_point_stabilizer() (generator-based, no L! enumeration).

- 45-DEGREE CUBE SLICES FOLD; THE FOLD SCALES WITH DIMENSION (v52): 4x4x4 cube stabilizer of the external site
  is the full O_h (|G_0|=48; 40 of them are 45-deg diagonal slices). All diagonal slices FOLD (+1 to 1e-10),
  none CANCELS (-1); proven for all t (sympy, axis-swap identity). Folding the N^n=64^n site sum by O_h is
  exact (5.2e-15) giving 18.62x fewer C_V evals at n=2 -> 48x. Fold = little-group order, growing with size AND
  dimension: 2x -> 8x -> 48x. cube_hopping()/cube_point_stabilizer().

- SUBSET CACHE COMPOSES WITH THE ORBIT FOLD (v53): D_vac/D_corr keyed on the vertex subset, memoized across
  the enumerated site sum: n=3 4x4 matches brute to 5.0e-15 with 29.9x fewer determinant evaluations
  (orbit 6.15x x cache 4.86x), 13.9x wall-clock. Interior mask-fold inside one C_V verified exact on
  symmetric configs but measure-zero generically (honest negative). cv_cached/fold_site_sum_cached.

- VALUE CHANNEL + SLICE HIERARCHY (v54): PH transpose carries the hunted -1 off-diagonal (2.5e-11) but the
  equal-time sum rule G(-mu)(i,i,0)+G(mu)(i,i,0)=1 (1e-15) dresses it into an operator identity with a density
  counterterm tower -- no per-config -1 at fixed mu (both naive forms failed by computation). Cube slice mine:
  1d configs carry x18.5 their weight share at R=0.22; 2d x2.1 at R=0.09; 3d bulk x0.65 at R=0.004. v55
  candidate: slice-stratified evaluation. value_channel_slices.py + VALUE_CHANNEL_SLICES_RESULT.md.

- SLICE-STRATIFIED ESTIMATOR (v55): stratify by exact span-dim label, enumerate heavy small strata, Neyman-
  sample the rest. n=2 cube vs exact truth: 22-44x variance cut at matched budget, bias <=0.5 sigma; n=3 with
  unenumerable heavy strata: 2.1x (few reps). Gain ~ concentration relative to budget; always unbiased.
  slice_stratified.py + SLICE_STRATIFIED_RESULT.md.

- GENERICITY CLOSED (v56): sign-vs-convergence optima are SEPARATED at every doped filling (beta=4 gaps >=1.0,
  R2 0.01-0.40 vs peak 0.82; beta=8 doped gaps 1.0-1.5) and ALIGN exactly only at half filling mu=U/2 at low T
  (mu_ref=0.0 = peak, R2=0.91, gap 0.00; forced by particle-hole symmetry: alpha_Hartree=U/2 maps to the
  shell). Metric-artifact alignment at mu=1.0 caught by the failing self-test and retracted on the record.
  genericity_search.py + GENERICITY_RESULT.md.

- SLICE HIERARCHY SURVIVES SCALE (v57): 1d/bulk per-config weight ratio GROWS 32x -> 74x -> 165x at L=4,6,8
  (FastCDet, validated 4.2e-17, makes 512 sites reachable); R(1d) 0.65 -> 0.24 vs bulk at/near floor (L=8
  anomaly flagged). v54's d=1 R refined (12-config noise -> 0.652 targeted). The weight lives in a growing,
  geometrically identifiable low-dim sector. slice_scaling.py + SLICE_SCALING_RESULT.md (sign half amended v58).

- WEIGHT UNIVERSALITY ROBUST; SIGN CLAIMS DOWNGRADED (v58): median 1d/bulk ratio 11x-184x across order/
  temperature/filling/observable, seed-stable; U exact by theorem. R-based per-class sign hierarchy exposed as
  heavy-tail estimator-fragile (0.44 vs 0.02, same cell/seed, 500 vs 400 samples) -- v54/v57 sign statements
  OPEN pending tail-aware statistics. slice_universality.py + SLICE_UNIVERSALITY_RESULT.md.

- DECAY-LAW DERIVATION FALSIFIED (v59): exponential form in L confirmed; MST geometry real but minor
  (R2=0.17, slope half of -1/xi); frozen-slope zero-parameter prediction under-predicts measured class ratios
  by 5-10x (3/5/7x vs 16/62/30x at L=4/6/8). Concentration mechanism UNIDENTIFIED; 1d class is an axis/diagonal
  mixture needing stratification. decay_law.py + DECAY_LAW_RESULT.md.

- DUAL MECHANISM (v60): tau-interference = 40% of var(ln|C|); integrating tau out doubles the MST law
  (R2 0.18->0.48). Anisotropy measured (xi 0.90 axis / 1.21 face / 1.20 body per Euclid at L=8) but the
  anisotropic metric does not close the prediction gap (6.8x vs 75.5x). Body-diagonal anomaly: longest lines,
  heaviest weight. Residual ~10x closed-line enhancement unexplained; ring-closure coherence hypothesis banked
  for v61. dual_mechanism.py + DUAL_MECHANISM_RESULT.md.

- WINDING-PHASE RING CLOSURE FALSIFIED (v61): antiperiodic twist (|H| bit-identical, only winding phase
  changes) leaves paired per-config line weights within ~±40%, axis-blind, no mirror -- the ~10x line
  enhancement is closure-independent. The unpaired version of the same experiment faked a 4x effect first
  (heavy-tail artifact, caught by pairing). Refined hypothesis banked untested: 1d channeling.
  ring_closure.py + RING_CLOSURE_RESULT.md.

- 1D CHANNELING CONFIRMED (v62): at matched MST with identical tau draws and exact anisotropy control,
  line/bent = 1.8-2.0x, line/zig = 1.9-2.4x, bent/zig = 1.3x -- monotone in collinearity. Third confirmed
  mechanism. Ledger: distance + tau-interference + anisotropy + channeling confirmed; winding falsified;
  ~4x of the ~75x class gap still unaccounted. channeling.py + CHANNELING_RESULT.md.

- MECHANISM CLOSURE LOCKED (v63): channeling compounds with length (c=+0.583/unit, paired-identified);
  distance b=0.537 (bulk-identified, l_coll=0); frozen composition 59x vs measured 75.5x = 1.27x agreement,
  within the pre-set 2x gate. Two fitting traps (spurious single-vertex credit; multicollinearity) caught and
  banked. Open: derive c. mechanism_closure.py + MECHANISM_CLOSURE_RESULT.md.

- GENERICITY LAW SPLIT (v64): alpha*=U/2 at half filling is UNIVERSAL (2 clusters x 3 couplings) and
  quasi-exact (6-ring err@K8 = 8.6e-6, five orders below any other shift; blocked sector ED validated 4.8e-07
  vs dense, ~150x faster). Sign alignment is CLUSTER-DEPENDENT: fails at half filling on the 6-ring (R 0.14
  at the PH point vs peak 0.51 at -1.0) exactly as predicted before the run -- v56's alignment was a 2x2
  coincidence. genericity_cluster.py + GENERICITY_CLUSTER_RESULT.md.

- BASELINE CONSOLIDATED (v65): cdet_best.py composes the verified stack (BestCDet 2.8e-17; fold x cache exact
  to 2.7e-15, 13x measured, 16384->578 determinants; stratification; the split shift law with its sign caveat;
  the concentration-law constants). BEST_METHODS.md v65 edition = composition table + two laws + standing
  methodology. The wall statement unchanged: R untouched at fixed mu.

- NO-BRUTE-FORCE SIMULATOR (v66): geometry surrogate (OOS R2 0.75) reproduces the v54 brute weight-share
  table with ZERO evaluations (within ~5 points/class) and guides small-budget estimation to 33x where the
  sign is mild (n=2); at the cancellation-dominated n=3 it gives no gain (0.7x) -- the wall as an estimator
  theorem. Exact n=3 truth (262,144 configs) in 11 s via the consolidated stack (168x fewer determinants).
  surrogate.py + SURROGATE_RESULT.md.

- SIGN MODEL (v67): r_g bootstrap CIs separate 1d/2d (0.70) from bulk (0.34) -- v58 question settled at the
  tau-integrated level; line-sector sign 92% predictable; d<=1 sector (0.3% of configs) carries 77% of the
  exact signed total; hybrid estimator unbiased at 0.46% budget. [GAIN CORRECTED v70: true ~6x by exact
  moments; the banked 87-110x was a lucky-baseline artifact.] A frozen-subsample 231x reading rejected.
  sign_model.py + SIGN_MODEL_RESULT.md.

- SECTOR ESTIMATOR (v70): coherent sector polynomially small by construction (3,774 of 10M at L=6); exact
  strata counts vectorized; exact-moment design analysis (new standing rule) corrected v67's gain to ~6x and
  decomposed uniform's noise (96% = sector rarity); L=6 exact sector sum NEGATIVE -- the v68 phase flip in
  exact arithmetic. sector_estimator.py + SECTOR_ESTIMATOR_RESULT.md.

- PAIRING DEPTH (v71): the orientation phase has NO finite pairing depth -- the COMPLETE single free
  determinant fails (OOC 44%, identical in the engine-matched time convention); by elimination the phase
  lives in the coupled two-spin determinant product over shared times: the engine integrand itself. Ladder
  complete: parity -> static -> chain -> any-depth determinant, all falsified frozen. Surrogate consequence:
  orientation must be a LEARNED channel if at all. pairing_depth.py + PAIRING_DEPTH_RESULT.md.

- BULK REMAINDER = FRIEDEL RINGS (v72): exact shell decomposition shows alternating-sign MST shells
  (+,-,+,- at mu=0.5; pattern shifts to -,-,-,+ at mu=1.5, net 6x larger), mid-range dominance (58%),
  2.3x inter-shell cancellation; frozen monotone-decay prediction falsified by its own gates -- the
  falsification is the discovery. bulk_remainder.py + BULK_REMAINDER_RESULT.md.

- LEARNED ORIENTATION CHANNEL CLOSED (v73): logistic 33% / MLP 35% held-out vs the 75% gate (train 74%
  both) -- anti-prediction at unseen mu because A PHASE WRAPS and smooth models cannot interpolate a wrap;
  the channel is closed from both directions (derived v69/71 + learned v73); remaining routes: tabulation,
  engine features, or the mu-period analytically. learned_orientation.py + LEARNED_ORIENTATION_RESULT.md.

- SURROGATE v2 (v74): ceilings measured first (mag 0.95; r_g 0.40/0.57 -- the old 0.32 was ~80% of ceiling);
  v66's R2=0.75 scope-corrected as mixture-flattered (median error 1.7x stands); TRANSFER is the gain
  (L=4->L=6 R2 0.33->0.57, med-err 2.88x->1.81x, 10 linear features, 8-shot intercept); r_pred regime map:
  +0.32/+0.27/-0.57 within rank 1/2/3 -- predictability lives where coherence lives.
  surrogate2.py + SURROGATE2_RESULT.md.

- THE L=6 SHELL FOLD (v75): wrap-collinearity correction (min-image collinearity ill-defined on even-L tori;
  true sectors 1,618/82% at L=4 and 16,950 at L=6 -- the v67/v70 sets were wrap-blind subsets); FIRST EXACT
  10M-config totals (mu=0.5 -2.498377e-3, validating the v70 pilot dead-on; mu=1.5 -2.224768e-3); sector
  share 82% -> 42% with size and OPPOSES the total at mu=1.5; rings persist with mu-dependent nodes; period
  unresolved (irregular 0.5-1.5 spacings vs predicted ~1.1-1.2). shell_fold.py + SHELL_FOLD_RESULT.md.

- RING PERIOD (v76): not resolved at L=6 and cannot be (xi_s/period ~ 2.5: ~2 oscillations before
  decoherence on ~5 usable radii); binned R_max near-miss (within 10% of 2kF, correct mu-shift) KILLED by
  permutation null (p = 0.20/0.16); contact-shell coherence real and mu-flipped (+0.66 / -0.53); route =
  larger L + coherence-boosted observables (v68 line protocol). ring_period.py + RING_PERIOD_RESULT.md.

- THE MU-PERIOD LAW (v77): Delta-mu* = pi/(q beta), q = 1.12/1.05/0.98 at beta = 4/6/8 -- charge-1 fugacity
  winding, R- and L-independent; Friedel falsified on pre-registered gates (spacing R-independent, winding
  5x faster than 2 kF R, beta-dependent); r_g dips at flips (physical zeros); the channel half-reopens
  (73-76% at the 75% bar; offset calibration is the residual, engineering not law-finding); beta >= 12
  protocol boundary; initial 79% claim downgraded by the seed sweep before banking.
  mu_period.py + MU_PERIOD_RESULT.md.

- THE COMB (v78): cancellation lemma -- <C>_tau is EXACTLY rational in z = e^{beta mu}, poles only at
  z = -e^{beta eps_k} < 0, i.e. Matsubara combs mu = eps_k + i(2m+1)pi/beta; detected DIRECTLY by complex-mu
  continuation (3.9e6-fold at-level divergence at y -> pi/beta vs x12 between levels; Cauchy-Riemann 6e-4);
  the charge-staircase reading (ours and the outside heuristic) falsified by flat ln|C| slopes; mechanism =
  comb-limited variation, deriving 1/beta scaling and R/L-independence; refined open item: the exact
  constant. fugacity_structure.py + FUGACITY_STRUCTURE_RESULT.md.

- CONSOLIDATED SURROGATE (v79): cdet_surrogate.py = wrap-safe sector + transferable magnitude + regime map +
  period-based orientation channel, scopes stated at point of use; BEST_METHODS v79 edition (component table,
  the phase arc closed, nine methodology rules). Integration-as-audit found two refinements: transfer is
  pooled 1.88x across draws (1.74x/2.69x; the v74 1.81x was the favorable end), and per-class intercepts
  were tested and rejected (offset diff 0.16; 8-shot LINE intercept consolidated).
  cdet_surrogate.py + BEST_METHODS.md.

- THE RESONANCE REGIME (v80, KT-review round): the v77 beta>=12 "unmeasurable" boundary RETRACTED -- the
  disagreement was two real scales (intra/inter-cluster). Two-regime law proved: flips attract to levels
  (p = 0.025 at beta = 12/16) and become GEOMETRY-INDEPENDENT (cross-geometry distance 0.020-0.025,
  p = 0.013-0.041, both L) at large beta; fine-grid Phase-0 reversal (beta=4 spacing 0.625, q ~ 1.26);
  naive midpoint law killed at L=6; core set external-time-independent (the 2(to+ti) coincidence killed by
  its own discriminator); transfer bimodal (positions universal, multiplicities geometry-dependent).
  resonance_regime.py + RESONANCE_REGIME_RESULT.md.

- THE PAIR LAW (v81): the limit set IS the spectrum -- resonance-regime flips converge to the levels
  two-sidedly as mu*_(+/-) = eps +/- c_eps/beta (four trajectory fits, r within 0.05 of level 1, best
  rms 0.004); every "midpoint" sighting was a pair partner in flight; candidate c = ln(deg)/2 (ln(36)/2 =
  ln 6 = 1.792, a 0.4% hit on the cleanest fit); level-2 grid-pinned, partner-conflation analysis trap
  caught; falsifiable no-free-parameter prediction banked. pair_law.py + PAIR_LAW_RESULT.md.

- THE TWO-CLASS STRUCTURE (v82): the fired prediction FAILED at L=8 level 2 (deg Phase-0-corrected 63 -> 39;
  no pair at 2 +/- 1.832/beta; ln(deg)/2 demoted to a one-level fit) -- exposing Class-II beta-STATIC
  crossings at specific level-pair midpoints (1.819 +/- 0.009 flat over beta 12-24 vs 1.828 =
  (0.828+2.828)/2; 2.121; 2.293; edge artifacts documented); midpoint law resurrects SELECTIVELY; the
  residue-pair selection rule and the Class-I c-formula are the open derivations.
  level2_structure.py + LEVEL2_STRUCTURE_RESULT.md.

- THE RESIDUE RATIO (v83): the Class-I flight constants DERIVED -- near a level, <C>_tau x
  e^{-(to-ti)(mu-eps)} is a polynomial p(f) in the level occupancy, and every flip sits at mu* = eps +
  logit(f*)/beta with f* a root of p; pair = roots straddling 1/2, central flip = root near 1/2,
  multiplicity = root count. Beta-transfer verified (beta=20 polynomial predicts beta=12-28 flips, max
  offset 0.022, no refitting); multiplicity confirmed across three geometries; the creep located
  (adjacent-comb residues at the ~1e-8 cancellation floor; the single-level freeze exact only at s=1/2);
  v81's fitted c's retro-identified as fit-basis artifacts and the ln(36)/2 coincidence resolved.
  residue_ratio.py + RESIDUE_RATIO_RESULT.md.

- THE SELECTION RULE (v84): Class-II statics require (i) a VANISHING saturated background and (ii)
  OPPOSITE-SIGN residues, sitting at mu* = mid + ln(-B/C)/(2 beta) -- the logit law with the two-residue
  ratio. Positive case measured in values (zero 1.8196, K = -0.35, A ~ 0 at 1 sigma, B*C < 0; beta-flow
  matches v82 at max dev 0.010; the 1.707-midpoint alternative rejected by 0.076 -- pair identity by FLOW,
  not numerology); negative case at 1.586 (A nonzero at 4.5 sigma, no flip anywhere). Narrow-window
  three-term degeneracy documented; the direct zero + flow is the robust extraction.
  selection_rule.py + SELECTION_RULE_RESULT.md.

- THE RESONANCE ATLAS (v85, CONSOLIDATION): v80-v84 integrated into one prediction surface with one spine
  -- mu* = anchor + ln(ratio)/(q beta) for both classes (Class I: level + root odds, q=1; Class II:
  midpoint + two-residue ratio, q=2); integration audit A-F PASS (cross-component devs 0.006-0.031; flow
  0.014; live check 0.003); honest catch: the L=6 ~1.8 object UNCLASSIFIED (c-drift 3.1 -> 5.5; conflated
  trajectories suspected); BEST_METHODS v85 edition with methodology rules 10-18.
  resonance_atlas.py + RESONANCE_ATLAS_RESULT.md.

- THE CORE C SURROGATE (v86): csurrogate.c/h -- every banked advance frozen into dependency-free C beside
  the engine: 10 features + frozen-weight magnitude model (v74/v79), wrap-safe sector (v75), pi/beta
  period (v77/v78), regime classifier (v80), Class-I logit-law flips from frozen roots (v81/v83),
  Class-II static with flow K (v82/v84), orientation parity stepping (v77/v85); scopes and the standing
  wall stated in the header. Engine-style gate: fresh-seed live Python references every run, -Wall
  -Werror, "ALL CASES MATCH THE PYTHON REFERENCE TO 1e-09" at worst dev 3.6e-15.
  csurrogate.c/h + csurrogate_test.c + csurrogate_params.h + csurrogate.py + CSURROGATE_RESULT.md.

- THE C SURROGATE UNDER TEST (v87): clean-room build caught 3 portability bugs (M_PI/strict-C99, pedantic
  const, POSIX macro -- fixed; builds c99 AND c11-pedantic -Wall -Werror); efficiency measured (features
  1.5 us = x212 vs Python; atlas laws 3-19 ns; ~875,000x per answer vs exact, growing ~2.6^n); the
  orders-of-n answer split into two ceilings (computational ~unbounded, O(1)-O(n^2), vs the measured
  exact wall x2.5-3.3/order reaching 745 ms at n=9; validity n=3 until higher-order extraction, cap
  n<=6-7 tau-averaged); transfer scope revised openly to 2.3x pooled / 1.7-2.7x per draw after fresh
  draws broke the old gate (contamination hypothesis tested and EXCLUDED, 0/8).
  csurrogate_bench.c + CSURROGATE_BENCH_RESULT.md + fixes/revisions in the v86 files.

- THE ORDER AXIS (v88): the spine is not an n=3 artifact -- n=4 roots 0.156/0.643 (pair straddling 1/2,
  distinct from every n=3 set), beta-transfer verified at max dev 0.024 with no refitting; n=5 lower root
  0.402 resolved and live-verified (dev 0.011) at the wall v87 predicted, upper root flagged marginal; the
  C surrogate gains ATLAS_ROOTS_N4/N5 + surr_class1_flips_order(); the fresh-seed gate caught a real
  numerics bug (float determinant noise on singular integer matrices) fixed with exact integer arithmetic
  on both sides. order_axis.py + ORDER_AXIS_RESULT.md + C extension + feats2 correction.

- THE DEEP PARTNER (v89): one level-2 extraction resolved three roots and closed two anomalies -- the
  ~1.8 object IS the deep lower partner (f*=0.0116, c=-4.44) and v80's "2.2 family" IS the upper partner
  (c=+2.95, flow devs 0.003-0.011); the central root matches at 0.010; the v85 c-drift quantified as
  sign-scan noise (|p| 0.4-5e-9 vs sem 3.2e-9); the deep root's logit law is LARGE-BETA SCOPED -- a
  designed value-level transfer at beta=14 missed by +0.086, banking the adjacent-comb creep as a
  measured, monotone-decaying mu-position correction (+0.114@12 -> +0.003@28).
  deep_partner.py + DEEP_PARTNER_RESULT.md.

- THE TWO-WINDOW CREEP CROSS-CHECK (v90, ledger #100): surrogate and brute force run independently and
  compared -- the deep trajectory is ANCHORED (z = 1.824(+/-0.022) - 0.72/beta, chi/dof 0.53; logit
  rejected at 2.90) and GEOMETRY-INDEPENDENT (frozen (1,3,5) discriminator: devs 0.001/0.001/0.011) --
  the third static-class instance, at L=6 where naive midpoints were excluded; anchor candidates
  2*sqrt(2)-1 (the L=8 static's exact anchor -- possible L-INDEPENDENT) vs 11/6, both open at +/-0.022;
  v89's Delta-decay reading retired as a baseline artifact (fit the trajectory, not the deviation);
  revision note atop DEEP_PARTNER_RESULT. creep_crosscheck.py + CREEP_CROSSCHECK_RESULT.md.

- THE CORRECTION PROPAGATED (v91): the v90 law pushed into both executable prediction surfaces -- the C
  surrogate gains ATLAS_L6_DEEP_A/B + surr_static_l6_deep(beta) with the Class-I scope CORRECTED (logit
  flow = mid-range roots only; deep small-f roots route to the static family); the Python atlas gains
  static_l6_deep() + audit gate G (the corrected law vs the v90 stored value-level zeros, max dev 0.022
  vs gate 0.025, audit now A-G); deep_partner.py carries a revised docstring header; all gates re-passed
  (fresh-seed 3.55e-15, pedantic-C11 clean). A correction that lives only in a result doc is a correction
  waiting to be forgotten. CORRECTION_PROPAGATION_RESULT.md.

- THE ANCHOR TEST (v92): the v90/v91 anchored law scoped to beta in [10,32] (the trajectory rises through
  both v90 candidates); the deep-beta heavy-tail audit -- kurtosis ~4500, single-draw CLT errors invalid
  at the cancellation floor, multi-draw + dense-grid protocol now mandatory; honest deep value a_inf =
  1.8437 +/- 0.0068 (z(48)=1.846(9), z(56)=1.8407(103); beta=64 unresolved); the bridge tool (imported
  from cdet-diagnose-bridge v0.57, edited as anchor_bridge.py) applies its own null rule: alphabet rarity
  83% -> NOT RIGID -- the octagon chord sqrt(2+sqrt2) [Q(sqrt2)/tau1-field] is LEADING at 0.60 sigma, the
  identification OPEN; sigma* = 0.0008 or the structural (background-zero) derivation closes it.
  anchor_test.py + anchor_bridge.py + ANCHOR_TEST_RESULT.md + constant corrections.

- THE EXPONENT-BALANCE LAW (v93): statics derived as integer-weighted means of the lattice's own levels,
  z = mu* + ln(r)/(q beta) -- the field theorem answers tau0/tau1 (statics live in the spectrum's field;
  the chord excluded structurally at L=6); L=8 static = the (1,1) balance of (2sqrt2-2, 2sqrt2) exactly;
  finite menu {11/6, 13/7, 15/8}; the frozen discriminator at beta=36/40 selected 11/6 at ~80:1 (global
  law 11/6 + 2.67/(6 beta), max 0.38 sigma over the honest pool). 13/7 not dead; ln r not yet derived;
  the (2,3) window found SUPPRESSED (probe inconclusive). exponent_balance.py +
  EXPONENT_BALANCE_RESULT.md + propagation (DEEPLAW test; atlas gate I).

- THE SIDE-BY-SIDE (v94): surfaces parity-locked (law + competitor lines, C vs Python at 1e-15);
  out-of-sample predictions frozen to disk, then measured -- z(44)=1.8510(76), z(52)=1.8527(52) score
  ~9:1 for 13/7 against the v93 frozen 11/6 (which had won 80:1 in-sample): the identification REOPENED.
  Six-point pool admits 11/6 / 13/7 / a constant 1.8467(21) (chi2/dof 0.96/0.32/0.47); the constant
  revives the chord (0.5 sigma) -- the menu-vs-flatness tension; the degree bound (weight <= 6 at n=3?)
  is the raised decisive item. z(30)=1.8138(37) demonstrates the law's scope floor (both lines miss by
  >= 8 sigma in the crossover window). law_sidebyside.py + SIDE_BY_SIDE_RESULT.md + status revisions.

- THE DEGREE BOUND (v95): settled by a symbolic census of the actual C_V (the port on symbolic
  occupancies) -- bound = 2n+1 = 7 (v93's 8 and v94's 6 both wrong), support FULL (330 monomials);
  balances come from exponent differences -> corrected menu {..., 11/6, 24/13, 13/7, 15/8, ...}; 24/13
  (q=13, near-flat approach) is 0.26 sigma from the v94 constant -- the menu-vs-flatness tension
  DISSOLVED; identification open among {13/7, 24/13}; the coefficient program is the named closing
  route. degree_bound.py + DEGREE_BOUND_RESULT.md + revisions.

- THE COEFFICIENT PROGRAM, PHASE 1 (v96): FrozenCDet built (window occupancies by hand), validated
  (A(20) matches v89) and proven faithful at the physical point; the background A(beta) measured ALIVE
  (4.6 sigma at beta=44 -- no background-zero, no midpoint static in the (1,2) window) and decaying at
  effective rate ~0.10-0.12 with prefactor curvature (asymptotic 1/7-vs-2/13 band not yet reached); the
  far-level antiperiodic images identified as the concrete creep carrier; the no-fit prediction test
  inconclusive (A's tails + small-s curvature) with the phase-2 spec computed. coefficient_flow.py +
  COEFFICIENT_FLOW_RESULT.md.

- THE PARITY TABLE (v97): five window backgrounds measured across both lattices (WindowFrozen
  generalized); the binary "even first-empty degeneracy => A=0" rule FALSIFIED by its own registered
  prediction (W8(0.828,1.414): A = -0.0208(55), 3.8 sigma); a robust suppression pattern survives
  (odd ~ +0.5-0.85 vs even 20-40x smaller); the v84 L=8 static reread as a root-flow crossing (A ~ 95%
  of the deviation term at 1.8284) with the deep-beta crossover replay REGISTERED as a frozen
  prediction; conditioning rule + mask-tolerance catch banked. parity_table.py + PARITY_TABLE_RESULT.md.

- THE METHOD AUDIT (v98): v97 audited against the KT-RG method v3.1 -- the suppression pattern found
  CONFOUNDED (degeneracy parity vs level rationality; the falsification test was the weakest available);
  deviation ratios computed and found underpowered (spec recorded); #107's root-flow claim downgraded to
  CANDIDATE; the L=8 prediction QUANTIFIED (frozen z8 curve from A8(40) = +0.1135(266), rate 0.1231(233):
  the v84 static violated by +0.013 at beta=40 if root-flow holds); the queue REORDERED by leverage
  (coefficient phase 2 first). METHOD_AUDIT_v97.md + parity_table.py revisions.

- COEFFICIENT PROGRAM PHASE 2 (v99): the heavy-tail problem SOLVED (integrand autopsy: alpha ~ 0.55
  infinite-variance tails at clustered times; mixture importance sampler, weights <= 2, ~31x variance
  reduction, analytically validated); the frozen polynomial measured to 3-7% (A = +0.3700(108), root
  s* = 0.00183(8), z_pol(36) = 1.8249(12)); the registered root-flow branch EXCLUDED at ~10 sigma; and
  THE TWO-SECTOR DISCOVERY: v96 faithfulness falsified at 3.4 sigma -- the freeze kills the delta1
  antiperiodic images (O(1) in the tau->beta corner); the physical zero balances the frozen polynomial
  against the hole-image sector Delta(s_phys) = +0.369(109). The decisive object is now Delta(s; beta).
  coefficient_phase2.py + COEFFICIENT_PHASE2_RESULT.md + downgrade notes.

- THE DELTA SECTOR (v100): the v99 "second player" RESOLVED as a delta1 x f2 CROSS-TERM, not a
  background -- Delta(0;beta) ~ 0 at both beta (vanishes when level 2 empty), so the freeze omitted a
  cross-coefficient, not a sector. The cross-slope measured (matched-s secants): d1(28)=+41.8(13.2),
  d1(36)=+88.8(21.5) e-9, GROWING with beta; it shifts c1_eff and moves the frozen root 0.00183 ->
  0.00327 toward the physical f2*=0.00376 (right direction). Delta1Frozen instrument validated against
  the physical value. The 13/7-vs-24/13 closure reduces to the assembled root flow z(beta); spec and a
  directional prediction registered. delta_sector.py + DELTA_SECTOR_RESULT.md.

- CONSOLIDATION (v101): the C surrogate brought current with v96-v100 (params status block + callable
  carriers surr_l6_zpol36 / surr_l6_cross_slope / surr_l6_root_linear; 4 new gate cases pass); the
  brute-force C reference drivers stamped (unmodified, still compile); all mds audited self-contained --
  the gen_golden/cdet_reference orphan in the engine docs corrected (golden.json ships and is
  authoritative); README given a live-record pointer. csurrogate.* + CONSOLIDATION_v101.md + de-orphaned
  engine docs. Frozen engine untouched (194/194).

- SURROGATE vs BRUTE SIDE-BY-SIDE (v102): the C surrogate run head-to-head against exact CDet,
  out-of-sample, both lattices (the accuracy check the gate omits). AGREE within scope: sector EXACT
  (0/120), ln-mag median 1.81x, 13/7 line (chi2 1.7) over 11/6 (5.6), z_pol36 1.8249 vs brute 1.8251,
  root_linear closes 80% of the cross-term gap. DISCREPANCY (surrogate): surr_class2_static (v84 L=8
  K-flow) disagrees with the v100 root-flow reread by up to 0.021 with OPPOSITE slope -- flagged stale,
  arbiter = the queued deep L=8 scan. DISCREPANCY (glue): a s->z sign bug, caught by the trustworthy
  surrogate value. SURROGATE_VS_BRUTE_RESULT.md + surrogate_vs_brute.py + supersession notes.

- PRECISION (v103): naive float64 silently DROPS the deep-beta far-level antiperiodic images (catastrophic
  1-nf cancellation on the corner configs that carry 95% of the MC mass) -- 8%-370% wrong, certified by
  mpmath-200. FIX: the LOG-DOMAIN stable engine (stable_cdet.StableCDet/StableFrozen, float64 speed,
  mpmath-certified to 1e-9). Re-measurement: frozen A survives (0.3s), the cross-term survives (0.8s),
  faithfulness still falsified (3.2s) -- but physical(1.845) MOVES ~4s (stable -0.19(5) vs naive +0.03(11))
  and the error bar halves, so the deep-beta ZERO and the empirical pool anchoring the menu must be
  re-measured on the stable engine. mpmath = the certifier; the stable engine = the brute's final form.
  stable_cdet.py + mp_cdet.py + PRECISION_RESULT.md + params caveat.

- DEEP-POOL RE-ANCHOR (v104): the stable integrand is STILL heavy-tailed (alpha ~ 1.06), so the precision
  fix needed a robust estimator too. Median-of-means (72 batches): physical(1.845) = -0.077(60),
  CONSISTENT WITH ZERO -> z(36) = 1.8428(40), 0.4 sigma from naive: THE POOL SURVIVES. v103's "zero moves
  4 sigma" RETRACTED (a single-IS-draw heavy-tail fluctuation -- the v92 lesson un-applied). Stands: the
  engine correctness, frozen A, and faithfulness-falsified (4.4 sigma, robust). Protocol amended: deep-beta
  means require the stable engine AND median-of-means. deep_pool.py + DEEP_POOL_RESULT.md.

- THE ROBUST FLOW (v105): the full certified pool z(36/44/52) = 1.8428(40)/1.8536(121)/1.8642(61) RISES
  monotonically (steeper than the nearly-flat naive pool) and fits NO single menu law (best 13/7 chi2
  6.5/2; all >3) -- by beta=52 it has passed 13/7=1.857. The naive flatness that drove v93-95 to
  {13/7, 24/13} was a corrupted+heavy-tailed ARTIFACT; the certified flow vindicates the v100 ASSEMBLED
  ROOT FLOW (not menu lines). Identification reopened as a FLOW. Honest limit: 3 points, ~2-3 sigma rise,
  ill-conditioned high beta. deep_pool.py (POOL_STABLE) + ROBUST_FLOW_RESULT.md.

- LOOP-FORMAT RESOLUTION (v106): the uploaded gravity-loop resummation (linear recurrence -> rational
  generating function -> dominant-root asymptote) TRANSFERS to the deep-beta series (A, <C> are sums of
  exp(-beta xi_k) -> linear-recurrent), directly targeting the v105 high-beta ill-conditioning. Adapted to
  our noise via the EXACT-INTEGER L=6 spectrum: rates known -> fit only amplitudes (well-posed; chi2
  0.75/2 on clean stable A(beta)). Target: z(inf) = 2 - (rho_A - rho_c1). Does NOT help the MC heavy tail
  (median-of-means stays) or move the wall; fwverify/MPFR confirms the v103 certifier. deep_beta_
  resummation.py + LOOP_FORMAT_RESULT.md.

- THE ASSEMBLED ROOT FLOW (v107): the closure via the loop-format rate difference. Measured A(beta) (fast,
  rho_A=0.141(16)) and c1(beta) (slow, rho_c1=0.022(10)) on the stable grid -> z(inf)=2-(rho_A-rho_c1)=
  1.8818(184), ABOVE the naive-favoured lower menu (24/13 1.9s, 13/7 1.3s disfavoured), consistent with
  the HIGH end 15/8=1.875 (0.4s; declared dead in v94/95 on naive data -- now resurrected). Internally
  consistent: leading-order flow sits ~0.03 below the robust pool = the v100 cross-term. Two independent
  methods agree the asymptote is ~1.88. Leading order; honest 10-40% rate errors. deep_beta_resummation.py
  (assembled_z_inf) + ASSEMBLED_FLOW_RESULT.md.

- DUAL CONSOLIDATION (v108): both C layers brought current with v104-v107 and compared across value /
  precision / speed. Surrogate: menu carriers superseded by the resolved z(inf)=1.8818 (lower menu falls,
  15/8 returns); added surr_l6_z_inf + surr_l6_pool. Brute C: the naive G0_atom carries the v103 deep-beta
  bug latent (benign-correct, ED-validated) -- built+certified the log-domain G0_atom_stable (cdet_stable.c,
  1.29x cost, deep-beta-correct, ~1000x the Python stable engine). DUAL INSIGHT: both inherit ONE flaw (the
  naive propagator) and take ONE cure (the log-domain form); stable-C fills the missing fast+correct
  quadrant. cdet_stable.{c,h} + DUAL_CONSOLIDATION_RESULT.md.

- STABLE C ENGINE (v109): cdet_stable_engine.c -- the frozen connected determinant with the log-domain
  propagator, reading the exact L=6 spectrum (spectrum_l6.bin), validated to machine precision vs Python
  C_V and vs high-stat Python A(40)=0.262 vs 0.267. A 6-point grid to beta=64 in 150 s (Python couldn't
  reach). EXPOSED: v107's A(beta) was heavy-tail-biased LOW (A(40) banked 0.119 vs true 0.267) -> z(inf)=
  1.882 was an UNDERESTIMATE. Corrected flow rises to z(64)=1.878 still climbing -> 15/8 DISFAVORED (flow
  passes through it), asymptote >=1.88 (17/9+), but extrapolation UNSTABLE (not pinned; needs beta>64 or a
  multi-exponential model). Internally consistent with the pool (shrinking cross-term lift). cdet_stable_
  engine.* + STABLE_C_ENGINE_RESULT.md.

- THE PLATEAU RUN (v110): pushed the long-double C engine (float64 NaNs at beta>=96; long double reaches
  120) to beta=120. NO PLATEAU: the flow z=2+ln(A/|c1|)/beta rises monotonically through every menu
  rational (15/8 at beta~61, 17/9 at ~74, 19/10 at ~87) to z(120)=1.920, still climbing, rho_A not
  converged. z(inf) in [1.95,2.0], plausibly the trivial z=2 with slow 1/beta corrections. RETRACTS the
  menu-rational identification (v93-v107): those were finite-beta crossings, not the asymptote. Insight:
  the freeze regularizes the determinant (frozen safe to beta=120; physical fails at beta~56). PLATEAU_
  RESULT.md.

- z(inf) RESOLVED = 2 (v111): model comparison on (2-z)*beta=ln(|c1|/A) over the clean flow REJECTS the
  exponential-gap/menu picture (chi2 622/7) for a power-law: A ~ beta^-2.8, |c1| ~ beta^-0.54 (both rates
  ~0), so |c1|/A ~ beta^2.3 and z(beta)=2-2.3*ln(beta)/beta -> 2. z(inf)=2 (the bare probe level) to within
  ~0.01. The menu rationals (11/6..17/9) are finite-beta crossings of a ln(beta)/beta approach, NOT
  asymptotes -- the v93-v107 identification fit the slow transient. deep_beta_asymptote.py + ZINF_RESULT.md.

- z(inf)=2 DERIVED (v112): A and c1 are tau-averages, so the power is set by J(beta)=beta^3*X = the
  un-normalized integral. J_A -> CONST (A corner-confined ~1/beta^3: the s=0 images align only in a
  beta-independent corner); J_c1 ~ beta^2.7 (c1 DE-confined by the smallest-gap level-2 channel xi_2=0.155,
  longest-range propagator). |c1|/A ~ beta^2.7 forces z=2-2.7*ln(beta)/beta -> 2. z(inf)=2 because the probe
  level IS the smallest gap. Windowed check J_c1(W)~W^2.6 confirms de-confinement. deep_beta_powerlaw_
  derivation.py + POWERLAW_DERIVATION_RESULT.md.

- SINGLE-CHANNEL SHARPENING TESTED (v113): an external proposal (c1=sum_n a_n exp(-xi_n beta), xi_2<xi_n,
  phase in n=2 -> 'sign problem = one mode of gap (2-mu)') splits: the kernel SURVIVES (xi_2<xi_n TRUE --
  level 2 closest to mu; phase carried by the single level-2 channel = v112), the literal exp form is
  FALSIFIED (c1 would decay at rate 0.155 -> 3e6x; measured 1.66x). The level-2 propagator SATURATES under
  tau-integration (int exp(-xi_2 tau)->1/xi_2=6.5) -> rate-0 power law, not an exp mode. gap (2-mu) = the
  de-confinement RANGE + the limit z(inf)=2, NOT a beta-rate. spectral_channel_test.py + SPECTRAL_CHANNEL_
  RESULT.md.

- z(inf)=2 LOCKED to the Fermi surface (v114): generalizing the freeze to an arbitrary probe (engine
  set_freeze + grid arg 10) and moving probe 2->3 shows the mechanism does NOT generalize -- probe=2 (Fermi
  surface) gives finite c1 and z->2, but probe=3 makes c1 DIVERGE as exp(+2.7 beta) (population inversion:
  level 3 occupied while level 2 empty, Fermi-forbidden). z(inf)=2 is locked to level 2 = the lowest empty
  level = the only valid probe. 'smallest gap' = 'Fermi surface' = 'only valid probe'. probe_generalization_
  test.py + PROBE_LOCK_RESULT.md.

- FULL DUAL CONSOLIDATION at the frontier (v115): both C layers brought current with z(inf)=2 (resolved/
  derived/Fermi-locked v111-v114). The surrogate's live carrier surr_l6_z_inf() had been returning the stale
  1.8818 despite 13 caveat layers -- now returns 2.0, plus surr_l6_z_finite (the ln(beta)/beta law) and a
  legacy carrier; brute-C re-stamped v115 pointing at the built stable engine. Three-layer side-by-side
  (surrogate carries 2.0 / stable-C derives 2.0 / brute-C ED-anchor at benign only; deep beta only stable-C
  correct; speed 7.4/14.2/17.4 ns). LESSON: the duality is a CHAIN -- surrogate can't compute, brute-C can't
  go deep, stable-C can't self-certify; the cross-validation between them caught every error (heavy-tail
  bias, precision walls, z=2 resolution). DUAL_CONSOLIDATION_v115_RESULT.md.

- SITE-CHOICE GENERALIZATION (v116): varying the lattice sites at fixed Fermi-surface probe (engine grid
  takes optional sites), z=2+ln(|A|/|c1|)/beta rises toward 2 for ALL 5 geometries tested -- z(inf)=2 is
  geometry-independent (registered prediction CONFIRMED), rate varies. NEW: the SIGN of (A,c1) varies by
  geometry (opposite->physical root s*>0, same->none); the SCALE (z=2) is DOUBLY universal (probe- AND
  site-independent), the SIGN structure is the GEOMETRIC degree of freedom. Sign and scale separate -- the
  anatomy of the sign problem. site_generalization_test.py + SITE_GENERALIZATION_RESULT.md.

- THE SIGN SIDE = FRIEDEL (v117): A's sign OSCILLATES with site separation -- scanning a vertex site along x,
  sign(A)=(-,-,-,+,+), a reproducible zero-crossing (seeds agree, |A| min at the flip). Friedel-class. The
  wavelength is LONG (~8 sites = 2k_F from mu=1.845 near the band top, small Fermi surface), NOT period-2
  (that sub-guess was wrong). UNIFYING: the Fermi surface governs BOTH -- its GAP sets the scale z(inf)=2,
  its MOMENTUM sets the sign (Friedel ~8 sites). v116 found sign/scale separate; v117 finds one origin (the
  Fermi surface) via two channels. site_sign_friedel.py + FRIEDEL_SIGN_RESULT.md.

- GAP-MOMENTUM UNIFICATION TEST = MOVE mu (v118): moving mu in (1,2) shows BOTH the sign pattern (x-scan
  sign(A)=(-,-,-,+,+) at mu=1.3/1.6/1.9) AND the z-flow (z=1.786/1.853/1.887, spread <0.005) are mu-INVARIANT.
  The registered continuous-2k_F prediction (lambda 3.64->9.89 sites) is FALSIFIED. ROOT CAUSE: the engine is
  FROZEN -- discrete occupations, so the Fermi surface is the level-1|level-2 boundary, fixed for all mu in the
  window. CORRECTS v117: the 2k_F(mu) wavelength match was coincidental; the sign is set by the DISCRETE frozen
  boundary. STRENGTHENED: one discrete (topological) object -- the filled-level set -- governs BOTH scale and
  sign, rigid in mu; mu matters only when it crosses a level (v114). mu_unification_test.py + MU_UNIFICATION_RESULT.md.

- FULL 2D FRIEDEL MAP, elementary resolution (v119): the elementary frozen object rho(0,r)=FT of the occupied
  region is cube-symmetric, SHORT-wavelength (~2-3 sites, wavevector (120,180)deg = level-1|2 boundary modes),
  and EXACTLY mu-invariant (ZERO modes in the gap (1,2) -> occupied set rigid; analytic proof of v118). A's
  sign is a determinant SUPERPOSITION of these short oscillations -- v117's ~8-site envelope was the
  superposition, not the elementary scale (v117 core survives). Same discrete Fermi surface sets scale (z=2)
  and sign. frozen_friedel_map.py + FROZEN_FRIEDEL_MAP_RESULT.md.

- FULL DUAL CONSOLIDATION at the sign frontier (v120): the surrogate was SCALE-ONLY; now it carries the
  sign-side analytic core -- surr_l6_gap_modes / surr_l6_occupied over the cube integer multiplicities +
  the Friedel wavevector -- confirmable in C with NO eig, matching Python exactly. SHARPER THEOREM produced
  by the consolidation: the cube_hopping(6) spectrum is INTEGER-valued, so no mode lies in any open unit
  interval -> the freeze is exactly mu-rigid in ANY unit interval (generalizing v118/v119's (1,2) result).
  Side-by-side (3 layers x 2 axes): SCALE surrogate/stable-C/brute-C as before; SIGN elementary rho=Python,
  determinant A=C, mu-rigidity=surrogate carrier. LESSON: the sign side is a CHAIN; consolidation
  out-performed experiment (the theorem fell out of asking how to carry the result). DUAL_CONSOLIDATION_v120_RESULT.md.

- ELEMENTARY rho(0,r) PORTED TO C (v121): the v119 sign object, Python-only until now, is in C -- cfriedel.c
  computes rho(0,r)=(1/N)sum_{eps(k)<=1}cos(k.r) from the plane-wave structure (cube=3 rings, projector
  basis-independent), NO eigenvectors / spectrum file / eigendecomposition. Validated worst-dev 4.81e-11 vs
  the Python eigh density matrix over all 216 sites; map identical to v119; occupied 156, integer-spectrum
  mu-rigid. Closes the v120 open fix: the sign side now has full three-layer C coverage (elementary rho =
  cfriedel.c, determinant A = engines, rigidity = surrogate carriers). cfriedel.c + FRIEDEL_PORT_RESULT.md.

- MULTI-LATTICE LAWS + SCALING + HYBRID (v122): testing the laws across L -- mu-rigidity (v120) is
  CRYSTALLOGRAPHIC (exact iff cos(2pi/L) rational iff L in {1,2,3,4,6}; verified L=2..12), while the SCALE law
  z(inf)=lowest-empty-level and the FRIEDEL law are UNIVERSAL (any L). SCALING: the determinant is over a fixed
  vertex set; the lattice enters only via O(N) plane-wave propagators (no eigenvectors/spectrum) -> brute force
  is O(N x MC), L-agnostic; cfriedel_L.c runs the structural layer to L=20 (N=8000) in <1s, zero stored data.
  HOW BIG: structural laws to L=20+ trivially; determinant to L~12-16; ceiling is analysis-context not lattice.
  HYBRID (third engine): phase 1 carries the laws (O(N), any L, instant) -> phase 2 optimized plane-wave
  determinant (O(N x MC)), handoff where the surrogate stops being exact. multi_lattice_laws.py + cfriedel_L.c
  + MULTI_LATTICE_RESULT.md.

- HYBRID PHASE 2 = L-GENERALIZED PLANE-WAVE DETERMINANT ENGINE (v123): cdet_planewave_engine.c computes A,c1
  at ANY L on the plane-wave propagator (no eigenvectors / spectrum file); validated == stable engine at L=6
  (A,c1 to the last digit). MULTI-LATTICE SCALE LAW PROVEN: z(inf)=lowest-empty-level -- L=4 ->2 (different
  lattice), L=6 probe=3 mu in (2,3) ->3 (different probe level). z(inf) is the lowest-empty level, NOT a
  constant 2. Cost ~linear in N (L=8 16s/point); L~12-16 feasible. Hybrid complete: phase 1 laws -> phase 2
  plane-wave determinant. Open: non-crystallographic L needs a continuous-threshold freeze. cdet_planewave_engine.c
  + hybrid_phase2_test.py + HYBRID_PHASE2_RESULT.md.

- TOWARD MILLION-SITE LATTICES (v124): (a) PROJECTOR FAST PATH -- regroup g0 by distinct eigenvalue,
  precompute P[dr][eps] for the ~7 fixed vertex displacements, propagator O(#distinct eps) not O(N); EXACT
  (L=6 fast==direct A=1.341555,c1=-234.4268), 73x at L=12, makes L=100 (1e6 sites) a day-long z-flow. (b)
  CONTINUOUS FREEZE (mode 2) for non-crystallographic L: z(inf)=lowest-empty eigenvalue = sqrt(2) (IRRATIONAL)
  at L=8 -- scale law holds even irrational. (c) run_to_log.py harness + engine NaN guard ('# NONFINITE' stop,
  no silent NaN; fsync-streamed log, crash/signal detection, last_good_beta) for safe day-long runs; streaming
  was already in place. cdet_planewave_engine.c + run_to_log.py + hybrid_scaling_test.py + SCALING_HARNESS_RESULT.md.

- LARGE-L STUDY: z(inf) MARCHES TO THE CONTINUUM FERMI LEVEL (v125). At fixed mu=1.0, z(inf)=lowest-empty(L)
  closes onto mu as L grows (gap~L^-3.3, ~1/L^3): asymptote marches 2.0 (L=6) -> 1.414 (L=8) -> 1.082 (L=16)
  -> 1.0002 (L=100), confirmed by fast-path z-flows tracking each L's value. Ran L=100 = 1e6 sites at 52s/pt
  (45x collapse, probe_val=1.000192==prediction). FINDING: z(inf)->mu thermodynamically (continuum Fermi
  surface) but the determinant signal vanishes as the gap closes -> signal-starved, needs growing stats; the
  wall sharpens onto mu. thermo_limit_study.py + THERMO_LIMIT_RESULT.md.

- SIGNAL BUDGET: resolving z(inf) at large L costs ~N, polynomial (v126). c1 (probe response) is the binding
  signal (relErr(c1)~gap^-0.47; relErr(A) flat). MC budget to hold z-precision ~ gap^-0.9 ~ L^3 ~ N -- NO
  exponential sign-problem wall in this observable. L=100: ~5% on c1 needs ~3.3e5 samples/pt (~5.5h), so a
  day-long run resolves a coarse million-site z-flow. Launch recipe (run_to_log + cpw -L 100 -fast) in the
  result. signal_budget_study.py + SIGNAL_BUDGET_RESULT.md.

- SELECTION RULE vs LARGE L = FINITE-GAP FRIEDEL (v127). v116's physical-root rule sign(A)!=sign(c1) tested vs
  L (fixed sites): sign(A) CONVERGES (bulk background, stable -) but sign(c1) FRIEDEL-OSCILLATES in L (seed-
  stable 24-/32+/40-/48+), |c1|->0 as the gap closes. So the rule's outcome ALTERNATES and goes MARGINAL in the
  continuum -- it is a finite-gap Friedel phenomenon, not a continuum invariant. Prediction (uniform persistence)
  partially falsified, banked. Sharpens v119: both A's and c1's signs are Friedel oscillations of the same
  density matrix; only the background survives. selection_rule_continuum.py + SELECTION_RULE_RESULT.md.

- c1 SIGN IN L = ARITHMETIC JITTER, NO FRIEDEL PERIOD (v128). v127's sign(c1) "oscillation" has no clean
  period: period-16 FALSIFIED (L=24- 28+ 32+ 36+ 40- 44- 48+ 52-; 28/44 and 36/52 mismatch, seed-stable). The
  probe momentum jumps number-theoretically (which cosine-sum multiplet is lowest-empty), so the Friedel phase
  at the x-vertices jitters. v119 CONTRAST: A integrates the whole sea -> clean continuum wavevector, sign
  converges; c1 picks one lowest-empty multiplet -> jitter, no period -- exactly why v127 saw A converge, c1
  oscillate. probe_jitter_analysis.py + PROBE_JITTER_RESULT.md.

- A's CONTINUUM FRIEDEL WAVEVECTOR (v129): v119's (120,180) dominant wavevector CONFIRMED as a convergent
  continuum feature. The Fermi surface {eps<=1}=cos-sum<=-1/2 is L-independent; rho's Friedel edge (half-max of
  W(kx)) along x converges kx/L 0.425->0.347 (~120deg, 3-site end) as L->inf. (120,180) were the L=6 discrete
  sampling; continuum lands at the 120 (3-site) end. Counterpart to v128: A integrates the whole sea (convergent
  wavevector, sign converges); c1 picks one multiplet (jitter). continuum_wavevector.py + CONTINUUM_WAVEVECTOR_RESULT.md.

- CONSOLIDATION v130: surrogate + brute + merged hybrid brought current to v124-v129, cross-validated. Surrogate
  gained surr_lowest_empty(L,mu) (scale law any L, no eig) + surr_friedel_edge(L,mu) (v129 edge); brute re-stamped
  (ED anchor); hybrid header merged (fast path + continuous freeze + NaN guard, one engine). THREE-WAY side-by-side
  z(inf)=lowest-empty AGREES (surrogate-C == hybrid-C == python); Friedel edge matches. Only build-hygiene drift
  fixed, no numerical drift. dual_consolidation_v130.py + CONSOLIDATION_v130_RESULT.md.

- CoS PROTOTYPE + INTEGRATION ASSESSMENT (v131): verified (vs the real engine, via cos_harness.c) that a CoS-style
  subset-convolution (O(2^n n^2)) reproduces C_V to machine precision, and a faithful Rossi port reproduces it
  exactly -- the engine's 'mask' = CoS's connectivity record R, same 2^n wall. Honest cost: 3^n combine only beats
  2^n n^2 at n>=12, and the shared 2^n*n^3 determinant cost dominates anyway -- so the combine swap is marginal;
  the real lever is the n^3->n^2 CoS forward DP. Ranked integration list (forward DP, SU(N), self-energy, MC
  symmetrization, subset-conv, record-R pruning, QTT) in the result. cos_prototype.py + cos_harness.c +
  COS_PROTOTYPE_RESULT.md.

- INTEGRATION #1 DONE (supplement): connected determinant in O(2^n n^2) (v132). Fast principal minors (one
  Schur recursion, O(2^n n^2)) reproduce all D_vac/D_corr; chained with the v131 subset-conv they reproduce the
  engine's C_V to 3e-15 -- the whole connected determinant at O(2^n n^2) vs the engine's O(2^n n^3 + 3^n).
  Verified live vs the engine, n=3..7. Standalone path (engine untouched); wire-in is a separate val-gated stage.
  Prerequisite for #2 (SU(N)) and #3 (self-energy). fast_minors.py + FAST_MINORS_RESULT.md.

- PHYSICAL MAPPING RESOLVED (v133): z(inf) IS a real spectral observable -- the single-particle ADDITION POLE
  (lowest-empty level). It tracks the moving pole (v125) and the v78 fugacity lemma puts the poles exactly at the
  levels eps_k; the deep-beta z-flow extracts the nearest one above the sea. Free now (g0 = free spectrum); the
  interacting addition energy eps_k+Re Sigma needs the self-energy resummation = integration #3. So z and #3 are
  the same physical target at two resummation levels. physical_mapping.py + PHYSICAL_MAPPING_RESULT.md.

- INTEGRATION #3 STEP 1 (supplement): self-energy = the interacting upgrade of z (v134). ED-verified: atom Sigma
  == closed-form atomic self-energy (1e-15); dimer addition pole == z(inf) at U=0 and = eps_free + Re Sigma at U>0
  (leading shift = Hartree U<n_-s>). z IS the Sigma=0 limit of the interacting addition energy. Supplements z;
  ED is only the verification anchor; engine untouched. Next: the diagrammatic Sigma (reusing v132 fast minors).
  self_energy.py + SELF_ENERGY_RESULT.md.

- INTEGRATION #3 STEP 2 (supplement): the diagrammatic self-energy converges to the exact Sigma (v135). Connected-
  determinant order series + resum + Dyson -> Sigma_diag, which converges geometrically to the exact ED Sigma inside
  the bare-series radius ~pi/beta (atom: 7e-6 @U=0.3 order 8; 6.6e-4 @U=0.5). The radius limit motivates the direct
  irreducible series (step 3 = the actual Simkovic-Kozik algorithm). self_energy_diagrammatic.py + result.

- INTEGRATION #3 STEP 3 (supplement): the 1PI series has a larger radius (v136). The self-energy's own series has
  radius R_Sigma (atom: the partition-fn zero ~1.76) > the bare-G radius R_G (~0.80), because the G-pole is a
  regular point of Sigma. Demonstrated vs exact ED Sigma: past R_G the bare series DIVERGES while the direct 1PI
  series stays converged -- why Simkovic-Kozik compute Sigma directly. sigma_n here = contour proxy; exact = the
  1PI determinant recursion (reusing v132 fast minors), the remaining engine build. self_energy_irreducible.py + result.

- INTEGRATION #3 STEP 4 + CORRECTION (v137): exact 1PI coefficients via the Dyson recursion (sigma_n =
  a_n/G0^2 - (1/G0) sum sigma_m a_{n-m}) reproduce ED Sigma to 1.9e-9 @U=0.3. Their decay RETRACTS v136: R_Sigma~0.84
  ~ R_G~0.73, NO radius advantage (v136's 1.76 was a contour-proxy artifact -- the contour enclosed Sigma's
  singularity). The real Simkovic-Kozik advantage is efficiency + MC variance, not radius. v133-135 unaffected.
  self_energy_irreducible.py (rewritten) + result.

- FULL CONSOLIDATION (v138): three paths (surrogate/plane-wave/python) agree on the addition pole (5e-10), fast
  minors == engine (3e-15), exact 1PI sigma_n == ED (7e-8); all v131-v137 advances live. README+QUICKSTART
  refreshed to the integration frontier. Learnings: plane-wave LD for deep cancellation; self-energy needs the
  engine wire-in + resummation for strong coupling; fast-minors wire-in (#5); surrogate could carry the Hartree
  shift. consolidation_v138.py + CONSOLIDATION_v138_RESULT.md.

- HYBRID STRESS TEST + GUARDS (v139): the hybrid is robust (val 0.00e+00, fast==direct bit-identical, NaN guard
  clean, 2.7M sites @193s, probe_val==surrogate). f64 walls @beta~100, LD reaches >=200 (use -DUSE_LD deep).
  Found + guarded 3 silent failure modes (input-only, val preserved): non-crystallographic L + mode 0/1 blows up
  (z~1e23); large delta flips c1; delta=0 -> c1=NaN. stress_test_v139.py + STRESS_TEST_v139_RESULT.md; the hybrid
  gained the guards. (New features still supplements, not wired in -- that is #5.)

- RESUMMATION / PRECISION (v140, answering the gravity-loop question): the exact-recurrence 15-digit trick does
  NOT transfer -- our sigma_n obey no finite recurrence (GF not rational). Pade extends strong-coupling REACH
  (3e13->0.23 @U=3 past the radius ~0.8) but not precision. Most models already have exact resummation (engine,
  surrogate, Dyson). The general accuracy lever is extended-precision ARITHMETIC (LD/mpmath) in cancellation
  regimes (LD reaches beta>=200 vs f64's 100). resummation.py + RESUMMATION_RESULT.md.

- FOLD-IN + RATIONAL HINT (v141): surrogate gains surr_interacting_pole (free pole + Hartree shift U<n_-s>; Sigma=0
  recovers free); v139 guards + LD already folded; fast-minors wire-in stays #5. THE HINT (live): at FIXED density
  the atom self-energy IS rational -- exact 1-term recurrence, [2/1] exact to 1e-15 past any bare radius. The
  grand-canonical nd(U) was the only non-rational piece -> the 15-digit route lives in the SKELETON/bold expansion.
  Lattice skeleton rationality = open standing lead. rational_skeleton.py + RATIONAL_SKELETON_RESULT.md.

- QUEUE #2 (SU(N)) STEP 1 (v142): the SU(N) atom EoS + the N-polynomial RECORD. ln Z U-coeffs are exact
  degree-(j+1) polynomials in N (cumulants of the pair count under the U=0 binomial; N=2..7 predict N=8,9,10 to
  5e-9; ED-checked 2e-11). N-independent kernel -> any flavor number, incl N=6 Yb (density 0.309 @U=1). Lattice
  connected-determinant record (reusing v132 fast minors) = step 2. sun_atom_record.py + SUN_ATOM_RECORD_RESULT.md.

- QUEUE #2 (SU(N)) STEP 2 (v143): the record SURVIVES HOPPING. 2-site SU(N) lattice ED -> ln Z coeffs stay
  degree-(j+1) polynomials in N (c1 deg 2 predicts N=5,6 to 5e-5; U=0 factorizes to 1e-14). So the N-independent
  kernel -> any flavor number holds for the lattice, not just the atom; the N=6 Yb EoS is reachable from the kernel.
  Production lattice CDet + closed-loop record (v132 fast minors) = the remaining engineering. sun_lattice_record.py
  + SUN_LATTICE_RECORD_RESULT.md.

- QUEUE #2 (SU(N)) STEP 3 (v144): the PRODUCTION EoS route. First coefficient from single-flavor g0 (d,d') x the
  record -- c1=-beta N(N-1)d^2, n1=-(N-1)d d' -- matches the 2-site SU(N) ED to 1e-7 for ALL N incl N=6, with NO
  N=6 diagonalization. The N=6 first-order EoS tracks ED at small U. Single-flavor g0 (once) x combinatorial record
  = EoS at any flavor number (CoS at SU(2) cost). Higher orders (full CDet+record+tau-integrals) remain.
  sun_lattice_production.py + SUN_LATTICE_PRODUCTION_RESULT.md.

- QUEUE #2 STEP 4 + GRAVITY-LOOP HINT (v145): 2nd-order EoS record persists (n2 low-deg poly in N, N=6 to 3e-4).
  THE HINT FOUND: the gravity recurrence->rational-GF->exact-resummation mechanism lives in N (not U, where only the
  atom is rational): coeffs poly in N -> finite recurrence in N (c1 3rd diff 7e-15) -> rational N-GF -> all-N EoS
  resums from a few small N (c1(6) exact, large-N rate -beta d^2). Same mechanism as gravity, in N; root 1 vs the
  gravity cubic. This is WHY CoS is N-independent. sun_resummation_N.py + SUN_RESUMMATION_N_RESULT.md.

- U-AXIS RATIONAL LEAD -> BOUNDARY (v146): Sigma(U) rational IFF eigenvalues linear in U IFF interaction diagonal
  (atom: ||[Hkin,Hint]||=0 -> rational, 15-digit). Hopping (dimer ||[Hkin,Hint]||=1.4) -> algebraic eigenvalues ->
  lattice Sigma ALGEBRAIC (branch points), NOT rational (recurrence residual 0.21 vs atom 1e-4). So the 15-digit
  rational route is atom/local (DMFT) only; the lattice needs conformal/algebraic resummation. Rational is exact
  along N (record) and along U only locally. rational_lattice_boundary.py + RATIONAL_LATTICE_BOUNDARY_RESULT.md.

- FULL CONSOLIDATION (v147): three models at highest capability. Frozen reference engine/ (194/194, never altered,
  fast/omp targets) + production hybrid (validates ==it, all caps: any-L/-fast/LD/guards/freeze) + surrogate (now
  with SU(N) EoS carriers sun_c1/sun_n1). Analysis supplements kept as separate CLI modules (design directive).
  README+QUICKSTART+engine/README refreshed. consolidation_v147.py + CONSOLIDATION_v147_RESULT.md.

- UNIFIED END-TO-END MODEL (v148): cdet_lab.py -- a control plane exposing EVERY capability as swappable components
  from the terminal (--target {eos,self-energy,addition-pole,double-occ,connected-det} x --method {ed,record,
  hubbard-i,diagrammatic,surrogate,hybrid,fast-minors,engine} x --model/params), without touching the frozen
  reference. Design grounded in a web search of physicist needs (SU(N) EoS, DMFT self-energy, DiagMC observables).
  `python3 cdet_lab.py list|validate|--target...`. cdet_lab.py + CDET_LAB_RESULT.md.

- IDIOT-PROOF CONVERSATIONAL FRONT-END (v149): cdet_shell.py -- plain language in, interpreted command shown back
  (all defaults visible, nothing hidden), confirm yes/no, run on yes; 'no' reverts to start but KEEPS named/saved
  configs. clig.dev best practices: CLI-as-conversation, discoverability (help/list/examples/configs), empathy
  (did-you-mean + example syntax on typos/bad methods). Synonyms map plain words to components (mott->hubbard-i,
  density->eos). Thin safe layer over cdet_lab (component map = single source of truth); every run routes through
  cdet_lab so the frozen reference stays the anchor. cdet_shell.py + CDET_SHELL_RESULT.md.

- BLIND-TEST HARDENING (v150): used cdet_shell as a zero-knowledge user trying to get stuck; found + fixed 6 real
  issues: (1) confirm step was a trap (cancel/back/help/quit looped -> couldn't even quit) -> now all escape; (2)
  N/n case collision (N=0 set vertices too) -> case-sensitive N vs n; (3) no validation (SU(0) ran, U=abc dropped
  silently) -> reject+warn; (4) synonym substring bug ('ed' matched inside 'connected') -> word-boundary scan; (5)
  rigid confirm phrasing -> intent-based yes/no ('actually nevermind' cancels); (6) menu/what-can-you-do -> help.
  Verdict: not possible to get stuck, always a labeled way back to start, logical, understandable, powerful.
  Self-test now 21 steps. cdet_shell.py + BLIND_TEST_v150_RESULT.md.

- SWEEP / STRESS HARNESS (v151): cdet_study.py -- scan a parameter (U/N/L/beta/mu/n) for any (target,method);
  detect convergence (|delta|<tol for k steps); cutoffs --max-time (wall-clock budget) and --accuracy-cutoff (error
  vs reference); outputs log + data.csv + summary.json + plot.png + ASCII plot with convergence/breakdown/cutoff
  points marked. Physically meaningful: diagrammatic Sigma vs ED breaks at the series radius (~pi/beta) -> the
  accuracy cutoff stops there; addition-pole vs L converges to z(inf). NL-drivable in cdet_shell ('sweep U from 0.2
  to 1.2 ... stop if accuracy drops below 5e-3'). cdet_study.py + CDET_STUDY_RESULT.md.

- SU(N) STEP 5 CAPSTONE (v152): the record-predicted EoS curve <n>(U). Extract per-flavor density U-series to K=8
  (complex-U contour, 2-site reference) for small N=2,3,4,5; record-predict the N=6 series (fit each order as a
  polynomial in N, evaluate at 6 -- NO SU(6) diagonalization); Pade-resum to the curve. Matches DIRECT SU(6) ED to
  ~1-2% out to U~1.2 (10x the bare-series radius ~0.16). Strong coupling needs conformal (v146 boundary). NET: EoS
  exactly N-predictable (record); U-reach set by the algebraic branch point. sun_eos_curve.py + SUN_EOS_CURVE_RESULT.md.

- STRONG COUPLING REACHED (v153): two-point resummation spans the whole U-axis. Anchor BOTH ends -- weak (lattice
  record series, v152) and strong (U->inf atomic limit, the v142 atom record m0 = single-site SU(N) atom density,
  no 2-site diag; + m1 hopping correction) -- both record-predictable from small N. A stable two-point Pade [2/2]
  (3 weak + 2 strong; higher orders get spurious poles) bridges the crossover. Record-predicted SU(6) EoS (only
  N<=5 data, no SU(6) diagonalization) matches direct SU(6) ED across ALL U, hits U/t=2.3 (Kozik benchmark) at
  2.4%, worst <5% to U=4. The SU(N) EoS is now record-predicted weak->strong. sun_eos_strong.py + SUN_EOS_STRONG_RESULT.md.

- 2D THERMODYNAMIC LIMIT (v154): the production route reaches the real 2D system. THE RECORD IS LATTICE-INDEPENDENT
  -- the leading EoS coeff n1=-(N-1)d d' (record x free single-flavor d,d') transfers across geometry, matching
  direct SU(N) cluster ED on 2-site/1D-ring/genuine-2D-cluster (2x3) to 1e-7..1e-9. Take the thermodynamic limit by
  replacing the cluster d,d' with converged free 2D k-integrals (eps=-2t(coskx+cosky)): d=0.6714,d'=0.1524 ->
  SU(6) 2D n1=-0.5116, NO diagonalization. Strong-coupling (atomic) anchor is lattice-independent, so the v153
  two-point extends to 2D (weak 2D Hartree + strong atom record), the production prediction to benchmark vs Kozik
  DQMC/experiment. sun_eos_2d.py + SUN_EOS_2D_RESULT.md.

- SECOND-ORDER coeff DECOMPOSED (v155): n2(N) = (N-1)^2 a + (N-1) b. a = d(d'^2 + 1/2 d d'') is the SELF-CONSISTENT
  HARTREE (free single-flavor derivs only; the naive 1/2 d^2 d'' is wrong -- it drops the d'^2 feedback term),
  validated vs the fitted (N-1)^2 coeff to 2e-7; the decomposition predicts n2(6) to 1.4e-4 vs direct SU(6) ED. b =
  genuine particle-hole bubble, subleading in N. THERMODYNAMIC LIMIT: a from converged 2D k-integrals (d,d',d'') ->
  2D SU(6) n2 dominant part 25 a_2D=0.1405, EXACT no diagonalization; bubble b is the one remaining single-flavor
  integral. Weak 2D series now exact through the dominant 2nd order. sun_eos_n2.py + SUN_EOS_N2_RESULT.md.

- CONSOLIDATION v156 (the v148-155 arc): a single health gate (consolidation_v156.py, ~1s) re-proves the whole
  current state coheres -- three-model cross-agreement (surrogate==production, addition pole, fast-minors==numpy)
  PLUS one fast live check, tied to an exact anchor, of every capability added since v147: the UI control plane
  (cdet_lab/cdet_shell/cdet_study) and the SU(N) EoS arc (weak record curve v152, strong two-point v153, 2D
  thermodynamic limit v154, 2nd-order Hartree decomposition v155). Frozen engine/ 194/194 untouched. The
  consolidation rule is now standing protocol (see THE CONSOLIDATION RULE section). consolidation_v156.py +
  CONSOLIDATION_v156_RESULT.md.

- TRIPLE-RUN BENCHMARK + hybrid improvement (v157): the consolidation rule now runs all THREE models head-to-head
  (surrogate / brute-force frozen reference / hybrid), compares strengths-weaknesses vs the frozen anchor, and
  applies improvements to the EVOLVING two only (the frozen source is never edited). FINDING: the hybrid's
  projector fast path is bit-identical to the default (verified: val 0.00e+00 and grid output unchanged) and
  collapses ~17x for crystallographic L. APPLIED: auto-enable it there (default-on, -nofast escape) -> measured
  ~26x grid speedup (0.34s vs 8.83s at NT=1500), val still 0.00e+00, frozen engine/ 194/194 untouched. Benchmark
  table recorded: surrogate ~1.5ms instant/exact-on-coverage, hybrid ~4ms exact+scalable+auto-fast, brute force
  ~2.5s canonical-but-slow. triple_benchmark.py + TRIPLE_BENCHMARK_v157_RESULT.md.

- CHAINED TWO-ROUND run (v158): run each model twice, round-1's terminal electron position (the RNG stream state)
  seeds round-2 -- a continuation, not a restart. Hybrid now exposes its terminal_state (print-only; val still
  0.00e+00; frozen source untouched). EFFICIENCY: chained 2xNT continuation gives 1.39x (~sqrt2) error reduction vs
  single NT (vs a high-NT ref), because the continued stream is independent/non-overlapping -- a naive SAME-seed
  rerun gives ZERO new info. EXPANSION: a deterministic result-seeded walk CYCLES (1-2 configs; a finite-state map
  must), but the chained-stream continuation sweeps 9/10 configs (no cycle). Both gains come from the same act of
  continuing the stream. Surrogate/brute role = fast evaluation (~1000x); stochastic continuation supplies
  exploration. chained_run.py + CHAINED_RUN_v158_RESULT.md.

- TWO-PARTICLE chained run (v159): repeat the chained two-round protocol with TWO particles -- exclusion (Pauli) +
  pair correlation, the two-body content the CDet captures. EXPANSION: the two-particle chained-continuation walk
  sweeps 10/10 pair-configs (no cycle) with exclusion held throughout (never double-occupies). EFFICIENCY: the
  chained continuation's ~sqrt2 error reduction reaches BOTH the one-body amplitude A (1.44x) and the two-body
  interaction response c1 (1.39x) -- so chaining helps the INTERACTION, not just the amplitude (an earlier 6-seed
  1.07x for c1 was noise; 12-14 seeds give ~sqrt2). The continuation gains survive one->two particles. Frozen engine
  untouched (only the v158 print-only terminal_state). two_particle_run.py + TWO_PARTICLE_RUN_v159_RESULT.md.

- CONFORMAL-BOREL resummation (v160): web-searched the CDet field -- lattice is the EASY axis (works in the
  thermodynamic limit; 12x12 in ~30s is normal validation range); the real frontier is ORDERS reached+resummed
  (~10-13 in practice), capped by a finite radius from a complex-U analytic structure (the v146 branch point). Added
  the field's state-of-the-art tool: conformal-Borel (Borel transform b_k=n_k/k!, Borel-Pade locate the COMPLEX
  Borel singularity |t_c|~1.05, exact re-expansion in w(t)=(sqrt(1+t/Uc)-1)/(sqrt(1+t/Uc)+1), Borel sum). Beats
  plain Pade 2-4x in the crossover (validated vs ED). HONEST CEILING: reliable strong-coupling reach needs the
  large-order/instanton structure (the field's hard part) or the v153 two-point bridge -- did NOT claim a fragile
  U=2.5 4% an early run showed. Pairs with the chained continuation (v158-159): reach-per-order (conformal-Borel) x
  orders-per-cost (chaining sqrt2) = the two levers the field pushes. sun_eos_conformal.py + SUN_EOS_CONFORMAL_v160_RESULT.md.

- CONSOLIDATION v161 (health gate + triple-run benchmark of the v157-160 arc; frozen baseline retained for parity):
  re-proved the whole state coheres -- v147 invariants (surrogate==production, addition pole, fast-minors==numpy);
  FROZEN BASELINE PARITY (hybrid 0.00e+00 vs the reference); v157 auto-fast bit-identical to -nofast (~28x); v158
  terminal-state chaining; v159 two-particle exclusion (10/10 pair-configs); v160 conformal-Borel beats Pade. Ran all
  three; recorded the parity benchmark (surrogate 3.55e-15 / hybrid 0.00e+00 / brute force 194/194 anchor). IMPROVEMENT
  CYCLE: profiled the inner loop -- set_freeze_d recomputes sample-INDEPENDENT occupation arrays every sample;
  precomputing+swapping is bit-identical (val 0.00e+00, grid identical) but the gain is NEGLIGIBLE (~0.6%, noise; C_V
  dominates) so it was NOT added; the genuine next lever (low-rank determinant update for the freeze-0->delta change,
  since the freeze enters g0 linearly) is identified but parity-risky and DEFERRED. Honest: not every cycle yields a
  new safe lever. Precedent: consolidation_v101/115/120/130/138/147/156. consolidation_v161.py + CONSOLIDATION_v161_RESULT.md.

- LARGE-L plane-wave propagator (v162): Paul's point -- the method's strength is that you do NOT need huge finite
  lattices; past the correlation length (~12-16 sites) results are already the thermodynamic limit. The 2D engine was
  capped at 16x16 because the numerical path stores eigenvectors (O(LMAX^2), LMAX=256). Added the documented closed-form
  route: square2d_G0_pw computes the free propagator straight from eps=-2t(cos kx+cos ky), G0(i,j;tau)=(1/N)sum_k
  cos(k.(r_i-r_j)) g_band(eps_k;tau), using only a 1D cosine table -> O(L) memory, NO eigenvectors. Reaches 100x100
  (10^4 sites, far beyond LMAX). EXACT vs the numerical path (worst |diff|=1.25e-16 at L=6,12). TD-convergence shown out
  to 100x100: NN propagator within ~5e-4 of infinite-system by 16x16, ~1e-5 by 32x32, Delta=2.2e-11 at 100x100 vs 64x64.
  The LMAX cap is BYPASSED (not raised -- raising it is O(LMAX^2) memory); the plane-wave path is the right tool, exactly
  as the original notes recommended. Existing numerical val2d still matches (no regression); frozen engine used read-only
  (194/194). square2d_pw_demo.c + lattices.c/.h + SQUARE2D_PW_v162_RESULT.md.

- UNIFIED CLI (v163): the first checklist item / quickest usability win -- a single top-level `cdet` command wrapping
  the whole suite, with subcommands validate/converge/resum/eos/run/sweep/lab/shell/info, --help, and friendly error
  handling. Output uses `rich` (colored tables/panels) IF installed, else a clean ASCII fallback -> the package stays
  SELF-CONTAINED (stdlib argparse only; no required deps). `cdet validate` runs all gates (frozen 194/194, surrogate,
  hybrid 0.00e+00 parity, 2D plane-wave, consolidation) and shows them green in one table; `cdet converge` is the
  4x4->100x100 TD demo; `cdet resum` the conformal-Borel-vs-Pade table. Defaults are fast (resum/eos N=4, fully
  ED-validated; N>=6 cold-atom is a several-minute production run with a disk cache + status note). Launcher `./cdet`;
  README quickstart prepended. cdet.py (self-test gate PASS).

- DOUBLE OCCUPANCY observable (v164): checklist item #3 (more observables) -- added D=<n_up n_dn> as a proper
  interacting observable (previously only the atomic single-site limit existed). Thermodynamic identity D per site =
  -(1/beta) dlnZ/dU / N_sites, so it rides the existing lnZ machinery: a complex-U contour gives the U-series (exactly
  like density_series for the mu-derivative). VALIDATED by TWO INDEPENDENT ED routes -- the lnZ U-derivative and the
  direct thermal average of the pair-occupancy operator D_hat -- agreeing to ~1e-10. Physical Mott suppression (D falls
  0.549->0.069 from U=0..3 for N=2); conformal-Borel resums (65x better than Pade at U=1); interaction energy
  E_int/site=U*D. Wired as `cdet docc`. double_occupancy.py (self-test gate PASS) + the CLI subcommand.

- SUSCEPTIBILITIES (v165): continued checklist #3 (more observables) with the linear-response pair -- charge
  compressibility kappa=d<n>/dmu and spin susceptibility chi_s=d<Sz>/dh|_{h=0}, on the 2-site SU(N) reference. Each is
  validated by TWO INDEPENDENT ED routes: a derivative route and a fluctuation-dissipation route (kappa==(beta/2N)Var(N),
  chi_s==beta Var(Sz)), agreeing to ~1e-7 (shared no code path). The physics is the opposite-trend Mott hallmark: kappa
  FALLS with U (charge fluctuations suppressed -> incompressible Mott state; 0.268->0.084) while chi_s RISES (local-moment
  formation -> magnetism; 0.268->0.487). Both get a complex-U weak series + conformal-Borel resummation (chi_s err 3.5e-3
  at U=1). Wired as `cdet chi`. susceptibilities.py (self-test gate PASS) + the CLI subcommand.

- VISUALIZATION (v166): checklist item #3 (built-in plots). Added plots.py -- matplotlib figures (Agg, no display)
  reproduced from the SAME validated code paths the gates use, so a figure cannot drift from the numbers: (1) 2D TD
  convergence (G0_NN vs L, 4->100, correlation-length band); (2) conformal-Borel vs plain Pade error vs U (log-y); (3)
  the Mott story (double occupancy + charge compressibility down, spin susceptibility up); (4) a 2x2 summary dashboard
  with a validation-status panel. Wired as `cdet plot [convergence|resummation|mott|summary]`. The python plane-wave
  G0_NN used for the convergence panel matches the validated C path to round-off. plots.py (self-test gate PASS) + the
  CLI subcommand. (cdet_figures/ is a runtime artifact, not shipped.)

- PACKAGING / CI (v167): checklist items #4/#6 (distribution readiness). Added pyproject.toml so `pip install -e .`
  installs a real `cdet` console command (entry point cdet:main) -- verified it runs `cdet validate` from outside the
  repo (5/5). Runtime deps numpy+mpmath; optional extras [viz]=matplotlib, [rich]=rich, [all]. MIT LICENSE. GitHub
  Actions CI (.github/workflows/ci.yml) runs on py3.9/3.11/3.12: builds the frozen engine + 194/194 gate, then
  `cdet validate`, the module self-tests, and the CLI self-test -- so the validation depth is enforced on every push.
  packaging_check.py gates the scaffolding (pyproject valid + entry resolves + CI runs the right gates + LICENSE).
  README quickstart now leads with `pip install -e ".[all]"`. (cdet_suite.egg-info is an install artifact, not shipped.)

- DUAL LICENSE (v168): Paul asked for free academic use but chargeable for business. Switched from MIT to the
  PolyForm Noncommercial License 1.0.0 (a standard license drafted by licensing lawyers) -- free for ANY noncommercial
  purpose, with educational institutions and public research organizations EXPLICITLY permitted (academic use is free
  regardless of funding source) -- plus a COMMERCIAL license required for business use (use by/on behalf of a for-profit,
  in a commercial product, or with anticipated commercial application). LICENSE now carries a DUAL-LICENSE header + the
  Required Notice + the full PolyForm NC text; COMMERCIAL-LICENSE.md describes the commercial grant + contact (placeholder
  to fill). pyproject license -> file=LICENSE with classifier Other/Proprietary; README updated. packaging_check.py now
  verifies the dual license (PolyForm NC text + explicit academic-free + commercial terms present). Honest caveat noted
  in-file: this is a standard structure, not legal advice -- have a lawyer review a real commercial offering. Package
  still installs (`pip install -e .`) and `cdet validate` is 5/5.

- SIGN GOVERNANCE (v68): parity falsified (50-59% even at mu=0); sign coherence decays on its own scale
  xi_s ~ 3.0 (3x magnitude); orientation is a mu-controlled phase (94% negative at mu=0.5 -> 75-100% positive
  at mu=1.5, same geometries) -- Friedel-class; coherence, not positivity, is the invariant. Quantitative
  phase law open. sign_governance.py + SIGN_GOVERNANCE_RESULT.md.

- PHASE LAW ATTEMPTED, DOUBLE FALSIFICATION (v69): static tau-averaged predictors 34% OOC (cannot represent
  the mu-flip); tau-integrated dominant chain 64-66% OOC (partial signal, parity-competition reversals);
  both under frozen single-cell calibration with a pre-set 75% gate. Magnitude lawful, phase determinant-
  level -- the hardness localized. phase_law.py + PHASE_LAW_RESULT.md.

## Open questions (to test next, one at a time)
- v37 DONE: 2D MC driver validated vs exact ED at orders 1-6; sign-problem wall mapped vs size and T.
- v38 DONE (the "extra orders" question answered): the determinant buys the ORDER axis (cost n^3 vs
  (n+1)!; removes per-order perm/|det| variance) but NOT the size/temperature wall (v37). Mechanism
  isolated and measured.
- v39 DONE (scaling law of R): metric adopted; but no clean parametric law at accessible sizes (shell-
  dominated, ensemble-sensitive, non-separable). A meaningful benchmark needs larger N at fixed density
  (unmeasurable now) or an asymptotically cleaner observable.
- v40 DONE: tested the aggregate observables; none decontaminates (single-order domination + shared a_n
  shell jumps). The lever is fixed filling fraction (closed shells), not a different summary statistic.
- v41 DONE: the organizing variable is the Fermi detuning delta; R is universal in delta at fixed T
  (amplitude A(N) shrinks with size). The controlled comparison is fixed delta (=0).
- v42 DONE: R(delta) = thermal near-shell feature (range ~ T, function of beta*delta on an isolated shell)
  + cluster background. Hierarchy T < shell spacing < bandwidth.
- v45 DONE: shifted-reference (pole-moving) expansion implemented and exactly verified; divergent bare ->
  convergent shifted at the Hartree-scale alpha; alpha* = the detuning knob. Coefficient-level exact.
- v46 DONE: counterterm=d/dmu identity (machine precision) + real-engine route (engine precision); shift
  realised as a resummation over bare engine output, frozen core untouched.
- v47 DONE: shifted coeffs sampled in one run via complex-mu contour on shared samples (no FD, no grid);
  orders 1-2 within 0.3 sigma of ED, mu-derivative cross-checked vs ED. Reference impl; engine untouched.
- v48 DONE: the shift's sign vs convergence optima COMPETE (same mu_ref, different settings); pole-moving does
  not move the sign wall and its optimal shift degrades the sign. Answer to the reviewer: no free lunch.
- v49 DONE: plundered contour deformation (the one sign-relevant tool from the roots-of-unity family) on the
  genuine v48 integrand -- NULL: optimal amplitude is the real axis, the cancellation is discrete between
  kink-pinned sectors. Our sign is a real sign-flip, not a complex phase. The deformation-covariate is also
  null (perfect correlation); the covariate family moves the prefactor, never R. Consolidated the three
  verified accelerations (shift/contour/control-variate, each a different axis) into best_methods.py +
  BEST_METHODS.md, all exact-checked, frozen engine untouched.
- v50 DONE: involution search by computation -- no sign-cancelling involution among the natural symmetries
  (ratio never -1), but an exact symmetry (|G_0|=2, diagonal swap fixing the external site) that folds the
  L^n site sum by up to |G_0|x, verified to 6.6e-17 and proven symbolically for all hopping t (sympy). Folds
  redundancy on the site space only -- not the Rossi 2^n, not the sign. symmetry_reduction.py + audit.
- v51 DONE: the redundancy fold scales with the lattice point group -- 4x4 stabilizer is full D4 (|G_0|=8,
  incl. column/row slices), giving up to 8x exact fold (4.65x/6.15x at n=2/3) vs 2x on 2x2; all slice ops
  fold (+1), none cancels (-1); proven for all t (sympy). square_point_stabilizer generator-based finder.
- v52 DONE: 45-degree slices of the 3D cube fold too -- 4x4x4 stabilizer is full O_h (|G_0|=48), all diagonal
  slices fold (+1), none cancels; exact 18.62x site-sum fold at n=2 -> 48x; proven for all t (sympy). The fold
  scales with size AND dimension (2x -> 8x -> 48x). cube_hopping/cube_point_stabilizer.
- v53 DONE: interior of the 2^n -- mask-fold fires only on symmetric configs (exact when it fires; measure-zero
  generically, honest negative); the generic win is the subset cache across the sum: 29.9x fewer determinants
  at n=3 4x4 (orbit x cache, independent), exact to 5e-15, 13.9x wall-clock. cv_cached/fold_site_sum_cached.
- v54 DONE: the -1 hunt closed -- it lives in the value channel (PH transpose) but is dressed by the equal-time
  sum rule into an inter-observable identity with counterterms; no per-config -1 at fixed mu. Slice mine: weight
  and sign concentrate on low-dim slices (x18.5 lines / x2.1 planes / x0.65 bulk; R 0.22/0.09/0.004).
- v55 DONE: slice-stratified estimator built and measured -- 22-44x at n=2 vs exact truth (Neyman demanded
  enumerating the heavy low-d strata), 2.1x at n=3 where the heavy stratum exceeds the enumeration budget;
  unbiased in both regimes.
- v56 DONE (ARC CLOSED): the sign-vs-convergence trade-off is generic in the doped regime; the one exact
  alignment is half filling at low T, forced by particle-hole symmetry (alpha_H=U/2 -> mu_ref=0 = the shell).
  A metric artifact (complex-vs-real residual) briefly faked a doped alignment; the self-test caught it and
  the correction is banked.
- v57 DONE (theory extraction begins): the slice hierarchy SURVIVES SCALE -- weight concentration strengthens
  (32x->165x, L=4->8); FastCDet (4.2e-17) banked as the scaling tool. [v58 amendment: the sign half of v57 is
  downgraded -- R estimator heavy-tail fragile; weight half stands and is strengthened.]
- v58 DONE: universality sweep -- weight concentration universal (all axes, robust, seed-stable; U exact by
  theorem); per-class sign structure downgraded to OPEN (estimator fragility demonstrated and banked).
- v59 DONE: the derivation attempt was made under freeze-then-predict and FALSIFIED -- MST/propagator
  geometry is a minor ingredient (~17% of variance, slope anomaly ~2xi); the concentration mechanism is open.
- v60 DONE: dual mechanism partially confirmed -- tau-interference is 40% of the variance (averaging it out
  doubles the geometric law); anisotropy real but insufficient; ~10x closed-line residual remains, with the
  ring-closure/winding-coherence hypothesis banked for v61.
- v61 DONE: the winding-phase form FALSIFIED by a paired antiperiodic-twist experiment (and the unpaired run's
  fake 4x banked as the artifact it was). The line enhancement is closure-independent; 1d channeling is the
  surviving untested hypothesis.
- v62 DONE: 1d channeling CONFIRMED (~2x at matched MST, graded monotone in collinearity, anisotropy-controlled,
  paired). Mechanism ledger: three confirmed + one falsified + ~4x residual unaccounted.
- v63 DONE (LOCKED): channeling compounds with length; clean identification gives b=0.537 (bulk-only) and
  c=+0.583 (paired contrast); frozen composition 59x vs measured 75.5x = 1.27x agreement (pre-set gate 2x).
  The weight-concentration mechanism arc is closed at the semi-quantitative level; deriving c is the open
  theory item.
- v64 DONE (PIVOT b): the genericity law split under testing -- PH convergence-lock (alpha*=U/2 at half
  filling) universal and quasi-exact across 2 clusters x 3 couplings; sign alignment cluster-dependent
  (fails on the 6-ring, as predicted from its own landscape). Blocked sector ED banked as the large-cluster
  tool.
- v65 DONE: baseline consolidated -- cdet_best.py front door (exact gates), BEST_METHODS.md v65 edition
  (composition table, two laws, standing methodology).
- v66 DONE: the no-brute-force simulator -- surrogate predicts brute structure with zero evaluations and
  accelerates signed totals where sign is mild; the measured ceiling (no gain at cancellation-dominated n=3)
  is the sign wall in estimator form. Next surrogate frontier would need a SIGN model -- exactly the open
  v58/tail-aware question.
- v67 DONE (THE KNOCK): sign model built -- v58 settled (CIs separate), line sign 92% predictable, the d<=1
  sector carries 77% of the signed answer at 0.3% of configs, and the hybrid estimator moves the ceiling to
  87-110x.
- v68 DONE: governance of the signed weight -- magnitude envelope x coherence decay (xi_s ~ 3, outliving
  weight) x mu-controlled orientation phase (Friedel-class; parity falsified). v67's mechanism restated
  correctly (coherence, not positivity).
- v69 DONE (NEGATIVE, BANKED): the formula-grade phase law -- static Friedel and dominant-chain reductions
  both falsified under frozen protocol; the phase is determinant-level interference as far as tested.
- v70 DONE (ROTATION 1/3, fold-in): sector_estimator.py -- scalable exact-sector machinery (any L), exact-
  moment design methodology (NEW STANDING RULE), v67 gain corrected 87-110x -> ~6x on the record, L=6 sector
  sign flip confirmed in exact arithmetic.
- v71 DONE (ROTATION 2/3, item a, surrogate-first): pairing depth -- NO finite depth; the complete single
  free determinant fails (44% OOC, both time conventions); the phase localized by elimination to the coupled
  two-spin integrand. STANDING MODE (user directive): surrogate-first with engine crosscheck until major
  surrogate gains.
- v72 DONE (ROTATION 3/3, item c, surrogate-first): the bulk remainder = mu-controlled FRIEDEL RINGS in MST
  (alternating-sign shells, mid-range dominance, mu-shifting pattern confirmed by frozen test); the
  monotone-decay surrogate model falsified by its own crosscheck -- the falsification is the discovery.
  ROTATION COMPLETE: all three passes converged on the orientation phase as the single missing object.
  NEXT (surrogate-first queue): the LEARNED orientation channel -- fit orientation vs geometry/mu/L with the
  exact shell tables as crosscheck; then L=6 shell fold; carried theory items: derive channeling c; explain
  PH quasi-exactness; 6-ring on-level sign peak.
- v73 DONE: the learned orientation channel FAILS the same frozen gate (33-35% held-out, both model classes;
  wrap-interpolation impossibility identified) -- the orientation channel is CLOSED from both directions at
  this scope.
- v74 DONE (queue item b): surrogate refinements -- ceilings-first practice; R2-mixture artifact corrected on
  our own reporting; the TRANSFERABLE magnitude model (L=4->L=6 R2 0.57, med-err 1.81x); r_pred regime map
  (+0.32/+0.27/-0.57 by rank).
- v75 DONE (the FOLD): wrap-collinearity correction (true sectors 1,618/82% at L=4 and 16,950 at L=6; the
  wrap-safe rule extends to definitions); first exact 10M-config totals (mu=0.5 -2.498e-3 validating the v70
  pilot; mu=1.5 -2.225e-3); sector share falls 82% -> 42% with size and opposes the total at mu=1.5; rings
  persist with mu-dependent nodes.
- v76 DONE: the ring period is NOT resolved at L=6 -- and cannot be (xi_s/period ~ 2.5). Spectral
  near-misses killed by permutation null; contact-shell coherence real and mu-flipped.
- v77 DONE (THE MU-PERIOD LAW): Delta-mu* = pi/(q beta), q -> 1; Friedel falsified; the channel
  half-reopens (73-76%, at the bar; offset calibration the residual); beta >= 12 protocol boundary.
- v78 DONE (THE COMB): cancellation lemma + direct complex-mu detection; the charge-staircase reading
  falsified; mechanism established (comb-limited variation).
- v79 DONE (CONSOLIDATION): cdet_surrogate.py + BEST_METHODS v79 edition; transfer pooled 1.88x; per-class
  intercepts tested and rejected.
- v80 DONE (THE RESONANCE REGIME, KT-review round): two-regime law proved; the v77 beta>=12 boundary
  RETRACTED; naive midpoint law killed; transfer bimodal via multiplicities.
- v81 DONE (THE PAIR LAW): flips converge to levels as eps +/- c/beta; candidate c = ln(deg)/2 banked with
  its no-free-parameter test queued.
- v82 DONE (THE TWO-CLASS STRUCTURE): the fired prediction FAILED at L=8 level 2, exposing Class-II
  beta-STATIC midpoint crossings; midpoint law resurrects selectively.
- v83 DONE (THE RESIDUE RATIO): c = logit of residue-polynomial roots, derived and
  beta-transfer-tested; multiplicity = root count; the creep located.
- v84 DONE (THE SELECTION RULE): both Class-II conditions measured; pair identity by flow.
- v85 DONE (CONSOLIDATION -- THE RESONANCE ATLAS): one spine; integration audit A-F; the unclassified
  ~1.8 object caught; BEST_METHODS v85 edition.
- v86 DONE (THE CORE C SURROGATE): every banked advance frozen into dependency-free C; engine-style
  fresh-seed gate at 3.6e-15.
- v87 DONE (THE C SURROGATE UNDER TEST): clean-room portability fixes; efficiency measured; two
  n-ceilings stated; transfer scope revised to 2.3x pooled.
- v88 DONE (THE ORDER AXIS): the spine survives n=4 and (partially) n=5; C surrogate extended;
  exact-determinant numerics catch.
- v89 DONE (THE DEEP PARTNER): three level-2 roots; two anomalies closed; the creep first seen in
  position. [Law-form REVISED in v90.]
- v90 DONE (#100, THE TWO-WINDOW CREEP CROSS-CHECK): the deep trajectory is ANCHORED and
  geometry-independent -- the third static-class instance; anchor open (2*sqrt(2)-1 vs 11/6).
- v91 DONE (THE CORRECTION PROPAGATED): both surfaces updated; gate G added.
- v92 DONE (THE ANCHOR TEST): law scoped; heavy-tail protocol installed; honest a_inf with the bridge
  verdict NOT RIGID -- structural route named primary.
- v93 DONE (THE EXPONENT-BALANCE LAW): law derived; field theorem; frozen test selected 11/6 at ~80:1.
- v94 DONE (THE SIDE-BY-SIDE): out-of-sample unselected 11/6 (~9:1 for 13/7 on the new points); the
  identification REOPENED among {11/6, 13/7, constant-1.8467/chord}; menu-vs-flatness tension named.
- v95 DONE (THE DEGREE BOUND): census-settled (7 = 2n+1; full support; differences-menu); tension
  dissolved (24/13, q=13); open among {13/7, 24/13}.
- v96 DONE (COEFFICIENT PROGRAM PHASE 1): FrozenCDet instrument validated + faithful; background ALIVE
  (no midpoint static in (1,2)); creep carrier = far-level antiperiodic images; prediction test
  inconclusive, phase-2 spec computed.
- v97 DONE (THE PARITY TABLE): strict A=0 rule falsified by its own frozen test; suppression pattern
  banked; v84 static reread as root-flow crossing; L=8 deep-beta crossover prediction REGISTERED.
- v98 DONE (THE METHOD AUDIT): confound found; ratios underpowered (spec recorded); #107 downgraded to
  CANDIDATE; L=8 prediction quantified (FROZEN_CURVE_Z8); queue reordered by leverage.
- v99 DONE (PHASE 2): IS estimator (31x); frozen polynomial measured; root-flow branch excluded;
  TWO-SECTOR DISCOVERY (the delta1 antiperiodic-image sector Delta is the second player at the zero).
- v100 DONE (THE DELTA SECTOR): the second player is a delta1 x f2 CROSS-TERM (Delta(0)~0), measured
  and beta-growing, reconciling the frozen root toward physical; the closure reduced to the assembled
  root flow z(beta).
  OPEN QUEUE (v118 frontier): the deep-beta SCALE program is CLOSED -- z(inf)=2 resolved (v111), derived
  (v112: A~1/beta^3 corner-confined, |c1|~beta^-0.3 level-2 de-confined), Fermi-locked (v114), and DOUBLY
  universal: probe-independent (v114) and site-independent (v116). The SIGN side: A's sign oscillates with
  geometry (v117, Friedel-class), and moving mu (v118) showed BOTH sign and scale are mu-INVARIANT in (1,2) --
  the FROZEN Fermi surface is a discrete object (the filled-level set) governing both, rigid in mu (this
  CORRECTED v117's coincidental 2k_F(mu) wavelength match). The full 2D Friedel map is DONE (v119): the elementary
  rho(0,r)=FT of the occupied region is cube-symmetric, short-wavelength (wavevector (120,180)deg = level-1|2
  boundary modes), and EXACTLY mu-invariant (0 modes in the gap (1,2)); A's sign superposes these. The
  elementary rho is now in C (v121: cfriedel.c, plane-wave form, no eig, ~5e-11 vs Python). MULTI-LATTICE
  (v122): mu-rigidity is CRYSTALLOGRAPHIC (L in {1,2,3,4,6}); scale (z=lowest-empty) + Friedel are UNIVERSAL;
  the plane-wave propagator makes the brute force O(N x MC), L-agnostic. PHASE 2 DONE (v123): cdet_planewave_engine.c (plane-wave
  determinant, any L, validated == stable at L=6); scale law z(inf)=lowest-empty-level PROVEN at L=4 (->2) and
  L=6 probe=3 (->3). DONE (v124): (a) continuous-threshold
  freeze (mode 2) -- z(inf)=sqrt2 (irrational) PROVEN at L=8; (b) projector fast path (EXACT, 73x at L=12) ->
  L=100 (1e6 sites) a day-long z-flow; run_to_log harness + NaN guard for safe unattended runs. LARGE-L STUDY DONE (v125): z(inf)(L)=lowest-empty(L) marches
  to mu (gap~L^-3.3), ran L=100 (1e6 sites) at 52s/pt; finding = signal vanishes as the gap closes. NEXT:
  signal budget QUANTIFIED (v126): c1 binds,
  budget ~ L^3 ~ N (polynomial, no exp wall); launch recipe written. selection rule vs L RESOLVED (v127): sign(c1)
  Friedel-oscillates, rule goes marginal in continuum. c1 jitter RESOLVED (v128): no period, arithmetic
  (which multiplet is lowest-empty); v119 contrast clean. NEXT: actually launch the day-long L=100 run (recipe
  ready) and bank the resolved coarse flow; profile fast-path precompute memory at L=100; adaptive eigenvalue
  binning past the ~45x collapse; A continuum wavevector EXTRACTED (v129):
  rho Friedel edge -> kx/L~0.347 (120deg, 3-site end), v119 confirmed as convergent continuum feature. NEXT:
  actually launch the day-long L=100 z-flow (recipe ready, v126) and bank the resolved coarse flow; profile
  fast-path precompute memory at L=100; pin the exact continuum edge value analytically (the W(kx) half-max
  of the fixed Fermi surface); test whether A's sign at the vertices is predicted by rho at kx/L~0.347. (consolidation v130 done.) CoS ASSESSMENT done (v131):
  integration list ranked. If pursuing: #1 DONE (v132, O(2^n n^2) path verified vs engine). NEXT
  integrations (all supplements): #2 SU(N) generalization (record-carrying minors, O(n^3 4^n) N-independent ->
  the N=6 Yb EoS); #3 self-energy/irreducible series (new observable); #4 CoS MC symmetrization; then wire the
  #1 O(2^n n^2) path into the engine hot loop behind the val-mode gate. AND (the crux Paul flagged): pin down
  whether z(inf)=lowest-empty encodes a real spectral observable -- RESOLVED v133: yes, the single-particle
  addition pole (free now; self-energy #3 -> interacting). CONSOLIDATED v138 (three paths agree; docs refreshed). NEXT, ranked
  by the v138 learnings: (a) #2 SU(N) (the N=6 Yb EoS, reuses fast minors): STEP 1 DONE (v142, atom EoS + N-polynomial record);
  STEP 2 DONE (v143, the record survives hopping on the 2-site lattice ED); STEP 3 DONE (v144, the production
  EoS route: first coeff from g0 x record, verified at N=6 with no N-flavor ED); STEP 4 DONE (v145, 2nd-order
  record persists + the gravity-loop resummation mechanism found IN N: the all-N EoS resums rationally from a few
  small N); STEP 5 NEXT = the full connected determinant + closed-loop record + tau-integrals (v132 fast minors)
  for the strong-coupling-IN-U EoS curve;
  (b) #3 resummation (Pade/conformal) to push Sigma past the bare radius ~0.8 -- the real strong-coupling route;
  (c) #5 wire fast minors / the diagrammatic sigma_n into the engine hot loop (val-gated); (d) surrogate Hartree
  carrier; (e) [v139 stress test] wire the deep-probe LD path + the 3 input guards are now in the hybrid. The
  self-energy observable + exact coefficients are in place; strong coupling = resummation (v140: Pade extends reach;
  precision = extended-precision arithmetic, not the gravity-loop exact-recurrence route which needs a rational series). RESOLVED (v146): rational structure lives (i) in U at the
  ATOM/LOCAL self-energy only (lattice Sigma is ALGEBRAIC -- hopping makes eigenvalues nonlinear in U) and (ii) in N
  via the record (v145, exact). So the 15-digit U-route is DMFT/atomic; the N-route is realized (why CoS is
  N-independent). Open continuations: SU(N) EoS DONE weak->strong (v153, U/t=2.3 at 2.4%) AND in the 2D THERMODYNAMIC LIMIT (v154: leading coeff via
  record x free 2D k-integral, transfers across geometry to 1e-8, no diagonalization). state CONSOLIDATED at v156; triple-run benchmark + hybrid auto-fast (26x) at v157; chained two-round continuation at v158; two-particle chained run at v159; conformal-Borel resummation (field's order-axis tool, beats Pade 2-4x) at v160. NEXT physics: the one remaining single-flavor
  amplitude -- the local 2D G(tau) particle-hole bubble (the (N-1) b term) -- to complete the exact 2D weak series,
  then feed it through conformal-Borel (v160) + the v153 two-point strong anchor for the full thermodynamic-limit
  curve vs Kozik DQMC. THE ORDER AXIS is the real frontier (lattice is easy -- thermodynamic limit): push more
  reliable orders (chained-continuation statistics, v158-159) and better resummation (conformal-Borel v160 +
  large-order/instanton structure). CoS MC symmetrization (#4); record-R pruning
  (#6); QTT (#7 parked). The unified
  control plane cdet_lab.py (v148) is the terminal entry point to every capability; cdet_shell.py (v149) is the
  friendly conversational front-end over it (plain language -> confirm -> run, named/saved configs). NEXT on the sign side: derive analytically how the determinant superposes the elementary short oscillations into the
  observable A-sign (the v117 envelope) -- i.e. the map from rho's boundary wavevector to A's apparent
  envelope; and whether the determinant superposition has its own selection rule (which site geometries give
  a physical root, the v116 sign(A,c1) pattern). Then re-examine v112-v113's 'gap = 2-mu' identification
  given the mu-invariance (the controlling gap may be the frozen level gap 2-1=1, not 2-mu -- a refinement,
  the asymptote z=2 is unaffected). Older scale threads (all theory-of-where, none move the wall):
  the corner-integral CONSTANT (J_A->const value) from first principles; the de-confinement power 2.7 from
  the level-2 channel count; whether the same corner/smallest-gap mechanism governs other windows ((1,3,5),
  delta-sector) -- NOTE v114: the PROBE cannot be moved off the Fermi-surface level (probe=3 diverges), so
  'other windows' means other SITE choices at the same Fermi-surface probe, not other probe levels. Carried: the suppression mechanism (even-window 20-40x); the (2,3) dead-residue; root flow
  with n; channel engineering; 6-ring on-level peak; PH quasi-exactness; exact pi/beta constant. Superseded note: v108 built+certified the log-domain
  G0_atom_stable in C at 1.29x the naive cost and ~1000x the Python stable engine -- port the deep-beta
  measurement loop to C so the 4-point/series A(beta), c1(beta) grids become 20-point grids, cutting
  v107's 10-40% rate errors and tightening z(inf)=1.882(18); then decide 15/8 vs 17/9). Original note: 15/8 vs
  17/9 open): pin rho_c1 with a denser c1(beta) grid, measure the CROSS-TERM d1(beta)'s own rate (does it
  shift the asymptotic rho_c1_eff?), and add the c2 curvature -- to decide 15/8 vs 17/9 vs a non-rational
  rate difference; then re-fit the surrogate's pool carriers to the assembled flow (the closure: the full
  coefficient grid A, c1_frozen, d1, c2 at
  beta in {36,44,52} to +/-5% via IS; assemble z(beta) = 2 - ln s*(beta)/beta; test vs the empirical
  pool's deep points 48/52/56 as a FROZEN PREDICTION -- closes 13/7-vs-24/13); THE TAU-INTEGRATED RATE
  RE-DERIVATION (the corner saddle for hole monomials -- fixes the menu theory; now also explains why
  d1 grows with beta; semi-analytic); THE L=8 CROSSOVER TEST (FROZEN_CURVE_Z8 carries the one-sector
  caveat -- re-derive with the cross-term or test as-is and learn); THE DISCRIMINATING PARITY WINDOW
  (A_even to +/-10%, cheap with IS); then: the suppression mechanism; the (2,3) dead-residue mechanism;
  the (1,3,5) deep-beta series; the root flow with n; channel engineering; the 6-ring on-level peak;
  carried: channeling c; PH quasi-exactness; the exact pi/beta constant.
- OPEN (v65 candidates): (a) tail-aware sign statistics (weighted bootstrap on per-class R) to settle the
  v58-downgraded sign-hierarchy question; (b) WHY does the 6-ring sign peak sit ON a level (-1.0) rather than
  in the PH gap -- the naive shell picture fails there (new, from v64); (c) theory items carried: derive the
  channeling coefficient c ~ 0.5-0.6, and explain the quasi-exactness of the PH-shifted series., or is there a 'both at once' regime?): repeat the
  alpha_conv vs alpha_sign comparison across (i) several fillings/mu on 2x2, (ii) a 3x3 cluster, (iii) two
  temperatures. The decisive search: a filling where the Hartree (convergence-optimal) point COINCIDES with a
  closed shell -- there, and only there, would the same shift improve both. If found, characterize it (the one
  expert-relevant case); if the optima are generically separated by ~half a shell spacing, bank 'trade-off is
  generic' with the pole-vs-shell mechanism as the explanation. EITHER outcome is a clean, honest result.
- v27 DONE: the high-order time-integration driver (cdet_order_mc) is built and validated against
  the frozen baseline at n=1,2 within MC error; n>=3 terms are now computable.
- v28 (now unblocked): wire the atomic-reference (hopping/shifted-mu) expansion as a g0/reference
  swap into cdet_order_mc (the engine ships G_exact_atom) + the counterterm; the payoff is reduced
  MC sign-variance at strong coupling so the same nmc reaches higher order. Validate the resummed
  observable against the FROZEN baseline / cdet_order_mc, re-run the v26 crash-safe stress as a true
  two-binary race, and handle the U~4t crossover seam with the v23 Pade resummation. Scheme already
  validated on exactly-solvable anchors (v23 atom, v24 dimer).
- separately: tame the MC sign-variance itself (importance sampling of vertex times near the external
  kinks / coincidences) so even the bare high-order series reaches further before the sign wall.
- v31 DONE: out-of-core blocked C_V (bit-split) validated -- exact arithmetic, peak RAM O(2^nL) fixed,
  the accuracy-first/RAM-bounded/HDD-overflow path. Butterfly shelved.
- v32/v34 DONE: blocked_cv is wired under cdet_order_mc as CDET_BLOCKED (out-of-core per-sample C_V,
  == PLAIN to 1.1e-12). REMAINING: push it to very large n on real disk for a huge-lattice run (hours
  acceptable); use flat in-RAM C_V for small n (fast), the blocked path only past the RAM wall.
- v32 (CV) DONE: the control-variate idea is proven low-order (71x) and tested high-order (simple
  references de-correlate -> 1-2x). High-order CV needs an adaptive/learned surrogate; high
  correlation at high order is the open problem (the sign problem in disguise).
- v33: a LEARNED high-order surrogate (TCI / low-rank fit of the actual C_V integrand) as the control
  variate for cdet_order_mc, OR fold the v30 atomic reference in as a residual-shrinking reference
  (which reduces variance at its source rather than via correlation). Then the out-of-core blocked_cv
  wiring (v32 plan above) for the huge-lattice runs.
- v33 DONE: the learned-pattern reference is the observable-level control variate (rho=0.998, 229x),
  ~100x stronger than v32's per-sample parametric ones; the two live at different levels (per-sample
  sign-variance vs observable/IR convergence).
- v34 DONE: the validated accelerations are now switchable config modes on cdet_order_mc_cfg (PLAIN
  bit-identical / BLOCKED out-of-core exact to 1.1e-12 / CVAR unbiased). CVAR nets 1x with an MC-
  estimated reference mean; the net-win needs an analytic E[Y] -- which is the v35 reference build next.
- v35: build the Luttinger-liquid GREEN'S-FUNCTION reference from the in-hand K_rho + spin/charge
  velocities and SUBTRACT it inside cdet_order_mc, so the high-order MC computes only the small
  residual (the correlator->Green's-function bridge). This is the concrete 'closing the loop': patterns
  learned from the engine, fed back to accelerate it. Then the out-of-core blocked_cv wiring for the
  huge-lattice runs.
- streaming/out-of-core: DROPPED by decision (v29) -- staying in RAM. The fast butterfly is retained
  only as an in-RAM speed option for the n~19-23 window (long-double Mobius for precision), not as a
  way to exceed RAM.
- v30 DONE (proxy): the atomic-reference lever is quantified exactly on the atom -- order to 1e-6 at
  U=2 goes infinity -> 3-11, largest term 3.8e12 -> 0.2 (cancellation cured). Target set.
- v31 (the real build): counterterm-correct atomic/shifted reference in cdet_order_mc's C path --
  swap lattice_G0 for a shifted-mu / dressed reference and carry the counterterm (a dressed reference
  double-counts self-energy insertions otherwise). Validate the resummed observable vs the frozen
  baseline / cdet_order_mc on a real lattice at strong coupling; hit the v30 target (single-digit
  orders where bare diverges); handle the U~4t seam with the v23 Pade. Scheme validated: atom (v30),
  dimer (v24).
- fold in the learned-IR control variate (exact K_rho power law / velocities / CFT tail) as the
  reference, closing the loop: patterns learned from the engine, fed back to accelerate it.
- v34/v35 DONE: the cdet_order np-overflow (quad.c node arrays double[64], overflow for np>64) is fixed
  (sized to np), confirmed converged for all np with MC agreement across params (standing gate 4), and as
  of v35 PROMOTED into the frozen baseline along with the v26 dynamic-buffer/OOM-safe cdet_engine.c --
  engine/ now reproduces all frozen constants exactly and additionally runs n>16 / np>64.
- the large-L INTERACTING tower point (L=20 = 240M states) stays beyond ED; from the
  DiagMC engine it needs a dynamical charge correlator + analytic continuation, with the
  per-order 2^n the documented wall -- the engine's regime, a separate effort.
- Spin/charge velocities from finite-size scaling; the Drude weight from twisted
  boundaries; the compressibility.
- Does a second scalar break the spin-correlator ~2.5% plateau, and is it worth it?
- Doping for the spatial correlator, where the shape itself becomes U-dependent
  (2k_F/4k_F competition) and the two-shape model is expected to need a third shape.
