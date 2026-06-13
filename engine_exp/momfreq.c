/* momfreq: the same propagator written in waves (k, i*omega_n) instead of site/time. See momfreq.h. */

#include "momfreq.h"
#include <math.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

void momfreq_init(MomFreqCtx *c, int L, double beta, double mu, double t, int nmax) {
 c->L = L; c->beta = beta; c->mu = mu; c->t = t;
 c->nmax = (nmax > 0) ? nmax : 4000;
}

double momfreq_eps_k(const MomFreqCtx *c, int k) {
 return -2.0 * c->t * cos(2.0 * M_PI * (double)k / (double)c->L);
}

void momfreq_G_k_iwn(const MomFreqCtx *c, int k, int n, double *re, double *im) {
 /* G = 1/(i w_n - xi) = (-xi - i w_n)/(xi^2 + w_n^2) ... just do it:
 * 1/(i w_n - xi) = (-xi - i w_n)/(xi^2 + w_n^2) */
 double xi = momfreq_eps_k(c, k) - c->mu;
 double wn = (2.0*n + 1.0) * M_PI / c->beta;
 double denom = xi*xi + wn*wn;
 *re = -xi / denom;
 *im = -wn / denom;
}

double momfreq_G0_site(const MomFreqCtx *c, int i, int j, double tau) {
 int L = c->L, nmax = c->nmax;
 double beta = c->beta;
 double total_re = 0.0; /* imaginary part cancels to round-off */

 /* Fold tau into the fundamental domain [0, beta) and carry the
 * antiperiodic sign G(tau + beta) = -G(tau). The Matsubara tail constant
 * (-1/2) and the reconstruction are only valid for 0 <= tau < beta; the
 * sign flip across each beta-window is applied here, exactly mirroring the
 * reference G0_atom folding. This is where the odd-frequency comb's flip
 * is realised in the reconstruction. */
 double sgn = 1.0;
 while (tau >= beta) { tau -= beta; sgn = -sgn; }
 while (tau < 0.0) { tau += beta; sgn = -sgn; }

 for (int k = 0; k < L; k++) {
 double xi = momfreq_eps_k(c, k) - c->mu;
 double gt_re = 0.0, gt_im = 0.0;
 for (int n = -nmax; n < nmax; n++) {
 double wn = (2.0*n + 1.0) * M_PI / beta;
 double denom = xi*xi + wn*wn;
 double f_re = -xi / denom, f_im = -wn / denom;
 double t_re = 0.0, t_im = -1.0/wn;
 double d_re = f_re - t_re, d_im = f_im - t_im;
 double cc = cos(wn*tau), ss = sin(wn*tau);
 gt_re += d_re*cc + d_im*ss;
 gt_im += d_im*cc - d_re*ss;
 }
 gt_re = gt_re/beta - 0.5; /* exact tail inverse for 0<=tau<beta */
 gt_im = gt_im/beta;
 double ph = 2.0*M_PI*(double)k*(double)(i-j)/(double)L;
 double pc = cos(ph), ps = sin(ph);
 total_re += (pc*gt_re - ps*gt_im) / (double)L;
 }
 return sgn * total_re;
}
