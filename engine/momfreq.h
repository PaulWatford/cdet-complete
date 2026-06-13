/* momfreq: the propagator written in waves instead of positions.
 *
 * Same free propagator, expressed in momentum-and-frequency (k, i*omega_n)
 * instead of site-and-time. Some quantities are simply cleaner to read in that
 * language, and the antiperiodic-in-time sign flip falls out of the frequency
 * comb automatically instead of being bolted on by hand. A second lens on the
 * same object, kept for cross-checks and convenience.
 */
#ifndef MOMFREQ_H
#define MOMFREQ_H

typedef struct {
 double beta, mu, t;
 int L; /* number of sites (ring) */
 int nmax; /* Matsubara cutoff: sum n in [-nmax, nmax) */
} MomFreqCtx;

void momfreq_init(MomFreqCtx *c, int L, double beta, double mu, double t, int nmax);

/* ring dispersion eps_k = -2 t cos(2 pi k / L) */
double momfreq_eps_k(const MomFreqCtx *c, int k);

/* free propagator in the diagonal basis: 1/(i w_n - (eps_k - mu)).
 * returns real/imag parts (it is complex in general). */
void momfreq_G_k_iwn(const MomFreqCtx *c, int k, int n, double *re, double *im);

/* reconstruct the imaginary-time site propagator G0(i,j;tau) from the
 * diagonal (k, i omega_n) data, with analytic tail subtraction. Returns the
 * real part (the imaginary part is ~0 to round-off and is discarded). */
double momfreq_G0_site(const MomFreqCtx *c, int i, int j, double tau);

#endif /* MOMFREQ_H */
