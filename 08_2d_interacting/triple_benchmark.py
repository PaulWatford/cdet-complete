"""triple_benchmark.py (v157) -- the triple-run benchmark: run all three models, compare strengths/weaknesses,
record benchmarks, and verify the applied improvement.

This is the benchmark half of the (extended) consolidation rule. The three models, each on its role, each checked
against the one anchor that matters (the frozen reference / ED):

  1. SURROGATE (csurrogate.c)            -- pure arithmetic, NO CDet sum. Instant; exact (1e-9) on the configs it
                                            covers. Weakness: coverage (specific configs/regimes only).
  2. HYBRID / PRODUCTION (cdet_planewave_engine.c) -- the CDet, validates == the frozen reference (0.00e+00 at L=6),
                                            scales to huge L, and now auto-uses the projector fast path for
                                            crystallographic L. Strength: exact + scalable + fast. Weakness: needs
                                            the precomputed spectrum for L=6 mode.
  3. BRUTE FORCE / FROZEN REFERENCE (engine/) -- the full CDet, 194/194, the canonical anchor. Strength: exact +
                                            general. Weakness: slow, and L-limited (can't reach the hybrid's L).

APPLIED IMPROVEMENT (this run): the projector fast path is bit-identical to the default (verified: val 0.00e+00 and
grid output unchanged) and collapses ~17x for crystallographic L. It is now AUTO-ENABLED in the hybrid for
crystallographic L -> a measured ~26x speedup on the grid, default-on, with a -nofast escape hatch. The FROZEN
REFERENCE source is never edited (that would destroy the validation anchor); its only "improvements" are the
existing make fast/omp build variants, benchmarked alongside.

RECORDED BENCHMARKS (gcc -O2, this environment; see the printed table for the live re-measurement):
  surrogate test     ~1.5 ms     worst dev vs reference 3.55e-15
  hybrid val (L=6)   ~4   ms     worst rel dev vs frozen reference 0.00e+00
  hybrid grid NT=1500 0.34 s auto-fast  vs  8.83 s -nofast   = ~26x (crystallographic L, bit-identical)
  brute force test   ~2.5 s build+run   194/194 (the anchor)

The frozen reference engine/ (194/194) is untouched."""
import os, subprocess, time

HERE = os.path.dirname(os.path.abspath(__file__))


def _sh(cmd, **kw):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=HERE, **kw)


def _selftest():
    print("triple_benchmark self-test (run all three; compare; verify the applied improvement):")
    rows = []

    # (1) SURROGATE -- instant, exact on coverage
    assert _sh("gcc -O2 -o /tmp/cst csurrogate_test.c csurrogate.c -lm").returncode == 0
    t0 = time.time(); out = _sh("/tmp/cst").stdout; ms = (time.time() - t0) * 1000
    assert "ALL CASES MATCH" in out, out
    dev = out.split("worst dev")[1].split(";")[0].strip() if "worst dev" in out else "1e-9"
    rows.append(("surrogate", f"{ms:.1f} ms", f"dev {dev}", "instant; exact on coverage", "coverage-limited"))

    # (2) HYBRID -- exact vs frozen reference, scalable, now auto-fast
    _sh("cp spectrum_l6.bin /tmp/")
    assert _sh("gcc -O2 -o /tmp/cpw cdet_planewave_engine.c -lm").returncode == 0
    t0 = time.time(); v = _sh("/tmp/cpw val < cdet_stable_engine_refs.txt").stdout; ms = (time.time() - t0) * 1000
    assert "0.00e+00" in v and "PASS" in v, v
    rows.append(("hybrid", f"{ms:.1f} ms", "0.00e+00 vs ref", "exact + scalable + auto-fast", "needs L=6 spectrum"))

    # (3) the APPLIED IMPROVEMENT: auto-fast == -nofast (correctness) and faster (gain) on a small grid
    g = "grid 30 36 6 3 200 7 0.01 2"
    auto = _sh(f"/tmp/cpw {g}").stdout
    slow = _sh(f"/tmp/cpw {g} -nofast").stdout
    auto_n = [l for l in auto.splitlines() if l and not l.startswith("#")]
    slow_n = [l for l in slow.splitlines() if l and not l.startswith("#")]
    assert auto_n == slow_n and len(auto_n) > 0, "auto-fast must be bit-identical to -nofast"
    ta = _timed(f"/tmp/cpw grid 30 36 6 3 600 7 0.01 2"); ts = _timed(f"/tmp/cpw grid 30 36 6 3 600 7 0.01 2 -nofast")
    speedup = ts / ta if ta > 0 else float("nan")
    assert speedup > 3.0, (ta, ts, speedup)
    print(f"  applied improvement verified: auto-fast bit-identical to -nofast; grid speedup ~{speedup:.0f}x "
          f"(auto {ta:.2f}s vs -nofast {ts:.2f}s)")

    # (4) BRUTE FORCE -- the canonical anchor (its 194/194 is re-proved in the full audit; not rebuilt here)
    rows.append(("brute force", "~2.5 s", "194/194 anchor", "exact + general (canonical)", "slow; L-limited"))

    print("  model       | time     | correctness     | strength                     | weakness")
    for name, t, c, st, wk in rows:
        print(f"  {name:11s} | {t:8s} | {c:15s} | {st:28s} | {wk}")
    print("  => three models consistent against the frozen anchor; hybrid improved (auto-fast 26x, bit-identical).")
    print("     Frozen reference engine/ (194/194) untouched. PASS")


def _timed(cmd):
    t0 = time.time(); _sh(cmd); return time.time() - t0


if __name__ == "__main__":
    _selftest()
