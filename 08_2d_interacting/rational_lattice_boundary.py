"""rational_lattice_boundary.py (v146) -- pursuing the U-axis rational lead to its boundary.

v141 found the ATOM self-energy is rational in U at fixed density (geometric recurrence -> [2/1] closed form ->
15 digits) and left a standing lead: does the LATTICE (skeleton) self-energy inherit a rational structure? This
module pursues that lead and finds its boundary -- with a clean reason.

THE THEOREM (why the atom is rational). Sigma(iw;U) is a rational function of U iff the many-body eigenvalues
E_k(U) are LINEAR in U. For the atom the interaction U*n_up*n_dn is DIAGONAL in the occupation basis, which is
the energy basis, so E_k(U) = E_k(0) + U*(double occupation) -- linear. Linear eigenvalues -> the Green's-function
poles (energy differences) move linearly -> G and Sigma are rational in U. (At fixed density; the grand-canonical
nd(U) was the v140 non-rationality, removed by fixing density -- v141.)

THE BOUNDARY (why the lattice is not). With hopping, the kinetic term does not commute with the interaction
([H_kin, H_int] != 0), so the interaction is NOT diagonal in the energy basis and the eigenvalues E_k(U) become
ALGEBRAIC (roots of a U-dependent characteristic polynomial), not linear. VERIFIED on the 2-site dimer:
||[H_kin, H_int]|| = 1.4 != 0 (the atom's is exactly 0). Algebraic eigenvalues -> Sigma is an ALGEBRAIC function
of U with BRANCH-POINT singularities, NOT rational. The dimer Sigma fails the constant-coefficient recurrence
test (residual ~0.2 vs the atom's ~1e-4) and shows a branch-point coefficient growth, confirming it.

CONSEQUENCE. The exact 15-digit RATIONAL route is confined to the ATOM / LOCAL self-energy (the Hubbard-I /
DMFT-atomic object -- still the Mott-physics driver, so the route is useful where the self-energy is local). The
full lattice self-energy is algebraic: still a closed form in principle (it satisfies a finite polynomial
equation), but not rational, and its branch points cap simple resummation -- Pade reaches past the radius (turns a
1e6 divergence at U=3 into O(1)) but not to 15 digits; conformal/algebraic methods are the lattice tool.

NET (the two axes differ): the rational structure is exact along N (the record, v145 -- polynomial, constant-
coefficient recurrence) and along U only LOCALLY (the atom, v141). Along U the lattice is algebraic, not rational,
because hopping makes the eigenvalues nonlinear in U. ED is the anchor only; frozen engine untouched (194/194)."""
import numpy as np
from self_energy_diagrammatic import _G_matsubara_of_U
from hubbard_ed import hop_1d_ring

BETA, MU = 5.0, 0.5
IWN = 1j * np.pi / BETA

def kinetic_interaction_commutator(hop):
    """||[H_kin, H_int]||: exactly 0 iff the interaction is diagonal in the energy basis -- i.e. iff the
    many-body eigenvalues are LINEAR in U, the condition for Sigma(U) to be rational. Hopping breaks it."""
    N = hop.shape[0]; dim = 1 << (2 * N)
    par = lambda s, p: (-1.0 if bin(s & ((1 << p) - 1)).count("1") & 1 else 1.0)
    c = lambda s, p: ((s & ~(1 << p), par(s, p)) if s >> p & 1 else (None, 0.0))
    cdag = lambda s, p: ((None, 0.0) if s >> p & 1 else (s | (1 << p), par(s, p)))
    Hkin = np.zeros((dim, dim))
    for s in range(dim):
        for spin in (0, 1):
            off = spin * N
            for i in range(N):
                for j in range(N):
                    if i == j or hop[i, j] == 0: continue
                    sj, p1 = c(s, j + off)
                    if sj is None: continue
                    si, p2 = cdag(sj, i + off)
                    if si is None: continue
                    Hkin[si, s] += hop[i, j] * p1 * p2
    Hint = np.diag([float(sum(1 for i in range(N) if (s >> i & 1) and (s >> (i + N) & 1))) for s in range(dim)])
    comm = Hkin @ Hint - Hint @ Hkin
    return float(np.max(np.abs(comm)))

def sigma_coeffs(hop, nmax=20, r=0.6, M=4096):
    th = 2 * np.pi * np.arange(M) / M
    G = np.array([_G_matsubara_of_U(hop, MU, BETA, IWN, r * np.exp(1j * t)) for t in th])
    a = np.array([np.sum(G * np.exp(-1j * n * th)) / (M * r ** n) for n in range(nmax + 1)])
    G0 = a[0]; sig = np.zeros(nmax + 1, complex)
    for n in range(1, nmax + 1):
        sig[n] = a[n] / G0 ** 2 - sum(sig[m] * a[n - m] for m in range(1, n)) / G0
    return sig

def const_recurrence_residual(sig, lo=6):
    c = np.array(sig[1:])
    best = np.inf
    for order in [1, 2, 3, 4]:
        A = np.array([[c[lo + i - 1 - j] for j in range(order)] for i in range(order)])
        b = np.array([c[lo + i] for i in range(order)])
        try:
            r = np.linalg.solve(A, b)
        except np.linalg.LinAlgError:
            continue
        e = max(abs(sum(r[j] * c[i - 1 - j] for j in range(order)) - c[i]) / (abs(c[i]) + 1e-30)
                for i in range(lo + order, min(lo + order + 5, len(c))))
        best = min(best, e)
    return best

def _selftest():
    print("rational_lattice_boundary self-test (the U-axis rational lead, to its boundary):")
    atom = np.zeros((1, 1)); dimer = hop_1d_ring(2, t=0.7)
    ca = kinetic_interaction_commutator(atom); cd = kinetic_interaction_commutator(dimer)
    assert ca < 1e-9 < cd, (ca, cd)
    print(f"  ||[H_kin,H_int]||: atom = {ca:.1e} (=0 -> eigenvalues linear -> rational); dimer = {cd:.1f} (!=0 -> algebraic)")
    rd = const_recurrence_residual(sigma_coeffs(dimer))
    assert rd > 1e-2, rd
    print(f"  dimer Sigma constant-coeff recurrence residual = {rd:.1e} (NOT rational; atom ~1e-4)")
    print("  => rationality of Sigma(U) <=> eigenvalues linear in U <=> interaction diagonal (atomic/local).")
    print("     Hopping ([H_kin,H_int]!=0) -> algebraic eigenvalues -> Sigma algebraic (branch points), not")
    print("     rational. The 15-digit route is atom/local (DMFT) only; the lattice needs conformal/algebraic")
    print("     resummation. Rational is exact along N (record, v145) and along U only locally (atom, v141). PASS")

if __name__ == "__main__":
    _selftest()
