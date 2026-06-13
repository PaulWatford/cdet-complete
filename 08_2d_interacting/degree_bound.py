"""degree_bound.py (v95) -- THE DEGREE BOUND, settled by a symbolic census of the actual C_V.

THE METHOD. The CDet port (cdet_port.CDet) is pure-Python generic arithmetic, so it can be run
with SYMBOLIC occupancies: g0 is patched to carry one sympy symbol per (spin, window level) for
the levels {0,1,2,3} (all other levels numeric-saturated), determinants go through sympy, and
the n=3 connected combination is expanded exactly. The result is the exact polynomial of the
stripped <C> in the deviation variables (f2, f3, delta1, delta0) at fixed tau's; repeating over
independent tau draws gives the generic monomial support.

THE THEOREM (verified): the maximal total deviation weight at order n is 2n+1 -- at n=3, SEVEN
(the up-spin determinant is (n+1)x(n+1) because of the external to/ti vertex: 4 propagators up
+ 3 down, each linear in occupancies). Both prior statements were wrong: v93's bound "8" (it
counted matrix dimension, not propagator count) and the v94-conjectured "6" (it missed the
external vertex). The support is FULL: all C(7+3,3) = 330 monomials up to weight 7 appear
generically (intersection over tau draws).

THE CORRECTED MENU. Balance positions come from exponent DIFFERENCES (Delta-vectors), not just
positive-weight pairs -- v93's 3-member menu {11/6, 13/7, 15/8} was doubly wrong. The realized
candidate set near the deep object, from the census support, is
    {25/14, 9/5, 20/11, 11/6, 24/13, 13/7, 15/8, 17/9}  in (1.78, 1.90),
with mu* = (2 Da + 3 Db - Dc) / (Da + Db - Dc - Dd) and q = |Da + Db - Dc - Dd| for
Delta = w(1) - w(2). All rational: the field theorem stands and the chord remains excluded.

THE TENSION DISSOLVED. 24/13 = 1.84615 (q = 13) sits 0.26 sigma from the v94 six-point constant
1.8467(21), and a q = 13 balance approaches as ln(r)/(13 beta) -- nearly flat across beta =
36-56. Fits over the six honest points: 11/6 ln r = +3.11(50) chi2 4.79/5; 13/7 ln r = -2.98(58)
chi2 1.58/5; 24/13 ln r = +0.13(107) chi2 2.41/5. The v94 "menu-vs-flatness tension" was an
artifact of the wrong menu: the constant reading IS the 24/13 member. (And 15/8, called
"structurally excluded" in v94 notes via the wrong bound, is in the menu -- it stays only
EMPIRICALLY dead at 4.6 sigma. Record corrected.)

STATUS AFTER v95: identification OPEN among menu members, leading {13/7 (q=7), 24/13 (q=13)},
with 11/6 (q=6) disfavored (chi2/dof 0.96 vs 0.32 / 0.48). The closing routes, in order: (a) THE
COEFFICIENT PROGRAM -- tau-average the 330 census coefficients (by symbolic draws or a numeric
occupancy-design regression) and predict the realized zero outright, no fitting; (b) deep-beta
precision (24/13 vs 13/7 separate by ~0.005 at beta = 72, ~0.007 at beta = 100).
"""
import numpy as np
import sympy as sp
from fractions import Fraction as Fr
from cdet_port import CDet
from symmetry_reduction import cube_hopping

BETA, MU = 20.0, 1.84
WIN = (0.0, 1.0, 2.0, 3.0)
POOL6 = {36: (1.8450, 0.0030), 40: (1.8457, 0.0046), 44: (1.8510, 0.0076),
         48: (1.846, 0.009), 52: (1.8527, 0.0052), 56: (1.8407, 0.0103)}
MENU_NEAR = [Fr(25, 14), Fr(9, 5), Fr(20, 11), Fr(11, 6), Fr(24, 13), Fr(13, 7),
             Fr(15, 8), Fr(17, 9)]


