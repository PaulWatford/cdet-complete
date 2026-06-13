#!/usr/bin/env python3
"""cdet_study.py (v151) -- the sweep / stress harness on top of cdet_lab.

Scan one parameter for a chosen (target, method), collect data, detect convergence or accuracy breakdown, stop on
user-defined cutoffs (wall-time budget OR accuracy drop), and emit a log + data + a graph with the points of
interest marked. Everything routes through the same evaluators the control plane uses, so the frozen reference
stays the anchor.

WHAT YOU CAN STUDY (sweep variable in {U, N, L, beta, mu, n}):
  - convergence:   addition-pole vs L      -> converges to z(inf); the harness reports the L where it settles.
  - accuracy drop: self-energy diagrammatic vs ED across U -> error blows up past the series radius (~pi/beta);
                   set --accuracy-cutoff to stop exactly where the cheap method stops being trustworthy.
  - cost / time:   connected-det vs n      -> cost grows; set --max-time to stop within a wall-clock budget.

CUTOFFS (either or both):
  --max-time T          stop once cumulative wall time exceeds T seconds.
  --accuracy-cutoff EPS  stop once the error vs the reference exceeds EPS (only for methods that have a reference).
  --conv-tol TOL        declare convergence when |delta y| < TOL for a few consecutive steps (default off).

OUTPUTS (written to ./cdet_runs/<stamp>_<target>_<var>/):
  data.csv      x, y, error, step_seconds, elapsed_seconds
  summary.json  the config, the stop reason, and every point of interest
  plot.png      y vs x with convergence / breakdown / cutoff markers (needs matplotlib; falls back gracefully)
  run.log       timestamped per-step log ending in a highlighted summary
  and an ASCII plot printed to the terminal (always, so it works headless).

Run:    python3 cdet_study.py --target self-energy --method diagrammatic --sweep U --range 0.1:1.2:0.1 \
                              --beta 5 --mu 1 --accuracy-cutoff 1e-3
Self-test:  python3 cdet_study.py --selftest
"""
import argparse, os, sys, json, time, math, datetime
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def evaluate(target, method, p):
    """Return (y, error_or_None) for one parameter point. error is vs the natural reference, when one exists."""
    beta = p.get("beta", 5.0); mu = p.get("mu", 1.0); U = p.get("U", 1.0)
    iwn = 1j * math.pi / beta
    if target == "self-energy":
        from self_energy_diagrammatic import _G_matsubara_of_U
        from hubbard_ed import hop_1d_ring
        hop = np.zeros((1, 1)) if p.get("model", "atom") == "atom" else hop_1d_ring(2, t=p.get("t", 1.0))
        S_ed = (iwn + mu) - 1.0 / _G_matsubara_of_U(hop, mu, beta, iwn, U)
        if method == "ed":
            return abs(S_ed), None
        if method == "hubbard-i":
            x = math.exp(beta * mu); Z = 1 + 2 * x + x * x * math.exp(-beta * U)
            n = (x + x * x * math.exp(-beta * U)) / Z
            S = U * n + U**2 * n * (1 - n) / (iwn + mu - U * (1 - n))
            return abs(S), None
        if method == "diagrammatic":
            from self_energy_irreducible import connected_g_coeffs, sigma_coeffs_exact
            sig = sigma_coeffs_exact(connected_g_coeffs(iwn, beta, mu, 16))
            S = sum(sig[k] * U**k for k in range(1, 17))
            return abs(S), abs(S - S_ed)
    if target == "addition-pole":
        from physical_mapping import addition_pole
        return addition_pole(int(p.get("L", 12)), mu), None
    if target == "eos":
        from sun_lattice_production import n1_production, g0_amplitudes
        N = int(p.get("N", 6))
        d, _ = g0_amplitudes(mu); n_rec = d + U * n1_production(N, mu)
        if method == "ed":
            from sun_lattice_record import lnZ
            h = 1e-5
            n_ed = (lnZ(N, p.get("t", 1.0), mu + h, U, beta) - lnZ(N, p.get("t", 1.0), mu - h, U, beta)) / (2 * h) / (beta * N * 2)
            return n_ed, None
        return n_rec, abs(n_rec - _eos_ed(N, mu, U, beta, p.get("t", 1.0)))
    if target == "double-occ":
        x = math.exp(beta * mu); Z = 1 + 2 * x + x * x * math.exp(-beta * U)
        return x * x * math.exp(-beta * U) / Z, None
    if target == "connected-det":
        from fast_minors import all_principal_minors
        n = int(p.get("n", 5)); M = np.random.default_rng(0).standard_normal((n, n))
        det = all_principal_minors(M)[(1 << n) - 1]
        return det, abs(det - np.linalg.det(M))
    raise ValueError(f"no evaluator for ({target}, {method})")


