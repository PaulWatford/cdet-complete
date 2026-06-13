/* lattices: each board answers one question, "how far apart, and the propagator".
 * Closed forms used where we have them, band-sum otherwise. See lattices.h. */

#include "lattices.h"
#include "cdet_engine.h"
#include <string.h>
#include <math.h>

/* ---------------------------- ATOM -------------------------------------- */
void atom_init(LatticeCtx *c, double beta, double mu) {
 memset(c, 0, sizeof(*c));
 c->beta = beta; c->mu = mu; c->t = 0.0; c->n_sites = 1;
}
double atom_G0(int i, int j, double tau, void *ctx) {
 (void)i; (void)j;
 LatticeCtx *c = (LatticeCtx*)ctx;
 return G0_atom(tau, c->beta, c->mu); /* tau==0 -> 0^- inside G0_atom */
}

/* ---------------- shared spectral-sum for diagonalised lattices --------- */
/* G0(i,j;tau) = sum_n <i|n><n|j> * g_band(eps_n - mu; tau),
 * g_band(tau; xi) = G0_atom(tau, beta, mu=-xi). Matches the Python exactly,
 * including the tau==0 -> 0^- convention via G0_atom. */
double lattice_G0(int i, int j, double tau, void *ctx) {
 LatticeCtx *c = (LatticeCtx*)ctx;
 int n = c->n_sites;
 double total = 0.0;
 for (int k = 0; k < n; k++) {
 double amp = c->evecs[i*n + k] * c->evecs[j*n + k];
 double xi = c->evals[k] - c->mu;
 total += amp * G0_atom(tau, c->beta, -xi);
 }
 return total;
}

/* ---------------- closed-form spectral data (CDNet technique #1) -------- */
/* Lagrange/resolvent projector onto eigenvalue e:
 * P_e = prod_{e' != e} (H - e' I) / (e - e')
 * Exact, basis-independent, handles degeneracy with no eigenvectors and no
 * iteration; the closed-form analogue of numerical diagonalisation, matching
 * the CDNet design choice (closed forms over matrix-exp / numerical eigh). */
void build_closed_form(LatticeCtx *c, const double *H,
 const double *distinct_evals, int n_distinct) {
 int n = c->n_sites;
 c->n_distinct = n_distinct;
 for (int d = 0; d < n_distinct; d++) {
 double e = distinct_evals[d];
 c->dist_evals[d] = e;
 /* M = I */
 double M[36], T[36];
 for (int i = 0; i < n*n; i++) M[i] = 0.0;
 for (int i = 0; i < n; i++) M[i*n+i] = 1.0;
 for (int dp = 0; dp < n_distinct; dp++) {
 if (dp == d) continue;
 double ep = distinct_evals[dp];
 double inv = 1.0 / (e - ep);
 /* T = M @ ((H - ep I) * inv) */
 for (int i = 0; i < n; i++) {
 for (int j = 0; j < n; j++) {
 double s = 0.0;
 for (int k = 0; k < n; k++) {
 double Hkj = H[k*n+j] - (k == j ? ep : 0.0);
 s += M[i*n+k] * Hkj * inv;
 }
 T[i*n+j] = s;
 }
 }
 for (int i = 0; i < n*n; i++) M[i] = T[i];
 }
 for (int i = 0; i < n*n; i++) c->proj[d][i] = M[i];
 }
}

double lattice_G0_closed(int i, int j, double tau, void *ctx) {
 LatticeCtx *c = (LatticeCtx*)ctx;
 if (c->n_distinct <= 0) return lattice_G0(i, j, tau, ctx); /* fallback */
 int n = c->n_sites;
 double total = 0.0;
 for (int d = 0; d < c->n_distinct; d++) {
 double amp = c->proj[d][i*n + j]; /* P_e[i,j] = sum over that eigenspace */
 double xi = c->dist_evals[d] - c->mu;
 total += amp * G0_atom(tau, c->beta, -xi);
 }
 return total;
}
void dimer_init(LatticeCtx *c, double beta, double mu, double t) {
 memset(c, 0, sizeof(*c));
 c->beta = beta; c->mu = mu; c->t = t; c->n_sites = 2;
 double H[4] = { 0.0, -t,
 -t, 0.0 };
 jacobi_eigh(H, 2, c->evals, c->evecs);
 /* exact distinct eigenvalues: -t, +t */
 double dev[2] = { -t, t };
 build_closed_form(c, H, dev, 2);
}

/* ---------------------------- PI-FLUX (4x4) ----------------------------- */
/* _HOP = [[0,1,0,-1],[1,0,1,0],[0,1,0,1],[-1,0,1,0]]; H_kin = -t * _HOP */
void piflux_init(LatticeCtx *c, double beta, double mu, double t) {
 memset(c, 0, sizeof(*c));
 c->beta = beta; c->mu = mu; c->t = t; c->n_sites = 4;
 double HOP[16] = {
 0, 1, 0,-1,
 1, 0, 1, 0,
 0, 1, 0, 1,
 -1, 0, 1, 0 };
 double H[16];
 for (int i = 0; i < 16; i++) H[i] = -t * HOP[i];
 jacobi_eigh(H, 4, c->evals, c->evecs);
 /* exact distinct eigenvalues: -sqrt(2) t, +sqrt(2) t (each doubly degenerate) */
 double s2 = sqrt(2.0) * t;
 double dev[2] = { -s2, s2 };
 build_closed_form(c, H, dev, 2);
}

/* ---------------------------- HEXRING (6x6) ----------------------------- */
/* nearest-neighbour ring: H[i, (i+1)%6] = H[(i+1)%6, i] = -t */
void hexring_init(LatticeCtx *c, double beta, double mu, double t) {
 memset(c, 0, sizeof(*c));
 c->beta = beta; c->mu = mu; c->t = t; c->n_sites = 6;
 double H[36];
 for (int i = 0; i < 36; i++) H[i] = 0.0;
 for (int i = 0; i < 6; i++) {
 int j = (i + 1) % 6;
 H[i*6 + j] = -t;
 H[j*6 + i] = -t;
 }
 jacobi_eigh(H, 6, c->evals, c->evecs);
 /* exact distinct eigenvalues: eps_k = -2t cos(2 pi k/6) = {-2t,-t,+t,+2t} */
 double dev[4] = { -2.0*t, -1.0*t, 1.0*t, 2.0*t };
 build_closed_form(c, H, dev, 4);
}
