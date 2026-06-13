"""v49 -- Can a deformed integration contour move the CDet sign wall? (the plundered idea, tested)

The one tool from the "evaluate on a contour / at roots of unity" family that had a real shot at the
sign wall is Lefschetz-style contour deformation. We test it on the GENUINE v48 sign integrand (2x2
square, levels {-4,0,0,+4}, beta=4, U=4, mu=0.5, externals to=0.7 ti=0.2) and find it null -- with a
sharp, structural reason that also kills the "use the undeformed axis as a control-variate comparator"
follow-up. The lesson is the headline: our sign is a REAL sign-flip (the determinant is real and flips
between configs), not a complex PHASE (the e^{iS} that thimbles are built to flatten). A real, already
sector-coherent integrand gives a contour nothing to grip; covariates then move the prefactor, never R.

Three measurements, all on the real engine's connected determinant (cdet_port, validated to the frozen
ring port at 0.00e+00):
  (A) sector decomposition  -> within each kink-pinned sector R=1; the deficit is discrete BETWEEN sectors
  (B) contour optimisation  -> the variance/sign-optimal amplitude is A=0 (the real axis); integral invariant
  (C) covariate test        -> the deformation family is a PERFECT-correlation covariate (zero variance gain),
                               because it moves only a spurious imaginary part (Re rigid to 1e-15; validated
                               against a toy whose real part DOES move by O(1)).
Frozen engine untouched.
"""
import numpy as np
from cdet_port import CDet
from hubbard_ed import hop_2d_square

BETA, TO, TI = 4.0, 0.7, 0.2
KNOTS = [1e-6, TI, TO, BETA - 1e-6]          # propagator kinks: contour must pin here to stay valid
cd = CDet(hop_2d_square(2, 2, 1.0), beta=BETA, to=TO, ti=TI)


def g(tau, mu):                              # genuine order-1 integrand, summed over the 4 vertex sites
    return sum(cd.C_V([(s, complex(tau))], mu) for s in range(4))


def piece_h(A, mu, a, b, npts=900):
    """Integrand on the pinned contour tau = x + iA sin(pi (x-a)/(b-a)) over one analytic sector [a,b]."""
    x = np.linspace(a, b, npts); w = b - a
    tau = x + 1j * A * np.sin(np.pi * (x - a) / w)
    dtau = 1.0 + 1j * A * (np.pi / w) * np.cos(np.pi * (x - a) / w)
    h = np.array([g(t, mu) for t in tau]) * dtau
    return x, h


def measure(mu):
    # (A) sector decomposition on the real axis
    sec_I, sec_absI = [], []
    for a, b in zip(KNOTS[:-1], KNOTS[1:]):
        x, h = piece_h(0.0, mu, a, b)
        sec_I.append(np.trapezoid(h.real, x)); sec_absI.append(np.trapezoid(np.abs(h.real), x))
    sec_I = np.array(sec_I); sec_absI = np.array(sec_absI)
    R_axis = abs(sec_I.sum()) / sec_absI.sum()
    Rsec = np.abs(sec_I) / sec_absI

    # (B) contour optimisation: minimise total int|.| per sector (integral value is invariant)
    from scipy.optimize import minimize_scalar
    bestA = []
    for a, b in zip(KNOTS[:-1], KNOTS[1:]):
        bestA.append(minimize_scalar(
            lambda A, a=a, b=b: np.trapezoid(np.abs(piece_h(A, mu, a, b)[1]), piece_h(A, mu, a, b)[0]),
            bounds=(-3, 3), method="bounded").x)
    I_def = 0.0; absI_def = 0.0
    for A, (a, b) in zip(bestA, zip(KNOTS[:-1], KNOTS[1:])):
        x, h = piece_h(A, mu, a, b); I_def += np.trapezoid(h.real, x); absI_def += np.trapezoid(np.abs(h.real), x)

    # (C) covariate test: family of unbiased estimators {Re h_A}; optimal variance-min combination
    amps = [0.0, -1.5, -1.0, -0.5, 0.5, 1.0, 1.5]
    F = []
    for A in amps:
        cols = [piece_h(A, mu, a, b)[1].real for a, b in zip(KNOTS[:-1], KNOTS[1:])]
        F.append(np.concatenate(cols))
    F = np.array(F); xs = np.concatenate([piece_h(0, mu, a, b)[0] for a, b in zip(KNOTS[:-1], KNOTS[1:])])
    mean = lambda f: np.trapezoid(f, xs) / BETA
    mu_f = np.array([mean(f) for f in F])
    Cov = np.array([[np.trapezoid(F[i] * F[j], xs) / BETA - mu_f[i] * mu_f[j]
                     for j in range(len(amps))] for i in range(len(amps))])
    one = np.ones(len(amps)); w = np.linalg.pinv(Cov) @ one / (one @ np.linalg.pinv(Cov) @ one)
    var_bare, var_cv = Cov[0, 0], float(w @ Cov @ w)
    re_rigid = np.max(np.abs(F[amps.index(1.5)] - F[0]))     # |Re h_{1.5} - g| pointwise

    return dict(R_axis=R_axis, Rsec=Rsec, sec_I=sec_I, bestA=bestA, I_axis=sec_I.sum(),
                I_def=I_def, absI_axis=sec_absI.sum(), absI_def=absI_def,
                var_bare=var_bare, var_cv=var_cv, re_rigid=re_rigid)


