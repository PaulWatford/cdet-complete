/* symmetry: skip the site arrangements that are just rotations of each other. See symmetry.h. */

#include "symmetry.h"
#include <stdlib.h>
#include <string.h>

/* canonical form of a site tuple under cyclic translation: the
 * lexicographically-smallest tuple among all L shifts (shift adds r mod L to
 * every entry). Writes canon[] (length n). */
static void canonical(const int *tuple, int n, int L, int *canon) {
 int best[16]; int have = 0;
 int cand[16];
 for (int r = 0; r < L; r++) {
 for (int i = 0; i < n; i++) cand[i] = (tuple[i] + r) % L;
 if (!have) { memcpy(best, cand, n*sizeof(int)); have = 1; continue; }
 /* lexicographic compare cand vs best */
 int c = 0;
 for (int i = 0; i < n; i++) { if (cand[i] != best[i]) { c = cand[i] - best[i]; break; } }
 if (c < 0) memcpy(best, cand, n*sizeof(int));
 }
 memcpy(canon, best, n*sizeof(int));
}

/* orbit size = L / (number of distinct shifts that map the canonical tuple to
 * itself). We compute it directly as the count of DISTINCT shifted tuples. */
static int orbit_size(const int *canon, int n, int L) {
 int seen = 0;
 int cand[16], uniq[64][16]; int nu = 0;
 (void)seen;
 for (int r = 0; r < L; r++) {
 for (int i = 0; i < n; i++) cand[i] = (canon[i] + r) % L;
 int dup = 0;
 for (int u = 0; u < nu; u++) {
 int same = 1;
 for (int i = 0; i < n; i++) if (uniq[u][i] != cand[i]) { same = 0; break; }
 if (same) { dup = 1; break; }
 }
 if (!dup) { memcpy(uniq[nu], cand, n*sizeof(int)); nu++; }
 }
 return nu; /* number of distinct configs in this orbit */
}

int translation_orbits(int L, int n, int *reps, int *mult) {
 /* enumerate all L^n tuples; keep each canonical tuple once. */
 long total = 1; for (int i = 0; i < n; i++) total *= L;
 int n_orb = 0;
 int tuple[16], canon[16];
 for (long idx = 0; idx < total; idx++) {
 long x = idx;
 for (int i = 0; i < n; i++) { tuple[i] = (int)(x % L); x /= L; }
 canonical(tuple, n, L, canon);
 /* is this tuple already its own canonical form? only then count it once */
 int is_canon = 1;
 for (int i = 0; i < n; i++) if (tuple[i] != canon[i]) { is_canon = 0; break; }
 if (!is_canon) continue;
 memcpy(&reps[n_orb*n], canon, n*sizeof(int));
 mult[n_orb] = orbit_size(canon, n, L);
 n_orb++;
 }
 return n_orb;
}
