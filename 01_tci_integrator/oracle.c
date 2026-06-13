/* batch oracle: read n times per line from stdin, print C_V (atom) per line */
#include <stdio.h>
#include <stdlib.h>
#include "cdet_engine.h"
typedef struct { double beta, mu; } Ctx;
static double atom_g0(int i,int j,double tau,void*ctx){(void)i;(void)j;Ctx*c=ctx;return G0_atom(tau,c->beta,c->mu);}
int main(int argc,char**argv){
    int n=atoi(argv[1]); Ctx ctx={5.0,0.3}; double beta=5.0, to=0.4*beta, ti=0.6*beta;
    Vertex V[20]; double t[20];
    for(;;){ int ok=1; for(int i=0;i<n;i++) if(scanf("%lf",&t[i])!=1){ok=0;break;} if(!ok) break;
        for(int i=0;i<n;i++){V[i].site=0;V[i].tau=t[i];}
        printf("%.16e\n", C_V(V,n,0,to,0,ti,atom_g0,&ctx)); }
    return 0;
}
