#include <stdio.h>
#include <stdlib.h>
#include "cdet_engine.h"
#include "lattices.h"
int main(int argc,char**argv){
    int n=atoi(argv[1]); double beta=5.0,mu=0.3,t=1.0;
    LatticeCtx ctx; hexring_init(&ctx,beta,mu,t);
    double to=0.4*beta, ti=0.6*beta; Vertex V[20]; double tau[20];
    for(;;){ int ok=1; for(int i=0;i<n;i++) if(scanf("%lf",&tau[i])!=1){ok=0;break;} if(!ok) break;
        for(int i=0;i<n;i++){V[i].site=i%6; V[i].tau=tau[i];}
        printf("%.16e\n", C_V(V,n,0,to,0,ti,lattice_G0,&ctx)); }
    return 0;
}
