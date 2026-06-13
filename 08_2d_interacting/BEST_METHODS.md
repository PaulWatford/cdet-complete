# Best methods — what works, what it moves, and what it does not

The verified accelerations for the CDet / DiagMC pipeline, consolidated. Each composes with the **frozen
engine** (which stays untouched, 194/194) and is exact-checked by `best_methods.py`
(`python3 08_2d_interacting/best_methods.py` → all PASS). The organising fact: the sign problem has three
*different* axes, and a method that moves one generally does not move the others. Stating that honestly is
the point.

| Method | Axis it moves | Verified | Does **not** move |
|---|---|---|---|
| **Shifted reference** (v45/46) | convergence (complex-U pole) | bare diverges (radius 1.0, K=11 err 1.6) → shifted converges (radius 2.6, K=11 err 1e-5) | the sign ratio R |
| **Complex-μ contour** (v47) | derivatives / counterterms | shifted coeffs via contour-sampled μ-derivatives match the direct shift to 6e-14 | the sign ratio R |
| **Free-baseline control variate** (02, v33) | prefactor (variance) | weak-U range reduction ×8.4 (U=0.5), fading to ×1.5 (U=4) | the sign ratio R |

## 1. Shifted reference — the convergence lever
The chemical-potential counterterm H(ξ;α) = [H₀(μ)+αN] + ξ(U·H_int − αN) is the physical Hamiltonian at
ξ=1 for **any** α, but α moves the convergence-limiting pole in the complex-U plane. At the Hartree-scale
shift α* ≈ U⟨n⟩/2 a divergent bare series becomes convergent — and since CDet per-order cost ~2ⁿ, saving
orders is an exponential cost cut. Use it whenever the bare series is slow or divergent.
Modules: `shifted_expansion.py`, `counterterm_shift.py`.

## 2. Complex-μ contour — the derivative lever (the roots-of-unity tool)
The one-body counterterm is exactly d/dμ, so the shifted coefficients are μ-derivatives of the bare ones.
Evaluating the bare coefficient on a **circle in complex μ** and applying the Cauchy / roots-of-unity
filter returns *all* μ-derivatives in a single pass, at machine precision, with no finite-difference bias
and no μ-grid. This is the family's master "total signed terms analytically" move, deployed: it is also
how the engine's exact coefficient extraction works. Modules: `counterterm_sampler.py`,
`counterterm_shift.py`.

## 3. Free-baseline control variate — the prefactor lever
Subtract the analytically known U=0 part and sample only the small interaction remainder. Where the
remainder is small (weak coupling) this strips most of the dynamic range before sampling — a genuine
variance (prefactor) reduction. The validated strong version is the learned IR/CFT reference
(`02_control_variate`, v33: ρ=0.998, ×229). Use at weak-to-moderate U; the win fades as U grows.

## The wall these do not move
**R, the per-configuration sign ratio, is untouched by all of the above.** The shift trades it (v48:
convergence-optimal shift has the *worst* sign); contour deformation and the deformation-covariate are null
on it (v49: our sign is a real sign-flip, not a complex phase — see `CONTOUR_DEFORMATION_RESULT.md`).
Control variates reduce variance, never R, so none of the prefactor tools change the exponential scaling.
That floor is the fundamental, NP-hard sign problem (Troyer–Wiese); the engine's per-order 2ⁿ is the
documented order-axis cost. The honest recommended pipeline is therefore: **shift for convergence, contour
for derivatives, control variate for the prefactor — and operate on a closed shell for the best available
R — with no claim that any of it crosses the wall.**


# v65 EDITION — the consolidated baseline (everything verified v49–v64, composed)

The front door is now **`cdet_best.py`** (self-test PASS, all gates exact). What it composes:

| layer | tool | measured factor | banked | exactness |
|---|---|---|---|---|
| evaluator | `BestCDet` (= FastCDet) | ~40× wall-clock | v57 | 4.2e-17 vs validated CDet |
| site sum | orbit fold (Burnside) | 2× / 8× / 48× by lattice | v50–52 | 5e-15, sympy-proven |
| site sum | subset cache | ~5–7× fewer determinants | v53 | 5e-15 |
| big lattices | slice stratification | 2–44× variance (unbiased) | v55 | bias ≤0.5σ vs exact truth |
| series | shifted reference α=U/2 at half filling | series **quasi-exact** (err ~1e-5 at K8) | v45/56/64 | ED |
| series | complex-μ contour derivatives | all orders, one pass | v47 | ED |
| variance | free-baseline control variate | prefactor | v33/49 | exact subtraction |

**The two laws the baseline encodes** (constants in `cdet_best.CONCENTRATION_LAW` and
`recommended_shift`):
- *Shift law (v56 split by v64):* α\*=U/2 at half filling is universal and quasi-exact; whether the
  PH point also has good sign is cluster-dependent — measure `r2_profile` before assuming.
- *Concentration law (v57–63, locked 1.27×):* ln W ≈ a − 0.537·MST + 0.583·ℓ_coll, modulated by
  τ-interference (40% of variance). Use for stratification/importance design.

**Standing methodology** (each rule bought with a banked failure): pair every comparison (v61);
robust statistics over heavy tails (v58); wrap-safe fits (v60); freeze-then-predict with pre-set
gates (v59–63); stratify mixtures before regressing (v59); identify coefficients where they can't
contaminate each other (v63); a failing gate is data (v56/58/62).

