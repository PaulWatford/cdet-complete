"""cdet_best.py (v65) -- THE CONSOLIDATED BASELINE: every verified tool from v49-v64 composed into
one default evaluation path, with exactness gates. The frozen C engine stays untouched (194/194);
everything here wraps it through the validated chain cdet_port.CDet -> FastCDet (4.2e-17).

THE COMPOSED STACK (each factor measured and banked in its own version):
    FastCDet            vectorized propagator         ~40x wall-clock      (v57, validated 4.2e-17)
  x orbit fold          Burnside-exact, little group  2x / 8x / 48x        (v50-52, exact 5e-15)
  x subset cache        D_vac/D_corr keyed on subset  ~5-7x fewer dets     (v53, exact 5e-15)
  x stratification      enumerate heavy low-d slices  2x-44x variance      (v55, unbiased)
  + shifted reference   alpha = U/2 at half filling   series QUASI-EXACT   (v45/56/64; split law below)
  + complex-mu contour  all derivatives in one pass                        (v47)
  + control variate     free-baseline subtraction     prefactor            (v33/49)

THE TWO LAWS THE BASELINE NOW ENCODES:
  SHIFT LAW (v56 + v64 split): at half filling the convergence-optimal shift is alpha*=U/2 -- the
    particle-hole point -- universally (2 clusters x 3 couplings) and quasi-exactly. Whether that
    point ALSO has good sign is CLUSTER-DEPENDENT (yes on the 2x2, no on the 6-ring): measure the
    cluster's sign landscape (genericity_search.r2_profile) before assuming. Doped: the optima
    compete; choose per goal.
  CONCENTRATION LAW (v57-63, locked 1.27x): per-configuration weight ~ exp(-b*MST + c*l_coll) with
    b=0.537, c=+0.583 (L=6 cube reference values; measured, not derived), modulated by
    tau-interference (40% of var ln|C|). Use it to design stratifications and importance sampling.

STANDING METHODOLOGY (each rule earned by a banked failure):
  1. PAIR every comparison in heavy-tailed systems -- same sites, same tau draws (v61).
  2. Ratios of means over heavy tails are not measurements until the estimator is shown stable;
     gate on robust statistics (median, sign-fraction) (v58).
  3. Wrap-safe fits only -- stay short of the torus antipode (v60).
  4. Freeze-then-predict for every theory claim; a pre-set gate decides (v59-63).
  5. Stratify mixtures before regressing across them (v59).
  6. When regressors coincide on a subpopulation, identify each coefficient where the other cannot
     contaminate it (v63).
  7. A failing self-test gate is data (v56, v58, v62->63).
"""
import numpy as np
from slice_scaling import FastCDet
from symmetry_reduction import (square_point_stabilizer, cube_point_stabilizer, cube_hopping,
                                fold_site_sum_cached, cv_cached)
from slice_stratified import classify_strata, stratified_site_sum

BestCDet = FastCDet  # the validated fast evaluator IS the baseline evaluator


def auto_group(hop, lattice):
    """Point-group stabilizer of the external site for the supported lattices.
    lattice = ('square', W, H) or ('cube', L)."""
    if lattice[0] == 'square':
        return square_point_stabilizer(lattice[1], lattice[2], hop)
    if lattice[0] == 'cube':
        return cube_point_stabilizer(lattice[1], hop)
    raise ValueError("supported: ('square', W, H) or ('cube', L)")


def best_site_sum(cdet, times, mu, group):
    """The default EXACT site sum: orbit fold x subset cache (v50-53). Returns
    (total, unique_determinants, brute_subset_evals)."""
    return fold_site_sum_cached(cdet, times, group, mu)


def best_site_sum_sampled(cdet, Lc, times, mu, budget, seed=0):
    """The default UNBIASED estimator for big cubes: slice stratification (v55).
    Enumerates heavy low-dimensional strata, Neyman-samples the bulk."""
    strata = classify_strata(Lc ** 3, Lc, len(times))
    rng = np.random.default_rng(seed)
    return stratified_site_sum(cdet, times, mu, strata, budget, rng)


