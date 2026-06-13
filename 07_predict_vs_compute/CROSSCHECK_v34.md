# Cross-check (v34) — the improvements, wired as switchable configurations (and a discrepancy chased down)

v33 ended with the honest admission that the acceleration ideas were standalone POCs, not options on
the solver. v34 wires the validated ones into one configurable driver, and — prompted by a real
discrepancy that surfaced during validation — pins down that the MC estimator and the deterministic
quadrature genuinely agree across the parameter space. The frozen baseline (engine/) is untouched;
everything lives in engine_exp/. Reproduce: engine_exp/cdet_config_validate.c.

## The interface
engine_exp/cdet_config.{h,c}: `cdet_order_mc_cfg(n, L, beta, mu, t, tau_out, tau_in, nmc, seed, cfg,
*err)` with `cfg->mode`:
- CDET_PLAIN   -- the v27 estimator, unchanged.
- CDET_BLOCKED -- per-sample C_V via the v31 out-of-core bit-split blocking (RAM bounded to ~3*2^nL
  doubles, the 2^n array on disk); for n so large a single flat C_V overflows RAM.
- CDET_CVAR    -- control variate: subtract a correlated shifted-mu reference C_V, mean from an
  independent pilot. Unbiased; reports rho and the variance reduction.
The butterfly / fast-subset-convolution POC is deliberately NOT wired (shelved v29: wrong trade).

## Gates (all pass; engine_exp/cdet_config_validate.c)
1. CDET_PLAIN is BIT-IDENTICAL to cdet_order_mc at n=1,2,3 (value and error bar) -- the wrapper does
   not perturb the reference path.
2. CDET_BLOCKED == PLAIN at n=8 (same seed) to rel.diff 1.1e-12 -- the out-of-core path reproduces the
   in-RAM estimate (the blocked arithmetic is the exact direct sum, matching flat C_V to ~1e-20).
3. CDET_CVAR is UNBIASED: 1.46 sigma (n=1) / 0.16 sigma (n=2) from the frozen baseline.
4. MC estimator == deterministic cdet_order across TWO parameter sets and n=1,2: agreement 1.84 / 0.29
   / 0.91 / 0.41 sigma. This gate is new in v34 (see below).

## The honest CVAR result (net = 1x, and why)
The control variate is correct, but its realized benefit is the key finding. The per-sample correlation
is high (rho = 0.98 at n=1, 0.92 at n=2), so the POTENTIAL reduction 1/(1-rho^2) is 27x / 6.5x -- **but
only if E[Y] is known exactly**. With E[Y] estimated by a Monte-Carlo pilot, the pilot's own variance
(beta^2 * Var(Y)/P) reintroduces almost exactly the variance the correlation removed, so the measured
NET reduction is 1.00x. The returned error bar includes this pilot term (an earlier draft omitted it and
produced a spurious "7.6 sigma bias" -- it was an undercounted error, not a bias). Conclusion, now
quantified end-to-end: the control variate net-wins only with an ANALYTIC reference mean -- the
atomic-counterterm / learned Luttinger-liquid-G reference flagged in v30/v33. The CVAR mode is the
correct plumbing waiting for it (drop a known E[Y] in and the 6-27x becomes real).

## The discrepancy that was chased down (and the fix)
During validation the MC estimator and cdet_order appeared to disagree wildly at one parameter choice
(tau_out=1.5, tau_in=0.5): MC gave ~0.18 at n=1, cdet_order gave ~-0.83. Run to ground:
- ROOT CAUSE: integrate_piecewise_1d/2d (quad.c) declared the Gauss-Legendre node/weight arrays as fixed
  `double nodes[64]` etc. gl_grid_1d(np,...) writes np entries, so np>64 OVERFLOWS THE STACK -- silent
  corruption, then an abort. I had evaluated cdet_order at np=120 (in the corrupt regime); the -0.83 was
  garbage, never a real cdet_order value.
- NO REAL DISCREPANCY: at safe np the quadrature is converged from np=8 upward (identical to 12 digits),
  and the MC matches it at BOTH parameter sets and n=1,2 (gate 4: <1 sigma at 20M samples). The MC and
  cdet_order compute the same integral; their prefactors coincide algebraically (MC n=1 expectation =
  L * sum_s integral C_V dtau = cdet_order n=1), and both call C_V with the same (0,tau_out,0,tau_in).
- FIX (v34, engine_exp only): quad.c now sizes nodes/wts (1d) and n1/w1/n2/w2 (2d) to np, removing the
  np>64 overflow. Bit-identical for np<=64 (C_V n=8,12,16 and cdet_order(1,2) unchanged to the last
  digit; engine_exp still 194/194); cdet_order now also runs correctly for np>64 (np=48,64,96 give the
  same converged value). engine/ is left frozen and still carries the original fixed buffers.
- CORRECTION to my earlier v34 wording: it is NOT "only safe at the designed np=40." It is safe and
  converged for every np up to the buffer size, and now (sandbox) for all np. np=40 was never special.

## Second correction (rigorous-honesty)
v33 stated blocked_cv "still has the known h=0 bug." That was WRONG: the h=0 guard was fixed back in
v31, and the blocked path reproduces flat C_V to ~1e-20 (n=12,16,18) -- re-confirmed here and wired as
CDET_BLOCKED with no fix needed.

## Status
VALIDATED (v34): the validated accelerations are switchable configurations on one driver
(cdet_order_mc_cfg): PLAIN (bit-identical), BLOCKED (out-of-core, exact to 1.1e-12), CVAR (unbiased).
CVAR honestly nets 1x with an MC-estimated reference mean -- correct plumbing awaiting an analytic E[Y].
Butterfly excluded by design. The MC<->cdet_order agreement is now a standing gate across params (gate
4). The np>64 quadrature overflow is FIXED in the sandbox; the apparent MC/cdet_order discrepancy it
caused was an artifact, not a real disagreement.
Open: (a) build the analytic-mean reference (atomic counterterm / learned-G) so CVAR's 6-27x becomes
net; (b) push BLOCKED to huge n on real disk; (c) carry the quad.c np fix into engine/ at the next
deliberate baseline refresh (kept frozen for now).
