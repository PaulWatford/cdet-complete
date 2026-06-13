# The sign side (v117): A's sign is a Friedel oscillation — the Fermi surface governs scale AND sign

v116 showed the sign of A is the geometric degree of freedom (scale z=2 universal, sign not). v117
asks whether the sign is *predictable*. The propagator g0(i,j,τ) = Σ_k U[i,k]U[j,k] occ_k(τ) carries
U[i,k]U[j,k] ~ cos(k·(r_i−r_j)) on the cube lattice, so the sign should oscillate with site separation
at a Fermi wavelength (Friedel-class, cf. v68). Prediction registered before measuring.

## Result — the sign oscillates, and the scale is the Fermi 2k_F

Scanning one vertex site along the x-axis (others fixed, β=24), sign(A) = **(−,−,−,+,+)** for x=1…5 —
a reproducible zero-crossing (signs agree across seeds 31 and 777; |A| is minimal at the flip).
**A's sign is geometric and oscillatory — Friedel-class, confirmed.**

The wavelength is **long, not period-2**. μ=1.845 sits near the 1D band top (max |ε|=2), so the Fermi
surface is small. From −2cos(θ_F)=μ: θ_F=2.745, the Friedel wavevector 2k_F aliases to 0.793 rad →
wavelength **≈7.93 sites** (half ≈4.0) → ~1 flip per 4 sites, matching the single flip seen in the
5-site scan. The registered period-2 sub-guess ("level-2 = momentum π") was **wrong** — it assumed the
wrong momentum; the actual Fermi surface at this μ is small and the wavelength long. A is a connected
determinant of several propagators, so the net sign is a superposition of cos(k·Δr) terms rather than
a single clean cosine, but the oscillation *scale* matches the Fermi 2k_F.

## The unifying conclusion

The Fermi surface governs **both** sides of the object:

- the deep-β **SCALE** z(∞)=2, via its energy **gap** ξ₂ = 2−μ = 0.155 (v112–v116), and
- the **SIGN** structure, via its **momentum** 2k_F → Friedel wavelength ~8 sites (v117).

v116 found sign and scale *separate* — independent axes (z=2 universal, sign geometric). v117 finds
they share **one origin**: the Fermi surface, acting through two channels. The **gap** sets where the
deep-β object sits (z=2); the **momentum** sets how its sign oscillates in space. The same Fermi
surface that pins the scale by its energy paints the sign by its wavevector.

This also localizes the old v68 "Friedel-class sign coherence": it is the background determinant A
itself whose sign oscillates at 2k_F. None of this moves the wall — but it is the first time the
*sign* and the *scale* of this object are traced to the same single object (the Fermi surface) by two
distinct mechanisms.

Reproduce: `python3 site_sign_friedel.py` (self-test PASS); the scan via
`./cse grid 24 24 1 16 2048 31 0.002 0 2 8 43 <j>` for j=1…5. Frozen engine untouched (194/194).
