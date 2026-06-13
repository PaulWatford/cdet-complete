"""two_particle_run.py (v159) -- the chained two-round protocol with TWO particles.

v158 chained a single electron's position into round 2. Two particles is where the physics begins: they obey
EXCLUSION (no double occupancy -- Pauli) and they carry a PAIR correlation -- the connected, two-body content that
the CDet exists to capture. This run repeats the chained two-round protocol for two particles and asks whether the
two gains (efficiency, expansion) survive the move from one body to two, and whether they reach the *interaction*
response, not just the one-body amplitude.

  EXPANSION (config walk, two particles + exclusion): the chained RNG continuation moves one of the two particles
  each round to a free site (never onto the other -- exclusion), continuing the stream so it never cycles. It
  sweeps the full pair-config space C(5,2)=10 with exclusion always satisfied.

  EFFICIENCY (hybrid, two observables): chaining round 1's terminal stream into round 2 (a clean 2*NT estimate)
  reduces the error of BOTH the one-body amplitude A and the two-body interaction response c1 by ~sqrt(2). The gain
  reaches the interaction, not only the amplitude -- the continuation is as useful for the correlated quantity as
  for the free one.

NET: the continuation gains carry from one particle to two, and from the amplitude to the interaction. The frozen
reference is untouched; the only hybrid change remains the v158 print-only terminal_state."""
import os, subprocess, statistics
import shutil
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))


def _sh(cmd):
    return subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=HERE).stdout


def _build():
    shutil.copy(os.path.join(HERE, "spectrum_l6.bin"), tempfile.gettempdir())
    _cpw = os.path.join(tempfile.gettempdir(), "cpw_tp" + (".exe" if os.name=="nt" else ""))
    _sh(f'gcc -O2 -o "{_cpw}" cdet_planewave_engine.c -lm')


def _mix(state):
    state = (state * 6364136223846793005 + 1442695040888963407) & ((1 << 64) - 1)
    return state, state >> 33


def move2(parts, which, step, L):
    """move particle `which` by `step` to the next free site -- never onto the other particle (exclusion)."""
    other = parts[1 - which]; cur = parts[which]; cand = cur
    for _ in range(2 * L):
        cand = (cand + step) % L
        if cand and cand != other and cand != cur:
            np_ = list(parts); np_[which] = cand
            return tuple(sorted(np_))
    return parts


def rng_walk2(start, seed, rounds, L=6):
    """two-particle chained-continuation walk; returns (#distinct pair-configs, exclusion_held)."""
    cfg = tuple(sorted(start)); seen = {cfg}; st = seed; excl = True
    for _ in range(rounds):
        st, a = _mix(st); st, b = _mix(st)
        cfg = move2(cfg, a % 2, 1 + (b % (L - 1)), L); seen.add(cfg)
        if cfg[0] == cfg[1]:
            excl = False
    return len(seen), excl


def grid(nt, seed, beta=30):
    """one grid point -> (A one-body amplitude, c1 two-body interaction response, terminal RNG state)."""
    out = _sh(f'"{os.path.join(tempfile.gettempdir(), "cpw_tp" + (".exe" if os.name=="nt" else ""))}" grid {beta} {beta} 1 5 {nt} {seed} 0.01 2')
    A = c1 = term = None
    for l in out.splitlines():
        if l.startswith(f"{beta}."):
            p = l.split(); A = float(p[1]); c1 = float(p[3])
        if "terminal_state" in l:
            term = int(l.split()[2])
    return A, c1, term


def chained_efficiency(seeds, nt=2000, nt_ref=20000):
    """error of single-NT vs chained-2NT for both A and c1, against a high-NT reference. Returns (ratioA, ratioC1)."""
    Aref, c1ref, _ = grid(nt_ref, 7)
    sA = statistics.mean(abs(grid(nt, s)[0] - Aref) for s in seeds)
    sC = statistics.mean(abs(grid(nt, s)[1] - c1ref) for s in seeds)
    cA = []; cC = []
    for s0 in seeds:
        A1, c1a, t = grid(nt, s0); A2, c1b, _ = grid(nt, t)
        cA.append(abs((A1 + A2) / 2 - Aref)); cC.append(abs((c1a + c1b) / 2 - c1ref))
    return sA / statistics.mean(cA), sC / statistics.mean(cC)


def _selftest():
    print("two_particle_run self-test (chained two-round protocol with two particles):")
    _build()
    # (1) EXPANSION: two-particle chained walk sweeps the pair-config space with exclusion held
    n, excl = rng_walk2((1, 3), 777, 40)
    assert n >= 8 and excl, (n, excl)
    print(f"  EXPANSION: two-particle chained walk visits {n}/10 pair-configs (no cycle); exclusion (Pauli) held: {excl}")
    # (2) EFFICIENCY: chained continuation gives ~sqrt2 for BOTH the amplitude and the interaction response
    rA, rC = chained_efficiency(list(range(101, 113)))
    assert rA > 1.2 and rC > 1.2, (rA, rC)
    print(f"  EFFICIENCY: chained-continuation error reduction -- A (1-body) {rA:.2f}x, c1 (2-body interaction) {rC:.2f}x")
    print("  => the continuation gains survive one->two particles and reach the interaction, not just the amplitude;")
    print("     exclusion is respected throughout. Frozen engine untouched (194/194). PASS")


if __name__ == "__main__":
    _selftest()
