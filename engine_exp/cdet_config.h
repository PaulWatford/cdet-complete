/* cdet_config.h  (v34) -- one configurable interface over the high-order MC driver.
 *
 * v27's cdet_order_mc is the plain Monte-Carlo estimator of the order-n term. This wraps it and the
 * two validated acceleration paths behind a single call with a mode toggle, so the scattered sandbox
 * POCs become switchable options instead of separate programs:
 *
 *   CDET_PLAIN   : the v27 estimator, unchanged (the reference). Bit-identical to cdet_order_mc.
 *   CDET_BLOCKED : per-sample C_V via the v31 out-of-core bit-split blocking (RAM bounded to O(2^nL),
 *                  the 2^n array on disk). For n so large a single flat C_V overflows RAM; same value
 *                  as PLAIN (the blocked arithmetic is the exact direct sum, matching flat to ~1e-20).
 *   CDET_CVAR    : control variate -- subtract a correlated reference C_V (shifted-mu propagator) with
 *                  its mean estimated in an independent pilot pass. Unbiased for any coefficient; the
 *                  variance reduction is 1/(1-rho^2). HONEST: with the current simple reference rho is
 *                  modest at high order (v32), so this does not net-win once the reference's own cost
 *                  is counted -- it is the correct plumbing, ready for a high-correlation reference
 *                  (atomic counterterm / learned Luttinger-liquid G), which is the documented build-ahead.
 *
 * The butterfly / fast-subset-convolution POC is deliberately NOT wired (shelved v29: wrong trade for
 * accuracy + RAM).
 */
#ifndef CDET_CONFIG_H
#define CDET_CONFIG_H
#include <stdint.h>

typedef enum { CDET_PLAIN = 0, CDET_BLOCKED = 1, CDET_CVAR = 2 } CdetMode;

typedef struct {
    CdetMode mode;
    /* CDET_BLOCKED */
    int         nL;        /* low-bit split (1..n-1); peak RAM ~ 3 * 2^nL doubles. 0 -> auto (n/2). */
    const char *scratch;   /* scratch directory for on-disk blocks. NULL -> "./blk_scratch". */
    /* CDET_CVAR */
    double cvar_mu_shift;  /* reference propagator mu offset (the control variate's surrogate). */
    long   cvar_pilot;     /* independent samples to estimate the reference mean E[Y]. 0 -> nmc. */
    double cvar_rho_out;   /* OUT: measured correlation rho(f, Y) (NaN if not CVAR). */
    double cvar_vr_out;    /* OUT: measured variance reduction 1/(1-rho^2) (NaN if not CVAR). */
} CdetConfig;

/* Default config = plain. */
static inline CdetConfig cdet_config_default(void) {
    CdetConfig c; c.mode = CDET_PLAIN; c.nL = 0; c.scratch = 0;
    c.cvar_mu_shift = 0.3; c.cvar_pilot = 0; c.cvar_rho_out = 0.0/0.0; c.cvar_vr_out = 0.0/0.0;
    return c;
}

/* Configurable order-n MC estimate. With cfg==NULL or cfg->mode==CDET_PLAIN this is bit-identical to
 * cdet_order_mc(...). err_out (if non-NULL) receives the 1-sigma MC standard error. */
double cdet_order_mc_cfg(int n, int L, double beta, double mu, double t,
                         double tau_out, double tau_in,
                         long nmc, uint64_t seed,
                         CdetConfig *cfg, double *err_out);

#endif
