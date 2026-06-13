# CROSSCHECK_v150 — blind usability test + hardening of cdet_shell.py

**Claims.** Used the shell as a zero-knowledge user; found and fixed six real issues: (1) the confirm step was a
trap (cancel/back/help/quit looped — couldn't quit) → all now escape, quit works from any state; (2) N/n
case-collision (N=0 set vertices too) → case-sensitive; (3) no validation (SU(0) ran, U=abc dropped silently) →
reject + warn; (4) synonym substring bug ('ed' inside 'connected') → word-boundary scan; (5) rigid confirm
phrasing → intent-based yes/no; (6) menu/"what can you do" → help. Verdict: not possible to get stuck, always a
labeled way back to start, logical, understandable, powerful.

**Reproduce.** `cd 08_2d_interacting && python3 cdet_shell.py --selftest` (21 steps).

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
