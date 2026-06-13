/* cdet_vs_naive.c (v38) -- does the determinant organization buy order reach?
 * At order n the engine evaluates det(M) of the (n+1)x(n+1) Wick matrix M[i,j]=G0(row_i,col_j) EXACTLY
 * in O(n^3) (D_corr). det(M) = sum over (n+1)! signed contractions. A method that instead sampled those
 * contractions stochastically suffers a sign problem of severity perm(|M|)/|det(M)| (sum of |terms| over
 * |sum of signed terms|). This program measures that ratio on the engine's ACTUAL matrices (same
 * lattice_G0), sampling configs as the MC does -- the variance the determinant removes per order.
 *   usage: cdet_vs_naive sq Lx Ly  nmax beta mu t to ti nsamp seed
 *          cdet_vs_naive ring L     nmax beta mu t to ti nsamp seed
 *
 * [v130 consolidation: still the ED-validated naive-but-benign anchor; the deep-beta / large-L
 * frontier now lives in the HYBRID plane-wave engine (cdet_planewave_engine.c) -- projector fast path ran a
 * MILLION sites (v124-v125), z(inf)=lowest-empty marches to mu (gap~L^-3.3), budget~L^3 (v126), and A's
 * continuum Friedel edge ~0.347/120deg confirms v119 (v129). This brute driver stays the small-beta ED anchor.]
 * [v120 consolidation] Brute-force CDet reference, unchanged since v38 and still ED-validated
 * (the engine stays frozen, 194/194). The deep-beta frontier (v92-v100: the coefficient program,
 * the two-sector/cross-term zero structure) lives in the Python modules of 08_2d_interacting and is
 * carried in C by csurrogate.* (params header). This driver is the exact-arithmetic ground truth
 * those approximations are checked against; it is intentionally NOT modified.
 *
 * [v115 PRECISION CAVEAT + DEEP-BETA POINTER] This driver's propagator is the frozen engine's NAIVE
 * G0_atom (engine/cdet_engine.c: -(1-n_F) exp(-xi tau)) -- correct and ED-validated at BENIGN beta
 * (where these drivers run), but v103 showed it catastrophically cancels at DEEP beta (a far occupied
 * level's (1-n_F) -> 1.0-1.0=0, the antiperiodic image VANISHES). These brute drivers are NEVER run at
 * deep beta, so they are correct in their validated domain. THE DEEP-BETA C LAYER IS NOW BUILT:
 * cdet_stable_engine.c (v109-v114) -- the frozen connected determinant with the log-domain propagator,
 * validated to machine precision against this brute reference at benign beta and against mpmath at deep
 * beta, float64 to beta~80 and long double (-DUSE_LD) to beta=120. It resolved the deep-beta object:
 * z(inf)=2 (the Fermi-surface probe level), the menu rationals were finite-beta crossings of a
 * ln(beta)/beta approach (v111 resolved, v112 derived A~1/beta^3 corner-confined & c1~beta^-0.3 level-2
 * de-confined, v113 saturation, v114 Fermi-lock). This brute driver stays naive-but-benign by design --
 * it is the ED-validated anchor that cdet_stable_engine.c is checked against.
 * SIGN SIDE (v116-v119): this driver computes the connected determinant A (whose SIGN is a multi-
 * propagator superposition); the elementary sign object is the frozen density matrix rho(0,r) (Python
 * frozen_friedel_map.py) and the distilled mu-rigidity carrier is surr_l6_gap_modes (csurrogate). The
 * scale z(inf)=2 and the sign are both set by the DISCRETE (integer-spectrum) frozen Fermi surface.
 */
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <math.h>
#include <stdint.h>
#include "lattices.h"

static uint64_t st; static inline uint64_t xs(void){uint64_t x=st;x^=x>>12;x^=x<<25;x^=x>>27;st=x;return x*0x2545F4914F6CDD1DULL;}
static inline double ur(void){return (double)(xs()>>11)*(1.0/9007199254740992.0);}

