#include <stdio.h>
#include <stdlib.h>
#include "cdet_engine.h"
#include "lattices.h"
/* argv: Lx Ly n ; stdin: lines of n pairs "site tau" ; out: C_V */
int main(int argc,char**argv){
    int Lx=atoi(argv[1]),Ly=atoi(argv[2]),n=atoi(argv[3]); double beta=5.0,mu=0.3,t=1.0;
    LatticeCtx ctx; square2d_init(&ctx,Lx,Ly,beta,mu,t);
    double to=0.4*beta, ti=0.6*beta; Vertex V[32];
    for(;;){ int ok=1;
        for(int i=0;i<n;i++){ int s; double ta; if(scanf("%d %lf",&s,&ta)!=2){ok=0;break;} V[i].site=s; V[i].tau=ta; }
        if(!ok) break;
        printf("%.16e\n", C_V(V,n,0,to,0,ti,lattice_G0,&ctx)); }
    return 0;
}