**What none of it moves:** R, the physical sign at fixed μ — the wall is mapped (fold channels are
provably +1; the value channel's −1 is dressed into an inter-observable identity, v54), not breached.
Honesty is the content.


# v79 EDITION — the surrogate consolidated (everything proven v66–v78, composed)

Two front doors now: **`cdet_best.py`** for exact computation (unchanged), **`cdet_surrogate.py`**
for no-brute-force prediction. What the surrogate composes, with verified scope at the point of use:

| Component | Law / capability | Verified | Honest limit |
|---|---|---|---|
| Wrap-safe sector (v75) | coherent sector = common cyclic line through origin (group-invariant) | true sectors 1,618 / **82%** at L=4; 16,950 at L=6; fold-consistent | sector share falls 82%→42% with size; opposes the total at μ=1.5 |
| Magnitude model (v74/79) | 10 linear features, L=4-calibrated, 8-shot **line** intercept transfer | pooled median per-config error **1.88×** at L=6 (draws 1.74×/2.69×, mixtures declared); ceiling 0.95 | in-distribution R² ~0.59 < ceiling; residual is the τ-structure family; per-class intercepts tested and **rejected** |
| r_pred regime map (v74) | sign-survival predictability coextensive with coherence | within-rank OOS R² **+0.32 / +0.27 / −0.57** | deep bulk strictly unpredictable — the surrogate reports the regime instead of pretending |
| Orientation channel (v77/78) | flips with period **Δμ\* = π/(qβ)**, q→1; mechanism = **Matsubara comb** (⟨C⟩_τ exactly rational in fugacity; poles at height π/β) | period law β=4–8, R/L-independent; comb detected directly (3.9e6× at-level divergence); calibrate-then-predict 73–76% held-out | **at the bar**, not above it; residual = offset calibration; β≥12 protocol boundary |

**The phase program's arc, closed (v68→v78):** observed → irreducible in geometry (derived *and*
learned routes closed under frozen gates) → law measured in (μ,β) → mechanism located in the
complex plane (the comb). The standing walls are unchanged and restated: **R(N,β) still decays
exponentially — nothing here crosses the sign problem**; per-geometry deep-bulk orientation remains
engine-only.

**Methodology rules earned since v65 (the short list):** measure the label-noise ceiling before
chasing R²; R² without a declared test mixture is not a quality claim; heavy-tailed estimator
comparisons must be exact-moment-based; spectral peaks need permutation-null calibration; discrete
coordinates are analyzed unbinned; wrap-safety applies to *definitions*, not just fits; protocol
claims require a seed-robustness sweep; check ξ_s/period before designing a period measurement;
and when a heuristic agrees with a measurement, test the mechanism's *distinctive* prediction.

# v85 EDITION — the resonance atlas (the sign structure of the μ-axis, v80–v84 consolidated)

The front door for resonance-regime predictions is **`resonance_atlas.py`** (integration audit A–F, PASS).
What the arc established, component by component:

| Version | Law | Verified | Honest limit |
|---|---|---|---|
| v80 two-regime | thermal π/β winding → level-locked, geometry-independent flips | attraction p=0.025; coincidence p=0.013–0.041; v77 β≥12 boundary retracted | crossover empirical (βΔε ≈ 8–12) |
| v81 pair law | Class-I flips → levels as ε ± c/β | 4 fits, best rms 0.004 | level 2 grid-pinned; ln(deg)/2 was a one-level fit |
| v82 two-class | Class-II β-static crossings at selected midpoints | 1.819±0.009 flat vs 1.828; prediction-failure exposed the class | selection unexplained at the time |
| v83 residue ratio | **c = logit of residue-polynomial roots**; multiplicity = root count | β-transfer max 0.022, no refitting; 3-geometry multiplicity pattern | one level, extraction at β=20 |
| v84 selection rule | static ⟺ background ≈ 0 AND opposite-sign residues; μ\* = mid + ln(−B/C)/2β | both conditions measured (1.0σ vs 4.5σ); pair identity by β-flow | one case each way; A-zeros underived |

**One spine.** Every resonance-regime flip is a logit-type law μ\* = anchor + ln(ratio)/(qβ):
Class I — anchor = a level, ratio = root odds, q=1; Class II — anchor = a level-pair midpoint,
ratio = the two-residue ratio, q=2. Residues decide attendance; positions are geometry-free,
multiplicities are not. The thermal regime keeps v77's π/β winding with geometry-dependent offsets.

**Methodology rules added by the arc (continuing the v79 nine):**
10. A discarded disagreement between two measurements may be two real scales — run IS/IS-NOT before
    declaring unmeasurability (v80).
11. Re-measure at finer resolution before banking a drift (v80).
12. When hunting a limit set, measure trajectories and extrapolate — candidate-set tests are
    underpowered against points in flight (v81).
13. A one-level fit hit at 0.4% is still only a fit — fire the no-free-parameter shot at new
    territory before promoting (v82).
14. When a predicted flight is absent, look for a static occupying the window (v82).
15. When a truncation fails, find the point where it is exact and read the breakdown outward — it
    localizes what crept in (v83).
16. Measure the discriminator (the slope probe) before fitting the model (v84).
17. Narrow-window multi-exponential fits are degenerate; the direct zero plus its β-flow is the
    robust extraction (v84).
18. Window-edge flip registrations and partner conflation are documented artifact classes — check
    both before interpreting multiplicities (v81/v82).

**Open after consolidation:** the background-zero derivation (why the saturated A vanishes where it
does); the unclassified L=6 ~1.8 object (audit catch D — likely conflated trajectories); the
root-derived parity-anchor channel; carried: channeling c, PH quasi-exactness, the exact π/β
constant.
