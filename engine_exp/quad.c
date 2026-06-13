/* quad: cut the integration range at the corners, integrate each smooth piece. See quad.h. */

#include "quad.h"
#include <math.h>
#include <stdlib.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

/* Gauss-Legendre nodes/weights on [-1,1] via Newton iteration on Legendre P_np,
 * then mapped to [a,b]. Matches numpy.polynomial.legendre.leggauss to ~1e-15. */
void gl_grid_1d(int np, double a, double b, double *nodes, double *weights) {
 for (int i = 0; i < np; i++) {
 /* initial guess: Chebyshev-like */
 double x = cos(M_PI * (i + 0.75) / (np + 0.5));
 double dp = 0.0;
 for (int it = 0; it < 100; it++) {
 /* evaluate Legendre P_np(x) and derivative via recurrence */
 double p0 = 1.0, p1 = x;
 for (int k = 2; k <= np; k++) {
 double p2 = ((2.0*k - 1.0)*x*p1 - (k - 1.0)*p0) / k;
 p0 = p1; p1 = p2;
 }
 dp = np * (x*p1 - p0) / (x*x - 1.0);
 double dx = -p1 / dp;
 x += dx;
 if (fabs(dx) < 1e-15) break;
 }
 /* node on [-1,1] is x; weight = 2/((1-x^2) dp^2) */
 double w = 2.0 / ((1.0 - x*x) * dp * dp);
 /* map to [a,b]; fill symmetric pair ordering left-to-right */
 nodes[i] = 0.5*(b - a)*x + 0.5*(a + b);
 weights[i] = 0.5*(b - a)*w;
 }
}

static int cmp_d(const void *x, const void *y) {
 double a = *(const double*)x, b = *(const double*)y;
 return (a < b) ? -1 : (a > b) ? 1 : 0;
}

int split_interval(double beta, const double *kinks, int n_kinks, double *out) {
 int m = 0;
 out[m++] = 0.0; out[m++] = beta;
 for (int i = 0; i < n_kinks; i++)
 if (kinks[i] > 0.0 && kinks[i] < beta) out[m++] = kinks[i];
 qsort(out, m, sizeof(double), cmp_d);
 /* dedupe */
 int w = 0;
 for (int i = 0; i < m; i++)
 if (w == 0 || fabs(out[i] - out[w-1]) > 1e-14) out[w++] = out[i];
 return w;
}

double integrate_piecewise_1d(double (*f)(double, void*), void *ctx,
 int np, double beta,
 const double *kinks, int n_kinks) {
 double bp[80]; int nb = split_interval(beta, kinks, n_kinks, bp);
 double nodes[np], wts[np];   /* v34: sized to np (was fixed [64], overflowed for np>64) */
 double total = 0.0;
 for (int p = 0; p < nb - 1; p++) {
 gl_grid_1d(np, bp[p], bp[p+1], nodes, wts);
 for (int i = 0; i < np; i++) total += wts[i] * f(nodes[i], ctx);
 }
 return total;
}

double integrate_piecewise_2d(double (*f)(double, double, void*), void *ctx,
 int np, double beta,
 const double *kinks1, int n_kinks1,
 const double *kinks2, int n_kinks2) {
 double bp1[80], bp2[80];
 int nb1 = split_interval(beta, kinks1, n_kinks1, bp1);
 int nb2 = split_interval(beta, kinks2, n_kinks2, bp2);
 double n1[np], w1[np], n2[np], w2[np];   /* v34: sized to np (was fixed [64]) */
 double total = 0.0;
 for (int p = 0; p < nb1 - 1; p++) {
 gl_grid_1d(np, bp1[p], bp1[p+1], n1, w1);
 for (int q = 0; q < nb2 - 1; q++) {
 gl_grid_1d(np, bp2[q], bp2[q+1], n2, w2);
 for (int i = 0; i < np; i++)
 for (int j = 0; j < np; j++)
 total += w1[i] * w2[j] * f(n1[i], n2[j], ctx);
 }
 }
 return total;
}
