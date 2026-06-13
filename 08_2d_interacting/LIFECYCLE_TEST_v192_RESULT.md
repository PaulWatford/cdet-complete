# Blind lifecycle test: pausing, interrupting, restarting, walking away (v192)

I used the program the way a real, distractible user does: Ctrl-C in the middle of runs, killing processes, restarting the
server while the old one was still up, walking away and coming back, and impatiently re-running things.

**Already robust (no fix needed).** Ctrl-C (SIGINT) on any CLI command prints a clean "interrupted." and exits 130 -- no
KeyboardInterrupt traceback (the top-level handler catches it). The browser console is stateless per request, so walking
away and coming back just works; it shuts down cleanly on Ctrl-C ("stopped."). The on-disk SU(N) series cache already
tolerates a corrupt/half-written file on read (falls back and recomputes), so an interrupted write never crashes a later
run.

**Real fragilities found, and fixed:**
1. **An interrupted `cdet sweep` lost all its work.** `data.csv`/`summary.json` were written only after the whole sweep
   finished, and the `run.log` buffer was never flushed -- so Ctrl-C (or a kill, or the laptop sleeping) threw away every
   point already computed. *Fixed:* `data.csv` is now written and flushed point-by-point, the log flushes on every line,
   and an interrupt is caught so the run still finalizes `summary.json` with a clear stop reason
   ("interrupted by user (Ctrl-C) after k of n points"). Verified: interrupting a 6-point sweep after one point leaves
   that point in `data.csv` and a correct stop reason -- partial work is preserved and labelled.
2. **Restarting the console while the old one was still running dumped an ugly traceback** --
   `OSError: [Errno 98] Address already in use`. A very common "did I already start it?" mistake. *Fixed:* the server now
   probes the requested port and the next nine, opens on the first free one with a note ("port 8811 was busy ... using
   8812 instead"), and if all are busy prints a friendly message pointing at the likely-running console or `--port`.
3. **The cache write was not atomic.** *Fixed:* it now writes a temp file and `os.replace`s it into place, so an interrupt
   mid-write can neither corrupt the cache nor destroy a previously-good one.

**Verified.** Normal use is unchanged (sweep completes and archives data.csv/summary.json/plot.png/run.log; validate 5/5;
frozen 194/194; diagmc and the surrogate gate still pass). No physics changed; the frozen reference engine is untouched.
`cdet_study.py`, `cdet_gui.py`, `cdet.py`.
