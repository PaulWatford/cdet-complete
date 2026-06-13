#define _POSIX_C_SOURCE 199309L
/* csurrogate_bench.c (v87) -- the benchmark + scaling harness for the core C surrogate.
 * Build: gcc -O2 -o bench csurrogate_bench.c csurrogate.c -lm   (self-contained, like the module)
 *
 * MEASURED ON THIS ENVIRONMENT (v87 round; gcc -O2):
 *   surr_features       ~1.5 us/call (0.68 M/s)      Python feats2: 312 us  -> x212
 *   surr_ln_magnitude   ~1.5 us/call (0.67 M/s)
 *   surr_sector         ~7.2 us/call (O(L^4) line enumeration)
 *   surr_class1_flips   ~19 ns ; class2/regime ~3 ns ; orientation ~6 ns  (O(1) in n)
 *   per-ANSWER vs exact: one tau-averaged n=3 coefficient (NT=576 protocol) ~1.3 s
 *                        vs 1.5 us prediction  ->  ~875,000x
 *   THE ORDERS-OF-n WALL (exact C_V, one tau-point, L=6): 1.75 ms (n=3) growing x2.5-3.3
 *                        per order -> 745 ms at n=9; the n-generalized feature kernel in C is
 *                        O(n^2): 0.5 us (n=3) -> 1.7 ms (n=200).
 *   VALIDITY CEILING (the honest one): the shipped laws and weights are n=3-derived; higher
 *                        orders need their own extraction (the v83 logit-map machinery), which is
 *                        capped by the exact wall at roughly n <= 6-7 tau-averaged.
 */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#include "csurrogate.h"
static double now_s(void){ struct timespec t; clock_gettime(CLOCK_MONOTONIC,&t); return t.tv_sec+1e-9*t.tv_nsec; }
int main(void){
    srand(7);
    int cfgs[1000][3];
    for(int i=0;i<1000;i++){ int a=1+rand()%215,b=1+rand()%215,c=1+rand()%215;
        if(a==b||b==c||a==c){i--;continue;} cfgs[i][0]=a;cfgs[i][1]=b;cfgs[i][2]=c; }
    double f[10], acc=0, o2[2], fl[4]={0.9,1.1,1.8,2.0}; double t0; long N;
    N=200000; t0=now_s();
    for(long k=0;k<N;k++){ surr_features(cfgs[k%1000],6,f); acc+=f[0]; }
    printf("surr_features      : %8.1f ns/call\n",(now_s()-t0)/N*1e9);
    N=200000; t0=now_s();
    for(long k=0;k<N;k++) acc+=surr_ln_magnitude(cfgs[k%1000],6);
    printf("surr_ln_magnitude  : %8.1f ns/call\n",(now_s()-t0)/N*1e9);
    N=5000; t0=now_s();
    for(long k=0;k<N;k++) acc+=surr_sector(cfgs[k%1000],6);
    printf("surr_sector        : %8.1f ns/call\n",(now_s()-t0)/N*1e9);
    N=20000000; t0=now_s();
    for(long k=0;k<N;k++){ surr_class1_flips((int)(k%3),12.0+(k%17),1.0,o2); acc+=o2[0]; }
    printf("surr_class1_flips  : %8.2f ns/call\n",(now_s()-t0)/N*1e9);
    N=50000000; t0=now_s();
    for(long k=0;k<N;k++) acc+=surr_class2_static(12.0+(k%17));
    printf("surr_class2_static : %8.2f ns/call\n",(now_s()-t0)/N*1e9);
    N=50000000; t0=now_s();
    for(long k=0;k<N;k++) acc+=surr_regime(4.0+(k%25),1.0);
    printf("surr_regime        : %8.2f ns/call\n",(now_s()-t0)/N*1e9);
    N=50000000; t0=now_s();
    for(long k=0;k<N;k++) acc+=surr_orientation(1,fl,4,0.5+(k%25)*0.1);
    printf("surr_orientation   : %8.2f ns/call\n",(now_s()-t0)/N*1e9);
    printf("(checksum %g)\nbench done\n",acc);
    return 0;
}
