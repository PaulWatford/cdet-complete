/* qss_det.c -- part of cdet-c-port v2.31
 * Author: Paul Watford, 2026. MIT license.
 */
/* qss_det: the fast determinant (the ratio/repeating-pieces trick). See qss_det.h. */

#include "qss_det.h"
#include <math.h>
#include <stdlib.h>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

void qss_build_ring(int L, double beta, double mu, double t,
 const double *tau, int n,
 double *A, double *Bu, double *Bl) {
 double s = 1.0 / sqrt((double)L);
 for (int k = 0; k < L; k++) {
 double eps = -2.0 * t * cos(2.0 * M_PI * (double)k / (double)L);
 double xi = eps - mu;
 double nF;
 double bx = beta * xi; /* overflow-stable Fermi fn */
 if (bx > 0) { double e = exp(-bx); nF = e / (1.0 + e); }
 else { nF = 1.0 / (1.0 + exp(bx)); }
 for (int a = 0; a < n; a++) {
 double ea_m = exp(-xi * tau[a]); /* e^{-xi tau_a} */
 double ea_p = exp(xi * tau[a]); /* e^{+xi tau_a} */
 A [a*L + k] = s * ea_m;
 Bu[a*L + k] = s * ea_p * nF;
 Bl[a*L + k] = s * ea_p * (-(1.0 - nF));
 }
 }
}

double qss_det(const double *A, const double *Bu, const double *Bl, int n, int L) {
 /* W is L x L, row-major, initialised to 0. */
 double W[36]; /* L <= 6 for the ring */
 for (int i = 0; i < L*L; i++) W[i] = 0.0;

 double det = 1.0;
 double WBu[6], WtA[6], redL[6], redU[6];

 for (int i = 0; i < n; i++) {
 const double *Ai = &A [i*L];
 const double *Bui = &Bu[i*L];
 const double *Bli = &Bl[i*L];

 /* WBu = W @ Bu_i (L^2) */
 for (int k = 0; k < L; k++) {
 double s = 0.0;
 for (int m = 0; m < L; m++) s += W[k*L + m] * Bui[m];
 WBu[k] = s;
 }
 /* pivot = A_i . (Bu_i - W Bu_i) */
 double piv = 0.0;
 for (int k = 0; k < L; k++) piv += Ai[k] * (Bui[k] - WBu[k]);
 det *= piv;
 if (piv == 0.0) return 0.0;

 /* WtA = W^T @ A_i (L^2) */
 for (int k = 0; k < L; k++) {
 double s = 0.0;
 for (int m = 0; m < L; m++) s += W[m*L + k] * Ai[m];
 WtA[k] = s;
 }
 /* reduced generators */
 for (int k = 0; k < L; k++) {
 redL[k] = Bli[k] - WBu[k];
 redU[k] = Ai[k] - WtA[k];
 }
 /* W += outer(redL, redU) / pivot (L^2) */
 double inv = 1.0 / piv;
 for (int k = 0; k < L; k++)
 for (int m = 0; m < L; m++)
 W[k*L + m] += redL[k] * redU[m] * inv;
 }
 return det;
}

void qss_reconstruct(const double *A, const double *Bu, const double *Bl,
 int n, int L, double *M) {
 for (int a = 0; a < n; a++) {
 for (int b = 0; b < n; b++) {
 const double *B = (a <= b) ? &Bu[b*L] : &Bl[b*L];
 double s = 0.0;
 for (int k = 0; k < L; k++) s += A[a*L + k] * B[k];
 M[a*n + b] = s;
 }
 }
}

/* ---- COMPLEX-generator qss (different-site vertex matrix) ---- */
void qss_build_ring_c(int L, double beta, double mu, double t,
 const int *site, const double *tau, int n,
 double _Complex *A, double _Complex *Bu, double _Complex *Bl) {
 double s = 1.0/sqrt((double)L);
 for (int k = 0; k < L; k++) {
 double eps = -2.0*t*cos(2.0*M_PI*(double)k/(double)L);
 double xi = eps - mu;
 double bx = beta*xi, nF;
 if (bx > 0) { double e=exp(-bx); nF=e/(1.0+e); } else nF=1.0/(1.0+exp(bx));
 double tpk = 2.0*M_PI*(double)k/(double)L;
 for (int a = 0; a < n; a++) {
 double _Complex phA = cexp(I*tpk*(double)site[a]);
 A[a*L+k] = s * phA * exp(-xi*tau[a]);
 }
 for (int b = 0; b < n; b++) {
 double _Complex phB = cexp(-I*tpk*(double)site[b]) * exp(xi*tau[b]);
 Bu[b*L+k] = s * phB * nF;
 Bl[b*L+k] = s * phB * (-(1.0 - nF));
 }
 }
}

