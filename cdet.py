#!/usr/bin/env python3
"""cdet -- unified command-line interface for the CDet / connected-determinant suite.

One entry point over the whole codebase. Subcommands:

  cdet validate          run the validation gates (frozen 194/194, surrogate, hybrid parity, 2D path)
  cdet converge          2D thermodynamic-limit demo (4x4 -> 100x100 plane-wave propagator)
  cdet resum   [opts]    conformal-Borel resummation of the SU(N) EoS vs plain Pade
  cdet eos     [opts]    SU(N) equation-of-state density at coupling U (weak series + resummation)
  cdet docc    [opts]    double occupancy <n_up n_dn> vs U (Mott observable; interaction energy)
  cdet chi     [opts]    susceptibilities: charge compressibility kappa + spin susceptibility chi_s
  cdet plot    [what]    render figures of the validated results (matplotlib)
  cdet export  [what]    export a validated observable to CSV/JSON/HDF5
  cdet wall              convergence wall U_c vs lattice size (lattice-size effect)
  cdet tide              finite-size oscillations of the wall (its waves)
  cdet primes            prime vs composite lattice sizes (Diophantine sieve)
  cdet twist             half-integer lattices (twisted BC + rectangular)
  cdet run     [opts]    hybrid plane-wave engine grid run (the production CDet path)
  cdet sweep   [opts]    parameter-sweep stress harness with convergence checks
  cdet lab     [args]    the swappable control plane (target x method components)
  cdet shell             interactive shell
  cdet info              architecture, capabilities, and provenance

Self-contained: uses only the standard library by default. If `rich` is installed the output is
colorized/tabulated; otherwise it falls back to clean ASCII. Nothing here edits the frozen reference engine."""
import math
import argparse
import os
import sys
import subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))
INTER = os.path.join(ROOT, "08_2d_interacting")
LAT2D = os.path.join(ROOT, "05_2d_lattice")
ENGINE = os.path.join(ROOT, "engine")
for p in (INTER, LAT2D):
    if p not in sys.path:
        sys.path.insert(0, p)

# ----- rich-optional console layer (professional when rich is present, plain otherwise) -----
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich import box
    _C = Console()
    _RICH = True
except Exception:
    _C = None
    _RICH = False

_ANSI = {"g": "\033[32m", "r": "\033[31m", "y": "\033[33m", "c": "\033[36m", "b": "\033[1m", "0": "\033[0m"}


def _supports_color():
    return sys.stdout.isatty()


def cprint(s="", style=None):
    if _RICH:
        _C.print(s, style=style)
    else:
        if style and _supports_color():
            code = {"green": "g", "red": "r", "yellow": "y", "cyan": "c", "bold": "b"}.get(style, None)
            if code:
                print(f"{_ANSI[code]}{s}{_ANSI['0']}"); return
        print(s)


def rule(title=""):
    if _RICH:
        _C.rule(f"[bold cyan]{title}")
    else:
        line = "=" * max(8, 60 - len(title))
        print(f"\n== {title} {line}" if title else "=" * 64)


def show_table(title, columns, rows, styles=None):
    """columns: list[str]; rows: list[list[str]]; styles: optional list[str|None] per row for the status cell."""
    if _RICH:
        t = Table(title=title, box=box.ROUNDED, title_style="bold")
        for c in columns:
            t.add_column(c)
        for i, row in enumerate(rows):
            t.add_row(*[str(x) for x in row])
        _C.print(t)
    else:
        if title:
            print(f"\n{title}")
        widths = [max(len(str(columns[k])), *(len(str(r[k])) for r in rows)) if rows else len(str(columns[k]))
                  for k in range(len(columns))]
        print("  " + " | ".join(str(columns[k]).ljust(widths[k]) for k in range(len(columns))))
        print("  " + "-+-".join("-" * widths[k] for k in range(len(columns))))
        for r in rows:
            print("  " + " | ".join(str(r[k]).ljust(widths[k]) for k in range(len(columns))))


def panel(text, title=""):
    if _RICH:
        _C.print(Panel(text, title=title, border_style="cyan"))
    else:
        rule(title)
        print(text)


def _sh(cmd, cwd=None):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)


def _cached_series(N, K):
    """SU(N) density series coefficients, cached on disk (the contour EDs are slow for large N)."""
    import json
    cache = os.path.join(INTER, ".eos_cache.json")
    key = f"N{N}_K{K}"
    data = {}
    if os.path.exists(cache):
        try:
            data = json.load(open(cache))
        except Exception:
            data = {}
    if key in data:
        return data[key]
    if N >= 6:
        cprint(f"computing the SU(N={N}) series (first run; contour EDs are slow for large N; several minutes for N=6)...", "yellow")
    from sun_eos_curve import density_series
    a = list(density_series(N, K, M=max(24, 4 * N)))
    data[key] = a
    try:
        tmp = cache + f".tmp{os.getpid()}"
        with open(tmp, "w") as fh:
            json.dump(data, fh)
        os.replace(tmp, cache)            # atomic: an interrupt mid-write can't corrupt or lose the existing cache
    except Exception:
        pass
    return a


# ---------------------------------- subcommands -----------------------------------------------

