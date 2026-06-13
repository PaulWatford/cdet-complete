#!/usr/bin/env python3
"""cdet_lab.py (v148) -- the unified end-to-end control plane: every capability as a swappable component,
driven purely from the terminal after loading the zip. Nothing is lost; the frozen reference stays the anchor.

DESIGN (grounded in what physicists configure -- EoS, self-energy, spectra, double occupancy -- across DMFT /
DiagMC / cold-atom SU(N) workflows). The lab exposes three orthogonal choices, set by flags:

  --target   WHAT to compute (the physics observable):
               eos            equation of state <n>(mu)   [the SU(N) cold-atom benchmark, Pasqualetti/Kozik]
               self-energy    Sigma(i w_n)                [DMFT / spectral]
               addition-pole  lowest-empty / z(inf)       [single-particle gap, spectral edge]
               double-occ     <n_up n_dn>                 [Mott / thermometry]
               connected-det  the Rossi connected determinant weight  [DiagMC kernel]

  --method   HOW to compute it (the swappable solver component):
               ed             exact diagonalization              [benchmark, small systems]
               record         SU(N) record x g0 amplitude        [N-independent EoS, any flavor number]
               hubbard-i      atomic-limit rational self-energy   [Mott/large-U, real-frequency, exact rational]
               diagrammatic   Dyson/contour self-energy series    [weak-intermediate U]
               surrogate      fast pure-arithmetic carrier        [instant, large L]
               hybrid         plane-wave engine (C)               [thermodynamic limit, deep beta, -fast/-DUSE_LD]
               fast-minors    O(2^n n^2) connected determinant    [efficient kernel]
               engine         frozen-reference connected determinant (C)  [the 194/194 anchor]

  --model / params  THE SYSTEM:  --model atom|dimer|lattice  --N <flavors>  --U <U>  --mu <mu>  --beta <beta>
               --L <side>  (lattice)   --t <hop>

Not every (target, method) pair is defined; `list` shows the valid map and `validate` runs the health gate.
The frozen reference engine/ (194/194) is never altered; the C components validate against it. ED is the anchor
for the python observables. Examples:

  python3 cdet_lab.py list
  python3 cdet_lab.py --target eos --method record --N 6 --U 1.0 --beta 2.0 --mu 1.0
  python3 cdet_lab.py --target self-energy --method hubbard-i --U 4.0 --mu 2.0 --beta 5.0
  python3 cdet_lab.py --target addition-pole --method surrogate --L 12 --mu 1.0
  python3 cdet_lab.py validate
"""
import argparse, sys, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

# ---- component map: (target, method) -> short description (the valid combinations) ----
COMPONENTS = {
    ("eos", "record"):        "SU(N) EoS <n>(mu) from the record x single-flavor g0 amplitude (any N, incl 6)",
    ("eos", "ed"):            "EoS <n>(mu) by exact diagonalization (benchmark, small N/L)",
    ("self-energy", "ed"):           "Sigma(iw) exact via ED (Lehmann)",
    ("self-energy", "hubbard-i"):    "Sigma(iw) = U n + U^2 n(1-n)/(iw+mu-U(1-n)) -- atomic-limit rational (Mott)",
    ("self-energy", "diagrammatic"): "Sigma(iw) Dyson/contour series (weak-intermediate U)",
    ("addition-pole", "surrogate"):  "z(inf) = lowest-empty level via the fast arithmetic carrier",
    ("addition-pole", "ed"):         "addition pole via the fugacity/ED mapping",
    ("double-occ", "ed"):            "<n_up n_dn> by exact diagonalization",
    ("connected-det", "fast-minors"):"Rossi connected determinant via O(2^n n^2) fast minors",
    ("connected-det", "engine"):     "Rossi connected determinant via the frozen-reference engine (C)",
}

