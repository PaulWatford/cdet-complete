/* bench_parallel.c -- part of cdet-c-port v2.31
 * Author: Paul Watford, 2026. MIT license.
 */
/* bench_parallel: time a batch of independent determinants computed serially
 * versus through the parallel batch path, and report the speedup. Built with
 * -fopenmp it uses all available threads; without it the batch path runs
 * serially and the speedup is about 1. Run with: make bench_parallel
 *
 * Run this on real hardware to see the multi-core curve; inside a single-core
 * or container build the speedup will be near 1 by design. */

#include "qss_det.h"
#include "qss_parallel.h"
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
    int n = 4096;      /* size of each determinant */
    int B = 256;       /* how many determinants in the batch */

    printf("parallel batch-determinant benchmark\n");
    printf("params: beta=%.3f mu=%.3f t=%.3f L=%d  batch=%d  n=%d\n", beta, mu, t, L, B, n);
    printf("threads available to the batch path: %d\n\n", qss_parallel_threads());

    /* build B independent generator sets (slightly shifted vertex times) */
    double **A  = malloc((size_t)B * sizeof(double *));
    double **Bu = malloc((size_t)B * sizeof(double *));
    double **Bl = malloc((size_t)B * sizeof(double *));
    int *nn = malloc((size_t)B * sizeof(int));
    double *out = malloc((size_t)B * sizeof(double));
    if (!A || !Bu || !Bl || !nn || !out) { printf("alloc failed\n"); return 1; }

    for (int b = 0; b < B; b++) {
        nn[b] = n;
        A[b]  = malloc((size_t)n * L * sizeof(double));
        Bu[b] = malloc((size_t)n * L * sizeof(double));
        Bl[b] = malloc((size_t)n * L * sizeof(double));
        double *tau = malloc((size_t)n * sizeof(double));
        double shift = 0.001 * b;
        for (int a = 0; a < n; a++) tau[a] = beta * (a + 0.5 + shift) / (n + 1);
        qss_build_ring(L, beta, mu, t, tau, n, A[b], Bu[b], Bl[b]);
        free(tau);
    }

    /* serial: one determinant at a time */
    double t0 = now_s();
    double acc_serial = 0.0;
    for (int b = 0; b < B; b++) acc_serial += qss_det(A[b], Bu[b], Bl[b], n, L);
    double t_serial = now_s() - t0;

    /* parallel batch path */
    double t1 = now_s();
    qss_det_batch((const double *const *)A, (const double *const *)Bu,
                  (const double *const *)Bl, nn, L, B, out);
    double t_batch = now_s() - t1;

    double acc_batch = 0.0;
    for (int b = 0; b < B; b++) acc_batch += out[b];

    printf("serial total time : %.4e s\n", t_serial);
    printf("batch  total time : %.4e s\n", t_batch);
    printf("speedup           : %.2f x\n", t_serial / t_batch);
    printf("answer check (sum) serial=%.10e batch=%.10e rel_err=%.2e\n",
           acc_serial, acc_batch,
           fabs(acc_serial) > 0 ? fabs(acc_serial - acc_batch) / fabs(acc_serial) : 0.0);
    printf("\n(speedup near 1 means a serial build or one core; on multi-core\n");
    printf("hardware built with make omp the batch path uses all threads.)\n");

    for (int b = 0; b < B; b++) { free(A[b]); free(Bu[b]); free(Bl[b]); }
    free(A); free(Bu); free(Bl); free(nn); free(out);
    return 0;
}
