/* cv_highorder.c (v32) -- does the control-variate idea (02_control_variate: a cheap correlated
 * surrogate corrected against the exact value -> variance reduction 1/(1-rho^2)) extend to the
 * HIGH-ORDER connected determinant C_V?
 *
 * 02_control_variate gets 71x at low order (n=4) with a TCI surrogate at rho=0.993. Here we test
 * cheap PARAMETRIC references at higher order: decoupled atoms, shifted-mu lattice, weak-hopping
 * lattice. Measured (1500 samples; rho is noisy at high order because C_V is a sign-oscillating
 * residual): all of them DE-CORRELATE -- |rho| <= ~0.7, erratic, giving only ~1-2x reduction, far
 * from 71x. The high-order connected value is too "chaotic" for a simple parametric surrogate to
 * track; high correlation there is as hard as the sign problem itself. Conclusion: the CV idea is
 * sound (and proven at low order), but the high-order surrogate must be ADAPTIVE/LEARNED (TCI-like),
 * not a fixed parametric reference.
 *
 * Build: gcc -O2 -Iengine_exp cv_highorder.c engine_exp/cdet_engine.c engine_exp/lattices.c \
 *            engine_exp/quad.c engine_exp/schur.c engine_exp/rankone.c engine_exp/symmetry.c -lm
 */
#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include "cdet_engine.h"
#include "lattices.h"
static unsigned long rs=88172645463325252UL;
static double ur(void){ rs^=rs<<13; rs^=rs>>7; rs^=rs<<17; return (rs>>11)*(1.0/9007199254740992.0); }
typedef struct{double beta,mu;} AtomP;
static double g0_atomic(int i,int j,double tau,void*ctx){ AtomP*a=ctx; if(i!=j)return 0.0;
    double t=tau,b=a->beta; while(t<0)t+=b; while(t>=b)t-=b; return G0_atom(t,b,a->mu); }
static double rho_of(int n,int L,double beta,g0_fn gf,void*gc,LatticeCtx*full,int M){
    double sf=0,sg=0,sff=0,sgg=0,sfg=0; Vertex*V=malloc(sizeof(Vertex)*n); rs=88172645463325252UL;
    for(int s=0;s<M;s++){ for(int k=0;k<n;k++){V[k].site=(int)(ur()*L);if(V[k].site>=L)V[k].site=L-1;V[k].tau=ur()*beta;}
        double f=C_V(V,n,0,1.5,0,0.5,lattice_G0,full); double g=C_V(V,n,0,1.5,0,0.5,gf,gc);
        sf+=f;sg+=g;sff+=f*f;sgg+=g*g;sfg+=f*g; }
    double mf=sf/M,mg=sg/M,vf=sff/M-mf*mf,vg=sgg/M-mg*mg,cfg=sfg/M-mf*mg; free(V);
    return cfg/sqrt(vf*vg);
}
int main(int argc,char**argv){
    int M = argc>1?atoi(argv[1]):1500;
    double beta=4.0,mu=0.7; LatticeCtx full; hexring_init(&full,beta,mu,1.0); AtomP ap={beta,mu};
    LatticeCtx shift; hexring_init(&shift,beta,mu+0.3,1.0);
    LatticeCtx wt;    hexring_init(&wt,beta,mu,0.7);
    printf("  n | rho(decoupled) | rho(shifted-mu) | rho(weak-hop) | best CV reduction\n");
    for(int n=4;n<=8;n+=2){
        double ra=rho_of(n,6,beta,g0_atomic,&ap,&full,M);
        double rsx=rho_of(n,6,beta,lattice_G0,&shift,&full,M);
        double rw=rho_of(n,6,beta,lattice_G0,&wt,&full,M);
        double best=fmax(fmax(fabs(ra),fabs(rsx)),fabs(rw)); double vr=1.0/(1.0-best*best);
        printf("  %2d |   %8.5f    |    %8.5f    |   %8.5f   |   %6.1fx\n", n, ra, rsx, rw, vr);
    }
    printf("(low order n=4 with a TCI surrogate reaches rho=0.993 -> 71x; see 02_control_variate.)\n");
    return 0;
}