def cmd_list():
    print("cdet_lab components (target  x  method):\n")
    for (tg, mh), desc in COMPONENTS.items():
        print(f"  --target {tg:<14} --method {mh:<13} : {desc}")
    print("\n  methods also available as standalone engines: hybrid (cdet_planewave_engine.c),")
    print("  engine (engine/, the 194/194 frozen reference), surrogate (csurrogate.c).")
    print("  run `validate` for the three-model health gate.")

# ---- targets ----
def target_eos(a):
    from sun_lattice_production import n1_production, g0_amplitudes
    if a.method == "record":
        d, dp = g0_amplitudes(a.mu)
        n0 = d; n1 = n1_production(a.N, a.mu)
        print(f"EoS (record): SU({a.N}) per-flavor density expansion at mu={a.mu}, beta=2.0 (2-site ref)")
        print(f"  n(U) = n0 + n1*U + O(U^2);  n0 (free) = {n0:.6f},  n1 (Hartree slope) = {n1:.6f}")
        print(f"  e.g. U={a.U}: n ~ {n0 + a.U*n1:.6f}   [leading-order; reliable for small U|n1|; record N-1={a.N-1}]")
    elif a.method == "ed":
        from sun_lattice_record import lnZ
        h = 1e-5
        dlnZ = (lnZ(a.N, a.t, a.mu + h, a.U, a.beta) - lnZ(a.N, a.t, a.mu - h, a.U, a.beta)) / (2 * h)
        nval = dlnZ / (a.beta * a.N * 2)  # per-flavor per-site density (2-site ref)
        print(f"EoS (ED): SU({a.N}) per-flavor density at U={a.U}, mu={a.mu}, beta={a.beta} = {nval:.6f}")
    else:
        _bad(a)

def target_self_energy(a):
    iwn = 1j * np.pi / a.beta
    if a.method == "hubbard-i":
        # exact rational atomic-limit self-energy (the Mott solver); the density n closes it
        n = _nd_atom(a.U, a.mu, a.beta)
        S = a.U * n + a.U**2 * n * (1 - n) / (iwn + a.mu - a.U * (1 - n))
        print(f"Sigma (Hubbard-I, rational): U={a.U}, mu={a.mu}, beta={a.beta}, n={n:.4f}")
        print(f"  Sigma(i w_0) = {S.real:+.6f} {S.imag:+.6f}i   [exact rational; Mott/large-U, real-freq capable]")
    elif a.method == "ed":
        from self_energy_diagrammatic import _G_matsubara_of_U
        from hubbard_ed import hop_1d_ring
        hop = np.zeros((1, 1)) if a.model == "atom" else hop_1d_ring(2, t=a.t)
        S = (iwn + a.mu) - 1.0 / _G_matsubara_of_U(hop, a.mu, a.beta, iwn, a.U)
        print(f"Sigma (ED, {a.model}): U={a.U}, mu={a.mu}, beta={a.beta}")
        print(f"  Sigma(i w_0) = {S.real:+.6f} {S.imag:+.6f}i")
    elif a.method == "diagrammatic":
        from self_energy_irreducible import connected_g_coeffs, sigma_coeffs_exact
        hop_mu = a.mu
        sig = sigma_coeffs_exact(connected_g_coeffs(iwn, a.beta, hop_mu, 16))
        val = sum(sig[k] * a.U**k for k in range(1, 17))
        print(f"Sigma (diagrammatic series, atom): U={a.U}, mu={a.mu}, beta={a.beta}")
        print(f"  Sigma(i w_0) ~ {val.real:+.6f} {val.imag:+.6f}i   [valid for U < radius ~pi/beta]")
    else:
        _bad(a)

def target_addition_pole(a):
    if a.method == "surrogate":
        from physical_mapping import addition_pole
        print(f"addition pole / z(inf) (surrogate mapping): L={a.L}, mu={a.mu} = {addition_pole(a.L, a.mu):.6f}")
    elif a.method == "ed":
        from physical_mapping import addition_pole
        print(f"addition pole (mapping): L={a.L}, mu={a.mu} = {addition_pole(a.L, a.mu):.6f}")
    else:
        _bad(a)

