/* cdet_config.c  (v34) -- see cdet_config.h. One configurable driver over the v27 MC estimator with
 * the v31 out-of-core blocking and a control-variate path wired in as switchable modes. The frozen
 * baseline (engine/) is untouched; this lives only in engine_exp/. */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include "cdet_engine.h"
#include "lattices.h"
#include "cdet_config.h"

/* xorshift64* -- identical to diagmc.c so CDET_PLAIN reproduces cdet_order_mc bit-for-bit. */
static uint64_t s_state;
static inline uint64_t xs64(void) {
    uint64_t x = s_state; x ^= x >> 12; x ^= x << 25; x ^= x >> 27; s_state = x;
    return x * 0x2545F4914F6CDD1DULL;
}
static inline double urand(void) { return (double)(xs64() >> 11) * (1.0 / 9007199254740992.0); }

static double order_prefactor(int n, int L, double beta) {
    double vol = 1.0; for (int i = 0; i < n; i++) vol *= (double)L * beta;
    double fact = 1.0; for (int i = 2; i <= n; i++) fact *= (double)i;
    return (double)L * vol / fact;
}

/* ---- out-of-core blocked C_V (ported from blocked_cv.c v31, h=0 guard intact) -------------------- */
static double* balloc(int NL){ return (double*)malloc((size_t)NL * 8); }
static void    bwrite(const char*d,const char*k,int h,const double*b,int NL){
    char p[600]; snprintf(p,sizeof p,"%s/%s_%d.bin",d,k,h); FILE*f=fopen(p,"wb");
    if(!f){perror(p);exit(2);} fwrite(b,8,NL,f); fclose(f); }
static double* bread(const char*d,const char*k,int h,int NL){
    char p[600]; snprintf(p,sizeof p,"%s/%s_%d.bin",d,k,h); double*b=balloc(NL);
    FILE*f=fopen(p,"rb"); if(!f){perror(p);exit(3);} size_t r=fread(b,8,NL,f);(void)r; fclose(f); return b; }

static double blocked_disk(const Vertex*V,int n,int nL,int so,double to,int si,double ti,
                           g0_fn g0,void*ctx,const char*dir){
    int nH=n-nL, NL=1<<nL, NH=1<<nH;
    Vertex*sub=(Vertex*)malloc(sizeof(Vertex)*n);
    for(int h=0;h<NH;h++){                                   /* phase 1: per-mask Dv,Dc -> disk */
        double*dv=balloc(NL),*dc=balloc(NL);
        for(int l=0;l<NL;l++){ int mask=(h<<nL)|l,m=0; for(int i=0;i<n;i++) if(mask&(1<<i)) sub[m++]=V[i];
            dv[l]=D_vac(sub,m,g0,ctx); dc[l]=D_corr(sub,m,so,to,si,ti,g0,ctx); }
        bwrite(dir,"dv",h,dv,NL); bwrite(dir,"dc",h,dc,NL); free(dv); free(dc);
    }
    for(int h=0;h<NH;h++){                                   /* phase 2: block-level subset recursion */
        double*acc=bread(dir,"dc",h,NL);
        if(h) for(int hs=(h-1)&h; ; hs=(hs-1)&h){            /* proper high-submasks (h=0 has none) */
            double*Cb=bread(dir,"c",hs,NL), *Dvb=bread(dir,"dv",h^hs,NL);
            for(int l=0;l<NL;l++){ double s=0; for(int sl=l;;sl=(sl-1)&l){ s+=Cb[sl]*Dvb[l^sl]; if(sl==0)break; } acc[l]-=s; }
            free(Cb); free(Dvb); if(hs==0) break;
        }
        double*Dv0=bread(dir,"dv",0,NL);                     /* within-block low recursion, in place */
        for(int l=0;l<NL;l++){ double v=acc[l]; if(l){ int sl=(l-1)&l; for(;;){ v-=acc[sl]*Dv0[l^sl]; if(sl==0)break; sl=(sl-1)&l; } } acc[l]=v; }
        free(Dv0); bwrite(dir,"c",h,acc,NL); free(acc);
    }
    double*last=bread(dir,"c",NH-1,NL); double r=last[NL-1]; free(last); free(sub);
    return r;
}

