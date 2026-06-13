# CROSSCHECK_v75 — the L=6 shell fold: exact 10M-config totals, rings, and the wrap correction

**Claims.** (1) Wrap correction: min-image collinearity is ill-defined on even-L tori (lines wrap
through the antipode; the per-config min-image rank is not orbit-consistent); the wrap-safe sector
(common cyclic line through origin) is 1,618 configs / 82% at L=4 (old: 808/77%) and 16,950 at L=6
(old: 3,774) — old numbers true for the smaller subsets; notes added to the v67/v70 docs.
(2) First exact L=6 totals over all 10,077,696 configs (240,464 orbit reps, both fillings): μ=0.5
−2.498377e-3 (the v70 pilot −2.3e-3 ± 4.5e-3 validated; the phase flip vs L=4 holds for the full
total); μ=1.5 −2.224768e-3. (3) Size trend, exact: sector share 82% (L=4) → 42% (L=6, μ=0.5), and
at μ=1.5 the sector opposes the total (−22%). (4) Rings persist at L=6 (2 sign changes per filling;
μ-dependent node positions ~3.0/4.5/5.5 vs ~3.5/4.0/5.0); period NOT resolved (irregular 0.5–1.5
spacings vs frozen π/k_F ≈ 1.1–1.2); refinement path named.

**Reproduce.** `cd 08_2d_interacting && python3 shell_fold.py` → sector counts, L=4 sector sum,
group-invariance over sampled orbits, stored-table arithmetic; "shell-fold self-test ... PASS"
(~1 min). The full fold reproduces from the staged pipeline (canonicalize → classify → evaluate in
range chunks, ~25 min), documented in SHELL_FOLD_RESULT.md.

**Scope (honest).** One β, fixed times, two fillings; ring period unresolved at this size/binning;
rank-2/3 sub-splits elsewhere in the package are deterministic partitions (valid for stratification)
whose geometric reading carries the same antipodal caveat.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
