/* diagmc.h  (v27)  --  high-order time-integration driver (the gate named in v26).
 *
 * engine/driver.c cdet_order only integrates the vertex times for n=1,2 (NAN beyond), via nested
 * deterministic quadrature. This driver integrates the SAME integrand for ARBITRARY order n by Monte
 * Carlo over the vertex times and sites -- the missing high-order path. It reproduces the frozen
 * baseline cdet_order at n=1,2 within MC error, and returns the first physical high-order terms
 * (n>=3) that the baseline cannot.
 *
 * The order-n term of the (translationally-summed) Green's function is
 *     cdet_order(n) = L * (1/n!) * SUM_{s_1..s_n} INT_0^beta dtau_1..dtau_n  C_V({(s_i,tau_i)}, ...)
 * Sampling (s_i, tau_i) jointly and uniformly gives the unbiased estimator
 *     cdet_order_mc(n) = L * (1/n!) * (L*beta)^n * < C_V >_{uniform (s_i,tau_i)}
 * with a 1-sigma MC standard error returned in *err_out.
 */
#ifndef DIAGMC_H
#define DIAGMC_H
#include <stdint.h>

/* Monte-Carlo estimate of the order-n connected term. Uses hexring_init + lattice_G0 (exactly the
 * integrand of engine/driver.c cdet_order). nmc = number of samples; seed = RNG seed (0 -> default).
 * If err_out != NULL it receives the 1-sigma MC standard error. */
double cdet_order_mc(int n, int L, double beta, double mu, double t,
                     double tau_out, double tau_in,
                     long nmc, uint64_t seed, double *err_out);

#endif