def recommended_shift(U, density_per_site=None, at_half_filling=False):
    """The shift law as the record now states it (v45/56/64).
    Returns (alpha, note). The sign caveat is part of the return value on purpose."""
    if at_half_filling:
        return U / 2.0, ("alpha=U/2 (particle-hole point): convergence-optimal universally and "
                         "quasi-exactly (v64). SIGN at this reference is CLUSTER-DEPENDENT -- "
                         "measure the landscape (genericity_search.r2_profile) before assuming "
                         "alignment (true on the 2x2, false on the 6-ring).")
    if density_per_site is None:
        raise ValueError("doped case needs density_per_site (use shifted_expansion.density)")
    return U * density_per_site / 2.0, ("Hartree-scale shift for convergence. WARNING (v56): in the "
                                        "doped regime convergence and sign optima COMPETE -- this "
                                        "shift typically lands ~a shell spacing from the sign peak.")


# reference constants of the concentration law (L=6 cube, beta=4, mu=0.5; v63, measured not derived)
CONCENTRATION_LAW = {"b_distance": 0.537, "c_channeling": 0.583,
                     "tau_interference_share": 0.40, "lockdown_agreement": 1.27}


def _selftest():
    import sys; sys.path.insert(0, '.')
    from cdet_port import CDet
    from hubbard_ed import hop_2d_square
    import itertools, time
    ok = True
    # gate 1: BestCDet identical to the frozen-port-validated CDet
    H = cube_hopping(4); a = CDet(H, beta=4.0, to=0.7, ti=0.2); b = BestCDet(H, beta=4.0, to=0.7, ti=0.2)
    rng = np.random.default_rng(0); worst = 0.0
    for _ in range(30):
        n = int(rng.integers(1, 4)); V = [(int(rng.integers(64)), float(rng.uniform(0, 4))) for _ in range(n)]
        worst = max(worst, abs(a.C_V(V, 0.5) - b.C_V(V, 0.5)))
    print(f"gate 1  BestCDet == validated CDet: max diff {worst:.1e}")
    ok = ok and worst < 1e-12
    # gate 2: exact composed sum on the 4x4 square (n=2)
    H4 = hop_2d_square(4, 4, 1.0); cd4 = BestCDet(H4, beta=4.0, to=0.7, ti=0.2)
    times = [0.9, 2.7]
    brute = sum(cd4.C_V([(s, t) for s, t in zip(st, times)], 0.5).real
                for st in itertools.product(range(16), repeat=2))
    tot, nuniq, nbrute = best_site_sum(cd4, times, 0.5, auto_group(H4, ('square', 4, 4)))
    print(f"gate 2  4x4 square n=2: fold+cache {tot:+.8f} vs brute {brute:+.8f}  "
          f"match {abs(tot - brute):.1e}  ({nbrute // 2} subset evals -> {nuniq} determinants)")
    ok = ok and abs(tot - brute) < 1e-12
    # gate 3: exact composed sum on the 4^3 cube (n=2), with wall-clock
    cdc = BestCDet(cube_hopping(4), beta=4.0, to=0.7, ti=0.2)
    t0 = time.time()
    bruteC = sum(cdc.C_V([(s, t) for s, t in zip(st, times)], 0.5).real
                 for st in itertools.product(range(64), repeat=2)); t1 = time.time()
    totC, nuC, nbC = best_site_sum(cdc, times, 0.5, auto_group(cube_hopping(4), ('cube', 4))); t2 = time.time()
    print(f"gate 3  4^3 cube n=2: match {abs(totC - bruteC):.1e}   brute {t1 - t0:.1f}s -> composed "
          f"{t2 - t1:.1f}s ({(t1 - t0) / max(t2 - t1, 1e-9):.0f}x)   determinants {nbC // 2} -> {nuC}")
    ok = ok and abs(totC - bruteC) < 1e-12
    # gate 4: the shift law's logic
    al, note = recommended_shift(4.0, at_half_filling=True)
    print(f"gate 4  recommended_shift(U=4, half filling) = {al} (expect 2.0); caveat present: "
          f"{'CLUSTER-DEPENDENT' in note}")
    ok = ok and al == 2.0 and 'CLUSTER-DEPENDENT' in note
    print("consolidated-baseline self-test:", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
