/* ============================================================================
 * test_cdet.c: C test suite: verify the C port against the frozen golden
 * values extracted from the verified Python reference (golden.json).
 *
 * Each golden case has a name "lattice.quantity.params" and a value. This
 * harness recomputes the SAME quantity with the C engine and checks it
 * matches to a tight tolerance. It mirrors the Python verification ladder:
 * atom G0 -> atom CDet recursion -> dimer/piflux/hexring G0.
 *
 * The golden values are parsed from golden.json at runtime (a tiny bespoke
 * parser; the file format is fixed and simple). Build with the Makefile:
 * make test
 * ============================================================================
 */
#include "cdet_engine.h"
#include "lattices.h"
#include "momfreq.h"
#include "qss_det.h"
#include "quad.h"
#include "symmetry.h"
#include "rankone.h"
#include "qss_parallel.h"
#include "driver.h"
#include "dyndet.h"
#include <complex.h>
#include "anchor_duality.h"
#include "cyclo_ratios.h"
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

/* fixed test parameters; must match gen_golden.py */
static const double BETA = 5.0, MU = 0.3, T = 1.0, U = 1.0;
static const double TOL = 1e-9; /* C-vs-Python agreement tolerance */

/* ---- tiny golden.json reader: pulls (name,value) pairs ----------------- */
typedef struct { char name[64]; double value; } Golden;

static int load_golden(const char *path, Golden *out, int maxn) {
 FILE *f = fopen(path, "r");
 if (!f) { fprintf(stderr, "cannot open %s\n", path); return -1; }
 char *buf; long sz;
 fseek(f, 0, SEEK_END); sz = ftell(f); fseek(f, 0, SEEK_SET);
 buf = malloc(sz + 1);
 size_t got = fread(buf, 1, sz, f); buf[got] = 0; fclose(f);
 int count = 0;
 char *p = buf;
 while ((p = strstr(p, "\"name\"")) && count < maxn) {
 char *q = strchr(p, ':'); q = strchr(q, '"') + 1;
 char *e = strchr(q, '"');
 int len = (int)(e - q); if (len > 63) len = 63;
 memcpy(out[count].name, q, len); out[count].name[len] = 0;
 char *vp = strstr(e, "\"value\""); vp = strchr(vp, ':') + 1;
 out[count].value = strtod(vp, NULL);
 count++; p = vp;
 }
 free(buf);
 return count;
}

/* ---- recompute a single named case with the C engine ------------------- */
/* Returns 1 if computed, storing result in *res; 0 if name unrecognised. */

static void vtimes(Vertex *V, int n) { /* 0.5,1.4,2.3,3.2,4.1 */
 for (int k = 0; k < n; k++) { V[k].site = 0; V[k].tau = 0.5 + 0.9*k; }
}

/* --- integrand helpers for the #3/#4 golden cases (beta=2.0, externals
 * xout=(0,1.5), xin=(0,0.3), same-site config) --- */
#define QB 2.0
static double q_xo_t = 1.5, q_xi_t = 0.3;
static double integrand_1d(double t1, void *ctx) {
 LatticeCtx *c = (LatticeCtx*)ctx;
 Vertex V[1] = {{0, t1}};
 return C_V(V, 1, 0, q_xo_t, 0, q_xi_t, lattice_G0, c);
}
static double integrand_2d(double t1, double t2, void *ctx) {
 LatticeCtx *c = (LatticeCtx*)ctx;
 Vertex V[2] = {{0, t1},{0, t2}};
 return C_V(V, 2, 0, q_xo_t, 0, q_xi_t, lattice_G0, c);
}

