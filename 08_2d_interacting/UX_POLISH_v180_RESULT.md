# UX polish v180: addressing a blind-user review

A reviewer exercised the CLI as a new user and flagged concrete usability gaps. Each actionable item is addressed; the
underlying engine and physics are untouched (this is interface polish, not a change to what the tool computes).

| review finding | fix |
|---|---|
| `cdet run` needs several options / unfriendly when missing | bare `cdet run` now works — the upper β resolves to one `--bstep` above `--beta`; a "customize:" line shows the full invocation |
| no progress bar on longer sweeps | `cdet sweep` prints per-point progress `[i/n] var=… ` (via a new `progress` hook in `study()`); `--verbose` still gives full detail |
| sweep / lab / run want more examples | each now has a worked-examples epilog in `--help` |
| natural-language shell sometimes fails | added synonyms (number density, occupancy, doublons, cdet, …); the "couldn't tell" message now points to `examples` and `help` |
| new user may wander into old oracle folders | README gained a "Try this first" block and an explicit note that the numbered folders are internals behind `./cdet` |

**Verified unchanged after polish:** `cdet validate` 5/5; frozen engine 194/194; surrogate 3.55e-15; `cdet converge`
still reaches 100×100 instantly; the shell menu/examples/parse paths work. Frozen reference engine untouched.

**Honest scope.** These are usability improvements that make the tool smoother for an expert user — the reviewer's
"commercial-viable for experts" is a *usability* judgment. They do not change the tool's standing as a validated,
pedagogical CDet implementation that reproduces known physics; they make it nicer to drive.
