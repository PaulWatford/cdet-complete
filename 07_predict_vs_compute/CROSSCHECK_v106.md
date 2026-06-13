# CROSSCHECK_v106 — the uploaded gravity-loop resummation, assessed and adapted for the deep-β tail

**Claims.** (1) The gravity-loop closed-form resummation (linear recurrence → rational generating
function → dominant-root asymptote) transfers to the deep-β series because A(β), ⟨C⟩(β) are finite
sums of exponentials over the spectrum (xi_k = level_k − μ), hence linear-recurrent on a uniform
β-grid — directly targeting the v105 high-β ill-conditioning. (2) Free-rate Prony is
noise-sensitive (spurious roots on the noisier naive data); the fix is the exact-integer L=6
spectrum → known rates → well-posed amplitude-only linear fit (χ²=0.75/2 on clean stable
A(β)=1.328(217)/0.357(125)/0.119(28)/0.051(23) at β=24/32/40/48). (3) The asymptote target is
z(∞) = 2 − (ρ_A − ρ_c1); the tool resolves it once A(β) and c1(β) are both measured clean. (4)
Boundary: it does not address the MC heavy tail (α≈1.06, statistical — median-of-means stays) or
move the wall; fwverify's two-route + MPFR-30-digit pattern confirms the v103 mpmath certifier.

**Reproduce.** `cd 08_2d_interacting && python3 deep_beta_resummation.py` (channels; known-rate
well-posed; free-rate contrast; extrapolation; PASS ~5 s).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