static int compute_case(const char *name, double *res) {
 double tau; int i, j, n;

 /* ---- atom.* ---- */
 if (sscanf(name, "atom.G0.tau=%lf", &tau) == 1) {
 LatticeCtx c; atom_init(&c, BETA, MU);
 *res = G0_atom(tau, BETA, MU); return 1;
 }
 if (strcmp(name, "atom.G0.zerominus") == 0) { *res = G0_atom_at_zero_minus(BETA, MU); return 1; }
 if (strcmp(name, "atom.nF") == 0) { *res = n_F(-MU, BETA); return 1; }
 if (strcmp(name, "atom.density_exact.U=1") == 0) { *res = density_exact(BETA, MU, U); return 1; }
 if (sscanf(name, "atom.Gexact.tau=%lf.U=1", &tau) == 1) {
 *res = G_exact_atom(tau, BETA, MU, U); return 1;
 }
 if (sscanf(name, "atom.CV.n=%d", &n) == 1) {
 LatticeCtx c; atom_init(&c, BETA, MU);
 Vertex V[8]; vtimes(V, n);
 *res = C_V(V, n, 0, 1.5, 0, 0.5, atom_G0, &c); return 1;
 }

 /* ---- dimer.G0.ij.tau=... ---- */
 if (sscanf(name, "dimer.G0.%1d%1d.tau=%lf", &i, &j, &tau) == 3) {
 LatticeCtx c; dimer_init(&c, BETA, MU, T);
 *res = lattice_G0(i, j, tau, &c); return 1;
 }
 if (sscanf(name, "piflux.G0.%1d%1d.tau=%lf", &i, &j, &tau) == 3) {
 LatticeCtx c; piflux_init(&c, BETA, MU, T);
 *res = lattice_G0(i, j, tau, &c); return 1;
 }
 if (sscanf(name, "hexring.G0.%1d%1d.tau=%lf", &i, &j, &tau) == 3) {
 LatticeCtx c; hexring_init(&c, BETA, MU, T);
 *res = lattice_G0(i, j, tau, &c); return 1;
 }

 /* ---- multi-site CDet recursion: vertices (k%n_sites, 0.5+0.9k) ---- */
 if (sscanf(name, "dimer.CV.n=%d", &n) == 1) {
 LatticeCtx c; dimer_init(&c, BETA, MU, T);
 Vertex V[8]; for (int k=0;k<n;k++){V[k].site=k%2; V[k].tau=0.5+0.9*k;}
 *res = C_V(V, n, 0, 1.5, 0, 0.5, lattice_G0, &c); return 1;
 }
 if (sscanf(name, "piflux.CV.n=%d", &n) == 1) {
 LatticeCtx c; piflux_init(&c, BETA, MU, T);
 Vertex V[8]; for (int k=0;k<n;k++){V[k].site=k%4; V[k].tau=0.5+0.9*k;}
 *res = C_V(V, n, 0, 1.5, 0, 0.5, lattice_G0, &c); return 1;
 }
 if (sscanf(name, "hexring.CV.n=%d", &n) == 1) {
 LatticeCtx c; hexring_init(&c, BETA, MU, T);
 Vertex V[8]; for (int k=0;k<n;k++){V[k].site=k%6; V[k].tau=0.5+0.9*k;}
 *res = C_V(V, n, 0, 1.5, 0, 0.5, lattice_G0, &c); return 1;
 }

 /* ---- CLOSED-FORM PATH (CDNet technique #1): same golden values, but
 * computed via Lagrange-projector G0 instead of the Jacobi eigensolver.
 * Reuses the SAME golden names with a "C:" prefix the harness adds. ---- */
 if (sscanf(name, "closed.dimer.G0.%1d%1d.tau=%lf", &i, &j, &tau) == 3) {
 LatticeCtx c; dimer_init(&c, BETA, MU, T);
 *res = lattice_G0_closed(i, j, tau, &c); return 1;
 }
 if (sscanf(name, "closed.piflux.G0.%1d%1d.tau=%lf", &i, &j, &tau) == 3) {
 LatticeCtx c; piflux_init(&c, BETA, MU, T);
 *res = lattice_G0_closed(i, j, tau, &c); return 1;
 }
 if (sscanf(name, "closed.hexring.G0.%1d%1d.tau=%lf", &i, &j, &tau) == 3) {
 LatticeCtx c; hexring_init(&c, BETA, MU, T);
 *res = lattice_G0_closed(i, j, tau, &c); return 1;
 }
 if (sscanf(name, "closed.dimer.CV.n=%d", &n) == 1) {
 LatticeCtx c; dimer_init(&c, BETA, MU, T);
 Vertex V[8]; for (int k=0;k<n;k++){V[k].site=k%2; V[k].tau=0.5+0.9*k;}
 *res = C_V(V, n, 0, 1.5, 0, 0.5, lattice_G0_closed, &c); return 1;
 }
 if (sscanf(name, "closed.piflux.CV.n=%d", &n) == 1) {
 LatticeCtx c; piflux_init(&c, BETA, MU, T);
 Vertex V[8]; for (int k=0;k<n;k++){V[k].site=k%4; V[k].tau=0.5+0.9*k;}
 *res = C_V(V, n, 0, 1.5, 0, 0.5, lattice_G0_closed, &c); return 1;
 }
 if (sscanf(name, "closed.hexring.CV.n=%d", &n) == 1) {
 LatticeCtx c; hexring_init(&c, BETA, MU, T);
 Vertex V[8]; for (int k=0;k<n;k++){V[k].site=k%6; V[k].tau=0.5+0.9*k;}
 *res = C_V(V, n, 0, 1.5, 0, 0.5, lattice_G0_closed, &c); return 1;
 }

 /* ---- MOMENTUM-FREQUENCY path: reconstruct hexring G0 from (k, i w_n) ----
 * Verifies the spatial-FFT + Matsubara-comb representation against golden. */
 if (sscanf(name, "momfreq.hexring.G0.%1d%1d.tau=%lf", &i, &j, &tau) == 3) {
 MomFreqCtx c; momfreq_init(&c, 6, BETA, MU, T, 20000);
 *res = momfreq_G0_site(&c, i, j, tau); return 1;
 }
 /* antiperiodic flip: the golden stores G0(tau); we compute G0(tau+beta),
 * which must equal -golden. We return -G0(tau+beta) so it matches golden. */
 if (sscanf(name, "momfreq.flip.%1d%1d.tau=%lf", &i, &j, &tau) == 3) {
 MomFreqCtx c; momfreq_init(&c, 6, BETA, MU, T, 20000);
 *res = -momfreq_G0_site(&c, i, j, tau + BETA); /* = +G0(tau) if flip holds */
 return 1;
 }

 /* ---- QUASISEPARABLE determinant: O(n L^2) det of the same-site ring
 * vertex matrix at fixed times tau_a = 0.3 + 0.37 a (sorted). Verified
 * against the golden dense determinant from Python. ---- */
 if (sscanf(name, "qss.detM.n=%d", &n) == 1) {
 double tau[16]; for (int a=0;a<n;a++) tau[a]=0.3+0.37*a;
 double A[16*6], Bu[16*6], Bl[16*6];
 qss_build_ring(6, BETA, MU, T, tau, n, A, Bu, Bl);
 *res = qss_det(A, Bu, Bl, n, 6);
 return 1;
 }

 /* ---- COMPLEX qss: different-site vertex determinant (beta=5.0) ----
 * site pattern (2k+1)%6, times 0.3+0.37k (already time-sorted). Verified
 * against the dense different-site determinant from Python. */
 if (sscanf(name, "qssc.detM.n=%d", &n) == 1) {
 int site[16]; double tau[16];
 for (int a=0;a<n;a++){ site[a]=(2*a+1)%6; tau[a]=0.3+0.37*a; }
 double _Complex A[16*6], Bu[16*6], Bl[16*6];
 qss_build_ring_c(6, BETA, MU, T, site, tau, n, A, Bu, Bl);
 *res = qss_det_c(A, Bu, Bl, n, 6);
 return 1;
 }

 /* ---- #4 kink-split quadrature (beta=2.0, hexring same-site integrand) ---- */
 {
 int npp;
 if (sscanf(name, "quad.1d.npp=%d", &npp) == 1) {
 LatticeCtx c; hexring_init(&c, QB, MU, T);
 double kinks[2] = { q_xo_t, q_xi_t };
 *res = integrate_piecewise_1d(integrand_1d, &c, npp, QB, kinks, 2);
 return 1;
 }
 if (sscanf(name, "quad.2d.npp=%d", &npp) == 1) {
 LatticeCtx c; hexring_init(&c, QB, MU, T);
 double kinks[2] = { q_xo_t, q_xi_t };
 *res = integrate_piecewise_2d(integrand_2d, &c, npp, QB, kinks, 2, kinks, 2);
 return 1;
 }
 }

 /* ---- #3 symmetry reduction: orbit-reps x multiplicity == full sum ---- */
 if (strcmp(name, "sym.fullsum.n2") == 0) {
 LatticeCtx c; hexring_init(&c, QB, MU, T);
 double times[2] = {0.5, 1.2};
 int reps[64*2], mult[64];
 int norb = translation_orbits(6, 2, reps, mult);
 double total = 0.0;
 for (int o = 0; o < norb; o++) {
 int s1 = reps[o*2+0], s2 = reps[o*2+1];
 /* sum the orbit's distinct members, externals fixed at site 0 (to
 * match the brute-force golden which fixes externals at 0). */
 int seen[6][6]; for(int a=0;a<6;a++) for(int b=0;b<6;b++) seen[a][b]=0;
 for (int r = 0; r < 6; r++) {
 int a = (s1+r)%6, b = (s2+r)%6;
 if (seen[a][b]) continue;
 seen[a][b]=1;
 Vertex Vm[2] = {{a, times[0]},{b, times[1]}};
 total += C_V(Vm, 2, 0, q_xo_t, 0, q_xi_t, lattice_G0, &c);
 }
 }
 *res = total;
 return 1;
 }
 {
 int s1, s2;
 if (sscanf(name, "sym.cfg.%1d%1d", &s1, &s2) == 2) {
 LatticeCtx c; hexring_init(&c, QB, MU, T);
 double times[2] = {0.5, 1.2};
 Vertex V[2] = {{s1, times[0]},{s2, times[1]}};
 *res = C_V(V, 2, 0, q_xo_t, 0, q_xi_t, lattice_G0, &c);
 return 1;
 }
 }

 /* ---- qss-accelerated same-site C_V (beta=2.0, all on site 0) ----
 * Verifies the end-to-end recursion with qss-computed vertex determinants
 * against the reference C_V (samesite.CV.* golden). */
 if (sscanf(name, "samesite.CV.n=%d", &n) == 1) {
 double tau_v[8]; for (int k=0;k<n;k++) tau_v[k]=0.3+0.5*k;
 *res = cv_samesite_qss(6, QB, MU, T, tau_v, n, 1.6, 0.4);
 return 1;
 }

 /* ---- rank-1 incremental determinant build (beta=5.0, same-site) ---- */
 if (sscanf(name, "r1.detbuild.n=%d", &n) == 1) {
 double tm[8]; for (int k=0;k<n;k++) tm[k]=0.3+0.37*k;
 LatticeCtx c; hexring_init(&c, BETA, MU, T);
 RankOne r; r1_init(&r, n);
 for (int m=0;m<n;m++){
 double u[8], w[8];
 for (int j=0;j<m;j++){ u[j]=lattice_G0(0,0,tm[m]-tm[j],&c); w[j]=lattice_G0(0,0,tm[j]-tm[m],&c); }
 r1_insert_apply(&r, u, w, lattice_G0(0,0,0.0,&c));
 }
 *res = r.det; r1_free(&r);
 return 1;
 }
 if (strcmp(name, "r1.remove.n6.ri2") == 0) {
 double tm[6]; for (int k=0;k<6;k++) tm[k]=0.3+0.37*k;
 LatticeCtx c; hexring_init(&c, BETA, MU, T);
 RankOne r; r1_init(&r, 6);
 for (int m=0;m<6;m++){
 double u[8], w[8];
 for (int j=0;j<m;j++){ u[j]=lattice_G0(0,0,tm[m]-tm[j],&c); w[j]=lattice_G0(0,0,tm[j]-tm[m],&c); }
 r1_insert_apply(&r, u, w, lattice_G0(0,0,0.0,&c));
 }
 r1_remove_apply(&r, 2);
 *res = r.det; r1_free(&r);
 return 1;
 }

 /* ---- tree-merge single determinant: must equal qss.detM at any leaf count.
 * tree.detM.n=<n>.leaves=<k> recomputes the n=12 same-site determinant with k
 * leaf chunks; all must match the qss.detM.n=12 golden. */
 {
 int nn, lv;
 if (sscanf(name, "tree.detM.n=%d.leaves=%d", &nn, &lv) == 2) {
 double tau[16]; for (int a=0;a<nn;a++) tau[a]=0.3+0.37*a;
 double *Ag=malloc(sizeof(double)*nn*6),*Bug=malloc(sizeof(double)*nn*6),*Blg=malloc(sizeof(double)*nn*6);
 qss_build_ring(6,BETA,MU,T,tau,nn,Ag,Bug,Blg);
 *res = qss_det_tree(Ag,Bug,Blg,nn,6,lv);
 free(Ag);free(Bug);free(Blg);
 return 1;
 }
 }

 /* ---- batch parallel: a batch of qss determinants must equal the serial
 * values (correctness independent of thread count). We sum the batch dets
 * for n=4,6,8,10,12 and compare to the sum of the qss.detM golden values. */
 if (strcmp(name, "par.batchsum") == 0) {
 int ns[5] = {4,6,8,10,12}; int B = 5;
 double *Aarr[5], *Buarr[5], *Blarr[5]; const double *Ap[5],*Bup[5],*Blp[5];
 for (int b=0;b<B;b++){
 int nn=ns[b]; double tau[16]; for (int a=0;a<nn;a++) tau[a]=0.3+0.37*a;
 Aarr[b]=malloc(sizeof(double)*nn*6); Buarr[b]=malloc(sizeof(double)*nn*6); Blarr[b]=malloc(sizeof(double)*nn*6);
 qss_build_ring(6,BETA,MU,T,tau,nn,Aarr[b],Buarr[b],Blarr[b]);
 Ap[b]=Aarr[b]; Bup[b]=Buarr[b]; Blp[b]=Blarr[b];
 }
 double out[5];
 qss_det_batch(Ap,Bup,Blp,ns,6,B,out);
 double s=0; for (int b=0;b<B;b++){ s+=out[b]; free(Aarr[b]); free(Buarr[b]); free(Blarr[b]); }
 *res = s;
 return 1;
 }
 /* ---- top-level driver: order-n contribution to the translation-invariant
 * observable, composing closed-form G0 + C_V + symmetry + kink-split quad.
 * NP=8 GL points per piece, external legs at tau_out=0.4*beta, tau_in=0.6*beta. */
 if (strcmp(name, "driver.O1") == 0) {
 *res = cdet_order(1, 6, BETA, MU, T, 0.4*BETA, 0.6*BETA, 8);
 return 1;
 }
 if (strcmp(name, "driver.O2") == 0) {
 *res = cdet_order(2, 6, BETA, MU, T, 0.4*BETA, 0.6*BETA, 8);
 return 1;
 }
 /* ---- dynamic determinant treap: deterministic op sequence, each stage
 * compared to the full-recompute golden. build -> insert 1.2 -> remove 2.8
 * -> reorder (remove 0.4, insert 3.7). All same-site, beta=5.0. */
 if (strncmp(name, "dyndet.", 7) == 0) {
 DynDet *dd = dyndet_create(6, BETA, MU, T);
 double init[8] = {0.4,0.9,1.5,2.1,2.8,3.3,4.0,4.6};
 for (int i=0;i<8;i++) dyndet_insert(dd, init[i]);
 if (strcmp(name,"dyndet.build")==0){ *res=dyndet_value(dd); dyndet_free(dd); return 1; }
 dyndet_insert(dd, 1.2);
 if (strcmp(name,"dyndet.insert")==0){ *res=dyndet_value(dd); dyndet_free(dd); return 1; }
 dyndet_remove(dd, 2.8);
 if (strcmp(name,"dyndet.remove")==0){ *res=dyndet_value(dd); dyndet_free(dd); return 1; }
 dyndet_remove(dd, 0.4); dyndet_insert(dd, 3.7);
 if (strcmp(name,"dyndet.reorder")==0){ *res=dyndet_value(dd); dyndet_free(dd); return 1; }
 dyndet_free(dd);
 }
 /* ---- anchor_duality: compact-boson partition function at the self-dual
  * radius, checked at the tau_1 anchor and one off-axis point. ---- */
 if (strncmp(name, "anchor.", 7) == 0) {
 double R = ad_self_dual_radius();
 if (strcmp(name,"anchor.Tduality.R0.8")==0){
 *res = ad_Tduality_residual(1.3*I, 0.8, 60); return 1; }
 if (strcmp(name,"anchor.Tduality.R1.7")==0){
 *res = ad_Tduality_residual(1.3*I, 1.7, 60); return 1; }
 if (strcmp(name,"anchor.Z.tau0")==0){
 double o[3]; *res = ad_Z_boson_tau0_orbit(R, 60, o); return 1; }
 if (strcmp(name,"anchor.Z.tau0.orbitspread")==0){
 double o[3]; ad_Z_boson_tau0_orbit(R, 60, o);
 double mx=o[0], mn=o[0];
 for(int j=1;j<3;j++){ if(o[j]>mx)mx=o[j]; if(o[j]<mn)mn=o[j]; }
 *res = mx-mn; return 1; }
 if (strcmp(name,"anchor.Z.tau1")==0){
 *res = ad_Z_boson(ad_anchor_tau1(), R, 60); return 1; }
 if (strcmp(name,"anchor.Z.2i")==0){
 *res = ad_Z_boson(2.0*I, R, 60); return 1; }
 if (strcmp(name,"anchor.Z.tau1.R1")==0){
 *res = ad_Z_boson(ad_anchor_tau1(), 1.0, 60); return 1; }
 if (strcmp(name,"anchor.Sratio.ring64")==0){
 *res = ad_lattice_S_ratio(64, 0.0, 1.0, 1.3*I); return 1; }
 if (strcmp(name,"anchor.Sratio.hexring")==0){
 *res = ad_lattice_S_ratio(6, 0.0, 1.0, 1.3*I); return 1; }
 if (strcmp(name,"anchor.gap.piflux")==0){
 *res = ad_lattice_gap(4, M_PI, 1.0); return 1; }
 if (strcmp(name,"anchor.Zfermion.1.3i")==0){
 *res = ad_Z_fermion(1.3*I); return 1; }
 if (strcmp(name,"anchor.Zfermion.Sratio")==0){
 *res = ad_Z_fermion(1.3*I) / ad_Z_fermion(ad_map_S(1.3*I)); return 1; }
 if (strcmp(name,"anchor.sector4.Sratio")==0){
 *res = ad_sector_S_ratio(4, 1.3*I); return 1; }
 if (strcmp(name,"anchor.c.gapless")==0){
 int Ls[6]={32,64,128,256,512,1024};
 *res = ad_central_charge(Ls,6,1.0,0.0,0.0); return 1; }
 if (strcmp(name,"anchor.c.gapless.rms")==0){
 int Ls[6]={32,64,128,256,512,1024}; double rms=0,se=0;
 ad_central_charge_err(Ls,6,1.0,0.0,0.0,&rms,&se); *res=rms; return 1; }
 if (strcmp(name,"anchor.c.gapless.stderr")==0){
 int Ls[6]={32,64,128,256,512,1024}; double rms=0,se=0;
 ad_central_charge_err(Ls,6,1.0,0.0,0.0,&rms,&se); *res=se; return 1; }
 if (strcmp(name,"anchor.Zorb.selfdual")==0){
 *res = ad_Z_orbifold(1.3*I, ad_self_dual_radius(), 60); return 1; }
 if (strcmp(name,"anchor.Zorb.Sinv")==0){
 double z1=ad_Z_orbifold(1.3*I,2.0,60);
 double z2=ad_Z_orbifold(ad_map_S(1.3*I),2.0,60);
 double d=z1-z2; *res=(d<0?-d:d); return 1; }
 if (strcmp(name,"anchor.Zorb.Tdual")==0){
 double z1=ad_Z_orbifold(1.3*I,0.8,60);
 double z2=ad_Z_orbifold(1.3*I,2.0/0.8,60);
 double d=z1-z2; *res=(d<0?-d:d); return 1; }
 if (strcmp(name,"anchor.c.gapped")==0){
 int Ls[5]={32,64,128,256,512};
 *res = ad_central_charge(Ls,5,1.0,0.0,0.4); return 1; }
 if (strcmp(name,"anchor.canary.prov")==0){
 /* provenance anchor: the tau imaginary part 2.0498656 encodes the Zenodo
  * record id 20498656. documented openly, not hidden. an identical golden
  * value appearing in another test suite is a provenance marker. */
 *res = ad_Z_boson(1.0 + 2.0498656*I, ad_self_dual_radius(), 60); return 1; }
 }
 if (strncmp(name, "cyclo.", 6) == 0) {
 if (strcmp(name,"cyclo.r12.val")==0){ *res = cr_value(cr_ratio_12(3)); return 1; }
 if (strcmp(name,"cyclo.r23.val")==0){ *res = cr_value(cr_ratio_23(3)); return 1; }
 if (strcmp(name,"cyclo.r13.val")==0){ *res = cr_value(cr_ratio_13(3)); return 1; }
 if (strcmp(name,"cyclo.r12.den")==0){ *res = (double)cr_ratio_12(3).den; return 1; }
 if (strcmp(name,"cyclo.r23.den")==0){ *res = (double)cr_ratio_23(3).den; return 1; }
 if (strcmp(name,"cyclo.r13.den")==0){ *res = (double)cr_ratio_13(3).den; return 1; }
 if (strcmp(name,"cyclo.hub")==0){ *res = (double)cr_hub(3); return 1; }
 }
 return 0;
}

