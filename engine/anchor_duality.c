/* anchor_duality.c -- part of cdet-c-port v2.31
 * Author: Paul Watford, 2026. MIT license.
 */
/* anchor_duality.c: the second-anchor companion. See anchor_duality.h. */

#include "anchor_duality.h"
#include <math.h>
#include <complex.h>
#include <stdlib.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

double complex ad_dedekind_eta(double complex tau, int nmax) {
    /* eta(tau) = exp(i pi tau / 12) * prod_{n>=1} (1 - q^n),  q = exp(2 pi i tau).
     * The product converges fast because |q| = exp(-2 pi Im tau) < 1. */
    double complex q = cexp(2.0 * M_PI * I * tau);
    double complex prod = 1.0 + 0.0 * I;
    double complex qn = 1.0 + 0.0 * I;
    for (int n = 1; n < nmax; n++) {
        qn *= q;                 /* qn = q^n */
        prod *= (1.0 - qn);
    }
    return cexp(I * M_PI * tau / 12.0) * prod;
}

double ad_Z_boson(double complex tau, double R, int Nmax) {
    /* Z(tau, R) = (1/|eta|^2) * sum_{n,w} q^h qbar^hbar,
     *   h    = (1/2)(n/R + w R/2)^2,  hbar = (1/2)(n/R - w R/2)^2,
     *   q = exp(2 pi i tau),  qbar = exp(-2 pi i conj(tau)).
     * n = momentum mode, w = winding mode (the two cycles of the torus). */
    double complex q  = cexp(2.0 * M_PI * I * tau);
    double complex qb = cexp(-2.0 * M_PI * I * conj(tau));
    double complex logq  = clog(q);    /* explicit principal log, computed once */
    double complex logqb = clog(qb);
    double complex eta = ad_dedekind_eta(tau, 300);
    double aeta2 = creal(eta * conj(eta));      /* |eta|^2, real */

    double complex s = 0.0 + 0.0 * I;
    for (int n = -Nmax; n <= Nmax; n++) {
        for (int w = -Nmax; w <= Nmax; w++) {
            double a = n / R + w * R / 2.0;
            double b = n / R - w * R / 2.0;
            double h  = 0.5 * a * a;
            double hb = 0.5 * b * b;
            /* q^h qbar^hbar via explicit log-space: cexp(h*logq + hb*logqb).
             * Identical to cpow on the imaginary axis; branch-cut-safe for
             * general tau (cpow's internal clog can jump across arg = +-pi). */
            s += cexp(h * logq + hb * logqb);
        }
    }
    return creal(s) / aeta2;     /* real on the imaginary axis */
}

double ad_self_dual_radius(void) {
    return sqrt(2.0);            /* T-duality fixed radius; boson = Dirac fermion here */
}

double complex ad_anchor_tau1(void) {
    return 0.0 + 1.0 * I;        /* tau_1 = i */
}

double complex ad_anchor_tau0(void) {
    return cexp(2.0 * M_PI * I / 3.0);   /* tau_0 = e^(2 pi i / 3) */
}

double complex ad_map_S(double complex tau) {
    return -1.0 / tau;           /* S: order 2, fixes tau_1 = i */
}

double complex ad_map_ST(double complex tau) {
    return -1.0 / (tau + 1.0);   /* ST: order 3, fixes tau_0 */
}

/* T-duality residual: the compact boson obeys Z(tau, R) = Z(tau, 2/R) in the
 * alpha' = 2 convention (self-dual at R = sqrt(2)). Returns the absolute
 * difference |Z(tau,R) - Z(tau,2/R)|, zero up to round-off for any R.
 * A direct check of the duality the c=1 line is built on. */
double ad_Tduality_residual(double complex tau, double R, int Nmax) {
    double z1 = ad_Z_boson(tau, R, Nmax);
    double z2 = ad_Z_boson(tau, 2.0 / R, Nmax);
    double d = z1 - z2;
    return d < 0.0 ? -d : d;
}

