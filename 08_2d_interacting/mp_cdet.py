"""mp_cdet.py (v103) -- THE CERTIFIER: a high-precision (mpmath) mirror of cdet_port.CDet, used to
prove the production float64 engine correct on the deep-beta corner configs (clustered tau near
beta) where naive float64 silently drops the far-level antiperiodic images.

This is NOT a production engine -- at the dps required for deep beta it is ~10^4-10^5x too slow
for Monte Carlo. Its sole job is to CERTIFY stable_cdet.StableCDet (which runs at float64 speed).
The required precision grows with beta: the g0 propagator sums per-level terms of size
e^{|xi| tau} (up to e^{~100} at beta=36) that cancel to O(0.04), so ~dps 120-200 is needed for
3-4 honest digits on the worst corner configs; naive float64 (16 digits) has ZERO correct digits
there. See PRECISION_RESULT.md.
"""
import numpy as np
import mpmath as mp


class MPCDet:
    def __init__(self, hop, beta, to=0.7, ti=0.2, dps=120):
        mp.mp.dps = dps
        ev, U = np.linalg.eigh(hop)
        self.ev = [mp.mpf(float(x)) for x in ev]
        self.U = [[mp.mpf(float(U[i, k])) for k in range(U.shape[1])] for i in range(U.shape[0])]
        self.beta, self.to, self.ti = mp.mpf(float(beta)), mp.mpf(float(to)), mp.mpf(float(ti))
        self.dps = dps

    def g0(self, i, j, tau, mu):
        beta = self.beta; tt = mp.mpf(float(complex(tau).real))
        while tt > beta: tt -= 2 * beta
        while tt <= -beta: tt += 2 * beta
        out = mp.mpf(0)
        for k in range(len(self.ev)):
            xi = self.ev[k] - mu
            nf = 1 / (mp.e**(beta * xi) + 1)
            if tt > 0: gk = -(1 - nf) * mp.e**(-xi * tt)
            elif tt < 0: gk = nf * mp.e**(-xi * tt)
            else: gk = nf
            out += self.U[i][k] * self.U[j][k] * gk
        return out

    def _bdet(self, rs, rt, cs, ct, mu):
        m = len(rs)
        if m == 0: return mp.mpf(1)
        M = mp.matrix(m, m)
        for a in range(m):
            for b in range(m):
                M[a, b] = self.g0(rs[a], cs[b], rt[a] - ct[b], mu)
        return mp.det(M)

    def _Dcorr(self, V, mu):
        n = len(V)
        rs = [0] + [v[0] for v in V]; rt = [self.to] + [v[1] for v in V]
        cs = [0] + [v[0] for v in V]; ct = [self.ti] + [v[1] for v in V]
        du = self._bdet(rs, rt, cs, ct, mu); dd = mp.mpf(1)
        if n > 0:
            s = [v[0] for v in V]; tt = [v[1] for v in V]; dd = self._bdet(s, tt, s, tt, mu)
        return ((-1)**n) * du * dd

    def _Dvac(self, V, mu):
        n = len(V)
        if n == 0: return mp.mpf(1)
        s = [v[0] for v in V]; tt = [v[1] for v in V]
        dA = self._bdet(s, tt, s, tt, mu)
        return ((-1)**n) * dA * dA

    def C_V(self, V, mu):
        n = len(V); mu = mp.mpf(float(mu))
        if n == 0: return self._Dcorr([], mu)
        N = 1 << n; Dv = [None] * N; C = [None] * N
        for mask in range(N):
            Dv[mask] = self._Dvac([V[i] for i in range(n) if mask & (1 << i)], mu)
        for k in range(n + 1):
            for mask in range(N):
                if bin(mask).count("1") != k: continue
                val = self._Dcorr([V[i] for i in range(n) if mask & (1 << i)], mu)
                sm = (mask - 1) & mask
                while True:
                    if sm != mask: val = val - C[sm] * Dv[mask ^ sm]
                    if sm == 0: break
                    sm = (sm - 1) & mask
                C[mask] = val
        return C[N - 1]


def _selftest():
    from cdet_port import CDet
    from symmetry_reduction import cube_hopping
    hop = cube_hopping(6)
    # benign beta=4: mpmath matches the validated float64 port
    a = CDet(hop, beta=4.0).C_V([(1, 1.3), (2, 2.7), (4, 3.1)], 0.5).real
    b = float(MPCDet(hop, beta=4.0, dps=60).C_V([(1, 1.3), (2, 2.7), (4, 3.1)], 0.5))
    dev = abs(a - b) / abs(b)
    print(f"mp_cdet beta=4 vs float64 port: rel dev {dev:.1e} (gate < 1e-8)")
    # self-convergence at deep beta: dps 120 vs 200 on a corner config
    V = [(1, 34.8), (2, 35.0), (4, 35.7)]
    v120 = float(MPCDet(hop, beta=36.0, dps=120).C_V(V, 1.845))
    v200 = float(MPCDet(hop, beta=36.0, dps=200).C_V(V, 1.845))
    conv = abs(v200 - v120) / abs(v200)
    print(f"mp_cdet deep-beta self-convergence dps120 vs dps200: rel {conv:.1e} (gate < 1e-2)")
    ok = dev < 1e-8 and conv < 1e-2
    print("mp_cdet self-test (benign match; deep convergence):", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
