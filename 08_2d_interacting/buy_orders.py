"""v38 -- "Can CDet buy extra useful orders before the wall hits?" Answered with measurements on the
engine's actual Wick matrices. The connected-determinant organization evaluates order n as a determinant
det(M) of the (n+1)x(n+1) propagator matrix -- a sum of (n+1)! signed Wick contractions done EXACTLY in
O((n+1)^3). We measure the two advantages over a method that stochastically samples those contractions,
and the one thing the determinant does NOT buy."""
import subprocess, math

def ratios(args, nmax, nsamp=30000, seed=31337):
    out=subprocess.run(["./cdet_vs_naive"]+args+[str(nmax),"4.0","0.5","1.0","0.7","0.2",str(nsamp),str(seed)],
                       capture_output=True,text=True).stdout
    return {int(l.split()[0]):float(l.split()[1]) for l in out.splitlines() if l.strip() and not l.startswith("#")}

print("="*74)
print("PILLAR 1 -- COST: naive (n+1)! contraction enumeration vs determinant O((n+1)^3)")
print("  n   (n+1)! ops    cube ops   naive/det")
for n in [3,5,7,9,12,15]:
    m=n+1; print(f" {n:2d}  {math.factorial(m):>12d}  {m**3:>8d}   {math.factorial(m)/m**3:.2e}")
print("  -> past order ~5 the determinant is the ONLY way to evaluate the order at all.")

print("="*74)
print("PILLAR 2 -- PER-ORDER VARIANCE: cancellation perm(|M|)/|det(M)| a contraction-sampler suffers")
print("  (geometric mean over sampled configs; the determinant removes this factor exactly)")
r4=ratios(["sq","2","2"],9); r16=ratios(["sq","4","4"],7)
print("  order:        " + " ".join(f"{n:>6d}" for n in range(1,8)))
print("  2x2 (N=4):    " + " ".join(f"{r4[n]:6.2f}" for n in range(1,8)))
print("  4x4 (N=16):   " + " ".join(f"{r16[n]:6.2f}" for n in range(1,8)))
print("  -> grows with ORDER on every cluster (universal); determinant evaluates det exactly, no sampling.")

print("="*74)
print("PILLAR 3 -- WHAT IT DOES NOT BUY: the determinant advantage is an ORDER effect, not size/T.")
print("  perm/|det| at FIXED order n=3, vs cluster size:")
for args,N in [(["sq","2","2"],4),(["sq","3","3"],9),(["sq","4","4"],16)]:
    print(f"    N={N:2d}: {ratios(args,3)[3]:.3f}")
print("  -> SHRINKS with cluster size -- opposite to the v37 sign wall (R collapses, cost ~1/R^2 GROWS")
print("     with N and beta at fixed order). Different wall. The determinant tames the WICK-contraction")
print("     (within-config, per-ORDER) cancellation; the configuration-level (across-config, per-SYSTEM)")
print("     sign problem of the MC integral is untouched.")

print("="*74)
print("ANSWER: YES for ORDER reach -- CDet makes high orders both EVALUABLE (n^3 vs (n+1)!) and lower-")
print("variance per evaluation (removes perm/|det|), so you can climb to order ~10-15 where naive")
print("enumeration is impossible. NO for the size/temperature wall: that is a different, configuration-")
print("level sign problem (v37) the determinant does not address. CDet buys the ORDER axis cheaply; the")
print("SIZE and TEMPERATURE axes -- where 2D Hubbard physics lives -- stay blocked at fixed order.")