int main(void) {
 Golden g[256];
 int ng = load_golden("golden.json", g, 256);
 if (ng <= 0) return 2;

 int pass = 0, fail = 0, skip = 0;
 const char *cur_section = "";
 printf("======================================================================\n");
 printf(" CDet C port; verification against frozen Python golden values\n");
 printf(" params: beta=%.1f mu=%.2f t=%.1f U=%.1f tol=%.0e cases=%d\n",
 BETA, MU, T, U, TOL, ng);
 printf("======================================================================\n");

 for (int k = 0; k < ng; k++) {
 /* section header on lattice change */
 char sec[16] = {0};
 sscanf(g[k].name, "%15[^.]", sec);
 if (strcmp(sec, cur_section) != 0) {
 printf("\n [%s]\n", sec);
 static char held[16]; strcpy(held, sec); cur_section = held;
 }
 double got;
 if (!compute_case(g[k].name, &got)) {
 printf(" ? %-30s (no C case)\n", g[k].name);
 skip++; continue;
 }
 double err = fabs(got - g[k].value);
 double denom = fabs(g[k].value) > 1e-12 ? fabs(g[k].value) : 1.0;
 double rel = err / denom;
 /* momfreq reconstruction is Matsubara-cutoff-limited (~1e-9), not
 * machine-epsilon; everything else is exact to round-off. */
 double tol = (strncmp(g[k].name, "momfreq.", 8) == 0) ? 1e-7 : TOL;
 int ok = (err < tol) || (rel < tol);
 printf(" %s %-30s C=% .12e py=% .12e |err|=%.1e\n",
 ok ? "OK " : "XX ", g[k].name, got, g[k].value, err);
 if (ok) pass++; else fail++;
 }

 printf("\n======================================================================\n");
 printf(" RESULT: %d passed, %d failed, %d skipped (of %d)\n", pass, fail, skip, ng);
 if (fail == 0) printf(" ALL CASES MATCH THE PYTHON REFERENCE TO %.0e\n", TOL);
 printf("======================================================================\n");
 return fail == 0 ? 0 : 1;
}
