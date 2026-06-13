# Assistant upgraded with chatbot best practices (v186)

I researched how production help-chatbots are built (intent matching, fallback design, fuzzy/typo tolerance,
disambiguation, UX) and applied the well-established techniques to the existing assistant. It stays exactly what it was —
**self-contained, offline, rule-based, runs nothing** — but the matcher and the conversation UX are much better. No model,
no inference, no new dependencies (Python standard library only: `difflib`, `math`, `re`).

**What changed, and the practice behind each:**
- **Relevance scoring, not raw keyword counts.** Queries are scored across a unified pool of commands, concepts, and
  workflows with **idf term-importance** — distinctive words (occupancy, susceptibility, radius) outweigh common ones,
  stopwords are dropped, and multi-word phrases get a bonus. (TF-IDF-style ranking; "score = similarity × term importance".)
- **Typo tolerance.** Near-miss words are matched by edit distance via `difflib` ("explain the wal" → wall; a misspelled
  command → "Did you mean **cdet wall**?"), plus light stemming so "started"→"start", "occupancy" matches "occupancy".
- **Confidence gating + disambiguation.** When one topic clearly leads, it answers; when two are genuinely close, it asks
  *"Did you mean X or Y?"* with tap-to-pick options instead of guessing — the single most-cited fix in the fallback
  literature.
- **Closest-match fallback.** An unrecognised query no longer gets a generic "not sure"; it surfaces the nearest topics as
  suggestions to recover from, rather than a dead end.
- **Intent signals.** An action verb (compute, run, measure) biases toward the actionable command; a definitional phrasing
  (*what is…*, *what does … mean*) biases toward the concept.
- **A forward path on every reply.** Each answer now returns tappable **quick-replies** (related topics, "what do its
  parameters mean?", "how do I start?"), and the welcome offers starter prompts — keeping the user moving.
- **Lightweight follow-up memory.** The panel threads the last topic as context, so "tell me more", "an example", or
  "what are the parameters" expand on what you just asked, without any server-side session state.

**Honest scope.** This is a better *help layer*, grounded in cited best practices — not a language model and not a change
to any physics. The assistant still imports no physics, runs nothing, and works alongside the docs. The GUI underneath is
still the pure CLI wrapper; the frozen reference engine is untouched (194/194).

**Verified.** Self-test extended to 10 query checks + 6 behaviour checks (typo tolerance, keyword intent, fallback
suggestions, forward path, follow-up via context, intent bias) — all pass. Live `/api/assist` returns the new
`suggestions` and `topic` fields; the panel renders quick-reply chips and threads context for follow-ups. `cdet_assistant.py`,
`cdet_gui.py`.
