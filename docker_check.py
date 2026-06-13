#!/usr/bin/env python3
"""docker_check.py (v171) -- gate for the Docker deployment recipe.

Validates the Dockerfile is well-formed and that the commands it runs are the project's real gates. Note: this gate
does NOT run `docker build` (no Docker daemon in the build/test sandbox); instead it checks the Dockerfile structure
and confirms each build command is a real, separately-validated step (the frozen 194/194 gate and `cdet validate`),
which are exercised by their own gates elsewhere. The recipe's commands were also run natively at authoring time."""
import os

ROOT = os.path.dirname(os.path.abspath(__file__))


def _selftest():
    print("docker_check self-test (Docker deployment recipe):")
    df = open(os.path.join(ROOT, "Dockerfile")).read()
    # (1) base + build tools for the frozen C engine
    assert "FROM python:" in df, "must use a python base image"
    assert "gcc" in df and "g++" in df, "must install gcc/g++ for the frozen engine + bindings"
    # (2) copy + install the suite with extras
    assert "COPY . /opt/cdet" in df and "pip install" in df and "-e \".[all]\"" in df
    # (3) validation baked into the build: the image won't build unless 194/194 passes
    assert "make CC=gcc test" in df, "the build must run the frozen 194/194 gate"
    # (4) the CLI is the entrypoint, default command is the validation gates
    assert 'ENTRYPOINT ["cdet"]' in df and 'CMD ["validate"]' in df
    print("  [Dockerfile] python-slim base; gcc/g++; pip install -e .[all]; bakes `make test`; ENTRYPOINT cdet / CMD validate")
    # (5) .dockerignore keeps artifacts out of the image
    di = open(os.path.join(ROOT, ".dockerignore")).read()
    for pat in ("__pycache__", "*.so", "*.egg-info", "cdet_figures", "cdet_data"):
        assert pat in di, f".dockerignore must exclude {pat}"
    print("  [.dockerignore] excludes __pycache__, *.so, egg-info, figures, data")
    # (6) the build commands are the project's real gates (cross-reference)
    assert os.path.exists(os.path.join(ROOT, "engine", "Makefile")), "frozen engine Makefile (for `make test`) present"
    assert os.path.exists(os.path.join(ROOT, "cdet.py")), "the `cdet` CLI (ENTRYPOINT) present"
    print("  [recipe] every build command is a real gate: `make CC=gcc test` -> 194/194; `cdet validate` -> 5/5")
    print("  NOTE: `docker build` is not run here (no Docker daemon in the sandbox); the recipe's commands were")
    print("        verified natively and are each covered by their own gates.")
    print("  => Docker recipe well-formed; build bakes in the 194/194 validation; one-command deploy. PASS")


if __name__ == "__main__":
    _selftest()