/* Boson Z evaluated around the tau_0 point under the order-3 map ST.
 * out[0] = Z at tau_0, out[1] = Z at ST(tau_0), out[2] = Z at ST(ST(tau_0)).
 * tau_0 is the fixed point of ST, so the three points coincide and the three
 * Z values are equal; the spread is a check that ST fixes tau_0 and that Z is
 * modular invariant (the tau_0-side analogue of S fixing tau_1). Returns the
 * value at tau_0. */
double ad_Z_boson_tau0_orbit(double R, int Nmax, double out[3]) {
    double complex t0 = ad_anchor_tau0();
    double complex t1 = ad_map_ST(t0);
    double complex t2 = ad_map_ST(t1);
    out[0] = ad_Z_boson(t0, R, Nmax);
    out[1] = ad_Z_boson(t1, R, Nmax);
    out[2] = ad_Z_boson(t2, R, Nmax);
    return out[0];
}

/* Single-particle energies of a nearest-neighbour ring, sorted ascending.
 * eps_k = -2 t cos(2 pi k / L + flux/L), k = 0 .. L-1. Caller frees. */
static void ring_spectrum(int L, double flux, double t, double *eps) {
    for (int k = 0; k < L; k++) {
        eps[k] = -2.0 * t * cos(2.0 * M_PI * k / (double)L + flux / (double)L);
    }
    /* simple insertion sort (L is modest in practice) */
    for (int i = 1; i < L; i++) {
        double v = eps[i]; int j = i - 1;
        while (j >= 0 && eps[j] > v) { eps[j+1] = eps[j]; j--; }
        eps[j+1] = v;
    }
}

double ad_lattice_gap(int L, double flux, double t) {
    double *eps = (double*)malloc((size_t)L * sizeof(double));
    if (!eps) return -1.0;
    ring_spectrum(L, flux, t, eps);
    double gap = eps[L/2] - eps[L/2 - 1];   /* half-filling HOMO-LUMO */
    free(eps);
    return gap;
}

/* Finite-L free-fermion ring partition function at modular parameter tau,
 * with the non-universal filled-sea energy removed. Fermi velocity 2t.
 * Returns Z; the caller forms the S-ratio. */
static double ring_Z(int L, const double *eps, double t, double complex tau) {
    double vF = 2.0 * t;
    double beta = cimag(tau) * (double)L / vF;
    double logZ = 0.0, E0 = 0.0;
    for (int k = 0; k < L; k++) {
        double e = eps[k];
        /* ln(1 + exp(-beta e)), computed stably */
        double x = -beta * e;
        logZ += (x > 0.0) ? (x + log1p(exp(-x))) : log1p(exp(x));
        if (e < 0.0) E0 += -e;     /* filled-sea energy = sum of |negative eps| */
    }
    return exp(logZ - beta * E0);
}

double ad_lattice_S_ratio(int L, double flux, double t, double complex tau) {
    double *eps = (double*)malloc((size_t)L * sizeof(double));
    if (!eps) return -1.0;
    ring_spectrum(L, flux, t, eps);
    double z1 = ring_Z(L, eps, t, tau);
    double z2 = ring_Z(L, eps, t, ad_map_S(tau));
    free(eps);
    if (z2 == 0.0) return -1.0;
    return z1 / z2;
}

double complex ad_theta2(double complex tau, int nmax) {
    /* theta2(tau) = sum_n exp(i pi tau (n+1/2)^2), nome q = e^{i pi tau} */
    double complex s = 0.0 + 0.0 * I;
    for (int n = -nmax; n < nmax; n++) {
        double m = n + 0.5;
        s += cexp(I * M_PI * tau * (m * m));
    }
    return s;
}

double complex ad_theta3(double complex tau, int nmax) {
    double complex s = 0.0 + 0.0 * I;
    for (int n = -nmax; n < nmax; n++)
        s += cexp(I * M_PI * tau * (double)(n * n));
    return s;
}

