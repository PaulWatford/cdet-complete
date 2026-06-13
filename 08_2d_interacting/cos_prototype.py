"""cos_prototype.py (v131) -- a verified CoS-style reorganization of the engine's connected determinant,
and an honest assessment of what (from Kozik 2024 + Simkovic-Kozik 2019) is worth integrating.

CONTEXT. The engine's C_V (engine/cdet_engine.c) is the Rossi connected determinant: it fills C[mask] for
all 2^n subsets of the n interaction vertices, and combines them with an O(3^n) submask loop
(value -= C[sm]*D_vac[mask^sm]). The Kozik 2024 "combinatorial summation" (CoS) reorganizes the SAME sum
as a forward dynamic program whose exponential lives in a connectivity record R (2^n ordered / 3^n SU(2) /
4^n SU(N)).

WHAT THIS MODULE VERIFIES (against the real engine, via cos_harness.c which dumps the engine's per-subset
D_corr/D_vac and ground-truth C_V):
  1. rossi_naive() -- a faithful port of the engine's recursion -- reproduces engine C_V EXACTLY (0.0e+00).
  2. cos_subsetconv() -- the CoS-style 2^n organization: solve D_corr = C (*) D_vac (subset convolution,
     D_vac[empty]=1) rank-by-rank in the zeta domain, O(2^n n^2) -- reproduces engine C_V to machine
     precision (fp reassociation only, ~1e-14).
So the CoS '2^n' organization is a correct drop-in for the engine's '3^n' combine.

HONEST COST PICTURE (the reason NOT to rush a port):
  engine  combine = 3^n ;  subset-conv combine = 2^n n^2 .  The 3^n only overtakes 2^n n^2 at n>=12.
  AND both share the dominant cost 2^n * n^3 of the 2^n sub-determinants, which subset-conv does NOT touch.
  So replacing the 3^n loop alone is a real but SMALL win, and only at high order. The big lever is the
  n^3 -> n^2 determinant prefactor, which needs the CoS *forward* DP that builds minors incrementally --
  a larger build, worth it only when pushing diagram order or going to SU(N).

The integration recommendations are in COS_PROTOTYPE_RESULT.md."""
import os, subprocess, numpy as np
import tempfile

def popcount(x): return bin(x).count('1')

def rossi_naive(n, seed, dv):
    """Faithful port of engine C_V: C[mask] = seed[mask] - sum_{sm proper submask} C[sm]*dv[mask^sm]."""
    N = 1 << n; C = np.zeros(N)
    for mask in sorted(range(N), key=popcount):
        val = seed[mask]; sm = (mask - 1) & mask
        while True:
            if sm != mask: val -= C[sm] * dv[mask ^ sm]
            if sm == 0: break
            sm = (sm - 1) & mask
        C[mask] = val
    return C

def _zeta(a):
    a = a.copy(); n = a.shape[0].bit_length() - 1
    for b in range(n):
        for m in range(1 << n):
            if m & (1 << b): a[m] += a[m ^ (1 << b)]
    return a
def _mobius(a):
    a = a.copy(); n = a.shape[0].bit_length() - 1
    for b in range(n):
        for m in range(1 << n):
            if m & (1 << b): a[m] -= a[m ^ (1 << b)]
    return a

def cos_subsetconv(n, seed, dv):
    """CoS-style 2^n organization: solve D_corr = C (*) D_vac for C, rank-by-rank in the zeta domain."""
    N = 1 << n; pc = np.array([popcount(m) for m in range(N)])
    sz = [_zeta(np.where(pc == k, seed, 0.0)) for k in range(n + 1)]
    dz = [_zeta(np.where(pc == k, dv,   0.0)) for k in range(n + 1)]
    Cz = [None] * (n + 1)
    for k in range(n + 1):                      # dz[0]=1 pointwise -> Cz[k] solved directly
        acc = sz[k].copy()
        for j in range(1, k + 1): acc = acc - Cz[k - j] * dz[j]
        Cz[k] = acc
    C = np.zeros(N)
    for k in range(n + 1):
        mk = _mobius(Cz[k]); C[pc == k] = mk[pc == k]
    return C

def _build_harness():
    here = os.path.dirname(os.path.abspath(__file__)); eng = os.path.join(here, '..', 'engine')
    out = os.path.join(tempfile.gettempdir(), 'cosh_selftest' + ('.exe' if os.name=='nt' else ''))
    r = subprocess.run(['gcc', '-O2', '-I', eng, '-o', out, os.path.join(here, 'cos_harness.c'),
                        os.path.join(eng, 'cdet_engine.c'), '-lm'], capture_output=True, text=True)
    return out if r.returncode == 0 else None

def _load(harness, n):
    out = subprocess.run([harness, str(n)], capture_output=True, text=True).stdout.splitlines()
    cv = float(out[0].split()[1]); N = 1 << n
    seed = np.zeros(N); dv = np.zeros(N)
    for ln in out[1:]:
        m, s, d = ln.split(); seed[int(m)] = float(s); dv[int(m)] = float(d)
    return cv, seed, dv

def _selftest():
    print("cos_prototype self-test (verify both reorganizations reproduce the real engine C_V):")
    h = _build_harness()
    if h is None:
        print("  (could not build harness; gcc/engine unavailable) -- skipping live check")
        return
    worst_naive = worst_conv = 0.0
    for n in [3, 4, 5, 6, 7]:
        cv, seed, dv = _load(h, n); full = (1 << n) - 1
        dn = abs(rossi_naive(n, seed, dv)[full] - cv)
        dc = abs(cos_subsetconv(n, seed, dv)[full] - cv)
        worst_naive = max(worst_naive, dn); worst_conv = max(worst_conv, dc)
        assert dn == 0.0, (n, dn)          # exact port of the engine
        assert dc < 1e-11, (n, dc)         # subset-conv to machine precision
    print(f"  naive port == engine C_V exactly (worst dev {worst_naive:.0e}, n=3..7)")
    print(f"  CoS subset-conv == engine C_V to machine precision (worst dev {worst_conv:.0e})")
    print("  => the CoS 2^n organization is a correct drop-in for the engine's 3^n combine. PASS")

if __name__ == '__main__':
    _selftest()