def _eos_ed(N, mu, U, beta, t):
    from sun_lattice_record import lnZ
    h = 1e-5
    return (lnZ(N, t, mu + h, U, beta) - lnZ(N, t, mu - h, U, beta)) / (2 * h) / (beta * N * 2)


def frange(spec):
    """parse 'lo:hi:step' -> list of floats (inclusive of hi within fp tolerance)."""
    lo, hi, step = (float(x) for x in spec.split(":"))
    n = int(round((hi - lo) / step)) + 1
    return [round(lo + i * step, 10) for i in range(n)]


def ascii_plot(xs, ys, poi=None, width=56, height=16):
    """compact terminal scatter; poi = {x: 'label-char'} marks points of interest."""
    poi = poi or {}
    if not ys:
        return "(no data)"
    ymin, ymax = min(ys), max(ys)
    if ymax == ymin:
        ymax = ymin + 1e-12
    xmin, xmax = min(xs), max(xs)
    span = (xmax - xmin) or 1e-12
    grid = [[" "] * width for _ in range(height)]
    for x, y in zip(xs, ys):
        c = int((x - xmin) / span * (width - 1))
        r = height - 1 - int((y - ymin) / (ymax - ymin) * (height - 1))
        grid[r][c] = "*" if grid[r][c] == " " else grid[r][c]
    for x, ch in poi.items():
        c = int((x - xmin) / span * (width - 1))
        for r in range(height):
            if grid[r][c] == "*":
                grid[r][c] = ch
                break
        else:
            grid[height - 1][c] = ch
    lines = [f"{ymax:>10.4g} |" + "".join(grid[0])]
    for r in range(1, height - 1):
        lines.append(" " * 10 + " |" + "".join(grid[r]))
    lines.append(f"{ymin:>10.4g} |" + "".join(grid[-1]))
    lines.append(" " * 11 + "+" + "-" * width)
    lines.append(" " * 12 + f"{xmin:<.4g}" + " " * (width - 8) + f"{xmax:.4g}")
    return "\n".join(lines)


