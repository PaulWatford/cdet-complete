"""sun_atom_record.py (v142) -- queue item #2 (SU(N)), step 1: the atom EoS and the N-polynomial record.

Kozik's 2024 CoS computes the SU(N) Hubbard equation of state (the N=6 173-Yb experiment) at a cost that is
INDEPENDENT of N: the diagram kernel is N-independent and the connectivity RECORD carries N as a polynomial
(each closed fermion/flavor loop contributes one factor of N). This module establishes that structure on the
exactly-solvable SU(N) atom -- the anchor for the lattice EoS to come.

THE SU(N) ATOM. Single site, N flavors, H = -mu sum_a n_a + U sum_{a<b} n_a n_b. The energy depends only on the
occupation k: E_k = -mu k + U k(k-1)/2, with degeneracy C(N,k). At U=0 the flavors are independent, so
k ~ Binomial(N, p), p = e^{beta mu}/(1+e^{beta mu}).

THE RECORD (verified here). The linked-cluster object ln Z(U) is the right place to see the N-structure (the
per-flavor density is a ratio and is NOT polynomial in N; ln Z is). Its U-series coefficients are
    c_j = kappa_j(Y) * (-beta)^j / j!,   Y_k = k(k-1)/2 (the interacting-pair count),
where kappa_j is the j-th cumulant of Y under the U=0 binomial. Because the factorial moments of a binomial are
polynomials in N, each c_j(N) is an EXACT polynomial in N of degree j+1. So: compute the N-independent cumulant
kernel once, then evaluate the polynomial at any flavor number N -- the CoS N-independence, on the atom.

VERIFIED: c_j(N) is a degree-(j+1) polynomial (fit on N=2..7 predicts N=8,9,10 to <=5e-9); the exact-cumulant
coefficients match an independent ED contour to 2e-11. OPEN (step 2): the lattice SU(N) connected determinant,
where the record is the closed-loop count of the actual diagrams (this reuses the v132 fast minors). ED/closed
form is the anchor only; frozen engine untouched (194/194)."""
import numpy as np
from math import comb, factorial

def binom_p(beta, mu):
    x = np.exp(beta * mu); return x / (1.0 + x)

def Y_moments(N, nmax, p):
    """Raw moments of the interacting-pair count Y=k(k-1)/2 under k~Binomial(N,p)."""
    pk = np.array([comb(N, k) * p ** k * (1 - p) ** (N - k) for k in range(N + 1)])
    Y = np.array([k * (k - 1) / 2.0 for k in range(N + 1)])
    return [float(np.sum(pk * Y ** m)) for m in range(nmax + 1)]

def cumulants(mom):
    n = len(mom) - 1; kap = [0.0] * (n + 1)
    for j in range(1, n + 1):
        kap[j] = mom[j] - sum(comb(j - 1, i - 1) * kap[i] * mom[j - i] for i in range(1, j))
    return kap

def lnZ_coeffs(N, nmax, beta, mu):
    """Exact U-series coefficients of ln Z for the SU(N) atom (via cumulants of the pair count)."""
    kap = cumulants(Y_moments(N, nmax, binom_p(beta, mu)))
    return [0.0] + [kap[j] * (-beta) ** j / factorial(j) for j in range(1, nmax + 1)]

def density_ed(N, mu, beta, U):
    """Per-flavor density of the SU(N) atom by exact diagonalization."""
    w = [comb(N, k) * np.exp(-beta * (-mu * k + U * k * (k - 1) / 2.0)) for k in range(N + 1)]
    Zt = sum(w); return sum(k * w[k] for k in range(N + 1)) / (N * Zt)

def _selftest():
    print("sun_atom_record self-test (#2 SU(N) step 1: atom EoS + N-polynomial record):")
    beta, mu, nmax = 2.0, 1.0, 4
    data = {N: lnZ_coeffs(N, nmax, beta, mu) for N in range(2, 11)}
    # (1) cross-check the exact-cumulant coeffs vs an independent ED contour (N=3)
    x = np.exp(beta * mu)
    def Z(N, U): return sum(comb(N, k) * x ** k * np.exp(-beta * U * k * (k - 1) / 2.0) for k in range(N + 1))
    th = 2 * np.pi * np.arange(1024) / 1024; r = 0.05
    Lc = np.array([np.log(Z(3, r * np.exp(1j * t))) for t in th])
    ed3 = [(np.sum(Lc * np.exp(-1j * j * th)) / (1024 * r ** j)).real for j in range(nmax + 1)]
    dev = max(abs(data[3][j] - ed3[j]) for j in range(1, nmax + 1))
    assert dev < 1e-8, dev
    print(f"  exact-cumulant ln Z coeffs vs ED contour (N=3): max dev {dev:.1e}")
    # (2) each c_j(N) is an exact degree-(j+1) polynomial in N (fit N=2..7, predict N=8,9,10)
    worst = 0.0
    for j in range(1, nmax + 1):
        Ns = np.arange(2, 8); ys = np.array([data[N][j] for N in Ns])
        co = np.polyfit(Ns, ys, j + 1)
        e = max(abs(np.polyval(co, M) - data[M][j]) for M in [8, 9, 10]); worst = max(worst, e)
    assert worst < 1e-6, worst
    print(f"  c_j(N) is a degree-(j+1) polynomial: N=2..7 predicts N=8,9,10 to {worst:.1e}")
    # (3) the EoS itself is exact for any N (e.g. N=6, the Yb case)
    n6 = density_ed(6, mu, beta, 1.0)
    assert 0 < n6 < 1, n6
    print(f"  SU(6) atom per-flavor density at U=1 (the Yb flavor number): {n6:.6f}")
    print("  => N-independent cumulant kernel -> evaluate at any N. The lattice connected-determinant")
    print("     record (reusing v132 fast minors) is step 2. PASS")

if __name__ == "__main__":
    _selftest()
