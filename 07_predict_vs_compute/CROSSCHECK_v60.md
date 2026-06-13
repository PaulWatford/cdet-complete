# CROSSCHECK_v60 — dual mechanism: τ-interference confirmed; anisotropy insufficient; closed-line residual

**Claims.** (1) Within-geometry (τ-only) fluctuation is 39–40% of var(ln|C|); integrating τ out raises
the MST law's R² from ~0.18–0.23 (per-sample) to 0.44–0.48 (τ-averaged). (2) Propagator decay is
anisotropic at L=8: ξ per Euclidean unit 0.90 (axis) vs 1.21–1.24 (face-diag) vs 1.20 (body-diag);
at L=6's short wrap-safe range the effect is only ~9% (range-dependent, flagged). (3) Neither the
τ-averaged Euclidean law (predicted 8.7×) nor the anisotropic-metric law (6.8×) reproduces the
measured τ-averaged 1d/bulk class ratio (75.5×, L=6); the stratified 1d class shows the
body-diagonal anomaly (MST 5.20, weight ≈ axis lines at MST 3.00). A ~10× closed-line enhancement
remains unexplained; the ring-closure/winding-coherence hypothesis is banked for v61 (untested).

**Reproduce.** `cd 08_2d_interacting && python3 dual_mechanism.py` → τ share, per-sample vs
τ-averaged R², L=8 anisotropy; gates (share 15–65%; averaging gain; face > 1.1× axis); "dual-mechanism
self-test ... PASS" (~2 min). Full three-round narrative and numbers: DUAL_MECHANISM_RESULT.md.

**Hardening note.** The first self-test draft printed ξ_face=114 at L=6 — a wraparound artifact (step
3 = antipode); fixed by wrap-safe step ranges and the anisotropy gate moved to L=8. Banked as a
lesson: wrap-unsafe fits can fake a 100× decay length.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
