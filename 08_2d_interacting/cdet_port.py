"""General CDet port: the frozen engine's connected determinant for ANY hopping matrix,
made complex-TIME capable so a contour can be deformed off the real imaginary-time axis.

This is the geometry-general sibling of counterterm_sampler.RingCDet (which is ring-only and
vectorised over a complex-mu circle). The connected recursion is identical to the frozen engine
(engine/cdet_engine.c: D_corr / D_vac / Rossi inclusion-exclusion). g0 is the engine propagator
with the 0^- convention; the branch (tau>0 vs tau<0) is selected by Re(tau), which is the analytic
continuation that keeps a deformed contour on the piece it started on.

Self-test (run as main) checks it reproduces the validated ring port to 1e-12, so it inherits the
counterterm_sampler 1e-16-vs-ED validation. Frozen engine untouched.
"""
import numpy as np


class CDet:
    def __init__(self, hop, beta=4.0, to=0.7, ti=0.2):
        self.beta, self.to, self.ti = beta, to, ti
        self.ev, self.U = np.linalg.eigh(hop)

    def g0(self, i, j, tau, mu):
        """Engine propagator, scalar complex tau, scalar (real or complex) mu."""
        beta = self.beta
        tt = complex(tau)
        while tt.real > beta:
            tt -= 2 * beta
        while tt.real <= -beta:
            tt += 2 * beta
        out = 0.0 + 0j
        for k in range(len(self.ev)):
            xi = self.ev[k] - mu
            nf = 1.0 / (np.exp(beta * xi) + 1.0)
            if tt.real > 0:
                gk = -(1.0 - nf) * np.exp(-xi * tt)
            elif tt.real < 0:
                gk = nf * np.exp(-xi * tt)
            else:
                gk = nf
            out += self.U[i, k] * self.U[j, k] * gk
        return out

    def _bdet(self, rs, rt, cs, ct, mu):
        m = len(rs)
        if m == 0:
            return 1.0 + 0j
        M = np.empty((m, m), complex)
        for a in range(m):
            for b in range(m):
                M[a, b] = self.g0(rs[a], cs[b], rt[a] - ct[b], mu)
        return np.linalg.det(M)

    def _Dcorr(self, V, mu):
        n = len(V)
        rs = [0] + [v[0] for v in V]; rt = [self.to] + [v[1] for v in V]
        cs = [0] + [v[0] for v in V]; ct = [self.ti] + [v[1] for v in V]
        du = self._bdet(rs, rt, cs, ct, mu); dd = 1.0 + 0j
        if n > 0:
            s = [v[0] for v in V]; tt = [v[1] for v in V]; dd = self._bdet(s, tt, s, tt, mu)
        return ((-1) ** n) * du * dd

    def _Dvac(self, V, mu):
        n = len(V)
        if n == 0:
            return 1.0 + 0j
        s = [v[0] for v in V]; tt = [v[1] for v in V]
        dA = self._bdet(s, tt, s, tt, mu)
        return ((-1) ** n) * dA * dA

    def C_V(self, V, mu):
        """Connected determinant of a vertex list V=[(site,tau),...] (Rossi recursion)."""
        n = len(V)
        if n == 0:
            return self._Dcorr([], mu)
        N = 1 << n; Dv = [None] * N; C = [None] * N
        for mask in range(N):
            Dv[mask] = self._Dvac([V[i] for i in range(n) if mask & (1 << i)], mu)
        for k in range(n + 1):
            for mask in range(N):
                if bin(mask).count("1") != k:
                    continue
                val = self._Dcorr([V[i] for i in range(n) if mask & (1 << i)], mu)
                sm = (mask - 1) & mask
                while True:
                    if sm != mask:
                        val = val - C[sm] * Dv[mask ^ sm]
                    if sm == 0:
                        break
                    sm = (sm - 1) & mask
                C[mask] = val
        return C[N - 1]


def _selftest():
    """Reproduce the validated ring port (counterterm_sampler.RingCDet) to 1e-12."""
    from hubbard_ed import hop_1d_ring
    from counterterm_sampler import RingCDet
    L, beta, mu = 2, 4.0, 1.1
    ref = RingCDet(L=L, beta=beta, to=0.7, ti=0.2)
    gen = CDet(hop_1d_ring(L, 1.0), beta=beta, to=0.7, ti=0.2)
    rng = np.random.default_rng(0); worst = 0.0
    for n in (0, 1, 2):
        for _ in range(40):
            V = [(int(rng.integers(L)), float(rng.uniform(0, beta))) for _ in range(n)]
            a = gen.C_V(V, mu)
            b = ref.C_V(V, np.array([mu + 0j]))[0]
            worst = max(worst, abs(a - b))
    print(f"cdet_port self-test: max|general - validated ring port| = {worst:.2e}  "
          f"({'PASS' if worst < 1e-12 else 'FAIL'})")
    return worst < 1e-12


if __name__ == "__main__":
    _selftest()
