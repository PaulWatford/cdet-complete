/* csurrogate_test.c (v86) -- engine-style validation of the C surrogate against the Python
 * reference vectors in csurrogate_refs.h (generated live by csurrogate.py). */
#include <stdio.h>
#include <math.h>
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif
#include "csurrogate.h"
#include "csurrogate_refs.h"

int main(void) {
    double worst = 0.0; int fail = 0;
    for (int i = 0; i < NREF; i++) {
        double f[10];
        surr_features(REF_SITES[i], REF_L[i], f);
        for (int k = 0; k < 10; k++) {
            double d = fabs(f[k] - REF_FEATS[i][k]);
            if (d > worst) worst = d;
            if (d > 1e-9) { fail++; printf("FEAT MISMATCH cfg %d feat %d: %g vs %g\n", i, k, f[k], REF_FEATS[i][k]); }
        }
        double m = surr_ln_magnitude(REF_SITES[i], REF_L[i]);
        double dm = fabs(m - REF_LNMAG[i]);
        if (dm > worst) worst = dm;
        if (dm > 1e-9) { fail++; printf("LNMAG MISMATCH cfg %d: %.12f vs %.12f\n", i, m, REF_LNMAG[i]); }
        int sec = surr_sector(REF_SITES[i], REF_L[i]);
        if (sec != REF_SECTOR[i]) { fail++; printf("SECTOR MISMATCH cfg %d: %d vs %d\n", i, sec, REF_SECTOR[i]); }
    }
    for (int i = 0; i < NC1; i++) {
        double o[2];
        surr_class1_flips(C1_G[i], C1_B[i], 1.0, o);
        double d = fmax(fabs(o[0] - C1_LO[i]), fabs(o[1] - C1_HI[i]));
        if (d > worst) worst = d;
        if (d > 1e-9) { fail++; printf("CLASS1 MISMATCH %d\n", i); }
    }
    for (int i = 0; i < NST; i++) {
        double d = fabs(surr_class2_static(ST_B[i]) - ST_V[i]);
        if (d > worst) worst = d;
        if (d > 1e-9) { fail++; printf("STATIC MISMATCH %d\n", i); }
    }
    /* v93 identified law vs the honest record (max dev <= 1 sigma) */
    { double zb[4][3] = {{36,1.8450,0.0030},{40,1.8457,0.0046},{48,1.846,0.009},{56,1.8407,0.0103}};
      for (int i = 0; i < 4; i++)
        if (fabs(surr_static_l6_deep_law(zb[i][0]) - zb[i][1]) > zb[i][2]) { fail++; printf("DEEPLAW FAIL\n"); } }
    /* v92 deep-beta plateau constant */
    if (fabs(surr_static_l6_deep_inf() - 1.8437) > 1e-12) { fail++; printf("DEEPINF FAIL\n"); }
    /* v91 static-family API against the closed form */
    if (fabs(surr_static_l6_deep(20.0) - (1.824 - 0.72 / 20.0)) > 1e-12 ||
        fabs(surr_static_l6_deep(12.0) - (1.824 - 0.72 / 12.0)) > 1e-12) { fail++; printf("L6DEEP FAIL\n"); }
    /* v141 interacting-pole carrier: Sigma=0 limit (U=0) recovers the free pole; U^1 = free + Hartree shift */
    if (fabs(surr_interacting_pole(8, 1.0, 0.0, 0.4) - surr_lowest_empty(8, 1.0)) > 1e-12 ||
        fabs(surr_interacting_pole(8, 1.0, 2.0, 0.4) - (surr_lowest_empty(8, 1.0) + 0.8)) > 1e-12) { fail++; printf("INTPOLE FAIL\n"); }
    /* v147 SU(N) production carriers: record N(N-1) and (N-1) times single-flavor amplitudes (matches v144) */
    if (fabs(surr_sun_c1(6, 0.741007) - (-6.0*5.0*0.741007*0.741007)) > 1e-12 ||
        fabs(surr_sun_n1(6, 0.741007, 0.267663) - (-5.0*0.741007*0.267663)) > 1e-12 ||
        fabs(surr_sun_c1(1, 0.5)) > 1e-12) { fail++; printf("SUNCARRIER FAIL\n"); }
    /* v88 higher-order APIs against closed-form references */
    {
        double o4[2], o5[2];
        surr_class1_flips_order(4, 20.0, 1.0, o4);
        surr_class1_flips_order(5, 20.0, 1.0, o5);
        double r4l = 1.0 + log(0.156 / 0.844) / 20.0, r5l = 1.0 + log(0.402 / 0.598) / 20.0;
        if (fabs(o4[0] - r4l) > 1e-12 || fabs(o5[0] - r5l) > 1e-12) { fail++; printf("ORDER FAIL\n"); }
    }
    /* v99/v100 coefficient-program carriers (against their stored references) */
    if (fabs(surr_l6_zpol36() - 1.8249) > 1e-12) { fail++; printf("ZPOL FAIL\n"); }
    if (fabs(surr_l6_cross_slope(28.0) - 41.8e-9) > 1e-12 ||
        fabs(surr_l6_cross_slope(36.0) - 88.8e-9) > 1e-12) { fail++; printf("XSLOPE FAIL\n"); }
    /* cross-slope grows with beta; linear root sits above the one-sector frozen root (toward physical) */
    if (!(surr_l6_cross_slope(36.0) > surr_l6_cross_slope(28.0))) { fail++; printf("XGROW FAIL\n"); }
    if (!(surr_l6_root_linear(36.0) > 0.00183 && surr_l6_root_linear(36.0) < 0.00420)) { fail++; printf("XROOT FAIL\n"); }
    /* v111-v114 RESOLVED carriers: z(inf)=2 (Fermi-surface probe level), ln(beta)/beta approach */
    if (fabs(surr_l6_z_inf() - 2.0) > 1e-12) { fail++; printf("ZINF FAIL\n"); }
    if (fabs(surr_l6_z_inf_legacy() - 1.8818) > 1e-12) { fail++; printf("ZINF-LEGACY FAIL\n"); }
    /* finite-beta law rises toward 2 and lies below it; the menu rationals are just crossings */
    if (!(surr_l6_z_finite(120.0) > surr_l6_z_finite(24.0) && surr_l6_z_finite(120.0) < 2.0)) { fail++; printf("ZFINITE FAIL\n"); }
    if (fabs(surr_l6_pool(36.0) - 1.8428) > 1e-12 || fabs(surr_l6_pool(52.0) - 1.8642) > 1e-12) { fail++; printf("POOL FAIL\n"); }
    /* v120 sign-side carriers: integer spectrum -> mu-rigidity, and the frozen occupied count */
    if (surr_l6_gap_modes(1.0, 2.0) != 0) { fail++; printf("GAP-MODES FAIL\n"); }          /* nothing in (1,2) -> exactly mu-rigid */
    if (surr_l6_occupied(1.3) != 156 || surr_l6_occupied(1.9) != 156) { fail++; printf("OCCUPIED FAIL\n"); } /* same set across the window */
    if (surr_l6_occupied(6.5) != 216) { fail++; printf("MULT-SUM FAIL\n"); }            /* all 216 modes occupied above the band top */
    /* API sanity: regime codes, thermal period, orientation parity stepping */
    if (surr_regime(4.0, 1.0) != 0 || surr_regime(16.0, 1.0) != 2 || surr_regime(10.0, 1.0) != 1) { fail++; printf("REGIME FAIL\n"); }
    if (fabs(surr_thermal_period(4.0) - M_PI / 4.0) > 1e-15) { fail++; printf("PERIOD FAIL\n"); }
    double fl[2] = {0.9, 1.1};
    if (surr_orientation(1, fl, 2, 0.5) != 1 || surr_orientation(1, fl, 2, 1.0) != -1 ||
        surr_orientation(1, fl, 2, 1.2) != 1) { fail++; printf("ORIENT FAIL\n"); }
    if (fail == 0)
        printf("ALL CASES MATCH THE PYTHON REFERENCE TO 1e-09 (worst dev %.3g; %d configs, %d class-1, %d statics)\n",
               worst, NREF, NC1, NST);
    else
        printf("FAILURES: %d\n", fail);
    return fail ? 1 : 0;
}
