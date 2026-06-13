# Literature map: the v36-v43 "separate walls" are documented, connected facets of one sign problem (v44)

A hard literature search on each phenomenon this program turned up. Honest headline: almost everything here
is known, much of it is explicitly connected in the literature, and the finding that felt most original
(R organized by Fermi-shell detuning) is a documented "closed-shell / magic-density" effect. This program
is a faithful, independent REDISCOVERY of known structure on a small cluster -- valuable as validation and
as a methodology record, not as new physics. Sources are cited in the chat synthesis accompanying this file.

## Finding-by-finding

1. v38 -- "CDet buys order reach: determinant removes per-order cancellation; cost ~ exp(order) not (order)!".
   ANCHOR: Rossi, Phys. Rev. Lett. 119, 045701 (2017), the founding connected-determinant paper -- the
   determinant produces massive inter-diagram cancellation and turns factorial cost into exponential-in-order.
   VERDICT: faithful reproduction of the method's DEFINING property. Not novel; it is the reason CDet exists.

2. v37 -- "sign wall: MC cost ~ 1/<s>^2, with <s> ~ exp(-aN)*exp(-b*beta)".
   ANCHOR: textbook DQMC sign scaling. <s> ~ e^{-alpha*beta*t*L^2} (pseudogap Hubbard quantum-simulator
   companion, arXiv 2509.18075); <sign> ∝ e^{-aN} (L>11) and ∝ e^{-b*beta} (beta>4) verified in a
   Gross-Neveu QMC study (arXiv 2112.09209); Troyer-Wiese NP-hardness (2005). VERDICT: reproduces the
   standard volume*beta exponential. Not novel.

3. v41 -- "R is organized by the Fermi-shell detuning delta; peaks when a shell sits at the Fermi level;
   oscillates with finite-size shell structure" (the result that felt most original).
   ANCHOR (bullseye): "Deconvolving the components of the sign problem" (arXiv 2108.00553) reports the
   average sign peaking at "magic densities" tied to CLOSED-SHELL fillings, with oscillations vs mu that
   strengthen as temperature drops and whose peaks sit at the closed-shell densities. Also "Finite-size
   effects in transport data from QMC" (arXiv 1107.0230): closed-shell effects from artificial finite-lattice
   gaps, and the compressibility TRACKS the average sign. VERDICT: this is the documented closed-shell /
   magic-density effect, rediscovered at the per-order coefficient level. Not novel -- but a clean independent
   rediscovery.

4. v42/v43 -- "near-shell feature width ~ T (thermal), but order-dependent; thermal origin underdetermined".
   ANCHOR: the compressibility tracks the sign (arXiv 1107.0230), and the compressibility's width at a shell
   crossing IS the Fermi-function thermal width ~ T -- so the order-2 thermal width is the expected
   shell-crossing/compressibility scale, a finite-size artifact, not a universal law. The deeper framing:
   sign suppression is quantitatively linked to quantum criticality / the pseudogap (Mondaini, Tarat,
   Scalettar, Science 375, 418 (2022)). VERDICT: my own v43 narrowing (it is a finite-size shell/thermal
   artifact, not a universal mechanism) is the literature's view. Consistent; not novel.

5. v36 -- "convergence radius ~ 0.5-1 in U from a contour-integral coefficient extraction; poles".
   ANCHOR: Wu, Ferrero, Georges, Kozik, Phys. Rev. B 96, 041105 (2017) compute, for the Hubbard atom, the
   series convergence radius as the distance to the nearest POLE in the complex-coupling plane, with the pole
   set by mu, n, beta. arXiv 2303.01607: weak-U exponential CDet convergence turns to divergence at large U
   from complex-U poles, leaving U/t~8, T/t~0.1 prohibited. VERDICT: matches the known analytic structure.
   Not novel. (Related caution: Kozik et al, Phys. Rev. Lett. 114, 156402 (2015) -- skeleton series can
   converge to the WRONG answer; bare-series convergence is not automatic.)

## The meta-point: these were never unrelated in the literature
The axes I treated as separate "walls" -- order, size N, temperature beta, filling/shell, coupling radius --
are recognized as facets of ONE sign problem, and at least two works explicitly unify them: "Geometry
Dependence of the Sign Problem" (arXiv 1501.02832) collates <S> vs beta, N, density, and geometry that were
"scattered through the literature"; and the Science 2022 paper ties the sign quantitatively to quantum
criticality. So the right honest statement is not "I connected unrelated cases" but "I independently
re-derived, on a 4-16-site cluster, structure that the DiagMC/DQMC community has already mapped and
connected." The program's worth is as a transparent, exactly-validated re-derivation and a methodology
record (how to avoid fooling yourself: anchor on exact limits, separate density from temperature, run the
order-cutoff control), not as a discovery.

## What is least obviously documented (candidate residue, stated weakly)
The per-ORDER coefficient's delta-structure being qualitatively DIFFERENT at each order (v43 Test A: n=1
monotonic, n=2 peak at delta=0, n=3 peak at +0.2 with opposite sign below the shell) is a finer-grained
statement than the closed-shell magic-density picture for the FULL average sign. It is plausibly implicit in
the coefficient-level analyses (e.g. the controllable-series / pole-moving work) but I did not find it stated
per-order in these terms. This is offered as "did not find," NOT "is new"; the honest next step is to read
the per-order coefficient literature (CDet self-energy coefficient studies) before any originality claim.


## CoS / external-method map (v131, from Gunnar Moller)
- Kozik, Nat. Commun. 15 (2024), 'Combinatorial summation of Feynman diagrams' (CoS): the dynamic-programming
  successor to CDet; sums connected diagrams via [l,h,e]+record-R graph, O(n^3 3^n) SU(2) / O(n^3 4^n) SU(N)
  N-independent / O(n^2 2^n) ordered. Our engine = the Rossi special case. See COS_PROTOTYPE_RESULT.md.
- Simkovic & Kozik, PRB 100, 121102(R) (2019): CDet for the self-energy (irreducible diagrams), O(n^3 2^n)+O(3^n).
- Frankenbach et al., PRR 7, 043032 (2025): QTT compression of 4-point vertices (DMFT+parquet) -- adjacent, parked.
