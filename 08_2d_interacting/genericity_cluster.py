"""Genericity beyond the 2x2 (v64): the v56 law SPLITS under larger-cluster + second-U testing.

THE TEST. v56 (one cluster, one U) said: sign and convergence optima separate in the doped regime
and align exactly only at half filling. Extended along both axes:

AXIS 1 -- SECOND/THIRD COUPLING (2x2, beta=8, U = 2 and 8, alongside v56's U=4):
    U=2: half filling mu=1.0 -> alpha*=1.0=U/2 -> mu_ref=0.0 = sign peak (R=0.91): ALIGNED.
         doped mu=0.25, 0.0 -> mu_ref=-0.75, -1.0 (R=0.13): separated.
    U=8: half filling mu=4.0 -> alpha*=4.0=U/2 -> mu_ref=0.0: ALIGNED.
         doped mu=1.0, 0.0 -> mu_ref=-2.0 (R~0.14): separated.
    The mechanism tracks the coupling EXACTLY: alpha* = U/2 at mu = U/2 at all three U.

AXIS 2 -- LARGER CLUSTER (6-site ring, U=2, beta=8; made feasible by BLOCKED SECTOR ED:
    (N_up, N_dn) conservation splits the 4096-dim Fock space into 49 sectors of <=400 -- validated
    against a full dense-eig reference G = -0.246331 to 4.8e-07, and ~150x faster, 0.8 s/eval):
    Half filling mu=U/2=1.0: alpha sweep gives err@K8 = 1.0e0 / 4.2e-1 / 8.6e-6 / 5.8e-1 / 1.5e0 at
    alpha = 0 / 0.5 / 1.0 / 1.5 / 2.0. The PH shift alpha*=U/2 wins by FIVE ORDERS OF MAGNITUDE --
    the error at the PH point sits at the extraction floor: the shifted series is essentially exact.
    BUT the 6-ring's measured sign landscape (v56, U-independent) peaks at mu_ref=-1.0 (R=0.51)
    while R(0)=0.14: at the convergence-optimal reference the sign is poor. SIGN ALIGNMENT FAILS AT
    HALF FILLING on this cluster -- exactly as predicted before the run from the v56 landscape.

THE REFINED LAW (the v56 statement, corrected by its own larger-cluster test):
    (i) UNIVERSAL: at half filling the convergence-optimal shift is alpha* = U/2 -- the particle-hole
        point -- confirmed at 2 clusters x 3 couplings, with the PH-symmetric reference making the
        series quasi-exact (a stronger statement than v56 made).
    (ii) CLUSTER-DEPENDENT: whether the PH point is ALSO the sign optimum depends on whether the
        cluster's sign landscape peaks there. True on the 2x2; FALSE on the 6-ring. "Sign and
        convergence align at half filling" was a 2x2 coincidence of two different special points.

Honest scope: 6-ring tested at half filling only (49 s per alpha; doped points untested there,
expected separated a fortiori); one beta; the 6-ring sign landscape is the v56 measurement.
"""
import numpy as np
from shifted_expansion import _build


def sectors(N):
    """Index lists of the (N_up, N_dn) sectors of the 2N-orbital Fock space."""
    dim = 1 << (2 * N); lab = {}
    for s in range(dim):
        nu = bin(s & ((1 << N) - 1)).count("1"); nd = bin(s >> N).count("1")
        lab.setdefault((nu, nd), []).append(s)
    return lab


def G_blocked(Hm, c0, c0d, beta, tau, lab):
    """G(tau) = -<T c0(tau) c0+(0)> by per-sector diagonalization (c0 maps (nu,nd)->(nu-1,nd)).
    Validated against the dense-eig reference on the 6-ring to 4.8e-07; ~150x faster."""
    eig = {}
    for k, ix in lab.items():
        sub = Hm[np.ix_(ix, ix)]
        w, VR = np.linalg.eig(sub)
        eig[k] = (np.array(ix), w, VR, np.linalg.inv(VR))
    allw = np.concatenate([eig[k][1] for k in eig])
    E0 = np.min(allw.real); Z = np.sum(np.exp(-beta * (allw - E0)))
    tot = 0.0 + 0j
    for k in eig:
        k2 = (k[0] - 1, k[1])
        if k2 not in eig:
            continue
        ixA, wA, VA, WiA = eig[k]; ixB, wB, VB, WiB = eig[k2]
        cAB = WiB @ c0[np.ix_(ixB, ixA)] @ VA
        cdBA = WiA @ c0d[np.ix_(ixA, ixB)] @ VB
        wt = np.exp(-beta * (wA - E0))
        ph = np.exp(tau * np.subtract.outer(wA, wB))
        tot += -np.sum(wt[:, None] * ph * (cAB.T * cdBA))
    return tot / Z


def shifted_coeffs_blocked(hop, mu, beta, tau, U, alpha, nmax=8, r=0.6, M=24, built=None, lab=None):
    """Shifted-expansion coefficients via the blocked Cauchy contour (drop-in for shifted_coeffs)."""
    H0, Nm, Hd, c0, c0d = built if built is not None else _build(hop, mu)
    if lab is None:
        lab = sectors(hop.shape[0])
    th = 2 * np.pi * np.arange(M) / M
    G = np.array([G_blocked(H0 + alpha * Nm + (r * np.exp(1j * t)) * (U * Hd - alpha * Nm),
                            c0, c0d, beta, tau, lab) for t in th])
    return np.array([np.sum(G * np.exp(-1j * n * th)) / (M * r ** n) for n in range(nmax + 1)])


DENSE_REFERENCE_6RING = -0.246331  # full dense-eig G(mu=1, beta=8, tau=0.5, U=2), 120 s run


def _selftest():
    import sys; sys.path.insert(0, '.')
    from hubbard_ed import hop_1d_ring, hop_2d_square
    from genericity_search import conv_optimal_shift
    H6 = hop_1d_ring(6, 1.0); beta, tau, U = 8.0, 0.5, 2.0
    built = _build(H6, 1.0); lab = sectors(6)
    g = G_blocked(built[0] + U * built[2], built[3], built[4], beta, tau, lab).real
    print(f"blocked vs dense reference: {g:.6f} vs {DENSE_REFERENCE_6RING}  diff {abs(g - DENSE_REFERENCE_6RING):.1e}")
    ok = abs(g - DENSE_REFERENCE_6RING) < 1e-5
    # 6-ring half filling: PH shift beats the unshifted series by orders of magnitude (reduced M)
    errs = {}
    for a in (0.0, 1.0):
        b = shifted_coeffs_blocked(H6, 1.0, beta, tau, U, a, nmax=6, M=12, built=built, lab=lab)
        errs[a] = abs(np.sum(b[:7]).real - g)
    print(f"6-ring half filling err@K6: alpha=0 -> {errs[0.0]:.2e}   alpha=U/2 -> {errs[1.0]:.2e}"
          f"   (ratio {errs[0.0] / errs[1.0]:.0e})")
    ok = ok and errs[1.0] < 1e-3 * errs[0.0]
    # 2x2 second-U alignment: U=2 half filling -> alpha* = 1.0
    a2, _ = conv_optimal_shift(hop_2d_square(2, 2, 1.0), 1.0, beta, tau, 2.0, np.arange(0.0, 2.01, 0.5))
    print(f"2x2 U=2 half filling: alpha* = {a2:.1f} (expect U/2 = 1.0)")
    ok = ok and abs(a2 - 1.0) < 0.26
    print("cluster-genericity self-test (blocked ED valid; PH shift quasi-exact on the 6-ring; "
          "U/2 alignment at second U):", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
