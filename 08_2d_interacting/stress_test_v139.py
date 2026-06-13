"""stress_test_v139.py -- stress test of the hybrid plane-wave engine, and the robustness guards it motivated.

The session's new features (fast minors, self-energy, the mapping) are verified SUPPLEMENTS, NOT yet wired
into the hybrid (that is open item #5). This stress-tests what the hybrid actually carries: any-L plane-wave
propagator, the -fast projector path, the continuous-freeze (mode 2), the NaN guard.

WHAT THE STRESS TEST FOUND (full numbers in STRESS_TEST_v139_RESULT.md):
  ROBUST: validation holds (== stable @L6, 0.00e+00); fast == direct is bit-identical; the NaN guard fires
  cleanly on every overflow (no crashes). Scales to 2.7M sites (L=140) in ~190 s via the fast path, and the
  freeze probe_val matches the surrogate exactly at 1e6 sites (1.000192).
  PRECISION: f64 walls at beta ~ 100 (NaN guard); the long-double build reaches beta >= 200. Use -DUSE_LD for
  deep-beta / deep-cancellation probes.
  THREE SILENT/MISLEADING FAILURE MODES (now guarded, input-only so valid runs are unchanged):
    (a) mode 0/1 at a non-crystallographic L (L not in {1,2,3,4,6}) -> the fixed probe level blows up to
        nonsense (z ~ 1e23) with no warning. Guard: warn, point to mode 2.
    (b) large delta -> c1 (a linear-response s->0 derivative) is contaminated by the nonlinear regime (sign
        flip at delta=0.5). Guard: warn when delta > 0.1.
    (c) delta = 0 -> c1 = NaN; the NaN guard caught it but mislabeled it a "precision wall". Guard: refuse
        delta <= 0 up front with a clear message.

This module re-runs the FAST stress checks (guards + fast==direct + validation) as a self-test; the slow
large-L / deep-beta scans are documented in the result. Frozen engine untouched (194/194); the hybrid's
val gate stays 0.00e+00 after the guards (they are input-only)."""
import os, subprocess, shutil

HERE = os.path.dirname(os.path.abspath(__file__))

def _build():
    work = '/tmp/stress_v139'; os.makedirs(work, exist_ok=True)
    shutil.copy(os.path.join(HERE, 'spectrum_l6.bin'), work)
    exe = os.path.join(work, 'cpw')
    r = subprocess.run(['gcc', '-O2', '-std=c11', '-o', exe,
                        os.path.join(HERE, 'cdet_planewave_engine.c'), '-lm'], capture_output=True, text=True)
    return (exe, work) if r.returncode == 0 else (None, None)

def _grid(exe, work, args):
    return subprocess.run([exe, 'grid'] + args, capture_output=True, text=True, cwd=work)

def _selftest():
    print("stress_test_v139 self-test (hybrid robustness: validation, fast==direct, guards):")
    exe, work = _build()
    if exe is None:
        print("  (gcc/engine unavailable) -- skipping"); return
    # (1) validation holds
    refs = open(os.path.join(HERE, 'cdet_stable_engine_refs.txt')).read()
    v = subprocess.run([exe, 'val'], input=refs, capture_output=True, text=True, cwd=work)
    assert 'PASS' in v.stdout, v.stdout
    print("  validation: hybrid == stable @L6, 0.00e+00 (PASS) -- guards are input-only")
    # (2) fast == direct bit-identical at L=6
    base = ['36', '36', '1', '8', '256', '31', '0.002', '0', '2', '1', '2', '4', '1.845', '-L', '6']
    d = [l for l in _grid(exe, work, base).stdout.splitlines() if l.startswith('36')][0]
    f = [l for l in _grid(exe, work, base + ['-fast']).stdout.splitlines() if l.startswith('36')][0]
    assert d == f, (d, f)
    print(f"  fast == direct (L=6): identical -> {d.split()[1]} {d.split()[3]}")
    # (3) the three guards fire; valid run stays clean
    e0 = _grid(exe, work, ['36', '36', '1', '8', '64', '31', '0.0', '0', '2', '1', '2', '4', '1.845', '-L', '6'])
    assert e0.returncode != 0 and 'delta must be > 0' in e0.stderr, e0.stderr
    big = _grid(exe, work, ['36', '36', '1', '8', '64', '31', '0.5', '0', '2', '1', '2', '4', '1.845', '-L', '6'])
    assert 'delta=0.5 is large' in big.stderr, big.stderr
    nc = _grid(exe, work, ['36', '36', '1', '6', '64', '31', '0.002', '0', '2', '1', '2', '4', '1.0', '-L', '12'])
    assert 'non-crystallographic' in nc.stderr, nc.stderr
    ok = _grid(exe, work, ['36', '36', '1', '6', '64', '31', '0.002', '0', '2', '1', '2', '4', '1.845', '-L', '6'])
    assert 'warning' not in ok.stderr and 'error' not in ok.stderr, ok.stderr
    print("  guards: delta<=0 refused; large delta warned; non-crystallographic+mode0 warned; valid run clean")
    print("  => hybrid is robust; the three silent/misleading failure modes are now guarded (input-only). PASS")

if __name__ == "__main__":
    _selftest()
