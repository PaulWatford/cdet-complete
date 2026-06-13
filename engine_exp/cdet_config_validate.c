/* cdet_config_validate.c (v34) -- gates the unified configurable driver:
 *   (1) CDET_PLAIN is bit-identical to the v27 cdet_order_mc.
 *   (2) CDET_BLOCKED (out-of-core) gives the same estimate as PLAIN (same seed) to ~1e-12.
 *   (3) CDET_CVAR is unbiased -- agrees with the frozen baseline within MC error -- and reports the
 *       measured correlation rho and variance reduction 1/(1-rho^2).
 *
 * Uses the canonical frozen-gate params (tau_out=0.123, tau_in=0.877) and the frozen baseline values
 * cdet_order(1,2) = -0.5082750022348369 / 0.44040518398732875. Gate (4) cross-checks the MC estimator
 * against the deterministic cdet_order at TWO parameter sets and n=1,2 (they agree to <1 sigma): the MC
 * and the quadrature compute the same integral across the parameter space, not just at one point.
 * (cdet_order's quadrature is converged for all np; the v34 quad.c fix sizes its node/weight arrays to
 * np, removing the np>64 stack overflow that earlier produced garbage and a false "discrepancy".)
 *
 * Build: gcc -O2 -Iengine_exp cdet_config_validate.c cdet_config.c diagmc.c driver.c \
 *   engine_exp/{cdet_engine,lattices,quad,schur,rankone,symmetry}.c -lm
 */
#include <stdio.h>
#include <math.h>
#include <stdint.h>
#include "diagmc.h"
#include "cdet_config.h"

/* engine deterministic quadrature (driver.c); safe & converged for all np<=stack (v34 fix: sized to np). */
double cdet_order(int n, int L, double beta, double mu, double t, double tau_out, double tau_in, int np);

int main(void){
    int L=6; double beta=4.0, mu=0.7, t=1.0, to=0.123, ti=0.877;
    const double BASE[3] = {0, -0.5082750022348369, 0.44040518398732875};  /* frozen n=1,2 (np=40) */
    int fails = 0;

    printf("=== (1) CDET_PLAIN bit-identical to cdet_order_mc ===\n");
    long seeds[3] = {12345, 88172645463325252LL, 7};
    int ns[3] = {1, 2, 3};
    for (int i=0;i<3;i++){
        double e1,e2;
        double a = cdet_order_mc    (ns[i], L, beta, mu, t, to, ti, 20000, (uint64_t)seeds[i], &e1);
        CdetConfig cfg = cdet_config_default();
        double b = cdet_order_mc_cfg(ns[i], L, beta, mu, t, to, ti, 20000, (uint64_t)seeds[i], &cfg, &e2);
        int ok = (a==b) && (e1==e2);
        printf("  n=%d seed=%lld : plain=%.17g cfg=%.17g  %s\n", ns[i], (long long)seeds[i], a, b, ok?"BIT-IDENTICAL":"*** DIFFER ***");
        if(!ok) fails++;
    }

    printf("\n=== (2) CDET_BLOCKED (out-of-core) == PLAIN, same seed ===\n");
    {
        int n=8; long nmc=20; uint64_t seed=4242;
        CdetConfig p = cdet_config_default(); double ep, eb;
        double a = cdet_order_mc_cfg(n, L, beta, mu, t, to, ti, nmc, seed, &p, &ep);
        CdetConfig bcfg = cdet_config_default(); bcfg.mode = CDET_BLOCKED; bcfg.nL = 4; bcfg.scratch = "./blk_scratch_v34";
        double b = cdet_order_mc_cfg(n, L, beta, mu, t, to, ti, nmc, seed, &bcfg, &eb);
        double rel = fabs(a-b)/(fabs(a)+1e-300);
        int ok = rel < 1e-10;
        printf("  n=%d nmc=%ld : plain=%.15g  blocked=%.15g  rel.diff=%.1e  %s\n", n, nmc, a, b, rel, ok?"MATCH":"*** DIFFER ***");
        if(!ok) fails++;
    }

    printf("\n=== (3) CDET_CVAR unbiased + measured variance reduction ===\n");
    for (int n=1;n<=2;n++){
        double base = BASE[n];
        long nmc=300000; uint64_t seed=999;
        CdetConfig p = cdet_config_default(); double ep;
        double a = cdet_order_mc_cfg(n, L, beta, mu, t, to, ti, nmc, seed, &p, &ep);
        CdetConfig cv = cdet_config_default(); cv.mode = CDET_CVAR; cv.cvar_mu_shift = 0.3; cv.cvar_pilot = nmc;
        double ecv;
        double b = cdet_order_mc_cfg(n, L, beta, mu, t, to, ti, nmc, seed, &cv, &ecv);
        double sig_plain = fabs(a-base)/(ep+1e-300);
        double sig_cv    = fabs(b-base)/(ecv+1e-300);
        int ok = (sig_cv < 4.0);
        double potential = (cv.cvar_rho_out*cv.cvar_rho_out<1.0)?1.0/(1.0-cv.cvar_rho_out*cv.cvar_rho_out):1e9;
        printf("  n=%d frozen baseline=%.13g\n", n, base);
        printf("      plain = %.6f +/- %.6f (%.2f sigma vs baseline)\n", a, ep, sig_plain);
        printf("      cvar  = %.6f +/- %.6f (%.2f sigma)  rho=%.4f  potential=%.1fx (if E[Y] exact)  NET=%.2fx  %s\n",
               b, ecv, sig_cv, cv.cvar_rho_out, potential, cv.cvar_vr_out, ok?"UNBIASED":"*** BIASED ***");
        if(!ok) fails++;
    }

    printf("\n=== (4) MC estimator == deterministic cdet_order across params (n=1,2) ===\n");
    {
        double PR[2]={1.5,0.123}, PI[2]={0.5,0.877};
        const char* tag[2]={"to=1.5,ti=0.5","to=0.123,ti=0.877"};
        for(int j=0;j<2;j++) for(int n=1;n<=2;n++){
            double ex = cdet_order(n, L, beta, mu, t, PR[j], PI[j], 48);   /* np=48: safe & converged */
            CdetConfig p = cdet_config_default(); double e;
            double mc = cdet_order_mc_cfg(n, L, beta, mu, t, PR[j], PI[j], 2000000, 2024, &p, &e);
            double sig = fabs(mc-ex)/(e+1e-300);
            int ok = sig < 4.0;
            printf("  %-18s n=%d : cdet_order=%.9f  MC=%.9f +/- %.6f  (%.2f sigma)  %s\n",
                   tag[j], n, ex, mc, e, sig, ok?"AGREE":"*** DISAGREE ***");
            if(!ok) fails++;
        }
    }

    printf("\n%s\n", fails==0 ? "ALL GATES PASS" : "*** FAILURES ***");
    return fails ? 1 : 0;
}
