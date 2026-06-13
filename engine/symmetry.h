/* symmetry: skip work the lattice tells you is repeated.
 *
 * The ring looks the same after a rotation, so most site arrangements are just
 * rotations of each other and give the identical answer. Instead of summing over
 * all L^n of them, we compute one from each rotation-family and multiply by the
 * family size. Same total, a fraction of the work. We stick to rotation symmetry
 * only (not reflections) so the shortcut stays provably exact and simple.
 */
#ifndef SYMMETRY_H
#define SYMMETRY_H

/* Enumerate translation-orbit representatives of n-vertex site tuples on a ring
 * of L sites. Two tuples are equivalent if one is a cyclic shift (by the same r
 * applied to every entry) of the other. For each orbit, writes the
 * lexicographically-smallest representative tuple into reps (row-major, each row
 * n ints) and its multiplicity (orbit size) into mult. Caller arrays must hold
 * up to L^n rows (an upper bound). Returns the number of orbits found.
 *
 * NOTE: a translation-invariant SUM over all L^n configs equals
 * sum over orbits of mult[o] * value(reps[o]).
 */
int translation_orbits(int L, int n, int *reps, int *mult);

#endif /* SYMMETRY_H */
