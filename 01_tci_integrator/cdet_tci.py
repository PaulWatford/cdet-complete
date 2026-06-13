"""
cdet_tci.py -- tensor-cross-interpolation integrator for the connected-determinant
time-integral, using the real cdet C_V engine as the oracle.

Method (what the data picked, and validated):
  * The order-n contribution integrates C_V over the n vertex times.
  * The integrand has cusps on every coincidence diagonal tau_i = tau_j (the
    propagator jumps at 0), so it is NOT quantics-low-rank in box coordinates.
  * It IS symmetric in the times, so we integrate over the ORDERED SIMPLEX
    (smooth there, no diagonal crossings) via a smooth cube->simplex map, x n!.
  * On the simplex the integrand is quantics-compressible; TCI (teneva.cross)
    learns its tensor train from ~rank^2 * bits * n adaptive evaluations,
    never forming the G^n grid.

Validated (atom, beta=5, mu=0.3) against brute-force grid integrals from the
same engine: integral error 5e-3..5e-5, evaluation savings growing with n
(1x at n=2 -> 4x at n=5; the gap widens at higher n).

Requires: teneva (pip install teneva), and the compiled ./oracle binary:
  cc -O2 -std=c99 -I<engine_dir> oracle.c cdet_engine.o -lm -o oracle
"""
import teneva, numpy as np, subprocess, math

def integrate(n, R=5, beta=5.0, harness="./oracle", m=800000, e=1e-12,
              nswp=80, dr_max=6, verbose=True):
    """Return (integral, n_evals, max_rank, TT) for the order-n time-integral."""
    G = 2**R
    xg = (np.arange(G) + 0.5) / G
    def cube_to_simplex(xs):
        taus = []; prev = 0.0; jac = 1.0
        for i in range(n):
            span = beta - prev; t = prev + span * xs[i]; jac *= span
            taus.append(t); prev = t
        return taus, jac
    def decode(row):
        xs = []
        for v in range(n):
            x = 0
            for p in range(R):
                x = (x << 1) | int(row[p * n + v])
            xs.append(xg[x])
        return xs
    calls = [0]
    def oracle(I):
        I = np.asarray(I); calls[0] += len(I)
        taus = []; jacs = []
        for row in I:
            t, j = cube_to_simplex(decode(row)); taus.append(t); jacs.append(j)
        inp = "\n".join(" ".join(f"{x:.12f}" for x in t) for t in taus) + "\n"
        out = subprocess.run([harness, str(n)], input=inp, capture_output=True, text=True).stdout
        return np.array([float(x) for x in out.split()]) * np.array(jacs)
    Y = teneva.cross(oracle, teneva.rand([2] * (n * R), r=2), m=m, e=e,
                     nswp=nswp, dr_max=dr_max, cache={})
    Y = teneva.truncate(Y, e=e)
    integral = teneva.sum(Y) * ((1.0 / G) ** n) * math.factorial(n)
    rk = max(teneva.ranks(Y))
    if verbose:
        print(f"order n={n}, R={R}: integral={integral:.8e}  evals={calls[0]} "
              f"(full grid {G**n})  max rank={rk}")
    return integral, calls[0], rk, Y

if __name__ == "__main__":
    for n in (2, 3, 4, 5):
        integrate(n, R=4)