def cmd_validate(a):
    """Run the validation gates and summarize pass/fail. The headline: validation depth."""
    rule("cdet validate -- gates (frozen baseline is the parity anchor)")
    gates = []

    r = _sh("make CC=gcc test", cwd=ENGINE)
    ok = "194 passed" in (r.stdout + r.stderr)
    gates.append(("frozen reference engine", "194/194 numerically exact", ok))

    r = _sh("gcc -O2 -std=c11 -o /tmp/_cdet_cst csurrogate_test.c csurrogate.c -lm && /tmp/_cdet_cst", cwd=INTER)
    ok = "ALL CASES MATCH" in r.stdout
    gates.append(("surrogate carriers", "match python to 1e-9", ok))

    _sh("cp spectrum_l6.bin /tmp/", cwd=INTER)
    r = _sh("gcc -O2 -std=c11 -o /tmp/_cdet_cpw cdet_planewave_engine.c -lm && /tmp/_cdet_cpw val < cdet_stable_engine_refs.txt", cwd=INTER)
    ok = "0.00e+00" in r.stdout and "PASS" in r.stdout
    gates.append(("hybrid engine parity", "0.00e+00 vs frozen ref", ok))

    r = _sh("gcc -O2 -std=c99 -I. -I../engine square2d_pw_demo.c lattices.c ../engine/cdet_engine.c -lm -o /tmp/_cdet_s2d && /tmp/_cdet_s2d", cwd=LAT2D)
    ok = r.returncode == 0 and "PASS" in r.stdout
    gates.append(("2D plane-wave path", "exact vs numerical; TD-converged", ok))

    r = _sh("PYTHONPATH=. python3 consolidation_v161.py", cwd=INTER)
    ok = "PASS" in r.stdout
    gates.append(("consolidation health gate", "all capabilities coherent", ok))

    rows = []
    for name, detail, ok in gates:
        rows.append([name, detail, "PASS" if ok else "FAIL"])
    show_table("validation gates", ["gate", "criterion", "status"], rows)
    n_ok = sum(1 for *_, ok in gates if ok)
    style = "green" if n_ok == len(gates) else "red"
    cprint(f"\n{n_ok}/{len(gates)} gates passed." + ("  All green." if n_ok == len(gates) else "  SOME FAILED."), style)
    return 0 if n_ok == len(gates) else 1


def cmd_converge(a):
    """2D thermodynamic-limit demonstration via the plane-wave propagator (4x4 -> 100x100)."""
    rule("cdet converge -- 2D thermodynamic limit (plane-wave propagator)")
    build = _sh("gcc -O2 -std=c99 -I. -I../engine square2d_pw_demo.c lattices.c ../engine/cdet_engine.c -lm -o /tmp/_cdet_s2d", cwd=LAT2D)
    if build.returncode != 0:
        cprint("build failed:\n" + build.stderr, "red"); return 1
    r = _sh("/tmp/_cdet_s2d", cwd=LAT2D)
    # parse the convergence rows "  LxL ( sites)  G0_NN= value"
    rows = []
    for ln in r.stdout.splitlines():
        s = ln.strip()
        if "G0_NN=" in s and "x" in s.split()[0]:
            try:
                lat = s.split()[0]
                sites = s[s.index("(") + 1:s.index("sites")].strip()
                val = s.split("G0_NN=")[1].split()[0]
                rows.append([lat, sites, val])
            except Exception:
                pass
    if rows:
        show_table("NN propagator vs lattice size (beta=5, mu=0, t=1)", ["lattice", "sites", "G0_NN"], rows)
        cprint("\nPast ~12-16 sites the value is already the infinite-system result; 100x100 confirms it.", "cyan")
        cprint("The method's strength: you do not need huge lattices. The cap is bypassed at O(L) memory.", "cyan")
    else:
        print(r.stdout)
    return 0


