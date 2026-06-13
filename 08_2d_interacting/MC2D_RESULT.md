# 2D high-order Monte Carlo: validated vs exact ED, and the sign-problem wall measured (v37)

v36 reached orders 1,2 in 2D by deterministic quadrature. v37 builds the high-order Monte-Carlo driver
for 2D and does two things: proves it correct against exact diagonalization at orders 3-6 (beyond
quadrature's practical reach), then measures WHERE the variance wall -- the fermion sign problem -- is.

## The driver
mc2d.c generalizes engine_exp/diagmc.c (which hardwires the 1D hexring) to ANY lattice: it takes a
prebuilt LatticeCtx + site count N and samples n internal (site,tau) vertices uniformly, averaging the
geometry-blind C_V. Estimator cdet_order(n) = N*(N*beta)^n/n! * mean(C_V) -> N*a_n. It also reports the
sign-cancellation ratio R = mean(C_V)/mean(|C_V|), an intrinsic measure needing no exact answer.

## (1) Correctness -- MC reproduces exact ED coefficients, orders 1-6 (2x2, beta=4, mu=0.5, tau=0.5)
Exact a_n from diagonalization via the Cauchy contour integral (hubbard_ed.exact_coeffs, r-independent
to 1e-13). Reproducible gate (mc_validate.py, ~70 s):

   n      MC estimate     stderr      exact N*a_n    sigma
   1      -0.5796135    0.000923    -0.5789477     0.72
   2      -0.4669807    0.001258    -0.4662779     0.56
   3       0.1383506    0.001165     0.1366135     1.49
   4       0.4713411    0.002769     0.4669114     1.60
   5       0.2214447    0.003824     0.2144823     1.82
   6      -0.2463949    0.007863    -0.2466214     0.03

Every order agrees within <2 sigma. Orders 5,6 are out of reach for the deterministic nested quadrature
(np^n ~ 64^5..64^6 = 1e9..7e10 time-points times the site sums); the MC reaches them and lands on the
exact answer. That is the milestone: the 2D MC machinery is correct at orders deterministic quadrature
cannot practically reach, anchored on exact diagonalization. (Higher-statistics single runs confirm the
same, e.g. n=6 at 8e5: -0.2408719 +/- 0.0027689 vs -0.2466214, 2.1 sigma.)

## (2) The wall -- where the sign problem appears (order 3; R = |mean|/mean|abs|; Nsamp->1% = cost for 1% rel.err)
Cluster-size sweep (beta=4):                Temperature sweep (3x3):
   cluster  N    |R|    Nsamp->1%              beta   |R|    Nsamp->1%
   2x2      4   0.342    7.0e5                  2    0.085    2.5e7
   3x2      6   0.079    9.0e6                  4    0.079    1.1e8
   3x3      9   0.079    1.1e8                  6    0.049    1.4e9
   4x4     16   0.047    1.8e8                  8    0.025    1.4e10

Reading it honestly: on the 2x2 the sign is benign (1% precision in ~7e5 samples). Growing the cluster
to 4x4 raises that cost ~260x; dropping the temperature on 3x3 from beta=2 to beta=8 raises it ~570x.
|R| collapses and the cost to reach fixed precision explodes roughly geometrically in both system size
and inverse temperature -- the signature of the fermion sign problem. This is the actual difficulty of
2D Hubbard, now quantified rather than asserted.

## Honest scope -- what is and is NOT established
IS: a 2D high-order connected-determinant MC driver, validated against exact diagonalization at orders
1-6; and a quantitative map of the sign-problem wall vs cluster size and temperature.
IS NOT: beating the sign problem. Reaching order 6 on the 2x2 is a CORRECTNESS result -- the 2x2 has
essentially no sign problem -- not a demonstration of solving large/cold systems. We measured the wall;
we did not move it. Also NOT done: a head-to-head "CDet vs a naive conventional expansion" variance
comparison (that needs a naive-expansion baseline implemented); so no claim is made that CDet reaches
higher order than a conventional expansion -- only that this CDet MC is correct and that the wall sits
where the table says. Overcoming the wall (variance reduction that beats the 1/R^2 scaling -- the CVAR
mode with a genuine analytic-mean reference, or importance sampling, or a different estimator) is the
open frontier; that is where 2D Hubbard physics actually begins.
