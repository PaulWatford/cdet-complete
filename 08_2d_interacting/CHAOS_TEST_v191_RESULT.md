# Adversarial "chaos" console test — break it like a cat on the keyboard (v191)

I hammered the console blind with every malformed, absurd, hostile, and nonsensical input I could think of: garbage
subcommands, unicode, keyboard mash, missing/typo'd flag values, injection payloads, absurd numbers, and huge inputs.

**Held up gracefully (no fix needed).** argparse rejects unknown subcommands, bad choices, and non-numeric flag values
with clean one-line errors and exit code 2 — no tracebacks. Shell-injection payloads are inert: the CLI never invokes a
shell, and both the CLI (`type=float`) and the GUI (per-flag casters + an allow-list) reject `1;rm -rf /`, `$(whoami)`,
and backticks as "invalid number". The GUI returns clean JSON errors (`{"error": "--U expects a number"}`,
`{"error": "unknown command: hackme"}`) for hostile input, HTTP 200, nothing executed.

**Real problems found, and fixed (all in `cdet.py`):**
1. **`cdet diagmc --nmax 99999` hung the console** — each order runs the ~2^n connected-determinant recursion, so a huge
   order count is a self-inflicted denial of service. Now `--nmax` is capped at 8 (with a note) and floored at 1.
2. **`cdet sweep` with a huge value list hung** — `--values $(seq 1 500)` ran until timeout. Now the point count is capped
   at 60 (with a note) and the sweep carries a 120 s time budget, so it always stops gracefully with a recorded reason
   instead of hanging.
3. **`cdet diagmc --samples 0` / `--nmax 0` produced nan** — averaging an empty sample set. `--samples` is now floored at
   100 and `--nmax` at 1, each with a note.
4. **`cdet diagmc --beta nan|inf`, `--U inf`, `--beta 0`** silently produced garbage. Now they return a clean
   "beta, mu and U must be finite numbers" / "beta must be positive" error.

**Noted, not bugs.** `cdet plot --out PATH` treats `PATH` as an output *directory* (it writes `cdet_summary.png` inside);
mildly surprising but intentional. argparse rejects negative scientific notation as a bare value (`--mu -1e5`); use the
equals form `--mu=-1e5` (a standard argparse behaviour, not specific to this tool).

**Verified.** Normal use is unchanged (diagmc, sweep, validate, the frozen 194/194 all still pass); the previously-hanging
inputs now return in well under a second with a friendly note; no physics changed; frozen reference engine untouched.
`cdet.py`.
