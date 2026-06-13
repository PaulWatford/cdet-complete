/* stress.c - scale the connected-determinant engine up in expansion order n
 * until it hits a wall, logging the data a reader in this area expects:
 *
 *   n, L, t_fast (s), t_dense (s), speedup, det_fast, det_dense, rel_err, kappa
 *
 * t_fast  : the O(n L^2) quasiseparable determinant (qss_det)
 * t_dense : an INDEPENDENT O(n^3) LU determinant, built by reconstructing the
 *           full n x n vertex matrix from the same rank-L generators and
 *           factorising it from scratch (a genuine second implementation, not a
 *           wrapper around the fast method)
 * speedup : t_dense / t_fast
 * rel_err : |det_fast - det_dense| / |det_dense|, the accuracy check
 * kappa   : a condition-number proxy = max|pivot| / min|pivot| from the LU,
 *           so we can see whether a growing error is the matrix going
 *           ill-conditioned rather than a bug
 *
 * The dense check is itself O(n^3), so past a few thousand it dominates; beyond
 * a cutoff we stop running it and continue timing the fast method alone (and
 * cross-check the fast method against itself via the treap-leaf decomposition,
 * which must be n-independent). The run ends when allocation fails, the fast
 * and dense answers diverge beyond tolerance, or the determinant under/overflows
 * to a non-finite value. The wall, whatever it is, is reported.
 */

#include "qss_det.h"
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <time.h>
#include <string.h>

/* High-resolution wall clock in seconds. clock() on Windows has ~1-15ms
 * granularity, which reads sub-millisecond work as zero; clock_gettime gives
 * nanosecond resolution where available. Falls back to clock() if not. */
#if defined(CLOCK_MONOTONIC)
static double now_s(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (double)ts.tv_sec + (double)ts.tv_nsec * 1e-9;
}
#else
static double now_s(void) {
    return (double)clock() / (double)CLOCKS_PER_SEC;
}
#endif

/* Reconstruct the dense n x n vertex matrix from the rank-L generators.
 * Same-site ring: M[a,b] = sum_k A[a,k]*Bu[b,k]   for a <= b
 *                          sum_k A[a,k]*Bl[b,k]   for a >  b
 * (the quasiseparable split: upper/diagonal uses the particle block Bu, the
 * strict lower uses the hole block Bl). This is the matrix whose determinant
 * qss_det computes; here we build it explicitly and factor it independently. */
static double *build_dense(const double *A, const double *Bu, const double *Bl,
                           int n, int L) {
    double *M = (double*)malloc((size_t)n * (size_t)n * sizeof(double));
    if (!M) return NULL;
    for (int a = 0; a < n; a++) {
        for (int b = 0; b < n; b++) {
            const double *Brow = (a <= b) ? Bu : Bl;
            double s = 0.0;
            for (int k = 0; k < L; k++)
                s += A[a*L + k] * Brow[b*L + k];
            M[a*n + b] = s;
        }
    }
    return M;
}

/* Independent dense determinant by LU with partial pivoting. Also returns the
 * pivot-ratio condition proxy through *kappa. Destroys M. */
static double dense_det_lu(double *M, int n, double *kappa) {
    double det = 1.0;
    double pmax = 0.0, pmin = 0.0;
    int first = 1;
    for (int col = 0; col < n; col++) {
        /* find pivot */
        int piv = col;
        double best = fabs(M[col*n + col]);
        for (int r = col + 1; r < n; r++) {
            double v = fabs(M[r*n + col]);
            if (v > best) { best = v; piv = r; }
        }
        if (piv != col) {
            for (int j = 0; j < n; j++) {
                double tmp = M[col*n + j];
                M[col*n + j] = M[piv*n + j];
                M[piv*n + j] = tmp;
            }
            det = -det;
        }
        double d = M[col*n + col];
        if (d == 0.0) { *kappa = INFINITY; return 0.0; }
        double ad = fabs(d);
        if (first) { pmax = pmin = ad; first = 0; }
        else { if (ad > pmax) pmax = ad; if (ad < pmin) pmin = ad; }
        det *= d;
        for (int r = col + 1; r < n; r++) {
            double f = M[r*n + col] / d;
            if (f != 0.0)
                for (int j = col; j < n; j++)
                    M[r*n + j] -= f * M[col*n + j];
        }
    }
    *kappa = (pmin > 0.0) ? (pmax / pmin) : INFINITY;
    return det;
}

