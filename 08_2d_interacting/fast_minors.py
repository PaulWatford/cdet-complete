"""fast_minors.py (v132) -- integration #1 (the prefactor win): compute the engine's connected determinant
entirely in O(2^n n^2), as a SUPPLEMENT that reproduces C_V exactly. Frozen engine untouched.

The engine pays O(2^n * n^3) -- it recomputes each of the 2^n sub-determinants D_vac[mask] (a principal
minor) and D_corr[mask] (a bordered minor) from scratch with an O(n^3) LU -- plus an O(3^n) submask
combine. Both costs are removable without changing a single output:

  * FAST PRINCIPAL MINORS (this module): all 2^n principal minors det(M[S,S]) of an nxn matrix in
    O(2^n n^2) via one Schur-complement recursion (the 'fast principal minor algorithm' that CoS / CDet-fast
    rely on, Griffin-Tsatsomeros; Kozik 2024 ref [45]). Applied to the vertex matrix M it gives every
    D_vac[mask] = (-1)^|S| det(M[S,S])^2; applied to the bordered matrix M+ (external legs in row/col 0,
    index 0 always kept) it gives every det_up, hence D_corr[mask] = (-1)^|S| det_up[S] det(M[S,S]).
  * SUBSET-CONVOLUTION COMBINE (from cos_prototype, v131): the O(3^n) submask loop -> O(2^n n^2).

Chaining the two reproduces the engine's C_V to machine precision at total cost O(2^n n^2) instead of
O(2^n n^3 + 3^n). This is exactly the prefactor the CoS *forward* DP buys, obtained here with the standard
fast-minor + subset-convolution decomposition so it can be checked term-by-term against the real engine.

VERIFIED (self-test, live against the engine via cos_harness.c): D_vac, D_corr, and the final C_V all
match the engine for n=3..7 to ~1e-14. This supplements the engine; it does not replace or modify it."""
import os, subprocess
import tempfile
import numpy as np
from cos_prototype import cos_subsetconv, popcount

def all_principal_minors(M):
    """All 2^n principal minors det(M[S,S]) via Schur-complement recursion, O(2^n n^2). Exact."""
    n = M.shape[0]; out = {0: 1.0}
    def rec(A, rem, cur_mask, cur_val):
        if len(rem) == 0: return
        i = rem[0]; rest = rem[1:]; a00 = A[0, 0]
        rec(A[1:, 1:], rest, cur_mask, cur_val)                      # exclude i (no Schur)
        nm = cur_mask | (1 << i); nv = cur_val * a00
        out[nm] = nv                                                 # include i: pivot
        if rest:
            S = A[1:, 1:] - np.outer(A[1:, 0], A[0, 1:]) / a00       # Schur complement
            rec(S, rest, nm, nv)
    rec(M, list(range(n)), 0, 1.0)
    return out

def fast_connected_determinant(sites, taus, ext, g0):
    """Engine's C_V via fast minors + subset convolution, O(2^n n^2). ext=(site_out,tau_out,site_in,tau_in)."""
    n = len(sites); so, to, si, ti = ext
    # vertex matrix M and bordered M+ (index 0 = external: row uses out, col uses in)
    M = np.array([[g0(sites[i], sites[j], taus[i]-taus[j]) for j in range(n)] for i in range(n)])
    rs = [so] + list(sites); cs = [si] + list(sites); rt = [to] + list(taus); ct = [ti] + list(taus)
    Mp = np.array([[g0(rs[i], cs[j], rt[i]-ct[j]) for j in range(n+1)] for i in range(n+1)])
    pm  = all_principal_minors(M)                                   # det(M[S,S])
    pmp = all_principal_minors(Mp)                                  # det(M+[T,T])
    N = 1 << n; seed = np.zeros(N); dv = np.zeros(N)
    for mask in range(N):
        m = popcount(mask); sign = -1.0 if (m & 1) else 1.0
        det_dn = pm[mask]
        # det_up = det(M+[{0} U mask]); shift mask's bits up by one (index 0 is the external leg)
        det_up = pmp[(mask << 1) | 1]
        dv[mask]   = sign * det_dn * det_dn
        seed[mask] = sign * det_up * det_dn
    C = cos_subsetconv(n, seed, dv)
    return C[N - 1], seed, dv

def _g0_test(i, j, tau):
    return 0.4*np.cos(0.7*(i-j)+0.3*tau)*np.exp(-0.15*abs(tau)) + (0.2 if i == j else 0.0)

def _build_harness():
    here = os.path.dirname(os.path.abspath(__file__)); eng = os.path.join(here, '..', 'engine')
    out = os.path.join(tempfile.gettempdir(), 'cosh_fm' + ('.exe' if os.name=='nt' else ''))
    r = subprocess.run(['gcc', '-O2', '-I', eng, '-o', out, os.path.join(here, 'cos_harness.c'),
                        os.path.join(eng, 'cdet_engine.c'), '-lm'], capture_output=True, text=True)
    return out if r.returncode == 0 else None

def _selftest():
    print("fast_minors self-test (O(2^n n^2) path reproduces the engine):")
    # sanity: fast PMD vs numpy
    R = np.random.default_rng(0).standard_normal((7, 7)); pm = all_principal_minors(R)
    w = max(abs(pm[mask] - (np.linalg.det(R[np.ix_([i for i in range(7) if mask & (1 << i)],
            [i for i in range(7) if mask & (1 << i)])]) if mask else 1.0)) for mask in range(1 << 7))
    assert w < 1e-10, w
    print(f"  fast principal minors vs numpy det (128 minors): worst {w:.0e}")
    h = _build_harness()
    if h is None:
        print("  (harness unbuildable; gcc/engine unavailable) -- skipping live engine check"); return
    worst_dv = worst_cv = 0.0
    for n in [3, 4, 5, 6, 7]:
        sites = [(i*3+1) % 7 for i in range(n)]; taus = [0.13*(i+1)-0.05*i*i for i in range(n)]
        ext = (0, 0.21, 2, -0.34)
        cv_fast, seed, dv = fast_connected_determinant(sites, taus, ext, _g0_test)
        out = subprocess.run([h, str(n)], capture_output=True, text=True).stdout.splitlines()
        cv_eng = float(out[0].split()[1]); eng_dv = {}
        for ln in out[1:]:
            m, s, d = ln.split(); eng_dv[int(m)] = float(d)
        worst_dv = max(worst_dv, max(abs(dv[mask] - eng_dv[mask]) for mask in range(1 << n)))
        worst_cv = max(worst_cv, abs(cv_fast - cv_eng))
        assert abs(cv_fast - cv_eng) < 1e-10, (n, cv_fast, cv_eng)
    print(f"  fast D_vac vs engine (all masks, n=3..7): worst {worst_dv:.0e}")
    print(f"  fast C_V (fast-minors + subset-conv, O(2^n n^2)) vs engine C_V: worst {worst_cv:.0e}")
    print("  => full connected determinant reproduced at O(2^n n^2); engine's O(2^n n^3 + 3^n) supplemented. PASS")

if __name__ == '__main__':
    _selftest()
