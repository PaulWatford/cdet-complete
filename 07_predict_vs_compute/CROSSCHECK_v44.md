# Cross-check (v44) — literature map: the v36–v43 findings are documented, connected facets of one sign problem

This is a LITERATURE iteration (no new computation); the "check" is mapping each prior result onto published
work. See 08_2d_interacting/LITERATURE_MAP.md and the chat synthesis for citations.

## Mapping (finding -> anchor -> verdict)
- v38 CDet order-reach (det removes per-order cancellation; exp(order) not factorial) -> Rossi PRL 119,
  045701 (2017), the founding CDet property. Reproduces the method's defining claim. Not novel.
- v37 sign wall (cost ~ 1/<s>^2; <s> ~ e^{-aN} e^{-b beta}) -> standard DQMC scaling <s> ~ e^{-alpha beta t L^2}
  (arXiv 2509.18075; e^{-aN},e^{-b beta} verified arXiv 2112.09209; Troyer-Wiese NP-hardness). Not novel.
- v41 R organized by Fermi-shell detuning, peaks at closed shell, oscillates with N -> "Deconvolving the
  components of the sign problem" (arXiv 2108.00553): sign peaks at closed-shell "magic densities", oscillates
  vs mu, strengthens at low T. Also closed-shell sign effects + compressibility-tracks-sign (arXiv 1107.0230).
  This is the documented closed-shell effect, rediscovered per-order. Not novel.
- v42/v43 near-shell width ~ T (order-dependent; thermal origin underdetermined) -> compressibility tracks the
  sign and carries the Fermi thermal width (arXiv 1107.0230); sign <-> quantum criticality (Science 375, 418
  (2022)). My v43 "finite-size shell/thermal artifact, not universal" matches the literature. Not novel.
- v36 convergence radius ~0.5-1, poles -> Hubbard-atom convergence radius = distance to complex-coupling pole
  (Wu-Ferrero-Georges-Kozik PRB 96, 041105 (2017)); weak-U convergence -> large-U divergence from complex-U
  poles (arXiv 2303.01607). Matches known analytic structure. Not novel.

## Conclusion
The "separate walls" were never unrelated in the literature: "Geometry Dependence of the Sign Problem"
(arXiv 1501.02832) already collates <S> vs beta,N,density,geometry, and Science 2022 ties the sign to quantum
criticality. This program is a transparent, exactly-validated INDEPENDENT REDISCOVERY of mapped structure --
worth is validation + methodology record, not discovery. Candidate residue (stated weakly, "did not find",
not "is new"): the per-ORDER coefficient's qualitatively different delta-structure by order (v43 Test A).

## Honesty
No new numerics. All prior CROSSCHECK_v5..v43 results stand. This iteration only recontextualizes them
against published work and explicitly DEFLATES any novelty read of the program.