double complex ad_theta4(double complex tau, int nmax) {
    double complex s = 0.0 + 0.0 * I;
    for (int n = -nmax; n < nmax; n++) {
        double sign = (n % 2 == 0) ? 1.0 : -1.0;
        s += sign * cexp(I * M_PI * tau * (double)(n * n));
    }
    return s;
}

double ad_Z_fermion(double complex tau) {
    /* Exact c=1 free-fermion Z = spin-structure sum / (2 |eta|^2). */
    double complex e = ad_dedekind_eta(tau, 300);
    double aeta2 = creal(e * conj(e));
    double complex t2 = ad_theta2(tau, 160);
    double complex t3 = ad_theta3(tau, 160);
    double complex t4 = ad_theta4(tau, 160);
    double s = creal(t2 * conj(t2)) + creal(t3 * conj(t3)) + creal(t4 * conj(t4));
    return 0.5 * s / aeta2;
}

/* c=1 Z2-orbifold partition function (Ginsparg). The circle piece is the
 * boson Z at radius R; the three twisted/projected blocks are |eta/theta_k|
 * for k=2,3,4. Modular S-invariant and R -> 2/R dual, like the circle branch. */
double ad_Z_orbifold(double complex tau, double R, int Nmax) {
    double complex e  = ad_dedekind_eta(tau, 300);
    double complex t2 = ad_theta2(tau, 160);
    double complex t3 = ad_theta3(tau, 160);
    double complex t4 = ad_theta4(tau, 160);
    double twisted = cabs(e / t2) + cabs(e / t3) + cabs(e / t4);
    return 0.5 * ad_Z_boson(tau, R, Nmax) + twisted;
}

double ad_sector_S_ratio(int sector, double complex tau) {
    /* |sector(tau)|^2 / |eta(tau)|^2 over the same at -1/tau. */
    double complex (*th)(double complex, int) =
        (sector == 2) ? ad_theta2 : (sector == 4) ? ad_theta4 : ad_theta3;
    double complex e1 = ad_dedekind_eta(tau, 300);
    double complex tm = ad_map_S(tau);
    double complex e2 = ad_dedekind_eta(tm, 300);
    double complex a = th(tau, 160), b = th(tm, 160);
    double z1 = creal(a * conj(a)) / creal(e1 * conj(e1));
    double z2 = creal(b * conj(b)) / creal(e2 * conj(e2));
    if (z2 == 0.0) return -1.0;
    return z1 / z2;
}

/* Half-filling ground-state energy of a ring (plain or pi-flux) or a dimerised
 * chain. For dimer_delta == 0: sum the negative single-particle energies of the
 * nearest-neighbour ring. For dimer_delta != 0: two-band closed form,
 * E(q) = -sqrt(t1^2 + t2^2 + 2 t1 t2 cos q), t1 = t(1+d), t2 = t(1-d), over the
 * L/2 cell momenta (this opens a gap, giving c ~ 0). */
static double ring_gs_energy(int L, double t, double flux, double dimer_delta) {
    double tot = 0.0;
    if (dimer_delta == 0.0) {
        /* antiperiodic spatial BC (the clean critical ground state; the periodic
         * ring has zero modes at the Fermi points that spoil the Casimir fit) */
        for (int k = 0; k < L; k++) {
            double e = -2.0 * t * cos(2.0 * M_PI * (k + 0.5) / (double)L + flux / (double)L);
            if (e < 0.0) tot += e;
        }
    } else {
        double t1 = t * (1.0 + dimer_delta), t2 = t * (1.0 - dimer_delta);
        int Nc = L / 2;
        for (int m = 0; m < Nc; m++) {
            double q = 2.0 * M_PI * m / (double)Nc;
            double E = sqrt(t1*t1 + t2*t2 + 2.0*t1*t2*cos(q));
            tot += -E;
        }
    }
    return tot;
}

