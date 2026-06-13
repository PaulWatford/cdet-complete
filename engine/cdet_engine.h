/* cdet_engine.h -- part of cdet-c-port v2.31
 * Author: Paul Watford, 2026. MIT license.
 */
/* cdet_engine: the shared rules every lattice plays by.
 *
 * Like a board-game rulebook that doesn't care which board you use. It knows how
 * a particle propagates, how to score a configuration (the Wick determinants),
 * and how to add up only the connected groups (the Rossi recursion). Each lattice
 * just hands it a "how far apart are two sites" function; the engine never looks
 * at the board's shape itself. Kept separate so all four lattices reuse one core.
 */
#ifndef CDET_ENGINE_H
#define CDET_ENGINE_H

#include <stddef.h>

/* ---- Hubbard-atom primitives (closed form; the band building block) ---- */
double n_F(double xi, double beta);
double G0_atom(double tau, double beta, double mu);
double G0_atom_at_zero_minus(double beta, double mu);
double G_exact_atom(double tau, double beta, double mu, double U);
double density_exact(double beta, double mu, double U);

/* ---- linear algebra (small dense, real) ---- */
/* Jacobi eigensolver for a real symmetric n x n matrix A (row-major).
 * On return evals[0..n-1] hold eigenvalues and evecs is n x n row-major with
 * column k the k-th eigenvector (evecs[i*n + k]). Matches numpy.linalg.eigh
 * up to the usual eigenvector sign/degeneracy freedom (the spectral SUM the
 * Green's function forms is invariant to that freedom). n <= 8. */
void jacobi_eigh(const double *A, int n, double *evals, double *evecs);

/* determinant of an m x m row-major matrix via LU with partial pivoting */
double det_lu(const double *M, int m);

/* ---- the CDet engine ----
 * A lattice provides a free Green's function through this signature.
 * site indices are ignored by the atom (pass 0,0). ctx carries lattice params.
 */
typedef double (*g0_fn)(int i, int j, double tau, void *ctx);

/* D_V(x_out,x_in) = (-1)^|V| det(M_up) det(M_dn) and D_V(empty)=(-1)^|V|det(A)^2
 * built from the supplied G0. Vertices carry a site and a time. */
typedef struct { int site; double tau; } Vertex;

double D_corr(const Vertex *V, int n,
 int site_out, double tau_out, int site_in, double tau_in,
 g0_fn g0, void *ctx);
double D_vac(const Vertex *V, int n, g0_fn g0, void *ctx);

/* Rossi connected correlator at vertex set V (length n).
 * n <= 16 (2^n subset table). For n=0 returns G0(out,in). */
double C_V(const Vertex *V, int n,
 int site_out, double tau_out, int site_in, double tau_in,
 g0_fn g0, void *ctx);

#endif /* CDET_ENGINE_H */
