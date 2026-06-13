"""csurrogate.py (v86) -- the gate module for THE CORE C SURROGATE (csurrogate.c/h). The C module
carries every banked advance -- the 10-feature transferable magnitude model (v74/v79), the
wrap-safe sector test (v75), the thermal period law (v77/v78), the regime classifier (v80), the
Class-I logit-law flips from residue-polynomial roots (v81/v83), the Class-II static with its flow
correction (v82/v84), and orientation parity stepping (v77/v85) -- frozen into dependency-free C
beside (never inside) the frozen engine.

THE GATE (run as main): parse the frozen parameters from csurrogate_params.h; generate FRESH
reference configs (new seed per run); compute features / ln-magnitude / sector in Python (the
frozen linear model, classify_true_rank1) and the atlas references live (residue_ratio,
selection_rule); regenerate csurrogate_refs.h; rebuild csurrogate_test with gcc; demand the
engine-style line "ALL CASES MATCH THE PYTHON REFERENCE TO 1e-09". Regenerating the trained
parameters themselves (retraining, seeds 130/131) is the documented --regen path.
"""
import re, json, subprocess, sys
import numpy as np
from surrogate2 import feats2
from shell_fold import line_masks, classify_true_rank1
import residue_ratio as rq
import selection_rule as sr

GID = {"124": 0, "135": 1, "123": 2}


def load_params(path="csurrogate_params.h"):
    t = open(path).read()
    arr = lambda name: np.array([float(x) for x in
                                 re.search(name + r"\[[0-9]*\]\s*=\s*\{([^}]*)\}", t).group(1).split(",")])
    sca = lambda name: float(re.search(name + r"\s*=\s*([-0-9.eE+]+)", t).group(1))
    return {"w": arr("SURR_W"), "mu": arr("SURR_MU"), "sd": arr("SURR_SD"),
            "off6": sca("SURR_OFF_L6"), "off4": sca("SURR_OFF_L4")}


def py_lnmag(sites, L, P):
    z = (np.array(feats2(sites, L)) - P["mu"]) / P["sd"]
    return float(np.r_[1.0, z] @ P["w"] + (P["off6"] if L == 6 else P["off4"]))


def gen_refs(seed, path="csurrogate_refs.h"):
    P = load_params()
    rng = np.random.default_rng(seed)
    rows = []
    for L in (6, 4):
        M = line_masks(L); N = L ** 3
        cfgs = [[1, 2, 3], [int(5 + 6) , int(3 + 18), int(4 + 12)] if L == 6 else [5, 10, 15]]
        while len(cfgs) < 14:
            c = sorted(int(x) for x in rng.choice(np.arange(1, N), 3, replace=False))
            if len(set(c)) == 3:
                cfgs.append(c)
        for c in cfgs:
            sec = int(bool(classify_true_rank1(np.array([c], dtype=int), M)[0]))
            rows.append((L, c, [float(x) for x in feats2(c, L)], py_lnmag(c, L, P), sec))
    z = sr.direct_zero(sr.OFFS, sr.V_POS, sr.MID_POS)
    K = 2 * sr.BETA0 * (z - sr.MID_POS)
    c1 = [(GID[g], float(b), 1 + np.log(r[0] / (1 - r[0])) / b, 1 + np.log(r[1] / (1 - r[1])) / b)
          for g, r in rq.ROOTS.items() for b in (12, 16, 20, 24, 28)]
    st = [(float(b), sr.MID_POS + K / (2 * b)) for b in (12, 16, 20, 24)]
    fmt = lambda x: f"{x:.17g}"
    lines = ["/* csurrogate_refs.h -- GENERATED Python reference vectors (csurrogate.py) */",
             "#ifndef CSURROGATE_REFS_H", "#define CSURROGATE_REFS_H",
             f"#define NREF {len(rows)}",
             "static const int REF_L[NREF] = {" + ", ".join(str(r[0]) for r in rows) + "};",
             "static const int REF_SITES[NREF][3] = {" + ", ".join("{%d,%d,%d}" % tuple(r[1]) for r in rows) + "};",
             "static const double REF_FEATS[NREF][10] = {"]
    for r in rows:
        lines.append("  {" + ", ".join(fmt(x) for x in r[2]) + "},")
    lines += ["};",
              "static const double REF_LNMAG[NREF] = {" + ", ".join(fmt(r[3]) for r in rows) + "};",
              "static const int REF_SECTOR[NREF] = {" + ", ".join(str(r[4]) for r in rows) + "};",
              f"#define NC1 {len(c1)}",
              "static const int    C1_G[NC1] = {" + ", ".join(str(x[0]) for x in c1) + "};",
              "static const double C1_B[NC1] = {" + ", ".join(fmt(x[1]) for x in c1) + "};",
              "static const double C1_LO[NC1] = {" + ", ".join(fmt(x[2]) for x in c1) + "};",
              "static const double C1_HI[NC1] = {" + ", ".join(fmt(x[3]) for x in c1) + "};",
              f"#define NST {len(st)}",
              "static const double ST_B[NST] = {" + ", ".join(fmt(x[0]) for x in st) + "};",
              "static const double ST_V[NST] = {" + ", ".join(fmt(x[1]) for x in st) + "};",
              "#endif"]
    open(path, "w").write("\n".join(lines) + "\n")
    return len(rows), len(c1), len(st)


def build_and_run():
    subprocess.run(["gcc", "-O2", "-Wall", "-Werror", "-o", "/dev/shm/csur_test",
                    "csurrogate_test.c", "csurrogate.c", "-lm"], check=True)
    out = subprocess.run(["/dev/shm/csur_test"], capture_output=True, text=True)
    return out.stdout.strip(), out.returncode


def _selftest():
    seed = int(np.random.default_rng().integers(1, 10 ** 6))   # FRESH configs every run
    n = gen_refs(seed)
    print(f"fresh reference vectors (seed {seed}): {n[0]} configs, {n[1]} class-1, {n[2]} statics")
    out, rc = build_and_run()
    print(out)
    ok = rc == 0 and "ALL CASES MATCH THE PYTHON REFERENCE TO 1e-09" in out
    print("c-surrogate gate (fresh refs; build -Wall -Werror; engine-style match):",
          "PASS" if ok else "FAIL")
    return ok


if __name__ == "__main__":
    _selftest()
