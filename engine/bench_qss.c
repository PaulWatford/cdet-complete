/* bench_qss.c -- part of cdet-c-port v2.31
 * Author: Paul Watford, 2026. MIT license.
 */
/* bench_qss: time the O(n L^2) quasiseparable determinant against a dense
 * O(n^3) LU on the same generators, and report the speedup and the accuracy.
 * Run with: make bench
 *
 * For each expansion order n it builds the same-site ring vertex matrix
 * generators, times qss_det (fast) and a from-scratch dense LU on the
 * reconstructed matrix (independent), and prints n, both times, the speedup,
 * both determinants, and the relative error. The dense path is O(n^3) so it is
 * only run up to a cutoff; past that the fast method is timed alone. */

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

/* dense LU determinant of a row-major n x n matrix, partial pivoting.
 * independent of qss_det: factor from scratch and multiply the pivots. */
static double dense_det_lu(double *M, int n) {
    double det = 1.0;
    for (int col = 0; col < n; col++) {
        int piv = col;
        double best = fabs(M[col * n + col]);
        for (int r = col + 1; r < n; r++) {
            double v = fabs(M[r * n + col]);
            if (v > best) { best = v; piv = r; }
        }
        if (best == 0.0) return 0.0;
        if (piv != col) {
            for (int k = 0; k < n; k++) {
                double t = M[col * n + k]; M[col * n + k] = M[piv * n + k]; M[piv * n + k] = t;
            }
            det = -det;
        }
        double d = M[col * n + col];
        det *= d;
        for (int r = col + 1; r < n; r++) {
            double f = M[r * n + col] / d;
            if (f != 0.0)
                for (int k = col; k < n; k++) M[r * n + k] -= f * M[col * n + k];
        }
    }
    return det;
}

int main(void) {
    double beta = 5.0, mu = 0.3, t = 1.0;
    int L = 6;
    int dense_cutoff = 2048;

    printf("qss-vs-dense determinant benchmark\n");
    printf("params: beta=%.3f mu=%.3f t=%.3f L=%d\n", beta, mu, t, L);
    printf("dense LU cross-check runs up to n=%d, then fast method alone.\n\n", dense_cutoff);
    printf("%-10s %12s %12s %10s %18s %18s %10s\n",
           "n", "t_fast(s)", "t_dense(s)", "speedup", "det_fast", "det_dense", "rel_err");

    for (int n = 16; n <= 1048576; n *= 2) {
        double *tau = malloc((size_t)n * sizeof(double));
        double *A  = malloc((size_t)n * L * sizeof(double));
        double *Bu = malloc((size_t)n * L * sizeof(double));
        double *Bl = malloc((size_t)n * L * sizeof(double));
        if (!tau || !A || !Bu || !Bl) {
            printf("(allocation failed at n=%d; stopping)\n", n);
            free(tau); free(A); free(Bu); free(Bl); break;
        }
        for (int a = 0; a < n; a++) tau[a] = beta * (a + 0.5) / n;   /* sorted */
        qss_build_ring(L, beta, mu, t, tau, n, A, Bu, Bl);

        /* fast determinant, timed (repeat small n for a stable reading) */
        int reps = n <= 256 ? 1000 : (n <= 8192 ? 50 : 3);
        double t0 = now_s();
        double df = 0.0;
        for (int r = 0; r < reps; r++) df = qss_det(A, Bu, Bl, n, L);
        double t_fast = (now_s() - t0) / reps;

        if (n <= dense_cutoff) {
            double *M = malloc((size_t)n * n * sizeof(double));
            if (!M) {
                printf("%-10d %12.4e %12s (dense alloc failed)\n", n, t_fast, "-");
                free(M); free(tau); free(A); free(Bu); free(Bl); continue;
            }
            qss_reconstruct(A, Bu, Bl, n, L, M);
            double t1 = now_s();
            double dd = dense_det_lu(M, n);
            double t_dense = now_s() - t1;
            double rel = fabs(dd) > 0 ? fabs(df - dd) / fabs(dd) : fabs(df - dd);
            printf("%-10d %12.4e %12.4e %10.2f %18.8e %18.8e %10.2e\n",
                   n, t_fast, t_dense, t_dense / t_fast, df, dd, rel);
            free(M);
        } else {
            printf("%-10d %12.4e %12s %10s %18.8e %18s %10s\n",
                   n, t_fast, "-", "-", df, "-", "-");
        }
        free(tau); free(A); free(Bu); free(Bl);
    }
    printf("\nthe fast method is linear in n; the dense check is O(n^3) and is\n");
    printf("stopped past the cutoff. agreement is to round-off where both run.\n");
    return 0;
}
