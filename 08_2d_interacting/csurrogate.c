/* csurrogate.c (v86) -- THE CORE C SURROGATE: every banked advance of the program, frozen into a
 * dependency-free C module that composes with (and never touches) the frozen engine.
 *
 * WHAT IT CARRIES (provenance in brackets; scopes in csurrogate.h):
 *   - the 10 geometric features + transferable ln-magnitude model    [v74/v79]
 *   - the wrap-safe coherent-sector test (cyclic line through 0)     [v75]
 *   - the thermal-regime period law pi/beta                          [v77/v78]
 *   - the regime classifier (thermal/crossover/resonance)            [v80]
 *   - Class-I flip prediction: mu* = eps + logit(root)/beta          [v81/v83]
 *   - Class-II static prediction: mu* = mid + K/(2 beta)             [v82/v84]
 *   - orientation-from-flips parity stepping (anchor calibration)    [v77/v85]
 *
 * Validation: csurrogate_test.c compares every output against Python-generated reference vectors
 * (csurrogate_refs.h) to 1e-9; the gate module csurrogate.py regenerates references live from the
 * Python surrogate + atlas and rebuilds. The frozen engine stays untouched.
 */
#include <math.h>
#include <stdlib.h>
#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif
#include <string.h>
#include "csurrogate.h"
#include "csurrogate_params.h"

/* ---------- geometry helpers ---------- */
static void coords(int s, int L, double *v) {
    v[0] = s % L; v[1] = (s / L) % L; v[2] = s / (L * L);
}
static void minimg(const double *v, int L, double *o) {
    for (int a = 0; a < 3; a++) {
        double x = fmod(v[a] + L / 2.0, (double)L);
        if (x < 0) x += L;
        o[a] = x - L / 2.0;
    }
}
static double dmin(const double *p, const double *q, int L) {
    double d[3], m[3];
    for (int a = 0; a < 3; a++) d[a] = p[a] - q[a];
    minimg(d, L, m);
    return sqrt(m[0] * m[0] + m[1] * m[1] + m[2] * m[2]);
}

/* Prim MST over up to 4 points, origin included (decay_law.mst_length semantics) */
static double mst_with_origin(double pts[][3], int n, int L) {
    double P[4][3] = {{0, 0, 0}};
    for (int i = 0; i < n; i++) memcpy(P[i + 1], pts[i], 3 * sizeof(double));
    int m = n + 1, intree[4] = {1, 0, 0, 0}, cnt = 1;
    double tot = 0.0;
    while (cnt < m) {
        double best = 1e9; int bj = -1;
        for (int a = 0; a < m; a++) if (intree[a])
            for (int b = 0; b < m; b++) if (!intree[b]) {
                double d = dmin(P[a], P[b], L);
                if (d < best) { best = d; bj = b; }
            }
        tot += best; intree[bj] = 1; cnt++;
    }
    return tot;
}

/* exact integer rank of the 3x3 min-image displacement matrix (entries are integers) */
static int int_rank3(long M[3][3]) {
    int rank = 0;
    for (int c = 0; c < 3 && rank < 3; c++) {
        int piv = -1;
        for (int r = rank; r < 3; r++) if (M[r][c] != 0) { piv = r; break; }
        if (piv < 0) continue;
        for (int a = 0; a < 3; a++) { long t = M[rank][a]; M[rank][a] = M[piv][a]; M[piv][a] = t; }
        for (int r = rank + 1; r < 3; r++) {
            long f = M[r][c], g = M[rank][c];
            for (int a = 0; a < 3; a++) M[r][a] = M[r][a] * g - M[rank][a] * f;
        }
        rank++;
    }
    return rank;
}