def study(target, method, base, var, values, max_time=None, accuracy_eps=None, conv_tol=None, conv_k=3,
          outroot=None, quiet=False, progress=None):
    """Run the sweep; return the summary dict and the output directory."""
    stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    outdir = os.path.join(outroot or os.path.join(os.getcwd(), "cdet_runs"), f"{stamp}_{target}_{var}")
    os.makedirs(outdir, exist_ok=True)
    log = open(os.path.join(outdir, "run.log"), "w")

    def emit(msg):
        log.write(msg + "\n"); log.flush()
        if not quiet:
            print(msg)

    emit(f"# cdet_study  target={target} method={method} sweep={var}  ({len(values)} points)")
    emit(f"# base params: {base}")
    if max_time:
        emit(f"# cutoff: stop if cumulative time > {max_time}s")
    if accuracy_eps:
        emit(f"# cutoff: stop if error vs reference > {accuracy_eps:g}")
    rows, t0, prev, conv_run, poi = [], time.time(), None, 0, {}
    stop = "completed"
    # write data.csv incrementally (header first, flush each row) so an interrupted sweep keeps its computed points
    dataf = open(os.path.join(outdir, "data.csv"), "w")
    dataf.write("x,y,error,step_seconds,elapsed_seconds\n"); dataf.flush()
    try:
        for _i, x in enumerate(values):
            if progress is not None:
                progress(_i, len(values), x)
            p = {**base, var: (int(x) if var in ("N", "L", "n") else x)}
            ts = time.time()
            y, err = evaluate(target, method, p)
            dt = time.time() - ts
            el = time.time() - t0
            rows.append((x, y, err, dt, el))
            dataf.write(f"{x},{y},{'' if err is None else err},{dt},{el}\n"); dataf.flush()
            emit(f"  {var}={x:<8g} y={y:<+.8g}" + (f"  err={err:.2e}" if err is not None else "") +
                 f"  ({dt*1e3:.1f} ms, elapsed {el:.2f}s)")
            if conv_tol and prev is not None:
                conv_run = conv_run + 1 if abs(y - prev) < conv_tol else 0
                if conv_run >= conv_k and "converged" not in poi.values():
                    poi[x] = "c"; emit(f"  -> CONVERGED at {var}={x} (|delta|<{conv_tol:g} for {conv_k} steps)")
            prev = y
            if accuracy_eps is not None and err is not None and err > accuracy_eps:
                poi[x] = "x"; stop = f"accuracy drop: error {err:.2e} > {accuracy_eps:g} at {var}={x}"
                emit(f"  -> STOP: {stop}"); break
            if max_time is not None and el > max_time:
                poi[x] = "t"; stop = f"time budget {max_time}s exceeded at {var}={x}"
                emit(f"  -> STOP: {stop}"); break
    except KeyboardInterrupt:
        stop = f"interrupted by user (Ctrl-C) after {len(rows)} of {len(values)} points"
        emit(f"\n  -> {stop}; partial results saved.")
    dataf.close()
    # extrema as points of interest
    if rows:
        ys = [r[1] for r in rows]
        poi.setdefault(rows[int(np.argmax(ys))][0], "^")
        poi.setdefault(rows[int(np.argmin(ys))][0], "v")
    # data.csv already written incrementally above (survives interruption)
    # summary.json
    summary = {
        "target": target, "method": method, "sweep_var": var, "base": base,
        "cutoffs": {"max_time": max_time, "accuracy_eps": accuracy_eps, "conv_tol": conv_tol},
        "n_points": len(rows), "stop_reason": stop,
        "points_of_interest": {str(k): {"c": "converged", "x": "accuracy-drop", "t": "time-cutoff",
                                        "^": "maximum", "v": "minimum"}[v] for k, v in poi.items()},
        "final": {"x": rows[-1][0], "y": rows[-1][1]} if rows else None,
    }
    json.dump(summary, open(os.path.join(outdir, "summary.json"), "w"), indent=2)
    # ascii plot (always)
    xs = [r[0] for r in rows]; ys = [r[1] for r in rows]
    chart = ascii_plot(xs, ys, poi)
    emit("\n" + chart)
    emit("  legend: * data   c converged   x accuracy-drop   t time-cutoff   ^ max   v min")
    # png (graceful)
    png = _save_png(outdir, xs, ys, [r[2] for r in rows], poi, target, method, var)
    emit(f"\n# stop: {stop}")
    emit(f"# wrote: data.csv, summary.json, run.log" + (", plot.png" if png else " (matplotlib absent: no plot.png)"))
    emit(f"# dir: {outdir}")
    log.close()
    return summary, outdir


def _save_png(outdir, xs, ys, errs, poi, target, method, var):
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except Exception:
        return None
    fig, ax = plt.subplots(figsize=(7, 4.2))
    ax.plot(xs, ys, "-o", ms=3, lw=1, color="#2b6cb0", label=f"{target} ({method})")
    marks = {"c": ("o", "#2f855a", "converged"), "x": ("X", "#c53030", "accuracy drop"),
             "t": ("s", "#b7791f", "time cutoff"), "^": ("^", "#6b46c1", "max"), "v": ("v", "#6b46c1", "min")}
    seen = set()
    for x, ch in poi.items():
        if x in xs:
            m, col, lab = marks[ch]
            ax.scatter([x], [ys[xs.index(x)]], marker=m, s=90, color=col, zorder=5,
                       label=lab if lab not in seen else None)
            seen.add(lab)
    if any(e is not None for e in errs):
        ax2 = ax.twinx()
        ax2.plot(xs, [e if e is not None else float("nan") for e in errs], ":", color="#c53030", lw=1)
        ax2.set_ylabel("error vs reference", color="#c53030"); ax2.set_yscale("log")
    ax.set_xlabel(var); ax.set_ylabel("value"); ax.set_title(f"{target} via {method}: sweep over {var}")
    ax.legend(fontsize=8, loc="best"); ax.grid(alpha=0.3); fig.tight_layout()
    path = os.path.join(outdir, "plot.png"); fig.savefig(path, dpi=110); plt.close(fig)
    return path