double ad_central_charge(const int *Ls, int n, double t, double flux,
                         double dimer_delta) {
    /* Fit E0(L) = a*L + b*(1/L) by least squares, then c = -6 b /(pi vF),
     * vF = 2t. The 1/L Casimir coefficient carries the central charge. */
    double vF = 2.0 * t;
    double Sxx = 0, Sxy = 0, Szz = 0, Szy = 0, Sxz = 0;
    /* design columns: x = L, z = 1/L; targets y = E0(L). Solve 2x2 normal eqns. */
    for (int i = 0; i < n; i++) {
        double L = (double)Ls[i];
        double x = L, z = 1.0 / L;
        double y = ring_gs_energy(Ls[i], t, flux, dimer_delta);
        Sxx += x * x; Szz += z * z; Sxz += x * z;
        Sxy += x * y; Szy += z * y;
    }
    /* [Sxx Sxz][a]=[Sxy]; [Sxz Szz][b]=[Szy] */
    double det = Sxx * Szz - Sxz * Sxz;
    if (det == 0.0) return -999.0;
    double b = (Sxx * Szy - Sxz * Sxy) / det;
    return -6.0 * b / (M_PI * vF);
}

/* Same Cardy fit as ad_central_charge, but also reports fit quality so the
 * value can be trusted or rejected. On return:
 *   *rms_out   = root-mean-square fit residual over the L points
 *   *stderr_out = standard error on c from the least-squares covariance
 * (uses sigma^2 = RSS/(n-2); set to a negative flag if fewer than 3 points).
 * The return value is c, identical to ad_central_charge. A clean c=1 shows up
 * as small rms and c within a few stderr of 1; a gapped lattice as c near 0.
 * The stderr is the statistical fit error only; with near-noiseless lattice
 * data it is tiny, so a small residual offset of c from 1 (the finite-size /
 * irrelevant-operator correction) can read as several stderr and is systematic,
 * not a failure to be critical. */
double ad_central_charge_err(const int *Ls, int n, double t, double flux,
                             double dimer_delta, double *rms_out,
                             double *stderr_out) {
    double vF = 2.0 * t;
    double Sxx = 0, Sxy = 0, Szz = 0, Szy = 0, Sxz = 0;
    for (int i = 0; i < n; i++) {
        double L = (double)Ls[i];
        double x = L, z = 1.0 / L;
        double y = ring_gs_energy(Ls[i], t, flux, dimer_delta);
        Sxx += x * x; Szz += z * z; Sxz += x * z;
        Sxy += x * y; Szy += z * y;
    }
    double det = Sxx * Szz - Sxz * Sxz;
    if (det == 0.0) { if(rms_out)*rms_out=-1.0; if(stderr_out)*stderr_out=-1.0; return -999.0; }
    double a = (Szz * Sxy - Sxz * Szy) / det;
    double b = (Sxx * Szy - Sxz * Sxy) / det;
    double c = -6.0 * b / (M_PI * vF);

    /* residual sum of squares over the fitted points */
    double rss = 0.0;
    for (int i = 0; i < n; i++) {
        double L = (double)Ls[i];
        double y = ring_gs_energy(Ls[i], t, flux, dimer_delta);
        double yhat = a * L + b / L;
        double r = y - yhat;
        rss += r * r;
    }
    if (rms_out) *rms_out = sqrt(rss / (double)n);

    /* standard error on c: var(b) = sigma^2 * (X^T X)^-1_bb, with
     * (X^T X)^-1_bb = Sxx/det and sigma^2 = RSS/(n-2). */
    if (stderr_out) {
        if (n > 2) {
            double s2 = rss / (double)(n - 2);
            double var_b = s2 * Sxx / det;
            if (var_b < 0.0) var_b = -var_b;
            *stderr_out = 6.0 * sqrt(var_b) / (M_PI * vF);
        } else {
            *stderr_out = -1.0;   /* not enough points for an error estimate */
        }
    }
    return c;
}