static double det_lu(double*A,int m){          /* destroys A */
    double d=1.0;
    for(int c=0;c<m;c++){
        int p=c; for(int r=c+1;r<m;r++) if(fabs(A[r*m+c])>fabs(A[p*m+c])) p=r;
        if(A[p*m+c]==0.0) return 0.0;
        if(p!=c){ for(int k=0;k<m;k++){double tmp=A[c*m+k];A[c*m+k]=A[p*m+k];A[p*m+k]=tmp;} d=-d; }
        d*=A[c*m+c];
        for(int r=c+1;r<m;r++){ double f=A[r*m+c]/A[c*m+c]; for(int k=c;k<m;k++) A[r*m+k]-=f*A[c*m+k]; }
    }
    return d;
}
/* permanent of |B| via Ryser's formula, m<=~16 */
static double perm_abs(const double*B,int m){
    /* Ryser: perm(A) = (-1)^m sum_{S} (-1)^{|S|} prod_i (sum_{j in S} A[i,j]); positive for |B|. */
    double tot=0.0; int full=1<<m;
    for(int s=1;s<full;s++){
        int bits=0; double prod=1.0;
        for(int i=0;i<m;i++){ double rs=0.0; for(int j=0;j<m;j++) if(s&(1<<j)) rs+=fabs(B[i*m+j]); prod*=rs; }
        for(int j=0;j<m;j++) if(s&(1<<j)) bits++;
        tot += ((bits&1)? -1.0:1.0)*prod;
    }
    return ((m&1)?-1.0:1.0)*tot;
}

int main(int argc,char**argv){
    LatticeCtx lat; int N=0,nmax; double beta,mu,t,to,ti; long nsamp; uint64_t seed; int base;
    if(!strcmp(argv[1],"sq")){ int Lx=atoi(argv[2]),Ly=atoi(argv[3]); nmax=atoi(argv[4]);
        beta=atof(argv[5]);mu=atof(argv[6]);t=atof(argv[7]);to=atof(argv[8]);ti=atof(argv[9]);
        nsamp=atol(argv[10]);seed=strtoull(argv[11],NULL,10); square2d_init(&lat,Lx,Ly,beta,mu,t); N=Lx*Ly; }
    else { int L=atoi(argv[2]); nmax=atoi(argv[3]);
        beta=atof(argv[4]);mu=atof(argv[5]);t=atof(argv[6]);to=atof(argv[7]);ti=atof(argv[8]);
        nsamp=atol(argv[9]);seed=strtoull(argv[10],NULL,10); ring_init(&lat,L,beta,mu,t); N=L; }
    st=seed?seed:88172645463325252ULL;
    printf("# %s N=%d beta=%g: geometric-mean perm(|M|)/|det(M)| over %ld configs vs order\n", argv[1],N,beta,nsamp);
    printf("# order   geomean(perm/|det|)   (variance factor the determinant removes per order)\n");
    for(int n=1;n<=nmax;n++){
        int m=n+1; double slog=0; long cnt=0;
        double*M=malloc(sizeof(double)*m*m), *B=malloc(sizeof(double)*m*m);
        int*rs=malloc(sizeof(int)*m),*cs=malloc(sizeof(int)*m); double*rt=malloc(sizeof(double)*m),*ct=malloc(sizeof(double)*m);
        for(long k=0;k<nsamp;k++){
            rs[0]=0; rt[0]=to; cs[0]=0; ct[0]=ti;                      /* externals at site 0 */
            for(int i=1;i<m;i++){ int s=(int)(ur()*N); if(s>=N)s=N-1; rs[i]=cs[i]=s; rt[i]=ct[i]=ur()*beta; }
            for(int i=0;i<m;i++) for(int j=0;j<m;j++){ double g=lattice_G0(rs[i],cs[j],rt[i]-ct[j],&lat); M[i*m+j]=g; B[i*m+j]=g; }
            double dt=det_lu(M,m);                                     /* M destroyed */
            if(fabs(dt)<1e-300) continue;
            double pa=perm_abs(B,m);
            slog += log(pa/fabs(dt)); cnt++;
        }
        printf("  %2d        %.6e\n", n, exp(slog/(double)cnt));
        free(M);free(B);free(rs);free(cs);free(rt);free(ct);
    }
    return 0;
}