double qss_det_c(const double _Complex *A, const double _Complex *Bu,
 const double _Complex *Bl, int n, int L) {
 double _Complex W[36];
 for (int i = 0; i < L*L; i++) W[i] = 0.0;
 double _Complex det = 1.0;
 double _Complex WBu[6], WtA[6], redL[6], redU[6];
 for (int i = 0; i < n; i++) {
 const double _Complex *Ai=&A[i*L], *Bui=&Bu[i*L], *Bli=&Bl[i*L];
 for (int k=0;k<L;k++){ double _Complex s=0; for(int m=0;m<L;m++) s+=W[k*L+m]*Bui[m]; WBu[k]=s; }
 double _Complex piv=0; for(int k=0;k<L;k++) piv+=Ai[k]*(Bui[k]-WBu[k]);
 det*=piv; if (piv==0.0) return 0.0;
 for (int k=0;k<L;k++){ double _Complex s=0; for(int m=0;m<L;m++) s+=W[m*L+k]*Ai[m]; WtA[k]=s; }
 for (int k=0;k<L;k++){ redL[k]=Bli[k]-WBu[k]; redU[k]=Ai[k]-WtA[k]; }
 double _Complex inv=1.0/piv;
 for (int k=0;k<L;k++) for(int m=0;m<L;m++) W[k*L+m]+=redL[k]*redU[m]*inv;
 }
 return creal(det);
}
static double local_det_lu(double *a, int m) {
 double det = 1.0;
 for (int col = 0; col < m; col++) {
 int piv = col; double best = fabs(a[col*m+col]);
 for (int r = col+1; r < m; r++)
 if (fabs(a[r*m+col]) > best) { best = fabs(a[r*m+col]); piv = r; }
 if (best == 0.0) return 0.0;
 if (piv != col) {
 for (int k=0;k<m;k++){ double tmp=a[col*m+k]; a[col*m+k]=a[piv*m+k]; a[piv*m+k]=tmp; }
 det = -det;
 }
 double d = a[col*m+col]; det *= d;
 for (int r = col+1; r < m; r++) { double f=a[r*m+col]/d; for(int k=col;k<m;k++) a[r*m+k]-=f*a[col*m+k]; }
 }
 return det;
}

/* same-site propagator G0(0,0; tau) on the ring, summed over bands. */
static double ss_g0(int L, double beta, double mu, double t, double tau) {
 double s = 1.0/(double)L, total = 0.0;
 for (int k = 0; k < L; k++) {
 double eps = -2.0*t*cos(2.0*M_PI*(double)k/(double)L);
 double xi = eps - mu;
 /* G0_atom with mu=-xi: fold tau into (-beta,beta] */
 double tt = tau;
 while (tt > beta) tt -= 2.0*beta;
 while (tt <= -beta) tt += 2.0*beta;
 double bx = beta*xi, nF;
 if (bx > 0) { double e=exp(-bx); nF=e/(1.0+e); } else nF=1.0/(1.0+exp(bx));
 double g;
 if (tt > 0) g = -(1.0-nF)*exp(-xi*tt);
 else if (tt < 0) g = nF*exp(-xi*tt);
 else g = nF;
 total += s*g;
 }
 return total;
}

static int popcnt(unsigned x){ int c=0; while(x){c+=x&1u;x>>=1;} return c; }

