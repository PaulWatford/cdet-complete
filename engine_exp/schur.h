/* schur: how to glue two time-chunks into one.
 *
 * Each chunk of vertices boils down to a tiny summary: its log-determinant plus
 * two LxL "what crosses the seam" matrices. This file is the glue: given the
 * summary of the earlier chunk and the later chunk, it produces the summary of
 * the two joined. The glue obeys monoid rules (an empty chunk changes nothing,
 * and grouping doesn't matter), which is exactly what lets qss_det's tree and
 * dyndet's balanced tree both reuse it. One verified copy of the gluing maths.
 */
#ifndef SCHUR_H
#define SCHUR_H

/* summary of a contiguous (time-sorted) chunk; W,X are L*L row-major buffers
 * OWNED by the struct (malloc'd by the builders below, freed by schur_free). */
typedef struct { double logabs, sign; double *W, *X; } Summary;

/* allocate an identity summary (empty chunk) for ring size L. */
Summary schur_identity(int L);

/* summary of a single vertex's generators (one row each of A,Bu,Bl, length L). */
Summary schur_leaf(const double *Arow, const double *Burow, const double *Blrow, int L);

/* summary of a contiguous run of n vertices (generators n*L row-major). */
Summary schur_chunk(const double *A, const double *Bu, const double *Bl, int n, int L);

/* combined = merge(left, right) (NEW buffers). left is the EARLIER-time chunk. */
Summary schur_merge(const Summary *left, const Summary *right, int L);

/* copy / free helpers */
Summary schur_copy(const Summary *s, int L);
void schur_free(Summary *s);

/* determinant from a summary: sign * exp(logabs). */
double schur_det(const Summary *s);

#endif /* SCHUR_H */
