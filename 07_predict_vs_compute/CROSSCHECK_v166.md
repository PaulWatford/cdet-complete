# CROSSCHECK_v166 — built-in visualization

**Claims.** (1) `plots.py` renders four figures (convergence, resummation, mott, summary) via matplotlib Agg. (2) Each
is built from the validated code paths (plane-wave G0, sun_eos_conformal, double_occupancy, susceptibilities), so it
cannot drift from the numbers; the python convergence G0_NN matches the validated C path to round-off. (3) Wired as
`cdet plot`. (4) Frozen engine not involved.

**Reproduce.**
```
cd 08_2d_interacting && PYTHONPATH=. python3 plots.py     # gate (writes 4 PNGs to /tmp/_cdet_plots)
python3 cdet.py plot summary                              # the dashboard
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