/* ---------- the 10 features (surrogate2.feats2, ported) ---------- */
void surr_features(const int *sites, int L, double *f) {
    double pts[4][3] = {{0, 0, 0}}, sp[3][3];
    for (int i = 0; i < 3; i++) { coords(sites[i], L, pts[i + 1]); memcpy(sp[i], pts[i + 1], 24); }
    double legs[6]; int li = 0;
    for (int i = 0; i < 4; i++)
        for (int j = i + 1; j < 4; j++) legs[li++] = dmin(pts[i], pts[j], L);
    double mst = mst_with_origin(sp, 3, L);
    double D[3][3]; long Mi[3][3];
    for (int i = 0; i < 3; i++) {
        double d[3] = {sp[i][0], sp[i][1], sp[i][2]};
        minimg(d, L, D[i]);
        for (int a = 0; a < 3; a++) Mi[i][a] = lround(D[i][a]);
    }
    /* exact integer determinant (entries are integers by construction; v88 numerics fix) */
    long det = Mi[0][0] * (Mi[1][1] * Mi[2][2] - Mi[1][2] * Mi[2][1])
             - Mi[0][1] * (Mi[1][0] * Mi[2][2] - Mi[1][2] * Mi[2][0])
             + Mi[0][2] * (Mi[1][0] * Mi[2][1] - Mi[1][1] * Mi[2][0]);
    double vol = (double)(det < 0 ? -det : det);
    int rank = int_rank3(Mi);
    /* collinear groups by canonical direction (rounded unit vector, sign-canonical) */
    long key[3][3]; int kn = 0;
    double gpts[3][3][3]; int gcount[3] = {0, 0, 0};
    for (int i = 0; i < 3; i++) {
        double d[3]; minimg(sp[i], L, d);
        double nrm = sqrt(d[0] * d[0] + d[1] * d[1] + d[2] * d[2]);
        if (nrm < 1e-9) continue;
        long u[3], un[3];
        for (int a = 0; a < 3; a++) { u[a] = lround(d[a] / nrm * 100000.0); un[a] = -u[a]; }
        /* canonical = lexicographically smaller tuple of (u, -u) */
        int useneg = 0;
        for (int a = 0; a < 3; a++) {
            if (un[a] < u[a]) { useneg = 1; break; }
            if (un[a] > u[a]) break;
        }
        if (useneg) for (int a = 0; a < 3; a++) u[a] = un[a];
        int g = -1;
        for (int k = 0; k < kn; k++)
            if (key[k][0] == u[0] && key[k][1] == u[1] && key[k][2] == u[2]) { g = k; break; }
        if (g < 0) { g = kn++; memcpy(key[g], u, sizeof(u)); }
        memcpy(gpts[g][gcount[g]++], sp[i], 24);
    }
    double colls[3] = {0, 0, 0}; int cn = 0;
    for (int g = 0; g < kn; g++)
        if (gcount[g] >= 2) colls[cn++] = mst_with_origin(gpts[g], gcount[g], L);
    /* sort descending */
    for (int a = 0; a < cn; a++)
        for (int b = a + 1; b < cn; b++)
            if (colls[b] > colls[a]) { double t = colls[a]; colls[a] = colls[b]; colls[b] = t; }
    double lc1 = cn > 0 ? colls[0] : 0.0, lc2 = cn > 1 ? colls[1] : 0.0;
    double ext[3] = {0, 0, 0};
    for (int i = 0; i < 3; i++) {
        double d[3]; minimg(sp[i], L, d);
        for (int a = 0; a < 3; a++) if (fabs(d[a]) > ext[a]) ext[a] = fabs(d[a]);
    }
    double sumlegs = 0, minfirst3 = 1e9, maxleg = 0; int unit = 0;
    for (int i = 0; i < 6; i++) {
        sumlegs += legs[i];
        if (legs[i] > maxleg) maxleg = legs[i];
        if (fabs(legs[i] - 1.0) < 1e-6) unit++;
    }
    for (int i = 0; i < 3; i++) if (legs[i] < minfirst3) minfirst3 = legs[i];
    double maxext = ext[0] > ext[1] ? (ext[0] > ext[2] ? ext[0] : ext[2])
                                    : (ext[1] > ext[2] ? ext[1] : ext[2]);
    f[0] = mst; f[1] = lc1; f[2] = (double)rank; f[3] = sumlegs; f[4] = minfirst3;
    f[5] = maxleg; f[6] = (double)unit; f[7] = maxext / (mst > 1e-9 ? mst : 1e-9);
    f[8] = cbrt(vol); f[9] = lc2;
}

/* ---------- magnitude (v74/v79, frozen weights) ---------- */
double surr_ln_magnitude(const int *sites, int L) {
    double f[10];
    surr_features(sites, L, f);
    double y = SURR_W[0];
    for (int i = 0; i < 10; i++) y += SURR_W[i + 1] * (f[i] - SURR_MU[i]) / SURR_SD[i];
    return y + (L == 6 ? SURR_OFF_L6 : (L == 4 ? SURR_OFF_L4 : SURR_OFF_L6));
}

/* ---------- wrap-safe sector (v75): all sites on one cyclic line through the origin ---------- */
int surr_sector(const int *sites, int L) {
    for (int dx = 0; dx < L; dx++)
        for (int dy = 0; dy < L; dy++)
            for (int dz = 0; dz < L; dz++) {
                if (!dx && !dy && !dz) continue;
                int on[3] = {0, 0, 0};
                for (int k = 0; k < L; k++) {
                    int s = ((k * dx) % L) + L * (((k * dy) % L) + L * ((k * dz) % L));
                    for (int i = 0; i < 3; i++) if (sites[i] == s) on[i] = 1;
                }
                if (on[0] && on[1] && on[2]) return 1;
            }
    return 0;
}

