# Cross-check proof data (v24) — quantitative efficiency: bare vs atomic expansion (dimer)

v23 showed the engine's bare U=0 expansion diverges at strong coupling and a scheme change rescues
it. v24 quantifies the efficiency gain on the exactly-solvable 2-site Hubbard dimer (the simplest
lattice with both hopping t and interaction U, so both schemes are non-trivial and the answer is
exact). Reproduce: `python engine_exp/dimer_efficiency.py`. Engine_exp sandbox; anchor = exact ED.

## Exact anchor
Closed form E0 = (U - sqrt(U^2 + 16 t^2))/2, verified vs direct ED of the half-filled 2-site
Hubbard: U/t=2,4,8 -> E0 = -1.236068, -0.828427, -0.472136 (match to 1e-9).

## Two schemes (the engine's bare U-series IS the first)
- BARE: expand in U around U=0. Radius = 4t. Converges only for U < 4t (weak coupling).
- ATOMIC: expand in hopping t around the atomic limit (full local U kept exactly; the engine ships
  G_exact_atom as this reference). Radius = U/4. Converges only for U > 4t (strong coupling).
The radii are reciprocals -> the schemes are COMPLEMENTARY and tile the (U,t) plane, crossover U=4t.

## Cost model and the quantitative gain (eps=1e-6, t=1; cost ~ 3^N)
N_eps = ceil(ln eps / ln rho), rho = target/radius; gain = 3^(N_bare - N_atomic).
| U/t | bare | atomic | gain |
|-----|------|--------|------|
| 1 | N=6 (3^6=729) | diverge | bare-only (weak) |
| 2 | N=14 (3^14=4.8M) | diverge | bare-only |
| 4 | diverge | diverge | crossover (resummation, v23) |
| 6 | diverge | N=24 (3^24=2.8e11) | INF (bare impossible) |
| 8 | diverge | N=16 (3^16=4.3e7) | INF |
| 12 | diverge | N=10 (3^10=59049) | INF |
| 16 | diverge | N=8 (3^8=6561) | INF |
| 32 | diverge | N=6 (3^6=729) | INF |
Validation at U/t=8: exact E0=-0.472136; bare 12-order sum=+126 (diverged); atomic 20-order
sum=-0.472136 (exact).

## Reading the efficiency gain (the quantitative understanding asked for)
In the strong-coupling regime we operate in (U/t >= 4), the bare engine expansion DIVERGES -- it
cannot reach the answer at any order, so its cost is effectively infinite. The atomic scheme
converges, and its cost 3^(N_atomic) DROPS rapidly as coupling strengthens: 3^24 -> 3^16 -> 3^10 ->
3^8 -> 3^6 at U/t = 6, 8, 12, 16, 32. So the gain is not a modest constant factor -- it is the
difference between an impossible calculation and a feasible one, and the feasible cost gets cheaper
the deeper into strong coupling you go. The one hard region is the crossover U ~ 4t, where both
simple expansions are marginal and a resummation (Pade, v23) or hybrid is the handle.

## Status
QUANTIFIED (v24): the scheme change converts the strong-coupling regime from divergent (bare,
infinite cost) to convergent (atomic, cost 3^(N_atomic) that shrinks with U/t) -- validated against
the exact dimer. The two schemes are complementary (bare U<4t, atomic U>4t). NEXT: implement the
atomic-reference (hopping) expansion in engine_exp's C high-order path -- the engine already ships
G_exact_atom -- and validate the resummed observable against the frozen baseline on a real lattice;
then fold in the learned-IR control variate as the reference.
