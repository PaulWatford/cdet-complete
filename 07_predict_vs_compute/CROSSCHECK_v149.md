# CROSSCHECK_v149 — the idiot-proof conversational front-end (cdet_shell.py)

**Claims.** (1) `cdet_shell.py` is a two-state (HOME/CONFIRM) conversational shell over `cdet_lab`: plain language
→ interpreted command shown back (all defaults visible) → confirm yes/no → run on yes. (2) 'no' reverts to HOME
but keeps the named/saved configuration library. (3) Intelligence on imperfect input: synonyms (mott→hubbard-i,
density→eos), typo-robust resolution, did-you-mean + example syntax on unrecognized input or unknown methods.
(4) Named configs: save/run/forget/configs, surviving reverts. (5) Thin safe layer — the (target,method) map is
imported from `cdet_lab` (single source of truth); every run routes through `cdet_lab`, frozen reference untouched.
Design grounded in clig.dev CLI best practices (conversation, discoverability, empathy).

**Reproduce.** `cd 08_2d_interacting && python3 cdet_shell.py --selftest` (14-step scripted session); interactive:
`python3 cdet_shell.py` then `help`.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
