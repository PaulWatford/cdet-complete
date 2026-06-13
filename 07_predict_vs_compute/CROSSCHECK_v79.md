# CROSSCHECK_v79 — the consolidated surrogate

**Claims.** (1) cdet_surrogate.py integrates, with verified scope stated at the point of use:
wrap-safe sector identification (v75 group-invariant definition; recognizes wrap-collinear lines),
the transferable magnitude model (v74 features, L=4 calibration, 8-shot line intercept), the r_pred
regime map (v74: +0.32/+0.27/−0.57 by rank — the surrogate reports the regime), and the
period-based orientation channel (v77 law Δμ\*=π/(qβ) with the v78 comb mechanism; at-the-bar
scoping). (2) BEST_METHODS.md gains the v79 edition: component table, the phase program's closed
arc (observed → irreducible in geometry → law in (μ,β) → mechanism in the complex plane), nine
methodology rules earned since v65, and the unchanged walls restated (R(N,β) still decays
exponentially; nothing crosses the sign problem). (3) Integration-as-audit refinements: the
transfer error is pooled **1.88×** across two independent declared-mixture draws (1.74×/2.69× —
the v74 1.81× sat at the favorable end of draw spread); a per-class-intercept hypothesis was
tested and **rejected** (line/bulk offsets differ by 0.16 ln units; bulk offsets noisier).

**Reproduce.** `cd 08_2d_interacting && python3 cdet_surrogate.py` → wrap-sector recognition,
two-draw pooled transfer gate ≤2.6×, orientation gates, integrated report;
"consolidated-surrogate self-test ... PASS" (~1–2 min). Component provenance: SHELL_FOLD,
SURROGATE2, MU_PERIOD, FUGACITY_STRUCTURE result docs.

**Scope (honest).** n=3, cubic lattices, β-window per component; the orientation channel remains
at the bar (73–76% across seeds), included with that label; draw-to-draw transfer spread is now
part of the banked number.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
