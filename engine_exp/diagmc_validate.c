/* diagmc_validate.c (v27) -- validate the high-order MC driver against the FROZEN baseline at
 * n=1,2, then report the first high-order terms (n>=3) the baseline cannot reach. */
#include <stdio.h>
#include "driver.h"
#include "diagmc.h"

int main(void) {
    setvbuf(stdout, NULL, _IONBF, 0);   /* unbuffered: partial output survives a kill */
    int L = 6; double beta = 4.0, mu = 0.7, t = 1.0, to = 0.123, ti = 0.877;
    double e1 = cdet_order(1, L, beta, mu, t, to, ti, 40);
    double e2 = cdet_order(2, L, beta, mu, t, to, ti, 40);
    printf("FROZEN baseline (nested quadrature):  n=1 = %.16g   n=2 = %.16g\n", e1, e2);
    printf("------------------------------------------------------------------------\n");
    long Ns[] = {100000L, 1000000L};
    for (int j = 0; j < 2; j++) {
        double er; double m = cdet_order_mc(1, L, beta, mu, t, to, ti, Ns[j], 12345, &er);
        printf("MC n=1  nmc=%8ld : %.7g +/- %.2g   dev %+.2f sigma\n", Ns[j], m, er, (m - e1) / er);
    }
    for (int j = 0; j < 2; j++) {
        double er; double m = cdet_order_mc(2, L, beta, mu, t, to, ti, Ns[j], 67890, &er);
        printf("MC n=2  nmc=%8ld : %.7g +/- %.2g   dev %+.2f sigma\n", Ns[j], m, er, (m - e2) / er);
    }
    printf("------------------------------------------------------------------------\n");
    printf("First high-order terms (baseline returns NaN here):\n");
    for (int n = 3; n <= 4; n++) {
        double er; double m = cdet_order_mc(n, L, beta, mu, t, to, ti, 500000L, 31337 + n, &er);
        double base = cdet_order(n, L, beta, mu, t, to, ti, 40);
        printf("MC n=%d  nmc=  500000 : %.7g +/- %.2g   (baseline cdet_order = %.3g)\n", n, m, er, base);
    }
    return 0;
}
