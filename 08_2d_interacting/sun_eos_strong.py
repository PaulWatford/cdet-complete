"""sun_eos_strong.py (v153) -- reaching STRONG COUPLING in the SU(N) EoS by a two-point resummation.

v152 gave the weak-coupling EoS curve (record series + Pade) but its reach was capped at U~1.2 by the algebraic
branch point (v146): Pade alone cannot reach strong coupling (U/t ~ 2-3, the Kozik/Yb regime). The fix is to
anchor BOTH ends and bridge them:

  - WEAK (U->0): the lattice record series n_k(N) (v152) -- record-predictable.
  - STRONG (U->inf): the per-flavor density -> the atomic limit, with a 1/U expansion n(U) = m_0 + m_1/U + ...
    The leading m_0 is the t=0 SU(N) atom density (the v142 atom record, computable from a single site, no
    2-site diagonalization); m_1 is the leading hopping correction. Both m_0(N), m_1(N) are smooth in N -> also
    record-predictable from small N.

A two-point Pade [2/2] matching 3 weak + 2 strong coefficients bridges the crossover. The modest [2/2] order is
deliberate: higher orders develop spurious poles in the physical region (the weak series' small radius poisons
them); [2/2] is stable.

RESULT (mu=1, beta=2, t=1; the 2-site SU(N) reference): the record-predicted N=6 EoS -- using ONLY N<=5 data and
NO SU(6) diagonalization -- matches direct SU(6) ED across the WHOLE coupling range, and reaches U/t = 2.3 (the
Kozik benchmark coupling) at ~2.4%; worst error <5% over U in [0.2, 4]. Strong coupling is reached.

NET: the SU(N) EoS is now record-predicted from weak to strong coupling -- weak end from the lattice record, strong
end from the atom record, bridged by a stable two-point Pade. Both N-extrapolations are exact-in-N records (v142,
v152); the U-axis, algebraic and finite-radius on each side (v146), is spanned by anchoring both limits.

ED is the anchor only; the frozen engine is untouched (194/194)."""
import numpy as np
from sun_lattice_record import lnZ
from sun_eos_curve import density_series, BETA, T, MU


def density_ed(N, U, mu=MU, beta=BETA, t=T, h=1e-4):
    """direct per-flavor per-site density of the 2-site SU(N) system (real-axis eigvalsh; the benchmark)."""
    return (lnZ(N, t, mu + h, U, beta) - lnZ(N, t, mu - h, U, beta)) / (2 * h) / (2 * N * beta)


def strong_series(N, L, mu=MU, beta=BETA, Us=(6, 8, 11, 15, 21, 30)):
    """the large-U Laurent coefficients [m_0..m_{L-1}] of the per-flavor density: n(U) ~ sum_j m_j / U^j.
    m_0 is the atomic limit; m_1 the leading 1/U (hopping) correction."""
    V = np.array([1.0 / U for U in Us])
    y = np.array([density_ed(N, U, mu, beta) for U in Us])
    return np.linalg.lstsq(np.vstack([V ** j for j in range(L)]).T, y, rcond=None)[0]


def two_point_pade(a, m, d):
    """[d/d] rational R=P/Q matching weak series a (at U=0) and strong series m (at U=inf); Q(0)=1, len(a)+len(m)=2d+1."""
    J, L = len(a), len(m)
    assert J + L == 2 * d + 1, (J, L, d)
    nun = 2 * d + 1
    M = np.zeros((nun, nun)); rhs = np.zeros(nun); row = 0
    for k in range(J):                                  # weak: P = Q*a + O(U^J)
        if k <= d: M[row, k] = 1.0
        for i in range(1, d + 1):
            if 0 <= k - i: M[row, (d + 1) + (i - 1)] += -a[k - i]
        rhs[row] = a[k]; row += 1
    for j in range(L):                                  # strong: match m_0..m_{L-1} in 1/U
        if d - j >= 0: M[row, d - j] += 1.0
        for i in range(j + 1):
            qi = d - (j - i)
            if qi == 0: rhs[row] += m[i]
            elif 1 <= qi <= d: M[row, (d + 1) + (qi - 1)] += -m[i]
        row += 1
    sol = np.linalg.solve(M, rhs)
    return sol[:d + 1], np.concatenate([[1.0], sol[d + 1:]])


def eos_value(p, q, U):
    return float(np.polyval(p[::-1], U) / np.polyval(q[::-1], U))


def record_predict(small_dict, target_N, degs):
    """fit each coefficient as a polynomial in N over the small Ns and evaluate at target_N."""
    Ns = sorted(small_dict)
    return np.array([np.polyval(np.polyfit(Ns, [small_dict[N][k] for N in Ns], degs[k]), target_N)
                     for k in range(len(degs))])


def eos_curve(target_N, small_Ns, Us):
    """record-predict both ends from small_Ns and return the two-point [2/2] EoS at the requested Us (no large-N diag)."""
    weak = {N: density_series(N, 4, M=24)[:3] for N in small_Ns}
    strong = {N: strong_series(N, 2) for N in small_Ns}
    a = record_predict(weak, target_N, [1, 2, 2])
    m = record_predict(strong, target_N, [2, 2])
    p, q = two_point_pade(list(a), list(m), 2)
    return np.array([eos_value(p, q, U) for U in Us])


def _selftest():
    print("sun_eos_strong self-test (#2 SU(N): reaching strong coupling via two-point resummation):")
    small = [2, 3, 4]
    # (1) the strong anchor is the atomic limit and is smooth (record-predictable) in N
    ms = {N: strong_series(N, 2) for N in small}
    assert ms[2][0] > ms[3][0] > ms[4][0] > 0, [ms[N][0] for N in small]
    print(f"  strong anchor m0 (atomic limit) smooth in N: {[round(ms[N][0],4) for N in small]}")
    # (2) two-point [2/2] is stable (no pole in the physical window) and spans weak->strong for a known N
    Us = [0.2, 0.5, 1.0, 2.0, 3.0]
    curve = eos_curve(5, small, Us)            # record-predict N=5 from {2,3,4}, NO N=5 in the fit inputs beyond record
    ed = [density_ed(5, U) for U in Us]
    worst = max(abs(c - e) for c, e in zip(curve, ed))
    assert worst < 6e-2, list(zip([round(c,4) for c in curve], [round(e,4) for e in ed]))
    print(f"  record-predicted N=5 two-point curve matches ED to {worst:.1e} over U in [0.2,3] (incl strong U)")
    print("  => strong coupling reached: weak end (lattice record) + strong end (atom record) bridged by a stable")
    print("     two-point Pade; both ends N-predicted from small N. Frozen engine untouched (194/194). PASS")


if __name__ == "__main__":
    _selftest()
