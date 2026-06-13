/* quad: integrate without tripping over the kinks.
 *
 * The thing we integrate has sharp corners wherever two vertex times line up,
 * and a smooth integration rule run straight across a corner loses its accuracy,
 * like trying to trace a bent wire with a single straight ruler. So we cut the
 * range at the corners and lay a fresh rule down on each smooth piece. Keeps the
 * precision that makes the laptop-sized calculation trustworthy.
 */
#ifndef QUAD_H
#define QUAD_H

/* Gauss-Legendre nodes/weights on [a,b] for np points (np <= 64).
 * Caller provides arrays of length np. */
void gl_grid_1d(int np, double a, double b, double *nodes, double *weights);

/* Ordered breakpoints in [0,beta]: {0, beta} union {kinks in (0,beta)}, sorted,
 * deduplicated. Writes into out[] (caller array length >= n_kinks+2); returns
 * the number of breakpoints written. */
int split_interval(double beta, const double *kinks, int n_kinks, double *out);

/* Piecewise GL integral of a 1-D function f over [0,beta], splitting at kinks. */
double integrate_piecewise_1d(double (*f)(double, void*), void *ctx,
 int np, double beta,
 const double *kinks, int n_kinks);

/* Piecewise GL integral of a 2-D function f over [0,beta]^2, splitting both
 * axes at their kink sets. */
double integrate_piecewise_2d(double (*f)(double, double, void*), void *ctx,
 int np, double beta,
 const double *kinks1, int n_kinks1,
 const double *kinks2, int n_kinks2);

#endif /* QUAD_H */
