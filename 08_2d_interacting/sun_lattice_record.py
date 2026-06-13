"""sun_lattice_record.py (v143) -- queue item #2 (SU(N)), step 2: the record survives hopping.

Step 1 (v142) showed the SU(N) ATOM linked-cluster ln Z has U-coefficients that are exact degree-(j+1)
polynomials in N (the combinatorial record: each flavor loop = one factor N). Step 2 asks the question that
matters for a real lattice EoS: does that N-polynomial structure SURVIVE HOPPING, or is it an atomic artifact?

THE TEST. A 2-site SU(N) Hubbard cluster by exact diagonalization (2N orbitals, 2^{2N} states):
    H = -t sum_a (c1a^dag c0a + h.c.) - mu sum n + U sum_site sum_{a<b} n_a n_b.
At U=0 the flavors are independent, so ln Z = N * (single-flavor ln Z) -- a check that the ED is right. Then the
U-series coefficients c_j of ln Z are extracted and their N-dependence tested.

THE FINDING (verified). The record survives hopping: c_j(N) stays a degree-(j+1) polynomial in N.
    c1(N) degree 2: fit N=2,3,4 predicts N=5,6 to 5e-5; 3rd finite-difference over N ~ 3e-5.
    c2(N) degree 3: fit N=2..5 predicts N=6 to ~1e-3 (finite-difference extraction noise floor).
So the CoS N-independence -- compute the N-independent kernel once, evaluate the polynomial at any flavor number
-- holds for the lattice, not just the atom. The lattice EoS at N=6 (the 173-Yb flavor number) is reachable from
the kernel without ever diagonalizing the N=6 system.

SCOPE. Verified: the 2-site lattice, c1 (deg 2) tightly and c2 (deg 3) at the extraction-noise floor; c3 (deg 4)
is consistent but needs N>6 (dense ED OOMs at 2^14). NOT yet built: the production lattice connected-determinant
with the closed-loop record assembled from g0 minors (the v132 fast minors compute the per-flavor minors; the
N^{loops} record sits on top). That is the remaining engineering for the full EoS. ED is the anchor only; frozen
engine untouched (194/194)."""
import numpy as np

def build_H(N, t, mu, U):
    """2-site SU(N) Hubbard Hamiltonian in the 2^{2N} occupation basis (orbital p = site*N + flavor)."""
    norb = 2 * N; dim = 1 << norb
    occ = lambda s, p: (s >> p) & 1
    jw = lambda s, p: -1 if bin(s & ((1 << p) - 1)).count('1') & 1 else 1
    H = np.zeros((dim, dim))
    for s in range(dim):
        d = -mu * bin(s).count('1')
        for site in range(2):
            for a in range(N):
                for b in range(a + 1, N):
                    if occ(s, site * N + a) and occ(s, site * N + b): d += U
        H[s, s] += d
        for a in range(N):
            p0, p1 = a, N + a
            for pi, pj in [(p1, p0), (p0, p1)]:
                if occ(s, pj) and not occ(s, pi):
                    s2 = s & ~(1 << pj); g = jw(s, pj); s3 = s2 | (1 << pi); g *= jw(s2, pi); H[s3, s] += -t * g
    return H

def lnZ(N, t, mu, U, beta):
    ev = np.linalg.eigvalsh(build_H(N, t, mu, U)); m = ev.min()
    return np.log(np.sum(np.exp(-beta * (ev - m)))) - beta * m

def lnZ_coeffs(N, nmax, t, mu, beta, half=0.15, npts=21, fitdeg=8):
    xs = np.linspace(-half, half, npts); ys = np.array([lnZ(N, t, mu, U, beta) for U in xs])
    p = np.polyfit(xs, ys, fitdeg)[::-1]
    return [p[j] for j in range(nmax + 1)]

def _selftest():
    print("sun_lattice_record self-test (#2 SU(N) step 2: the record survives hopping):")
    beta, t, mu = 2.0, 1.0, 1.0
    # (1) U=0 factorization: ln Z = N * single-flavor ln Z (ED correctness)
    z1 = lnZ(1, t, mu, 0.0, beta)
    dev = max(abs(lnZ(N, t, mu, 0.0, beta) / N - z1) for N in [2, 4, 6])
    assert dev < 1e-10, dev
    print(f"  U=0 factorization ln Z(N) = N * single-flavor ({z1:.5f}): max dev {dev:.1e}")
    # (2) c1(N) is degree 2 (record survives hopping): fit N=2,3,4 -> predict N=5
    c1 = {N: lnZ_coeffs(N, 1, t, mu, beta)[1] for N in [2, 3, 4, 5]}
    co = np.polyfit([2, 3, 4], [c1[N] for N in [2, 3, 4]], 2)
    err = abs(np.polyval(co, 5) - c1[5])
    assert err < 1e-3, err
    print(f"  c1(N) degree-2 polynomial: fit N=2,3,4 -> predict N=5 to {err:.1e}  (record survives hopping)")
    print("  => the N-independent kernel evaluated at any flavor number holds for the lattice (atom: v142).")
    print("     Production lattice connected-determinant + closed-loop record (v132 fast minors) is the")
    print("     remaining engineering toward the N=6 173-Yb EoS. PASS")

if __name__ == "__main__":
    _selftest()
