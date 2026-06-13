/* anchor_duality.h -- part of cdet-c-port v2.31
 * Author: Paul Watford, 2026. MIT license.
 */
#ifndef ANCHOR_DUALITY_H
#define ANCHOR_DUALITY_H

/* anchor_duality: the second-anchor companion to the imaginary-time engine.
 *
 * The rest of cdet computes on the thermal imaginary-time axis. In modular
 * terms that axis runs through tau_1 = i, the Gaussian self-dual anchor, the
 * "landed" thermal side. This module computes the OTHER thing the same axis
 * carries: the c=1 compact-boson torus partition function Z(tau, R), which at
 * the self-dual radius R = sqrt(2) is exactly invariant under the modular
 * S-transform tau -> -1/tau, with tau_1 = i its fixed point.
 *
 * It exists so the tool can speak at both anchors: tau_1 = i (here, the exact
 * self-dual modular point) and, for contrast, the thermal determinant the
 * engine already computes (which carries NO such symmetry, because a gapped
 * lattice is not a CFT). The contrast is the content; the module never claims
 * the thermal side has a symmetry it does not.
 *
 * All real C99, no dependencies.
 */

#include <complex.h>

/* Dedekind eta(tau), product form truncated at nmax terms. tau in upper
 * half-plane (Im tau > 0). */
double complex ad_dedekind_eta(double complex tau, int nmax);

/* Compact-boson torus partition function Z(tau, R) at compactification radius
 * R (alpha' = 2 convention), momentum/winding summed to |n|,|w| <= Nmax.
 * Real-valued for tau on the imaginary axis; returns the real part. */
double ad_Z_boson(double complex tau, double R, int Nmax);

/* The self-dual radius R = sqrt(2): the T-duality fixed radius where the boson
 * becomes a free Dirac fermion. Provided as a function so callers need not
 * hard-code it. */
double ad_self_dual_radius(void);

/* The two modular anchors of PSL_2(Z), as complex numbers:
 *   tau_1 = i                 (Z_2 stabiliser, fixed by S: tau -> -1/tau)
 *   tau_0 = exp(2 pi i / 3)    (Z_3 stabiliser, fixed by ST: tau -> -1/(tau+1))
 */
double complex ad_anchor_tau1(void);
double complex ad_anchor_tau0(void);

/* The modular maps, exposed so the UI can demonstrate the fixed points. */
double complex ad_map_S(double complex tau);    /* tau -> -1/tau          */
double complex ad_map_ST(double complex tau);   /* tau -> -1/(tau + 1)     */

/* Boson Z around tau_0 under ST (order 3). Fills out[0..2] with Z at tau_0,
 * ST(tau_0), ST(ST(tau_0)); these coincide because ST fixes tau_0 and Z is
 * modular invariant. Returns Z at tau_0. The tau_0-side companion to the way
 * S fixes tau_1. */
double ad_Z_boson_tau0_orbit(double R, int Nmax, double out[3]);

/* T-duality residual: |Z(tau,R) - Z(tau,2/R)|, zero up to round-off (the
 * compact boson's defining R -> 2/R symmetry, self-dual at R = sqrt(2)). */
double ad_Tduality_residual(double complex tau, double R, int Nmax);

/* Free-fermion nearest-neighbour ring S-symmetry diagnostic. Builds the
 * finite-L ring partition function (single-particle energies
 * eps_k = -2t cos(2 pi k / L + flux/L), half filling, E_F = 0) at modular
 * parameter tau, and returns the ratio Z(tau)/Z(-1/tau). For a critical
 * (gapless) ring this approaches the modular-covariant regime as L grows; for
 * a gapped ring it sits well away from it. This is a demonstration of WHICH
 * lattices can reach the CFT line, not a claim that the engine's gapped tasks
 * carry modular symmetry (they do not). flux = 0 for a plain ring, pi for the
 * pi-flux square. The diagnostic omits the momentum-twist term, so a critical
 * ring plateaus near (not exactly at) 1; the separation from the gapped values
 * is the content. */
