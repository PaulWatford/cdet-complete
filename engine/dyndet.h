/* dyndet: keep the determinant fresh as one vertex changes, cheaply.
 *
 * In Monte Carlo we move one dancer at a time, so redoing the whole determinant
 * each step is waste. We keep the vertices in a self-balancing tree sorted by
 * time, and each branch remembers a small summary of everything below it. Change
 * one vertex and only its branch back to the trunk gets recomputed (O(L^3 log n))
 * instead of the whole thing. Insert, remove, and "a vertex crosses another in
 * time" are all the same move underneath. Same-site (real) case, the common one.
 */
#ifndef DYNDET_H
#define DYNDET_H

typedef struct DynDet DynDet; /* opaque: a treap of vertex-time summaries */

/* create/destroy a dynamic determinant over a ring of L sites (same-site). */
DynDet *dyndet_create(int L, double beta, double mu, double t);
void dyndet_free(DynDet *d);

/* insert a vertex at time tau (O(L^3 log n)). Ties broken consistently. */
void dyndet_insert(DynDet *d, double tau);

/* remove the vertex nearest to time tau (must exist; O(L^3 log n)). */
void dyndet_remove(DynDet *d, double tau);

/* current determinant of the n x n same-site quasiseparable matrix (O(1)). */
double dyndet_value(const DynDet *d);

/* number of vertices currently held. */
int dyndet_size(const DynDet *d);

#endif /* DYNDET_H */
