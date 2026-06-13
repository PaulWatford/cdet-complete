# Consolidation v176: one wall core, all models side by side

**What changed.** The v172–175 wall arc had spawned four modules (`wall_vs_size`, `wall_tide`, `wall_primes`,
`wall_twist`). `wall_twist` re-implemented the Lindhard susceptibility that `wall_vs_size` already had, just generalized
to rectangular + twisted grids. This consolidates them onto **one canonical core**, `wall_vs_size.chi0_max_rect(Lx, Ly,
beta, mu, thx, thy, t)`, of which the square-periodic `chi0_max` is the special case. `wall_twist` now delegates;
`wall_tide` and `wall_primes` already imported the core. Duplicate `_fermi`/`chi0_max` removed; results unchanged
(square-periodic dev 0.0e+00). The rect/twist upgrade now lives in the base, available to every wall module.

**Docs.** README gains a "Wall physics" section documenting `wall` / `tide` / `primes` / `twist` / `crosscheck` and the
shared core. New subcommand `cdet crosscheck` runs the side-by-side test below.

**The models, side by side, and what each informs about the others.**

| model | what it computes | cross-link verified |
|---|---|---|
| A frozen reference engine | atom G0 / connected determinant | parity anchor 194/194; A==C bit-identical (cdet validate) |
| B plane-wave lattice engine | free 2D propagator from eps_k | A==B at 0.00e+00 (cdet validate) |
| C analytic surrogate | the carrier constants | bit-identical to A |
| D SU(N) EoS + observables | 2-site interacting series + resummation | D<->E below |
| E wall suite | lattice Lindhard wall (one core) | E internal: 4 modules, one core (dev 0.0e+00) |

Cross-links checked by `cdet crosscheck`:
- **E internal** — `wall`/`tide`/`primes`/`twist` all route through `chi0_max_rect` (square dev 0.0e+00).
- **B <-> E** — the wall's susceptibility and the lattice density share the dispersion: `chi0(q=0) == dn/dmu` (the free
  compressibility) to 7e-13.
- **D <-> E** — the **same finite-radius phenomenon in two systems**: the EoS bare-U series has radius U_c^EoS = 1.054
  (the conformal-Borel singularity), the lattice RPA series has radius U_c^wall = 1.975. In both, resummation extends
  past the wall: at U=0.7 the bare EoS series has diverged (|bare-ED|=3.6) but conformal-Borel still tracks ED
  (|cb-ED|=0.009). The wall suite generalizes the EoS radius finding to the lattice.

**Issues found and fixed.** (1) duplicate Lindhard core across wall modules -> single `chi0_max_rect`; (2) README did
not document the wall suite -> added. (Other modules' dispersion/fermi belong to different physics — the weak-coupling
2D series and the production lattice — and were correctly left independent.)

**Retest (all models, post-consolidation, all pass).** surrogate (worst dev 3.55e-15); frozen 194/194; `cdet validate`
5/5; observable models D (eos/conformal/docc/chi/resummation/export) OK; wall models E (vs_size/tide/primes/twist) PASS;
consolidation cross-check PASS; CLI self-test, packaging, docker gates PASS. Frozen reference engine untouched.
