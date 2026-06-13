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

#define LMAX 256  /* max lattice sites (ring extension); was implicitly 6 */

typedef struct {
 double beta, mu, t;
 int n_sites;
 double evals[LMAX];
 double evecs[LMAX*LMAX]; /* row-major n x n; column k = k-th eigenvector */
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

/* general L-site nearest-neighbour ring (analytic plane-wave eigenbasis, any
 * L up to LMAX; no diagonaliser). Extends hexring past 6 sites. */
void ring_init(LatticeCtx *c, int L, double beta, double mu, double t);

/* 2D square lattice (Lx x Ly torus, periodic). Separable circulant => eigenbasis
 * is the tensor product of two 1D ring bases; eps = -2t(cos kx + cos ky).
 * site index = y*Lx + x. Requires Lx*Ly <= LMAX. Numerical path (n_distinct=0). */
void square2d_init(LatticeCtx *c, int Lx, int Ly, double beta, double mu, double t);

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

/* ---- large-L plane-wave path (v162): the closed-form free propagator straight
 * from the dispersion eps = -2t(cos kx + cos ky), with NO O(N^2) eigenvector
 * storage. Memory is O(L) (a single 1D cosine table), so it reaches lattices far
 * beyond LMAX (e.g. 100x100 = 10^4 sites). Matches square2d_init / lattice_G0 to
 * round-off where both apply. This is the documented optimization route for going
 * past the 16x16 numerical cap; the point of the method is that you do not need
 * to -- past the correlation length (~12-16 sites) results are already the
 * thermodynamic limit -- but the path makes the infinite-system check cheap. */
#define PWLMAX 2048   /* 1D table cap -> lattices up to 2048x2048 if ever wanted */
typedef struct { int L, n; double beta, mu, t; double cos1d[PWLMAX]; } Square2DPW;
void   square2d_pw_init(Square2DPW *c, int L, double beta, double mu, double t);
double square2d_G0_pw(int i, int j, double tau, void *ctx);  /* ctx = Square2DPW* */

#endif /* LATTICES_H */
