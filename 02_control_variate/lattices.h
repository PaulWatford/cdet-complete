/* lattices: the four boards, each just supplying "how far apart".
 *
 * Atom, dimer, pi-flux, hexring. Each one only has to answer one question for the
 * engine: given two sites and a time gap, what's the propagator? It can answer
 * the slow way (sum over bands) or, where we worked it out, the exact closed form
 * (Lagrange/resolvent projectors), which is both faster and more precise. The
 * engine stays geometry-blind; all the board-specific knowledge lives here.
 */
#ifndef LATTICES_H
#define LATTICES_H

typedef struct {
 double beta, mu, t;
 int n_sites;
 double evals[6];
 double evecs[36]; /* row-major n x n; column k = k-th eigenvector */
 /* closed-form path (CDNet technique #1): distinct eigenvalues and their
 * Lagrange/resolvent projectors P_e (exact, basis-independent). When
 * n_distinct > 0 the spectral sum uses these instead of the Jacobi
 * eigenvectors above. */
 int n_distinct;
 double dist_evals[6];
 double proj[6][36]; /* proj[e] is n x n row-major projector onto eigenvalue e */
} LatticeCtx;

/* atom: single site, no diagonalisation */
void atom_init(LatticeCtx *c, double beta, double mu);
double atom_G0(int i, int j, double tau, void *ctx);

/* multi-site lattices: build kinetic matrix, diagonalise, cache */
void dimer_init (LatticeCtx *c, double beta, double mu, double t);
void piflux_init (LatticeCtx *c, double beta, double mu, double t);
void hexring_init(LatticeCtx *c, double beta, double mu, double t);

/* shared spectral-sum G0 for any diagonalised lattice (numerical/Jacobi path) */
double lattice_G0(int i, int j, double tau, void *ctx);

/* closed-form spectral-sum G0 (CDNet technique #1): uses the exact distinct
 * eigenvalues + Lagrange projectors instead of the iterative eigensolver.
 * Identical result to lattice_G0 to round-off; deterministic, no iteration.
 * Falls back to lattice_G0 if no closed-form data is present. */
double lattice_G0_closed(int i, int j, double tau, void *ctx);

/* build the exact distinct-eigenvalue Lagrange projectors for a lattice whose
 * kinetic matrix H (n x n row-major) has the given distinct eigenvalues. */
void build_closed_form(LatticeCtx *c, const double *H,
 const double *distinct_evals, int n_distinct);

#endif /* LATTICES_H */
