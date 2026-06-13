# CROSSCHECK_v168 — dual license (free academic, paid commercial)

**Claims.** (1) LICENSE is a dual license: the PolyForm Noncommercial License 1.0.0 (free for any noncommercial
purpose, with educational institutions and public research organizations explicitly permitted) + a commercial license
for business use. (2) COMMERCIAL-LICENSE.md describes the commercial grant and contact. (3) pyproject points license to
the LICENSE file with an Other/Proprietary classifier. (4) The package still installs and `cdet validate` is 5/5. (5)
`packaging_check.py` verifies the dual license. (6) Frozen engine untouched.

**Reproduce.**
```
PYTHONPATH=. python3 packaging_check.py        # gate (checks the dual license)
pip install -e . && cdet validate              # still 5/5
```

**Note.** The dual-license structure is standard but not legal advice; a real commercial offering should be
lawyer-reviewed and the contact/pricing filled in.

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
