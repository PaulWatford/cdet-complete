# An optional, self-contained help assistant (v185)

**What.** A toggle-on **assistant** panel in the console (top-right `assistant` button). The user types a question or an
intent; it answers in plain language, suggests the exact commands to try (clickable chips that copy), and points to the
docs. It works alongside QUICKSTART/README/INDEX — it does not replace them, and it never runs anything for you.

**Honest about the technology.** This is **not** an LLM. Bundling a real model (Llama/Mistral via Ollama/GPT4All) would
add 2–7 GB to the package and run slowly on CPU — the wrong trade for a help assistant. Instead `cdet_assistant.py` is a
**rule-based knowledge graph**: 21 commands, 9 physics concepts, and 6 workflows, with a keyword matcher. It is fully
offline, has no dependencies, no downloads, and responds instantly. It gives AI-style, conversational answers without any
inference — and it stays correct, because every command and concept in it corresponds to something real in the package.

**What it knows.** Every subcommand (what it does, its parameters, an example, related commands); the physics (the sign
problem, CDet, the wall and U_c, the true/thermal radius, resummation, Mott physics, the thermodynamic limit, the
three-model architecture, the parameters β/μ/U/N/L); and workflows (getting started, computing observables, the wall
study, lattice runs, learning the method, exporting data). The matcher weights specific multi-word phrases over generic
ones, recognises command names, greetings, and "what can you do", and falls back gracefully.

**Design.** A slide-in panel, hidden by default (purely optional, as asked). Chat bubbles; bot replies render light
markdown and a row of suggested-command chips that copy to the clipboard. Same instrument palette as the console.

**Verified.** The module's 10-query self-test passes (start, the wall, CDet, double occupancy, true radius, parameters,
a bare command, export, capabilities, and a nonsense fallback), and every command example is a real command. Through the
server, `/api/assist` returns sensible answers with relevant command chips; the page carries the toggle and panel; the
panel is hidden until toggled. The GUI remains a pure CLI wrapper; the assistant adds no physics and runs nothing.
Frozen reference engine untouched (194/194). `cdet_assistant.py`, panel in `cdet_gui.py`.
