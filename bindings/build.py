#!/usr/bin/env python3
"""build.py -- compile the optional native bindings (cdet_core) against the FROZEN engine (read-only).

Opt-in performance feature: the pure-python install needs no compiler; this builds a native extension so Python can
call the frozen engine's primitives directly (no subprocess). Run: python bindings/build.py"""
import os
import subprocess
import sys
import sysconfig

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENGINE = os.path.join(ROOT, "engine")
LAT = os.path.join(ROOT, "05_2d_lattice")
OUT = os.path.join(ROOT, "bindings")


def build():
    import pybind11
    suffix = sysconfig.get_config_var("EXT_SUFFIX") or ".so"
    obj = "/tmp/_cdet_bind_obj"
    os.makedirs(obj, exist_ok=True)
    # frozen engine + lattices compiled as C (gcc), unmodified
    subprocess.run(["gcc", "-O2", "-fPIC", "-I", ENGINE, "-c",
                    os.path.join(ENGINE, "cdet_engine.c"), "-o", os.path.join(obj, "engine.o")], check=True)
    subprocess.run(["gcc", "-O2", "-fPIC", "-I", LAT, "-I", ENGINE, "-c",
                    os.path.join(LAT, "lattices.c"), "-o", os.path.join(obj, "lattices.o")], check=True)
    so = os.path.join(OUT, "cdet_core" + suffix)
    subprocess.run(["g++", "-O2", "-shared", "-std=c++14", "-fPIC",
                    "-I", pybind11.get_include(), "-I", LAT, "-I", ENGINE] +
                   [s for s in sysconfig.get_config_var("INCLUDEPY").split() if s] * 0 +
                   ["-I", sysconfig.get_path("include"),
                    os.path.join(OUT, "cdet_core.cpp"), os.path.join(obj, "engine.o"), os.path.join(obj, "lattices.o"),
                    "-o", so], check=True)
    return so


if __name__ == "__main__":
    p = build()
    print("built:", p)
