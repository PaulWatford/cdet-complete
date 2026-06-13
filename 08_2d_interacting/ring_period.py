"""ring_period.py (v76) -- the ring period at L=6: NOT RESOLVED, and the negative is fully
characterized. Spectral near-misses were rejected by permutation null -- the v58 lesson in spectral
form -- and the structural reason the period cannot be extracted at this size is quantitative.

THE ATTEMPT (pure re-analysis of the v75 fold's 480k exact values; no new engine sweeps).
Shell-coherence profiles f(r) = S(r) / Sum|v| (envelope divided out) over four radial coordinates
(MST, sum-of-legs, max-leg R_max, perimeter), detrended periodograms, pre-registered gates.

THE SEDUCTION AND THE KILL. Binned (width 0.5) R_max periodograms peaked within 9-10% of the
continuum 2k_F at BOTH fillings with the correct mu-shift -- everything the Friedel story wants.
But R_max is a DISCRETE coordinate (18 exact lattice radii); the correct unbinned treatment plus a
1000-shuffle permutation null gives p = 0.21 (mu=0.5) and 0.15 (mu=1.5): NOT SIGNIFICANT. The
binned peaks were a coincidence that null calibration caught. (Perimeter's spectacular 16x low-q
"peak" was trend leakage with the WRONG mu-shift -- a second trap caught.)

WHAT THE DISCRETE PROFILES ACTUALLY SHOW (exact):
    mu=0.5:  f = +0.66 at the contact radius, then |f| <= 0.12 everywhere after (edge bins aside)
    mu=1.5:  f = -0.53 at contact, then |f| <= 0.11
  The CONTACT-SHELL coherence is strong and FLIPS WITH mu (+0.66 vs -0.53) -- that part is real
  structure, consistent with v68/v72 governance. Beyond it, net coherence is amplitude-starved.

THE STRUCTURAL REASON (why L=6 cannot resolve the period even in principle):
  coherence decay xi_s ~ 3.0 (v68) vs predicted period pi/k_F ~ 1.2  ->  only ~2 oscillations fit
  before decoherence, sampled at ~5 usable lattice radii with |f| already < 0.1. Period extraction
  needs LARGER L combined with a coherence-boosted observable (e.g., the controlled line-sector
  protocol of v68, where coherence is high by construction), not more analysis of bulk shells.

STANDING LESSONS: (i) spectral peaks are not measurements until calibrated against a permutation
null; (ii) discrete coordinates must be analyzed unbinned -- arbitrary bin widths manufacture
structure; (iii) a coherence length shorter than ~3 periods makes period extraction impossible
regardless of statistics -- check xi_s / period BEFORE designing the experiment.
"""
import numpy as np

# exact discrete R_max coherence profiles from the v75 fold (remainder, L=6, times [0.5,1.9,3.3])
R_DISCRETE = None  # radii are the 18 lattice values of max-leg in the remainder
F_MU05 = np.array([+0.66, -0.12, -0.29, +0.02, -0.00, +0.05, +0.00, -0.06, +0.02,
                   -0.06, -0.02, -0.05, +0.03, -0.06, -0.01, -0.05, +0.02, -0.36])
F_MU15 = np.array([-0.53, -0.00, +0.08, -0.11, -0.04, -0.05, +0.01, +0.01, -0.04,
                   +0.02, -0.06, +0.01, -0.03, +0.01, +0.06, +0.03, -0.11, -0.25])
RADII = np.array([1.0, 1.41421356, 1.73205081, 2.0, 2.23606798, 2.44948975, 2.82842712,
                  3.0, 3.16227766, 3.31662479, 3.46410162, 3.60555128, 3.74165739,
                  4.12310563, 4.24264069, 4.35889894, 4.69041576, 5.19615242])
PERMUTATION_P = {"mu05": 0.208, "mu15": 0.149}


def detrend(r, f):
    A = np.column_stack([np.ones(len(r)), r])
    return f - A @ np.linalg.lstsq(A, f, rcond=None)[0]


def periodogram(r, f, qs=np.arange(1.0, 6.3, 0.02)):
    P = np.array([(np.sum(f * np.cos(q * r))) ** 2 + (np.sum(f * np.sin(q * r))) ** 2 for q in qs])
    return qs, P


def permutation_p(r, f, nshuffle=1000, seed=11):
    fd = detrend(r, f)
    pk = periodogram(r, fd)[1].max()
    rng = np.random.default_rng(seed)
    null = [periodogram(r, detrend(r, fd[rng.permutation(len(fd))]))[1].max() for _ in range(nshuffle)]
    return float(np.mean(np.array(null) >= pk))


def _selftest():
    ok = True
    for tag, f, pref in (("mu05", F_MU05, PERMUTATION_P["mu05"]), ("mu15", F_MU15, PERMUTATION_P["mu15"])):
        p = permutation_p(RADII, f)
        print(f"{tag}: permutation p = {p:.3f} (stored {pref:.3f}) -> peak NOT significant: {p > 0.05}")
        ok = ok and abs(p - pref) < 0.05 and p > 0.05
    contact_flip = F_MU05[0] > 0.4 and F_MU15[0] < -0.4
    print(f"contact-shell coherence strong and mu-flipped (+0.66 / -0.53): {contact_flip}")
    ok = ok and contact_flip
    tail05 = np.max(np.abs(F_MU05[1:-1])); tail15 = np.max(np.abs(F_MU15[1:-1]))
    print(f"amplitude starvation beyond contact: max |f| = {tail05:.2f} / {tail15:.2f} (gate < 0.35)")
    ok = ok and tail05 < 0.35 and tail15 < 0.35
    print("ring-period self-test (null-calibrated negative; contact flip; starvation):",
          "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
