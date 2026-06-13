/* blocked_cv.c (v31) -- out-of-core connected-determinant recursion by bit-split blocking.
 *
 * The scattered O(3^n) submask recursion factorizes over a bit-split mask=(h,l) (n = nH high + nL low
 * bits): sm subset mask  <=>  sm_H subset h AND sm_L subset l. So it becomes a BLOCK-LEVEL subset
 * recursion where each element is a contiguous 2^nL block and the product is a low-block convolution:
 *     C[h,.] = Dc[h,.] - SUM_{hs proper-subset h} C[hs,.] (low-conv) Dv[h\hs,.]  - (within-block low recursion)
 * Processing h in increasing order (hs subset h => hs < h) gives a PREDICTABLE schedule: to build
 * block h, load only the blocks hs subset h and h\hs, one at a time. Peak RAM is O(2^nL) (a few
 * blocks), independent of n; the full 2^n lives on disk. Arithmetic is the EXACT direct sum (no
 * Mobius), so accuracy equals the flat engine -- this is the accuracy-first, RAM-bounded, HDD-overflow
 * path (speed is traded away: total block I/O ~ 3^nH).
 *
 * VALIDATED: reproduces the flat engine C_V to ~1e-20 across splits (n=12,16,18); peak RAM = 3 blocks
 * regardless of n (n=18,nL=10: 0.025 MB vs flat 4.19 MB = 171x less; grows with n). Needs engine_exp
 * (buffers removed, v26) so the per-mask determinants are uncapped.
 *
 * Build: gcc -O2 -Iengine_exp blocked_cv.c engine_exp/cdet_engine.c engine_exp/lattices.c \
 *            engine_exp/quad.c engine_exp/schur.c engine_exp/rankone.c engine_exp/symmetry.c -lm
 * Run:   ./a.out [scratch_dir]      (default ./blk_scratch; blocks are written there and removed)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include "cdet_engine.h"
#include "lattices.h"

static size_t g_res=0, g_peak=0;                       /* resident-block byte counter */
static double* balloc(int NL){ double*p=malloc((size_t)NL*8); g_res+=(size_t)NL*8; if(g_res>g_peak)g_peak=g_res; return p; }
static void    bfree(double*p,int NL){ free(p); g_res-=(size_t)NL*8; }
static void    bwrite(const char*d,const char*k,int h,const double*b,int NL){
    char p[600]; snprintf(p,sizeof p,"%s/%s_%d.bin",d,k,h); FILE*f=fopen(p,"wb"); if(!f){perror(p);exit(2);} fwrite(b,8,NL,f); fclose(f); }
static double* bread(const char*d,const char*k,int h,int NL){
    char p[600]; snprintf(p,sizeof p,"%s/%s_%d.bin",d,k,h); double*b=balloc(NL);
    FILE*f=fopen(p,"rb"); if(!f){perror(p);exit(3);} size_t r=fread(b,8,NL,f);(void)r; fclose(f); return b; }

/* out-of-core blocked C_V; returns C[2^n - 1], peak resident bytes left in g_peak */
static double blocked_disk(const Vertex*V,int n,int nL,int so,double to,int si,double ti,
                           g0_fn g0,void*ctx,const char*dir){
    int nH=n-nL, NL=1<<nL, NH=1<<nH;
    Vertex*sub=malloc(sizeof(Vertex)*n);
    for(int h=0;h<NH;h++){                              /* phase 1: per-mask Dv,Dc blocks -> disk */
        double*dv=balloc(NL),*dc=balloc(NL);
        for(int l=0;l<NL;l++){ int mask=(h<<nL)|l,m=0; for(int i=0;i<n;i++) if(mask&(1<<i)) sub[m++]=V[i];
            dv[l]=D_vac(sub,m,g0,ctx); dc[l]=D_corr(sub,m,so,to,si,ti,g0,ctx); }
        bwrite(dir,"dv",h,dv,NL); bwrite(dir,"dc",h,dc,NL); bfree(dv,NL); bfree(dc,NL);
    }
    for(int h=0;h<NH;h++){                              /* phase 2: block-level subset recursion */
        double*acc=bread(dir,"dc",h,NL);
        if(h) for(int hs=(h-1)&h; ; hs=(hs-1)&h){       /* proper high-submasks (h=0 has none) */
            double*Cb=bread(dir,"c",hs,NL), *Dvb=bread(dir,"dv",h^hs,NL);
            for(int l=0;l<NL;l++){ double s=0; for(int sl=l;;sl=(sl-1)&l){ s+=Cb[sl]*Dvb[l^sl]; if(sl==0)break; } acc[l]-=s; }
            bfree(Cb,NL); bfree(Dvb,NL);
            if(hs==0) break;
        }
        double*Dv0=bread(dir,"dv",0,NL);                /* within-block low recursion, in place */
        for(int l=0;l<NL;l++){ double v=acc[l]; if(l){ int sl=(l-1)&l; for(;;){ v-=acc[sl]*Dv0[l^sl]; if(sl==0)break; sl=(sl-1)&l; } } acc[l]=v; }
        bfree(Dv0,NL);
        bwrite(dir,"c",h,acc,NL); bfree(acc,NL);
    }
    double*last=bread(dir,"c",NH-1,NL); double r=last[NL-1]; bfree(last,NL); free(sub);
    return r;
}

int main(int argc,char**argv){
    setvbuf(stdout,NULL,_IONBF,0);
    const char*dir = argc>1 ? argv[1] : "./blk_scratch";
    char cmd[700]; snprintf(cmd,sizeof cmd,"mkdir -p '%s'",dir); int rc=system(cmd);(void)rc;
    char clean[700]; snprintf(clean,sizeof clean,"rm -f '%s'/*.bin",dir);
    double beta=4.0; LatticeCtx c; hexring_init(&c,beta,0.7,1.0);
    printf("  n | nL nH | flat C_V vs disk-blocked        | peak RAM       | flat 2*2^n | reduction\n");
    int ns[]={12,16,18}; 
    for(int t=0;t<3;t++){ int n=ns[t]; int nL=(n>=16)?10:6;
        Vertex*V=malloc(sizeof(Vertex)*n); for(int k=0;k<n;k++){V[k].site=k%6;V[k].tau=beta*(k+0.5)/n;}
        double flat=C_V(V,n,0,1.5,0,0.5,lattice_G0,&c);
        g_peak=g_res=0;
        double blk=blocked_disk(V,n,nL,0,1.5,0,0.5,lattice_G0,&c,dir);
        double flatRAM=2.0*(double)(1<<n)*8.0;
        printf("  %2d | %2d %2d | %.13g  (diff %.1g) | %.3g MB (%d blk) | %.3g MB | %.0fx less\n",
               n,nL,n-nL, blk, fabs(flat-blk), g_peak/1e6, (int)(g_peak/((size_t)(1<<nL)*8)), flatRAM/1e6, flatRAM/(double)g_peak);
        rc=system(clean); free(V);
    }
    snprintf(cmd,sizeof cmd,"rmdir '%s' 2>/dev/null",dir); rc=system(cmd);
    return 0;
}