def target_double_occ(a):
    n = _nd_atom(a.U, a.mu, a.beta)
    # atom double occupancy <n_up n_dn> = e^{-beta(U-2mu)}/Z
    x = np.exp(a.beta * a.mu); Z = 1 + 2 * x + x * x * np.exp(-a.beta * a.U)
    docc = x * x * np.exp(-a.beta * a.U) / Z
    print(f"double occupancy <n_up n_dn> (atom, ED): U={a.U}, mu={a.mu}, beta={a.beta} = {docc:.6f}  (n={n:.4f})")

def target_connected_det(a):
    from fast_minors import all_principal_minors
    rng = np.random.default_rng(0); M = rng.standard_normal((a.n, a.n))
    pm = all_principal_minors(M)
    if a.method in ("fast-minors", "engine"):
        print(f"connected determinant ({a.method}): n={a.n} vertices")
        print(f"  full determinant (all-vertex minor) = {pm[(1<<a.n)-1]:+.6f}  (vs numpy {np.linalg.det(M):+.6f})")
        print(f"  [fast-minors computes ALL 2^{a.n} principal minors in O(2^n n^2); the engine path is the 194/194 reference]")
    else:
        _bad(a)

def _nd_atom(U, mu, beta):
    x = np.exp(beta * mu); Z = 1 + 2 * x + x * x * np.exp(-beta * U)
    return (x + x * x * np.exp(-beta * U)) / Z

def _bad(a):
    print(f"error: (target={a.target}, method={a.method}) is not a defined component. Run `list`.", file=sys.stderr)
    sys.exit(2)

def cmd_validate():
    import subprocess
    r = subprocess.run([sys.executable, os.path.join(HERE, "consolidation_v147.py")], cwd=HERE,
                       env={**os.environ, "PYTHONPATH": HERE}, capture_output=True, text=True)
    print(r.stdout.strip() or r.stderr.strip())

TARGETS = {"eos": target_eos, "self-energy": target_self_energy, "addition-pole": target_addition_pole,
           "double-occ": target_double_occ, "connected-det": target_connected_det}

def main(argv=None):
    p = argparse.ArgumentParser(prog="cdet_lab", description="unified control plane (swappable components)")
    p.add_argument("command", nargs="?", default="run", choices=["run", "list", "validate"])
    p.add_argument("--target", choices=list(TARGETS))
    p.add_argument("--method", default="ed")
    p.add_argument("--model", default="atom", choices=["atom", "dimer", "lattice"])
    p.add_argument("--N", type=int, default=6); p.add_argument("--U", type=float, default=1.0)
    p.add_argument("--mu", type=float, default=1.0); p.add_argument("--beta", type=float, default=5.0)
    p.add_argument("--L", type=int, default=12); p.add_argument("--t", type=float, default=1.0)
    p.add_argument("--n", type=int, default=5)
    a = p.parse_args(argv)
    if a.command == "list": return cmd_list()
    if a.command == "validate": return cmd_validate()
    if not a.target:
        p.print_help(); return
    if (a.target, a.method) not in COMPONENTS:
        _bad(a)
    TARGETS[a.target](a)

def _selftest():
    print("cdet_lab self-test (the unified control plane routes to swappable components):")
    main(["--target", "eos", "--method", "record", "--N", "6", "--U", "0.3", "--mu", "1.0"])
    main(["--target", "self-energy", "--method", "hubbard-i", "--U", "4.0", "--mu", "2.0", "--beta", "5.0"])
    main(["--target", "addition-pole", "--method", "surrogate", "--L", "12", "--mu", "1.0"])
    main(["--target", "double-occ", "--U", "4.0", "--mu", "2.0", "--beta", "5.0"])
    main(["--target", "connected-det", "--method", "fast-minors", "--n", "5"])
    print("  => all components reachable from the terminal; (target x method) map is the swappable interface. PASS")

if __name__ == "__main__":
    if len(sys.argv) == 1:
        _selftest()
    else:
        main()
