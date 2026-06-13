#include <stdio.h>
#include <stdlib.h>
#include "lattices.h"
int main(int argc,char**argv){
    int Lx=atoi(argv[1]),Ly=atoi(argv[2]); double beta=5.0,mu=0.3,t=1.0;
    LatticeCtx ctx; square2d_init(&ctx,Lx,Ly,beta,mu,t);
    int N=ctx.n_sites; printf("%d\n",N);
    for(int k=0;k<N;k++) printf("%.16e ",ctx.evals[k]); printf("\n");
    for(int i=0;i<N;i++){ for(int k=0;k<N;k++) printf("%.16e ",ctx.evecs[i*N+k]); printf("\n"); }
    return 0;
}