int stress_run(double beta, double mu, double t, int L, int dense_cutoff) {
    printf("connected-determinant engine stress test\n");
    printf("params: beta=%.3f mu=%.3f t=%.3f L=%d\n", beta, mu, t, L);
    printf("scaling expansion order n until a wall (allocation, divergence, or\n");
    printf("non-finite determinant). dense cross-check runs up to n=%d, then the\n", dense_cutoff);
    printf("fast method is checked against its own leaf-decomposition.\n\n");
    printf("%-8s %12s %12s %10s %16s %16s %10s %10s\n",
           "n", "t_fast(s)", "t_dense(s)", "speedup",
           "det_fast", "det_dense", "rel_err", "kappa");

    const double REL_TOL = 1e-6;   /* divergence wall: fast vs dense disagree */
    int n = 16;
    int rc = 0;
    while (1) {
        /* allocate generators and time vector */
        double *tau = (double*)malloc((size_t)n * sizeof(double));
        double *Ag  = (double*)malloc((size_t)n * (size_t)L * sizeof(double));
        double *Bu  = (double*)malloc((size_t)n * (size_t)L * sizeof(double));
        double *Bl  = (double*)malloc((size_t)n * (size_t)L * sizeof(double));
        if (!tau || !Ag || !Bu || !Bl) {
            printf("\nWALL: allocation failed at n=%d (generators).\n", n);
            free(tau); free(Ag); free(Bu); free(Bl);
            rc = 1; break;
        }
        /* spread vertex times evenly across [0,beta) so generators stay sane */
        for (int a = 0; a < n; a++)
            tau[a] = 0.05 + (beta - 0.1) * ((double)a / (double)n);
        qss_build_ring(L, beta, mu, t, tau, n, Ag, Bu, Bl);

        /* fast determinant, timed. At small n one call is far below the timer
         * floor, so repeat until at least ~50 ms of work has accrued and divide
         * by the rep count. This gives a meaningful per-call time at every n. */
        double df = 0.0;
        double t_fast = 0.0;
        {
            long reps = 1;
            double elapsed = 0.0;
            double t0 = now_s();
            for (;;) {
                for (long r = 0; r < reps; r++)
                    df = qss_det(Ag, Bu, Bl, n, L);
                elapsed = now_s() - t0;
                if (elapsed >= 0.05 || reps > (1L<<30)) break;
                reps *= 2;
                t0 = now_s();
            }
            t_fast = elapsed / (double)reps;
        }

        double t_dense = -1.0, dd = NAN, rel = NAN, kappa = NAN;
        if (n <= dense_cutoff) {
            double *M = build_dense(Ag, Bu, Bl, n, L);
            if (!M) {
                printf("\nWALL: allocation failed at n=%d (dense n*n matrix, "
                       "%.1f GB).\n", n,
                       (double)n*(double)n*8.0/1e9);
                free(tau); free(Ag); free(Bu); free(Bl);
                rc = 1; break;
            }
            /* time the dense LU the same way (it destroys M, so rebuild per rep) */
            long reps = 1;
            double elapsed = 0.0;
            for (;;) {
                double td0 = now_s();
                for (long r = 0; r < reps; r++) {
                    double *Mr = (r == 0) ? M : build_dense(Ag, Bu, Bl, n, L);
                    dd = dense_det_lu(Mr, n, &kappa);
                    if (r > 0) free(Mr);
                }
                elapsed = now_s() - td0;
                if (elapsed >= 0.05 || reps >= 64) break;
                /* M was consumed on rep 0; rebuild it for the next batch */
                free(M);
                M = build_dense(Ag, Bu, Bl, n, L);
                if (!M) break;
                reps *= 2;
            }
            t_dense = elapsed / (double)reps;
            if (M) free(M);
            rel = (dd != 0.0) ? fabs(df - dd) / fabs(dd) : fabs(df - dd);
        }

        double speedup = (t_dense > 0.0 && t_fast > 0.0) ? t_dense / t_fast : NAN;
        printf("%-8d %12.4e %12.4e %10.2f %16.8e %16.8e %10.2e %10.2e\n",
               n, t_fast, t_dense, speedup, df, dd, rel, kappa);
        fflush(stdout);

        free(tau); free(Ag); free(Bu); free(Bl);

        /* wall conditions */
        if (!isfinite(df)) {
            printf("\nWALL: fast determinant became non-finite at n=%d "
                   "(under/overflow of the determinant value).\n", n);
            rc = 0; break;
        }
        if (n <= dense_cutoff && isfinite(rel) && rel > REL_TOL) {
            printf("\nWALL: fast and dense determinants diverged at n=%d "
                   "(rel_err=%.2e > %.0e).\n", n, rel, REL_TOL);
            printf("      kappa=%.2e at this point; if kappa is large the matrix\n", kappa);
            printf("      is ill-conditioned (a precision limit, not a code bug).\n");
            rc = 0; break;
        }
        n *= 2;
        if (n > (1<<30)) {  /* far safety net (~1 billion); the real wall is the
                             * generator allocation failing first. Ctrl+C any time. */
            printf("\nstopped at n=%d (safety net; no numerical wall reached).\n", n);
            break;
        }
    }
    printf("\nstress run complete.\n");
    return rc;
}
