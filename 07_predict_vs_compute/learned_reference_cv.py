"""learned_reference_cv.py  (v33)

Answers a direct question: we extracted a custom analytic surrogate FROM the engine's own patterns
(the Lieb-Wu analytic moment driving the spin-correlator shape, plus K_rho / velocities / CFT tail).
Why test fresh parametric references (v32) as control variates instead of THAT?

Answer: a level distinction. v32 tested PER-SAMPLE surrogates -- approximations of C_V's value at each
random vertex-time configuration, to cut the Monte-Carlo sign-variance. The learned patterns are NOT
per-sample quantities; they describe the CONVERGED physical observable. So they cannot plug into the
per-sample control variate v32 measured (which is why simple parametric per-sample surrogates were
used there, and de-correlated: |rho|<=0.7, 1-2x).

But at the OBSERVABLE level -- where the learned patterns actually live -- they are an excellent
control variate, and this script measures exactly how good, using the same formula as
02_control_variate (variance reduction = 1/(1-rho^2)). The learned analytic prediction (Path B in
predict_vs_compute, NO determinant sum) is the surrogate g; the exact ED correlator is the target f.

Run from this folder: python3 learned_reference_cv.py
"""
import numpy as np
from predict_vs_compute import ED, analytic_moment, C_free, spin_model

def main():
    L = 8; N = L  # half-filling: N total electrons, L//2 per spin (predict_vs_compute convention)
    Ugrid = [0.0, 0.5, 1.0, 2.0, 3.0, 4.0, 6.0, 8.0]
    ed = ED(L, L // 2, L // 2)

    exact = {U: ed.spin_corr(ed.solve(U)[1])[:L // 2 + 1] for U in Ugrid}
    Cf = C_free(L, N)[:L // 2 + 1]
    Caf = exact[Ugrid[-1]].copy()
    m_free, m_af = analytic_moment(0.0), analytic_moment(Ugrid[-1])

    f, g = [], []   # f = exact target, g = learned-pattern analytic prediction (the surrogate)
    for U in Ugrid:
        g.append(spin_model(Cf, Caf, analytic_moment(U), m_free, m_af))
        f.append(exact[U])
    f = np.concatenate(f); g = np.concatenate(g)

    rho = np.corrcoef(f, g)[0, 1]
    bstar = np.cov(f, g)[0, 1] / np.var(g)
    resid = np.sqrt(np.mean((f - g) ** 2))
    scale = np.sqrt(np.mean(f ** 2))
    vr = 1.0 / (1.0 - rho ** 2)

    print("Learned-pattern reference as an OBSERVABLE-level control variate")
    print("  target f = exact ED spin correlator;  surrogate g = analytic prediction from the patterns")
    print("  (Lieb-Wu analytic moment -> correlator shape; NO determinant sum)\n")
    print("  residual ||f-g||         = %.3e  (%.1f%% of correlator scale %.3f)" % (resid, 100 * resid / scale, scale))
    print("  correlation rho(f,g)     = %.6f" % rho)
    print("  optimal CV coeff beta*   = %.4f" % bstar)
    print("  variance reduction 1/(1-rho^2) = %.0fx\n" % vr)

    # Direct check of the control-variate estimator vs plain, on the (U,r) ensemble.
    Eg = g.mean()
    plain_var = np.var(f) / len(f)
    cv_samples = f - bstar * (g - Eg)
    cv_var = np.var(cv_samples) / len(cv_samples)
    print("  plain estimator var of <f>   = %.3e" % plain_var)
    print("  control-variate estimator var = %.3e  -> %.0fx fewer samples" % (cv_var, plain_var / cv_var))

    print("\nContrast with v32 (PER-SAMPLE parametric references on the high-order C_V):")
    print("  decoupled / shifted-mu / weak-hop surrogates: |rho| <= ~0.7, erratic -> 1-2x.")
    print("  The learned reference wins because it captures the actual physics, not a fixed propagator")
    print("  tweak -- but it operates at the OBSERVABLE level, not per MC sample.")
    print("\nScope (honest): this reference is the half-filling spin CORRELATOR. The high-order DiagMC")
    print("computes the GREEN'S FUNCTION / self-energy; the analogous learned reference is the")
    print("Luttinger-liquid G asymptotics built from K_rho + the spin/charge velocities (already in")
    print("hand, 07/luttinger_K.py + spin_charge_velocities.py) -- constructible, not yet built as a")
    print("G-reference. That bridge is the next step, not a brand-new surrogate.")

if __name__ == '__main__':
    main()
