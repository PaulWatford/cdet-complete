/* cdet_stable.c (v108) -- see cdet_stable.h. */
#include "cdet_stable.h"
#include <math.h>

double softplus_stable(double x) {            /* log(1+exp(x)) without overflow */
    if (x > 0.0) return x + log1p(exp(-x));
    return log1p(exp(x));
}

double G0_atom_stable(double tau, double beta, double mu) {
    double xi = -mu;
    while (tau > beta)  tau -= 2.0 * beta;     /* antiperiodic fold, period 2 beta */
    while (tau <= -beta) tau += 2.0 * beta;
    if (tau > 0.0)        /* particle: (1-nf) = exp(-softplus(-beta xi)) */
        return -exp(-xi * tau - softplus_stable(-beta * xi));
    else if (tau < 0.0)   /* hole: nf = exp(-softplus(beta xi)) */
        return  exp(-xi * tau - softplus_stable(beta * xi));
    else                  /* tau == 0 -> 0^- : n_F */
        return  exp(-softplus_stable(beta * xi));
}
