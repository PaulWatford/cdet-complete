/* bench_scaling.c -- part of cdet-c-port v2.31
 * Author: Paul Watford, 2026. MIT license.
 */
/* bench_scaling: time the fast determinant across a wide range of expansion
 * order n at fixed lattice size, then fit the runtime to a power law t ~ n^p
 * by least squares on log(t) vs log(n). The O(n L^2) kernel should give p ~ 1.
 * Run with: make bench_scaling */

#include "qss_det.h"
#include "cdet_engine.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>

#if defined(CLOCK_MONOTONIC)
static double now_s(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + (double)ts.tv_nsec * 1e-9;
}
#else
static double now_s(void) { return (double)clock() / (double)CLOCKS_PER_SEC; }
#endif

int main(void) {
    double beta = 5.0, mu = 0.3, t = 1.0;
    int L = 6;

    printf("fast-determinant scaling benchmark\n");
    printf("params: beta=%.3f mu=%.3f t=%.3f L=%d\n\n", beta, mu, t, L);
    printf("%-12s %14s\n", "n", "t_fast(s)");

    /* collect log-log points for the fit (skip the smallest, timer-noise n) */
    double sx = 0, sy = 0, sxx = 0, sxy = 0;
    int npts = 0;

    for (int n = 64; n <= 4194304; n *= 2) {
        double *tau = malloc((size_t)n * sizeof(double));
        double *A  = malloc((size_t)n * L * sizeof(double));
        double *Bu = malloc((size_t)n * L * sizeof(double));
        double *Bl = malloc((size_t)n * L * sizeof(double));
        if (!tau || !A || !Bu || !Bl) {
            printf("(allocation failed at n=%d; stopping)\n", n);
            free(tau); free(A); free(Bu); free(Bl); break;
        }
        for (int a = 0; a < n; a++) tau[a] = beta * (a + 0.5) / n;
        qss_build_ring(L, beta, mu, t, tau, n, A, Bu, Bl);

        int reps = n <= 1024 ? 200 : (n <= 65536 ? 20 : 3);
        double t0 = now_s();
        volatile double df = 0.0;
        for (int r = 0; r < reps; r++) df = qss_det(A, Bu, Bl, n, L);
        (void)df;
        double tf = (now_s() - t0) / reps;

        printf("%-12d %14.6e\n", n, tf);
        double lx = log((double)n), ly = log(tf);
        sx += lx; sy += ly; sxx += lx * lx; sxy += lx * ly; npts++;

        free(tau); free(A); free(Bu); free(Bl);
    }

    if (npts >= 2) {
        double slope = (npts * sxy - sx * sy) / (npts * sxx - sx * sx);
        printf("\nfitted scaling exponent p in t ~ n^p:  %.3f\n", slope);
        printf("(the O(n L^2) kernel predicts p = 1; dense LU would give p = 3.)\n");
    }
    return 0;
}
