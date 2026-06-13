# CROSSCHECK_v189 — connected-determinant Monte Carlo (the sign wall, measured)

**Claims.** (1) cdet_diagmc.py samples the connected-determinant series with the validated cdet_connected kernel and
reproduces exact ln(Z/Z0) within error bars (per-order coeffs, summed observable, and a grand-canonical Metropolis walk).
(2) it measures the sign problem as the across-order series <s>=|sum a_n U^n|/sum|a_n|U^n collapsing toward the radius
(cost ~1/<s>^2). (3) it does NOT defeat the sign problem; order bounded by 2^n; validated on atom+2-site. (4) frozen
engine untouched.

**Reproduce.**
```
python3 08_2d_interacting/cdet_diagmc.py --selftest    # all checks PASS (~49s)
./cdet diagmc --system atom --U 1.5                     # MC coeffs + ln(Z/Z0) vs exact + the sign-wall scan
./cdet diagmc --system 2site --beta 3 --mu 0.5 --U 1
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
