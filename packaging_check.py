#!/usr/bin/env python3
"""packaging_check.py (v167) -- gate for the packaging/CI scaffolding.

Verifies the distribution-readiness pieces are present and coherent: a valid pyproject.toml that declares the `cdet`
console entry point and runtime dependencies, a CI workflow that runs the frozen 194/194 gate and `cdet validate`, a
LICENSE, and an importable entry point. This is the gate that keeps the packaging honest."""
import os
import sys

ROOT = os.path.dirname(os.path.abspath(__file__))


def _load_toml(path):
    try:
        import tomllib
        return tomllib.load(open(path, "rb"))
    except ModuleNotFoundError:                # py<3.11
        import tomli
        return tomli.load(open(path, "rb"))


def _selftest():
    print("packaging_check self-test (distribution-readiness scaffolding):")
    # (1) pyproject valid + entry point + deps
    d = _load_toml(os.path.join(ROOT, "pyproject.toml"))
    proj = d["project"]
    assert proj["scripts"]["cdet"] == "cdet:main", proj["scripts"]
    assert any("numpy" in dep for dep in proj["dependencies"]), proj["dependencies"]
    assert "viz" in proj["optional-dependencies"] and "rich" in proj["optional-dependencies"]
    print(f"  [pyproject] name={proj['name']} v{proj['version']}; entry `cdet`=cdet:main; deps={proj['dependencies']}")
    # (2) entry point resolves
    if ROOT not in sys.path:
        sys.path.insert(0, ROOT)
    import cdet as _cdet
    assert callable(_cdet.main), "entry point cdet:main must be callable"
    print("  [entry] `cdet:main` imports and is callable")
    # (3) CI workflow runs the right gates
    ci = open(os.path.join(ROOT, ".github", "workflows", "ci.yml")).read()
    assert "make CC=gcc test" in ci and "cdet validate" in ci, "CI must run the frozen gate and cdet validate"
    assert "--selftest" in ci
    print("  [CI] workflow runs the frozen 194/194 gate, `cdet validate`, module + CLI self-tests")
    # (4) dual license present: PolyForm Noncommercial (free academic) + commercial offer
    lic = open(os.path.join(ROOT, "LICENSE")).read()
    assert "PolyForm Noncommercial License 1.0.0" in lic and "DUAL LICENSE" in lic, "LICENSE must be the dual license"
    assert "educational institution" in lic, "academic use must be explicitly free"
    assert os.path.exists(os.path.join(ROOT, "COMMERCIAL-LICENSE.md")), "commercial license terms must be present"
    print("  [license] dual license: free for academic/noncommercial (PolyForm NC 1.0.0) + commercial offer")
    print("  => packaging coherent: `pip install -e .` gives a working `cdet`; CI enforces the validation gates. PASS")


if __name__ == "__main__":
    _selftest()