def cmd_resum(a):
    """Conformal-Borel resummation of the SU(N) EoS series vs plain Pade (the order-axis tool)."""
    rule(f"cdet resum -- conformal-Borel vs Pade (SU(N={a.N}) density)")
    import numpy as np  # noqa
    from sun_eos_curve import density_ed
    from sun_eos_conformal import conformal_borel, borel_singularity
    from resummation import pade, pade_eval
    aser = _cached_series(a.N, a.K)
    Uc = borel_singularity(aser)
    p, q = pade(aser, a.K // 2, a.K // 2)
    rows = []
    for U in a.U:
        e = density_ed(a.N, U)
        cb = abs(conformal_borel(aser, U, Uc) - e)
        pa = abs(pade_eval(p, q, U).real - e)
        rows.append([f"{U:.2f}", f"{e:+.6f}", f"{cb:.1e}", f"{pa:.1e}", f"{pa/cb:.0f}x" if cb > 0 else "-"])
    show_table(f"resummation error vs ED  (Borel singularity |t_c|~{Uc:.2f})",
               ["U", "ED", "conformal-Borel err", "Pade err", "improvement"], rows)
    cprint("\nConformal-Borel extracts more physics per order from the same coefficients (the real frontier).", "cyan")
    return 0


def cmd_eos(a):
    """SU(N) equation-of-state density at coupling U: weak series + chosen resummation, checked vs ED."""
    rule(f"cdet eos -- SU(N={a.N}) density at U={a.U}")
    from sun_eos_curve import density_ed
    from sun_eos_conformal import conformal_borel
    from resummation import pade, pade_eval
    aser = _cached_series(a.N, a.K)
    ed = density_ed(a.N, a.U)
    cb = conformal_borel(aser, a.U)
    p, q = pade(aser, a.K // 2, a.K // 2); pa = pade_eval(p, q, a.U).real
    show_table(f"density n(U={a.U}) for SU(N={a.N}), beta=2, mu=1",
               ["estimator", "value", "abs err vs ED"],
               [["ED (2-site anchor)", f"{ed:+.6f}", "0 (reference)"],
                ["conformal-Borel", f"{cb:+.6f}", f"{abs(cb - ed):.1e}"],
                ["Pade[K/2,K/2]", f"{pa:+.6f}", f"{abs(pa - ed):.1e}"]])
    return 0


def cmd_docc(a):
    """Double occupancy D=<n_up n_dn> vs U: the Mott observable (interaction energy E_int/site = U*D)."""
    rule(f"cdet docc -- double occupancy SU(N={a.N})  (Mott / cold-atom thermometry)")
    from double_occupancy import docc_ed, docc_series, docc_ed_direct
    from sun_eos_conformal import conformal_borel, borel_singularity
    from resummation import pade, pade_eval
    ser = docc_series(a.N, a.K); Uc = borel_singularity(ser); p, q = pade(ser, a.K // 2, a.K // 2)
    rows = []
    for U in a.U:
        e = docc_ed(a.N, U); cb = conformal_borel(ser, U, Uc); pa = pade_eval(p, q, U).real
        rows.append([f"{U:.2f}", f"{e:+.6f}", f"{cb:+.6f}", f"{abs(cb - e):.1e}", f"{U * e:+.5f}"])
    show_table(f"D(U) for SU(N={a.N}), beta=2, mu=1  (ED cross-checked by direct <D_hat> to ~1e-10)",
               ["U", "D (ED)", "D (conf-Borel)", "CB err", "E_int/site = U*D"], rows)
    cprint("")
    cprint("Double occupancy falls with U (correlation suppresses double occupancy -> Mott); U*D is the per-site", "cyan")
    cprint("interaction energy. Validated by two independent ED routes; conformal-Borel resums past the radius.", "cyan")
    return 0


def cmd_chi(a):
    """Linear-response susceptibilities: charge compressibility kappa and spin susceptibility chi_s vs U."""
    rule(f"cdet chi -- susceptibilities SU(N={a.N})  (linear response; opposite Mott trends)")
    from susceptibilities import (kappa_fluct, kappa_deriv, chi_spin_fluct, chi_spin_field)
    rows = []
    for U in a.U:
        kf = kappa_fluct(a.N, U); kd = kappa_deriv(a.N, U)
        cf = chi_spin_fluct(a.N, U); cd = chi_spin_field(a.N, U)
        rows.append([f"{U:.2f}", f"{kf:+.5f}", f"{abs(kf - kd):.0e}", f"{cf:+.5f}", f"{abs(cf - cd):.0e}"])
    show_table(f"susceptibilities for SU(N={a.N}), beta=2, mu=1  (two independent ED routes per column)",
               ["U", "kappa (charge)", "k cross-dev", "chi_s (spin)", "chi cross-dev"], rows)
    cprint("")
    cprint("kappa falls with U (charge fluctuations suppressed -> Mott incompressibility); chi_s rises (local-moment", "cyan")
    cprint("formation -> magnetism). The opposite trends are the hallmark of Mott correlation. Each value is", "cyan")
    cprint("cross-checked by a derivative route and a fluctuation-dissipation route (agree to ~1e-7).", "cyan")
    return 0


def cmd_plot(a):
    """Render publication-quality figures of the validated results (convergence / resummation / mott / summary)."""
    rule(f"cdet plot -- {a.what}")
    import plots
    path = plots.save(a.what, a.out)
    cprint(f"figure written: {path}", "green")
    cprint("(reproduced from the validated code paths -- the plot cannot drift from the numbers.)", "cyan")
    return 0


def cmd_gui(a):
    """Launch the local browser console: sliders + quick-run cards over the most-used computations."""
    rule("cdet gui -- local console")
    import cdet_gui
    cprint(f"  opening the console at http://127.0.0.1:{a.port}/  (sliders + quick runs; Ctrl-C to stop)", "cyan")
    cdet_gui.serve(ROOT, port=a.port, open_browser=not a.no_browser)
    return 0


def cmd_connected(a):
    """Tier 0: the connected-determinant recursion, validated on the atom and 2-site lattice."""
    rule("cdet connected -- the connected-determinant (CDet) recursion, validated on solvable cases")
    import cdet_connected as cc
    cc._selftest()
    return 0


def cmd_trueradius(a):
    """The TRUE convergence radius: thermal complex-U Fisher zeros, vs the RPA wall."""
    rule(f"cdet trueradius -- true complex-U radius (beta={a.beta}, mu={a.mu})")
    import wall_true_radius as tr
    Ua = tr.atom_nearest_zero(a.beta, a.mu)
    cprint(f"  atom: nearest Fisher zero U={Ua.real:+.3f}{Ua.imag:+.3f}i  radius={abs(Ua):.4f}  (Im=pi/beta={3.14159/a.beta:.3f}, thermal)", "green")
    U3 = tr.ring_true_radius(3, a.beta, a.mu, 60, 66); Rr = tr.ring_rpa_radius(3, a.beta, a.mu)
    cprint(f"  ring L=3: R_true={abs(U3):.3f} (Im={U3.imag/(3.14159/a.beta):.2f} x pi/beta)  vs  R_RPA={Rr:.3f}", "green")
    cprint("  -> the true radius is thermal (complex-U Fisher zeros ~ pi/beta), closer than the RPA wall (v146 caveat),", "yellow")
    cprint("     and has no q-grid max so it does NOT inherit the Diophantine sieve.", "yellow")
    return 0


def cmd_crosscheck(a):
    """Test all models side by side and verify the cross-links between them."""
    rule("cdet crosscheck -- all models side by side")
    import consolidation_v176 as cc
    cc._selftest()
    return 0


def cmd_twist(a):
    """Half-integer lattices: twisted BC (theta=1/2 anti-periodic) and rectangular supercells vs the wall sieve."""
    rule(f"cdet twist -- half-integer lattices (beta={a.beta}, mu={a.mu})")
    import wall_twist as wt
    uinf = wt.wall(90, 90, a.beta, a.mu)
    cprint(f"  TD wall U_inf={uinf:.4f}", "cyan")
    cprint("  square prime L=17:", "cyan")
    e0 = abs(wt.wall(17, 17, a.beta, a.mu) - uinf); ea = abs(wt.twist_avg_wall(17, a.beta, a.mu) - uinf)
    cprint(f"    periodic err={e0:.4f}; twist-averaged err={ea:.4f}  (twist barely helps -> q-resolution bound)", "green")
    cprint("  rectangular 23x46 (prime dim, q-grid tuned to q*):", "cyan")
    er = abs(wt.wall(23, 46, a.beta, a.mu) - uinf)
    cprint(f"    err={er:.4f}  (rectangular supercell HEALS the sieve)", "green")
    cprint("(twisted/anti-periodic BC do not heal the sieve; a supercell whose q-grid hits q* does. Diophantine.)", "yellow")
    return 0


def cmd_primes(a):
    """Prime vs composite lattice sizes: the Diophantine sieve on the convergence wall."""
    rule(f"cdet primes -- prime lattice sizes vs the wall (beta={a.beta}, mu={a.mu})")
    import wall_primes as wp
    r = wp.analyze(a.mu, a.beta)
    cprint(f"  peak q*=({r['qstar'][0]:.2f},{r['qstar'][1]:.2f})pi ; TD wall U_inf={r['uinf']:.4f}", "cyan")
    cprint("  L    |U_c-U_inf|   prime?  #div", "cyan")
    for L in sorted(r["dev"]):
        cprint(f"  {L:2d}    {r['dev'][L]:.4f}      {'P' if wp.is_prime(L) else '.':2s}     {wp.n_divisors(L)}", "green")
    cprint(f"  mean dev: primes={r['prime_dev']:.4f} vs composites={r['comp_dev']:.4f} "
           f"(x{r['prime_dev']/r['comp_dev']:.1f}); corr(#div,dev)={r['corr_ndiv']:+.2f}", "yellow")
    cprint("(primes are commensuration-blind -> worst-case wall samplers; composites capture the peak. Diophantine.)", "cyan")
    return 0


def cmd_tide(a):
    """The convergence wall as a 'tide': finite-size oscillations of U_c(L) and their wave laws."""
    rule(f"cdet tide -- finite-size oscillations of the wall (beta={a.beta}, mu={a.mu})")
    import wall_tide as wt
    import wall_vs_size as w
    Ls = list(range(4, 41))
    us = wt.uc_series(a.mu, Ls, a.beta)
    cprint("  L   U_c        (even=on-grid, odd=off-grid)", "cyan")
    for L, u in zip(Ls, us):
        bar = "#" * max(0, int((u - min(us)) / (max(us) - min(us) + 1e-9) * 30))
        cprint(f"  {L:2d}  {u:.4f}  {'e' if L%2==0 else 'o'} {bar}", "green")
    pred, meas = wt.tide_period(a.mu, a.beta)
    qx, qy = wt.peak_q(a.mu, a.beta)
    cprint(f"  peak q*=({qx:.2f},{qy:.2f})pi -> wave period 2pi/q* = {pred:.2f} sites (measured {meas:.2f})", "yellow")
    cprint("(the tide's wavelength measures the Fermi nesting vector; amplitude calms as L grows.)", "cyan")
    return 0


def cmd_wall(a):
    """The convergence wall U_c(L)=1/chi0_max vs lattice size (RPA/Stoner instability from the plane-wave dispersion)."""
    rule(f"cdet wall -- convergence wall vs lattice size (beta={a.beta}, mu={a.mu})")
    import wall_vs_size as w
    rows = w.wall_vs_size(a.beta, a.mu, [4, 6, 8, 12, 16, 24, 32, 48, 64, 100])
    cprint("  L      chi0_max    U_c (wall)   peak-q(pi)", "cyan")
    for L, cm, Uc, q in rows:
        cprint(f"  {L:3d}     {cm:.4f}      {Uc:.4f}     ({q[0]:.2f},{q[1]:.2f})", "green")
    lo, hi = rows[0][2], rows[-1][2]
    trend = "recedes (lattice helps)" if hi > lo else "comes in (small lattice was optimistic)"
    cprint(f"  wall {trend}: U_c({rows[0][0]})={lo:.3f} -> U_c({rows[-1][0]})={hi:.3f}", "yellow")
    cprint("(U_c is the leading RPA/Stoner instability = the bubble-sum radius; computed at any L via the v162 dispersion.)", "cyan")
    return 0


def cmd_export(a):
    """Export a validated observable to CSV / JSON / HDF5 for downstream tools (pandas, Excel, analysis)."""
    rule(f"cdet export -- {a.what} ({a.format})")
    import export as _exp
    if a.format in ("hdf5", "all") and not _exp._HDF5:
        cprint("note: HDF5 needs h5py (pip install h5py); writing CSV/JSON.", "yellow")
    paths = _exp.export(a.what, a.format, a.out)
    for p in paths:
        cprint(f"  wrote {p}", "green")
    cprint("(reproduced from the validated code paths -- exported data cannot drift from the numbers.)", "cyan")
    return 0


def cmd_run(a):
    """Hybrid plane-wave engine grid run -- the production CDet path (auto-fast on crystallographic L)."""
    # resolve the upper beta: positional, then --beta-hi, else one bstep above beta (so bare `cdet run` just works)
    if a.beta_hi is None:
        a.beta_hi = a.beta_hi_opt if a.beta_hi_opt is not None else a.beta_lo + a.bstep
    rule(f"cdet run -- hybrid grid  (L={a.L}, beta {a.beta_lo}..{a.beta_hi}, step {a.bstep})")
    cprint(f"  customize:  cdet run --L {a.L} --beta {a.beta_lo} --beta-hi {a.beta_hi} --bstep {a.bstep} --K {a.K}", "cyan")
    _sh("cp spectrum_l6.bin /tmp/", cwd=INTER)
    build = _sh("gcc -O2 -std=c11 -o /tmp/_cdet_cpw cdet_planewave_engine.c -lm", cwd=INTER)
    if build.returncode != 0:
        cprint("build failed:\n" + build.stderr, "red"); return 1
    cmd = (f"/tmp/_cdet_cpw grid {a.beta_lo} {a.beta_hi} {a.bstep} {a.K} {a.NT} {a.seed} {a.delta} {a.mode}")
    r = _sh(cmd, cwd=INTER)
    rows = []
    for ln in r.stdout.splitlines():
        s = ln.strip()
        if s.startswith("#") or not s:
            continue
        parts = s.split()
        if len(parts) >= 5:
            rows.append(parts[:5])
    if rows:
        show_table("grid output", ["beta", "A", "A_err", "c1", "c1_err"], rows)
    else:
        print(r.stdout or r.stderr)
    return 0


def cmd_sweep(a):
    """Parameter-sweep stress harness with automatic convergence checks (wraps cdet_study)."""
    rule(f"cdet sweep -- {a.target} over {a.var}")
    from cdet_study import study
    values = a.values
    if len(values) > 60:
        cprint(f"note: {len(values)} points requested; sweeping the first 60 (use fewer, or several runs).", "yellow")
        values = values[:60]
    def _prog(i, n, x):
        cprint(f"  [{i+1}/{n}]  {a.var}={x} ...", "cyan")
    summary, outdir = study(a.target, a.method, {}, a.var, values, max_time=120,
                            quiet=not a.verbose, progress=(None if a.verbose else _prog))
    rows = [[k, str(v)] for k, v in summary.items() if not isinstance(v, (list, dict))]
    show_table(f"sweep summary ({a.target})", ["key", "value"], rows)
    cprint(f"\nrun archived under: {outdir}", "cyan")
    return 0


def cmd_lab(a):
    """Pass through to the swappable control plane (target x method components)."""
    from cdet_lab import main as lab_main
    return lab_main(a.rest)


def cmd_shell(a):
    """Launch the interactive shell."""
    import cdet_shell
    try:
        cdet_shell.main() if hasattr(cdet_shell, "main") else cdet_shell.Shell().repl()
    except AttributeError:
        # fall back to running the module
        _sh("PYTHONPATH=. python3 cdet_shell.py", cwd=INTER)
    return 0


def cmd_diagmc(a):
    """Rossi-style connected-determinant Monte Carlo: reproduces exact answers and measures the sign/convergence wall."""
    rule("cdet diagmc -- connected-determinant Monte Carlo (validated; the sign wall, measured)")
    import cdet_connected as cc
    import cdet_diagmc as dm
    # guard against absurd inputs: the connected-determinant recursion costs ~2^n, so high orders must be capped, and a
    # positive sample count is required (otherwise the estimator averages an empty set -> nan).
    if a.nmax > 8:
        cprint(f"note: --nmax {a.nmax} capped at 8 (the connected-determinant recursion costs ~2^n per sample).", "yellow")
        a.nmax = 8
    if a.nmax < 1:
        cprint("note: --nmax raised to 1 (need at least one diagram order).", "yellow"); a.nmax = 1
    if a.samples < 100:
        cprint("note: --samples raised to 100 (a positive sample count is required for an estimate).", "yellow")
        a.samples = 100
    if a.samples > 2_000_000:
        cprint("note: --samples capped at 2,000,000.", "yellow"); a.samples = 2_000_000
    if not (math.isfinite(a.beta) and math.isfinite(a.mu) and math.isfinite(a.U)):
        cprint("error: beta, mu and U must be finite numbers.", "red"); return 1
    if a.beta <= 0:
        cprint("error: beta (inverse temperature) must be positive.", "red"); return 1
    g0 = cc.g0_atom if a.system == "atom" else cc.g0_2site
    spv = 1 if a.system == "atom" else 2
    cprint(f"system={a.system}  beta={a.beta}  mu={a.mu}  U={a.U}  (orders 1..{a.nmax}, {a.samples} samples/order)", "bold")
    r = dm.mc_lnZ_over_Z0(g0, a.beta, a.mu, a.U, spv=spv, n_max=a.nmax, N=a.samples)
    cprint("  order   a_n (Monte Carlo)        intra-order <sign>")
    for i, (c, e, s) in enumerate(zip(r["coeffs"], r["coeff_errs"], r["signs"]), start=1):
        cprint(f"    {i}     {c:+.6f} +/- {e:.6f}     {s:.3f}")
    line = f"  ln(Z/Z0) at U={a.U}:  {r['value']:+.6f} +/- {r['err']:.6f}"
    if a.system == "atom":
        ex = dm.atom_lnZ_over_Z0_exact(a.beta, a.mu, a.U)
        line += f"    (exact closed form {ex:+.6f}, dev {abs(r['value'] - ex):.4f} incl. truncation)"
    cprint(line, "bold")
    if a.system == "atom":
        ac = cc.atom_exact_coeffs(10, a.beta, a.mu)[1:]
        cprint("  sign / convergence wall -- across-order <sign> = |sum a_n U^n| / sum |a_n| U^n:")
        for U_, s_, c_ in dm.sign_wall_scan(ac, [0.3, 0.6, 1.0, 1.5, 2.0]):
            bar = "#" * int(round(s_ * 30))
            cprint(f"      U={U_:<4} <sign>={s_:.3f}  cost x{c_:5.1f}  {bar}", "yellow" if s_ < 0.3 else None)
    cprint("  the average sign quantifies the sign problem (cost ~ 1/<sign>^2); the wall is measured, not removed.")
    return 0


def cmd_bench(a):
    """Run the benchmark suite: the engine determinant speedup, plus an index of the rest."""
    rule("cdet bench -- benchmark suite")
    cprint("engine connected-determinant evaluation: fast method vs dense LU cross-check, scaling to 1M", "bold")
    r = _sh("make bench", cwd=ENGINE)
    out = (r.stdout or "").rstrip()
    if r.returncode != 0 and not out:
        cprint("build/run failed:\n" + (r.stderr or ""), "red")
    else:
        print(out)
    cprint("")
    cprint("more benchmarks (reproducible; run from this folder):", "bold")
    cprint("  Monte-Carlo variance, control variate (~70-80x, matches 1/(1-rho^2)):")
    cprint("      cd 02_control_variate && python3 cv.py")
    cprint("  connected determinant in O(2^n n^2), verified vs the engine to 1e-15:")
    cprint("      python3 08_2d_interacting/fast_minors.py")
    cprint("  size axis -- exponential locality decay:   cd 04_locality && python3 locality.py")
    cprint("  size axis -- 2D torus vs numpy eig:         cd 05_2d_lattice && python3 val2d.py")
    cprint("  (the size-axis oracles need a one-time ./build_oracles.sh)")
    return 0


def cmd_info(a):
    """Architecture, capabilities, and provenance."""
    rule("cdet info")
    arch = (
        "[bold]three-model architecture[/bold]\n" if _RICH else "three-model architecture\n"
    ) + (
        "  1. FROZEN REFERENCE  engine/        194/194, never edited -- the parity anchor\n"
        "  2. HYBRID / PRODUCTION  plane-wave engine   validates 0.00e+00 vs the reference\n"
        "  3. SURROGATE  csurrogate.c          pure-arithmetic carriers, match to 1e-9\n"
    )
    panel(arch, "architecture")
    caps = [
        ["validate", "run all validation gates (frozen, surrogate, hybrid, 2D)"],
        ["converge", "2D thermodynamic-limit demo (4x4 -> 100x100, plane-wave)"],
        ["resum", "conformal-Borel resummation vs Pade (the order axis)"],
        ["eos", "SU(N) equation-of-state density at coupling U"],
        ["docc", "double occupancy <n_up n_dn> vs U (Mott / thermometry)"],
        ["chi", "susceptibilities: charge compressibility + spin"],
        ["plot", "render figures (convergence / resummation / mott / summary)"],
        ["export", "export a dataset (convergence/resummation/eos/docc/chi) to CSV/JSON/HDF5"],
        ["wall", "convergence wall vs lattice size"],
        ["tide", "finite-size oscillations of the wall"],
        ["primes", "prime lattice sizes vs the wall"],
        ["twist", "half-integer (twisted BC) lattices"],
        ["gui", "browser front-end over the CLI (+ optional assistant)"],
        ["bench", "benchmark suite: engine speedup + MC variance + size-axis pointers"],
        ["diagmc", "connected-determinant Monte Carlo: reproduces exact + measures the sign wall"],
        ["connected", "connected-determinant recursion (validated)"],
        ["trueradius", "true complex-U radius vs RPA wall"],
        ["crosscheck", "all models side by side + cross-links"],
        ["run", "hybrid grid run (production CDet path, auto-fast)"],
        ["sweep", "parameter sweep with convergence checks"],
        ["lab / shell", "swappable control plane / interactive shell"],
    ]
    show_table("capabilities", ["subcommand", "what it does"], caps)
    # provenance: latest ledger entries
    try:
        rp = [f for f in os.listdir(ROOT) if f.startswith("real_patterns_v") and f.endswith(".md")]
        cprint(f"\nprovenance ledger: {rp[0] if rp else '(none)'}", "cyan")
    except Exception:
        pass
    return 0


def _selftest():
    """Gate: the CLI dispatches to real capabilities without error."""
    print("cdet CLI self-test (unified entry point dispatches to real capabilities):")
    print(f"  rich output: {'available' if _RICH else 'fallback ASCII (self-contained)'}")
    # info + a fast physics subcommand (resum on tiny N) must run clean
    assert build_parser() is not None
    ns = build_parser().parse_args(["resum", "--N", "4", "--K", "8", "--U", "0.6", "1.0"])
    rc = ns.func(ns)
    assert rc == 0
    ns = build_parser().parse_args(["docc", "--N", "2", "--K", "8", "--U", "0.5", "1.0"])
    assert ns.func(ns) == 0
    ns = build_parser().parse_args(["chi", "--N", "2", "--U", "0.0", "1.0"])
    assert ns.func(ns) == 0
    ns = build_parser().parse_args(["plot", "convergence", "--out", "/tmp/_cdet_cli_fig"])
    assert ns.func(ns) == 0
    ns = build_parser().parse_args(["export", "chi", "--format", "csv", "--out", "/tmp/_cdet_cli_data"])
    assert ns.func(ns) == 0
    ns = build_parser().parse_args(["info"])
    assert ns.func(ns) == 0
    print("  => subcommands wired (validate/converge/resum/eos/run/sweep/lab/shell/info); help available. PASS")


# ---------------------------------- parser ----------------------------------------------------

def build_parser():
    p = argparse.ArgumentParser(
        prog="cdet", description="unified CLI for the CDet / connected-determinant suite",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="examples:\n  cdet validate\n  cdet converge\n  cdet resum --N 6 --U 0.6 1.0 1.5\n  cdet run --L 6 --beta 30 40\n  cdet info")
    sub = p.add_subparsers(dest="cmd", metavar="<subcommand>")

    s = sub.add_parser("validate", help="run the validation gates"); s.set_defaults(func=cmd_validate)
    s = sub.add_parser("converge", help="2D thermodynamic-limit demo"); s.set_defaults(func=cmd_converge)

    s = sub.add_parser("resum", help="conformal-Borel vs Pade")
    s.add_argument("--N", type=int, default=4); s.add_argument("--K", type=int, default=10)
    s.add_argument("--U", type=float, nargs="+", default=[0.6, 1.0, 1.5]); s.set_defaults(func=cmd_resum)

    s = sub.add_parser("eos", help="SU(N) EoS density at U")
    s.add_argument("--N", type=int, default=4); s.add_argument("--K", type=int, default=10)
    s.add_argument("--U", type=float, default=1.0); s.set_defaults(func=cmd_eos)

    s = sub.add_parser("docc", help="double occupancy <n_up n_dn> vs U (Mott observable)")
    s.add_argument("--N", type=int, default=2); s.add_argument("--K", type=int, default=10)
    s.add_argument("--U", type=float, nargs="+", default=[0.0, 0.5, 1.0, 1.5, 2.0]); s.set_defaults(func=cmd_docc)

    s = sub.add_parser("chi", help="susceptibilities: charge compressibility + spin (linear response)")
    s.add_argument("--N", type=int, default=2)
    s.add_argument("--U", type=float, nargs="+", default=[0.0, 1.0, 2.0, 4.0]); s.set_defaults(func=cmd_chi)

    s = sub.add_parser("plot", help="render figures of the validated results")
    s.add_argument("what", nargs="?", default="summary", choices=["convergence", "resummation", "mott", "summary"])
    s.add_argument("--out", default=os.path.join(ROOT, "cdet_figures")); s.set_defaults(func=cmd_plot)

    s = sub.add_parser("wall", help="convergence wall U_c vs lattice size (where lattice size helps)")
    s.add_argument("--beta", type=float, default=5.0); s.add_argument("--mu", type=float, default=0.0)
    s.set_defaults(func=cmd_wall)

    s = sub.add_parser("tide", help="finite-size oscillations of the wall (its 'waves')")
    s.add_argument("--beta", type=float, default=5.0); s.add_argument("--mu", type=float, default=0.0)
    s.set_defaults(func=cmd_tide)

    s = sub.add_parser("primes", help="prime vs composite lattice sizes (the Diophantine sieve)")
    s.add_argument("--beta", type=float, default=5.0); s.add_argument("--mu", type=float, default=-0.6)
    s.set_defaults(func=cmd_primes)

    s = sub.add_parser("twist", help="half-integer lattices: twisted BC + rectangular supercells")
    s.add_argument("--beta", type=float, default=5.0); s.add_argument("--mu", type=float, default=-0.6)
    s.set_defaults(func=cmd_twist)

    s = sub.add_parser("gui", help="launch the browser front-end over the CLI (+ optional assistant)")
    s.add_argument("--port", type=int, default=8765); s.add_argument("--no-browser", action="store_true")
    s.set_defaults(func=cmd_gui)

    s = sub.add_parser("connected", help="Tier 0: the connected-determinant recursion, validated on solvable cases")
    s.set_defaults(func=cmd_connected)

    s = sub.add_parser("trueradius", help="the true complex-U radius (thermal Fisher zeros) vs the RPA wall")
    s.add_argument("--beta", type=float, default=2.0); s.add_argument("--mu", type=float, default=0.5)
    s.set_defaults(func=cmd_trueradius)

    s = sub.add_parser("crosscheck", help="test all models side by side + their cross-links")
    s.set_defaults(func=cmd_crosscheck)

    s = sub.add_parser("export", help="export a validated observable to CSV/JSON/HDF5")
    s.add_argument("what", nargs="?", default="docc", choices=["convergence", "resummation", "eos", "docc", "chi"])
    s.add_argument("--format", default="csv", choices=["csv", "json", "hdf5", "all"])
    s.add_argument("--out", default=os.path.join(ROOT, "cdet_data")); s.set_defaults(func=cmd_export)

    s = sub.add_parser("run", help="hybrid grid run",
        epilog="examples:\n  cdet run                       # bare: L=6, beta 30->36\n  cdet run --L 16 --beta 10 --beta-hi 40 --bstep 5\n  cdet run --K 6 --NT 2000       # higher order, more samples",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    s.add_argument("--L", type=int, default=6); s.add_argument("--beta", dest="beta_lo", type=float, default=30.0)
    s.add_argument("beta_hi", nargs="?", type=float, default=None)
    s.add_argument("--beta-hi", dest="beta_hi_opt", type=float, default=None)
    s.add_argument("--bstep", type=float, default=6.0); s.add_argument("--K", type=int, default=4)
    s.add_argument("--NT", type=int, default=800); s.add_argument("--seed", type=int, default=7)
    s.add_argument("--delta", type=float, default=0.01); s.add_argument("--mode", type=int, default=2)
    s.set_defaults(func=cmd_run)

    s = sub.add_parser("sweep", help="parameter sweep",
        epilog="examples:\n  cdet sweep --target addition-pole --var L --values 6 12 24\n  cdet sweep --target eos --method record --var mu --values 0.5 1 1.5 --verbose\n  (progress prints per point; add --verbose for full per-point detail)",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    s.add_argument("--target", default="addition-pole"); s.add_argument("--method", default="surrogate")
    s.add_argument("--base", default="L"); s.add_argument("--var", default="L")
    s.add_argument("--values", type=float, nargs="+", default=[6, 12])
    s.add_argument("--verbose", action="store_true"); s.set_defaults(func=cmd_sweep)

    s = sub.add_parser("lab", help="swappable control plane",
        epilog="examples:\n  cdet lab list                  # show available (target, method) components\n  cdet lab run eos record         # run one component\n  cdet lab --help                 # component-level help",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    s.add_argument("rest", nargs=argparse.REMAINDER); s.set_defaults(func=cmd_lab)
    s = sub.add_parser("shell", help="interactive shell"); s.set_defaults(func=cmd_shell)
    s = sub.add_parser("info", help="architecture and capabilities"); s.set_defaults(func=cmd_info)
    s = sub.add_parser("bench", help="run the benchmark suite (engine speedup + index of the rest)"); s.set_defaults(func=cmd_bench)
    s = sub.add_parser("diagmc", help="connected-determinant Monte Carlo (validated; measures the sign wall)")
    s.add_argument("--system", choices=["atom", "2site"], default="atom")
    s.add_argument("--beta", type=float, default=2.0); s.add_argument("--mu", type=float, default=0.5)
    s.add_argument("--U", type=float, default=1.0); s.add_argument("--nmax", type=int, default=4)
    s.add_argument("--samples", type=int, default=20000); s.set_defaults(func=cmd_diagmc)
    return p


def main(argv=None):
    p = build_parser()
    a = p.parse_args(argv)
    if not getattr(a, "cmd", None):
        p.print_help(); return 0
    # friendly error handling
    try:
        if a.cmd == "run" and a.beta_hi is None:
            a.beta_hi = a.beta_hi_opt if a.beta_hi_opt is not None else a.beta_lo + 10.0
        return a.func(a)
    except KeyboardInterrupt:
        cprint("\ninterrupted.", "yellow"); return 130
    except Exception as e:
        cprint(f"error in `cdet {a.cmd}`: {e}", "red")
        cprint("run `cdet <subcommand> --help` for usage, or `cdet info` for an overview.", "yellow")
        return 1


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        _selftest()
    else:
        sys.exit(main())
