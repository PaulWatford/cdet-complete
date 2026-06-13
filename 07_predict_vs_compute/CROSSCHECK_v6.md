# Cross-check proof data (v6) — spin velocity via the Casimir energy (robust route)

The velocity, done the robust way. The endpoint-derivative route (v5 attempt) was
fragile: the dressed energy vanishes at the Fermi point, and reading its slope right
at the edge diverged at small U. This route uses an INTEGRATED quantity instead —
the finite-size Casimir term of the ground-state energy — so there is no boundary
slope, only ground-state energies. Reproduce: `python spin_velocity.py`.

## Method
    E0(L) = e_inf * L - (pi c v)/(6 L) + ...      (1+1D CFT, c per gapless sector)
Fit E0/L vs 1/L^2; v = -6*slope/(pi c). Ground-state energies only.

## Verification 1 — method against the EXACT Heisenberg spinon velocity (v_s = pi/2)
| fit window | v_s | vs pi/2 |
|---|---|---|
| L=12,14,16 | 1.6068 | +2.3% |
| L=14,16,18 | 1.5997 | +1.8% |
| L=16,18,20 | 1.5948 | +1.5% |
Monotone convergence toward pi/2 = 1.5708; the residual is the known SU(2)
logarithmic finite-size correction, which shrinks with L. e_inf is recovered to
0.02% (1/4 - ln2). The method recovers an exactly-known velocity.

## Verification 2 — Hubbard spin sector at strong coupling
Half-filled Hubbard, L=8,10,12, c=1:
| U | u_sigma | Heisenberg 2pi/U |
|---|---|---|
| 8  | 0.663 | 0.785 |
| 12 | 0.519 | 0.524 (1%) |
At U=12 the charge sector is frozen and u_sigma matches the Heisenberg value 2pi/U
to ~1%: the spin sector has flowed to a Heisenberg chain with J=4/U, and the Casimir
method pins it. Two independent confirmations of the same strong-coupling velocity.

## Honest boundary (what is NOT clean)
- Below U~10 on L<=12 the charge gap is too small to freeze the charge sector out of
  the Casimir term; the fit then conflates charge and spin and the small-U u_sigma is
  unreliable (negative at U=2). This needs larger lattices, not a different method.
- The weak-coupling end is bracketed exactly by u_sigma(U=0) = 2 (= v_F at half
  filling), but the interior small-U curve is not resolved here.
- The charge velocity u_rho at n=0.5 would need the doped Casimir sum (both sectors
  gapless), for which only L=8,12 are accessible — too few sizes for a clean fit.

## Status
- A robust, integrated-quantity velocity method, VERIFIED against the exact Heisenberg
  spinon velocity (pi/2) and confirmed in the Hubbard spin sector at strong coupling.
- The spin velocity is pinned at strong coupling and bracketed by the free value 2;
  the full u_sigma(U) curve and the charge velocity await larger lattices.
- This replaces the diverging endpoint-slope attempt: the method now lands on an
  exactly-known number instead of blowing up. That is the real win this pass.
