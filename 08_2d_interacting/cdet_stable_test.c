#include <stdio.h>
#include <math.h>
#include "cdet_stable.h"
#include "cdet_engine.h"   /* the frozen naive G0_atom */
int main(void) {
    int fail = 0;
    /* 1) benign beta=2: stable must match the frozen naive propagator */
    double taus[3] = {0.5, 1.3, -0.7};
    for (int i = 0; i < 3; i++) {
        double a = G0_atom(taus[i], 2.0, 0.3), b = G0_atom_stable(taus[i], 2.0, 0.3);
        if (fabs(a - b) > 1e-12) { fail++; printf("BENIGN MISMATCH tau=%g: %.6e vs %.6e\n", taus[i], a, b); }
    }
    /* 2) deep beta=36, far occupied level (xi=-3 -> mu=3), tau near beta: naive DROPS the image */
    double beta = 36.0, mu = 3.0, tau = 35.0;     /* xi = -3 (occupied), tau>0 particle branch */
    double naive  = G0_atom(tau, beta, mu);
    double stable = G0_atom_stable(tau, beta, mu);
    double truth  = -exp(3.0 * tau - softplus_stable(108.0));   /* = -exp(-xi(beta-tau)-..) analytic */
    printf("deep-beta far-level (beta=36, xi=-3, tau=35):\n");
    printf("  naive  G0_atom        = %.6e  (the bug: 1-nf -> 0)\n", naive);
    printf("  stable G0_atom_stable = %.6e\n", stable);
    printf("  analytic reference    = %.6e\n", truth);
    if (fabs(naive) > 1e-12) printf("  (naive nonzero here -- bug not triggered at this point)\n");
    int naive_wrong = fabs(naive - truth) > 1e-6 * fabs(truth) + 1e-30;
    int stable_ok   = fabs(stable - truth) < 1e-9 * fabs(truth) + 1e-30;
    printf("  naive WRONG vs analytic? %s   stable OK? %s\n", naive_wrong?"YES":"no", stable_ok?"YES":"NO");
    if (!stable_ok) fail++;
    if (fail == 0) printf("\ncdet_stable: BENIGN MATCH (1e-12) + DEEP-BETA stable-correct -> PASS\n");
    else printf("\nFAILURES: %d\n", fail);
    return fail ? 1 : 0;
}
