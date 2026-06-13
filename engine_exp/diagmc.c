/* diagmc.c  (v27)  --  high-order time-integration via Monte Carlo over vertex times and sites.
 * See diagmc.h. Reproduces engine/driver.c cdet_order at n=1,2 within MC error and extends to n>=3.
 */
#include <stdlib.h>
#include <math.h>
#include "cdet_engine.h"
#include "lattices.h"
#include "diagmc.h"

/* xorshift64* -- small, fast, reproducible. */
static uint64_t s_state;
static inline uint64_t xs64(void) {
    uint64_t x = s_state;
    x ^= x >> 12; x ^= x << 25; x ^= x >> 27;
    s_state = x;
    return x * 0x2545F4914F6CDD1DULL;
}
/* uniform double in [0,1) */
static inline double urand(void) {
    return (double)(xs64() >> 11) * (1.0 / 9007199254740992.0);  /* 53-bit mantissa */
}

double cdet_order_mc(int n, int L, double beta, double mu, double t,
                     double tau_out, double tau_in,
                     long nmc, uint64_t seed, double *err_out) {
    if (n < 1 || L < 1 || nmc < 1) { if (err_out) *err_out = NAN; return NAN; }
    LatticeCtx lat; hexring_init(&lat, beta, mu, t);
    s_state = seed ? seed : 88172645463325252ULL;

    Vertex *V = (Vertex *)malloc((size_t)n * sizeof(Vertex));
    if (!V) { if (err_out) *err_out = NAN; return NAN; }

    /* Welford-style running mean/variance for a stable error bar over many samples. */
    double mean = 0.0, m2 = 0.0;
    for (long k = 1; k <= nmc; k++) {
        for (int i = 0; i < n; i++) {
            int s = (int)(urand() * (double)L);
            if (s >= L) s = L - 1;                 /* guard the urand()==~1 edge */
            V[i].site = s;
            V[i].tau  = urand() * beta;
        }
        double c = C_V(V, n, 0, tau_out, 0, tau_in, lattice_G0, &lat);
        double d  = c - mean;
        mean += d / (double)k;
        m2   += d * (c - mean);
    }
    free(V);

    /* prefactor: L * (L*beta)^n / n! */
    double vol = 1.0;
    for (int i = 0; i < n; i++) vol *= (double)L * beta;
    double fact = 1.0;
    for (int i = 2; i <= n; i++) fact *= (double)i;
    double pref = (double)L * vol / fact;

    if (err_out) {
        double var = (nmc > 1) ? m2 / (double)(nmc - 1) : 0.0;   /* sample variance of C_V */
        *err_out = pref * sqrt(var / (double)nmc);                /* SE of the mean, scaled */
    }
    return pref * mean;
}
