/* cdet_stable.h (v108) -- the LOG-DOMAIN stable atomic propagator in C.
 *
 * The frozen engine's G0_atom (engine/cdet_engine.c) uses the naive form
 *   tau>0: -(1 - n_F(xi,beta)) * exp(-xi tau)
 * which is correct at benign beta (the engine is ED-validated there, 194/194) but, as v103
 * discovered in Python, catastrophically cancels at DEEP beta: for a far occupied level
 * (xi << 0), (1 - n_F) computes as 1.0 - 1.0 = 0 and the antiperiodic image VANISHES. This
 * header provides the float64-stable replacement, assembling the exponent in the LOG DOMAIN
 * before exp (softplus = log(1+exp)), so every term is bounded and the image is preserved.
 * Certified against the Python stable_cdet / mpmath path (cdet_stable_test.c). The frozen
 * engine is NOT modified; this is the additive deep-beta-correct C propagator. */
#ifndef CDET_STABLE_H
#define CDET_STABLE_H
double softplus_stable(double x);                         /* log(1+exp(x)), overflow-safe      */
double G0_atom_stable(double tau, double beta, double mu);/* log-domain atomic propagator      */
#endif
