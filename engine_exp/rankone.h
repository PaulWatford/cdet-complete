/* rankone: add or drop one vertex without redoing the matrix.
 *
 * Adding a vertex just glues one new row and column onto the edge of the matrix.
 * Rather than refactor from scratch (O(m^3)), we patch the stored inverse and
 * running determinant in O(m^2), the way you'd update a running total instead of
 * re-adding the whole column. Two uses: building a determinant up through nested
 * subsets, and Monte Carlo accept/reject ratios for insert/remove moves. A stock
 * dense library can't do this; it doesn't know the matrices are related.
 */
#ifndef RANKONE_H
#define RANKONE_H

typedef struct {
 int m; /* current size */
 int cap; /* capacity */
 double *Minv; /* cap x cap row-major inverse (top-left m x m valid) */
 double det; /* current determinant */
 double *tmp; /* scratch length cap (p, q) */
 double *tmp2;
} RankOne;

/* allocate for matrices up to capacity x capacity. Starts empty (m=0, det=1). */
void r1_init(RankOne *r, int capacity);
void r1_free(RankOne *r);

/* ratio for appending row u^T (length m), col w (length m), corner d:
 * returns s = det(new)/det(old). Does NOT modify state (use for MC accept test). */
double r1_insert_ratio(const RankOne *r, const double *u, const double *w, double d);

/* apply the append (updates Minv and det). u,w length m (current size). */
void r1_insert_apply(RankOne *r, const double *u, const double *w, double d);

/* ratio for removing row/col index ri: det(new)/det(old). No state change. */
double r1_remove_ratio(const RankOne *r, int ri);

/* apply the removal of row/col ri (updates Minv and det). */
void r1_remove_apply(RankOne *r, int ri);

#endif /* RANKONE_H */
