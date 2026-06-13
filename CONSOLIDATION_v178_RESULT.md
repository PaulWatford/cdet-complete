# Consolidation v178: a single index for the whole package

**What.** Consolidate all files and docs. The package had grown to ~647 files (127 RESULT findings, 176 CROSSCHECK
records, a 145-entry ledger, the frozen engine, the wall suite) with **no top-level map**. Added `INDEX.md`: the single
authoritative entry point that catalogs the three-model architecture, the directory map, all 19 CLI subcommands, the two
arcs (the elevation checklist v163–171 and the wall-physics arc v172–177), and where each kind of knowledge lives
(ledger / RESULTs / CROSSCHECKs / benchmark note).

**Doc consistency.** README now lists the full wall suite including `trueradius` (was missing) and points to `INDEX.md`;
QUICKSTART (build-and-verify) remains current. Verified: every file reference in INDEX/README resolves to a real file;
all 19 CLI subcommands are documented in the INDEX; no broken references or orphans anywhere; strings clean.

**Verified consistent (post-consolidation).** `cdet validate` 5/5; frozen engine 194/194; surrogate worst dev 3.55e-15;
orphan scan clean across all docs. Frozen reference engine untouched.

**Navigation map.**
- `INDEX.md` — the map (start here).
- `QUICKSTART.md` — build and verify in minutes.
- `README.md` — the CLI and feature overview.
- `real_patterns_v178.md` — the ledger (#1…#188).
- `*_RESULT.md` (127) — the findings; `07_predict_vs_compute/CROSSCHECK_v*.md` (176) — the predictions.
