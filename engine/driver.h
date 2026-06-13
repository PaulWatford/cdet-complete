/* driver: one call that does a whole order of the calculation.
 *
 * The single button that stacks all four shortcuts together for perturbative
 * order n: closed-form propagators, the connected-determinant engine, the
 * symmetry shortcut, and the kink-aware integration. Hands back the order-n
 * contribution to a translation-invariant observable. Built so a user drives the
 * physics with one function, not by wiring the four pieces together by hand.
 *
 * Careful: the symmetry shortcut only holds when the external legs rotate WITH
 * the internal vertices, so the reduction is applied to the external-site sum
 * (an exact factor of L), not the internal sites. (Reducing the internal sites
 * with the external one pinned gives the wrong answer; we tested it.)
 */
#ifndef DRIVER_H
#define DRIVER_H

#include "cdet_engine.h"

/* order-n contribution to the translation-invariant observable, for n in {1,2}.
 * L : ring size (6 for hexring)
 * beta,mu,t : model params
 * tau_out,tau_in : external leg times in (0,beta)
 * np_per_piece : Gauss-Legendre points per smooth sub-interval
 * Uses lattice_G0 (closed-form propagator) + C_V + symmetry + kink-split quad.
 * Returns O_n. For n outside {1,2} returns NAN. */
double cdet_order(int n, int L, double beta, double mu, double t,
 double tau_out, double tau_in, int np_per_piece);

#endif /* DRIVER_H */
