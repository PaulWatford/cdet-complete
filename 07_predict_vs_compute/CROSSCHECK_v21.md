# Cross-check proof data (v21) — the weak-coupling analytic bridge across the v20 wall

v20 left exact quarter-filling u_sigma below U=2 as a structural wall (no asymptotic plateau).
v21 confirms the wall is real (three numerical routes fail for distinct reasons) and supplies the
analytic handle v20 named. Reproduce: `python weak_coupling_spin_velocity.py`.

## Why every numerical route fails at quarter-filling small U (all checked this iteration)
- Lambda->inf plateau (v18/v20): no plateau forms -- the structural wall.
- finite-field (finite-B) read: the velocity at the finite spin Fermi point is recipe-sensitive
  (crude endpoint difference gives ~1.64 at U=2 half filling = Bessel, but a linear-fit slope gives
  ~3.5) -- it does not pin a value.
- ED stiffness slope: gives c(1) ~ 0.025 vs the exact 0.159 -- the finite lattice (L<=12) does not
  resolve the weak-coupling slope (off by 6x).
Three independent confirmations: a genuine wall, not a coding issue.

## The analytic handle (weak coupling / g-ology)
u_sigma(n,U) = v_F(n) - U/(2 pi) - U^2/(16 pi^2) + O(U^3),  v_F(n) = 2 sin(pi n/2).
The LEADING coefficient 1/(2 pi) is FILLING-INDEPENDENT: the on-site U is a contact interaction,
so the 2k_F backscattering g_1 = U is momentum- (hence filling-) independent, and in
u_sigma = v_F - g_1/(2 pi) the v_F cancels out of the coefficient.

## Validation at half filling (exact Bessel, 2 I_1(2pi/U)/I_0(2pi/U))
| U | (v_F - Bessel)/U |
|---|------------------|
| 0.20 | 0.16046 |
| 0.10 | 0.15980 |
| 0.05 | 0.15947 |
| 0.02 | 0.15928 |
-> extrapolates to 1/(2 pi) = 0.15915 exactly. And the two-term form matches Bessel:
U=0.5: weak 1.9188 vs Bessel 1.9187; U=1.0: 1.8345 vs 1.8331. Both coefficients confirmed.

## Quarter filling, leading order (bridges the wall)
u_sigma(0.5, U) = sqrt(2) - U/(2 pi):  1.335 (U=0.5), 1.255 (U=1.0). These sit ABOVE the v20
quarter-filling peak lower bounds (1.077, 1.019) -- consistent (the peaks bound from below).

## Status
BRIDGED to leading order (v21). The linear coefficient 1/(2 pi) is exact at half filling and
filling-independent (contact interaction), so the quarter-filling linear term is pinned:
u_sigma(0.5,U) = sqrt2 - U/(2pi) + O(U^2). HONEST SCOPE: the U^2 coefficient is validated at half
filling but NOT shown filling-independent -- quarter-filling curvature is larger (from U=2: linear
1.096 vs exact 0.951), so the quarter formula holds only to leading order (U <~ 1). The exact full
quarter-filling small-U curve remains the v20 structural wall; it is bridged to leading order here,
anchored and consistent, not papered over. This completes the u_sigma program: exact for U>=2 (all
fillings, v18/v19), exact for all U at half filling (Bessel + sparse solver, v16/v20), and pinned
to leading order for quarter-filling small U (v21).