def main(argv=None):
    p = argparse.ArgumentParser(prog="cdet_study", description="parameter-sweep stress harness")
    p.add_argument("--target", required=True)
    p.add_argument("--method", required=True)
    p.add_argument("--sweep", required=True, help="variable to scan: U|N|L|beta|mu|n")
    p.add_argument("--range", required=True, help="lo:hi:step")
    p.add_argument("--model", default="atom")
    p.add_argument("--N", type=int, default=6); p.add_argument("--U", type=float, default=1.0)
    p.add_argument("--mu", type=float, default=1.0); p.add_argument("--beta", type=float, default=5.0)
    p.add_argument("--L", type=int, default=12); p.add_argument("--t", type=float, default=1.0)
    p.add_argument("--n", type=int, default=5)
    p.add_argument("--max-time", type=float, default=None)
    p.add_argument("--accuracy-cutoff", type=float, default=None)
    p.add_argument("--conv-tol", type=float, default=None)
    a = p.parse_args(argv)
    base = {"model": a.model, "N": a.N, "U": a.U, "mu": a.mu, "beta": a.beta, "L": a.L, "t": a.t, "n": a.n}
    base.pop(a.sweep, None)
    study(a.target, a.method, base, a.sweep, frange(a.range),
          max_time=a.max_time, accuracy_eps=a.accuracy_cutoff, conv_tol=a.conv_tol)


def _selftest():
    print("cdet_study self-test (sweeps, convergence, cutoffs, outputs):")
    import tempfile
    root = tempfile.mkdtemp()
    # 1) convergence study: addition pole vs L settles -> conv flagged
    s, d = study("addition-pole", "surrogate", {"mu": 1.0}, "L", [8, 12, 16, 24, 32, 48, 64, 96, 128],
                 conv_tol=1e-3, outroot=root, quiet=True)
    assert any(v == "converged" for v in s["points_of_interest"].values()), s["points_of_interest"]
    assert os.path.exists(os.path.join(d, "data.csv")) and os.path.exists(os.path.join(d, "summary.json"))
    assert os.path.exists(os.path.join(d, "plot.png")), "png should be written (matplotlib present)"
    print("  [ok] convergence: addition-pole vs L flags a converged point; csv/json/png written")
    # 2) accuracy-drop study: diagrammatic self-energy vs ED breaks past the radius -> stop
    s2, _ = study("self-energy", "diagrammatic", {"model": "atom", "mu": 1.0, "beta": 5.0}, "U",
                  frange("0.2:2.0:0.2"), accuracy_eps=1e-2, outroot=root, quiet=True)
    assert "accuracy drop" in s2["stop_reason"], s2["stop_reason"]
    print(f"  [ok] accuracy cutoff: diagrammatic Sigma vs ED stops at the radius -> {s2['stop_reason']}")
    # 3) time budget: connected-det vs n stops within budget (tiny budget forces early stop)
    s3, _ = study("connected-det", "fast-minors", {}, "n", [3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                  max_time=1e-6, outroot=root, quiet=True)
    assert "time budget" in s3["stop_reason"], s3["stop_reason"]
    print(f"  [ok] time cutoff: connected-det vs n stops on budget -> {s3['stop_reason']}")
    # 4) ascii plot renders
    assert "|" in ascii_plot([0, 1, 2], [1.0, 2.0, 1.5])
    print("  [ok] ascii plot renders headless")
    print("  => sweeps run; convergence + accuracy-drop + time cutoffs all fire; logs/data/graphs emitted. PASS")


if __name__ == "__main__":
    if "--selftest" in sys.argv:
        _selftest()
    else:
        main()
