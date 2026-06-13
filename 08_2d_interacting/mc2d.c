/* mc2d.c (v37) -- high-order connected-determinant Monte Carlo for ANY lattice (ring or 2D square).
 * Generalizes engine_exp/diagmc.c (which hardwires hexring) by taking a prebuilt LatticeCtx + site
 * count N; C_V is geometry-blind so only the lattice/site-sampling/prefactor change. Estimates
 * cdet_order(n) = N * a_n by uniform MC over n internal (site,tau) vertices. Also reports the
 * sign-cancellation ratio R = mean(C_V)/mean(|C_V|): R->0 is the fermion sign problem.
 *   usage: mc2d sq Lx Ly  n beta mu t to ti nmc seed
 *          mc2d ring L     n beta mu t to ti nmc seed
 * prints: estimate  stderr  R  scaled_mean_abs
 */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include "cdet_engine.h"
#include "lattices.h"

static uint64_t s_state;
static inline uint64_t xs64(void){ uint64_t x=s_state; x^=x>>12; x^=x<<25; x^=x>>27; s_state=x; return x*0x2545F4914F6CDD1DULL; }
static inline double urand(void){ return (double)(xs64()>>11)*(1.0/9007199254740992.0); }

static double mc_order(int n,int N,LatticeCtx*lat,double beta,double to,double ti,
                       long nmc,uint64_t seed,double*err_out,double*absmean_out,double*sign_out){
    s_state = seed?seed:88172645463325252ULL;
    Vertex*V=(Vertex*)malloc((size_t)n*sizeof(Vertex));
    double mean=0,m2=0,sa=0;
    for(long k=1;k<=nmc;k++){
        for(int i=0;i<n;i++){ int s=(int)(urand()*(double)N); if(s>=N)s=N-1; V[i].site=s; V[i].tau=urand()*beta; }
        double c=C_V(V,n,0,to,0,ti,lattice_G0,lat);
        double d=c-mean; mean+=d/(double)k; m2+=d*(c-mean); sa+=fabs(c);
    }
    free(V);
    double vol=1.0; for(int i=0;i<n;i++) vol*=(double)N*beta;
    double fact=1.0; for(int i=2;i<=n;i++) fact*=(double)i;
    double pref=(double)N*vol/fact;
    double var=(nmc>1)?m2/(double)(nmc-1):0.0;
    double absmean=sa/(double)nmc;
    if(err_out)    *err_out=pref*sqrt(var/(double)nmc);
    if(absmean_out)*absmean_out=pref*absmean;
    if(sign_out)   *sign_out=(absmean>0)?mean/absmean:0.0;
    return pref*mean;
}

int main(int argc,char**argv){
    LatticeCtx lat; int N=0,n; double beta,mu,t,to,ti; long nmc; uint64_t seed;
    if(argc>=12 && !strcmp(argv[1],"sq")){
        int Lx=atoi(argv[2]),Ly=atoi(argv[3]); n=atoi(argv[4]);
        beta=atof(argv[5]);mu=atof(argv[6]);t=atof(argv[7]);to=atof(argv[8]);ti=atof(argv[9]);
        nmc=atol(argv[10]); seed=strtoull(argv[11],NULL,10);
        square2d_init(&lat,Lx,Ly,beta,mu,t); N=Lx*Ly;
    } else if(argc>=11 && !strcmp(argv[1],"ring")){
        int L=atoi(argv[2]); n=atoi(argv[3]);
        beta=atof(argv[4]);mu=atof(argv[5]);t=atof(argv[6]);to=atof(argv[7]);ti=atof(argv[8]);
        nmc=atol(argv[9]); seed=strtoull(argv[10],NULL,10);
        ring_init(&lat,L,beta,mu,t); N=L;
    } else { fprintf(stderr,"usage: mc2d sq Lx Ly n beta mu t to ti nmc seed | mc2d ring L n beta mu t to ti nmc seed\n"); return 1; }
    double err,absm,sign;
    double est=mc_order(n,N,&lat,beta,to,ti,nmc,seed,&err,&absm,&sign);
    printf("%.10g %.10g %.10g %.10g\n", est, err, sign, absm);
    return 0;
}
