# Blind usability test of `cdet_shell.py` — findings and hardening (v150)

I used the shell as a zero-knowledge user would: typing vague, wrong, impatient, and contradictory things, and
actively trying to get stuck or lose my way back to the start. The test found six real problems; all are fixed and
regression-guarded in the self-test (now 21 scripted steps).

## What the blind test found

| # | problem | how it showed up | severity |
|---|---|---|---|
| 1 | **Confirm step was a trap** | at the yes/no prompt, `cancel`, `back`, `help`, and even `quit` all looped on "Please answer yes or no" — the only exits were `no` or ctrl-D | **high** (couldn't even quit) |
| 2 | **N-vs-n collision** | `N=0` set *both* flavors and vertices to 0 (both lowercase to "n") | medium (silent wrong config) |
| 3 | **No validation** | `N=0` ran as nonsensical SU(0); `U=abc` was silently dropped | medium |
| 4 | **Synonym substring bug** | "connected determinant" picked method `ed` because "ed" matched inside "connect**ed**" | medium (wrong solver) |
| 5 | **Rigid confirm phrasing** | "actually nevermind" / "no thanks" were ignored (only exact "no" worked) | low |
| 6 | **Dead-end first contact** | `menu` / "what can you do" didn't route to help | low |

## The fixes

1. **Confirm is no longer a trap.** `yes/no` now match by intent (first word + keyword), so "yes please",
   "no thanks", "actually nevermind", "cancel", "back", "stop", "abort" all work. `quit`/`exit` leave the shell
   from any state. `help` at the confirm step explains the options. The fallback message names every escape, and
   if the user types a *new request* mid-confirm, the shell explains how to switch instead of stonewalling.
2. **Case-correct parsing.** `N` (flavors) and `n` (vertices) are parsed case-sensitively, ending the collision;
   the other parameters stay case-insensitive.
3. **Validation + warnings.** Out-of-range values are rejected with a fix ("N must be ≥ 1; try N=6"); a
   non-numeric assignment like `U=abc` produces a clear warning and is dropped rather than silently ignored.
4. **Word-boundary synonyms.** Synonym matching now respects word boundaries, so short tokens like "ed" no longer
   match inside other words.
5. **Lenient confirm intent** (as in 1).
6. **Friendly first contact.** `menu`, `options`, `commands`, "what can you do" all route to help; a stray
   `yes`/`no` at the home prompt gets a gentle "nothing is pending" rather than a confusing parse error.

## Verdict against the criteria

- **Possible to get stuck?** No longer. Every state has labeled exits; `quit` always works; no input loops without
  offering a way out.
- **Easy to get back to start?** Yes — `no`, `cancel`, `back`, `stop`, "nevermind" all revert, and the saved
  configuration library survives the revert.
- **Logical?** Yes — one consistent loop: describe → see the exact command → confirm → result.
- **Easy to understand?** Yes — plain-language input, every assumed default shown, errors that suggest the fix.
- **Powerful?** Yes — the full control plane is reachable: every observable × solver, named/saved configs,
  the validation health gate, and the frozen-reference anchor underneath.

Reproduce the regression suite: `python3 cdet_shell.py --selftest` (21 steps). The frozen engine is untouched
(194/194); every run still routes through `cdet_lab`.
