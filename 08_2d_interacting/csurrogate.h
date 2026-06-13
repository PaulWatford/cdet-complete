/* csurrogate.h (v86; consolidated v120) -- the core C surrogate API. Scopes are the banked ones:
 *   ln-magnitude: median per-config transfer error 2.3x pooled over four independent draws,
 *     per-draw spread 1.7-2.7x (v79, revised v87); ceiling 0.95.
 *   sector: exact group-invariant test (v75).
 *   thermal period: pi/beta law verified beta 4-8 (v77); offsets geometry-dependent there.
 *   regime: empirical crossover beta*gap ~ 8-12 (v80).
 *   class-1 flips: roots stored for L=6 level 1, geom ids 0=(1,2,4) 1=(1,3,5) 2=(1,2,3);
 *     beta-transfer verified to max 0.022 over beta 12-28 (v83). CORRECTED SCOPE (v90/v91):
 *     the logit flow applies to mid-range roots; DEEP (small-f) roots live at the cancellation
 *     floor where the polynomial's tail is beta-dependent -- use the static family instead.
 *   static family: the L=8 (0.828+2.828)/2 crossing, K = -0.355 by flow (v84); and the L=6
 *     deep static z = 1.824 - 0.72/beta, geometry-independent (v90, devs 0.001-0.011).
 *   coefficient program (v96-v107): the (1,2)-window deep object's background is ALIVE; its frozen
 *     f2-polynomial root is z_pol(36)=1.8249 (surr_l6_zpol36); faithfulness FALSIFIED -> the delta1
 *     x f2 CROSS-TERM (surr_l6_cross_slope). v103: naive float64 drops the deep antiperiodic images
 *     (use the stable engine). v104-105: the robust pool RISES and fits no menu line (surr_l6_pool).
 *     v107-v114: the deep-beta program RESOLVED z(inf)=2 (surr_l6_z_inf): the menu rationals were
 *     finite-beta crossings of a ln(beta)/beta approach (surr_l6_z_finite); A is corner-confined ~1/beta^3,
 *     c1 level-2 de-confined ~beta^-0.3, and the probe is LOCKED to the Fermi surface. See csurrogate_params.h.
 *   orientation: parity stepping from one anchor measurement + a flip set (v77/v85).
 * The sign problem's exponential wall is NOT moved by any of this (the standing statement). */
#ifndef CSURROGATE_H
#define CSURROGATE_H
void   surr_features(const int *sites, int L, double *f10);
double surr_ln_magnitude(const int *sites, int L);
int    surr_sector(const int *sites, int L);
int    surr_regime(double beta, double gap);
double surr_thermal_period(double beta);
void   surr_class1_flips(int geom_id, double beta, double eps, double *out2);
void   surr_class1_flips_order(int order, double beta, double eps, double *out2); /* order 4 or 5 (v88);
   n=5 upper root marginal -- see params header */
double surr_class2_static(double beta); /* v84 L=8 K-flow form; SUPERSEDED by the v97/v100 root-flow
   reread (rises with beta; see SURROGATE_VS_BRUTE_RESULT.md) -- decisive deep L=8 scan queued */
double surr_static_l6_deep(double beta);   /* v91 law; v92 SCOPE: valid beta in [10,32] only */
double surr_static_l6_deep_inf(void);      /* v92: the measured deep-beta value (honest pool)  */
double surr_static_l6_deep_law(double beta); /* v93: z = 11/6 + ln(r)/(6 beta), the identified law */
double surr_static_l6_deep_alt(double beta); /* v94: the 13/7 competitor line, kept for scoring   */
double surr_l6_zpol36(void);             /* v99: one-sector frozen-polynomial root at beta=36 (1.8249) */
double surr_l6_cross_slope(double beta); /* v100: the delta1 x f2 cross-slope d1(beta) in e-9 (grows) */
double surr_l6_root_linear(double beta); /* v100: linear root s* ~ A/|c1+d1| (beta=36 ref); see header */
double surr_l6_z_inf(void);              /* v111-v114: RESOLVED z(inf)=2 (Fermi-surface probe level)    */
double surr_l6_z_finite(double beta);    /* v112: finite-beta law z = 2 - p*ln(beta)/beta (-> 2)        */
double surr_l6_z_inf_legacy(void);       /* SUPERSEDED v107 underestimate 1.8818 (history only)         */
int    surr_l6_gap_modes(double lo, double hi); /* v120: cube eigenvalues strictly in (lo,hi); (1,2)->0 (mu-rigid) */
int    surr_l6_occupied(double mu);      /* v120: frozen occupied count at mu (156 for mu in (1,2))     */
/* v124-v129 CONSOLIDATION: the scale law z(inf) generalized to ANY L (surr_lowest_empty) -- it equals the
 * lowest-empty eigenvalue and MARCHES to mu as L->inf (gap ~ L^-3.3, v125); ran a MILLION sites via the
 * hybrid's projector fast path (v124-v125). Budget to resolve z(inf) ~ L^3 ~ N (polynomial, no exp wall;
 * v126). The v116 sign(A,c1) selection rule: sign(A) converges (background), sign(c1) is ARITHMETIC JITTER
 * in L (v127-v128). A's continuum Friedel wavevector = the rho edge surr_friedel_edge -> ~0.347 (~120deg,
 * 3-site end), confirming v119's (120,180) as the L=6 sampling of the fixed Fermi surface (v129). */
double surr_lowest_empty(int L, double mu); /* v124-v125: z(inf)=lowest-empty eigenvalue for ANY L (-> mu)  */
double surr_interacting_pole(int L, double mu, double U, double nsig); /* v141: free pole + Hartree shift U<n_-s> */
double surr_sun_c1(int Nf, double d);            /* v147: SU(N) 1st linked-cluster coeff -N(N-1)d^2 (per beta*site) */
double surr_sun_n1(int Nf, double d, double dp); /* v147: SU(N) 1st-order EoS density coeff -(N-1)d d' */
double surr_friedel_edge(int L, double mu); /* v129: rho Friedel edge kx/L (half-max W); -> ~0.347 (120deg) */
double surr_l6_pool(double beta);        /* v105: robust deep pool z(beta) at the certified grid 36/44/52 */
int    surr_orientation(int anchor_sign, const double *flips, int nflips, double mu);
#endif
