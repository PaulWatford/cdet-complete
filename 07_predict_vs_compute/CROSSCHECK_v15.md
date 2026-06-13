# Cross-check proof data (v15) — u_sigma, a second independent ED route (triplet gap)

v14 could not reach an EXACT u_sigma (the Bethe endpoint route is singular at zero field).
The partial assist this round: measure u_sigma a SECOND independent way in ED and check it
against the v13 spin stiffness. Reproduce: `python spin_susceptibility_qf.py`.

## Method -- lowest triplet gap (finite-size spin susceptibility)
    Delta_t(U) = E0(S_z=1) - E0(S_z=0) = E0(N_up=L/4+1,N_dn=L/4-1) - E0(N_up=N_dn=L/4).
The first magnetization step sits at B = Delta_t, so chi_s ~ (1/L)/Delta_t, and in the c=1
SU(2)_1 spin sector chi_s = 2/(pi v_s) up to a constant; hence v_s ~ L*Delta_t. The lowest-
triplet dimension is U-independent in the CFT, so the constant is fixed ONCE at the exact
U=0 limit (real_patterns #11): v_s(U) = v_F * Delta_t(U)/Delta_t(0), v_F = sqrt2.

This shares nothing with the v13 spin stiffness except the U=0 anchor: the stiffness is a
ground-state TWIST response (curvature of E0 under a spin flux); this is an EXCITATION gap.

## Result (L=12, n=0.5)
| U | Delta_t | L*Delta_t | v_s (triplet) | v_s (v13 stiffness) | diff |
|---|---------|-----------|---------------|---------------------|------|
| 0 | 0.7321 | 8.7846 | 1.4142 | 1.4304 | 1.1% |
| 1 | 0.6555 | 7.8665 | 1.2664 | 1.3733 | 7.8% |
| 2 | 0.5863 | 7.0362 | 1.1327 | 1.2623 | 10.3% |
| 4 | 0.4697 | 5.6366 | 0.9074 | 1.0309 | 12.0% |
| 8 | 0.3236 | 3.8831 | 0.6251 | 0.7083 | 11.7% |

## Reading it
- The two independent ED observables of v_s agree at U=0 (calibration) and differ ~8-12%
  at U>0, the triplet route systematically LOWER. Both fall monotonically from v_F toward 0.
- The integrated spin stiffness (v13) stays the more reliable value: no operator-dimension
  assumption, no marginal corrections. The triplet gap carries the SU(2)_1 marginally-
  irrelevant current-current correction (a known log finite-size suppression of the triplet
  gap in spin chains), which pushes v_s(triplet) low and grows with the coupling -- the
  likely source of the ~10% gap (offered as the explanation, not a separately verified claim).
- It cannot be scaled away here: at n=0.5, L=12 (N=3) is the ONLY non-degenerate closed shell
  in ED reach (L=8, L=16 are open-shell; L=20 = 240M states). A documented ceiling, not an
  oversight.

## Status & next
CORROBORATED (v15): u_sigma(n=0.5) now rests on TWO independent robust ED measurements -- the
spin stiffness (v13) and the triplet gap (v15) -- agreeing at U=0 and bracketing u_sigma within
~12% across U=0..8. Combined with the v14 exact-limit bracket (U->0 -> v_F, U->inf -> 0), the
spin velocity is well constrained from several directions, though not yet pinned to an exact
curve. OPEN (the genuine remaining step): an EXACT u_sigma(U) via an INTEGRATED (not endpoint-
slope) Bethe formulation -- the spin susceptibility from the field response, or a Fourier-space
solution of the zero-field spin equation. The v9->v15 arc: detect (v9) -> verify pure-charge
(v10) -> finite-size control (v11) -> both velocities (v12) -> correct u_sigma (v13) -> exact-
limit bracket + Bethe-machinery validated on charge (v14) -> second independent u_sigma (v15).
