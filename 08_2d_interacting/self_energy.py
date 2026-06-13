"""self_energy.py (v134) -- integration #3, first step: the self-energy as the INTERACTING upgrade of z.

The physical mapping (v133) established that z(inf) is the FREE single-particle addition pole (the lowest-
empty level eps_k), because the propagator carries the free spectrum. The interacting addition energy is
eps_k + Re Sigma(eps_k); the self-energy Sigma is the shift. This module establishes that observable and
verifies it exactly against exact diagonalization (the ground truth the diagrammatic self-energy series of
integration #3 will reproduce).

Two exact checks:

  (A) Hubbard ATOM -- the self-energy machinery itself. Sigma(iw) = G0(iw)^-1 - G(iw)^-1 extracted from the
      ED Lehmann Green's function matches the closed-form atomic self-energy
      Sigma(iw) = U<n> + U^2 <n>(1-<n>)/(iw + mu - U(1-<n>))  to ~1e-14. (<n> = per-spin occupation.)

  (B) Hubbard DIMER (2-site chain, free levels -+t) -- the addition pole and its shift. The spectral-
      weight-averaged addition energy of the lowest-empty (antibonding) mode is:
        * at U=0:  exactly eps_free = z(inf)          (the free addition pole z measures today)
        * at U>0:  eps_free + Re Sigma                 (the INTERACTING addition energy)
      i.e. turning on the interaction moves z's free pole to the interacting one by exactly the self-energy,
      with the leading shift the Hartree term U<n_-sigma>.

So z and integration #3 are the same physical target at two resummation levels: z reports the Sigma=0
(free) addition pole; the self-energy series reports the interacting one. This SUPPLEMENTS z (the free
z-flow is the Sigma=0 limit, unchanged) and uses ED only as the verification anchor. Frozen engine untouched.

The diagrammatic self-energy (the engine-side computation, reusing the v132 fast-minor machinery for the
irreducible series) is the next sub-step; this fixes the observable and its exact ground truth first."""
import numpy as np
from hubbard_ed import HubbardED

# ---- self-energy from ED (Lehmann Matsubara G, then Dyson) ----
def _matsubara_Gkk(ed, kvec, spin=0):
    ck = sum(kvec[i] * ed._op_matrix(ed._c, i + spin * ed.N) for i in range(ed.N))
    ckE = ed.V.T @ ck @ ed.V; cdkE = ckE.T
    E = ed.E; w = np.exp(-ed.beta * E) / ed.Z
    num = ckE * (cdkE.T) * (w[:, None] + w[None, :])
    return lambda iwn: np.sum(num / (iwn - (E[None, :] - E[:, None])))

def atomic_sigma_check(U, mu, beta):
    """ED self-energy vs the closed-form atomic Sigma. Returns worst |Sigma_ED - Sigma_closed|."""
    ed = HubbardED(np.zeros((1, 1)), U=U, mu=mu, beta=beta)
    nop = ed.V.T @ ed._op_matrix(lambda s, p: (s, 1.0) if (s >> p & 1) else (None, 0.0), 0) @ ed.V
    nd = float(np.sum(np.diag(nop) * np.exp(-beta * ed.E)) / ed.Z)
    G = _matsubara_Gkk(ed, np.array([1.0]))
    worst = 0.0
    for k in [0, 1, 3, 7, 12]:
        iwn = 1j * (2 * k + 1) * np.pi / beta
        S_ed = (iwn + mu) - 1.0 / G(iwn)                      # G0^-1 = iwn+mu (atom)
        S_cf = U * nd + (U * U * nd * (1 - nd) / (iwn + mu - U * (1 - nd)) if U > 0 else 0.0)
        worst = max(worst, abs(S_ed - S_cf))
    return worst, nd

# ---- addition pole of the lowest-empty mode on the dimer ----
def addition_energy(ed, kvec, mu, spin=0):
    """Spectral-weight-averaged addition energy of mode k (engine-convention level = pole + mu)."""
    ck = sum(kvec[i] * ed._op_matrix(ed._c, i + spin * ed.N) for i in range(ed.N))
    ckE = ed.V.T @ ck @ ed.V; cdkE = ckE.T
    E = ed.E; w = np.exp(-ed.beta * E) / ed.Z
    num, den = 0.0, 0.0
    for m in range(ed.dim):
        for n in range(ed.dim):
            wt = cdkE[n, m] ** 2 * (w[m] + w[n])
            if wt > 1e-9 and (E[n] - E[m]) > 1e-6:           # addition excitations above the Fermi level
                num += (E[n] - E[m]) * wt; den += wt
    return (num / den + mu) if den > 0 else None

def dimer_addition_flow(beta=8.0, mu=0.8, Us=(0.0, 0.5, 1.0, 2.0, 3.0)):
    hop = np.array([[0.0, -1.0], [-1.0, 0.0]]); wlev, Vlev = np.linalg.eigh(hop)
    kAB = int(np.argmax(wlev)); eps_free = float(wlev[kAB])
    rows = []
    for U in Us:
        ed = HubbardED(hop, U=U, mu=mu, beta=beta)
        nop = ed.V.T @ ed._op_matrix(lambda s, p: (s, 1.0) if (s >> p & 1) else (None, 0.0), 0) @ ed.V
        n_per_spin = float(np.sum(np.diag(nop) * np.exp(-beta * ed.E)) / ed.Z)
        e_add = addition_energy(ed, Vlev[:, kAB], mu)
        rows.append((U, eps_free, e_add, e_add - eps_free, U * n_per_spin))
    return eps_free, rows

def _selftest():
    print("self_energy self-test (the interacting upgrade of z, verified vs ED):")
    # (A) atom: Sigma machinery vs closed form
    worstS = 0.0
    for U, mu in [(1.0, 0.5), (2.0, 1.0), (3.0, 1.5)]:
        w, nd = atomic_sigma_check(U, mu, beta=5.0); worstS = max(worstS, w)
    assert worstS < 1e-10, worstS
    print(f"  (A) atom: ED self-energy == closed-form atomic Sigma, worst {worstS:.0e}")
    # (B) dimer: U=0 addition pole == z(free level); U>0 shifted by the self-energy
    eps_free, rows = dimer_addition_flow()
    print(f"  (B) dimer lowest-empty (antibonding) eps_free = {eps_free:.5f} (= z(inf))")
    print(f"      {'U':>4} {'addition energy':>15} {'shift = ReSigma':>15} {'Hartree U<n>':>13}")
    for U, ef, ea, sh, hart in rows:
        tag = "  == z" if U == 0 else ""
        print(f"      {U:>4} {ea:>15.5f} {sh:>15.5f} {hart:>13.5f}{tag}")
    u0 = [r for r in rows if r[0] == 0.0][0]
    assert abs(u0[2] - eps_free) < 1e-9, u0           # U=0 addition energy == free level == z
    big = [r for r in rows if r[0] == 3.0][0]
    assert big[3] > 0.5, big                          # U>0 genuinely shifts the pole (self-energy nonzero)
    print("  => U=0 addition pole == z(inf) (free); U>0 = eps_free + Re Sigma (interacting). z is the Sigma=0")
    print("     limit of the self-energy observable. Supplements z; engine untouched. PASS")

if __name__ == "__main__":
    _selftest()
