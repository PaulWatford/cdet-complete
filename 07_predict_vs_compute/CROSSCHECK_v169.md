# CROSSCHECK_v169 — data export (CSV/JSON/HDF5)

**Claims.** (1) `export.py` exports five validated observables (convergence, resummation, eos, docc, chi) to CSV, JSON,
and HDF5. (2) Each dataset is reproduced from the gated code paths, so files cannot drift from the numbers. (3) CSV+JSON
are stdlib (always available); HDF5 is optional (h5py). (4) The self-test round-trips every dataset (write, read back,
numeric match). (5) Wired as `cdet export`; frozen engine untouched.

**Reproduce.**
```
cd 08_2d_interacting && PYTHONPATH=. python3 export.py     # gate (round-trips all datasets)
python3 cdet.py export docc --format all                   # CSV + JSON + HDF5
```

**Frozen engine.** Untouched: `cd engine && make CC=gcc test` → 194/194; constants bit-identical
(−0.5082750022348369  0.44040518398732875).
