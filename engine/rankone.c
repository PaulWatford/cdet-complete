/* rankone: patch the stored inverse and determinant when one vertex is added or dropped. See rankone.h. */

#include "rankone.h"
#include <stdlib.h>
#include <string.h>

void r1_init(RankOne *r, int capacity) {
 r->m = 0; r->cap = capacity; r->det = 1.0;
 r->Minv = malloc(sizeof(double)*(size_t)capacity*capacity);
 r->tmp = malloc(sizeof(double)*(size_t)capacity);
 r->tmp2 = malloc(sizeof(double)*(size_t)capacity);
}
void r1_free(RankOne *r) { free(r->Minv); free(r->tmp); free(r->tmp2); }

/* p = Minv w, q = Minv^T u, s = d - u.p */
static double schur(const RankOne *r, const double *u, const double *w, double d,
 double *p, double *q) {
 int m = r->m, cap = r->cap;
 for (int i = 0; i < m; i++) {
 double sp = 0.0, sq = 0.0;
 for (int j = 0; j < m; j++) { sp += r->Minv[i*cap+j]*w[j]; sq += r->Minv[j*cap+i]*u[j]; }
 p[i] = sp; q[i] = sq;
 }
 double s = d;
 for (int i = 0; i < m; i++) s -= u[i]*p[i];
 return s;
}

double r1_insert_ratio(const RankOne *r, const double *u, const double *w, double d) {
 if (r->m == 0) return d;
 return schur(r, u, w, d, r->tmp, r->tmp2);
}

void r1_insert_apply(RankOne *r, const double *u, const double *w, double d) {
 int m = r->m, cap = r->cap;
 if (m == 0) { r->Minv[0] = 1.0/d; r->det *= d; r->m = 1; return; }
 double *p = r->tmp, *q = r->tmp2;
 double s = schur(r, u, w, d, p, q);
 double inv = 1.0/s;
 /* top-left += p q^T / s */
 for (int i = 0; i < m; i++)
 for (int j = 0; j < m; j++)
 r->Minv[i*cap+j] += p[i]*q[j]*inv;
 /* new col m: -p/s ; new row m: -q/s ; corner 1/s */
 for (int i = 0; i < m; i++) { r->Minv[i*cap+m] = -p[i]*inv; r->Minv[m*cap+i] = -q[i]*inv; }
 r->Minv[m*cap+m] = inv;
 r->det *= s;
 r->m = m+1;
}

double r1_remove_ratio(const RankOne *r, int ri) {
 /* removing row/col ri: ratio = 1 / Minv[ri,ri] after permuting ri to last,
 * but Minv[ri,ri] is permutation-invariant on the diagonal -> ratio = 1/h
 * where h is the (ri,ri) entry. det(new) = det(old) * h. */
 int cap = r->cap;
 return r->Minv[ri*cap+ri];
}

void r1_remove_apply(RankOne *r, int ri) {
 int m = r->m, cap = r->cap;
 double h = r->Minv[ri*cap+ri];
 /* A^{-1} = E - f g^T / h, where f = col ri (excl ri), g = row ri (excl ri).
 * We remove row/col ri by compacting. Work on indices != ri. */
 /* gather f (col ri) and g (row ri) over the kept indices */
 int idx[1]; (void)idx;
 /* downdate in place over kept indices */
 for (int i = 0; i < m; i++) {
 if (i == ri) continue;
 double fi = r->Minv[i*cap+ri];
 for (int j = 0; j < m; j++) {
 if (j == ri) continue;
 double gj = r->Minv[ri*cap+j];
 r->Minv[i*cap+j] -= fi*gj/h;
 }
 }
 /* compact out row ri and col ri */
 for (int i = 0, di = 0; i < m; i++) {
 if (i == ri) continue;
 for (int j = 0, dj = 0; j < m; j++) {
 if (j == ri) continue;
 r->Minv[di*cap+dj] = r->Minv[i*cap+j];
 dj++;
 }
 di++;
 }
 r->det *= h;
 r->m = m-1;
}
