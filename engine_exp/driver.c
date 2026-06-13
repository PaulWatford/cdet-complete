/* driver: one call that stacks all four shortcuts for a whole order. See driver.h.
 * Note: the symmetry shortcut is applied to the external-site sum (exact factor L),
 * because it only holds when the external legs rotate with the internal vertices. */

#include "driver.h"
#include "lattices.h"
#include "quad.h"
#include <math.h>

static double g0_lat(int i, int j, double tau, void *ctx) {
 return lattice_G0(i, j, tau, ctx);
}

/* shared params for the nested integrand */
typedef struct {
 int e, s1, s2;
 double tau_out, tau_in, beta;
 int np;
 g0_fn g0; void *lat;
 double t1; /* outer variable, stashed for the inner integral */
} DCtx;

/* ---- order 1: single internal vertex (s1, tau) ---- */
static double f1(double tau, void *vp) {
 DCtx *d = vp;
 Vertex V[1] = { { d->s1, tau } };
 return C_V(V, 1, d->e, d->tau_out, d->e, d->tau_in, d->g0, d->lat);
}

/* ---- order 2: nested. inner over t2 at fixed t1; outer over t1 ---- */
static double f2_inner(double t2, void *vp) {
 DCtx *d = vp;
 Vertex V[2] = { { d->s1, d->t1 }, { d->s2, t2 } };
 return C_V(V, 2, d->e, d->tau_out, d->e, d->tau_in, d->g0, d->lat);
}
static double f2_outer(double t1, void *vp) {
 DCtx *d = vp;
 d->t1 = t1;
 double kinks[3] = { d->tau_out, d->tau_in, t1 }; /* inner kinks: ext + t1 */
 return integrate_piecewise_1d(f2_inner, d, d->np, d->beta, kinks, 3);
}

double cdet_order(int n, int L, double beta, double mu, double t,
 double tau_out, double tau_in, int np) {
 LatticeCtx lat;
 hexring_init(&lat, beta, mu, t);
 double ext_kinks[2] = { tau_out, tau_in };

 if (n == 1) {
 double tot = 0.0;
 for (int s = 0; s < L; s++) {
 DCtx d; d.e=0; d.s1=s; d.s2=0; d.tau_out=tau_out; d.tau_in=tau_in;
 d.beta=beta; d.np=np; d.g0=g0_lat; d.lat=&lat; d.t1=0;
 tot += integrate_piecewise_1d(f1, &d, np, beta, ext_kinks, 2);
 }
 return (double)L * tot; /* 1/1! = 1 */
 }

 if (n == 2) {
 double tot = 0.0;
 for (int s1 = 0; s1 < L; s1++)
 for (int s2 = 0; s2 < L; s2++) {
 DCtx d; d.e=0; d.s1=s1; d.s2=s2; d.tau_out=tau_out; d.tau_in=tau_in;
 d.beta=beta; d.np=np; d.g0=g0_lat; d.lat=&lat; d.t1=0;
 tot += integrate_piecewise_1d(f2_outer, &d, np, beta, ext_kinks, 2);
 }
 return (double)L * tot / 2.0; /* 1/2! */
 }

 return NAN;
}
