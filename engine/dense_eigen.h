/* dense_eigen: hand genuinely-dense matrices to the experts.
 *
 * For matrices with no structure to exploit, our own determinant has nothing
 * clever to do, so we delegate to Eigen, a mature library that's been tuned for
 * years. Optional, behind a build flag: the package stays dependency-free unless
 * you actually hit a big unstructured matrix and ask for it. Don't reinvent a
 * wheel someone polished for a decade.
 */
#ifndef DENSE_EIGEN_H
#define DENSE_EIGEN_H

#ifdef __cplusplus
extern "C" {
#endif

/* determinant of an n x n row-major matrix via Eigen's partial-pivot LU. */
double eigen_det(const double *M, int n);

/* eigenvalues of a real-symmetric n x n row-major matrix (ascending) via
 * Eigen's SelfAdjointEigenSolver. Writes n values into evals; if evecs != NULL,
 * writes the n x n row-major eigenvector matrix (column k = k-th eigenvector).
 * Returns 0 on success. */
int eigen_eigh(const double *A, int n, double *evals, double *evecs);

/* solve M x = b (M is n x n row-major, b length n) via Eigen partial-pivot LU.
 * writes x (length n). Returns 0 on success. */
int eigen_solve(const double *M, const double *b, int n, double *x);

#ifdef __cplusplus
}
#endif

#endif /* DENSE_EIGEN_H */
