/* cfriedel.c (v121) -- the elementary frozen Friedel object rho(0,r), ported to C.
 *
 * The decisive sign-side object (v119) is the frozen one-particle density matrix
 *     rho(0,r) = sum_{occupied k} U[0,k] U[r,k] = (1/N) sum_{eps(k)<=1} cos(k.r),
 * the Fourier transform of the OCCUPIED REGION in k-space. Until v120 it lived only in Python
 * (frozen_friedel_map.py, via numpy eigh). This port computes it directly from the PLANE-WAVE
 * structure of cube_hopping(6): the cube factorizes into three rings, so the eigenmodes are plane
 * waves k=(kx,ky,kz) with eps(k) = -2(cos(2pi kx/6)+cos(2pi ky/6)+cos(2pi kz/6)), and the projector
 * matrix element rho(0,r) is basis-independent. No eigenvectors, no spectrum file -- fully
 * self-contained, and exact (validated to 1e-9 against the Python eigh density matrix).
 *
 * The occupied set {eps(k)<=1} has 156 modes (matches surr_l6_occupied(mu in (1,2))=156). Because the
 * spectrum is INTEGER-valued (v120), this set is rigid for every mu in (1,2) -> rho is mu-invariant.
 *
 * Build: gcc -O2 -Wall -Werror -std=c11 -pedantic -o cfriedel cfriedel.c -lm
 * Usage: cfriedel test            -- self-validate against embedded Python references (prints PASS)
 *        cfriedel r x y z         -- print rho(0,(x,y,z))
 *        cfriedel map z           -- print the 2D sign-map over the (x,y,z=const) plane
 *        cfriedel occ             -- print the occupied-mode count (should be 156)
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

#define L 6
#define N (L*L*L)
static const double PI = 3.14159265358979323846;

static double eps(int kx, int ky, int kz) {
    return -2.0*(cos(2*PI*kx/L) + cos(2*PI*ky/L) + cos(2*PI*kz/L));
}

/* the elementary frozen density matrix rho(0,r): occupied = eps(k) <= 1 (level 1|2 boundary) */
double cfriedel_rho(int x, int y, int z) {
    double s = 0.0;
    for (int kx = 0; kx < L; kx++)
        for (int ky = 0; ky < L; ky++)
            for (int kz = 0; kz < L; kz++)
                if (eps(kx, ky, kz) <= 1.0 + 1e-9)
                    s += cos(2*PI*(kx*x + ky*y + kz*z)/(double)L);
    return s/(double)N;
}

int cfriedel_occupied(void) {
    int n = 0;
    for (int kx = 0; kx < L; kx++)
        for (int ky = 0; ky < L; ky++)
            for (int kz = 0; kz < L; kz++)
                if (eps(kx, ky, kz) <= 1.0 + 1e-9) n++;
    return n;
}

static int selftest(void) {
    /* embedded references from the Python eigh density matrix (frozen_friedel_map.py) */
    struct { int x, y, z; double v; } ref[] = {
        {0,0,0, 0.7222222222}, {1,0,0, 0.1388888889}, {2,0,0,-0.0277777778},
        {3,0,0, 0.0277777778}, {1,1,0,-0.0416666667}, {2,1,0,-0.0138888889},
        {1,1,1,-0.0185185185}, {3,3,3,-0.1018518519}, {2,3,0, 0.0000000000},
    };
    int nref = (int)(sizeof(ref)/sizeof(ref[0])), fail = 0;
    double worst = 0.0;
    for (int i = 0; i < nref; i++) {
        double got = cfriedel_rho(ref[i].x, ref[i].y, ref[i].z);
        double dev = fabs(got - ref[i].v);
        if (dev > worst) worst = dev;
        if (dev > 1e-9) { fail++; printf("RHO FAIL (%d,%d,%d): got %.10f want %.10f\n",
                                          ref[i].x, ref[i].y, ref[i].z, got, ref[i].v); }
    }
    if (cfriedel_occupied() != 156) { fail++; printf("OCC FAIL: %d != 156\n", cfriedel_occupied()); }
    if (fail == 0)
        printf("cfriedel: %d references MATCH the Python eigh density matrix (worst dev %.2e); occupied=156 -> PASS\n",
               nref, worst);
    return fail;
}

int main(int argc, char **argv) {
    if (argc >= 2 && !strcmp(argv[1], "test")) return selftest() ? 1 : 0;
    if (argc >= 2 && !strcmp(argv[1], "occ")) { printf("occupied modes (eps<=1): %d\n", cfriedel_occupied()); return 0; }
    if (argc >= 5 && !strcmp(argv[1], "r")) {
        int x = atoi(argv[2]), y = atoi(argv[3]), z = atoi(argv[4]);
        printf("rho(0,(%d,%d,%d)) = %+.10f\n", x, y, z, cfriedel_rho(x, y, z));
        return 0;
    }
    if (argc >= 3 && !strcmp(argv[1], "map")) {
        int z = atoi(argv[2]);
        printf("# elementary frozen Friedel sign-map rho(0,(x,y,%d)); +/- and 0=node, o=origin\n", z);
        printf("     ");
        for (int x = 0; x < L; x++) printf("x%d ", x);
        printf("\n");
        for (int y = 0; y < L; y++) {
            printf("y%d:  ", y);
            for (int x = 0; x < L; x++) {
                if (x == 0 && y == 0 && z == 0) { printf(" o "); continue; }
                double v = cfriedel_rho(x, y, z);
                printf(" %c ", fabs(v) < 1e-9 ? '0' : (v > 0 ? '+' : '-'));
            }
            printf("\n");
        }
        return 0;
    }
    fprintf(stderr, "usage: cfriedel test | r x y z | map z | occ\n");
    return 1;
}
