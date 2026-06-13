/* cos_harness.c -- dump the engine's per-subset seed (D_corr) and D_vac arrays plus the ground-truth
 * connected determinant C_V, so a CoS-style subset-convolution can be checked against the real engine.
 * Build: gcc -O2 -I../engine -o cos_harness cos_harness.c ../engine/cdet_engine.c -lm */
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include "cdet_engine.h"

/* a deterministic, well-conditioned propagator (the ALGEBRA we test is g0-independent) */
static double g0_test(int i, int j, double tau, void *ctx) {
    (void)ctx;
    return 0.4 * cos(0.7 * (i - j) + 0.3 * tau) * exp(-0.15 * fabs(tau)) + ((i == j) ? 0.2 : 0.0);
}

int main(int argc, char **argv) {
    int n = (argc > 1) ? atoi(argv[1]) : 5;
    Vertex V[16];
    for (int i = 0; i < n; i++) { V[i].site = (i * 3 + 1) % 7; V[i].tau = 0.13 * (i + 1) - 0.05 * i * i; }
    int so = 0, si = 2; double to = 0.21, ti = -0.34;

    double cv = C_V(V, n, so, to, si, ti, g0_test, NULL);     /* ground truth (engine) */

    int N = 1 << n;
    printf("%d %.17g\n", n, cv);                               /* line 1: n  C_V */
    Vertex sub[16];
    for (int mask = 0; mask < N; mask++) {
        int m = 0;
        for (int i = 0; i < n; i++) if (mask & (1 << i)) sub[m++] = V[i];
        double seed = D_corr(sub, m, so, to, si, ti, g0_test, NULL);   /* per-subset D_corr */
        double dv   = D_vac(sub, m, g0_test, NULL);                    /* per-subset D_vac  */
        printf("%d %.17g %.17g\n", mask, seed, dv);            /* mask  seed  dvac */
    }
    return 0;
}
