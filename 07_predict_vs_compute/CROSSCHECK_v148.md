# CROSSCHECK_v148 — the unified end-to-end model (cdet_lab.py control plane)

**Claims.** (1) `cdet_lab.py` exposes every capability as swappable components from the terminal via three
orthogonal choices: `--target` {eos, self-energy, addition-pole, double-occ, connected-det} × `--method` {ed,
record, hubbard-i, diagrammatic, surrogate, hybrid, fast-minors, engine} × `--model`/params. (2) The
(target,method) map is enforced (undefined combos rejected). (3) The design is grounded in a web search of
physicist needs (SU(N) EoS ⟨n⟩(μ), DMFT self-energy with Hubbard-I rational Σ for the Mott regime, DiagMC
observables). (4) The frozen reference is not touched; `validate` runs the three-model health gate.

**Reproduce.** `cd 08_2d_interacting && python3 cdet_lab.py` (self-test, 5 components); `python3 cdet_lab.py list`;
`python3 cdet_lab.py validate`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
