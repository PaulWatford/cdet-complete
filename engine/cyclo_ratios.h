/* cyclo_ratios.h -- part of cdet-c-port v2.31
 * Author: Paul Watford, 2026. MIT license.
 */
#ifndef CYCLO_RATIOS_H
#define CYCLO_RATIOS_H

/* cyclo_ratios: cyclotomic arithmetic at the two modular stabiliser orders.
 *
 * The modular group PSL_2(Z) has two elliptic fixed points with non-trivial
 * stabilisers: tau_1 = i (order 2) and tau_0 = e^(2 pi i / 3) (order 3). The
 * anchor_duality module already computes c=1 CFT objects at those points. This
 * module computes a few exact rational numbers built from the cyclotomic
 * polynomials Phi_d evaluated at the order-3 stabiliser index N = 3, namely the
 * integers k_H = Phi_1(3) = 2, k_grav = Phi_2(3) = 4, Phi_3(3) = 13,
 * Phi_6(3) = 7, and the product Phi_3*Phi_6 = 91.
 *
 * The quantities are returned as exact reduced fractions (numerator and
 * denominator) so they can be checked to be the rationals claimed. This is a
 * numerical demonstration of cyclotomic arithmetic at the modular stabiliser
 * orders and nothing more: no physical claim is asserted, and no connection to
 * particle physics or to the values of physical constants is made here. Any
 * physical interpretation lives entirely in the separate references, not in
 * this code.
 *
 * All integer arithmetic, no dependencies.
 */

/* Phi_d(N): the d-th cyclotomic polynomial for d in {1,2,3,4,6,12}, evaluated
 * at integer N. (Only these divisors of 12 are needed here.) */
long cr_phi(int d, long N);

/* A reduced fraction. */
typedef struct { long num; long den; } cr_frac;

/* The three ratios, as exact reduced fractions at N = 3:
 *   cr_ratio_12: k_H^2 / (k_H^2 + N^2)        = 4/13
 *   cr_ratio_23: N^2 / k_grav^2               = 9/16
 *   cr_ratio_13: 2 / (Phi_3 * Phi_6)          = 2/91
 * Built only from cyclotomic integers; returned reduced. */
cr_frac cr_ratio_12(long N);
cr_frac cr_ratio_23(long N);
cr_frac cr_ratio_13(long N);

/* The cross hub integer Phi_3(N) * Phi_6(N) (= 91 at N = 3). */
long cr_hub(long N);

/* Decimal value of a fraction, for comparison against a tolerance. */
double cr_value(cr_frac f);

#endif /* CYCLO_RATIOS_H */