/* ---------- the resonance atlas (v80-v85) ---------- */
int surr_regime(double beta, double gap) {
    double x = beta * gap;
    return x < REGIME_LO ? 0 : (x < REGIME_HI ? 1 : 2);   /* thermal / crossover / resonance */
}
double surr_thermal_period(double beta) { return M_PI / beta; }
void surr_class1_flips(int geom_id, double beta, double eps, double *out2) {
    for (int i = 0; i < 2; i++) {
        double r = ATLAS_ROOTS[geom_id][i];
        out2[i] = eps + log(r / (1.0 - r)) / beta;
    }
}
void surr_class1_flips_order(int order, double beta, double eps, double *out2) {
    const double *r = (order == 5) ? ATLAS_ROOTS_N5 : ATLAS_ROOTS_N4;
    for (int i = 0; i < 2; i++) out2[i] = eps + log(r[i] / (1.0 - r[i])) / beta;
}
double surr_class2_static(double beta) { return ATLAS_STATIC_MID + ATLAS_STATIC_K / (2.0 * beta); }
double surr_static_l6_deep(double beta) { return ATLAS_L6_DEEP_A + ATLAS_L6_DEEP_B / beta; }
double surr_static_l6_deep_inf(void) { return ATLAS_L6_DEEP_INF; }
double surr_static_l6_deep_law(double beta) { return ATLAS_L6_DEEP_ID + ATLAS_L6_DEEP_LNR / (6.0 * beta); }
double surr_static_l6_deep_alt(double beta) { return ATLAS_L6_DEEP_ALT + ATLAS_L6_DEEP_ALT_LNR / (7.0 * beta); }
/* v99/v100 coefficient-program carriers (see params header for the full status). */
double surr_l6_zpol36(void) { return ATLAS_L6_ZPOL36; }   /* the one-sector frozen-polynomial root */
double surr_l6_cross_slope(double beta) {                 /* v100 Delta cross-slope d1(beta), e-9   */
    double b0 = ATLAS_L6_XSLOPE_B[0], b1 = ATLAS_L6_XSLOPE_B[1];
    double d0 = ATLAS_L6_XSLOPE_D[0], d1 = ATLAS_L6_XSLOPE_D[1];
    return d0 + (d1 - d0) * (beta - b0) / (b1 - b0);       /* two-point secant interpolation         */
}
double surr_l6_root_linear(double beta) {                 /* linear (A + c1_eff s) root estimate     */
    double c1eff = ATLAS_L6_C1_FROZEN + surr_l6_cross_slope(beta);
    return ATLAS_L6_A_IS36 / (-c1eff);                    /* s* ~ A / |c1_eff|; beta=36 reference    */
}
double surr_l6_z_inf(void) { return ATLAS_L6_Z_INF_RESOLVED; }  /* v111-v114: RESOLVED z(inf)=2 (Fermi-surface probe level) */
double surr_l6_z_finite(double beta) {                   /* v112 finite-beta law: z = 2 - p*ln(beta)/beta */
    return 2.0 - ATLAS_L6_ZLAW_P * log(beta) / beta;     /* approaches 2 as a ln(beta)/beta crawl (p~2.6) */
}
double surr_l6_z_inf_legacy(void) { return ATLAS_L6_Z_INF; }   /* SUPERSEDED v107 underestimate 1.8818, kept for history */

int surr_l6_gap_modes(double lo, double hi) {
    /* number of cube_hopping(6) eigenvalues strictly in (lo,hi), from the integer multiplicities.
       For (1,2) returns 0 -> the freeze is exactly mu-rigid within a unit interval (v118/v119). */
    int n = 0;
    for (int lev = -6; lev <= 6; lev++)
        if ((double)lev > lo + 1e-12 && (double)lev < hi - 1e-12) n += ATLAS_L6_MULT[lev + 6];
    return n;
}
int surr_l6_occupied(double mu) {
    /* frozen occupied count for chemical potential mu: modes with eigenvalue <= floor-side of mu.
       In (1,2) this is the levels <=1 set (156), rigid across the interval. */
    int n = 0;
    for (int lev = -6; lev <= 6; lev++) if ((double)lev <= mu + 1e-12) n += ATLAS_L6_MULT[lev + 6];
    return n;
}

