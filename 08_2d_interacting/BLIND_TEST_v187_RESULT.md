# Blind usability test as a first-year student (v187)

I installed and used the package from a clean unzip, reading only what a new user sees and following the on-ramp
literally — no insider knowledge — to find where a first-year learning lattice work gets stuck.

**What already works (a student succeeds).** The README "Try this first" block is a clean on-ramp; `make CC=gcc test` →
194/194; `./cdet validate` → a 5/5 dashboard; `./cdet converge` → a clear thermodynamic-limit table with a plain-language
takeaway; and bare `./cdet eos`, `./cdet wall`, `./cdet docc` all run with no flags, each ending in a one-line
explanation. Good for learning.

**Friction found, and fixed:**

1. **QUICKSTART contradicted the README's front door.** README points to `./cdet validate/converge/gui` and the
   assistant; QUICKSTART step 1 said `make test` (no `CC=gcc`), never mentioned `./cdet` or the GUI/assistant, and steered
   the student into low-level `cdet_lab.py`/`cdet_shell.py` plus a researcher-only "What to show Möller" section.
   *Fix:* added a "Start here (the friendly on-ramp)" block at the top of QUICKSTART (the four `./cdet` commands, the
   assistant, bare-command tip, and the `CC=gcc` note), and relabeled the Möller section "(Researchers)".

2. **Assistant beginner gaps.** It was strong on specific terms (beta, wall) but failed the naive questions a real
   first-year asks:
   - "what should I run first" → returned the *heavy* `cdet run` (the word "run" collided).
   - "what is the hubbard model" → returned the three-**model** *architecture*.
   - "what is a lattice / exact diagonalization / monte carlo" → no foundational concept; confusing matches.
   - "I'm a first year / what do I do / I don't understand" → bounced to a disambiguation instead of the on-ramp.
   *Fix:* added a **beginner-SOS intent** (new / lost / "what do I do" / "what should I run first" / "I don't understand"
   → the getting-started path directly, no flags), and four **foundational concepts** — lattice, Hubbard model, exact
   diagonalization, Monte Carlo — each a short beginner-level explanation that points to the right command. These also
   resolve the keyword collisions.

3. **Minor:** refreshed a stale `cdet info` row ("local browser console" → "browser front-end over the CLI (+ optional
   assistant)").

**Verified.** Every failing question above now answers correctly, live through `/api/assist`; the specific-term answers
are unchanged (no regressions); the assistant self-test grew to 14 query + 6 behaviour checks and passes; 13 concepts now.
Docs/help only — no physics changed; assistant still offline and runs nothing; GUI still the pure CLI wrapper; frozen
engine untouched (194/194). `cdet_assistant.py`, `QUICKSTART.md`, `cdet.py`.
