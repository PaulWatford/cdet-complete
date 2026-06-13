/* cdet_small.c (v36) -- engine connected-determinant order-(1,2) coefficient of the local Hubbard G,
 * for a 1D ring (ring_init) or 2D square torus (square2d_init). Same nested Gauss-Legendre quadrature
 * as driver.c cdet_order; geometry-blind C_V. Used to pin and validate the order<->U convention
 * against exact diagonalization (pin_convention.py).
 *   usage: cdet_small ring  L      beta mu t to ti
 *          cdet_small sq    Lx Ly  beta mu t to ti
 *
 * [v130 consolidation: still the ED-validated naive-but-benign anchor; the deep-beta / large-L
 * frontier now lives in the HYBRID plane-wave engine (cdet_planewave_engine.c) -- projector fast path ran a
 * MILLION sites (v124-v125), z(inf)=lowest-empty marches to mu (gap~L^-3.3), budget~L^3 (v126), and A's
 * continuum Friedel edge ~0.347/120deg confirms v119 (v129). This brute driver stays the small-beta ED anchor.]
 * [v120 consolidation] Brute-force CDet reference, unchanged since v36 and still ED-validated
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
#include "lattices.h"
#include "quad.h"
#include "cdet_engine.h"
#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct { int e; double to,ti,beta; int np; void*lat; double t1; int s1,s2; } DCtx;
static double f1(double tau,void*vp){ DCtx*d=vp; Vertex V[1]={{d->s1,tau}};
    return C_V(V,1,d->e,d->to,d->e,d->ti,lattice_G0,d->lat); }
static double f2i(double t2,void*vp){ DCtx*d=vp; Vertex V[2]={{d->s1,d->t1},{d->s2,t2}};
    return C_V(V,2,d->e,d->to,d->e,d->ti,lattice_G0,d->lat); }
static double f2o(double t1,void*vp){ DCtx*d=vp; d->t1=t1; double k[3]={d->to,d->ti,t1};
    return integrate_piecewise_1d(f2i,d,d->np,d->beta,k,3); }

static double cdet_n(int n,int N,LatticeCtx*lat,double beta,double to,double ti,int np){
    double ext[2]={to,ti};
    if(n==1){ double tot=0; for(int s=0;s<N;s++){ DCtx d={0,to,ti,beta,np,lat,0,s,0};
        tot+=integrate_piecewise_1d(f1,&d,np,beta,ext,2);} return (double)N*tot; }
    if(n==2){ double tot=0; for(int s1=0;s1<N;s1++)for(int s2=0;s2<N;s2++){ DCtx d={0,to,ti,beta,np,lat,0,s1,s2};
        tot+=integrate_piecewise_1d(f2o,&d,np,beta,ext,2);} return (double)N*tot/2.0; }
    return NAN;
}

int main(int argc,char**argv){
    int np=64; LatticeCtx lat; int N;
    double beta,mu,t,to,ti;
    if(argc>=8 && !strcmp(argv[1],"ring")){
        int L=atoi(argv[2]); beta=atof(argv[3]);mu=atof(argv[4]);t=atof(argv[5]);to=atof(argv[6]);ti=atof(argv[7]);
        ring_init(&lat,L,beta,mu,t); N=L;
    } else if(argc>=9 && !strcmp(argv[1],"sq")){
        int Lx=atoi(argv[2]),Ly=atoi(argv[3]); beta=atof(argv[4]);mu=atof(argv[5]);t=atof(argv[6]);to=atof(argv[7]);ti=atof(argv[8]);
        square2d_init(&lat,Lx,Ly,beta,mu,t); N=Lx*Ly;
    } else { fprintf(stderr,"usage: cdet_small ring L beta mu t to ti | sq Lx Ly beta mu t to ti\n"); return 1; }
    printf("%.15g %.15g %.15g\n", lattice_G0(0,0,to-ti,&lat), cdet_n(1,N,&lat,beta,to,ti,np), cdet_n(2,N,&lat,beta,to,ti,np));
    return 0;
}