/* ------------------------------------------------------------------------------------------------- */
double cdet_order_mc_cfg(int n, int L, double beta, double mu, double t,
                         double tau_out, double tau_in,
                         long nmc, uint64_t seed,
                         CdetConfig *cfg, double *err_out) {
    if (n < 1 || L < 1 || nmc < 1) { if (err_out) *err_out = NAN; return NAN; }
    CdetMode mode = cfg ? cfg->mode : CDET_PLAIN;
    LatticeCtx lat; hexring_init(&lat, beta, mu, t);
    double pref = order_prefactor(n, L, beta);
    uint64_t seed0 = seed ? seed : 88172645463325252ULL;
    Vertex *V = (Vertex *)malloc((size_t)n * sizeof(Vertex));
    if (!V) { if (err_out) *err_out = NAN; return NAN; }

    if (mode == CDET_PLAIN || mode == CDET_BLOCKED) {
        int nL = 0; char scratch[600] = {0};
        if (mode == CDET_BLOCKED) {
            nL = (cfg && cfg->nL > 0 && cfg->nL < n) ? cfg->nL : n / 2;
            if (nL < 1) nL = 1;
            const char *dir = (cfg && cfg->scratch) ? cfg->scratch : "./blk_scratch";
            snprintf(scratch, sizeof scratch, "%s", dir);
            char cmd[700]; snprintf(cmd, sizeof cmd, "mkdir -p '%s'", scratch); int rc = system(cmd); (void)rc;
        }
        s_state = seed0;
        double mean = 0.0, m2 = 0.0;
        for (long k = 1; k <= nmc; k++) {
            for (int i = 0; i < n; i++) {
                int s = (int)(urand() * (double)L); if (s >= L) s = L - 1;
                V[i].site = s; V[i].tau = urand() * beta;
            }
            double c = (mode == CDET_BLOCKED)
                     ? blocked_disk(V, n, nL, 0, tau_out, 0, tau_in, lattice_G0, &lat, scratch)
                     : C_V(V, n, 0, tau_out, 0, tau_in, lattice_G0, &lat);
            double d = c - mean; mean += d / (double)k; m2 += d * (c - mean);
        }
        if (mode == CDET_BLOCKED && scratch[0]) {
            char cmd[700]; snprintf(cmd, sizeof cmd, "rm -f '%s'/*.bin; rmdir '%s' 2>/dev/null", scratch, scratch);
            int rc = system(cmd); (void)rc;
        }
        free(V);
        if (err_out) { double var = (nmc > 1) ? m2 / (double)(nmc - 1) : 0.0; *err_out = pref * sqrt(var / (double)nmc); }
        return pref * mean;
    }

    /* CDET_CVAR: control variate with a shifted-mu reference propagator, mean from an independent pilot. */
    LatticeCtx ref; hexring_init(&ref, beta, mu + (cfg ? cfg->cvar_mu_shift : 0.3), t);
    long pilot = (cfg && cfg->cvar_pilot > 0) ? cfg->cvar_pilot : nmc;

    /* pilot pass: independent samples -> E[Y] (reference per-sample mean), unbiased & independent. */
    s_state = seed0 ^ 0x9E3779B97F4A7C15ULL;
    double muY = 0.0;
    for (long k = 1; k <= pilot; k++) {
        for (int i = 0; i < n; i++) { int s=(int)(urand()*(double)L); if(s>=L)s=L-1; V[i].site=s; V[i].tau=urand()*beta; }
        double y = C_V(V, n, 0, tau_out, 0, tau_in, lattice_G0, &ref);
        muY += (y - muY) / (double)k;
    }
    /* main pass: f and Y on the SAME configs (correlated). Accumulate for beta*, rho, both means. */
    s_state = seed0;
    double mf=0, my=0, sff=0, syy=0, sfy=0;
    for (long k = 0; k < nmc; k++) {
        for (int i = 0; i < n; i++) { int s=(int)(urand()*(double)L); if(s>=L)s=L-1; V[i].site=s; V[i].tau=urand()*beta; }
        double f = C_V(V, n, 0, tau_out, 0, tau_in, lattice_G0, &lat);
        double y = C_V(V, n, 0, tau_out, 0, tau_in, lattice_G0, &ref);
        mf += f; my += y; sff += f*f; syy += y*y; sfy += f*y;
    }
    free(V);
    double N = (double)nmc;
    double meanf = mf/N, meany = my/N;
    double varf = sff/N - meanf*meanf, vary = syy/N - meany*meany, covfy = sfy/N - meanf*meany;
    double beta_star = (vary > 0) ? covfy/vary : 0.0;
    double rho = (varf>0 && vary>0) ? covfy/sqrt(varf*vary) : 0.0;
    double potential = (rho*rho < 1.0) ? 1.0/(1.0 - rho*rho) : INFINITY;  /* if E[Y] known exactly */

    /* HONEST error: the returned estimate is meanf - beta*(meany - muY). Its variance has TWO parts:
     *   within-pass residual  varf*(1-rho^2)/N   (the correlation gain), AND
     *   pilot-mean uncertainty beta^2 * vary / P (muY is MC-estimated, not known exactly).
     * With an MC-estimated muY the second term reintroduces ~the variance the first removed, so the
     * NET reduction is ~1x: the correlation gain is only realizable with an ANALYTIC E[Y]. */
    double P = (double)pilot;
    double var_resid = varf*(1.0 - rho*rho)/N;
    double var_pilot = beta_star*beta_star*vary/P;
    double var_total = var_resid + var_pilot;
    double net_vr = (var_total > 0) ? (varf/N)/var_total : INFINITY;       /* honest realized reduction */
    if (cfg) { cfg->cvar_rho_out = rho; cfg->cvar_vr_out = net_vr; }

    double theta = meanf - beta_star * (meany - muY);            /* unbiased control-variate estimate */
    if (err_out) *err_out = pref * sqrt(var_total);
    (void)potential;
    return pref * theta;
}
