#include <stdio.h>
#include <stdlib.h>
#include "lattices.h"
int main(int argc,char**argv){
    int Lx=atoi(argv[1]),Ly=atoi(argv[2]),n=atoi(argv[3]); double beta=5.0,mu=0.3,t=1.0;
    LatticeCtx ctx; square2d_init(&ctx,Lx,Ly,beta,mu,t);
    int site[256]; double tau[256];
    for(int i=0;i<n;i++) if(scanf("%d %lf",&site[i],&tau[i])!=2) return 1;
    for(int i=0;i<n;i++){ for(int j=0;j<n;j++)
        printf("%.16e ", lattice_G0(site[i],site[j],tau[i]-tau[j],&ctx)); printf("\n"); }
    return 0;
}
