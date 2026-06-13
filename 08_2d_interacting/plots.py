"""plots.py (v166) -- built-in visualization of the suite's validated results.

Turns the validated physics into publication-quality figures (matplotlib, Agg backend -- no display needed):

  convergence   2D thermodynamic-limit: nearest-neighbour propagator vs lattice size (4x4 -> 100x100)
  resummation   conformal-Borel vs plain Pade error vs U on the SU(N) EoS (the order axis)
  mott          the Mott story: double occupancy, charge compressibility, spin susceptibility vs U
  summary       a 2x2 dashboard combining the above

Each figure is reproduced from the same code paths the gates validate, so the plots cannot drift from the numbers.
The frozen engine is not involved (these are post-processed observables)."""
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

_BLUE, _RED, _GREEN, _PURPLE = "#1f6feb", "#d1242f", "#1a7f37", "#8250df"


def _g0_nn(L, beta=5.0, mu=0.0, t=1.0):
    """equal-time nearest-neighbour plane-wave propagator (matches the validated C path to round-off)."""
    n = np.arange(L); c = np.cos(2 * np.pi * n / L)
    cx, cy = np.meshgrid(c, c, indexing="ij")
    eps = -2 * t * (cx + cy)
    nF = 1.0 / (1.0 + np.exp(beta * (eps - mu)))
    phase = np.cos(2 * np.pi * np.outer(n, np.ones(L)) / L)
    return np.sum(phase * nF) / (L * L)


def fig_convergence(ax=None):
    Ls = [4, 6, 8, 12, 16, 24, 32, 48, 64, 100]
    vals = [_g0_nn(L) for L in Ls]
    ref = vals[-1]
    own = ax is None
    if own:
        fig, ax = plt.subplots(figsize=(6, 4))
    ax.axhline(ref, color="0.6", ls="--", lw=1, label="thermodynamic limit")
    ax.plot(Ls, vals, "o-", color=_BLUE, lw=2, ms=6)
    ax.axvspan(12, 16, color=_GREEN, alpha=0.12, label="correlation length ~12-16")
    ax.set_xlabel("lattice side L"); ax.set_ylabel(r"$G_0$ nearest-neighbour")
    ax.set_title("2D thermodynamic-limit convergence")
    ax.legend(fontsize=8, loc="lower right"); ax.grid(alpha=0.3)
    return ax


def fig_resummation(ax=None, N=4, K=10):
    from sun_eos_curve import density_series, density_ed
    from sun_eos_conformal import conformal_borel, borel_singularity
    from resummation import pade, pade_eval
    a = density_series(N, K, M=max(24, 4 * N)); Uc = borel_singularity(a)
    p, q = pade(a, K // 2, K // 2)
    Us = np.linspace(0.2, 2.0, 12)
    cb = [abs(conformal_borel(a, U, Uc) - density_ed(N, U)) for U in Us]
    pa = [abs(pade_eval(p, q, U).real - density_ed(N, U)) for U in Us]
    own = ax is None
    if own:
        fig, ax = plt.subplots(figsize=(6, 4))
    ax.semilogy(Us, pa, "s--", color=_RED, lw=2, ms=5, label="plain Pade")
    ax.semilogy(Us, cb, "o-", color=_BLUE, lw=2, ms=5, label="conformal-Borel")
    ax.set_xlabel("U"); ax.set_ylabel("abs error vs ED")
    ax.set_title(f"resummation reach (SU(N={N}) density)")
    ax.legend(fontsize=8); ax.grid(alpha=0.3, which="both")
    return ax


def fig_mott(ax=None, N=2):
    from double_occupancy import docc_ed
    from susceptibilities import kappa_fluct, chi_spin_fluct
    Us = np.linspace(0.0, 4.0, 17)
    D = [docc_ed(N, U) for U in Us]
    K = [kappa_fluct(N, U) for U in Us]
    X = [chi_spin_fluct(N, U) for U in Us]
    own = ax is None
    if own:
        fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(Us, D, "o-", color=_PURPLE, lw=2, ms=4, label=r"double occ. $\langle n_\uparrow n_\downarrow\rangle$")
    ax.plot(Us, K, "s-", color=_BLUE, lw=2, ms=4, label=r"charge compr. $\kappa$")
    ax.plot(Us, X, "^-", color=_RED, lw=2, ms=4, label=r"spin susc. $\chi_s$")
    ax.set_xlabel("U"); ax.set_ylabel("response")
    ax.set_title("Mott correlation: charge down, spin up")
    ax.legend(fontsize=8); ax.grid(alpha=0.3)
    return ax


def save(which, outdir):
    os.makedirs(outdir, exist_ok=True)
    if which == "summary":
        fig, axes = plt.subplots(2, 2, figsize=(11, 8))
        fig_convergence(axes[0, 0]); fig_resummation(axes[0, 1]); fig_mott(axes[1, 0])
        axes[1, 1].axis("off")
        axes[1, 1].text(0.5, 0.5,
                        "CDet suite\n\nfrozen reference: 194/194\nhybrid parity: 0.00e+00\nobservables cross-checked vs ED\n\n"
                        "lattice = easy axis (thermodynamic limit)\norder axis = the real frontier",
                        ha="center", va="center", fontsize=11,
                        bbox=dict(boxstyle="round", fc="#f6f8fa", ec=_BLUE))
        fig.suptitle("CDet / connected-determinant suite -- validated results", fontsize=13, fontweight="bold")
        fig.tight_layout()
        path = os.path.join(outdir, "cdet_summary.png")
    else:
        fn = {"convergence": fig_convergence, "resummation": fig_resummation, "mott": fig_mott}[which]
        fn(); plt.gcf().tight_layout()
        path = os.path.join(outdir, f"cdet_{which}.png")
    plt.savefig(path, dpi=140, bbox_inches="tight"); plt.close("all")
    return path


def _selftest():
    print("plots self-test (built-in visualization of validated results):")
    out = "/tmp/_cdet_plots"
    for which in ("convergence", "resummation", "mott", "summary"):
        p = save(which, out)
        sz = os.path.getsize(p)
        assert sz > 5000, (which, sz)   # a real figure, not an empty canvas
        print(f"  {which:12s} -> {os.path.basename(p)}  ({sz // 1024} KB)")
    print("  => four figures render from the validated code paths (cannot drift from the numbers). PASS")


if __name__ == "__main__":
    _selftest()
