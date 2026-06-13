/* cdet_engine.c -- part of cdet-c-port v2.31
 * Author: Paul Watford, 2026. MIT license.
 */
/* cdet_engine: the shared rules every lattice plays by. See cdet_engine.h. */

#include "cdet_engine.h"
#include <math.h>
#include <string.h>
#include <stdlib.h>

/* ---------------- Hubbard-atom closed-form primitives ------------------- */

double n_F(double xi, double beta) {
 /* n_F(xi) = 1/(exp(beta*xi)+1), overflow-stable (matches Python). */
 double bx = beta * xi;
 if (bx > 0) { double e = exp(-bx); return e / (1.0 + e); }
 return 1.0 / (1.0 + exp(bx));
}

double G0_atom(double tau, double beta, double mu) {
 double xi = -mu;
 /* fold tau into (-beta, beta] via antiperiodicity (period 2 beta) */
 while (tau > beta) tau -= 2.0*beta;
 while (tau <= -beta) tau += 2.0*beta;
 if (tau > 0.0) return -(1.0 - n_F(xi, beta)) * exp(-xi * tau);
 else if (tau < 0.0) return n_F(xi, beta) * exp(-xi * tau);
 else return n_F(xi, beta); /* tau=0 -> 0^- convention */
}

double G0_atom_at_zero_minus(double beta, double mu) {
 return n_F(-mu, beta);
}

double G_exact_atom(double tau, double beta, double mu, double U) {
 double sign = 1.0;
 while (tau >= beta) { tau -= beta; sign *= -1.0; }
 while (tau < 0.0) { tau += beta; sign *= -1.0; }
 double Z = 1.0 + 2.0*exp(beta*mu) + exp(beta*(2.0*mu - U));
 double term1 = exp(mu * tau);
 double term2 = exp(mu*(beta + tau) - tau*U);
 return sign * (-(term1 + term2) / Z);
}

double density_exact(double beta, double mu, double U) {
 double Z = 1.0 + 2.0*exp(beta*mu) + exp(beta*(2.0*mu - U));
 return (exp(beta*mu) + exp(beta*(2.0*mu - U))) / Z;
}

/* ----------------------- small dense linear algebra --------------------- */

void jacobi_eigh(const double *A, int n, double *evals, double *evecs) {
 /* classic cyclic Jacobi for real symmetric A (n<=8). */
 double a[64]; /* working copy, up to 8x8 */
 for (int i = 0; i < n*n; i++) a[i] = A[i];
 for (int i = 0; i < n; i++)
 for (int j = 0; j < n; j++) evecs[i*n + j] = (i == j) ? 1.0 : 0.0;

 for (int sweep = 0; sweep < 100; sweep++) {
 double off = 0.0;
 for (int p = 0; p < n; p++)
 for (int q = p+1; q < n; q++) off += a[p*n+q]*a[p*n+q];
 if (off < 1e-30) break;
 for (int p = 0; p < n; p++) {
 for (int q = p+1; q < n; q++) {
 double apq = a[p*n+q];
 if (fabs(apq) < 1e-300) continue;
 double app = a[p*n+p], aqq = a[q*n+q];
 double phi = 0.5 * atan2(2.0*apq, aqq - app);
 double c = cos(phi), s = sin(phi);
 /* rotate rows/cols p,q */
 for (int k = 0; k < n; k++) {
 double akp = a[k*n+p], akq = a[k*n+q];
 a[k*n+p] = c*akp - s*akq;
 a[k*n+q] = s*akp + c*akq;
 }
 for (int k = 0; k < n; k++) {
 double apk = a[p*n+k], aqk = a[q*n+k];
 a[p*n+k] = c*apk - s*aqk;
 a[q*n+k] = s*apk + c*aqk;
 }
 for (int k = 0; k < n; k++) {
 double vkp = evecs[k*n+p], vkq = evecs[k*n+q];
 evecs[k*n+p] = c*vkp - s*vkq;
 evecs[k*n+q] = s*vkp + c*vkq;
 }
 }
 }
 }
 for (int i = 0; i < n; i++) evals[i] = a[i*n+i];
}

double det_lu(const double *M, int m) {
 /* Heap copy so arbitrarily large m is supported (the prior 8x8 stack buffer
 * was a latent bug for the large-matrix path). For the tiny Wick matrices
 * this allocation is negligible. */
 double *a = malloc(sizeof(double) * (size_t)m * m);
 if (!a) return 0.0/0.0;
 for (int i = 0; i < m*m; i++) a[i] = M[i];
 double det = 1.0;
 for (int col = 0; col < m; col++) {
 int piv = col; double best = fabs(a[col*m+col]);
 for (int r = col+1; r < m; r++)
 if (fabs(a[r*m+col]) > best) { best = fabs(a[r*m+col]); piv = r; }
 if (best == 0.0) { free(a); return 0.0; }
 if (piv != col) {
 for (int k = 0; k < m; k++) {
 double tmp = a[col*m+k]; a[col*m+k] = a[piv*m+k]; a[piv*m+k] = tmp;
 }
 det = -det;
 }
 double d = a[col*m+col];
 det *= d;
 for (int r = col+1; r < m; r++) {
 double f = a[r*m+col] / d;
 for (int k = col; k < m; k++) a[r*m+k] -= f * a[col*m+k];
 }
 }
 free(a);
 return det;
}

