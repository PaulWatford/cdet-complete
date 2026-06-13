# GUI: a recent-runs memory (v183)

**Recent strip.** The console now keeps a small memory of your explicit runs. A `recent` strip above the cards shows the
last few (up to 8) as chips — card name, the slider values used, and the result (e.g. `wall L24 β5 μ0 → 1.975`). Click a
chip to restore those sliders and re-run. A `clear` link empties it. State lives server-side, so it survives a page
refresh within the session.

Design choices that keep it honest and unobtrusive:
- **Only explicit Run clicks are remembered.** Run sends `&log=1`; the Live auto-reruns (on slider drag) do not, so the
  memory reflects what you chose to run, not every twitch of a slider.
- **Consecutive identical configs collapse** (no duplicate chips), and the buffer caps at 8.
- Physical-limit cards (wall, true radius) show their value in amber, matching the readouts.

**Bug fixed along the way (a real one, from v181).** The sweep cards rebuilt their trace by calling the 2-site ED
repeatedly, and that ED scales steeply with N: instant to N=4 (0.09 s), 3.3 s at N=5, and effectively hangs at N≥6. With
the N slider going to 8, a single click could wedge the request for a minute. Fixed by capping the GUI's N at 4 (where
every run is sub-second) and trimming the sweeps to 11 points; the API clamps N≤4 server-side too. Larger SU(N) is still
available from the terminal via each card's copy-as-CLI command (where the cached-series path handles it) — a clean split:
the GUI is for instant interactive runs, the CLI for the heavier cached ones. A hint on the rail says so.

**Verified (server up, then down).** Three explicit runs recorded most-recent-first; a repeated config dedupes; an
unlogged live rerun is not recorded; clear empties it; the page carries the strip and wiring. Routes are now sub-second
even when N is requested high (clamped): eos 0.94 s, chi 0.26 s. Front-end only; no new physics. Frozen reference engine
untouched (194/194). `cdet_gui.py`.
