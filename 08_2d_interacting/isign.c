/* isign.c (v40) -- the AVERAGE SIGN INTEGRATED OVER ORDERS, the quantity that actually controls the cost
 * of computing G(U) (unlike a single-order R, which v39 showed is contaminated by finite-size shell
 * structure). One MC: each sample draws an order n in [1,nmax] and n internal (site,tau) vertices; the
 * weight w = U^n * N*(N*beta)^n/n! * C_V estimates G(U)-G0 = sum_n U^n cdet_n. The integrated sign is
 * S = sum(w)/sum(|w|): orders are combined with their physical U^n weights, washing out per-order shell
 * sign-flips if anything can. Reports S and its stderr.
 *   usage: isign sq Lx Ly  nmax U beta mu t to ti nmc seed
 */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include "cdet_engine.h"
#include "lattices.h"

static uint64_t st; static inline uint64_t xs(void){uint64_t x=st;x^=x>>12;x^=x<<25;x^=x>>27;st=x;return x*0x2545F4914F6CDD1DULL;}
static inline double ur(void){return (double)(xs()>>11)*(1.0/9007199254740992.0);}

int main(int argc,char**argv){
    if(strcmp(argv[1],"sq")){ fprintf(stderr,"usage: isign sq Lx Ly nmax U beta mu t to ti nmc seed\n"); return 1; }
    int Lx=atoi(argv[2]),Ly=atoi(argv[3]),nmax=atoi(argv[4]);
    double U=atof(argv[5]),beta=atof(argv[6]),mu=atof(argv[7]),t=atof(argv[8]),to=atof(argv[9]),ti=atof(argv[10]);
    long nmc=atol(argv[11]); uint64_t seed=strtoull(argv[12],NULL,10);
    LatticeCtx lat; square2d_init(&lat,Lx,Ly,beta,mu,t); int N=Lx*Ly; st=seed?seed:88172645463325252ULL;
    /* per-order positive prefactor U^n * N*(N*beta)^n/n! */
    double pref[64]; for(int n=1;n<=nmax;n++){ double v=1; for(int i=0;i<n;i++) v*=N*beta; double f=1; for(int i=2;i<=n;i++) f*=i; pref[n]=pow(U,n)*N*v/f; }
    Vertex V[64];
    double sw=0,swa=0,sw2=0;          /* sum w, sum|w|, sum w^2 (for stderr of mean w) */
    for(long k=0;k<nmc;k++){
        int n=1+(int)(ur()*nmax); if(n>nmax)n=nmax;
        for(int i=0;i<n;i++){ int s=(int)(ur()*N); if(s>=N)s=N-1; V[i].site=s; V[i].tau=ur()*beta; }
        double c=C_V(V,n,0,to,0,ti,lattice_G0,&lat);
        double w=(double)nmax*pref[n]*c;       /* nmax = 1/P(n) for uniform order choice */
        sw+=w; swa+=fabs(w); sw2+=w*w;
    }
    double S=(swa>0)?sw/swa:0.0;
    /* stderr of S ~ stderr(mean w)/mean|w| */
    double meanw=sw/nmc, meanwa=swa/nmc, varw=sw2/nmc-meanw*meanw;
    double sS=(meanwa>0)?sqrt(fabs(varw)/nmc)/meanwa:0.0;
    printf("%.8g %.8g\n", S, sS);     /* integrated average sign, stderr */
    return 0;
}
