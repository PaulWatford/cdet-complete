"""v37 sign-problem characterization. The 2x2 validation proves the MC driver correct; this shows where
the variance WALL appears. We measure the sign-cancellation ratio R = mean(C_V)/mean(|C_V|) (intrinsic,
needs no exact answer) and the relative statistical error, as functions of cluster size and temperature
at fixed order. Small |R| => severe cancellation => the cost to reach fixed precision explodes like 1/R^2.
This is the fermion sign problem -- the real difficulty of 2D Hubbard -- made quantitative."""
import subprocess
def mc(args, n, beta, nmc=500000, seed=4242):
    out=subprocess.run(["./mc2d"]+args+[str(n),str(beta),"0.5","1.0","0.7","0.2",str(nmc),str(seed)],
                       capture_output=True,text=True).stdout.split()
    est,err,R,absm=[float(x) for x in out]
    rel=abs(err/est) if est!=0 else float('inf')
    n1pct=nmc*(rel/0.01)**2                       # samples projected for 1% relative error
    return est,err,abs(R),rel,n1pct

print("=== cluster-size sweep (order 3, beta=4) ===")
print(f"{'cluster':8s} {'N':>3s} {'|R|':>8s} {'rel.err':>9s} {'Nsamp->1%':>12s}")
for args,N in [(["sq","2","2"],4),(["sq","3","2"],6),(["sq","3","3"],9),(["sq","4","4"],16)]:
    est,err,R,rel,n1=mc(args,3,4.0)
    print(f"{' '.join(args):8s} {N:3d} {R:8.4f} {rel:9.4f} {n1:12.3e}")

print("\n=== temperature sweep (order 3, cluster 3x3) ===")
print(f"{'beta':>5s} {'|R|':>8s} {'rel.err':>9s} {'Nsamp->1%':>12s}")
for beta in [2.0,4.0,6.0,8.0]:
    est,err,R,rel,n1=mc(["sq","3","3"],3,beta)
    print(f"{beta:5.1f} {R:8.4f} {rel:9.4f} {n1:12.3e}")