def census(seed=1033, draws=1):
    """one (or more) symbolic draws; returns the monomial support set of (f2,f3,d1,d0)."""
    hop = cube_hopping(6)
    base = CDet(hop, beta=BETA, to=0.7, ti=0.2)
    ev, U = base.ev, base.U
    lev = np.round(ev, 9)

    class SymCDet(CDet):
        def __init__(self, syms):
            self.beta, self.to, self.ti = BETA, 0.7, 0.2
            self.ev, self.U = ev, U
            self.syms = syms

        def g0(self, i, j, tau, mu):
            tt = complex(tau)
            while tt.real > self.beta:
                tt -= 2 * self.beta
            while tt.real <= -self.beta:
                tt += 2 * self.beta
            out = sp.Integer(0); num = 0.0 + 0j
            groups = {}
            for k in range(len(ev)):
                groups.setdefault(lev[k], []).append(k)
            for l, ks in groups.items():
                w = sum(U[i, k] * U[j, k] for k in ks)
                xi = l - mu
                if tt.real > 0:
                    e = -np.exp(-xi * tt); part = "1-n"
                elif tt.real < 0:
                    e = np.exp(-xi * tt); part = "n"
                else:
                    e = 1.0; part = "n"
                if l in self.syms:
                    occ = (1 - self.syms[l]) if part == "1-n" else self.syms[l]
                    out += sp.Float(float((w * e).real), 15) * occ \
                        + sp.I * sp.Float(float((w * e).imag), 15) * occ
                else:
                    nf = 1.0 / (np.exp(BETA * xi) + 1.0)
                    num += w * e * ((1.0 - nf) if part == "1-n" else nf)
            return out + sp.Float(float(num.real), 15) + sp.I * sp.Float(float(num.imag), 15)

        def _bdet(self, rs, rt, cs, ct, mu):
            m = len(rs)
            if m == 0:
                return sp.Integer(1)
            M = sp.Matrix(m, m, lambda a, b: self.g0(rs[a], cs[b], rt[a] - ct[b], mu))
            return sp.expand(M.det(method='berkowitz'))

    rng = np.random.default_rng(seed)
    support = None
    for _ in range(draws):
        taus = sorted(rng.uniform(0, BETA, 3))
        su = {l: sp.Symbol(f"nu{int(l)}") for l in WIN}
        sd = {l: sp.Symbol(f"nd{int(l)}") for l in WIN}
        cu, cd = SymCDet(su), SymCDet(sd)
        V = [(1, taus[0]), (2, taus[1]), (4, taus[2])]

        # spin selection: the up determinant carries the external to time
        class Hybrid2(CDet):
            def __init__(self):
                self.beta, self.to, self.ti = BETA, 0.7, 0.2
                self.ev, self.U = ev, U

            def _bdet(self, rs, rt, cs, ct, mu):
                is_up = (self.to in list(rt))
                return (cu if is_up else cd)._bdet(rs, rt, cs, ct, mu)

        expr = sp.expand(Hybrid2().C_V(V, MU))
        subs, devs = {}, {}
        for tag, syms in (("u", su), ("d", sd)):
            for l, nsym in syms.items():
                li = int(l)
                if li <= 1:
                    d = sp.Symbol(f"D{li}{tag}"); subs[nsym] = 1 - d; devs[d] = li
                else:
                    f = sp.Symbol(f"F{li}{tag}"); subs[nsym] = f; devs[f] = li
        P = sp.Poly(sp.expand(expr.subs(subs)), *devs.keys())
        sup = set()
        for mono, coef in P.terms():
            if abs(complex(coef)) < 1e-22:
                continue
            agg = {"F2": 0, "F3": 0, "D1": 0, "D0": 0}
            for g, p in zip(P.gens, mono):
                agg[str(g)[:2]] += p
            sup.add((agg["F2"], agg["F3"], agg["D1"], agg["D0"]))
        support = sup if support is None else (support & sup)
    return support


def balances(support, lo=Fr(1), hi=Fr(2)):
    out = set()
    S = list(support)
    for i in range(len(S)):
        for j in range(i + 1, len(S)):
            da, db, dc, dd = (S[i][k] - S[j][k] for k in range(4))
            den = da + db - dc - dd
            if den == 0:
                continue
            mu = Fr(2 * da + 3 * db - dc, den)
            if lo < mu < hi and mu != 2:
                out.add(mu)
    return sorted(out)


def fit(mu, q):
    B = np.array(sorted(POOL6)); Z = np.array([POOL6[b][0] for b in B])
    E = np.array([POOL6[b][1] for b in B])
    be = (Z - float(mu)) * q * B; berr = E * q * B; w = 1 / berr**2
    bb = float(np.sum(w * be) / np.sum(w)); sb = float(1 / np.sqrt(np.sum(w)))
    chi = float(np.sum(((be - bb) / berr)**2))
    return bb, sb, chi


def _selftest():
    ok = True
    sup = census(draws=1)
    mx = max(sum(m) for m in sup)
    print(f"census (1 draw): {len(sup)} monomials, max weight {mx} "
          f"(gates: 330 = full simplex, max = 7 = 2n+1)")
    ok = ok and len(sup) == 330 and mx == 7
    near = [m for m in balances(sup) if Fr(178, 100) < m < Fr(190, 100)]
    print(f"menu near the object: {[str(x) for x in near]} (gate == MENU_NEAR)")
    ok = ok and near == MENU_NEAR
    chord = float(np.sqrt(2 + np.sqrt(2)))
    ok = ok and all(abs(float(x) - chord) > 1e-9 for x in near)
    print(f"field theorem: menu all-rational; chord {chord:.5f} still excluded (gate)")
    f116, f137, f2413 = fit(Fr(11, 6), 6), fit(Fr(13, 7), 7), fit(Fr(24, 13), 13)
    print(f"fits: 11/6 chi2 {f116[2]:.2f}/5; 13/7 chi2 {f137[2]:.2f}/5; "
          f"24/13 ln r = {f2413[0]:+.2f}({f2413[1]:.2f}) chi2 {f2413[2]:.2f}/5")
    print(f"  (gates: 24/13 chi2 < 4 with |ln r| < 1.5 -- the flat reading IS the q=13 member; "
          f"13/7 chi2 < 4; 11/6 chi2 > both)")
    ok = ok and f2413[2] < 4 and abs(f2413[0]) < 1.5 and f137[2] < 4 \
        and f116[2] > f137[2] and f116[2] > f2413[2]
    print("degree-bound self-test (census; menu; field; fits):", "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