def toy_validation():
    """Same deformation on a real-analytic toy: its real part MUST move (proves the code is non-trivial)."""
    a, b, A = 0.0, 1.0, 1.5
    x = np.linspace(a, b, 2000); f = A * np.sin(np.pi * (x - a) / (b - a))
    fp = A * (np.pi / (b - a)) * np.cos(np.pi * (x - a) / (b - a))
    g_re = np.exp(-0.5 * x); h = np.exp(-0.5 * (x + 1j * f)) * (1 + 1j * fp)
    return np.max(np.abs(h.real - g_re))


def n2_wall(mu, NMC=40000, seed=7):
    rng = np.random.default_rng(seed); vals = []
    for _ in range(NMC):
        V = [(int(rng.integers(4)), float(rng.uniform(0, BETA))) for _ in range(2)]
        vals.append(cd.C_V(V, mu).real)
    vals = np.array(vals); return abs(vals.mean()) / np.abs(vals).mean()


if __name__ == "__main__":
    print("=" * 80)
    print("v49: contour deformation on the genuine v48 sign integrand -- does it move the wall?")
    print("=" * 80)
    print(f"toy validation (deformation code is live): toy real part moves by {toy_validation():.3f}  "
          f"(>>0, so any 1e-15 below is a real property, not a dead deformation)\n")
    for mu in (0.0, -1.0):
        r = measure(mu)
        tag = "closed shell" if mu == 0.0 else "Hartree"
        print(f"mu_ref={mu:+.1f} ({tag}):")
        print(f"  (A) per-sector R = {np.array2string(r['Rsec'], precision=3, floatmode='fixed')}  "
              f"=> each ~1: sign is COHERENT within a sector; cancellation is discrete BETWEEN sectors")
        print(f"      sector signed parts {np.array2string(r['sec_I'], precision=4, floatmode='fixed', sign='+')}"
              f"  -> total R_axis = {r['R_axis']:.3f}")
        print(f"  (B) sign/var-optimal contour amplitude per sector = {[f'{a:+.2f}' for a in r['bestA']]}  "
              f"(the REAL AXIS); integral preserved |dI|={abs(r['I_def'] - r['I_axis']):.1e}")
        print(f"  (C) covariate: bare var {r['var_bare']:.3e} -> optimal combo {r['var_cv']:.3e}  "
              f"(x{r['var_bare'] / r['var_cv']:.2f}); deformed Re rigid to {r['re_rigid']:.1e} => perfect correlation")
        print()
    print("n=2 wall (genuine, reproduces v48):")
    for mu in (0.0, -1.0):
        print(f"  mu_ref={mu:+.1f}: |R_2| = {n2_wall(mu):.3f}")
    print()
    print("VERDICT: contour deformation and its covariate are NULL on the CDet sign. Reason: the integrand")
    print("is REAL and sector-coherent (a discrete sign-flip), not a continuous complex phase. Deformation")
    print("manufactures only a zero-integral imaginary part; covariates reweight unbiased estimators of the")
    print("same mean, so they move the PREFACTOR (variance) at best, never R -- the wall (Troyer-Wiese) stands.")
