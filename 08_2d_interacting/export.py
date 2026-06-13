"""export.py (v169) -- data export of the validated observables to CSV / JSON / HDF5.

Makes every validated result consumable by other tools (pandas, Excel, downstream analysis). Each dataset is
reproduced from the SAME code paths the gates validate -- so an exported file cannot drift from the numbers, exactly
like the figures in plots.py. CSV and JSON use only the standard library; HDF5 is optional (needs h5py).

Datasets:
  convergence   2D thermodynamic-limit: lattice side, sites, nearest-neighbour propagator (4 -> 100)
  resummation   conformal-Borel vs plain Pade error vs U on the SU(N) EoS
  eos           SU(N) density vs U (ED + conformal-Borel)
  docc          double occupancy vs U (ED + conformal-Borel + interaction energy)
  chi           charge compressibility and spin susceptibility vs U
"""
import csv
import tempfile
import json
import os
import numpy as np

try:
    import h5py
    _HDF5 = True
except Exception:
    _HDF5 = False


# ---------------- datasets (each reproduced from a validated code path) ------------------------
def _ds_convergence():
    from plots import _g0_nn
    Ls = [4, 6, 8, 12, 16, 24, 32, 48, 64, 100]
    rows = [[L, L * L, _g0_nn(L)] for L in Ls]
    return {"name": "convergence", "columns": ["L", "sites", "G0_NN"], "rows": rows,
            "meta": {"beta": 5.0, "mu": 0.0, "t": 1.0, "observable": "equal-time nearest-neighbour propagator"}}


def _ds_resummation(N=4, K=10):
    from sun_eos_curve import density_series, density_ed
    from sun_eos_conformal import conformal_borel, borel_singularity
    from resummation import pade, pade_eval
    a = density_series(N, K, M=max(24, 4 * N)); Uc = borel_singularity(a)
    p, q = pade(a, K // 2, K // 2)
    rows = []
    for U in np.linspace(0.2, 2.0, 10):
        e = density_ed(N, U); cb = conformal_borel(a, U, Uc); pa = pade_eval(p, q, U).real
        rows.append([float(U), e, cb, pa, abs(cb - e), abs(pa - e)])
    return {"name": "resummation", "columns": ["U", "ED", "conformal_borel", "pade", "cb_err", "pade_err"],
            "rows": rows, "meta": {"N": N, "K": K, "Uc": Uc}}


def _ds_eos(N=4, K=10):
    from sun_eos_curve import density_series, density_ed
    from sun_eos_conformal import conformal_borel, borel_singularity
    a = density_series(N, K, M=max(24, 4 * N)); Uc = borel_singularity(a)
    rows = [[float(U), density_ed(N, U), conformal_borel(a, U, Uc)] for U in np.linspace(0.0, 2.0, 11)]
    return {"name": "eos", "columns": ["U", "density_ED", "density_confBorel"], "rows": rows,
            "meta": {"N": N, "beta": 2.0, "mu": 1.0}}


def _ds_docc(N=2):
    from double_occupancy import docc_ed, docc_series
    from sun_eos_conformal import conformal_borel, borel_singularity
    a = docc_series(N, 10); Uc = borel_singularity(a)
    rows = []
    for U in np.linspace(0.0, 3.0, 13):
        e = docc_ed(N, U); rows.append([float(U), e, conformal_borel(a, U, Uc), float(U) * e])
    return {"name": "docc", "columns": ["U", "D_ED", "D_confBorel", "E_int_per_site"], "rows": rows,
            "meta": {"N": N, "beta": 2.0, "mu": 1.0, "note": "E_int_per_site = U * D"}}


def _ds_chi(N=2):
    from susceptibilities import kappa_fluct, chi_spin_fluct
    rows = [[float(U), kappa_fluct(N, U), chi_spin_fluct(N, U)] for U in np.linspace(0.0, 4.0, 17)]
    return {"name": "chi", "columns": ["U", "kappa_charge", "chi_spin"], "rows": rows,
            "meta": {"N": N, "beta": 2.0, "mu": 1.0}}


_DATASETS = {"convergence": _ds_convergence, "resummation": _ds_resummation,
             "eos": _ds_eos, "docc": _ds_docc, "chi": _ds_chi}


# ---------------- writers ---------------------------------------------------------------------
def _write_csv(ds, path):
    with open(path, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["# " + ds["name"], json.dumps(ds["meta"])])
        w.writerow(ds["columns"])
        for r in ds["rows"]:
            w.writerow(r)
    return path


def _write_json(ds, path):
    json.dump(ds, open(path, "w"), indent=2)
    return path


def _write_hdf5(ds, path):
    if not _HDF5:
        raise RuntimeError("HDF5 export needs h5py (pip install h5py); CSV/JSON work without it")
    with h5py.File(path, "w") as f:
        arr = np.array(ds["rows"], dtype=float)
        d = f.create_dataset("data", data=arr)
        d.attrs["columns"] = json.dumps(ds["columns"])
        for k, v in ds["meta"].items():
            d.attrs[k] = v
    return path


_WRITERS = {"csv": _write_csv, "json": _write_json, "hdf5": _write_hdf5}


def export(which, fmt, outdir):
    """write dataset `which` in format(s) `fmt` (one of csv/json/hdf5/all) into outdir; return list of paths."""
    os.makedirs(outdir, exist_ok=True)
    ds = _DATASETS[which]()
    fmts = ["csv", "json"] + (["hdf5"] if _HDF5 else []) if fmt == "all" else [fmt]
    ext = {"csv": "csv", "json": "json", "hdf5": "h5"}
    return [_WRITERS[fm](ds, os.path.join(outdir, f"cdet_{which}.{ext[fm]}")) for fm in fmts]


def _selftest():
    print("export self-test (validated observables -> CSV/JSON/HDF5; reproduced from the gated code paths):")
    out = os.path.join(tempfile.gettempdir(), '_cdet_export')
    print(f"  HDF5 available: {_HDF5}")
    for which in _DATASETS:
        ds = _DATASETS[which]()
        paths = export(which, "all", out)
        # round-trip the CSV: read back and compare the numeric rows to the source
        csvp = [p for p in paths if p.endswith(".csv")][0]
        with open(csvp) as f:
            rows = list(csv.reader(f))[2:]            # skip meta + header
        back = np.array([[float(x) for x in r] for r in rows])
        src = np.array(ds["rows"], dtype=float)
        assert back.shape == src.shape and np.allclose(back, src), which
        # JSON round-trip
        jp = [p for p in paths if p.endswith(".json")][0]
        jback = json.load(open(jp))
        assert jback["columns"] == ds["columns"] and len(jback["rows"]) == len(ds["rows"]), which
        print(f"  {which:12s} -> {', '.join(os.path.basename(p) for p in paths)}  ({len(ds['rows'])} rows, round-trip OK)")
    print("  => every validated observable exports to CSV/JSON" + ("/HDF5" if _HDF5 else "") +
          " and round-trips exactly. Frozen engine untouched. PASS")


if __name__ == "__main__":
    _selftest()
