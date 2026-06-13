/* qss_parallel: spread the determinant work across cores.
 *
 * Two jobs. One, run a whole batch of independent determinants at once across
 * cores, which is the real cost in Monte Carlo (many configs, all separate).
 * Two, split a single big determinant into time-chunks, summarise each chunk in
 * parallel, then glue the summaries up a tree. Both lean on the same verified
 * gluing maths, so the answer never depends on how many cores you used.
 */
#ifndef QSS_PARALLEL_H
#define QSS_PARALLEL_H

/* OpenMP batch: determinants of B independent real same-site quasiseparable
 * matrices. A[b],Bu[b],Bl[b] are each n[b]*L row-major generators. Writes
 * out[b] = qss_det(...). Embarrassingly parallel across b. */
void qss_det_batch(const double *const *A, const double *const *Bu,
 const double *const *Bl, const int *n, int L,
 int B, double *out);

/* Hierarchical tree-merge determinant of ONE real same-site quasiseparable
 * matrix (generators n*L row-major), using `nleaves` leaf chunks (>=1, clamped
 * to <= n). Leaves are summarised in parallel (OpenMP), then merged pairwise up
 * a balanced binary tree. Identical to qss_det to round-off. */
double qss_det_tree(const double *A, const double *Bu, const double *Bl,
 int n, int L, int nleaves);

/* number of OpenMP threads the batch will use (1 if built without OpenMP). */
int qss_parallel_threads(void);

#endif /* QSS_PARALLEL_H */