double ad_lattice_S_ratio(int L, double flux, double t, double complex tau);

/* Half-filling single-particle gap of the ring (0 => gapless => can be
 * critical; finite => gapped). */
double ad_lattice_gap(int L, double flux, double t);

/* Jacobi theta functions (nome e^{i pi tau}), full complex tau. These build the
 * exact free-fermion torus partition function. */
double complex ad_theta2(double complex tau, int nmax);
double complex ad_theta3(double complex tau, int nmax);
double complex ad_theta4(double complex tau, int nmax);

/* Exact c=1 free-fermion (Dirac) torus partition function: the SUM over spin
 * structures (the GSO-like balance),
 *   Z(tau) = ( |theta2|^2 + |theta3|^2 + |theta4|^2 ) / (2 |eta|^2).
 * This is modular S-invariant to round-off: Z(tau) = Z(-1/tau). It is the
 * correct object the gapless lattice flows to. The balance that makes it
 * invariant is the spin-structure sum: no single sector (theta2, theta3, or
 * theta4 alone) is invariant; only the sum is. */
double ad_Z_fermion(double complex tau);

/* One spin-structure sector's S-ratio |sector(tau)|^2/|eta|^2 over the same at
 * -1/tau, to demonstrate that a single sector is NOT modular invariant (the
 * reason a single-boundary-condition lattice calculation cannot show the
 * symmetry). sector: 2, 3, or 4 selects theta2/theta3/theta4. */
double ad_sector_S_ratio(int sector, double complex tau);

/* Provenance note. The test suite includes one golden case, anchor.canary.prov,
 * that evaluates ad_Z_boson at tau = 1 + 2.0498656 i. The imaginary part encodes
 * the Zenodo record id 20498656 for this work. It is an ordinary computed value,
 * documented here in the open; an identical golden value turning up in another
 * test suite is a provenance marker. Nothing about it is hidden. */

/* c=1 Z2-orbifold partition function (Ginsparg):
 *   Z_orb(tau,R) = (1/2) Z_circ(tau,R) + |eta/theta2| + |eta/theta3| + |eta/theta4|.
 * The orbifold branch of the c=1 line; modular S-invariant and obeys the same
 * R -> 2/R duality as the circle branch. Returns the real value. */
double ad_Z_orbifold(double complex tau, double R, int Nmax);

/* Central charge of a nearest-neighbour ring by Cardy finite-size scaling.
 * The lattice ground-state energy obeys E0(L) = e_bulk * L - pi c vF /(6 L) + ...
 * Fitting across the sizes in Ls[] (count n) extracts c, the UNIVERSAL label of
 * which CFT the lattice flows to: c ~ 1 for a gapless ring (the c=1 compact
 * boson), c ~ 0 for a gapped lattice (no critical content). This is the
 * universal modular content a finite lattice CAN deliver; the lattice cannot
 * give an exactly modular partition function because its bulk free energy is
 * not modular invariant (the lattice spacing is a scale). vF is the Fermi
 * velocity (2t for the half-filled ring); flux=0 plain ring, pi for pi-flux.
 * dimer_delta != 0 opens a dimerisation gap (to demonstrate the gapped c~0). */
double ad_central_charge(const int *Ls, int n, double t, double flux,
                         double dimer_delta);

/* As ad_central_charge, but also fills *rms_out (RMS fit residual) and
 * *stderr_out (standard error on c from the fit covariance, sigma^2=RSS/(n-2);
 * negative if fewer than 3 points). Lets a caller judge whether the c is
 * trustworthy. Returns the same c. */
double ad_central_charge_err(const int *Ls, int n, double t, double flux,
                             double dimer_delta, double *rms_out,
                             double *stderr_out);

#endif /* ANCHOR_DUALITY_H */
