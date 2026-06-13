/* qss_det.h -- part of cdet-c-port v2.31
 * Author: Paul Watford, 2026. MIT license.
 */
/* qss_det: the fast determinant for these matrices.
 *
 * A normal determinant treats the matrix as a dense blob and pays O(n^3). But
 * with the vertices sorted in time, every entry is really a ratio of the same
 * clock at two moments, so the whole matrix is built from only L repeating
 * pieces. We sweep through once carrying a small LxL running state and read the
 * answer off the pivots, in O(n*L^2). qss_det_c is the same trick over complex
 * numbers, for when the two ends sit on different sites (the sites add a phase).
 * Why: the determinant is the inner loop of everything; this is where the speed
 * lives.
 */
#ifndef QSS_DET_H
#define QSS_DET_H

#include <complex.h>

/* Build the rank-L generators for the same-site ring vertex matrix.
 * tau[] must be sorted ascending, length n. A,Bu,Bl are caller-allocated
 * arrays of size n*L (row-major: entry [a,k] at index a*L+k). */
void qss_build_ring(int L, double beta, double mu, double t,
 const double *tau, int n,
 double *A, double *Bu, double *Bl);

/* O(n L^2) quasiseparable determinant from the generators. */
double qss_det(const double *A, const double *Bu, const double *Bl, int n, int L);

/* ---- COMPLEX-generator qss for the DIFFERENT-site vertex matrix ----
 * Different lattice sites introduce phase factors e^{i 2pi k (i_a - j_b)/L} in
 * the eigenvector overlaps, making the generators complex (rank still L). The
 * recursion is identical, over C. The determinant of the (real) CDet matrix is
 * real; this returns its real part (imag is ~0 to round-off).
 *
 * Build generators for n time-sorted vertices, each (site[a], tau[a]):
 * A[a,k] = (1/sqrt L) e^{+i 2pi k site_a / L} e^{-xi_k tau_a}
 * Bu[b,k] = (1/sqrt L) e^{-i 2pi k site_b / L} e^{+xi_k tau_b} nF_k
 * Bl[b,k] = (1/sqrt L) e^{-i 2pi k site_b / L} e^{+xi_k tau_b} (-(1-nF_k))
 * A,Bu,Bl are caller arrays of n*L double _Complex (row-major). */
void qss_build_ring_c(int L, double beta, double mu, double t,
 const int *site, const double *tau, int n,
 double _Complex *A, double _Complex *Bu, double _Complex *Bl);

/* real part of the O(n L^2) determinant from complex generators. */
double qss_det_c(const double _Complex *A, const double _Complex *Bu,
 const double _Complex *Bl, int n, int L);

/* Reconstruct the dense matrix from generators (for cross-checking), row-major
 * n x n. M[a,b] = sum_k A[a,k] Bu[b,k] for a<=b, sum_k A[a,k] Bl[b,k] for a>b. */
void qss_reconstruct(const double *A, const double *Bu, const double *Bl,
 int n, int L, double *M);

/* ---- qss-accelerated same-site connected correlator ----
 * Computes C_V for n internal vertices and external (tau_out, tau_in), ALL on
 * the same ring site, using the Rossi recursion but with the square same-site
 * vertex determinants (D_vac's A and D_corr's M_dn) computed by the O(n L^2)
 * qss determinant instead of dense LU. The external-bordered M_up uses dense LU
 * (its two-sequence structure is not yet fast-pathed). Verified end-to-end
 * against the reference C_V (samesite.CV.* golden cases).
 *
 * tau_v[] are the n vertex times (need NOT be pre-sorted; sorted internally per
 * subset). Returns C_V. */
double cv_samesite_qss(int L, double beta, double mu, double t,
 const double *tau_v, int n,
 double tau_out, double tau_in);

#endif /* QSS_DET_H */