double surr_l6_pool(double beta) {                       /* v105 robust pool z(beta) (nearest grid) */
    int best = 0; double bd = 1e9;
    for (int i = 0; i < 3; i++) { double d = beta > POOL_STABLE_B[i] ? beta - POOL_STABLE_B[i] : POOL_STABLE_B[i] - beta;
        if (d < bd) { bd = d; best = i; } }
    return POOL_STABLE_Z[best];
}
int surr_orientation(int anchor_sign, const double *flips, int nflips, double mu) {
    int s = anchor_sign;
    for (int i = 0; i < nflips; i++) if (flips[i] < mu) s = -s;
    return s;
}

/* ---- v124-v129 consolidation: L-generalized scale law + continuum Friedel edge (no eigendecomposition) ---- */

double surr_lowest_empty(int L, double mu) {
    /* z(inf) for cube_hopping(L) at chemical potential mu = the lowest eigenvalue above mu.
       eps(k) = -2(cos+cos+cos); 1D values c[k] take ceil((L+1)/2) distinct values. Pure arithmetic. */
    double best = 1e300;
    for (int a = 0; a < L; a++) {
        double ca = -2.0 * cos(2.0 * M_PI * a / L);
        for (int b = 0; b < L; b++) {
            double cab = ca - 2.0 * cos(2.0 * M_PI * b / L);
            for (int c = 0; c < L; c++) {
                double e = cab - 2.0 * cos(2.0 * M_PI * c / L);
                if (e > mu + 1e-9 && e < best) best = e;
            }
        }
    }
    return best;   /* v124-v125: z(inf)=lowest-empty-level for ANY L; -> mu as L->inf (gap ~ L^-3.3) */
}

double surr_interacting_pole(int L, double mu, double U, double nsig) {
    /* v141 fold-in: the leading INTERACTING addition pole = free pole + Hartree shift U<n_-sigma>.
       z_interacting ~ surr_lowest_empty(L,mu) + U*nsig. This carries the v134 leading self-energy term
       (the Hartree shift; the exact interacting pole is eps + ReSigma, of which this is the U^1 piece).
       Pure arithmetic; the Sigma=0 limit (U=0 or nsig=0) recovers the free pole exactly. */
    return surr_lowest_empty(L, mu) + U * nsig;
}

double surr_sun_c1(int Nf, double d) {
    /* v147: SU(N) production carrier -- the first linked-cluster EoS coefficient from g0 x record (v144).
       c1 = -N(N-1) d^2: the N-independent amplitude d^2 (per-flavor density) times the record N(N-1).
       The full 2-site ln Z coefficient is beta times this (c1_production = beta * surr_sun_c1).
       Pure arithmetic; the record N(N-1) IS rational in N (v145), so this carries to any flavor number. */
    return -(double)Nf * (Nf - 1) * d * d;
}

double surr_sun_n1(int Nf, double d, double dp) {
    /* v147: SU(N) production carrier -- the first-order EoS density coefficient from g0 x record (v144).
       n1 = -(N-1) d d': the N-independent amplitudes d (per-flavor density) and d'=d(d)/dmu, times the
       record (N-1). Gives the leading interacting per-flavor density at any flavor number incl N=6 (Yb). */
    return -(double)(Nf - 1) * d * dp;
}

double surr_friedel_edge(int L, double mu) {
    /* v129: the Friedel edge of rho along x = half-max crossing of the occupied weight W(kx).
       W(kx) = #{(ky,kz): eps(k) <= mu}. Converges to kx/L ~ 0.347 (~120deg, 3-site end) as L->inf. */
    double *c = (double *)calloc((size_t)L, sizeof(double));
    for (int k = 0; k < L; k++) c[k] = -2.0 * cos(2.0 * M_PI * k / L);
    int half = L / 2 + 1;
    double *W = (double *)calloc((size_t)half, sizeof(double));
    double Wmax = 0.0;
    for (int kx = 0; kx < half; kx++) {
        long cnt = 0; double thr = mu - c[kx] + 1e-9;
        for (int ky = 0; ky < L; ky++)
            for (int kz = 0; kz < L; kz++)
                if (c[ky] + c[kz] <= thr) cnt++;
        W[kx] = (double)cnt; if (W[kx] > Wmax) Wmax = W[kx];
    }
    for (int kx = 0; kx < half; kx++) W[kx] /= Wmax;
    int i = 1; while (i < half - 1 && W[i] > 0.5) i++;   /* keep i in [1, half-1] */
    double w0 = W[i - 1], w1 = W[i], denom = (w1 - w0);
    double frac = (denom != 0.0) ? (i - 1) + (0.5 - w0) / denom : (double)i;   /* interpolated half-max */
    free(c); free(W);
    return frac / L;
}
