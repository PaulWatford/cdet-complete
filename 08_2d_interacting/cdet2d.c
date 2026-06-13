/* cdet2d.c (v36) -- first INTERACTING 2D step: the connected-determinant order-n coefficient of the
 * (translationally-summed, local) Hubbard Green's function on an Lx x Ly square torus.
 *
 * This is driver.c's cdet_order with hexring_init -> square2d_init and the external symmetry factor
 * L -> N=Lx*Ly. The connected recursion C_V (cdet_engine.c) is geometry-blind; only the propagator
 * (square2d lattice_G0) and the site sums change. Deterministic nested Gauss-Legendre quadrature over
 * vertex times (n=1,2), exactly as in 1D. Validated against exact 2D Hubbard ED (hubbard_ed.py).
 *
 * cdet_order_2d(n) = N * (1/n!) * SUM_{internal sites} INT dtau_1..dtau_n  C_V({(s_i,tau_i)}, 0,to,0,ti)
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

typedef struct { int e; double tau_out, tau_in, beta; int np; void *lat; double t1; int s1, s2; } DCtx;

static double f1(double tau, void *vp){ DCtx*d=vp; Vertex V[1]={{d->s1,tau}};
    return C_V(V,1,d->e,d->tau_out,d->e,d->tau_in,lattice_G0,d->lat); }
static double f2_inner(double t2, void *vp){ DCtx*d=vp; Vertex V[2]={{d->s1,d->t1},{d->s2,t2}};
    return C_V(V,2,d->e,d->tau_out,d->e,d->tau_in,lattice_G0,d->lat); }
static double f2_outer(double t1, void *vp){ DCtx*d=vp; d->t1=t1;
    double kinks[3]={d->tau_out,d->tau_in,t1};
    return integrate_piecewise_1d(f2_inner,d,d->np,d->beta,kinks,3); }

double cdet_order_2d(int n, int Lx, int Ly, double beta, double mu, double t,
                     double tau_out, double tau_in, int np){
    int N=Lx*Ly; LatticeCtx lat; square2d_init(&lat,Lx,Ly,beta,mu,t);
    double ext[2]={tau_out,tau_in};
    if(n==1){ double tot=0;
        for(int s=0;s<N;s++){ DCtx d={0,tau_out,tau_in,beta,np,&lat,0,s,0};
            tot+=integrate_piecewise_1d(f1,&d,np,beta,ext,2); }
        return (double)N*tot; }
    if(n==2){ double tot=0;
        for(int s1=0;s1<N;s1++) for(int s2=0;s2<N;s2++){ DCtx d={0,tau_out,tau_in,beta,np,&lat,0,s1,s2};
            tot+=integrate_piecewise_1d(f2_outer,&d,np,beta,ext,2); }
        return (double)N*tot/2.0; }
    return NAN;
}

int main(int argc,char**argv){
    int Lx=argc>1?atoi(argv[1]):2, Ly=argc>2?atoi(argv[2]):2;
    double beta=argc>3?atof(argv[3]):4.0, mu=argc>4?atof(argv[4]):0.5, t=1.0;
    double to=argc>5?atof(argv[5]):0.7, ti=argc>6?atof(argv[6]):0.2;
    int np=64;
    LatticeCtx l0; square2d_init(&l0,Lx,Ly,beta,mu,t);
    printf("# 2D square %dx%d  beta=%g mu=%g t=%g  tau_out=%g tau_in=%g  np=%d\n",Lx,Ly,beta,mu,t,to,ti,np);
    printf("G0(0,0;to,ti) = %.15g\n", lattice_G0(0,0,to-ti,&l0));
    printf("cdet_order_2d(1) = %.15g\n", cdet_order_2d(1,Lx,Ly,beta,mu,t,to,ti,np));
    printf("cdet_order_2d(2) = %.15g\n", cdet_order_2d(2,Lx,Ly,beta,mu,t,to,ti,np));
    return 0;
}
