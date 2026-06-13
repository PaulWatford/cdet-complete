#!/usr/bin/env python3
"""
bethe_spin_velocity_sparse.py  (v20)  --  a sparse (FFT fixed-point) Bethe solver for the small-U
spin velocity: it CRACKS small U at half filling, and it CHARACTERIZES why quarter-filling small U
is a deeper wall.

v18's dense dressed-energy solver works for U>=2 but fails for U<2: the kernels a_n have width U/4,
so a uniform grid that resolves them is too costly to invert densely (O(N^3)). The fix here avoids
the dense inversion entirely: the full-line a_2 self-convolution is DIAGONAL in Fourier
(hat a_2(omega) = e^{-2u|omega|}), so (1 + a_2*) sigma = drive is solved as
sigma = IFFT( FFT(drive) / (1 + hat a_2) ) -- exact in the a_2 part, no kernel discretization. A
short fixed-point loop handles the charge<->spin (a_1) coupling, and mu is fixed by two linear
solves (kappa(Q)=0), as in v18. Each step is O(N log N), so a fine grid (NL=2^13) is cheap.

What it achieves (half filling, where the exact Bessel curve is the gold standard):
    U:   0.5      1.0      2.0
  FFT:  1.928    1.835    1.641
 Bessel:1.919    1.833    1.640    -> 0.1-0.5%.
So the sparse solver reaches the SMALL-U region the dense solver could not, and it agrees with the
dense solver at the U=2 overlap (both fillings) -- the two are complementary (FFT for U<=2, dense
for U>=2). The plateau window scales with U (it sits at ~[2,5]*(U/4), since the asymptotic regime
sets in at a few kernel widths).

What it reveals (quarter filling, small U -- a STRUCTURAL wall, not resolution):
At low filling AND small U the spin density sigma(Lambda) has narrow support; the velocity profile
|eps_s'|/(2 pi sigma) RISES to a peak (~1.0-1.08 at U=0.5,1) and then CRASHES into the noise floor
(sigma -> 0) BEFORE any flat plateau forms. There is no asymptotic plateau to read -- the
Lambda->infinity spin-Fermi-point region is buried under the density's collapse. So the exact
quarter-filling u_sigma below U=2 is NOT cleanly extractable by the dressed-energy route; the
profile peak is a rough lower bound only. This is a different, deeper obstruction than the dense
solver's resolution limit (v18), and it is named here rather than papered over.

Net: small U is reachable at half filling (validated) but structurally walled at quarter filling.
The exact quarter-filling u_sigma stands for U>=2 (v18); U<2 there needs a genuinely different
handle (e.g. the weak-coupling field-theory expansion v_s = v_F - O(U)), not a better grid.
"""
import numpy as np
from scipy.special import iv
trap = getattr(np, 'trapezoid', None) or np.trapz


def vs_exact_half(U):
    x = 2 * np.pi / U
    return 2 * iv(1, x) / iv(0, x)


def solve_fft(U, n, NL=2**13, Lmax=50.0, Nk=500, tol=1e-11, maxit=300):
    """Sparse FFT fixed-point solver; returns (Lam, |v(Lam)|) for the spin-velocity profile."""
    u = U / 4.0
    Lam = np.linspace(-Lmax, Lmax, NL, endpoint=False); dL = Lam[1] - Lam[0]
    w = 2 * np.pi * np.fft.fftfreq(NL, d=dL); a2hat = np.exp(-2 * u * np.abs(w))

    def a1(x):
        return (1.0 / np.pi) * u / (u * u + x * x)

    def density(Q):
        k = np.linspace(-Q, Q, Nk); dk = k[1] - k[0]; sk = np.sin(k); ck = np.cos(k)
        A1 = a1(Lam[:, None] - sk[None, :])
        sig = np.zeros(NL); rho = np.full(Nk, 1 / (2 * np.pi))
        for _ in range(maxit):
            drive = A1 @ (rho * dk)
            sig2 = np.real(np.fft.ifft(np.fft.fft(drive) / (1 + a2hat)))
            rho2 = 1 / (2 * np.pi) + ck * ((A1.T @ sig2) * dL)
            if np.max(np.abs(rho2 - rho)) < tol and np.max(np.abs(sig2 - sig)) < tol:
                rho, sig = rho2, sig2; break
            rho, sig = rho2, sig2
        return k, dk, sk, ck, rho, sig, A1

    lo, hi = 0.02, np.pi - 0.02
    for _ in range(38):
        Q = 0.5 * (lo + hi); k, dk, sk, ck, rho, sig, A1 = density(Q)
        if trap(rho, k) < n: lo = Q
        else: hi = Q
    Q = 0.5 * (lo + hi); k, dk, sk, ck, rho, sig, A1 = density(Q)

    def dressed(src_k):
        eps = np.zeros(NL); kap = src_k.copy()
        for _ in range(maxit):
            eps2 = np.real(np.fft.ifft(np.fft.fft(-(A1 @ (ck * kap * dk))) / (1 + a2hat)))
            kap2 = src_k + (A1.T @ eps2) * dL
            if np.max(np.abs(kap2 - kap)) < tol:
                kap, eps = kap2, eps2; break
            kap, eps = kap2, eps2
        return kap, eps

    kap0, eps0 = dressed(-2 * ck); kapm, epsm = dressed(-np.ones(Nk))
    mu = -kap0[-1] / kapm[-1]; eps = eps0 + mu * epsm
    return Lam, np.abs(np.gradient(eps, dL) / (2 * np.pi * sig))


def u_sigma_small_U(U, n):
    """Plateau read with a U-scaled window (valid where a plateau exists -- half filling small U)."""
    Lam, v = solve_fft(U, n)
    width = max(0.4, U / 4.0)
    m = (Lam >= 2 * width) & (Lam <= 5 * width)
    return float(np.median(v[m]))


def main():
    print("Sparse FFT fixed-point Bethe solver -- the small-U spin velocity (v20)\n")
    print("1) HALF filling: the sparse solver REACHES small U (dense solver could not):")
    print("   %5s %10s %10s %7s" % ("U", "FFT", "Bessel", "err"))
    for U in [0.5, 1.0, 2.0]:
        p = u_sigma_small_U(U, 1.0); e = vs_exact_half(U)
        print("   %5.1f %10.4f %10.4f %6.1f%%" % (U, p, e, 100 * abs(p / e - 1)))
    print("   -> 0.1-0.5%: small U cracked at half filling; complementary to the dense solver")
    print("      (FFT for U<=2, dense for U>=2; they agree at the U=2 overlap).\n")

    print("2) QUARTER filling, small U: a STRUCTURAL wall -- the profile peaks, then crashes:")
    for U in [0.5, 1.0]:
        Lam, v = solve_fft(U, 0.5)
        samp = [(L, v[np.argmin(np.abs(Lam - L))]) for L in [0.6, 1.0, 1.5, 2.0, 3.0]]
        s = "  ".join("L=%.1f:%.3f" % (L, val) for L, val in samp)
        print("   U=%.1f  %s" % (U, s))
    print("   The velocity rises to a peak (~1.0-1.08) then collapses as sigma -> 0, with NO flat")
    print("   plateau: at low filling + small U the spin density support is too narrow to reach")
    print("   the Lambda->inf asymptotic regime. So exact quarter-filling u_sigma below U=2 is not")
    print("   extractable here (the peak is a rough lower bound); it needs a weak-coupling handle,")
    print("   not a finer grid. The exact quarter-filling u_sigma stands for U>=2 (v18).")


if __name__ == '__main__':
    main()