double cv_samesite_qss(int L, double beta, double mu, double t,
 const double *tau_v, int n,
 double tau_out, double tau_in) {
 if (n == 0) return ss_g0(L, beta, mu, t, tau_out - tau_in);
 if (n < 1 || n > 28) return 0.0/0.0; /* 2^n table; guard bounds (and warns) */

 /* ---- precompute ALL propagators ONCE (the fix: ss_g0 was being recomputed
 * O(m^2) times per subset, i.e. an exponential number of redundant exp/cos
 * evaluations on the SAME time-differences). Index 0..n-1 = vertices,
 * index n = tau_out (rows), index n+1 = tau_in (cols). G[a*(n+2)+b] =
 * ss_g0(time_a - time_b). Built in O(n^2 L); every subset just reads it. */
 int NT = n + 2;
 double *time = malloc(sizeof(double)*NT);
 for (int i=0;i<n;i++) time[i]=tau_v[i];
 time[n]=tau_out; time[n+1]=tau_in;
 double *G = malloc(sizeof(double)*NT*NT);
 for (int a=0;a<NT;a++) for (int b=0;b<NT;b++)
 G[a*NT+b] = ss_g0(L, beta, mu, t, time[a]-time[b]);

 /* qss generators for the FULL vertex set, ONCE. A subset's generators are
 * just the selected rows (they don't depend on the subset), so we build the
 * n-row generator table once and gather rows per subset. NOTE qss requires
 * the rows in ascending-time order; we keep a time-sorted index of vertices
 * so a subset's gathered rows are already sorted. */
 /* sorted vertex order */
 int *ord = malloc(sizeof(int)*n);
 for (int i=0;i<n;i++) ord[i]=i;
 for (int a=1;a<n;a++){ int key=ord[a]; double kt=tau_v[key]; int b=a-1;
 while(b>=0 && tau_v[ord[b]]>kt){ ord[b+1]=ord[b]; b--; } ord[b+1]=key; }
 double *Aall=malloc(sizeof(double)*n*L), *Buall=malloc(sizeof(double)*n*L), *Blall=malloc(sizeof(double)*n*L);
 double *ts=malloc(sizeof(double)*n);
 for (int i=0;i<n;i++) ts[i]=tau_v[ord[i]];
 qss_build_ring(L, beta, mu, t, ts, n, Aall, Buall, Blall);
 free(ts);
 /* map vertex original-index -> its position in sorted order */
 int *pos = malloc(sizeof(int)*n);
 for (int p=0;p<n;p++) pos[ord[p]] = p;

 int N = 1 << n;
 double *Dc = malloc(sizeof(double)*(size_t)N);
 double *Dv = malloc(sizeof(double)*(size_t)N);
 double *C = malloc(sizeof(double)*(size_t)N);
 double *A=malloc(sizeof(double)*n*L), *Bu=malloc(sizeof(double)*n*L), *Bl=malloc(sizeof(double)*n*L);
 double *Mup=malloc(sizeof(double)*(n+1)*(n+1));
 double *Add=malloc(sizeof(double)*n*n);
 int *idx=malloc(sizeof(int)*n); /* sorted vertex indices in subset */

 int crossover = 3*L; /* measured ~18 for L=6 */

 for (int mask = 0; mask < N; mask++) {
 /* gather the subset's vertices in time-sorted order, as ORIGINAL indices */
 int m = 0;
 for (int p=0;p<n;p++){ int v=ord[p]; if (mask&(1<<v)) idx[m++]=v; }

 if (m == 0) { Dc[mask] = G[n*NT + (n+1)]; Dv[mask] = 1.0; continue; }

 double detA;
 if (m > crossover) {
 /* gather sorted generator rows (already ascending by construction) */
 for (int i=0;i<m;i++){ int r=pos[idx[i]];
 for (int k=0;k<L;k++){ A[i*L+k]=Aall[r*L+k]; Bu[i*L+k]=Buall[r*L+k]; Bl[i*L+k]=Blall[r*L+k]; } }
 detA = qss_det(A, Bu, Bl, m, L); /* O(m L^2) */
 } else {
 /* dense det, entries READ from the precomputed table (no recompute) */
 for (int i=0;i<m;i++) for (int j=0;j<m;j++)
 Add[i*m+j] = G[idx[i]*NT + idx[j]];
 detA = local_det_lu(Add, m);
 }

 double sign = (m & 1) ? -1.0 : 1.0;
 Dv[mask] = sign * detA * detA; /* D_vac = (-1)^m det(A)^2 */

 /* M_up: row0=tau_out (index n), col0=tau_in (index n+1), rest = subset.
 * all entries read from the precomputed table. */
 int d = m+1;
 Mup[0] = G[n*NT + (n+1)];
 for (int j=0;j<m;j++) Mup[(j+1)] = G[n*NT + idx[j]];
 for (int i=0;i<m;i++) Mup[(i+1)*d] = G[idx[i]*NT + (n+1)];
 for (int i=0;i<m;i++) for (int j=0;j<m;j++)
 Mup[(i+1)*d + (j+1)] = G[idx[i]*NT + idx[j]];
 double detUp = local_det_lu(Mup, d);
 Dc[mask] = sign * detUp * detA; /* det(M_dn)=detA */
 }

 /* Rossi recursion */
 for (int k=0;k<=n;k++){
 for (int mask=0;mask<N;mask++){
 if (popcnt((unsigned)mask)!=k) continue;
 double value=Dc[mask];
 int sm=(mask-1)&mask;
 while(1){
 if (sm!=mask){ int comp=mask^sm; value -= C[sm]*Dv[comp]; }
 if (sm==0) break;
 sm=(sm-1)&mask;
 }
 C[mask]=value;
 }
 }
 double result = C[N-1];
 free(time); free(G); free(ord); free(Aall); free(Buall); free(Blall);
 free(pos); free(Dc); free(Dv); free(C); free(A); free(Bu); free(Bl);
 free(Mup); free(Add); free(idx);
 return result;
}
