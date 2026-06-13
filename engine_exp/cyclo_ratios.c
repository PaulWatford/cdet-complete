/* cyclo_ratios.c -- part of cdet-c-port v2.31
 * Author: Paul Watford, 2026. MIT license.
 */
/* cyclo_ratios.c: exact cyclotomic arithmetic at the modular stabiliser orders.
 * See cyclo_ratios.h. Numerical demonstration only; no physical claim. */

#include "cyclo_ratios.h"

long cr_phi(int d, long N) {
    switch (d) {
        case 1:  return N - 1;
        case 2:  return N + 1;
        case 3:  return N*N + N + 1;
        case 4:  return N*N + 1;
        case 6:  return N*N - N + 1;
        case 12: return N*N*N*N - N*N + 1;
        default: return 0;
    }
}

/* greatest common divisor, for reducing fractions */
static long cr_gcd(long a, long b) {
    if (a < 0) a = -a;
    if (b < 0) b = -b;
    while (b) { long t = a % b; a = b; b = t; }
    return a ? a : 1;
}

static cr_frac cr_make(long num, long den) {
    long g = cr_gcd(num, den);
    cr_frac f;
    f.num = num / g;
    f.den = den / g;
    if (f.den < 0) { f.num = -f.num; f.den = -f.den; }
    return f;
}

cr_frac cr_ratio_12(long N) {
    long kH = cr_phi(1, N);                 /* 2 at N=3 */
    return cr_make(kH*kH, kH*kH + N*N);     /* 4/13 */
}

cr_frac cr_ratio_23(long N) {
    long kg = cr_phi(2, N);                 /* 4 at N=3 */
    return cr_make(N*N, kg*kg);             /* 9/16 */
}

cr_frac cr_ratio_13(long N) {
    long hub = cr_phi(3, N) * cr_phi(6, N); /* 91 at N=3 */
    return cr_make(2, hub);                 /* 2/91 */
}

long cr_hub(long N) {
    return cr_phi(3, N) * cr_phi(6, N);
}

double cr_value(cr_frac f) {
    return (double)f.num / (double)f.den;
}
