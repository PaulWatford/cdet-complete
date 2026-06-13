# What the z-flow actually measures: the single-particle addition pole (v133)

The crux question: does z(∞)=lowest-empty-level encode a **real spectral observable**, or is it only an
internal property of our frozen construction? The answer is the former, and the proof chain was already
present in pieces — this consolidates it and states the bound.

## The mapping

**z(∞) is the leading single-particle addition pole** — the energy of the lowest unoccupied single-particle
excitation above the Fermi sea. Three established links close the chain:

1. **z(∞) = ε_probe.** z(β) = ε_probe + ln(s\*)/β with s\* = A/|c1| (ZINF_RESULT.md, v111); the ln β/β
   approach sends z → ε_probe, the lowest-empty level.
2. **It tracks a *moving* pole.** As L grows the lowest-empty level sweeps 2.0 → √2 → 1.268 → 1.082 →
   1.0002 (v125), and z(∞) follows it in every case (dev ≤ 4e-7 here). A constant cannot do that — z is a
   *detector* of a pole whose position it reports.
3. **Why it is a pole.** The v78 cancellation lemma (FUGACITY_STRUCTURE_RESULT.md) proves ⟨C⟩(μ) is
   *exactly* a rational function of the fugacity e^{βμ}, with poles **only** at μ = ε_k — the Matsubara
   comb anchored at the single-particle levels. `fugacity_structure.py` detected that pole directly (a
   3.9×10⁶-fold rise approaching the comb). The deep-β z-flow is a real-axis extraction of the nearest such
   pole above the sea, i.e. the lowest-empty level.

So z(∞) is the single-particle addition spectrum's leading pole — the same object DiagMC reconstructs by
analytic continuation. It is a standard, real spectral observable.

## The honest bound — and why it points straight at integration #3

The fugacity poles sit at the **bare** levels ε_k, because the propagator g0 carries the free spectrum.
So **z(∞) is currently the FREE addition energy.** The interacting addition energy ε_k + ReΣ(ε_k) requires
the self-energy resummation that shifts the poles — which is exactly **integration #3** (the Šimkovic–Kozik
irreducible/self-energy series). z and #3 are therefore the same physical target at two resummation levels:
#3 turns the free addition spectrum z(∞) measures today into the interacting one.

That is the concrete payoff of pinning the mapping: it converts "port the self-energy algorithm" from a
generic upgrade into *the* step that makes our own observable a physical, interacting spectral quantity on
the Hubbard model — and it does so without undoing anything (the free z-flow remains exactly what it is, the
Σ=0 limit).

## Status

Verified: z(∞) == the single-particle addition pole across all measured cases (worst dev 4e-7), and the pole
sweeps 1.0002…2.0 with z tracking it. Links to fugacity_structure.py (pole↔level) and ZINF/thermo_limit
(the flow and the sweep). Reproduce: `python3 physical_mapping.py`. Frozen engine untouched (194/194).