/* ----------------------- Wick determinants ------------------------------ */
/* Build matrix M[i,j] = G0(rows[i], cols[j]) where each entry is a
 * (site,tau) pair. Equal (site,tau) -> handled inside the lattice G0 via the
 * tau==0 0^- convention (the Python relies on G0(0)=0^-). */


static double build_and_det(const int *rs, const double *rt,
 const int *cs, const double *ct, int m,
 g0_fn g0, void *ctx) {
 if (m <= 0) return 1.0;
 double M[m*m];  /* v26: dynamic dim, no MAXDIM cap */
 for (int i = 0; i < m; i++)
 for (int j = 0; j < m; j++)
 M[i*m+j] = g0(rs[i], cs[j], rt[i] - ct[j], ctx);
 return det_lu(M, m);
}

double D_corr(const Vertex *V, int n,
 int site_out, double tau_out, int site_in, double tau_in,
 g0_fn g0, void *ctx) {
 int rs[n+1], cs[n+1]; double rt[n+1], ct[n+1];  /* v26: dynamic */
 /* M_up: (n+1)x(n+1); row0/col0 are external */
 rs[0] = site_out; rt[0] = tau_out;
 cs[0] = site_in; ct[0] = tau_in;
 for (int k = 0; k < n; k++) {
 rs[k+1] = V[k].site; rt[k+1] = V[k].tau;
 cs[k+1] = V[k].site; ct[k+1] = V[k].tau;
 }
 double det_up = build_and_det(rs, rt, cs, ct, n+1, g0, ctx);
 double det_dn = 1.0;
 if (n > 0) {
 int s[n]; double tt[n];
 for (int k = 0; k < n; k++) { s[k] = V[k].site; tt[k] = V[k].tau; }
 det_dn = build_and_det(s, tt, s, tt, n, g0, ctx);
 }
 double sign = (n & 1) ? -1.0 : 1.0;
 return sign * det_up * det_dn;
}

double D_vac(const Vertex *V, int n, g0_fn g0, void *ctx) {
 if (n == 0) return 1.0;
 int s[n]; double tt[n];
 for (int k = 0; k < n; k++) { s[k] = V[k].site; tt[k] = V[k].tau; }
 double detA = build_and_det(s, tt, s, tt, n, g0, ctx);
 double sign = (n & 1) ? -1.0 : 1.0;
 return sign * detA * detA;
}

/* ----------------------- Rossi recursion -------------------------------- */

static int popcount_int(unsigned x) {
 int c = 0; while (x) { c += x & 1u; x >>= 1; } return c;
}

double C_V(const Vertex *V, int n,
 int site_out, double tau_out, int site_in, double tau_in,
 g0_fn g0, void *ctx) {
 if (n == 0)
 return D_corr(NULL, 0, site_out, tau_out, site_in, tau_in, g0, ctx);

 int N = 1 << n;
 /* Memory: the DP must keep C (every submask C[sm] is read when a larger mask
  * is formed) and Dv (read as Dv[complement] for many masks): 2*2^n doubles.
  * Dc is read exactly once -- when its own C[mask] is formed -- so it need not
  * be stored. Computing the seed inline drops a full 2^n array (-1/3 RAM here)
  * with no change to the arithmetic or its order: result is bit-identical. */
 double *Dv = malloc(sizeof(double) * N);
 double *C = malloc(sizeof(double) * N);
 if (!Dv || !C) { free(Dv); free(C); return NAN; }  /* v26: OOM-safe, no segfault */

 Vertex sub[n];  /* v26: dynamic scratch, no fixed order cap */
 memset(sub, 0, sizeof(sub));
 for (int mask = 0; mask < N; mask++) {
 int m = 0;
 for (int i = 0; i < n; i++) if (mask & (1 << i)) sub[m++] = V[i];
 Dv[mask] = D_vac(sub, m, g0, ctx);
 }

 /* bottom-up by popcount; optimal submask iteration (3^n total) */
 for (int k = 0; k <= n; k++) {
 for (int mask = 0; mask < N; mask++) {
 if (popcount_int((unsigned)mask) != k) continue;
 int m = 0;
 for (int i = 0; i < n; i++) if (mask & (1 << i)) sub[m++] = V[i];
 double value = D_corr(sub, m, site_out, tau_out, site_in, tau_in, g0, ctx); /* seed, read once */
 int sm = (mask - 1) & mask;
 while (1) {
 if (sm != mask) {
 int complement = mask ^ sm; /* mask \ sm */
 value -= C[sm] * Dv[complement];
 }
 if (sm == 0) break;
 sm = (sm - 1) & mask;
 }
 C[mask] = value;
 }
 }
 double result = C[N - 1];
 free(Dv); free(C);
 return result;
}
